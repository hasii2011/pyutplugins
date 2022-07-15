
from typing import cast

from plugins.common.Types import OglClasses
from plugins.common.Types import OglLinks
from plugins.io.dtd.DTDParser import DTDParser

from pyutplugincore.ICommunicator import ICommunicator
from pyutplugincore.IOPluginInterface import IOPluginInterface

from pyutplugincore.coretypes.InputFormat import InputFormat
from pyutplugincore.coretypes.OutputFormat import OutputFormat

from pyutplugincore.coretypes.PluginDataTypes import PluginDescription
from pyutplugincore.coretypes.PluginDataTypes import PluginExtension
from pyutplugincore.coretypes.PluginDataTypes import PluginName
from pyutplugincore.coretypes.SingleFileRequestResponse import SingleFileRequestResponse

PLUGIN_NAME:        PluginName        = PluginName("DTD")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('dtd')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('W3C DTD 1.0 file format')


class IODTD(IOPluginInterface):

    def __init__(self, communicator: ICommunicator):
        super().__init__(communicator)

        # from super class
        self._name    = "IoDTD"
        self._author  = "C.Dutoit <dutoitc@hotmail.com>"
        self._version = '1.0'
        self._inputFormat  = InputFormat(name=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = cast(OutputFormat, None)

        self._fileToImport: str = ''

    def setImportOptions(self) -> bool:
        """
        We do not need to ask any questions

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
