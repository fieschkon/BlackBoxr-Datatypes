
from BBData.BBData import Delegate


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