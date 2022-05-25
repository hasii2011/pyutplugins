from pkgutil import ModuleInfo
from pkgutil import iter_modules

from importlib import import_module
from typing import cast

import gists.io
import gists.tools


class PluginManager:

    def __init__(self):
        self.loadIOPlugins()
        self.loadToolPlugins()

    def loadIOPlugins(self):
        self._loadPlugins(gists.io)

    def loadToolPlugins(self):
        self._loadPlugins(gists.tools)

    def _loadPlugins(self, pluginPackage):
        for info in self._iterateNameSpace(pluginPackage):
            moduleInfo: ModuleInfo = cast(ModuleInfo, info)
            loadedModule = import_module(moduleInfo.name)
            print(f'{dir(loadedModule)=}')
            print(f'{loadedModule.__name__=}')

    def _iterateNameSpace(self, pluginPackage):
        print(f'{dir(pluginPackage)}')
        return iter_modules(pluginPackage.__path__, pluginPackage.__name__ + ".")


pm: PluginManager = PluginManager()


