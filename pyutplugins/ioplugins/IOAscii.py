
from typing import cast

from logging import Logger
from logging import getLogger

from pyutplugins.coreinterfaces.IOPluginInterface import IOPluginInterface
from pyutplugins.coreinterfaces.IPluginAdapter import IPluginAdapter

from pyutplugins.coretypes.InputFormat import InputFormat
from pyutplugins.coretypes.OutputFormat import OutputFormat

from pyutplugins.coretypes.PluginDataTypes import FormatName
from pyutplugins.coretypes.PluginDataTypes import PluginDescription
from pyutplugins.coretypes.PluginDataTypes import PluginExtension
from pyutplugins.coretypes.PluginDataTypes import PluginName

from pyutplugins.CoreTypes import OglObjects


FORMAT_NAME:        FormatName       = FormatName('Ascii')
PLUGIN_EXTENSION:   PluginExtension  = PluginExtension('acl')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Export OGL as ASCII')


class IOAscii(IOPluginInterface):
    """
    Write ASCII and can read ASCII
    This just the skeleton.  Not sure if I want to do this
    """

    def __init__(self, pluginAdapter: IPluginAdapter):
        """

        Args:
            pluginAdapter:   A class that implements IPluginAdapter
        """
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('ASCII Class Export')
        self._author    = 'Philippe Waelti & Humberto A. Sanchez I>'
        self._version   = '2.0'

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

    def setImportOptions(self) -> bool:
        """
        We do not support import
        Returns:  False
        """
        return True

    def setExportOptions(self) -> bool:
        return True

    def read(self) -> bool:
        return False

    def write(self, oglObjects: OglObjects):
        pass