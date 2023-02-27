from abc import abstractmethod
import copy
from datetime import datetime
from enum import Enum
import os
import shutil
from types import NoneType
from BBData.Delegate import Delegate
from BBData import config
from BBData.Fields import Checks, Field, FieldType, LongText, Radio, ShortText, parseField
from BBData.FileSystem import Tree, TreeNode
from BBData.utilities import currentTime, first, getDuration, getFilesWithExtension, loadJsonLike
from dictdiffer import diff
import json
from typing import Callable, Union
import uuid
import warnings


class CollectionElement(TreeNode):

    def diff(elementA, elementB):
        '''
        Diff elements

        Args:
            elementA (CollectionElement): Original Element
            elementB (CollectionElement): New Element

        Returns:
            list: List of changes
        '''
        return list(diff(elementA.toDict(), elementB.toDict()))

    def fromDict(inDict: dict):
        '''
        Creates Collection Element from dict

        Args:
            inDict (dict): Dictionary to parse

        Returns:
            CollectionElement: Element
        '''
        e = CollectionElement()

        # Identifiers
        e.uuid = inDict['uuid']

        # Fields are used to denote public and private fields
        e.public = [parseField(serializedField)
                    for serializedField in inDict['public']]
        e.private = [parseField(serializedField)
                     for serializedField in inDict['private']]

        # Time tracking
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        return e

    def copy(element):
        '''
        Create a copy of an element

        Args:
            element (CollectionElement): Element to copy

        Returns:
            CollectionElement: Copied Element
        '''
        e = CollectionElement.fromDict(element.toDict())
        e.uuid = str(uuid.uuid4())
        return copy.deepcopy(e)

    def serialize(self):
        pass

    def __init__(self, tree, parent=None) -> None:
        id = str(uuid.uuid4())
        # Identifiers
        self.uuid = id
        super().__init__(id, tree, parent)

        # Public fields are shown in views, private are only shown in panels and accessable by plugins.
        self.public: list[Field] = []
        self.private: list[Field] = []

        # Time tracking
        self.createDate = currentTime()
        self.updateDate = self.createDate

        # Delegate
        self.attributeChanged = Delegate()

    def addPublicField(self, field: Field):
        self.public.append(field)
        field.fieldChanged.connect(
            lambda changedField: self.attributeChanged.emit(self, changedField))
        self.attributeChanged.emit(self, field)

    def addPublicFields(self, fields: list[Field]):
        [self.addPublicField(field) for field in fields]

    def addPrivateField(self, field: Field):
        self.private.append(field)
        field.fieldChanged.connect(
            lambda changedField: self.attributeChanged.emit(self, changedField))
        self.attributeChanged.emit(self, field)

    def addPrivateFields(self, fields: list[Field]):
        [self.addPrivateField(field) for field in fields]

    def removePublicField(self, index: Union[str, int]):
        if isinstance(index, int):
            target = self.public[index]
        else:
            target = [field for field in self.public if field.name == index][0]
        target.fieldChanged.disconnect(
            lambda changedField: self.attributeChanged.emit(self, changedField))
        self.public.remove(target)

    def removePrivateField(self, index: Union[str, int]):
        if isinstance(index, int):
            target = self.private[index]
        else:
            target = [field for field in self.private if field.name == index][0]
        target.fieldChanged.disconnect(
            lambda changedField: self.attributeChanged.emit(self, changedField))
        self.private.remove(target)

    def getPublicField(self, search: Union[str, int]):
        if isinstance(search, int):
            return self.public[search]
        else:
            return first([field for field in self.public if field.name == search])

    def getPrivateField(self, search: Union[str, int]):
        if isinstance(search, int):
            return self.private[search]
        else:
            return first([field for field in self.private if field.name == search])

    def toDict(self) -> dict:
        '''
        Serialize to dict

        Returns:
            dict: serialized dict
        '''
        d = {}
        d['uuid'] = str(self.uuid)
        d['public'] = [field.toDict() for field in self.public]
        d['private'] = [field.toDict() for field in self.private]
        d['createDate'] = self.createDate
        d['updateDate'] = self.updateDate
        return d

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        strrep = f'{self.uuid}\n{self.getPath()}\nPublic Fields:\n'
        for field in [self.getPublicField(i) for i in range(len(self.public))]:
            strrep += f'{str(field)}\n'
        strrep += 'Private Fields:\n'
        for field in [self.getPrivateField(i) for i in range(len(self.private))]:
            strrep += f'{str(field)}\n'

        return strrep

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CollectionElement):
            return self.toDict() == __o.toDict()
        elif isinstance(__o, dict):
            warnings.warn(
                "Warning: instance {} is dict, not Element.".format(__o))
            return self.toDict() == __o
        elif isinstance(__o, str):
            warnings.warn(
                "Warning: instance {} is str, not Element.".format(__o))
            return str(self) == __o
        else:
            return False

    def updateUpdateTime(self):
        self.updateDate = currentTime()


