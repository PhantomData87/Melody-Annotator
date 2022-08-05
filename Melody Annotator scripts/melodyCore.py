#Adding plugins
from sys import path as mod
from os.path import abspath as ful
mod.insert(0, ful('../plugins')) # To include the other directory to have working plugins
import pluginMediator as pm

#Gui


# For a globally defined plugin mediator
plug = pm.plugs()

class notes():
    def __init__(self):
        pass
    def organize(self):
        pass
    def pluginCheck(self):
        pass

class noteNode():
    def __init__(self, keyPair, localInfo, localFile):
        self._info = localInfo
        self._file = localFile
        self._identifiers = keyPair
        
        self._left = None
        self._right = None
        self._behind = None

if __name__ == "__main__":
    pass