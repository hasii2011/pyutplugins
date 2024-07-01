
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from sys import maxsize

from dataclasses import dataclass

from wx import Window

from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage


from tests.scaffoldv2.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler


UmlObject  = Union[OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2]
UmlObjects = NewType('UmlObjects', List[UmlObject])


NO_INTEGER: int = cast(int, None)


@dataclass
class OglObjectBoundaries:
    minX: int = NO_INTEGER
    minY: int = NO_INTEGER
    maxX: int = NO_INTEGER
    maxY: int = NO_INTEGER


class UmlFrame(UmlFrameShapeHandler):

    def __init__(self, parent: Window):
        """

        Args:
            parent:  The window where we put the UML Diagram Frames
        """

        super().__init__(parent)

        self.logger:       Logger = getLogger(__name__)

    def clearDiagram(self):
        """
        Remove all shapes, get a brand new empty diagram.
        TODO:  rename to clearDiagram
        """
        self._diagram.DeleteAllShapes()
        self.Refresh()

    def getDiagram(self):
        """
        Returns this frame's diagram

        Returns:  wx.Diagram
        """
        return self._diagram

    @property
    def umlObjects(self) -> UmlObjects:
        """
        Retrieve UML objects from the UML Frame

        Returns:  The Uml objects on this diagram
        """
        umlObjects: UmlObjects = UmlObjects([])

        for s in self._diagram.shapes:
            # This is a duplicate of the UmlObject, since I cannot use NewType
            if isinstance(s, (OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2)):
                umlObjects.append(s)

        return umlObjects

    @property
    def objectBoundaries(self) -> OglObjectBoundaries:
        """

        Return object boundaries (coordinates)

        """
        minX: int = maxsize
        maxX: int = -maxsize
        minY: int = maxsize
        maxY: int = -maxsize

        # Get boundaries
        for shapeObject in self._diagram.shapes:
            # Get object limits
            ox1, oy1 = shapeObject.GetPosition()
            ox2, oy2 = shapeObject.GetSize()
            ox2 += ox1
            oy2 += oy1

            # Update min-max
            minX = min(minX, ox1)
            maxX = max(maxX, ox2)
            minY = min(minY, oy1)
            maxY = max(maxY, oy2)

        # Return values
        return OglObjectBoundaries(minX=minX, minY=minY, maxX=maxX, maxY=maxY)
