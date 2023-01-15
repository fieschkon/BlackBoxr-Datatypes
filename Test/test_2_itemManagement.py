from random import randint
import random
import string
from BBData.BBData import ItemDefinitionCollection
from BBData.Fields import *


def generateRandomFields():
    fields = []
    for i in range(randint(1, 5)):
        fields.append((i, f'Check {i}', bool(randint(0, 1))))
    return fields

def randomString(length=5)->str:
  return ''.join(random.choices(string.ascii_letters, k=length))

class TestCollection:
    def test_createCollection(self):
        commonFields = [Checks(generateRandomFields()), Radio(generateRandomFields()), ShortText(randomString(), LongText(randomString(length=10)))]
        ic = ItemDefinitionCollection()
        ic.addItems(commonFields)

        ic2 = ItemDefinitionCollection()
        ic2.addItems(commonFields)

        ic3 = ItemDefinitionCollection()
        ic3.addItems([Checks(generateRandomFields()), Radio(generateRandomFields()), ShortText(randomString(), LongText(randomString(length=10)))])
        # Force same uuid
        ic2.uuid = ic.uuid
        assert ic == ic2
        assert ic3 != ic2
        

