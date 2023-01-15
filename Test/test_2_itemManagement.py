from random import randint
import random
import string
from BBData.BBData import ItemDefinitionCollection
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

class TestCollection:
    def test_createCollection(self):
        commonFields = [Checks(generateRandomFieldTuples()), Radio(generateRandomFieldTuples()), ShortText(randomString(), LongText(randomString(length=10)))]
        ic = ItemDefinitionCollection()
        ic.addRequirements(commonFields)

        ic2 = ItemDefinitionCollection()
        ic2.addRequirements(commonFields)

        ic3 = ItemDefinitionCollection()
        ic3.addRequirements([Checks(generateRandomFieldTuples()), Radio(generateRandomFieldTuples()), ShortText(randomString(), LongText(randomString(length=10)))])
        # Force same uuid
        ic2.uuid = ic.uuid
        assert ic == ic2
        assert ic3 != ic2
        
    def test_serialization(self):
        ic = ItemDefinitionCollection()
        ic.addRequirements(generateRandomFieldItems())
        ic.addDesignElements(generateRandomFieldItems())
        ic.addTestitems(generateRandomFieldItems())
        
        assert ic == ItemDefinitionCollection.fromDict(ic.toDict())