
from os import getcwd
from typing import Union
from typing import cast

from miniogl.DiagramFrame import DiagramFrame
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics
from core.types.Types import OglClasses
from core.types.Types import PluginProject
from tests.scaffoldv2.eventengine.EventEngine import EventEngine


class ScaffoldMediator(IMediator):
    """
    Shortcut implement the version and screen metrics properties
    """

    def __init__(self, umlFrame: DiagramFrame, currentDirectory: str = ''):

        super().__init__()
        if currentDirectory is None or currentDirectory == '':
            self._currentDirectory: str = getcwd()
        else:
            self._currentDirectory = currentDirectory

        self._umlFrame: DiagramFrame = umlFrame

        self._pyutVersion = 'Scaffold 1.0'

    @property
    def pyutVersion(self) -> str:
        return self._pyutVersion

    @pyutVersion.setter
    def pyutVersion(self, newVersion: str):
        self._pyutVersion = newVersion

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    @property
    def currentDirectory(self) -> str:
        return self._currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, theNewValue: str):
        self._currentDirectory = theNewValue

    @property
    def umlFrame(self) -> DiagramFrame:
        return self._umlFrame

    @umlFrame.setter
    def umlFrame(self, newValue: DiagramFrame):
        self._umlFrame = newValue

    @property
    def eventEngine(self) -> EventEngine:
        return cast(EventEngine, None)

    @eventEngine.setter
    def eventEngine(self, eventEngine: EventEngine):
        pass

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
        pass
