
from abc import ABC
from abc import abstractmethod


from pyutplugincore.AbstractPlugin import AbstractPlugin
from pyutplugincore.ICommunicator import ICommunicator
from pyutplugincore.coretypes.Helper import OglClasses
from pyutplugincore.coretypes.OutputFormat import OutputFormat


class AbstractIOPlugin(AbstractPlugin, ABC):
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
    def __init__(self, communicator: ICommunicator, oglClasses: OglClasses):

        super().__init__(communicator, oglClasses)

        self._oglObjects: OglClasses = oglClasses

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
            outputFormat: OutputFormat = self.outputFormat
            if outputFormat is None:
                pass
            else:
                if self.setExportOptions() is False:
                    pass
                else:
                    # prefs: PyutPreferences = PyutPreferences()
                    # if prefs.pyutIoPluginAutoSelectAll is True:       TODO:  Need plugin preferences
                    #    mediator.selectAllShapes()
                    self.__oglObjects = self._communicator.selectedOglObjects
                    if len(self.__oglObjects) == 0:
                        self.displayNoSelectedOglObjects()
                    else:
                        self.write(self._oglObjects)
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
    def read(self) -> OglClasses:
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
