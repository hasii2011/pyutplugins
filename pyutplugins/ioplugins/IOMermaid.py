
from typing import cast

from logging import Logger
from logging import getLogger

from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.plugintypes.ExportDirectoryResponse import ExportDirectoryResponse
from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName


FORMAT_NAME:        FormatName = FormatName('Mermaid')
PLUGIN_EXTENSION:   PluginExtension = PluginExtension('mer')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Export Ogl to Mermaid')


class IOMermaid(IOPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._requireSelection = False      # Override base class

        # from super class
        self._name    = PluginName('Mermaid Writer')
        self._author  = 'Humberto A. Sanchez II'
        self._version = '0.50'
        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectoryName: str = ''

    def setImportOptions(self) -> bool:
        return False

    def setExportOptions(self) -> bool:
        response: ExportDirectoryResponse = self.askForExportDirectoryName(preferredDefaultPath=None)
        if response.cancelled is True:
            return False
        else:
            self._exportDirectoryName = response.directoryName

        return True

    def read(self) -> bool:
        return False

    def write(self, oglObjects: OglObjects):
        directoryName: str        = self._exportDirectoryName
        self.logger.warning(f'TODO:  export to {directoryName}')
