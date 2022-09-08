
from typing import Union

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.types.Types import OglObjects
from core.types.Types import PluginProject


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
        pass

    @currentDirectory.setter
    @abstractmethod
    def currentDirectory(self, theNewValue: str):
        pass

    @property
    @abstractmethod
    def umlFrame(self) -> DiagramFrame:
        pass

    @umlFrame.setter
    @abstractmethod
    def umlFrame(self, newValue: DiagramFrame):
        pass

    @property
    @abstractmethod
    def selectedOglObjects(self) -> OglObjects:
        """
        Select all the Ogl shapes in the currently displayed frame
        Returns:
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
    def addProject(self, pluginProject: PluginProject):
        """
        Abstract
        This is the preferred way of adding projects to Pyut

        Args:
            pluginProject:

        """
        pass
