
from typing import cast

from logging import Logger
from logging import getLogger


from plugins.tools.gml.GMLExporter import GMLExporter

from pyutplugincore.IOPluginInterface import IOPluginInterface
from pyutplugincore.ICommunicator import ICommunicator

from pyutplugincore.coretypes.Helper import OglClasses
from pyutplugincore.coretypes.InputFormat import InputFormat
from pyutplugincore.coretypes.OutputFormat import OutputFormat
from pyutplugincore.coretypes.PluginDataTypes import PluginDescription
from pyutplugincore.coretypes.PluginDataTypes import PluginExtension
from pyutplugincore.coretypes.PluginDataTypes import PluginName
from pyutplugincore.coretypes.SingleFileRequestResponse import SingleFileRequestResponse


class IoGML(IOPluginInterface):
    """
    Sample class for input/output plug-ins.
    """
    def __init__(self, communicator: ICommunicator, oglClasses: OglClasses):
        """

        Args:
            communicator:   A class that implements ICommunicator
            oglClasses:     The Pyut Ogl graphical classes that plugins manipulate
        """
        super().__init__(communicator=communicator, oglClasses=oglClasses)

        self.logger: Logger = getLogger(__name__)

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)

    @property
    def name(self) -> str:
        """
        Returns: the name of the plugin.
        """
        return "Output GML"

    @property
    def author(self) -> str:
        """
        Returns: The author's name
        """
        return "Humberto A. Sanchez II"

    @property
    def version(self) -> str:
        """
        Returns: The plugin version string
        """
        return GMLExporter.VERSION

    @property
    def inputFormat(self) -> InputFormat:
        """
        Returns:
            None, I don't read GML
        """
        return cast(InputFormat, None)

    @property
    def outputFormat(self) -> OutputFormat:
        """

        Returns:
            Return a specification tuple.
        """
        return OutputFormat(name=PluginName('GML'),
                            extension=PluginExtension('gml'),
                            description=PluginDescription('Graph Modeling Language - Portable Format for Graphs'))

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

    def read(self) -> OglClasses:
        """
        Read data from filename.
        """
        pass

    def write(self, oglClasses: OglClasses):
        """
        Write data

        Args:
            oglClasses:     list of exported objects
        """
        gmlExporter: GMLExporter = GMLExporter()

        gmlExporter.translate(umlObjects=oglClasses)

        gmlExporter.write(self._exportResponse.fileName)
