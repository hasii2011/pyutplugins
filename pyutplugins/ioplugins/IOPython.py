
from typing import cast
from typing import Dict
from typing import List

from logging import Logger
from logging import getLogger

from os import sep as osSep

from pyutmodel.PyutClass import PyutClass

from ogl.OglClass import OglClass

from wx import ICON_ERROR
from wx import OK
from wx import PD_APP_MODAL
from wx import PD_ELAPSED_TIME

from wx import MessageBox
from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import ProgressDialog

from wx import Yield as wxYield

from pyutplugins.coreinterfaces.IPluginAdapter import IPluginAdapter
from pyutplugins.coreinterfaces.IOPluginInterface import IOPluginInterface

from pyutplugins.CoreTypes import OglClasses
from pyutplugins.CoreTypes import OglLinks
from pyutplugins.CoreTypes import OglObjects

from pyutplugins.coretypes.PluginDataTypes import PluginExtension
from pyutplugins.coretypes.PluginDataTypes import PluginName
from pyutplugins.coretypes.PluginDataTypes import FormatName
from pyutplugins.coretypes.PluginDataTypes import PluginDescription

from pyutplugins.coretypes.ExportDirectoryResponse import ExportDirectoryResponse
from pyutplugins.coretypes.MultipleFileRequestResponse import MultipleFileRequestResponse
from pyutplugins.coretypes.InputFormat import InputFormat
from pyutplugins.coretypes.OutputFormat import OutputFormat

from pyutplugins.ioplugins.python.PyutToPython import MethodsCodeType
from pyutplugins.ioplugins.python.PyutToPython import PyutToPython
from pyutplugins.ioplugins.python.ReverseEngineerPython2 import ReverseEngineerPython2

FORMAT_NAME:        FormatName        = FormatName("Python File(s)")
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('py')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Python code generation and reverse engineering')


class IOPython(IOPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        # from super class
        self._name    = PluginName('IOPython')
        self._author  = 'Humberto A. Sanchez II'
        self._version = '1.0'
        self._inputFormat  = InputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._exportDirectoryName: str         = ''
        self._importDirectoryName: str         = ''
        self._filesToImport:       List['str'] = []

        self._readProgressDlg: ProgressDialog = cast(ProgressDialog, None)

    def setImportOptions(self) -> bool:
        """
        We do need to ask for the input file names

        Returns:  'True', we support import
        """
        response: MultipleFileRequestResponse = self.askToImportMultipleFiles(startDirectory=None)
        if response.cancelled is True:
            return False
        else:
            self._importDirectoryName = response.directoryName
            self._filesToImport   = response.fileList

        return True

    def setExportOptions(self) -> bool:
        response: ExportDirectoryResponse = self.askForExportDirectoryName(preferredDefaultPath=None)
        if response.cancelled is True:
            return False
        else:
            self._exportDirectoryName = response.directoryName
            return True

    def read(self) -> bool:
        """

        Returns:
        """
        BeginBusyCursor()
        wxYield()
        status: bool = True
        try:
            reverseEngineer: ReverseEngineerPython2 = ReverseEngineerPython2()

            fileCount: int        = len(self._filesToImport)
            self._readProgressDlg = ProgressDialog('Parsing Files', 'Starting',  parent=None, style=PD_APP_MODAL | PD_ELAPSED_TIME)
            self._readProgressDlg.SetRange(fileCount)

            reverseEngineer.reversePython(directoryName=self._importDirectoryName, files=self._filesToImport, progressCallback=self._readProgressCallback)
            oglClasses: OglClasses = reverseEngineer.oglClasses
            oglLinks:   OglLinks   = reverseEngineer.oglLinks()

            self.logger.warning(f'Classes: {oglClasses}')
            self.logger.warning(f'Links:   {oglLinks}')

            self._layoutUmlClasses(oglClasses=oglClasses)
            self._layoutLinks(oglLinks=oglLinks)
        except (ValueError, Exception) as e:
            self._readProgressDlg.Destroy()
            MessageBox(f'{e}', 'Error', OK | ICON_ERROR)
            status = False
        else:
            self._readProgressDlg.Destroy()
            EndBusyCursor()
            self._pluginAdapter.indicatePluginModifiedProject()
        return status

    def write(self, oglObjects: OglObjects):

        directoryName: str = self._exportDirectoryName

        self.logger.info("IoPython Saving...")
        pyutToPython: PyutToPython = PyutToPython()
        classes:           Dict[str, List[str]] = {}
        generatedClassDoc: List[str]            = pyutToPython.generateTopCode()
        # oglClasses: OglClasses = self._communicator.selectedOglObjects

        for oglClass in oglObjects:
            if isinstance(oglClass, OglClass):
                pyutClass:          PyutClass = oglClass.pyutObject
                generatedStanza:    str       = pyutToPython.generateClassStanza(pyutClass)
                generatedClassCode: List[str] = [generatedStanza]

                clsMethods: MethodsCodeType = pyutToPython.generateMethodsCode(pyutClass)

                # Add __init__ Method
                if PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR in clsMethods:
                    methodCode = clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]
                    generatedClassCode += methodCode
                    del clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]

                # Add others methods in order
                for pyutMethod in pyutClass.methods:
                    methodName: str = pyutMethod.name
                    if methodName != PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR:
                        try:
                            otherMethodCode: List[str] = clsMethods[methodName]
                            generatedClassCode += otherMethodCode
                        except (ValueError, Exception, KeyError) as e:
                            self.logger.warning(f'{e}')

                generatedClassCode.append("\n\n")
                # Save into classes dictionary
                classes[pyutClass.name] = generatedClassCode

        # Write class code to a file
        for (className, classCode) in list(classes.items()):
            self._writeClassToFile(classCode, className, directoryName, generatedClassDoc)

        self.logger.info("IoPython done !")

    def _writeClassToFile(self, classCode, className, directory, generatedClassDoc):

        filename: str = f'{directory}{osSep}{str(className)}.py'

        file = open(filename, "w")
        file.writelines(generatedClassDoc)
        file.writelines(classCode)

        file.close()

    def _readProgressCallback(self, currentFileCount: int, msg: str):
        """

        Args:
            currentFileCount:   The current file # we are working pm
            msg:    An updated message
        """

        self._readProgressDlg.Update(currentFileCount, msg)
