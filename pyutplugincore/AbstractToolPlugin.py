
from abc import ABC
from abc import abstractmethod

from pyutplugincore.AbstractPlugin import AbstractPlugin

from pyutplugincore.ICommunicator import ICommunicator

from pyutplugincore.coretypes.Helper import OglObjects


class AbstractToolPlugin(AbstractPlugin, ABC):
    """
    This interface defines the methods and properties that Pyut Tool
    plugins must implement.
    """

    def __init__(self, communicator: ICommunicator, oglObjects: OglObjects):

        super().__init__(communicator, oglObjects)

    def executeTool(self):
        """
        This is used by Pyut to invoke the tool.  This should NOT
        be overridden
        """
        if self.setOptions() is True:
            selectedShapes = self._communicator.selectedOglObjects
            self.doAction(self._oglObjects, selectedShapes)

    @property
    @abstractmethod
    def menuTitle(self) -> str:
        pass

    @abstractmethod
    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to query the user for additional plugin options

        Returns: if False, the import is cancelled.
        """
        pass

    @abstractmethod
    def doAction(self, oglObjects: OglObjects, selectedObjects: OglObjects):
        """
        Do the tool's action

        Args:
            oglObjects:         list of the uml objects in the diagram
            selectedObjects:    list of the selected objects
        """
        pass
