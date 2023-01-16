import copy
from enum import Enum

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

class Field():

    def fromDict(indict : dict):
        return Field(fieldname = indict['name'])

    def __init__(self, fieldname : str = 'Default Field Name') -> None:
        self.name = fieldname
        self.type = FieldType.NONE

    def toDict(self):
        d = {}
        d['name'] = self.name
        d['type'] = self.type.value
        return copy.deepcopy(d)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Field):
            return self.toDict() == __o.toDict()
        return False

class Checks(Field):

    def fromDict(indict: dict):
        c = Checks(indict['options'], fieldname = indict['name'])
        return c

    def __init__(self, options : list[tuple[int, str, bool]], fieldname : str = 'Default Checkbox Field') -> None:
        super().__init__(fieldname)
        self.type = FieldType.CHECKS

        self.stateChanged = Delegate()
        if isinstance(options, dict):
            self.options = options
        else:
            self.options = {tup[0] : {'name' : tup[1] , 'state' : tup[2]} for tup in options}

    def setOption(self, index : int, state : bool):
        self.options[index]['state'] = state
        self.stateChanged.emit(index, self.options[index]['name'], self.options[index]['state'])

    def getOption(self, index : int):
        return self.options[index]['name'], self.options[index]['state']

    def toDict(self):
        d = super().toDict()
        d['options'] = self.options
        return d

class Radio(Checks):

    def fromDict(indict: dict):
        c = Radio(indict['options'], maximumAllowedChecks=indict['maxallowed'], fieldname = indict['name'])
        return c

    def __init__(self, options: list[tuple[int, str, bool]], maximumAllowedChecks = 1 , fieldname: str = 'Default Checkbox Field') -> None:
        super().__init__(options, fieldname)
        self.type = FieldType.RADIO
        if maximumAllowedChecks == -1:
            # Auto calculate allowed numbers
            self.maxAllowed = len([item for item in options if item[2]])
        else:
            self.maxAllowed = maximumAllowedChecks
        self.stateChanged.connect(self.disableOtherOptions)
        
    def disableOtherOptions(self, args):
        # args[0] # index
        for key in list(self.options.keys()):
            if key != args[0]:
                self.options[key]['state'] = False

    def toDict(self):
        d = super().toDict()
        d['maxallowed'] = self.maxAllowed
        return d


class ShortText(Field):

    def fromDict(indict: dict):
        return ShortText(fieldname=indict['name'], defaultText=indict['text'])

    def __init__(self, fieldname: str = 'Default ShortText Name', defaultText = '') -> None:
        super().__init__(fieldname)
        self.type = FieldType.LINETEXT
        self.text = defaultText

    def toDict(self):
        d = super().toDict()
        d['text'] = self.text
        return d

class LongText(Field):

    def fromDict(indict: dict):
        return LongText(fieldname=indict['name'], defaultText=indict['text'])

    def __init__(self, fieldname: str = 'Default LongText Name', defaultText='') -> None:
        super().__init__(fieldname)
        self.type = FieldType.LONGTEXT
        self.text = defaultText
    
    def toDict(self):
        d = super().toDict()
        d['type'] = self.type.value
        d['text'] = self.text
        return d