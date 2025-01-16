
from abc import ABC
from abc import abstractmethod

from pyutplugins.plugininterfaces.BasePluginInterface import BasePluginInterface
from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.ExternalTypes import FrameInformation
from pyutplugins.ExternalTypes import OglObjects


class IOPluginInterface(BasePluginInterface, ABC):
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

    def executeImport(self):
        """
        Called by Pyut to begin the import process.
        """
        # TODO Fix later
        # noinspection PyTypeChecker
        self._pluginAdapter.getFrameInformation(callback=self._executeImport)   # type ignore

    def _executeImport(self, frameInformation: FrameInformation):
        """
        The callback necessary to start the import process;
        Args:
            frameInformation:
        """
        assert self.inputFormat is not None, 'Developer error. We cannot import w/o an import format'
        if self._requireActiveFrame is True:
            if frameInformation.frameActive is False:
                self.displayNoUmlFrame()
                return
        if self.setImportOptions() is True:
            self.read()

    def executeExport(self):
        """
        Called by Pyut to begin the export process.
        """
        if self._autoSelectAll is True:
            self._pluginAdapter.selectAllOglObjects()
        self._pluginAdapter.getFrameInformation(callback=self._executeExport)

    def _executeExport(self, frameInformation: FrameInformation):

        assert self.outputFormat is not None, 'Developer error. We cannot export w/o an output format'

        self._frameInformation = frameInformation

        if frameInformation.frameActive is False:
            self.displayNoUmlFrame()
        else:
            self._selectedOglObjects = frameInformation.selectedOglObjects  # syntactic sugar

            if len(self._selectedOglObjects) == 0 and self._requireSelection is True:
                self.displayNoSelectedOglObjects()
            else:
                if self.setExportOptions() is True:
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
