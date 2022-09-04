
from os import getcwd

from miniogl.DiagramFrame import DiagramFrame

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics


class ScaffoldMediator(IMediator):
    """
    Shortcut implement the version and screen metrics properties
    """

    def __init__(self, umlFrame: DiagramFrame, currentDirectory: str = ''):

        if currentDirectory is None or currentDirectory == '':
            self._currentDirectory: str = getcwd()
        else:
            self._currentDirectory = currentDirectory

        super().__init__(currentDirectory=currentDirectory, umlFrame=umlFrame)

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
