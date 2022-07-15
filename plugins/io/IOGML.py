
from typing import cast

from logging import Logger
from logging import getLogger

from plugins.common.Types import OglClasses
from plugins.io.gml.GMLExporter import GMLExporter

from core.IOPluginInterface import IOPluginInterface
from core.ICommunicator import ICommunicator

from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName
from core.types.SingleFileRequestResponse import SingleFileRequestResponse


PLUGIN_NAME:        PluginName = PluginName('GML')
PLUGIN_EXTENSION:   PluginExtension = PluginExtension('gml')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Graph Modeling Language - Portable Format for Graphs')


class IOGML(IOPluginInterface):
    """
    Sample class for input/output plug-ins.
    """
    def __init__(self, communicator: ICommunicator):
        """

        Args:
            communicator:   A class that implements ICommunicator
        """
        super().__init__(communicator=communicator)

        self.logger: Logger = getLogger(__name__)

        self._name    = 'Output GML'
        self._author  = "Humberto A. Sanchez II"
        self._version = GMLExporter.VERSION

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(name=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

    def setImportOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            if False, the import will be cancelled.
        """
        return False

    def setExportOptions(self) -> bool:
        """
        Prepare the export.
        This can be used to ask the user some questions

        Returns:
            if False, the export is cancelled.
        """
        self._exportResponse = self.askForFileToExport()

        if self._exportResponse.cancelled is True:
            return False
        else:
            return True

    def read(self) -> bool:
        """
        Read data from filename.
        """
        return False

    def write(self, oglClasses: OglClasses):
        """
        Write data

        Args:
            oglClasses:     list of exported objects
        """
        gmlExporter: GMLExporter = GMLExporter()

        gmlExporter.translate(umlObjects=oglClasses)

        gmlExporter.write(self._exportResponse.fileName)
