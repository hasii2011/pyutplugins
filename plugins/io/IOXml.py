
from typing import cast

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

from core.types.Types import OglLinks
from core.types.Types import OglObjects

from oglio.Reader import Reader
from oglio.Writer import Writer
from oglio.Types import OglProject
from oglio.Types import OglDocument
from oglio.Types import OglDocuments

from core.types.Types import PluginDocument
from core.types.Types import PluginDocumentType
from core.types.Types import PluginDocumentTitle
from core.types.Types import PluginProject
from core.types.Types import OglClasses

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

        self._prettyPrint:  bool = True
        self._fileToExport: str  = ''
        self._fileToImport: str  = ''

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
        prettPrintAnswer: int = MessageBox("Do you want pretty xml ?", "Export option", style=YES_NO | CANCEL | CENTRE | ICON_QUESTION)
        if prettPrintAnswer is YES:
            self._prettyPrint = True
            response: SingleFileRequestResponse = self.askForFileToExport()
            if response.cancelled is True:
                exportAnswer: bool = False
            else:
                self._fileToExport = response.fileName
                exportAnswer = True
        else:
            exportAnswer = False

        return exportAnswer

    def read(self) -> bool:
        reader: Reader = Reader()

        oglProject: OglProject = reader.read(fqFileName=self._fileToImport)

        pluginProject: PluginProject = PluginProject()

        pluginProject.projectName = PluginProject.toProjectName(fqFilename=self._fileToImport)
        pluginProject.version     = oglProject.version
        pluginProject.codePath    = oglProject.codePath

        oglDocuments: OglDocuments = oglProject.oglDocuments
        for oglDocument in oglDocuments.values():
            pluginDocument: PluginDocument = PluginDocument()
            pluginDocument.documentType    = PluginDocumentType.toEnum(oglDocument.documentType)
            pluginDocument.documentTitle   = PluginDocumentTitle(oglDocument.documentTitle)
            pluginDocument.scrollPositionX = oglDocument.scrollPositionX
            pluginDocument.scrollPositionY = oglDocument.scrollPositionY
            pluginDocument.pixelsPerUnitX  = oglDocument.pixelsPerUnitX
            pluginDocument.pixelsPerUnitY  = oglDocument.pixelsPerUnitY
            pluginDocument.oglClasses      = cast(OglClasses, oglDocument.oglClasses)
            pluginDocument.oglLinks        = cast(OglLinks, oglDocument.oglLinks)

            pluginProject.pluginDocuments[pluginDocument.documentTitle] = pluginDocument

        self._mediator.loadProject(pluginProject=pluginProject)
        return True

    def write(self, oglObjects: OglObjects):

        oglProject: OglProject = OglProject()
        oglProject.version  = self._mediator.pyutVersion
        oglProject.codePath = ''

        oglDocument: OglDocument = OglDocument()
        oglDocument.scrollPositionX = 0
        oglDocument.scrollPositionY = 0
        oglDocument.pixelsPerUnitX = self._mediator.screenMetrics.dpiX
        oglDocument.pixelsPerUnitY = self._mediator.screenMetrics.dpiY

        writer:     Writer = Writer()

        writer.write(oglProject=oglProject, fqFileName=self._fileToExport)
