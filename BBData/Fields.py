import copy
from enum import Enum
from typing import Union

from BBData.Delegate import Delegate


class FieldType(Enum):
    '''
    FieldType for interpreting serialization
    '''
    NONE = 0
    LINETEXT = 1
    LONGTEXT = 2
    CHECKS = 3
    RADIO = 4
    ENUM = 5

class Field():

    def fromDict(indict : dict):
        return Field(fieldname = indict['name'])

    def __init__(self, fieldname : str = 'Default Field Name') -> None:
        self.name = fieldname
        self.type = FieldType.NONE
        self.fieldChanged = Delegate()

    def toDict(self):
        d = {}
        d['name'] = self.name
        d['type'] = self.type.value
        return copy.deepcopy(d)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Field):
            return self.toDict() == __o.toDict()
        return False

    def __str__(self) -> str:
        return str(self.name)

    def reconcile(self, templatefield):
        self.name = templatefield.name
        if not isinstance(templatefield, type(self)):
            raise TypeError

class Enum(Field):

    def fromDict(indict: dict):
        c = Enum(indict['options'], default= indict['default'], fieldname = indict['name'])
        c.currentItem = indict['currentItem']
        return c

    def __init__(self, options : list[str], default : str, fieldname : str = 'Default Enum Field') -> None:
        super().__init__(fieldname)
        self.type = FieldType.ENUM

        self.stateChanged = Delegate()
        self.options = options
        self.default = default
        self.currentItem = self.default

    def getCurrent(self):
        return self.currentItem

    def __str__(self) -> str:
        return f'{super().__str__()}\n\t{self.currentItem} / {str(self.options)}'

    def getIndexFromStr(self, option : str):
        return self.options.index(option)

    def setCurrent(self, index : Union[int, str]):
        if isinstance(index, int):
            self.currentItem = self.options[index]
        else:
            self.currentItem = index

    def toDict(self):
        d = super().toDict()
        d['options'] = self.options
        d['default'] = self.default
        d['currentItem'] = self.currentItem
        return d

    def reconcile(self, templatefield):
        super().reconcile(templatefield)
        self.options = templatefield.options
        self.default = templatefield.default
        if self.currentItem not in self.options:
            self.currentItem = self.default

class Checks(Field):

    def fromDict(indict: dict):
        c = Checks(indict['options'], fieldname = indict['name'])
        return c

    def __init__(self, options : dict[str : bool], fieldname : str = 'Default Checkbox Field') -> None:
        super().__init__(fieldname)
        self.type = FieldType.CHECKS

        self.stateChanged = Delegate()
        self.options = options

    def __str__(self) -> str:
        reppr = f'{super().__str__()}\n'
        for key, value in self.options.items():
            valuerep = 'x' if value else ' '
            reppr += f'\t[{valuerep}] {key}'
        return 

    def setOption(self, name : Union[str, int], state : bool):
        '''
        Sets the state of a field from the index or name of field.

        Args:
            name (Union[str, int]): Either the name of the field or the index.
            state (bool): New state
        '''
        if isinstance(name, str):
            self.options[name] = state
            self.stateChanged.emit(self, name, state)
            self.fieldChanged.emit(self, name)
        else:
            key = list(self.options.keys())[name]
            self.options[key] = state
            self.stateChanged.emit(self, key, state)
            self.fieldChanged.emit(self, key)

    def getOption(self, name : Union[str, int]):
        '''
        Gets the state from the index or name of field.

        Args:
            name (Union[str, int]): Either the name of the field or the index.

        Returns:
            bool: The state of the field
        '''
        if isinstance(name, str):
            return self.options[name]
        else:
            return self.options[list(self.options.keys())[name]]

    def toDict(self):
        d = super().toDict()
        d['options'] = self.options
        return d

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Checks):
            return self.toDict() == __o.toDict()
        return False

    def reconcile(self, templatefield):
        super().reconcile(templatefield)
        newkeys = templatefield.options.items()
        currentkeys = list(self.options.keys())
        for newkey, newvalue in newkeys:
            if newkey not in currentkeys:
                self.options[newkey] = newvalue
            elif newvalue == True:
                self.options[newkey] = newvalue

class Radio(Checks):

    def fromDict(indict: dict):
        c = Radio(indict['options'], maximumAllowedChecks=indict['maxallowed'], fieldname = indict['name'])
        return c

    def __init__(self, options: dict[str : bool], maximumAllowedChecks : int = 1 , fieldname: str = 'Default Checkbox Field') -> None:
        super().__init__(options, fieldname)
        self.type = FieldType.RADIO
        if maximumAllowedChecks == -1:
            # Auto calculate allowed numbers
            self.maxAllowed = len([item for item in options if item[2]])
        else:
            self.maxAllowed = maximumAllowedChecks
        self.stateChanged.connect(self.disableOtherOptions)
        
    def disableOtherOptions(self, args):
        # args[1] # index
        for key, value in self.options.items():
            if key != args[1]:
                self.options[key] = False
        self.fieldChanged.emit(self)

    def toDict(self):
        d = super().toDict()
        d['maxallowed'] = self.maxAllowed
        return d

    def reconcile(self, templatefield):
        newkeys = templatefield.options.items()
        currentkeys = list(self.options.keys())
        for newkey, newvalue in newkeys:
            if newkey not in currentkeys:
                self.options[newkey] = newvalue


class ShortText(Field):

    def fromDict(indict: dict):
        return ShortText(fieldname=indict['name'], defaultText=indict['text'])

    def __init__(self, fieldname: str = 'Default ShortText Name', defaultText = '') -> None:
        super().__init__(fieldname)
        self.type = FieldType.LINETEXT
        self.__text = defaultText

    def __str__(self) -> str:
        return f'{super().__str__()}\n\t{self.text()}'

    def setText(self, text):
        self.__text = text
        self.fieldChanged.emit(self)

    def text(self):
        return self.__text

    def toDict(self):
        d = super().toDict()
        d['text'] = self.__text
        return d

class LongText(ShortText):

    def fromDict(indict: dict):
        return LongText(fieldname=indict['name'], defaultText=indict['text'])

    def __init__(self, fieldname: str = 'Default LongText Name', defaultText='') -> None:
        super().__init__(fieldname)
        self.type = FieldType.LONGTEXT
        self.setText(defaultText)
    
    def toDict(self):
        d = super().toDict()
        d['type'] = self.type.value
        d['text'] = self.text()
        return d

def parseField(indict : dict) -> Union[ShortText, LongText, Checks, Radio, Enum]:
    match indict['type']:

        case FieldType.LINETEXT.value:
            return ShortText.fromDict(indict)

        case FieldType.LONGTEXT.value:
            return LongText.fromDict(indict)

        case FieldType.CHECKS.value:
            return Checks.fromDict(indict)

        case FieldType.RADIO.value:
            return Radio.fromDict(indict)

        case FieldType.ENUM.value:
            return Enum.fromDict(indict)
