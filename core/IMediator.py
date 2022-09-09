
from typing import Union

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.types.Types import OglObjects
from core.types.Types import PluginProject
from tests.scaffoldv2.eventengine.EventEngine import EventEngine


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

    TODO:  Ignore for properties because mypy does not know how to handle them  @abstractproperty is deprecated
    """
    def __init__(self):
        pass

    @property               # type: ignore
    @abstractmethod
    def pyutVersion(self) -> str:
        """
        Returns:  The current Pyut version
        """
        pass

    @pyutVersion.setter     # type: ignore
    @abstractmethod
    def pyutVersion(self, newVersion: str):
        pass

    @property               # type: ignore
    @abstractmethod
    def screenMetrics(self) -> ScreenMetrics:
        """
        Returns:  appropriate metrics;  wxPython is a helpe
        """
        pass

    @property
    def currentDirectory(self) -> str:
        """
        Returns:  The current directory
        """
        return ''

    @currentDirectory.setter
    def currentDirectory(self, theNewValue: str):
        """
        TODO:  Should plugins be allowed to manipulate the application's current directory
        Args:
            theNewValue:
        """
        pass

    @property           # type: ignore
    @abstractmethod
    def umlFrame(self) -> DiagramFrame:
        pass

    @umlFrame.setter    # type: ignore
    @abstractmethod
    def umlFrame(self, newValue: DiagramFrame):
        pass

    @property       # type: ignore
    @abstractmethod
    def eventEngine(self) -> EventEngine:
        pass

    @eventEngine.setter     # type: ignore
    @abstractmethod
    def eventEngine(self, eventEngine: EventEngine):
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
    def loadProject(self, pluginProject: PluginProject):
        """
        Abstract
        This is the preferred way for plugins to projects into Pyut

        Args:
            pluginProject:

        """
        pass
