from abc import abstractmethod
import copy
from datetime import datetime
from BBData.Delegate import Delegate
from BBData.Fields import Checks, Field, FieldType, LongText, Radio, ShortText
from dictdiffer import diff
import json
from typing import Callable
import uuid
import warnings


class CollectionElement():

    @staticmethod
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

    @staticmethod
    def fromDict(inDict : dict):
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
        e.public = inDict['public']
        e.private = inDict['private']

        # Time tracking 
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        return e

    @staticmethod
    def fromStr(inStr : str):
        '''
        Creates Collection Element from str

        Args:
            inStr (str): Input String

        Returns:
            CollectionElement: Element
        '''
        return CollectionElement.fromDict(json.loads(inStr))

    @staticmethod
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

    def __init__(self) -> None:

        # Identifiers 
        self.uuid = str(uuid.uuid4())
        
        # Fields are used to denote public and private fields 
        self.public = {}
        self.private = {'tags' : []}

        # Time tracking 
        self.createDate = self.generateCreateTime()
        self.updateDate = self.createDate

        # Delegate
        self.anyAttributeChanged = Delegate()

    def setPublicValue(self, key, value):
        self.public[key] = value
        self.anyAttributeChanged.emit('public', (key, value))

    def getPublicValue(self, key):
        return self.public.get(key)

    def getPrivateValue(self, key):
        return self.private.get(key)

    def setPrivateValue(self, key, value):
        self.private[key] = value
        self.anyAttributeChanged.emit('private', (key, value))

    def generateCreateTime(self):
        '''
        Generate the current time

        Returns:
            str: Current Time
        '''
        return datetime.now().strftime("%m/%d/%y %H:%M:%S")

    def toDict(self) -> dict:
        '''
        Serialize to dict

        Returns:
            dict: serialized dict
        '''
        d = {}
        d['uuid'] = str(self.uuid)
        d['public'] = self.public
        d['private'] = self.private
        d['createDate'] = self.createDate
        d['updateDate'] = self.updateDate
        return d

    def __setattr__(self, key, value):
        if hasattr(self, key):
            if key not in ['updateDate'] and value != self.__getattribute__(key):
                self.updateDate = self.generateCreateTime()
                self.anyAttributeChanged.emit(key, value)
        super().__setattr__(key, value)

    def __repr__(self) -> str:
        return str(self.uuid)

    def __str__(self) -> str:
        return json.dumps(self.toDict())

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CollectionElement):
            return self.toDict() == __o.toDict()
        elif isinstance(__o, dict):
            warnings.warn("Warning: instance {} is dict, not Element.".format(__o))
            return self.toDict() == __o
        elif isinstance(__o, str):
            warnings.warn("Warning: instance {} is str, not Element.".format(__o))
            return str(self) == __o
        else: return False

class ItemDefinition(CollectionElement):
    '''
    Defines an item to be displayed in panels and on the canvas. Contains fields that change how input is taken from the user.
    '''
    @staticmethod
    def fromDict(inDict : dict):
        '''
        Creates ItemDefinitionCollection from dict

        Args:
            inDict (dict): Dictionary to parse

        Returns:
            ItemDefinitionCollection: Item Collection
        '''
        e = ItemDefinition()

        # Identifiers 
        e.uuid = inDict['uuid']
        
        # Fields are used to denote public and private fields 
        e.public = inDict['public']
        e.private = inDict['private']

        # Time tracking 
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        e.name = inDict['name']

        for element in inDict['fields']:
            match element['type']:
                case FieldType.NONE:
                    element = Field.fromDict(element)
                case FieldType.LINETEXT:
                    element = ShortText.fromDict(element)
                case FieldType.LONGTEXT:
                    element = LongText.fromDict(element)
                case FieldType.RADIO:
                    element = Radio.fromDict(element)
                case FieldType.CHECKS:
                    element = Checks.fromDict(element)
            e.fields.append(element)

        return e

    def __init__(self, name : str = "Item Definition", fields : list[Field] = []) -> None:
        '''
        Initializes an Item Definition, to be used to display information in the canvas with various UI Elements

        Args:
            name (str, optional): Name of item. Defaults to "Item Definition".
            fields (list[Field], optional): Editable Fields. Defaults to [].
        '''
        super().__init__()
        self.name = name
        self.fields : list[Field] = fields

    def toDict(self) -> dict:
        '''
        Serializes Item Definition to dict

        Returns:
            dict: output dictionary
        '''
        based = super().toDict()
        based['name'] = self.name
        based['fields'] = [d.toDict() for d in self.fields]     
        return based

    def addField(self, field : Field):
        '''
        Adds a field to the item definition

        Args:
            field (Field): Field to add
        '''
        self.fields.append(field)
    
    def addFields(self, fields : list[Field]):
        '''
        Adds a list of fields to the item definition.

        Args:
            fields (list[Field]): Fields to add
        '''
        self.fields += fields

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ItemDefinition):
            return __o.toDict() == self.toDict()
        return super().__eq__(__o)

    def __str__(self) -> str:
        return json.dumps(self.toDict())

    def __repr__(self) -> str:
        return self.uuid

