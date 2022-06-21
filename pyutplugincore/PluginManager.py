
from typing import Callable
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from pkgutil import ModuleInfo
from pkgutil import iter_modules

from importlib import import_module

from wx import NewIdRef

from pyutplugincore.coretypes.PluginDataTypes import PluginList
from pyutplugincore.coretypes.PluginDataTypes import PluginIDMap

import plugins.io
import plugins.tools
from pyutplugincore.coretypes.PluginDataTypes import PluginType

TOOL_PLUGIN_NAME_PREFIX: str = 'Tool'
IO_PLUGIN_NAME_PREFIX:   str = 'IO'


class PluginManager:
    """
    Is responsible for:

    * Finding the plugin loader files
    * Creating tool and Input/Output Menu Items
    * Providing the callbacks to invoke the appropriate methods on the
    appropriate plugins to invoke there functionality.

    Plugin Loader files have the following format:

    ToolPlugin=packageName.PluginModule
    IOPlugin=packageName.PluginModule

    By convention prefix the plugin tool module name with the characters 'Tool'
    By convention prefix the plugin I/O module with the characters 'IO'

    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        # These are built later on
        self._toolPluginsMenu: PluginIDMap = cast(PluginIDMap, None)
        self._ioPluginsMenu:   PluginIDMap = cast(PluginIDMap, None)

        self._ioPluginClasses:   PluginList = PluginList([])
        self._toolPluginClasses: PluginList = PluginList([])

        self._loadIOPlugins()
        self._loadToolPlugins()

    @property
    def inputPlugins(self) -> PluginList:
        """
        Get the input plugins.

        Returns:  A list of classes (the plugins classes).
        """

        pluginList = cast(PluginList, [])
        for plugin in self._ioPluginClasses:
            pluginClass = cast(type, plugin)
            classInstance = pluginClass(None, None)
            if classInstance.inputFormat is not None:
                pluginList.append(plugin)
        return pluginList

    @property
    def outputPlugins(self) -> PluginList:
        """
        Get the output plugins.

        Returns:  A list of classes (the plugins classes).
        """
        pluginList = cast(PluginList, [])
        for plugin in self._ioPluginClasses:
            pluginClass = cast(type, plugin)
            classInstance = pluginClass(None, None)
            if classInstance.outputFormat() is not None:
                pluginList.append(plugin)
        return pluginList

    @property
    def toolPlugins(self) -> PluginList:
        """
        Get the tool plugins.

        Returns:    A list of classes (the plugins classes).
        """
        return self._toolPluginClasses

    @property
    def toolPluginsMenu(self) -> PluginIDMap:
        if self._toolPluginsMenu is None:
            self._toolPluginsMenu = self.__mapWxIdsToPlugins(self._toolPluginClasses)
        return self._toolPluginsMenu

    @property
    def ioPluginsMenu(self) -> PluginIDMap:
        return self._ioPluginsMenu

    def _loadIOPlugins(self):
        self._ioPluginClasses = self.__loadPlugins(plugins.io)

    def _loadToolPlugins(self):
        self._toolPluginClasses = self.__loadPlugins(plugins.tools)

    def _iterateNameSpace(self, pluginPackage):
        self.logger.debug(f'{dir(pluginPackage)}')
        return iter_modules(pluginPackage.__path__, pluginPackage.__name__ + ".")

    def __loadPlugins(self, pluginPackage) -> PluginList:

        pluginList: PluginList = PluginList([])
        for info in self._iterateNameSpace(pluginPackage):
            moduleInfo: ModuleInfo = cast(ModuleInfo, info)

            loadedModule = import_module(moduleInfo.name)

            moduleName:  str      = moduleInfo.name
            className:   str      = self.__computePluginClassNameFromModuleName(moduleName=moduleName)
            if className.startswith(IO_PLUGIN_NAME_PREFIX) is True or className.startswith(TOOL_PLUGIN_NAME_PREFIX):

                pluginClass: Callable = getattr(loadedModule, className)

                self.logger.warning(f'{type(pluginClass)=}')
                pluginList.append(cast(PluginType, pluginClass))
        return pluginList

    def __computePluginClassNameFromModuleName(self, moduleName: str) -> str:
        """
        Typical module names are:
            * plugins.io.IoDTD
            * plugins.tools.ToAscii
        Args:
            moduleName: A fully qualified module name

        Returns: A string that is the contained class name
        """

        splitName: List[str] = moduleName.split('.')
        className: str       = splitName[len(splitName) - 1]

        return className

    def __mapWxIdsToPlugins(self, pluginList: PluginList) -> PluginIDMap:

        pluginMap: PluginIDMap = cast(PluginIDMap, {})

        nb: int = len(pluginList)

        for x in range(nb):
            wxId: int = NewIdRef()

            pluginMap[wxId] = pluginList[x]

        return pluginMap