class WorkItemDefinition(CollectionElement):
    fileextension = f'{config.fileprefix}def'
    '''
    Defines an item to be displayed in panels and on the canvas. Contains fields that change how input is taken from the user.
    '''

    def fromDict(inDict: dict):
        '''
        Creates ItemDefinitionCollection from dict

        Args:
            inDict (dict): Dictionary to parse

        Returns:
            ItemDefinitionCollection: Item Collection
        '''
        e = WorkItemDefinition()

        # Identifiers
        e.uuid = inDict['uuid']

        # Fields are used to denote public and private fields
        e.public = [parseField(serializedField)
                    for serializedField in inDict['public']]
        e.private = [parseField(serializedField)
                     for serializedField in inDict['private']]

        e.downstream = inDict['downstream']
        e.upstream = inDict['upstream']

        # Time tracking
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        e.name = inDict['name']

        return e

    def __init__(self, tree=None, parent=None, name: str = "Item Definition") -> None:
        super().__init__(tree, parent)
        '''
        Initializes an Item Definition, to be used to display information in the canvas with various UI Elements

        Args:
            name (str, optional): Name of item. Defaults to "Item Definition".
            fields (list[Field], optional): Editable Fields. Defaults to [].
        '''
        self.name = name

        self.templateChanged = Delegate()
        # For definitions, streams define the stream rules
        self.downstream: list[str] = []
        self.upstream: list[str] = []

    def serialize(self):
        path = os.path.join(Scope.currentWorkspace.getFullPath(
            Scope.currentWorkspace.getDefinitionPath(self)))
        with open(f'{path}{WorkItemDefinition.fileextension}', "w") as outfile:
            json.dump(self.toDict(), outfile)

    def addDownstreamRule(self, definition, allow=True):
        target = definition if isinstance(
            definition, WorkItemDefinition) else Scope.currentWorkspace.getDefinitionByUUID(definition)
        if target.uuid in self.downstream:
            return
        if allow:
            self.downstream.append(target.uuid)
            target.addUpstreamRule(self)
        else:
            self.downstream.remove(target.uuid)
            target.addUpstreamRule(self, False)

    def addUpstreamRule(self, definition, allow=True):
        target = definition if isinstance(
            definition, WorkItemDefinition) else Scope.currentWorkspace.getDefinitionByUUID(definition)
        if target.uuid in self.upstream:
            return
        if allow:
            self.upstream.append(target.uuid)
            target.addDownstreamRule(self)
        else:
            self.upstream.remove(target.uuid)
            target.addDownstreamRule(self, False)

    def getDownstream(self) -> list:
        return [Scope.currentWorkspace.getDefinitionByUUID(id) for id in self.downstream]

    def getUpstream(self) -> list:
        return [Scope.currentWorkspace.getDefinitionByUUID(id) for id in self.upstream]

    def addPrivateField(self, field: Field):
        super().addPrivateField(field)
        self.templateChanged.emit(self)

    def addPublicField(self, field: Field):
        super().addPublicField(field)
        self.templateChanged.emit(self)

    def toDict(self) -> dict:
        '''
        Serializes Item Definition to dict

        Returns:
            dict: output dictionary
        '''
        based = super().toDict()
        based['name'] = self.name
        based['downstream'] = self.downstream
        based['upstream'] = self.upstream
        return based

    def __str__(self) -> str:
        return f'{self.name}\n{super().__str__()}'

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, WorkItemDefinition):
            return __o.toDict() == self.toDict()
        return super().__eq__(__o)


