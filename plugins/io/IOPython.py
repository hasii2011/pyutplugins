
from typing import List

from core.ICommunicator import ICommunicator
from core.IOPluginInterface import IOPluginInterface

from core.types.InputFormat import InputFormat
from core.types.MultipleFileRequestResponse import MultipleFileRequestResponse
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import FormatName
from plugins.common.Types import OglClasses

PLUGIN_NAME:        FormatName        = FormatName("Python File(s)")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('py')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Python code generation and reverse engineering')


class IOPython(IOPluginInterface):

    def __init__(self, communicator: ICommunicator):
        super().__init__(communicator)

        # from super class
        self._name    = FormatName('IOPython')
        self._author  = 'Humberto A. Sanchez II'
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._filesToImport: List['str'] = []

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file name

        Returns:  'True', we support import
        """
        response: MultipleFileRequestResponse = self.askToImportMultipleFiles()
        if response.cancelled is True:
            return False
        else:
            self._filesToImport = response.fileList

        return True

    def setExportOptions(self) -> bool:
        return False

    def read(self) -> bool:
        pass

    def write(self, oglClasses: OglClasses):
        pass
