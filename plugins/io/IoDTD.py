
from typing import cast

from pyutplugincore.ICommunicator import ICommunicator
from pyutplugincore.IOPluginInterface import IOPluginInterface

from pyutplugincore.coretypes.Helper import OglClasses
from pyutplugincore.coretypes.InputFormat import InputFormat
from pyutplugincore.coretypes.OutputFormat import OutputFormat

from pyutplugincore.coretypes.PluginDataTypes import PluginDescription
from pyutplugincore.coretypes.PluginDataTypes import PluginExtension
from pyutplugincore.coretypes.PluginDataTypes import PluginName
from pyutplugincore.coretypes.SingleFileRequestResponse import SingleFileRequestResponse

PLUGIN_NAME:        PluginName        = PluginName("DTD")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('dtd')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('W3C DTD 1.0 file format')


class IoDTD(IOPluginInterface):

    def __init__(self, communicator: ICommunicator, oglClasses: OglClasses):
        super().__init__(communicator, oglClasses)

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

    def read(self) -> OglClasses:
        pass

    def write(self, oglClasses: OglClasses):
        """

        Args:
            oglClasses:

        Returns:  False, write not supported

        """
        return None
