
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.DiagramFrame import DiagramFrame

from wx import CLIP_CHILDREN
from wx import ICON_ERROR
from wx import ID_ANY
from wx import OK
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import Frame
from wx import Notebook
from wx import SplitterWindow
from wx import TreeCtrl

from wx import MessageDialog

from wx import TreeItemId

from tests.scaffoldv2.MediatorV2 import MediatorV2
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

        self._mediatorV2: MediatorV2 = MediatorV2()
        #
        # Inject this so we can receive messages from the plugins
        #
        self._mediatorV2.eventEngine = self._eventEngine

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
        self._currentFrame = cast(DiagramFrame, None)

    def _onAddProject(self, addProjectEvent: AddProjectEvent):

        pyutProject:     PyutProject = addProjectEvent.pyutProject
        projectTreeRoot: TreeItemId  = pyutProject.projectTreeRoot

        # self._treeRoot = self._projectTree.AppendItem(parent=self._projectsRoot, text=projectName, data=pyutProject)
        self._projectTree.Expand(projectTreeRoot)

        # Add the frames
        # for document in pyutProject.documents:
        #     document.addToTree(self._tree, self._treeRoot)

    def __addProjectToNotebook(self, project: PyutProject) -> bool:

        success: bool = True
        try:
            # for document in project.getDocuments():
            for document in project.documents:
                diagramTitle: str = document.title
                # shortName:    str = self.__shortenNotebookPageFileName(diagramTitle)
                shortName:    str = diagramTitle
                self._notebook.AddPage(page=document.getFrame(), text=shortName)

            self.__notebookCurrentPage = self._notebook.GetPageCount()-1
            self._notebook.SetSelection(self.__notebookCurrentPage)

            self._updateTreeNotebookIfPossible(project=project)
        except (ValueError, Exception) as e:
            # PyutUtils.displayError(_(f"An error occurred while adding the project to the notebook {e}"))
            booBoo: MessageDialog = MessageDialog(parent=None, caption='Try Again!',
                                                  message=f'An error occurred while adding the project to the notebook {e}',
                                                  style=OK | ICON_ERROR)
            booBoo.ShowModal()

            success = False

        return success

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

    def _updateTreeNotebookIfPossible(self, project: PyutProject):

        # project.selectFirstDocument()

        # if len(project.getDocuments()) > 0:
        if len(project.documents) > 0:
            # self._currentFrame = project.getDocuments()[0].getFrame()
            self._currentFrame = project.documents[0].getFrame()
            self._syncPageFrameAndNotebook(frame=self._currentFrame)

    def _syncPageFrameAndNotebook(self, frame):
        for i in range(self._notebook.GetPageCount()):
            pageFrame = self._notebook.GetPage(i)
            if pageFrame is frame:
                self._notebook.SetSelection(i)
                break
