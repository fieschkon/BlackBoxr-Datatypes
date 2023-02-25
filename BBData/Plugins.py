
from enum import Enum

class PluginRole(Enum):
    NONE = 0
    PATHING = 1
    IMPORT = 2
    EXPORT = 3

class PluginBase():

    name : str = ''
    author : str = ''
    description : str = ''
    version : str = ''
    requires : list[str] = []
    role = PluginRole.NONE

    def initialize(*args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

    def onexit(self, *args, **kwargs):
        pass