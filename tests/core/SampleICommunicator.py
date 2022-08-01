
from logging import Logger
from logging import getLogger
from typing import cast

from wx import Frame

from core.IMediator import IMediator


class SampleIMediator(IMediator):

    def __init__(self):
        self.logger:            Logger = getLogger(__name__)
        self._currentDirectory: str    = '/tmp'

    @property
    def currentDirectory(self) -> str:
        return self._currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, newValue: str):
        self._currentDirectory = newValue

    @property
    def umlFrame(self) -> Frame:
        return cast(Frame, None)
