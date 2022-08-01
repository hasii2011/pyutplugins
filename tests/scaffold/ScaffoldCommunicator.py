
from os import getcwd

from miniogl.DiagramFrame import DiagramFrame

from core.IMediator import IMediator


class ScaffoldMediator(IMediator):

    def __init__(self, umlFrame: DiagramFrame, currentDirectory: str = ''):

        if currentDirectory is None or currentDirectory == '':
            self._currentDirectory: str = getcwd()
        else:
            self._currentDirectory = currentDirectory

        super().__init__(currentDirectory=currentDirectory, umlFrame=umlFrame)
