
from typing import cast

from logging import Logger
from logging import getLogger

from time import strftime

from pathlib import Path

from tempfile import NamedTemporaryFile

from wx import MessageBox
from wx import OK

from pyutplugins.ExternalTypes import FrameInformation

from pyutplugins.common.Common import createScreenImageFile

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse

from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension

from pyimage2pdf.PyImage2Pdf import PdfOptions
from pyimage2pdf.PyImage2Pdf import PyImage2Pdf
from pyimage2pdf.PyImage2Pdf import KeyWordList
from pyimage2pdf.PyImage2Pdf import PdfMetaData


FORMAT_NAME:        FormatName        = FormatName('PDF')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('pdf')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Generate a simple PDF for visible UML diagram')

PLUGIN_VERSION: str = '2.0'


class IOPdf(IOPluginInterface):
    """
    Set up for PDF generation;  However, with a simple refactor to
    move definition generation and a new subclass we can generate
    png images;  Waiting on pyumldiagrams to be images to support
    Notes and lollipop interfaces
    """
    def __init__(self, pluginAdapter: IPluginAdapter):
        """

        Args:
            pluginAdapter:   A class that implements IMediator
        """
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name    = PluginName('Output PDF')
        self._author  = "Humberto A. Sanchez II"
        self._version = PLUGIN_VERSION

        self._exportResponse: SingleFileRequestResponse = cast(SingleFileRequestResponse, None)

        self._inputFormat  = cast(InputFormat, None)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportFileName: Path = cast(Path, None)

        self._autoSelectAll = True     # we are taking a picture of the entire diagram

    def setImportOptions(self) -> bool:
        return False

    def setExportOptions(self) -> bool:
        """
        Prepare the export.

        Returns:
            if False, the export is cancelled.
        """
        self._exportResponse = self.askForFileToExport(defaultPath=str(self._pluginPreferences.outputPath),
                                                       defaultFileName=str(self._pluginPreferences.exportFileName))

        if self._exportResponse.cancelled is True:
            self._pluginAdapter.deselectAllOglObjects()
            return False
        else:
            self._exportFileName = Path(self._exportResponse.fileName)
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
        frameInformation: FrameInformation = self._frameInformation
        pluginAdapter:    IPluginAdapter   = self._pluginAdapter
        pluginAdapter.deselectAllOglObjects()

        tempFile        = NamedTemporaryFile(dir='/tmp', suffix='.png')
        imagePath: Path = Path(tempFile.name)

        success: bool = createScreenImageFile(frameInformation=frameInformation, imagePath=imagePath)
        if success is False:
            msg: str = f'Error on image write to {imagePath}'
            MessageBox(message=msg, caption='Error', style=OK)
        else:
            image2Pdf: PyImage2Pdf = PyImage2Pdf()

            pdfOptions:     PdfOptions = PdfOptions()
            creationDate:   str = strftime(self._pluginPreferences.dateFormat)
            annotationText: str = f'{self._pluginPreferences.title} - {creationDate}'

            pdfOptions.annotationText      = annotationText
            pdfOptions.annotationLeft      = self._pluginPreferences.annotationLeft
            pdfOptions.annotationWidth     = self._pluginPreferences.annotationWidth
            pdfOptions.annotationTopOffset = self._pluginPreferences.annotationTopOffset
            pdfOptions.annotationHeight    = self._pluginPreferences.annotationHeight

            pdfMetaData: PdfMetaData = PdfMetaData()

            pdfMetaData.author   = self._pluginPreferences.author
            pdfMetaData.producer = f'IOPdf Plugin {PLUGIN_VERSION}'
            pdfMetaData.title    = self._pluginPreferences.title
            pdfMetaData.subject  = self._pluginPreferences.subject
            keyWordList: KeyWordList = KeyWordList([])
            pdfMetaData.keywords = keyWordList

            pdfOptions.pdfMetaData = pdfMetaData
            image2Pdf.convert(imagePath=imagePath, pdfPath=self._exportFileName, pdfOptions=pdfOptions)