class WorkItem(WorkItemDefinition):
    fileextension = f'{config.fileprefix}item'

    def fromDict(inDict: dict):
        e = WorkItem(template=Scope.currentWorkspace.getDefinitionByUUID(
            inDict['template']))

        # Identifiers
        e.uuid = inDict['uuid']

        # Streams
        e.downstream = inDict['downstream']
        e.upstream = inDict['upstream']

        # Fields are used to denote public and private fields
        e.public = [parseField(serializedField)
                    for serializedField in inDict['public']]
        e.private = [parseField(serializedField)
                     for serializedField in inDict['private']]

        # Time tracking
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        e.name = inDict['name']

        return e

    def __init__(self, tree=None, parent=None, name: str = "Item Definition", template: WorkItemDefinition = None) -> None:
        super().__init__(tree, parent, name)
        self.itemChanged = Delegate()
        if template == None:
            return
        self.template = template
        self.template.templateChanged.connect(self.populateFromTemplate)

        self.populateFromTemplate(self.template)

    def serialize(self):
        path = os.path.join(Scope.currentWorkspace.getFullPath(
            Scope.currentWorkspace.getWorkitemPath(self)))
            
        with open(os.path.normpath(f'{path}{WorkItem.fileextension}'), "w") as outfile:
            json.dump(self.toDict(), outfile)

    def addDownstreamRule(self, definition, allow=True):
        pass

    def addUpstreamRule(self, definition, allow=True):
        pass

    def getDownstream(self) -> list:
        return [Scope.currentWorkspace.getWorkItemByUUID(id) for id in self.downstream]

    def getUpstream(self) -> list:
        return [Scope.currentWorkspace.getWorkItemByUUID(id) for id in self.upstream]

    def addDownstream(self, item):
        def commit():
            self.downstream.append(target.uuid)
            target.addUpstream(self)
        target = item if isinstance(
            item, WorkItem) else Scope.currentWorkspace.getWorkItemByUUID(item)
        if target.uuid in self.downstream:
            return
        if Scope.rulespolicy == Scope.RulesPolicy.STRICT:
            if target.template.uuid in self.template.downstream:
                commit()
            return
        elif Scope.rulespolicy == Scope.RulesPolicy.WARN:
            if target.template.uuid not in self.template.downstream:
                warnings.warn(
                    f'Warning: Rule broken while connecting {target.uuid} downstream of {self.uuid}.')
        commit()

    def addUpstream(self, item):
        def commit():
            self.upstream.append(target.uuid)
            target.addDownstream(self)
        target = item if isinstance(
            item, WorkItem) else Scope.currentWorkspace.getWorkItemByUUID(item)
        if target.uuid in self.upstream:
            return
        if Scope.rulespolicy == Scope.RulesPolicy.STRICT:
            if target.template.uuid in self.template.upstream:
                commit()
            return
        elif Scope.rulespolicy == Scope.RulesPolicy.WARN:
            if target.template.uuid not in self.template.upstream:
                warnings.warn(
                    f'Warning: Rule broken while connecting {target.uuid} upstream of {self.uuid}.')
        commit()

    def populateFromTemplate(self, template: WorkItemDefinition):
        currentpublicidentifiers = {field.name: field for field in self.public}
        currentpublickeys = list(currentpublicidentifiers.keys())
        for currentkey in currentpublickeys:
            if currentkey not in [field.name for field in template.public]:
                self.removePublicField(currentkey)
        for publictemplatefield in template.public:
            if publictemplatefield.name in currentpublickeys:
                currentpublicidentifiers[publictemplatefield.name].reconcile(
                    publictemplatefield)
            else:
                self.addPublicField(copy.deepcopy(publictemplatefield))

        currentprivateidentifiers = {
            field.name: field for field in self.private}
        currentprivatekeys = list(currentprivateidentifiers.keys())
        for currentkey in currentprivatekeys:
            if currentkey not in [field.name for field in template.private]:
                self.removePrivateField(currentkey)
        for privatetemplatefield in template.private:
            if privatetemplatefield.name in list(currentprivateidentifiers.keys()):
                currentprivateidentifiers[privatetemplatefield.name].reconcile(
                    privatetemplatefield)
            else:
                self.addPrivateField(copy.deepcopy(privatetemplatefield))

    def toDict(self) -> dict:
        d = super().toDict()
        d['template'] = self.template.uuid
        return d


