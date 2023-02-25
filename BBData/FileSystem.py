import os
from types import NoneType

from BBData.utilities import first, getFilesWithExtension

class Tree():
    def __init__(self) -> None:
        self.nodes = []

    def print(self):
        for node in self.nodes:
            print(node.printable())

    def addNode(self, node):
        nodeids = [existingnode.uuid for existingnode in self.nodes]
        if node.uuid not in nodeids:
            self.nodes.append(node)

    def getNode(self, id):
        return first([node.uuid for node in self.nodes if node.uuid == id])

class TreeNode():
    def __init__(self,id : str, tree = None, parent = None) -> None:
        self.uuid = id
        self.parent = parent
        self.tree = tree
        if tree != None:
            self.tree.addNode(self)

        
    def getPath(self):
        if isinstance(self.parent, NoneType):
            return f'{os.sep}{self.uuid}'
        else:
            return f'{self.parent.getPath()}{os.sep}{self.uuid}'

    def printable(self) -> str:
        if isinstance(self.parent, NoneType):
            return f'{os.sep}{self.name}'
        else:
            return f'{self.parent.printable()}{os.sep}{self.name}'
