import os
from random import randint
import random
import string
from BBData.BBData import WorkItem, WorkItemDefinition, Scope
from BBData.Fields import *

Scope.setCurrentWorkspaceFromDirectory(os.path.join(os.getcwd(), f'Test{os.sep}TestProject'))

def randomString(length=5)->str:
  return ''.join(random.choices(string.ascii_letters, k=length))

def generateRandomField():
    type = randint(1, 5)
    match type:

        case FieldType.LINETEXT.value:
            return ShortText(randomString(), randomString())

        case FieldType.LONGTEXT.value:
            return LongText(randomString(), randomString(20))

        case FieldType.CHECKS.value:
            return Checks({randomString() : bool(randint(0, 1)) for i in range(randint(1, 5))}, randomString())

        case FieldType.RADIO.value:
            return Radio({randomString() : bool(randint(0, 1)) for i in range(randint(1, 5))}, fieldname=randomString())

        case FieldType.ENUM.value:
            l = [randomString() for i in range(randint(1, 5))]
            return Enum(l, l[0], randomString())

def generateRandomFieldItems():
    return [generateRandomField() for i in range(randint(1, 5))]


def generateDefinition():
    c = WorkItemDefinition(tree=Scope.currentWorkspace)
    c.addPublicFields(generateRandomFieldItems())
    return c

class TestItemDefinition:
    def test_equality(self):
        commonFields = generateRandomFieldItems()
        ic = WorkItemDefinition(tree=Scope.currentWorkspace)
        ic.addPublicFields(commonFields)

        ic2 = WorkItemDefinition(tree=Scope.currentWorkspace)
        ic2.addPublicFields(commonFields)

        ic3 = WorkItemDefinition(tree=Scope.currentWorkspace)
        ic3.addPublicFields(generateRandomFieldItems())
        # Force same uuid
        ic2.uuid = ic.uuid
        assert ic == ic2
        assert ic3 != ic2
        
    def test_serialization(self):
        ic = WorkItemDefinition(tree=Scope.currentWorkspace)
        ic.addPublicFields(generateRandomFieldItems())
        
        assert ic == WorkItemDefinition.fromDict(ic.toDict())

    def test_rules(self):
        
        ic = Scope.currentWorkspace.createNewWorkItemDefinition()

        ic2 = Scope.currentWorkspace.createNewWorkItemDefinition()

        ic.addDownstreamRule(ic2)

        assert ic2 in ic.getDownstream()
        assert ic in ic2.getUpstream()

class TestGenericItems:
    def test_creation(self):
        # Create Template
        definition = generateDefinition()
        requirement = WorkItem(template=definition, tree=Scope.currentWorkspace)
        assert requirement.public == definition.public

        def2 = generateDefinition()
        requirement.populateFromTemplate(def2)
        assert requirement.public[0].name == def2.public[0].name
