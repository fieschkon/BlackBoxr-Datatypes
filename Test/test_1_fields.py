from BBData.Fields import Checks, Radio

fields = [(0, 'Check1', False), (1, 'Check2', False), (2, 'Check3', False)]

class TestCheck:

    def test_getandset(self):
        testitem = Checks(fields)
        testitem.setOption(0, True)

        assert testitem.getOption(0)[1] == True
        assert testitem.getOption(1)[1] == testitem.options[1]['state']

class TestRadio:

    def test_getandset(self):
        testitem = Radio(fields)
        testitem.setOption(0, True)

        assert testitem.getOption(0)[1] == True
        assert testitem.getOption(1)[1] == testitem.options[1]['state']

        testitem.setOption(1, True)
        assert testitem.getOption(0)[1] == False
        assert testitem.getOption(1)[1] == True
