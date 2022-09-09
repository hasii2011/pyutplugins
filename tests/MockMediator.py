
from typing import Union
from typing import cast

from unittest.mock import MagicMock

from os import getcwd

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics
from core.types.Types import OglObjects
from core.types.Types import PluginProject
from tests.scaffoldv2.eventengine.EventEngine import EventEngine


class MockMediator(IMediator):
    """
    A simple mostly do nothing mediator for unit tests
    """
    # noinspection PyUnusedLocal
    def __init__(self, umlFrame: DiagramFrame = None, currentDirectory: str = ''):
        """

        Args:
            umlFrame:           Never going to use this
            currentDirectory:
        """

        if currentDirectory is None or currentDirectory == '':
            self._currentDirectory: str = getcwd()
        else:
            self._currentDirectory = currentDirectory

        # ignore whatever comes in
        mockFrame: MagicMock = MagicMock(spec=DiagramFrame)

        super().__init__()

        self._pyutVersion = 'Mock Mediator 1.0'

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
    def currentDirectory(self) -> str:
        return ''

    @currentDirectory.setter
    def currentDirectory(self, theNewValue: str):
        pass

    @property
    def umlFrame(self) -> DiagramFrame:
        return cast(DiagramFrame, None)

    @umlFrame.setter
    def umlFrame(self, newValue: DiagramFrame):
        pass

    @property
    def eventEngine(self) -> EventEngine:
        return cast(EventEngine, None)

    @eventEngine.setter
    def eventEngine(self, eventEngine: EventEngine):
        pass

    def selectedOglObjects(self) -> OglObjects:
        pass

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
