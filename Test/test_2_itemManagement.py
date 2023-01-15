from random import randint
import random
import string
from BBData.BBData import ItemDefinition, ItemTypeCollection
from BBData.Fields import *


def generateRandomFieldTuples():
    fields = []
    for i in range(randint(2, 5)):
        fields.append((i, f'Check {i}', bool(randint(0, 1))))
    return fields

def generateRandomFieldItems():
    return [Checks(generateRandomFieldTuples()), Radio(generateRandomFieldTuples()), ShortText(randomString(), LongText(randomString(length=10)))]

def randomString(length=5)->str:
  return ''.join(random.choices(string.ascii_letters, k=length))

def generateDefinition():
    c = ItemDefinition()
    c.addFields([Checks(generateRandomFieldTuples()), Radio(generateRandomFieldTuples()), ShortText(randomString(), LongText(randomString(length=10)))])
    return c
class TestItemDefinition:
    def test_equality(self):
        commonFields = [Checks(generateRandomFieldTuples()), Radio(generateRandomFieldTuples()), ShortText(randomString(), LongText(randomString(length=10)))]
        ic = ItemDefinition()
        ic.addFields(commonFields)

        ic2 = ItemDefinition()
        ic2.addFields(commonFields)

        ic3 = ItemDefinition()
        ic3.addFields([Checks(generateRandomFieldTuples()), Radio(generateRandomFieldTuples()), ShortText(randomString(), LongText(randomString(length=10)))])
        # Force same uuid
        ic2.uuid = ic.uuid
        assert ic == ic2
        assert ic3 != ic2
        
    def test_serialization(self):
        ic = ItemDefinition()
        ic.addFields(generateRandomFieldItems())
        
        assert ic == ItemDefinition.fromDict(ic.toDict())

class TestItemDefinitionCollection:
    def test_additems(self):
        self.reqflag = False
        self.desflag = False
        self.testflag = False

        self.col = ItemTypeCollection()

        def onRequirementAdded(args):
            assert args[0] in self.col.requirements
            self.reqflag = True

        def onDesignAdded(args):
            assert args[0] in self.col.designelements
            self.desflag = True

        def onTestAdded(args):
            assert args[0] in self.col.testitems
            self.testflag = True

        self.col.requirementAdded.connect(onRequirementAdded)
        self.col.designelementAdded.connect(onDesignAdded)
        self.col.testitemAdded.connect(onTestAdded)
        
        self.col.addRequirements([generateDefinition() for i in range(5)])
        self.col.addDesignElements([generateDefinition() for i in range(5)])
        self.col.addTestItems([generateDefinition() for i in range(5)])

        assert self.reqflag 
        assert self.desflag 
        assert self.testflag

    def test_serialization(self):
        col = ItemTypeCollection()
        col.addRequirements([generateDefinition() for i in range(5)])
        col.addDesignElements([generateDefinition() for i in range(5)])
        col.addTestItems([generateDefinition() for i in range(5)])

        assert col == ItemTypeCollection.fromDict(col.toDict())