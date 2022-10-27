
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglActor import OglActor
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage
from wx import CANCEL
from wx import CENTRE
from wx import ICON_QUESTION
from wx import MessageBox
from wx import YES
from wx import YES_NO

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglInterface2 import OglInterface2

from core.IPluginAdapter import IPluginAdapter

from core.IOPluginInterface import IOPluginInterface

from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import FormatName
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName
from core.types.SingleFileRequestResponse import SingleFileRequestResponse

from core.types.Types import OglActors
from core.types.Types import OglLinks
from core.types.Types import OglNotes
from core.types.Types import OglObjects

from oglio.Reader import Reader
from oglio.Writer import Writer
from oglio.Types import OglProject
from oglio.Types import OglDocument
from oglio.Types import OglDocuments
from oglio.Types import OglDocumentTitle

from core.types.Types import OglClasses
from core.types.Types import OglSDInstances
from core.types.Types import OglSDMessages
from core.types.Types import OglTexts
from core.types.Types import OglUseCases
from core.types.Types import PluginDocument
from core.types.Types import PluginDocumentType
from core.types.Types import PluginDocumentTitle
from core.types.Types import PluginProject

FORMAT_NAME:        FormatName        = FormatName("XML")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('xml')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Pyut XML File')


class IOXml(IOPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        self.logger: Logger = getLogger(__name__)

        super().__init__(pluginAdapter=pluginAdapter)

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

        self._requireActiveFrame = False

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

        oglProject: OglProject = reader.readXmlFile(fqFileName=self._fileToImport)

        pluginProject: PluginProject = PluginProject()

        pluginProject.fileName    = self._fileToImport
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
            pluginDocument.oglClasses      = cast(OglClasses,     oglDocument.oglClasses)
            pluginDocument.oglLinks        = cast(OglLinks,       oglDocument.oglLinks)
            pluginDocument.oglNotes        = cast(OglNotes,       oglDocument.oglNotes)
            pluginDocument.oglTexts        = cast(OglTexts,       oglDocument.oglTexts)
            pluginDocument.oglActors       = cast(OglActors,      oglDocument.oglActors)
            pluginDocument.oglUseCases     = cast(OglUseCases,    oglDocument.oglUseCases)
            pluginDocument.oglSDInstances  = cast(OglSDInstances, oglDocument.oglSDInstances)
            pluginDocument.oglSDMessages   = cast(OglSDMessages,  oglDocument.oglSDMessages)

            pluginProject.pluginDocuments[pluginDocument.documentTitle] = pluginDocument

        self._pluginAdapter.loadProject(pluginProject=pluginProject)
        return True

    def write(self, oglObjects: OglObjects):

        oglProject: OglProject = OglProject()
        oglProject.version  = self._pluginAdapter.pyutVersion
        oglProject.codePath = ''

        oglDocument: OglDocument = OglDocument()
        oglDocument.scrollPositionX = 0
        oglDocument.scrollPositionY = 0
        oglDocument.pixelsPerUnitX = self._pluginAdapter.screenMetrics.dpiX
        oglDocument.pixelsPerUnitY = self._pluginAdapter.screenMetrics.dpiY
        oglDocument.documentTitle  = OglDocumentTitle(self._frameInformation.diagramTitle)
        oglDocument.documentType   = self._frameInformation.diagramType
        for oglObject in oglObjects:
            match oglObject:
                case OglClass() as oglObject:
                    oglDocument.oglClasses.append(oglObject)
                case OglInterface2() as oglObject:
                    # TODO Fix this in oglio
                    oglDocument.oglLinks.append(oglObject)  # type: ignore
                case OglLink() as oglObject:
                    oglDocument.oglLinks.append(oglObject)
                case OglNote() as oglObject:
                    oglDocument.oglNotes.append(oglObject)
                case OglText() as oglObject:
                    oglDocument.oglTexts.append(oglObject)
                case OglUseCase() as oglObject:
                    oglDocument.oglUseCases.append(oglObject)
                case OglActor() as oglObject:
                    oglDocument.oglActors.append(oglObject)
                case OglSDMessage() as oglObject:
                    oglSDMessage: OglSDMessage         = cast(OglSDMessage, oglObject)
                    modelId:      int                  = oglSDMessage.pyutObject.id
                    oglDocument.oglSDMessages[modelId] = oglSDMessage
                case OglSDInstance() as oglObject:
                    oglSDInstance: OglSDInstance        = cast(OglSDInstance, oglObject)
                    modelId                             = oglSDInstance.pyutObject.id
                    oglDocument.oglSDInstances[modelId] = oglSDInstance
                case _:
                    self.logger.warning(f'Unsaved {oglObject=}')
        oglProject.oglDocuments[oglDocument.documentTitle] = oglDocument

        writer:     Writer = Writer()

        writer.writeXmlFile(oglProject=oglProject, fqFileName=self._fileToExport)
