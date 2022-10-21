
from typing import cast

from abc import ABC
from abc import abstractmethod

from core.PluginInterface import PluginInterface
from core.IPluginAdapter import IPluginAdapter

from core.types.Types import FrameInformation
from core.types.Types import OglObjects


class IOPluginInterface(PluginInterface, ABC):
    """
    Abstract class for input/output plug-ins.

    If you want to do a new plugin, you must inherit from this class and
    implement the abstract methods.

    The plugin may require user interaction for plugin parameters.  Implement
    these methods:

        `setImportOptions`
        `setExportOptions`

    The import/export work is done in:

        `read(self, oglObjects, umlFrame)`
        `write(self, oglObjects)`

    Pyut invokes the plugin, by instantiating it, and calling one of:

        `doImport`
        `doExport`

    """
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter=pluginAdapter)

        self._oglObjects:         OglObjects = cast(OglObjects, None)               # The imported Ogl Objects
        self._selectedOglObjects: OglObjects = cast(OglObjects, None)               # The selected Ogl Objects requested by .executeExport()
        self._frameInformation:   FrameInformation = cast(FrameInformation, None)   # The frame information requested by .executeExport()

    def executeImport(self):
        """
        Called by Pyut to begin the import process.  Checks to see if an import format is
        supported if not returns None;  Checks to see if there are any import options;
        If the method return True the import proceeds

        Returns:
            None if cancelled, else a list of OglObjects
        """
        if self.inputFormat is None:
            self._oglObjects = None
        else:
            if self.setImportOptions() is True:
                self._oglObjects = self.read()
            else:
                self._oglObjects = None

        return self._oglObjects

    def executeExport(self):
        """
        Called by Pyut to begin the export process.
        """
        self._pluginAdapter.getFrameInformation(callback=self._executeExport)

    def _executeExport(self, frameInformation: FrameInformation):

        assert self.outputFormat is not None, 'Developer error. We cannot export w/o and output format'
        if frameInformation.frameActive is False:
            self.displayNoUmlFrame()
        else:
            if self.setExportOptions() is True:
                self._frameInformation   = frameInformation
                self._selectedOglObjects = frameInformation.selectedOglObjects  # syntactic sugar
                # prefs: PyutPreferences = PyutPreferences()
                # if prefs.pyutIoPluginAutoSelectAll is True:       TODO:  Need plugin preferences
                #    pluginAdapter.selectAllShapes()

                if len(self._selectedOglObjects) == 0:
                    self.displayNoSelectedOglObjects()
                else:
                    self.write(self._selectedOglObjects)
                    self._pluginAdapter.deselectAllOglObjects()

    @abstractmethod
    def setImportOptions(self) -> bool:
        """
        Prepare for the import.
        Use this method to query the end-user for any additional import options

        Returns:
            if False, the import is cancelled
        """
        pass

    @abstractmethod
    def setExportOptions(self) -> bool:
        """
        Prepare for the export.
        Use this method to query the end-user for any additional export options

        Returns:
            if False, the export is cancelled
        """
        pass

    @abstractmethod
    def read(self) -> bool:
        """
        Read data from a file;  Presumably, the file was specified on the call
        to setImportOptions
        """
        pass

    @abstractmethod
    def write(self, oglObjects: OglObjects):
        """
        Write data to a file;  Presumably, the file was specified on the call
        to setExportOptions

         Args:
            oglObjects:  list of exported objects

        """
        pass
