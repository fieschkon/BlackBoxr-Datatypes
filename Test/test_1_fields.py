from BBData.Fields import Checks, Radio

fields = [(0, 'Check1', False), (1, 'Check2', False), (2, 'Check3', False)]

class TestCheck:

    def test_getandset(self):
        testitem = Checks(fields)
        testitem.setOption(0, True)

        assert testitem.getOption(0)[1] == True
        assert testitem.getOption(1)[1] == testitem.options[1]['state']

    def test_serialize(self):
        testitem = Checks(fields)
        testitem.setOption(0, True)

        testitem2 = Checks(fields)
        testitem3 = Checks(fields)

        assert testitem != testitem2
        assert testitem2 == testitem3
class TestRadio:

    def test_getandset(self):
        testitem = Radio(fields)
        testitem.setOption(0, True)

        assert testitem.getOption(0)[1] == True
        assert testitem.getOption(1)[1] == testitem.options[1]['state']

        testitem.setOption(1, True)
        assert testitem.getOption(0)[1] == False
        assert testitem.getOption(1)[1] == True

    def test_serialize(self):
        testitem = Radio(fields)
        testitem.setOption(0, True)

        testitem2 = Radio(fields)
        testitem3 = Radio(fields)

        assert testitem != testitem2
        assert testitem2 == testitem3