
from enum import Enum
from BBData.Scope import ScopeManager

class PluginRole(Enum):
    NONE = 0
    PATHING = 1
    IMPORT = 2
    EXPORT = 3

class PluginBase():

    name = ''
    author = ''
    description = ''
    version = ''
    role = PluginRole.NONE

    def initialize(*args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

    def onexit(self, *args, **kwargs):
        pass