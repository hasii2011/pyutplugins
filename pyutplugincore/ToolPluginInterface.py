
from abc import ABC
from abc import abstractmethod

from pyutplugincore.PluginInterface import PluginInterface

from pyutplugincore.ICommunicator import ICommunicator


class ToolPluginInterface(PluginInterface, ABC):
    """
    This interface defines the methods and properties that Pyut Tool
    plugins must implement.
    """

    def __init__(self, communicator: ICommunicator):

        super().__init__(communicator)

        self._menuTitle: str = 'Not Set'

    def executeTool(self):
        """
        This is used by Pyut to invoke the tool.  This should NOT
        be overridden
        """
        if self.setOptions() is True:
            selectedShapes = self._communicator.selectedOglObjects
            self.doAction(self._oglClasses, selectedShapes)

    @property
    def menuTitle(self) -> str:
        return self._menuTitle

    @abstractmethod
    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to query the user for additional plugin options

        Returns: if False, the import is cancelled.
        """
        pass

    @abstractmethod
    def doAction(self):
        """
        Do the tool's action
        """
        pass
