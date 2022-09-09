from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from wx import Frame

from miniogl.DiagramFrame import DiagramFrame

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics
from core.types.Types import OglObjects
from core.types.Types import PluginProject
from tests.scaffoldv2.eventengine.EventEngine import EventEngine


class SampleIMediator(IMediator):

    def __init__(self):

        super().__init__()
        self.logger:            Logger = getLogger(__name__)
        self._currentDirectory: str    = ''
        self._pyutVersion:      str    = 'Sample Mediator'

    @property
    def currentDirectory(self) -> str:
        return self._currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, newValue: str):
        self._currentDirectory = newValue

    @property
    def umlFrame(self) -> Frame:
        return cast(Frame, None)

    @umlFrame.setter
    def umlFrame(self, newValue: DiagramFrame):
        pass

    @property
    def pyutVersion(self) -> str:
        return self._pyutVersion

    @pyutVersion.setter
    def pyutVersion(self, newVersion: str):
        pass

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    @property
    def eventEngine(self) -> EventEngine:
        return cast(EventEngine, None)

    @eventEngine.setter
    def eventEngine(self, eventEngine: EventEngine):
        pass

    @property
    def selectedOglObjects(self) -> OglObjects:
        return cast(OglObjects, None)

    def refreshFrame(self):
        pass

    def selectAllOglObjects(self):
        pass

    def deselectAllOglObjects(self):
        pass

    def addShape(self, shape: Union[OglObject, OglLink]):
        pass

    def addProject(self, pluginProject: PluginProject):
        pass
