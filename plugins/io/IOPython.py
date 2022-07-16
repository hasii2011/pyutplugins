
from typing import List

from logging import Logger
from logging import getLogger

from json import dumps as jsonDumps

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import ICON_ERROR
from wx import MessageBox
from wx import OK

from wx import Yield as wxYield

from core.ICommunicator import ICommunicator
from core.IOPluginInterface import IOPluginInterface

from core.types.InputFormat import InputFormat
from core.types.MultipleFileRequestResponse import MultipleFileRequestResponse
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import FormatName

from plugins.common.Types import OglClasses
from plugins.io.pythonsupport.ReverseEngineerPython2 import ReverseEngineerPython2

PLUGIN_NAME:        FormatName        = FormatName("Python File(s)")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('py')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Python code generation and reverse engineering')


class IOPython(IOPluginInterface):

    def __init__(self, communicator: ICommunicator):

        super().__init__(communicator)

        self.logger: Logger = getLogger(__name__)

        # from super class
        self._name    = FormatName('IOPython')
        self._author  = 'Humberto A. Sanchez II'
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectoryName: str         = ''
        self._importDirectoryName: str         = ''
        self._filesToImport:       List['str'] = []

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file name

        Returns:  'True', we support import
        """
        response: MultipleFileRequestResponse = self.askToImportMultipleFiles()
        if response.cancelled is True:
            return False
        else:
            self._importDirectoryName = response.directoryName
            self._filesToImport   = response.fileList

        return True

    def setExportOptions(self) -> bool:
        return False

    def read(self) -> bool:
        """

        Returns:
        """
        BeginBusyCursor()
        wxYield()
        status: bool = True
        try:
            reverseEngineer: ReverseEngineerPython2 = ReverseEngineerPython2()
            reverseEngineer.reversePython(directoryName=self._importDirectoryName, files=self._filesToImport)
            # TODO: Don't expose the internals
            self.logger.debug(f'classNames: {jsonDumps(reverseEngineer.visitor.classMethods, indent=4)}')
            self.logger.debug(f'methods: {jsonDumps(reverseEngineer.visitor.parameters, indent=4)}')

        except (ValueError, Exception) as e:
            MessageBox(f'{e}', 'Error', OK | ICON_ERROR)
            status = False

        EndBusyCursor()
        return status

    def write(self, oglClasses: OglClasses):
        pass
