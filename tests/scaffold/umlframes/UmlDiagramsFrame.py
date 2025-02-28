from logging import Logger
from logging import getLogger

from wx import Notebook

from tests.scaffold.umlframes.UmlFrame import UmlFrame


class UmlDiagramsFrame(UmlFrame):
    """
    ClassFrame : class diagram frame.

    This class is a frame where we can draw Class diagrams.

    It is used by UmlClassDiagramsFrame
    """

    def __init__(self, parent: Notebook):
        """

        Args:
            parent: wx.Window parent window;  In practice this is always wx.Notebook instance
        """
        self.umlDiagramFrameLogger: Logger = getLogger(__name__)

        super().__init__(parent)
