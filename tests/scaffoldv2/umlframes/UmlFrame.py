
from logging import Logger
from logging import getLogger

from wx import Window

from tests.scaffoldv2.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler


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
