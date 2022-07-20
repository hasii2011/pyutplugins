from logging import Logger
from logging import getLogger
from typing import List

from core.ICommunicator import ICommunicator
from core.IOPluginInterface import IOPluginInterface
from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import FormatName
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName
from plugins.common.Types import OglObjects

PLUGIN_NAME:        FormatName        = FormatName("Java File(s)")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('java')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Java code generation & reverse engineer to UML')


class IOJava(IOPluginInterface):

    def __init__(self, communicator: ICommunicator):

        super().__init__(communicator)

        self.logger: Logger = getLogger(__name__)

        # from super class
        self._name    = PluginName('IOJava')
        self._author  = 'N. Dubois <nicdub@gmx.ch> & C.Dutoit <dutoitc@hotmail.com>'
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=PLUGIN_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectoryName: str         = ''
        self._importDirectoryName: str         = ''
        self._filesToImport:       List['str'] = []

    def setImportOptions(self) -> bool:
        pass

    def setExportOptions(self) -> bool:
        pass

    def read(self) -> bool:
        pass

    def write(self, oglObjects: OglObjects):
        pass

