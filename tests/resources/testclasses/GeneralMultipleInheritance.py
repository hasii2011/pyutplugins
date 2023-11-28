from abc import abstractmethod
from logging import Logger
from logging import getLogger

from abc import ABC
from typing import Any
from typing import List
from typing import cast

from wx import MouseEvent


class EventEngineMixin(ABC):
    """
    Some of the graphic components needs to send messages when they do significant UI
    actions
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._eventEngine = None

    @property
    def eventEngine(self):
        return self._eventEngine

    @abstractmethod
    def GetDiagram(self):
        pass

    @abstractmethod
    def HasDiagramFrame(self):
        pass


class ShapeEventHandler:

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):
        pass

    def OnLeftDown(self, event: MouseEvent):
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        event.Skip()

    def OnLeftDClick(self, event: MouseEvent):
        event.Skip()

    def OnMiddleDown(self, event: MouseEvent):
        event.Skip()

    def OnMiddleUp(self, event: MouseEvent):
        event.Skip()

    def OnMiddleDClick(self, event: MouseEvent):
        event.Skip()

    def OnRightDown(self, event: MouseEvent):
        event.Skip()

    def OnRightUp(self, event: MouseEvent):
        event.Skip()

    def OnRightDClick(self, event: MouseEvent):
        event.Skip()


class RectangleShape:
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):

        self._x:      int = x
        self._y:      int = y
        self._width:  int = width   # width and height can be < 0 !!!
        self._height: int = height

        self._drawFrame: bool = True
        self._resizable: bool = True
        self._selected:  bool = False

        self._ox: int = 0   # This is done in Shape but Pycharm can't see this in the ShowSizer() code

    @property
    def selected(self) -> bool:
        """
        Override Shape

        Returns: 'True' if selected 'False' otherwise
        """
        return self._selected

    @selected.setter
    def selected(self, state: bool):
        self._selected = state


class OglObject(RectangleShape, ShapeEventHandler, EventEngineMixin):
    """
    Stub class for testing
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, pyutObject=None, width: int = 0, height: int = 0):
        """

        Args:
            pyutObject: Associated PyutObject
            width:      Initial width
            height:     Initial height
        """
        self._pyutObject = pyutObject

        super().__init__(0, 0, width, height)

        self._modifyCommand = None
        self._oglLinks: List[Any]      = cast(Any, None)

    @property
    def pyutObject(self):
        return self._pyutObject

    @pyutObject.setter
    def pyutObject(self, pyutObject):
        self._pyutObject = pyutObject

    @property
    def links(self):
        return self._oglLinks

    def addLink(self, link):
        self._oglLinks.append(link)

    def OnLeftDown(self, event: MouseEvent):
        event.Skip()

    def OnLeftUp(self, event: MouseEvent):
        event.Skip()

    def autoResize(self):
        """
        Find the right size to see all the content and resize self.

        """
        pass

    def SetPosition(self):
        self._indicateDiagramModified()

    def SetSelected(self, state=True):
        self.selected = state

    def _indicateDiagramModified(self):
        pass

    def GetDiagram(self):
        pass

    def HasDiagramFrame(self):
        pass
