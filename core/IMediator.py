
from typing import Union
from typing import cast

from dataclasses import dataclass

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.types.Types import OglClasses
from core.types.Types import PluginProject


@dataclass
class ScreenMetrics:
    screenWidth:  int = 0
    screenHeight: int = 0

    dpiX: int = 0
    dpiY: int = 0


class IMediator:
    """
    This the interface specification that allows the plugins to manipulate the Pyut UML Frame
    The Pyut application must implement this and override the appropriate methods and/or
    set appropriate protected variables after call this class
    constructor

    I really wanted to use Python's built-in ABC but caused problems when I tried to use it as an interface
    I have tried using several 3rd party packages like:  https://pypi.org/project/python-interface/
    but, either they do not work quite right or not regularly updated
    So this is the best I can do
    """
    def __init__(self, currentDirectory: str, umlFrame: DiagramFrame):

        self._umlFrame:         DiagramFrame = umlFrame
        self._currentDirectory: str          = currentDirectory

    @property
    def pyutVersion(self) -> str:
        """
        Abstract Method
        Returns:  The current Pyut version
        """
        return ''

    @pyutVersion.setter
    def pyutVersion(self, newVersion: str):
        pass

    @property
    def screenMetrics(self) -> ScreenMetrics:
        """
        Abstract
        Returns:  appropriate metrics;  wxPython is a helpe
        """
        return cast(ScreenMetrics, None)

    @property
    def currentDirectory(self) -> str:
        return self._currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, theNewValue: str):
        self._currentDirectory = theNewValue

    @property
    def umlFrame(self) -> DiagramFrame:
        return self._umlFrame

    @property
    def selectedOglObjects(self) -> OglClasses:
        return self._umlFrame.GetSelectedShapes()

    def refreshFrame(self):
        self._umlFrame.Refresh()

    def selectAllOglObjects(self):
        pass

    def deselectAllOglObjects(self):
        self._umlFrame.DeselectAllShapes()

    def addShape(self, shape: Union[OglObject, OglLink]):

        diagram = self._umlFrame.GetDiagram()
        diagram.AddShape(shape)

    def addProject(self, pluginProject: PluginProject):
        """
        Abstract
        This is the preferred way of adding projects to Pyut

        Args:
            pluginProject:

        """
        pass
