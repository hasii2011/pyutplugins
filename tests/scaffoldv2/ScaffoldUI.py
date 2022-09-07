
from logging import Logger
from logging import getLogger

from wx import CLIP_CHILDREN
from wx import Frame
from wx import ID_ANY
from wx import Notebook
from wx import SplitterWindow
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT
from wx import TreeCtrl


class ScaffoldUI:
    """
    This class is a container class that create user interface components
    in the parent frame
    """

    def __init__(self, topLevelFrame: Frame):

        self._topLevelFrame: Frame = topLevelFrame
        self.logger:         Logger = getLogger(__name__)

        self._initializeUIElements()

    def _initializeUIElements(self):
        """
        Instantiate all the UI elements
        """
        self._splitter        = SplitterWindow(parent=self._topLevelFrame, id=ID_ANY)
        self._projectTree     = TreeCtrl(parent=self._splitter, id=ID_ANY, style=TR_HIDE_ROOT + TR_HAS_BUTTONS)
        # diagram container
        self._notebook = Notebook(parent=self._splitter, id=ID_ANY, style=CLIP_CHILDREN)
        self._splitter.SetMinimumPaneSize(20)
        self._splitter.SplitVertically(self._projectTree, self._notebook, 160)

        self._notebookCurrentPage = -1
