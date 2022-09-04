
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics
from core.IOPluginInterface import IOPluginInterface
from core.types.InputFormat import InputFormat
from core.types.OutputFormat import OutputFormat
from core.types.PluginDataTypes import FormatName
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName
from core.types.SingleFileRequestResponse import SingleFileRequestResponse

from plugins.common.Types import OglObjects
from plugins.io.pdf.ImageFormat import ImageFormat
from plugins.io.pdf.ImageOptions import ImageOptions
from plugins.io.pdf.OglToPyUmlDefinition import OglToPyUmlDefinition

FORMAT_NAME:        FormatName = FormatName('PDF')
PLUGIN_EXTENSION:   PluginExtension = PluginExtension('pdf')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('A simple PDF for UML diagrams')


class IOPdf(IOPluginInterface):
    """
    """
    def __init__(self, mediator: IMediator):
        """

        Args:
            mediator:   A class that implements IMediator
        """
        super().__init__(mediator=mediator)

        self.logger: Logger = getLogger(__name__)

        self._name    = PluginName('Output PDF')
        self._author  = "Humberto A. Sanchez II"
        self._version = '1.2'

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._imageOptions: ImageOptions = ImageOptions()

        self._imageOptions.imageFormat = ImageFormat.PDF

    def setImportOptions(self) -> bool:
        return False

    def setExportOptions(self) -> bool:
        """
        Prepare the export.

        Returns:
            if False, the export is cancelled.
        """
        self._exportResponse = self.askForFileToExport()

        if self._exportResponse.cancelled is True:
            return False
        else:
            self._imageOptions.outputFileName = self._exportResponse.fileName
            return True

    def read(self) -> bool:
        return False

    def write(self, oglObjects: OglObjects):
        """
        Write data to a file;  Presumably, the file was specified on the call
        to setExportOptions

         Args:
            oglObjects:  list of exported objects

        """
        self.logger.info(f'export file name: {self._imageOptions.outputFileName}')
        wxYield()

        pluginVersion: str = self.version
        pyutVersion:   str = self._mediator.pyutVersion

        screenMetrics: ScreenMetrics = self._mediator.screenMetrics
        dpi:           int           = screenMetrics.dpiX

        oglToPdf: OglToPyUmlDefinition = OglToPyUmlDefinition(imageOptions=self._imageOptions,
                                                              dpi=dpi,
                                                              pyutVersion=pyutVersion,
                                                              pluginVersion=pluginVersion
                                                              )

        oglToPdf.toClassDefinitions(oglObjects=oglObjects)
        oglToPdf.layoutLines(oglObjects=oglObjects)
        oglToPdf.write()