class Document(TreeNode):
    fileextension = f'{config.fileprefix}doc'
    '''
    Collection of item types to be used inside systems and standards collections.
    '''

    def fromDict(inDict: dict):
        '''
        Create Document from dictionary.

        Args:
            inDict (dict): input dictionary

        Returns:
            Document: Document
        '''
        e = Document(name=inDict['name'])
        # Identifiers
        e.uuid = inDict['uuid']

        # Time tracking
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        e.name = inDict['name']

        e.workItems = inDict['workItems']

        return e

    def __init__(self, name: str = "Item Collection", tree=None, parent=None) -> None:
        id = str(uuid.uuid4())
        super().__init__(id, tree, parent)
        '''
        Initializes a Document with name.

        Args:
            name (str, optional): Name of the collection. Defaults to "Item Collection".
        '''
        self.name = name

        self.createDate = currentTime()
        self.updateDate = currentTime()

        self.workItems: list[str] = []

    def serialize(self):
        path = os.path.join(Scope.currentWorkspace.getFullPath(
            Scope.currentWorkspace.getDocumentPath(self)))
        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, f'{self.name}{Document.fileextension}'), "w") as outfile:
            json.dump(self.toDict(), outfile)

    def getWorkItems(self):
        return [Scope.currentWorkspace.getWorkItemByUUID(workitem) for workitem in self.workItems]

    def toDict(self) -> dict:
        '''
        Serializes ItemTypeCollection to dict

        Returns:
            dict: output dict
        '''
        based = {}
        based['uuid'] = self.uuid
        based['name'] = self.name
        based['createDate'] = self.createDate
        based['updateDate'] = self.updateDate
        based['workItems'] = self.workItems
        return based


class Project(CollectionElement):
    '''
    The Project holds data for a project

    Returns:
        _type_: _description_
    '''

    fileextension = f'{config.fileprefix}proj'

    def __init__(self, name='Default Project Name', tree=None, parent=None) -> None:
        super().__init__(tree, parent)
        self.name = name

        self.definitions: list[str] = []
        self.workitems: list[str] = []
        self.documents: list[str] = []

    def serialize(self):
        path = Scope.currentWorkspace.getFullPath(
            Scope.currentWorkspace.getDocumentPath(self))
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, f'{self.name}{Project.fileextension}'), "w") as outfile:
            json.dump(self.toDict(), outfile)

    def toDict(self) -> dict:
        d = super().toDict()
        d['name'] = self.name
        d['definitions'] = self.definitions
        d['workitems'] = self.workitems
        d['documents'] = self.documents
        return d

    def fromDict(inDict: dict):
        e = Project()

        # Identifiers
        e.uuid = inDict['uuid']
        e.name = inDict['name']

        # Fields are used to denote public and private fields
        e.public = [parseField(serializedField)
                    for serializedField in inDict['public']]
        e.private = [parseField(serializedField)
                     for serializedField in inDict['private']]

        e.definitions = inDict['definitions']
        e.workitems = inDict['workitems']
        e.documents = inDict['documents']

        # Time tracking
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        return e

    def createWorkItemDefinition(self, name='Default Work Item Definition', parent=None):
        if parent == None:
            parent = self

        definition = Scope.currentWorkspace.createNewWorkItemDefinition(
            name, parent)
        self.definitions.append(definition.uuid)
        return definition

    def createWorkItem(self, name=None, template=None, parent=None):
        if parent == None:
            parent = self
        workitem = Scope.currentWorkspace.createNewWorkItem(
            name=name, template=template, parent=parent)
        self.workitems.append(workitem.uuid)
        return workitem

    def createNewDocument(self, name='Default Document', parent=None):
        if parent == None:
            parent = self
        doc = Scope.currentWorkspace.createNewDocument(name, parent)
        self.documents.append(doc.uuid)
        return doc


