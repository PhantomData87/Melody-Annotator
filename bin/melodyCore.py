from sys import path as mod
from os.path import abspath as ful
mod.insert(0, ful('../plugins')) # To include the other directory to have working plugins
import pluginMediator as pm

# For a globally defined plugin mediator
plug = plugs()

class tkInterface():
    def __init__(self):
        pass

    class menubar():
        def file(self):
            pass
        def edit(self):
            pass
        def view(self):
            pass
        def share(self):
            pass
        def pluginsConfigUI(self):
            pass

    class scrollSelector():
        def __init__(self):
            pass
        def fileOptions(self):
            pass
        def colorOptions(self):
            pass
        def UIOptions(Self):
            pass
    
    class actionBar():
        def __init__(self):
            pass
        def debugListen(self):
            pass
        def listener(self):
            pass
        def buttonUI(self):
            pass
        def keyBinds(self):
            pass
    
    def markdown(self):
        pass

    def pluginEdit(self):
        pass

    def run(self):
        pass

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