
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger

from miniogl.Diagram import Diagram
from ogl.events.OglEventEngine import OglEventEngine
from wx import EVT_CLOSE
from wx import EVT_PAINT
from wx import Frame

from wx import MouseEvent
from wx import Window

from ogl.OglInterface2 import OglInterface2
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink

from ogl.sd.OglSDMessage import OglSDMessage

from miniogl.DiagramFrame import DiagramFrame

DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

UmlObject  = Union[OglObject, OglLink, OglSDMessage, OglInterface2]
UmlObjects = NewType('UmlObjects', List[UmlObject])


class DisplayUmlFrame(DiagramFrame):
    """
    Represents a minimal canvas for drawing diagrams.
    Used for the manual testing of Plugins that need to display their results
    """
    PIXELS_PER_UNIT_X: int = 20
    PIXELS_PER_UNIT_Y: int = 20

    def __init__(self, parent: Window, frame: Frame):
        """

        Args:
            parent: The parent window
            frame:  The uml frame
        """
        super().__init__(parent)

        self._frame: Window = frame
        self.logger: Logger = getLogger(__name__)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / DisplayUmlFrame.PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / DisplayUmlFrame.PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(DisplayUmlFrame.PIXELS_PER_UNIT_X, DisplayUmlFrame.PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        # Close event
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_PAINT, self.OnPaint)

        self.SetInfinite(True)

        self._defaultCursor = self.GetCursor()
        # self.Layout()
        #
        # We won't forward anything just yet
        self._eventEngine: OglEventEngine = OglEventEngine(listeningWindow=self)

    @property
    def eventEngine(self) -> OglEventEngine:
        return self._eventEngine

    def cleanUp(self):
        """
        """
        self._mediator = None
        self._frame = None

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE
        """
        self.cleanUp()
        self.Destroy()

    def OnLeftDown(self, event: MouseEvent):
        """
        Manage a left down mouse event.
        If there's an action pending in the mediator, give it the event, else
        let it go to the next handler.
        """
        # DiagramFrame.OnLeftDown(self, event)
        super().OnLeftDown(event)

    def OnLeftUp(self, event):
        """
        to make the right action if it is a selection or a zoom.
        """
        # DiagramFrame.OnLeftUp(self, event)
        super().OnLeftUp(event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Manage a left double click mouse event.

        Args:
            event:
        """

        # x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        # self._mediator.editObject(x, y)

        # DiagramFrame.OnLeftDClick(self, event)
        super().OnLeftDClick(event)

    def clearDiagram(self):
        """
        Remove all shapes, get a brand new empty diagram.
        """
        self._diagram.DeleteAllShapes()
        self.Refresh()

    @property
    def diagram(self) -> Diagram:
        """
        Return this frame's diagram
        """
        return self._diagram

    def getUmlObjects(self) -> UmlObjects:
        """
        Retrieve UML objects from the UML Frame

        Returns:  The Uml objects on this diagram
        """
        umlObjects: UmlObjects = UmlObjects([])

        for s in self._diagram.GetShapes():
            if isinstance(s, (OglObject, OglLink, OglSDMessage, OglInterface2)):
                umlObjects.append(s)

        return umlObjects

    def getWidth(self):
        """

        Returns:  The frame width

        """
        return self.maxWidth

    def getHeight(self):
        """

        Returns: The frame height
        """
        return self.maxHeight

    def getUmlObjectById(self, objectId: int):
        """

        Args:
            objectId:  The ID of the object we want

        Returns:  The uml object that has the specified id. If there is no
        matching object, None may be returned.
        """
        for shape in self.GetDiagram().GetShapes():
            if isinstance(shape, (OglObject, OglLink)):
                if shape.pyutObject.id == objectId:
                    return shape
        return None

    def addShape(self, oglObject: Union[OglObject, OglLink, OglInterface2]):
        self._diagram.AddShape(oglObject)
