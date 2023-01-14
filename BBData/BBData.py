from abc import abstractmethod
from datetime import datetime
import difflib
import json
from typing import Callable
import uuid
import warnings


class Delegate():

    def __init__(self) -> None:
        self.subscribers = []
    
    def connect(self, function : Callable):
        '''
        connect Connect function handle to delegate.

        Args:
            function (Callable): The handle for the method to be executed. Must handle *args.
        '''
        self.subscribers.append(function)

    def disconnect(self, function : Callable):
        '''
        disconnect Disconnects function handle from delegate.

        Args:
            function (Callable): The handle to be disconnected from the delegate.
        '''
        self.subscribers.remove(function)

    def emit(self, *args):
        for function in self.subscribers:
            function(args)

class CollectionElement():

    @staticmethod
    def diff(elementA, elementB):
        '''
        diff Diff elements

        Args:
            elementA (CollectionElement): Original Element
            elementB (CollectionElement): New Element

        Returns:
            list: List of changes
        '''
        return list(difflib(elementA.toDict(), elementB.toDict()))

    @staticmethod
    def fromDict(inDict : dict):
        '''
        fromDict Creates Collection Element from dict

        Args:
            inDict (dict): Dictionary to parse

        Returns:
            CollectionElement: Element
        '''
        e = CollectionElement()

        # Identifiers 
        e.uuid = uuid.UUID(inDict['uuid'])
        
        # Fields are used to denote public and private fields 
        e.public = inDict['public']
        e.private = inDict['private']

        # Time tracking 
        e.createDate = inDict['createDate']
        e.updateDate = inDict['updateDate']

        return e

    @staticmethod
    def fromStr(inStr : str):
        '''
        fromStr Creates Collection Element from str

        Args:
            inStr (str): Input String

        Returns:
            CollectionElement: Element
        '''
        return CollectionElement.fromDict(json.loads(str))

    @staticmethod
    def copy(element):
        '''
        copy Create a copy of an element

        Args:
            element (CollectionElement): Element to copy

        Returns:
            CollectionElement: Copied Element
        '''
        return CollectionElement.fromDict(element.toDict())

    def __init__(self) -> None:

        # Identifiers 
        self.uuid = uuid.uuid4()
        
        # Fields are used to denote public and private fields 
        self.public = {}
        self.private = {'tags' : []}

        # Time tracking 
        self.createDate = self.generateCreateTime()
        self.updateDate = self.createDate

        # Delegate
        self.anyAttributeChanged = Delegate()

    def generateCreateTime(self):
        '''
        generateCreateTime Generate the current time

        Returns:
            str: Current Time
        '''
        return datetime.now().strftime("%m/%d/%y %H:%M:%S")

    def toDict(self) -> dict:
        '''
        toDict Serialize to dict

        Returns:
            dict: serialized dict
        '''
        d = {}
        d['uuid'] = str(self.uuid)
        d['public'] = self.public
        d['private'] = self.private
        d['createDate'] = self.createDate
        d['updateDate'] = self.updateDate
        return d

    def __setattr__(self, key, value):
        if hasattr(self, key):
            if key not in ['updateDate'] and value != self.__getattribute__(key):
                self.updateDate = self.generateCreateTime()
                self.anyAttributeChanged.emit(key, value)
        super().__setattr__(key, value)

    def __repr__(self) -> str:
        return str(self.uuid)

    def __str__(self) -> str:
        return json.dumps(self.toDict())

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CollectionElement):
            return self.toDict() == __o.toDict()
        elif isinstance(__o, dict):
            warnings.warn("Warning: instance {} is dict, not Element.".format(__o))
            return self.toDict() == __o
        elif isinstance(__o, str):
            warnings.warn("Warning: instance {} is str, not Element.".format(__o))
            return str(self) == __o

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.toDict())))