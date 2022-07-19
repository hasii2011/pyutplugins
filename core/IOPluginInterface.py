
from abc import ABC
from abc import abstractmethod

from plugins.common.Types import OglClasses
from core.PluginInterface import PluginInterface
from core.ICommunicator import ICommunicator
from core.types.OutputFormat import OutputFormat


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
    def __init__(self, communicator: ICommunicator):

        super().__init__(communicator)

    @property
    def name(self) -> str:
        """
        Implementations must override this property

        Returns:  The plugin name
        """
        return self._name

    @property
    def version(self) -> str:
        """
        Implementations must override this property

        Returns: The plugin version string
        """
        return self._version

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
        if self._communicator.umlFrame is None:
            self.displayNoUmlFrame()
        else:
            outputFormat: OutputFormat = self.outputFormat      # TODO this is probably not needed Pyut groups appropriately
            if outputFormat is None:
                pass
            else:
                if self.setExportOptions() is False:
                    pass
                else:
                    # prefs: PyutPreferences = PyutPreferences()
                    # if prefs.pyutIoPluginAutoSelectAll is True:       TODO:  Need plugin preferences
                    #    mediator.selectAllShapes()
                    oglObjects = self._communicator.selectedOglObjects
                    if len(oglObjects) == 0:
                        self.displayNoSelectedOglObjects()
                    else:
                        self.write(oglObjects)
                        self._communicator.deselectAllOglObjects()

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
    def write(self, oglClasses: OglClasses):
        """
         Write data to a file;  Presumably, the file was specified on the call
        to setExportOptions

         Args:
            oglClasses:  list of exported objects

        """
        pass