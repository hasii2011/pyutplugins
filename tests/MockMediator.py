
from os import getcwd
from unittest.mock import MagicMock

from miniogl.DiagramFrame import DiagramFrame

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics


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

        super().__init__(currentDirectory=currentDirectory, umlFrame=mockFrame)

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