class ItemTypeCollection(CollectionElement):
    '''
    Collection of item types to be used inside systems and standards collections.
    '''
    @staticmethod
    def fromDict(inDict : dict):
        '''
        Create ItemTypeCollection from dictionary.

        Args:
            inDict (dict): input dictionary

        Returns:
            ItemTypeCollection: ItemTypeCollection
        '''
        e = ItemTypeCollection(name=inDict['name'])
        # Identifiers 
        e.uuid = inDict['uuid']
        
        # Fields are used to denote public and private fields 
        e.public = inDict['public']
        e.private = inDict['private']

        # Time tracking 
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        e.name = inDict['name']

        mapping = [('requirements', e.requirements), ('designelements', e.designelements), ('testitems', e.testitems)]
        for mp in mapping:
            for itemtype in inDict[mp[0]]:
                mp[1].append(ItemDefinition.fromDict(itemtype))
        return e

    def __init__(self, name : str = "Item Definition Collection") -> None:
        '''
        Initializes a ItemTypeCollection with name.

        Args:
            name (str, optional): Name of the collection. Defaults to "Item Definition Collection".
        '''
        super().__init__()
        self.name = name

        self.requirementAdded = Delegate()
        self.designelementAdded = Delegate()
        self.testitemAdded = Delegate()

        self.requirements : list[ItemDefinition] = []
        self.designelements : list[ItemDefinition] = []
        self.testitems : list[ItemDefinition] = []

    def toDict(self) -> dict:
        '''
        Serializes ItemTypeCollection to dict

        Returns:
            dict: output dict
        '''
        based = super().toDict()
        based['name'] = self.name
        based['requirements'] = [d.toDict() for d in self.requirements]
        based['designelements'] = [d.toDict() for d in self.designelements]    
        based['testitems'] = [d.toDict() for d in self.testitems]    
        return based

    def addRequirement(self, requirement : ItemDefinition):
        '''
        Adds a single requirement

        Args:
            requirement (ItemDefinition): Requirement type to add
        '''
        self.requirements.append(requirement)
        self.requirementAdded.emit(requirement)
    
    def addRequirements(self, requirements : list[ItemDefinition]):
        '''
        Adds multiple requirements

        Args:
            requirements (list[ItemDefinition]): Requirement types to add
        '''
        for i in requirements:
            self.addRequirement(i)

    def addDesignElement(self, designelement : ItemDefinition):
        '''
        Adds a single design element definition

        Args:
            designelement (ItemDefinition): Design element to add
        '''
        self.designelements.append(designelement)
        self.designelementAdded.emit(designelement)
   
    def addDesignElements(self, designelements : list[ItemDefinition]):
        '''
        Adds multiple design element definitions

        Args:
            designelements (list[ItemDefinition]): Design elements to add
        '''
        for i in designelements:
            self.addDesignElement(i)

    def addTestItem(self, testitem : ItemDefinition):
        '''
        Adds a test item definition

        Args:
            testitem (ItemDefinition): Test item
        '''
        self.testitems.append(testitem)
        self.testitemAdded.emit(testitem)

    def addTestItems(self, testitems : list[ItemDefinition]):
        '''
        Adds multiple test item definitions

        Args:
            testitems (list[ItemDefinition]): Definitions to add
        '''
        for i in testitems:
            self.addTestItem(i)

class System(CollectionElement):
    def __init__(self) -> None:
        super().__init__()
        self.DL = []
        self.RL = []
        self.TE = []