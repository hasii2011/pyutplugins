
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger

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

        for s in self._diagram.GetShapes():
            # This is a duplicate of the UmlObject, since I cannot use NewType
            if isinstance(s, (OglClass, OglLink, OglNote, OglText, OglSDMessage, OglSDInstance, OglActor, OglUseCase, OglInterface2)):
                umlObjects.append(s)

        return umlObjects
