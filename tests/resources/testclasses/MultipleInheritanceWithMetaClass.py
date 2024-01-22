
from logging import Logger
from logging import getLogger

from abc import abstractmethod
from abc import ABCMeta

from wx import Command


class BaseWxCommand(Command):
    """
    This is a stubbed out class from Pyut to test multiple inheritance
    with a metaclass
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, canUndo: bool, name: str):

        super().__init__(canUndo=canUndo, name=name)

    def _removeOglObjectFromFrame(self):
        pass

    def _addOglClassToFrame(self):
        pass

    def _isSameObject(self) -> bool:
        """
        Returns:  `True` if they are one and the same, else `False`
        """
        ans: bool = False

        return ans


BaseWxCommandMeta = type(BaseWxCommand)


class MyMetaBaseWxCommand(ABCMeta, BaseWxCommandMeta):
    """
    I have no idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class BaseWxCreateCommand(BaseWxCommand, metaclass=MyMetaBaseWxCommand):
    """
    Stubbed out class from Pyut
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, canUndo: bool, name: str, x: int, y: int):

        super().__init__(canUndo=canUndo, name=name)

        self._oglObjX:     int = x
        self._oglObjY:     int = y
        self._name:        str = name

    def GetName(self) -> str:
        return self._name

    def CanUndo(self):
        return True

    def Do(self) -> bool:
        self._placeShapeOnFrame()
        return True

    def Undo(self) -> bool:
        return True

    @abstractmethod
    def _createPrototypeInstance(self):
        """
        Creates an appropriate class for the new command

        Returns:    The newly created class
        """
        pass

    @abstractmethod
    def _placeShapeOnFrame(self):
        pass

    def _cbGetActiveUmlFrameForUndo(self):
        pass

    def _cbAddOglObjectToFrame(self):
        pass
