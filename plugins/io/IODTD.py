
from typing import cast

from plugins.common.Types import OglClasses
from plugins.common.Types import OglLinks
from plugins.io.dtd.DTDParser import DTDParser

from core.ICommunicator import ICommunicator
from core.IOPluginInterface import IOPluginInterface

from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat

from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import FormatName
from core.types.SingleFileRequestResponse import SingleFileRequestResponse

PLUGIN_NAME:        FormatName        = FormatName("DTD")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('dtd')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('W3C DTD 1.0 file format')


class IODTD(IOPluginInterface):

    def __init__(self, communicator: ICommunicator):
        super().__init__(communicator)

        # from super class
        self._name    = 'IoDTD'
        self._author  = "C.Dutoit <dutoitc@hotmail.com>"
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = cast(OutputFormat, None)

        self._fileToImport: str = ''

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file name

        Returns:  'True', we support import
        """
        response: SingleFileRequestResponse = self.askForFileToImport()
        if response.cancelled is True:
            return False
        else:
            self._fileToImport = response.fileName

        return True

    def setExportOptions(self) -> bool:
        return False

    def read(self) -> bool:
        """

        Returns:  True if import succeeded, False if error or cancelled
        """
        filename: str = self._fileToImport

        dtdParser: DTDParser = DTDParser()

        dtdParser.open(filename=filename)

        oglClasses: OglClasses = dtdParser.oglClasses
        for oglClass in oglClasses:
            self._communicator.addShape(oglClass)

        oglLinks: OglLinks = dtdParser.links
        for oglLink in oglLinks:
            self._communicator.addShape(oglLink)

        self._communicator.refreshFrame()

        return True

    def write(self, oglClasses: OglClasses):
        """

        Args:
            oglClasses:

        Returns:  False, write not supported

        """
        return False
