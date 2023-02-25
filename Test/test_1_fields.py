import random
import string
from BBData.Fields import Checks, Radio, Enum, ShortText, LongText, parseField

def randomString(length=5)->str:
  return ''.join(random.choices(string.ascii_letters, k=length))

def randomCheckFieldDict():
    return {randomString() : bool(random.randint(0, 1)) for i in range(random.randint(2, 5))}

def randomEnumList():
    return [randomString() for i in range(random.randint(2,5))]
 
commonCheckFields= randomCheckFieldDict()
commonEnumFields = randomEnumList()
commonText = randomString()

class TestParser:

    def test_parsing(self):
        testCheck = Checks(commonCheckFields)
        testRadio = Radio(commonCheckFields) 
        testEnum = Enum(commonEnumFields, commonEnumFields[0])
        testShortText = ShortText(defaultText=commonText)
        testLongText = LongText(defaultText=commonText)

        testitems = [testCheck, testRadio, testEnum, testShortText, testLongText]

        for item in testitems:
            assert item == parseField(item.toDict())

class TestCheck:

    def test_getandset(self):
        config = randomCheckFieldDict()
        testitem = Checks(config)
        testitem.setOption(0, True)

        assert testitem.getOption(0) == True
        assert testitem.getOption(1) == testitem.options[list(testitem.options.keys())[1]]

    def test_equality(self):
        testitem = Checks(commonCheckFields)

        testitem2 = Checks(randomCheckFieldDict())
        testitem3 = Checks(commonCheckFields)

        assert testitem != testitem2
        assert testitem == testitem3

    def test_serialize(self):
        testitem = Checks(commonCheckFields)
        testitem2 = Checks(commonCheckFields)

        assert testitem == testitem2
        assert testitem == Checks.fromDict(testitem2.toDict())

    
class TestRadio:

    def test_getandset(self):
        config = randomCheckFieldDict()
        testitem = Radio(config)
        testitem.setOption(0, True)

        assert testitem.getOption(0) == True
        assert testitem.getOption(1) == testitem.options[list(testitem.options.keys())[1]]

    def test_equality(self):
        testitem = Radio(commonCheckFields)

        testitem2 = Radio(randomCheckFieldDict())
        testitem3 = Radio(commonCheckFields)

        assert testitem != testitem2
        assert testitem == testitem3

    def test_serialize(self):
        testitem = Radio(commonCheckFields)
        testitem2 = Radio(commonCheckFields)

        assert testitem == testitem2
        assert testitem == Radio.fromDict(testitem2.toDict())

class TestEnum:

    def test_getandset(self):
        config = randomEnumList()
        testitem = Enum(config, config[0])
        
        assert testitem.getCurrent() == config[0]
        testitem.setCurrent(1)
        assert testitem.getCurrent() == config[1]

    def test_equality(self):
        testitem = Enum(commonEnumFields, commonEnumFields[0])
        r = randomEnumList()
        testitem2 = Enum(r, r[0])
        testitem3 = Enum(commonEnumFields, commonEnumFields[0])

        assert testitem != testitem2
        assert testitem == testitem3

    def test_serialize(self):
        testitem = Enum(commonEnumFields, commonEnumFields[0])
        testitem2 = Enum(commonEnumFields, commonEnumFields[0])

        assert testitem == testitem2
        assert testitem == Enum.fromDict(testitem2.toDict())

class TestShortText:

    def test_getandset(self):
        st = randomString()
        testitem = ShortText(defaultText=st)
        
        assert testitem.text() == st
        st = randomString()
        assert testitem.text() != st
        testitem.setText(st)
        assert testitem.text() == st

    def test_equality(self):
        common = randomString()
        testitem = ShortText(defaultText=common)
        r = randomEnumList()
        testitem2 = ShortText(defaultText=randomEnumList())
        testitem3 = ShortText(defaultText=common)

        assert testitem != testitem2
        assert testitem == testitem3

    def test_serialize(self):
        common = randomString()
        testitem = ShortText(defaultText=common)
        testitem2 = ShortText(defaultText=common)

        assert testitem == testitem2
        assert testitem == ShortText.fromDict(testitem2.toDict())

class TestLongText:

    def test_getandset(self):
        st = randomString()
        testitem = LongText(defaultText=st)
        
        assert testitem.text() == st
        st = randomString()
        assert testitem.text() != st
        testitem.setText(st)
        assert testitem.text() == st

    def test_equality(self):
        common = randomString()
        testitem = LongText(defaultText=common)
        r = randomEnumList()
        testitem2 = LongText(defaultText=randomEnumList())
        testitem3 = LongText(defaultText=common)

        assert testitem != testitem2
        assert testitem == testitem3

    def test_serialize(self):
        common = randomString()
        testitem = LongText(defaultText=common)
        testitem2 = LongText(defaultText=common)

        assert testitem == testitem2
        assert testitem == LongText.fromDict(testitem2.toDict())