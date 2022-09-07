
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.DiagramFrame import DiagramFrame
from wx import CLIP_CHILDREN
from wx import ID_ANY
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import Frame
from wx import Notebook
from wx import SplitterWindow
from wx import TreeCtrl

from wx import TreeItemId

from tests.scaffoldv2.PyutProject import PyutProject

from tests.scaffoldv2.eventengine.EventEngine import EventEngine
from tests.scaffoldv2.eventengine.Events import AddProjectEvent
from tests.scaffoldv2.eventengine.Events import EVENT_ADD_PROJECT
from tests.scaffoldv2.eventengine.Events import EVENT_NEW_PROJECT
from tests.scaffoldv2.eventengine.Events import NewProjectEvent

PyutProjects = NewType('PyutProjects', List[PyutProject])


class ScaffoldUI:
    """
    This class is a container class that create user interface components
    in the parent frame
    """

    def __init__(self, topLevelFrame: Frame, createEmptyProject: bool = True):

        self._topLevelFrame: Frame = topLevelFrame
        self.logger:         Logger = getLogger(__name__)

        self._splitter:    SplitterWindow = cast(SplitterWindow, None)
        self._projectTree: TreeCtrl       = cast(TreeCtrl, None)
        self._notebook:    Notebook       = cast(Notebook, None)

        self._projectsRoot: TreeItemId    = cast(TreeItemId, None)

        self._projects:    PyutProjects = PyutProjects([])
        self._eventEngine: EventEngine  = EventEngine(listeningWindow=self._topLevelFrame)

        self._eventEngine.registerListener(EVENT_NEW_PROJECT, self._onNewProject)
        self._eventEngine.registerListener(EVENT_ADD_PROJECT, self._onAddProject)

        self._initializeUIElements()

        self._notebookCurrentPage: int = -1
        self._currentFrame:        DiagramFrame = cast(DiagramFrame, None)
        if createEmptyProject is True:
            self.createEmptyProject()

    def createEmptyProject(self):
        self._onNewProject(cast(NewProjectEvent, None))

    # noinspection PyUnusedLocal
    def _onNewProject(self, newProjectEvent: NewProjectEvent):
        """
        Begin a new project
        """
        project: PyutProject = PyutProject()
        projectTreeRoot: TreeItemId = self._projectTree.AppendItem(self._projectsRoot, PyutProject.DEFAULT_PROJECT_NAME, data=project)

        self._projectTree.Expand(projectTreeRoot)

        project.projectTreeRoot = projectTreeRoot

        self._projects.append(project)
        self._currentProject = project
        self._currentFrame = None

    def _onAddProject(self, addProjectEvent: AddProjectEvent):

        pyutProject:     PyutProject = addProjectEvent.pyutProject
        projectTreeRoot: TreeItemId  = pyutProject.projectTreeRoot

        # self._treeRoot = self._projectTree.AppendItem(parent=self._projectsRoot, text=projectName, data=pyutProject)
        self._projectTree.Expand(projectTreeRoot)

        # Add the frames
        # for document in pyutProject.documents:
        #     document.addToTree(self._tree, self._treeRoot)

    def _initializeUIElements(self):
        """
        Instantiate all the UI elements
        """
        self._splitter        = SplitterWindow(parent=self._topLevelFrame, id=ID_ANY)
        self._projectTree     = TreeCtrl(parent=self._splitter, id=ID_ANY, style=TR_HIDE_ROOT | TR_HAS_BUTTONS)
        # self._projectTree     = TreeCtrl(parent=self._splitter, id=ID_ANY, style=TR_HAS_BUTTONS)
        # diagram container
        self._notebook = Notebook(parent=self._splitter, id=ID_ANY, style=CLIP_CHILDREN)

        self._splitter.SetMinimumPaneSize(20)
        self._splitter.SplitVertically(self._projectTree, self._notebook, 160)

        self._projectsRoot = self._projectTree.AddRoot("Ozzee")

        # self._projectTree.Expand(self._projectsRoot)

        print(f'Hello')
        # Callbacks
        # self._parent.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onNotebookPageChanged)
        # self._parent.Bind(EVT_TREE_SEL_CHANGED, self._onProjectTreeSelChanged)
        # self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self.__onProjectTreeRightClick)
