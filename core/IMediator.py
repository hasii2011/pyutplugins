from typing import Tuple
from typing import Union

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSizeCallback
from core.types.Types import PluginProject
from core.types.Types import SelectedOglObjectsCallback


@dataclass
class ScreenMetrics:
    screenWidth:  int = 0
    screenHeight: int = 0

    dpiX: int = 0
    dpiY: int = 0


class IMediator(ABC):
    """
    This the interface specification that allows the plugins to manipulate the Pyut UML Frame
    The Pyut application must implement this and override the appropriate methods and/or
    set appropriate protected variables after call this class
    constructor

    """
    def __init__(self):
        pass

    @property
    @abstractmethod
    def pyutVersion(self) -> str:
        """
        Returns:  The current Pyut version
        """
        pass

    @pyutVersion.setter
    @abstractmethod
    def pyutVersion(self, newVersion: str):
        pass

    @property
    @abstractmethod
    def screenMetrics(self) -> ScreenMetrics:
        """
        Returns:  appropriate metrics;  wxPython is a helpe
        """
        pass

    @property
    @abstractmethod
    def currentDirectory(self) -> str:
        """
        Returns:  The current directory
        """
        pass

    @currentDirectory.setter
    @abstractmethod
    def currentDirectory(self, theNewValue: str):
        """
        TODO:  Should plugins be allowed to manipulate the application's current directory
        Args:
            theNewValue:
        """
        pass

    @abstractmethod
    def getFrameSize(self, callback: FrameSizeCallback):
        pass

    @abstractmethod
    def getFrameInformation(self, callback: FrameInformationCallback):
        pass

    @abstractmethod
    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        """
        Requests all the selected in the currently displayed frame

        Args:
            callback:  This method is invoked with a list of all the selected OglObjects
        """
        pass

    @abstractmethod
    def refreshFrame(self):
        """
        Refresh the currently displayed frame
        """
        pass

    @abstractmethod
    def selectAllOglObjects(self):
        """
        Select all the Ogl shapes in the currently displayed frame
        """
        pass

    @abstractmethod
    def deselectAllOglObjects(self):
        """
        Deselect all the Ogl shapes in the currently displayed frame
        """
        pass

    @abstractmethod
    def addShape(self, shape: Union[OglObject, OglLink]):
        """
        Add an Ogl shape in the currently displayed frame
        Args:
            shape:
        """
        pass

    @abstractmethod
    def loadProject(self, pluginProject: PluginProject):
        """
        Abstract
        This is the preferred way for plugins to projects into Pyut

        Args:
            pluginProject:

        """
        pass
