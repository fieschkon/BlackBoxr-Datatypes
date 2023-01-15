from typing import Callable


class Delegate():

    def __init__(self) -> None:
        self.subscribers = []
    
    def connect(self, function : Callable):
        '''
        Connect function handle to delegate.

        Args:
            function (Callable): The handle for the method to be executed. Must handle *args.
        '''
        self.subscribers.append(function)

    def disconnect(self, function : Callable):
        '''
        Disconnects function handle from delegate.

        Args:
            function (Callable): The handle to be disconnected from the delegate.
        '''
        self.subscribers.remove(function)

    def emit(self, *args):
        for function in self.subscribers:
            function(args)