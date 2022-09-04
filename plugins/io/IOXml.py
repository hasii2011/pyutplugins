from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CENTRE
from wx import ICON_QUESTION
from wx import MessageBox
from wx import YES
from wx import YES_NO

from core.IMediator import IMediator
from core.IOPluginInterface import IOPluginInterface
from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat

from core.types.PluginDataTypes import FormatName
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName
from core.types.SingleFileRequestResponse import SingleFileRequestResponse

from core.types.Types import OglObjects

from oglio.Reader import Reader
from oglio.Types import OglProject

FORMAT_NAME:        FormatName        = FormatName("XML")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('xml')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Pyut XML File')


class IOXml(IOPluginInterface):

    def __init__(self, mediator: IMediator):

        self.logger: Logger = getLogger(__name__)

        super().__init__(mediator)

        # from super class
        self._name    = PluginName('IOXml')
        # noinspection SpellCheckingInspection
        self._author  = "Humberto A. Sanchez II"
        self._version = '2.0'
        self._inputFormat  = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._prettyPrint:         bool = True
        self._exportDirectoryName: str  = ''
        self._fileToImport:        str  = ''

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file names

        Returns:  'True', we support import
        """
        response: SingleFileRequestResponse = self.askForFileToImport()
        if response.cancelled is True:
            return False
        else:
            self._fileToImport   = response.fileName

        return True

    def setExportOptions(self) -> bool:
        """
        Prepare the export.

        Returns:
        """
        ans: bool = MessageBox("Do you want pretty xml ?", "Export option", style=YES_NO | CANCEL | CENTRE | ICON_QUESTION)
        self._prettyPrint = (ans == YES)

        return ans != CANCEL

    def read(self) -> bool:
        reader: Reader = Reader()

        oglProject: OglProject = reader.read(fqFileName=self._fileToImport)

        return True

    def write(self, oglObjects: OglObjects):
        pass
