
from os import getcwd

from miniogl.DiagramFrame import DiagramFrame

from pyutplugincore.ICommunicator import ICommunicator


class ScaffoldCommunicator(ICommunicator):

    def __init__(self, umlFrame: DiagramFrame, currentDirectory: str = ''):

        if currentDirectory is None or currentDirectory == '':
            self._currentDirectory: str = getcwd()
        else:
            self._currentDirectory = currentDirectory

        super().__init__(currentDirectory=currentDirectory, umlFrame=umlFrame)
