
from typing import Callable
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from pkgutil import ModuleInfo
from pkgutil import iter_modules

from importlib import import_module

from wx import ICON_ERROR
from wx import OK

from wx import MessageDialog
from wx import NewIdRef
from wx import BeginBusyCursor
from wx import EndBusyCursor

from wx import Yield as wxYield

from core.IOPluginInterface import IOPluginInterface
from core.IPluginAdapter import IPluginAdapter
from core.Singleton import Singleton

from core.ToolPluginInterface import ToolPluginInterface
from core.types.PluginDataTypes import IOPluginMap
from core.types.PluginDataTypes import IOPluginMapType
from core.types.PluginDataTypes import PluginList
from core.types.PluginDataTypes import PluginIDMap
from core.types.PluginDataTypes import PluginType

import plugins.io
import plugins.tools

TOOL_PLUGIN_NAME_PREFIX: str = 'Tool'
IO_PLUGIN_NAME_PREFIX:   str = 'IO'


class PluginManager(Singleton):
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

    def init(self,  *args, **kwargs):
        """
        Expects a pluginAdapter parameter in kwargs
        Args:
            *args:
            **kwargs:
        """

        self.logger: Logger = getLogger(__name__)

        # These are built later on
        self._toolPluginsIDMap:   PluginIDMap  = cast(PluginIDMap, None)
        self._inputPluginsIDMap:  PluginIDMap  = cast(PluginIDMap, None)
        self._outputPluginsIDMap: PluginIDMap  = cast(PluginIDMap, None)
        self._inputPluginsMap:    IOPluginMap  = cast(IOPluginMap, None)
        self._outputPluginsMap:   IOPluginMap  = cast(IOPluginMap, None)

        self._ioPluginClasses:   PluginList = PluginList([])
        self._toolPluginClasses: PluginList = PluginList([])

        self._loadIOPlugins()
        self._loadToolPlugins()

        self._pluginAdapter: IPluginAdapter = kwargs['pluginAdapter']

    @property
    def inputPlugins(self) -> PluginList:
        """
        Get the input plugins.

        Returns:  A list of classes (the plugins classes).
        """

        pluginList = cast(PluginList, [])
        for plugin in self._ioPluginClasses:
            pluginClass = cast(type, plugin)
            classInstance = pluginClass(None)
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
            classInstance = pluginClass(None)
            if classInstance.outputFormat is not None:
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
    def toolPluginsIDMap(self) -> PluginIDMap:
        if self._toolPluginsIDMap is None:
            self._toolPluginsIDMap = self.__mapWxIdsToPlugins(self.toolPlugins)
        return self._toolPluginsIDMap

    @property
    def inputPluginsIDMap(self) -> PluginIDMap:
        if self._inputPluginsIDMap is None:
            self._inputPluginsIDMap = self.__mapWxIdsToPlugins(self.inputPlugins)
        return self._inputPluginsIDMap

    @property
    def outputPluginsIDMap(self) -> PluginIDMap:
        if self._outputPluginsIDMap is None:
            self._outputPluginsIDMap = self.__mapWxIdsToPlugins(self.outputPlugins)
        return self._outputPluginsIDMap

    @property
    def inputPluginsMap(self) -> IOPluginMap:

        if self._inputPluginsMap is None:
            self._inputPluginsMap = IOPluginMap()

            self._inputPluginsMap.mapType     = IOPluginMapType.INPUT_MAP
            self._inputPluginsMap.pluginIdMap = self.__mapWxIdsToPlugins(self.inputPlugins)

        return self._inputPluginsMap

    @property
    def outputPluginsMap(self) -> IOPluginMap:

        if self._outputPluginsMap is None:
            self._outputPluginsMap = IOPluginMap()

            self._outputPluginsMap.mapType     = IOPluginMapType.OUTPUT_MAP
            self._outputPluginsMap.pluginIdMap = self.__mapWxIdsToPlugins(self.outputPlugins)

        return self._outputPluginsMap

    def doToolAction(self, wxId: int):
        """

        Args:
            wxId:   The ID ref of the menu item
        """

        pluginMap: PluginIDMap = self.toolPluginsIDMap

        # TODO: Fix this later for mypy
        clazz: type = pluginMap[wxId]   # type: ignore
        # Create a plugin instance
        pluginInstance: ToolPluginInterface = clazz(pluginAdapter=self._pluginAdapter)

        if pluginInstance.setOptions() is True:
            # Do plugin functionality
            BeginBusyCursor()
            try:
                pluginInstance.doAction()
                self.logger.debug(f"After tool plugin do action")
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')
            EndBusyCursor()

    def doImport(self, wxId: int):
        """

        Args:
            wxId:       The ID ref of the menu item
        """
        idMap:        PluginIDMap       = self.inputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(pluginAdapter=self._pluginAdapter)
        self._doIOAction(methodToCall=plugInstance.executeImport)

    def doExport(self, wxId: int):
        pass
        """

        Args:
            wxId:       The ID ref of the menu item
        """
        idMap:        PluginIDMap      = self.outputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(pluginAdapter=self._pluginAdapter)
        self._doIOAction(methodToCall=plugInstance.executeExport)

    def _doIOAction(self, methodToCall: Callable):
        """
        Args:
            methodToCall:
        """

        try:
            wxYield()
            methodToCall()
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            booBoo: MessageDialog = MessageDialog(parent=None,
                                                  message=f'An error occurred while executing the selected plugin - {e}',
                                                  caption='Error!', style=OK | ICON_ERROR)
            booBoo.ShowModal()

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

                self.logger.debug(f'{type(pluginClass)=}')
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
