
import json
from BBData.BBData import CollectionElement
from BBData.Delegate import Delegate


class TestDelegate:

    def test_subscribenotify(self):

        class DelegateHaver():
            def __init__(self) -> None:
                self.delegate = Delegate()

            def triggerEmit(self):
                self.delegate.emit(12)

        def emitReceiver(a):
            assert a[0] == 12
        
        def lambdaReceiver(boo):
            assert boo

        testitem = DelegateHaver()
        testitem.delegate.connect(emitReceiver)
        testitem.delegate.connect(lambda x: lambdaReceiver(x[0] == 12))
        testitem.triggerEmit()

class TestCollection:

    def test_subscribenotify(self):
        self.trigger = False
        def onChanged(args):
            assert args[0] == 'public'
            assert args[1][0] == 'testkey'
            assert args[1][1] == 'value'
            self.trigger = True

        element = CollectionElement()
        element.anyAttributeChanged.connect(onChanged)
        element.setPublicValue('testkey', 'value')
        assert self.trigger

        self.trigger = False
        element.anyAttributeChanged.disconnect(onChanged)
        element.setPublicValue('testkey', 'value2')
        assert self.trigger == False
        

    def test_fieldEdits(self):
        element = CollectionElement()
        self.publicTrigger = False
        self.privateTrigger = False
        self.trigger = False
        def onChanged(args):
            assert args[0] in ['public', 'private']
            if args[0] == 'public':
                assert element.public[args[1][0]] == args[1][1]
                self.publicTrigger = True
            elif args[0] == 'private':
                assert element.private[args[1][0]] == args[1][1]
                self.privateTrigger = True
            self.trigger = True
        
        element.anyAttributeChanged.connect(onChanged)
        element.setPublicValue('testkey', 'value')
        element.setPrivateValue('testkey', 'value')
        assert self.trigger
        assert self.publicTrigger and self.privateTrigger

        assert element.getPrivateValue('testkey') == 'value'
        assert element.getPublicValue('testkey') == 'value'

    def test_serialize(self):
        element = CollectionElement()
        element.setPublicValue('testkey', 'value')
        element.setPrivateValue('testkey', 'value')
        d = element.toDict()
        assert element == CollectionElement.fromDict(d) == CollectionElement.fromStr(json.dumps(d))
        strel = json.dumps(d)
        assert str(element) == strel

    def test_diffing(self):
        element = CollectionElement()
        element.setPublicValue('testkey', 'value')
        element.setPrivateValue('testkey', 'value')

        element2 = CollectionElement.copy(element)
        element2.setPublicValue('testkey', 'skaboop')
        diff = CollectionElement.diff(element, element2)
        assert diff[0][0] == 'change'
        assert diff[1][0] == 'change'
        assert diff[0][1] == 'uuid'
        assert diff[1][1] == 'public.testkey'

    def test_equality(self):
        element = CollectionElement()
        assert element == element.toDict()
        assert element == str(element)
        assert element.uuid == repr(element)
        assert element != 12
