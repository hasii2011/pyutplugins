from logging import Logger
from logging import getLogger
from typing import List
from typing import cast

from os import sep as osSep

from wx import BeginBusyCursor
from wx import EndBusyCursor as wxEndBusyCursor
from wx import Yield as wxYield

from core.IPluginAdapter import IPluginAdapter
from core.IOPluginInterface import IOPluginInterface

from core.types.ExportDirectoryResponse import ExportDirectoryResponse
from core.types.MultipleFileRequestResponse import MultipleFileRequestResponse

from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import FormatName
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName

from core.types.Types import OglClasses
from core.types.Types import OglLinks

from core.types.Types import OglObjects

from plugins.io.java.JavaReader import JavaReader
from plugins.io.java.JavaWriter import JavaWriter

FORMAT_NAME:        FormatName        = FormatName("Java")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('java')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Java file format')


class IOJava(IOPluginInterface):
    """
    Plugin that can
        * Write Java code from Ogl Classes in a UML Diagram
        * Read Java to and transform to a UML Diagram

    In the original implementation these were two different I/O Plugins
    """

    def __init__(self, pluginAdapter: IPluginAdapter):

        self.logger: Logger = getLogger(__name__)

        super().__init__(pluginAdapter)

        # from super class
        self._name    = PluginName('Java Code Reader and Writer')
        self._author  = "C.Dutoit <dutoitc@hotmail.com> and N. Dubois <nicdub@gmx.ch"
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectoryName: str         = ''
        self._importDirectoryName: str         = ''
        self._filesToImport:       List['str'] = []

    def setImportOptions(self) -> bool:

        response: MultipleFileRequestResponse = self.askToImportMultipleFiles()
        if response.cancelled is True:
            return False
        else:
            self._importDirectoryName = response.directoryName
            self._filesToImport   = response.fileList

        return True

    def setExportOptions(self) -> bool:
        response: ExportDirectoryResponse = self.askForExportDirectoryName()
        if response.cancelled is True:
            return False
        else:
            self._exportDirectoryName = response.directoryName

        return True

    def read(self) -> bool:
        BeginBusyCursor()
        wxYield()

        directoryName: str        = self._importDirectoryName
        importFiles:   List[str]  = self._filesToImport
        javaReader:    JavaReader = JavaReader()

        for importFile in importFiles:
            fqFileName: str = f'{directoryName}{osSep}{importFile}'
            javaReader.parseFile(fqFileName)

        assert javaReader.reversedClasses is not None, 'Something is broken'

        oglClasses: OglClasses = OglClasses(list(javaReader.reversedClasses.values()))
        self._layoutUmlClasses(oglClasses=oglClasses)
        self._layoutLinks(oglLinks=cast(OglLinks, javaReader.reversedLinks))

        wxEndBusyCursor()
        return True

    def write(self, oglObjects: OglObjects):

        directoryName: str        = self._exportDirectoryName
        javaWriter:    JavaWriter = JavaWriter(writeDirectory=directoryName)

        javaWriter.write(oglObjects=oglObjects)
