import copy
from enum import Enum

from BBData.Delegate import Delegate


class FieldType(Enum):
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

    def toDict(self):
        d = {}
        d['name'] = self.name
        d['type'] = FieldType.NONE
        return copy.deepcopy(d)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Field):
            return self.toDict() == __o.toDict()
        return False

class Checks(Field):

    def fromDict(indict: dict):
        c = Checks(indict['name'])
        c.options = indict['options']

    def __init__(self, options : list[tuple[int, str, bool]], fieldname : str = 'Default Checkbox Field') -> None:
        super().__init__(fieldname)
        self.stateChanged = Delegate()
        self.options = {tup[0] : {'name' : tup[1] , 'state' : tup[2]} for tup in options}

    def setOption(self, index : int, state : bool):
        self.options[index]['state'] = state
        self.stateChanged.emit(index, self.options[index]['name'], self.options[index]['state'])

    def getOption(self, index : int):
        return self.options[index]['name'], self.options[index]['state']

    def toDict(self):
        d = super().toDict()
        d['type'] = FieldType.CHECKS
        d['options'] = self.options
        return d

class Radio(Checks):

    def fromDict(indict: dict):
        c = Radio(indict['name'])
        c.options = indict['options']
        c.maxAllowed = indict['maxallowed']

    def __init__(self, options: list[tuple[int, str, bool]], maximumAllowedChecks = 1 , fieldname: str = 'Default Checkbox Field') -> None:
        super().__init__(options, fieldname)
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
        d['type'] = FieldType.RADIO
        d['maxallowed'] = self.maxAllowed
        return d


class ShortText(Field):

    def fromDict(indict: dict):
        return ShortText(fieldname=indict['name'], defaultText=indict['text'])

    def __init__(self, fieldname: str = 'Default ShortText Name', defaultText = '') -> None:
        super().__init__(fieldname)
        self.text = defaultText

    def toDict(self):
        d = super().toDict()
        d['type'] = FieldType.LINETEXT
        d['text'] = self.text
        return d

class LongText(ShortText):

    def fromDict(indict: dict):
        return LongText(fieldname=indict['name'], defaultText=indict['text'])

    def __init__(self, fieldname: str = 'Default LongText Name', defaultText='') -> None:
        super().__init__(fieldname, defaultText)
    
    def toDict(self):
        d = super().toDict()
        d['type'] = FieldType.LONGTEXT
        return d