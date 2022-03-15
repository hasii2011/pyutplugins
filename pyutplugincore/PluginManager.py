
from logging import Logger
from logging import getLogger
from typing import List

from pyutplugincore.coretypes.PluginDataTypes import PluginMap


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
    By convention prefix the plugin I/O module with the characters "IO"

    The following are valid plugin specifications

    ToolPlugin=arrangelinks.ToolArrangeLinks
    IOPlugin=-iopython.IOPython

    """

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        # These are built later on
        self._toolPluginsMenu = None
        self._ioPluginsMenu   = None

    def loadToolPlugins(self):
        pass

    def loadIOPlugins(self):
        pass

    @property
    def toolPluginsMenu(self) -> PluginMap:
        return self._toolPluginsMenu

    @property
    def ioPluginsMenu(self) -> PluginMap:
        return self._ioPluginsMenu

    def _findPluginLoaderFiles(self, pathsToSearch: List[str]):
        """

        Args:
            pathsToSearch:   Fully qualified paths to search for plugin loader files

        Returns:
        """
        pass
