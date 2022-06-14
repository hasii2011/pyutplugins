from typing import Callable
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from pkgutil import ModuleInfo
from pkgutil import iter_modules

from importlib import import_module

from pyutplugincore.coretypes.PluginDataTypes import PluginList
from pyutplugincore.coretypes.PluginDataTypes import PluginMap

import plugins.io
import plugins.tools


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
    By convention prefix the plugin I/O module with the characters 'Io'

    """
    IO_PLUGINS:   PluginList = PluginList([])
    TOOL_PLUGINS: PluginList = PluginList([])

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        # These are built later on
        self._toolPluginsMenu = None
        self._ioPluginsMenu   = None

        self._loadIOPlugins()
        self._loadToolPlugins()

    @property
    def inputPlugins(self) -> PluginList:
        """
        Get the input plugins.

        Returns:  A list of classes (the plugins classes).
        """

        pluginList = cast(PluginList, [])
        for plug in self.IO_PLUGINS:
            obj = plug(None, None)
            if obj.getInputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    @property
    def outputPlugins(self) -> PluginList:
        """
        Get the output plugins.

        Returns:  A list of classes (the plugins classes).
        """
        pluginList = cast(PluginList, [])
        for plug in self.IO_PLUGINS:
            obj = plug(None, None)
            if obj.getOutputFormat() is not None:
                pluginList.append(plug)
        return pluginList

    @property
    def toolPlugins(self) -> PluginList:
        """
        Get the tool plugins.

        Returns:    A list of classes (the plugins classes).
        """
        return self.TOOL_PLUGINS

    @property
    def toolPluginsMenu(self) -> PluginMap:
        return self._toolPluginsMenu

    @property
    def ioPluginsMenu(self) -> PluginMap:
        return self._ioPluginsMenu

    def _loadIOPlugins(self):
        self.__loadPlugins(plugins.io)

    def _loadToolPlugins(self):
        self.__loadPlugins(plugins.tools)

    def _iterateNameSpace(self, pluginPackage):
        self.logger.debug(f'{dir(pluginPackage)}')
        return iter_modules(pluginPackage.__path__, pluginPackage.__name__ + ".")

    def __loadPlugins(self, pluginPackage):

        for info in self._iterateNameSpace(pluginPackage):
            moduleInfo: ModuleInfo = cast(ModuleInfo, info)

            loadedModule = import_module(moduleInfo.name)

            moduleName:  str      = moduleInfo.name
            className:   str      = self.__computePluginClassNameFromModuleName(moduleName=moduleName)
            if className.startswith('Io') is True or className.startswith('Tool'):

                pluginClass: Callable = getattr(loadedModule, className)

                self.logger.warning(f'{type(pluginClass)=}')

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