class Workspace(Tree):

    def __init__(self, directory: str) -> None:
        super().__init__()
        self.root = directory

        if not os.path.exists(directory):
            os.makedirs(directory)

        self.__definitions = {}
        self.__projects = {}
        self.__workitems = {}
        self.__documents = {}
        if directory == None:
            return

    def discoveritems(self, directory):
        self.discoverDocuments(directory)
        self.discoverProjects(directory)
        self.discoverDefinitions(directory)
        self.discoverWorkItems(directory)

        self.updateStructureFromFileStructure()

    def updateStructureFromFileStructure(self):

        dicts = [self.__definitions, self.__workitems]
        for dict in dicts:
            for uuid, itemlookup in dict.items():
                parent = first([lookup['item'] for uuid, lookup in self.__documents.items() if os.path.dirname(self.getFullPath(itemlookup['path'])) == os.path.dirname(self.getFullPath(
                    lookup['path']))] + [lookup['item'] for uuid, lookup in self.__projects.items() if os.path.dirname(self.getFullPath(itemlookup['path'])) == os.path.dirname(self.getFullPath(lookup['path']))])
                itemlookup['item'].tree = self
                self.addNode(itemlookup['item'])
                itemlookup['item'].parent = parent
                item = itemlookup['item']
                loc = itemlookup['path']
                print(f'Calculated Path: {item.getPath()}\nStored: {loc}')

        dicts = [self.__projects, self.__documents]
        for dict in dicts:
            for uuid, itemlookup in dict.items():
                parent = first([lookup['item'] for uuid, lookup in self.__documents.items() if os.path.dirname(os.path.dirname(self.getFullPath(itemlookup['path']))) == os.path.dirname(self.getFullPath(
                    lookup['path']))] + [lookup['item'] for uuid, lookup in self.__projects.items() if os.path.dirname(os.path.dirname(self.getFullPath(itemlookup['path']))) == os.path.dirname(self.getFullPath(lookup['path']))])
                itemlookup['item'].tree = self
                self.addNode(itemlookup['item'])                
                itemlookup['item'].parent = parent
                item = itemlookup['item']
                loc = itemlookup['path']
                print(f'Calculated Path: {item.getPath()}\nStored: {loc}')

    def getFullPath(self, relpath: str):
        return f'{self.root}{os.sep}{relpath}'

    def moveItem(self, item, newparent):
        
        source = self.getFullPath(item.getPath())

        destination = os.path.join(self.getFullPath(newparent.getPath()), os.path.basename(source))

        print(f'{source}, {destination}')
        item.parent = newparent
        shutil.move(os.path.normpath(source), os.path.normpath(destination))

    # Discovery

    def discoverDefinitions(self, dir: str):
        # Get all definitions
        for definitionpath in getFilesWithExtension([dir], extension=WorkItemDefinition.fileextension, recursive=True):
            item = WorkItemDefinition.fromDict(loadJsonLike(
                os.path.relpath(definitionpath, os.path.dirname(dir))))
            self.__definitions[item.uuid] = {
                'path': os.path.relpath(definitionpath, dir),
                'item':  item
            }

    def discoverDocuments(self, dir: str):
        # Get All Documents
        for documentpath in getFilesWithExtension([dir], extension=Document.fileextension, recursive=True):
            doc = Document.fromDict(loadJsonLike(
                os.path.relpath(documentpath, os.path.dirname(dir))))
            self.__documents[doc.uuid] = {
                'path': os.path.relpath(documentpath, dir),
                'item': doc
            }

    def discoverWorkItems(self, dir: str):
        # Get All Work Items
        for workitempath in getFilesWithExtension([dir], extension=WorkItem.fileextension, recursive=True):
            wi = WorkItem.fromDict(loadJsonLike(
                os.path.relpath(workitempath, os.path.dirname(dir))))

            self.__workitems[wi.uuid] = {
                'path': os.path.relpath(workitempath, dir),
                'item': wi
            }

    def discoverProjects(self, dir: str):
        # Get all projects
        for projectpath in getFilesWithExtension([dir], extension=Project.fileextension, recursive=True):
            project = Project.fromDict(loadJsonLike(
                os.path.relpath(projectpath, os.path.dirname(dir))))
            self.__projects[project.uuid] = {
                'path': os.path.relpath(projectpath, dir),
                'item': project
            }

    # Getters/Lazy loader

    def getWorkItemByUUID(self, uuid: str):
        if isinstance(self.__workitems[uuid]['item'], NoneType):
            self.__workitems[uuid]['item'] = WorkItem.fromDict(
                loadJsonLike(self.getFullPath(self.__workitems[uuid]['path'])))
        return self.__workitems[uuid]['item']

    def getWorkItems(self):
        return [self.getWorkItemByUUID(id) for id in self.__workitems]

    def getProjectByUUID(self, uuid: str):
        if isinstance(self.__projects[uuid]['item'], NoneType):
            self.__projects[uuid]['item'] = Project.fromDict(
                loadJsonLike(self.getFullPath(self.__projects[uuid]['path'])))
        return self.__projects[uuid]['item']

    def getProjects(self):
        return [self.getProjectByUUID(id) for id in self.__projects]

    def getDefinitionByUUID(self, uuid: str):
        if isinstance(self.__definitions[uuid]['item'], NoneType):
            self.__definitions[uuid]['item'] = WorkItemDefinition.fromDict(
                loadJsonLike(self.getFullPath(self.__definitions[uuid]['path'])))
        return self.__definitions[uuid]['item']

    def getDefinitions(self):
        return [self.getDefinitionByUUID(id) for id in self.__definitions]

    def getDocumentByUUID(self, uuid: str):
        if isinstance(self.__documents[uuid]['item'], NoneType):
            self.__documents[uuid]['item'] = Document.fromDict(
                loadJsonLike(self.getFullPath(self.__documents[uuid]['path'])))

        return self.__documents[uuid]['item']

    def getDocuments(self):
        return [self.getDocumentByUUID(id) for id in self.__documents]

    def getDocumentPath(self, document: Document):
        return self.__documents[document.uuid]['path']

    def getDefinitionPath(self, definition: WorkItemDefinition):
        return self.__definitions[definition.uuid]['path']

    def getWorkitemPath(self, workitem: WorkItem):
        return self.__workitems[workitem.uuid]['path']

    def getProjectPath(self, project: Project):
        return self.__projects[project.uuid]['path']

    # Item Creation
    def createNewWorkItemDefinition(self, name=None, parent=None):
        item = WorkItemDefinition(
            tree=Scope.currentWorkspace, name=name, parent=parent)
        self.addNode(item)
        if parent == None:
            path = os.sep
        else:
            path = parent.getPath()
        self.__definitions[item.uuid] = {
            'path': os.path.join(path, item.name),
            'item': item
        }
        item.serialize()
        return item

    def createNewWorkItem(self, name=None, template=None, parent=None):
        item = WorkItem(tree=Scope.currentWorkspace, name=name,
                        parent=parent, template=template)
        self.addNode(item)
        if parent == None:
            path = os.sep
        else:
            path = parent.getPath()
        self.__workitems[item.uuid] = {
            'path': os.path.join(path, item.name),
            'item': item
        }
        item.serialize()
        return item

    def createNewDocument(self, name=None, parent: CollectionElement = None):
        doc = Document(tree=Scope.currentWorkspace, name=name, parent=parent)
        self.addNode(doc)
        if parent == None:
            path = os.sep
        else:
            path = parent.getPath()
        self.__documents[doc.uuid] = {
            'path': os.path.join(path, doc.name),
            'item': doc
        }
        doc.serialize()
        return doc

    def createNewProject(self, name=None, parent: CollectionElement = None):
        doc = Project(tree=Scope.currentWorkspace, name=name, parent=parent)
        self.addNode(doc)
        if parent == None:
            path = os.sep
        else:
            path = parent.getPath()
        self.__documents[doc.uuid] = {
            'path': os.path.join(path, doc.name),
            'item': doc
        }
        doc.serialize()
        return doc


class Scope:

    class RulesPolicy(Enum):
        STRICT = 0  # Completely disallow rule breaking
        WARN = 1  # Throw a warning when a rule is broken
        NONE = 2  # Allow rule breaking

    currentWorkspace = None
    rulespolicy = RulesPolicy.STRICT

    def setCurrentWorkspaceFromDirectory(directory):
        Scope.currentWorkspace = Workspace(directory)
        Scope.currentWorkspace.discoveritems(directory)
        return Scope.currentWorkspace
