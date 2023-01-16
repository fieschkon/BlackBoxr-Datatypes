
from enum import Enum
from BBData.Scope import ScopeManager

class PluginRole(Enum):
    NONE = 0
    PATHING = 1
    IMPORT = 2
    EXPORT = 3

class PluginBase():

    def __init__(self, scope : ScopeManager, name = '', author = '', description = '', version = '', role = PluginRole.NONE) -> None:
        self.scope = scope
        self.name = name
        self.author = author
        self.description = description
        self.version = version
        self.role = role

    def run(self, *args, **kwargs):
        pass

    def onexit(self, *args, **kwargs):
        pass