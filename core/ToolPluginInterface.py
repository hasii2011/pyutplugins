
from abc import ABC
from abc import abstractmethod

from core.PluginInterface import PluginInterface

from core.IMediator import IMediator


class ToolPluginInterface(PluginInterface, ABC):
    """
    This interface defines the methods and properties that Pyut Tool
    plugins must implement.
    """

    def __init__(self, communicator: IMediator):

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
        Prepare for the tool action
        This can be used to query the user for additional plugin options

        Returns: If False, the import should be cancelled.  'True' to proceed
        """
        pass

    @abstractmethod
    def doAction(self):
        """
        Do the tool's action
        """
        pass
