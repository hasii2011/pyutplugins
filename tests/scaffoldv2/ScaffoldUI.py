
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.SelectAnchorPoint import SelectAnchorPoint
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from wx import CLIP_CHILDREN
from wx import ClientDC
from wx import EVT_TREE_SEL_CHANGED
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
from wx import TreeEvent

from wx import TreeItemId

from wx import Yield as wxYield

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglInterface2 import OglInterface2

from core.IPluginAdapter import IPluginAdapter
from core.types.Types import FrameInformation
from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSize
from core.types.Types import FrameSizeCallback

from core.types.Types import PluginDocument
from core.types.Types import PluginDocumentType
from core.types.Types import PluginProject
from core.types.Types import OglLinks
from core.types.Types import SelectedOglObjectsCallback

from tests.scaffoldv2.PluginAdapterV2 import PluginAdapterV2
from tests.scaffoldv2.PyutDiagramType import PyutDiagramType
from tests.scaffoldv2.PyutDocument import PyutDocument
from tests.scaffoldv2.PyutProject import PyutProject
from tests.scaffoldv2.PyutProject import UmlFrameType

from tests.scaffoldv2.eventengine.EventEngine import EventEngine
from tests.scaffoldv2.eventengine.Events import DeSelectAllShapesEvent
from tests.scaffoldv2.eventengine.Events import EVENT_DESELECT_ALL_SHAPES

from tests.scaffoldv2.eventengine.Events import EVENT_FRAME_INFORMATION
from tests.scaffoldv2.eventengine.Events import EVENT_FRAME_SIZE
from tests.scaffoldv2.eventengine.Events import EVENT_REFRESH_FRAME
from tests.scaffoldv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES
from tests.scaffoldv2.eventengine.Events import EVENT_LOAD_PROJECT
from tests.scaffoldv2.eventengine.Events import EVENT_NEW_PROJECT
from tests.scaffoldv2.eventengine.Events import EVENT_SELECTED_OGL_OBJECTS

from tests.scaffoldv2.eventengine.Events import FrameSizeEvent
from tests.scaffoldv2.eventengine.Events import FrameInformationEvent
from tests.scaffoldv2.eventengine.Events import LoadProjectEvent
from tests.scaffoldv2.eventengine.Events import NewProjectEvent
from tests.scaffoldv2.eventengine.Events import RefreshFrameEvent
from tests.scaffoldv2.eventengine.Events import SelectAllShapesEvent
from tests.scaffoldv2.eventengine.Events import SelectedOglObjectsEvent

from tests.scaffoldv2.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from tests.scaffoldv2.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from tests.scaffoldv2.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

PyutProjects = NewType('PyutProjects', List[PyutProject])

TreeDataType = Union[PyutProject, UmlClassDiagramsFrame]


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

        self._initializeUIElements()

        self._notebookCurrentPage: int = -1
        self._currentFrame:        DiagramFrame = cast(DiagramFrame, None)

        self._mediatorV2: IPluginAdapter = cast(IPluginAdapter, None)

        if createEmptyProject is True:
            self.createEmptyProject()

    def getProjectFromFrame(self, frame: UmlDiagramsFrame) -> PyutProject:
        """
        Return the project that owns a given frame

        Args:
            frame:  the frame to get This project

        Returns:
            PyutProject or None if not found
        """
        for project in self._projects:
            if frame in project.frames:
                return project
        return cast(PyutProject, None)

    def _setPluginMediator(self, mediatorV2: PluginAdapterV2):
        """
        Write only property used to inject the plugin pluginAdapter
        Args:
            mediatorV2:
        """
        self._mediatorV2 = mediatorV2

    def _setEventEngine(self, eventEngine: EventEngine):
        """
        Write only property used to inject the event engine
        Once we get the event engine we can register our listeners

        Args:
            eventEngine:
        """
        self._eventEngine = eventEngine
        self._eventEngine.registerListener(EVENT_NEW_PROJECT,          self._onNewProject)
        self._eventEngine.registerListener(EVENT_LOAD_PROJECT,         self._onLoadProject)
        self._eventEngine.registerListener(EVENT_SELECT_ALL_SHAPES,    self._onSelectAll)
        self._eventEngine.registerListener(EVENT_DESELECT_ALL_SHAPES,  self._onDeSelectAll)
        self._eventEngine.registerListener(EVENT_SELECTED_OGL_OBJECTS, self._onSelectedOglObjects)
        self._eventEngine.registerListener(EVENT_REFRESH_FRAME,        self._onRefreshFrame)
        self._eventEngine.registerListener(EVENT_FRAME_SIZE,           self._onFrameSize)
        self._eventEngine.registerListener(EVENT_FRAME_INFORMATION,    self._onFrameInformation)

    pluginMediator = property(fset=_setPluginMediator)
    eventEngine    = property(fset=_setEventEngine)

    def createEmptyProject(self):
        self._onNewProject(cast(NewProjectEvent, None))

    # noinspection PyUnusedLocal
    def _onDeSelectAll(self, event: DeSelectAllShapesEvent):
        self._selectShapes(False)

    # noinspection PyUnusedLocal
    def _onSelectAll(self, event: SelectAllShapesEvent):
        self._selectShapes(True)
        # shapes = self._currentFrame.GetDiagram().GetShapes()
        # for shape in shapes:
        #     shape.SetSelected(True)
        #     self._currentFrame.GetSelectedShapes()
        #
        # self._currentFrame.SetSelectedShapes(shapes)
        # self._currentFrame.Refresh()

    def _selectShapes(self, selected: bool):
        """

        Args:
            selected: 'True' selects them all, 'False' deselects them
        """

        shapes = self._currentFrame.GetDiagram().GetShapes()
        for shape in shapes:
            shape.SetSelected(selected)
            self._currentFrame.GetSelectedShapes()

        self._currentFrame.SetSelectedShapes(shapes)
        self._currentFrame.Refresh()

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

    def _onLoadProject(self, loadProjectEvent: LoadProjectEvent):
        """
        When we load a project the Project node will have a PyutProject associated with it.
        Document nodes will have a PyutDocument node associated with them

        Args:
            loadProjectEvent:  The event has the PluginProject from the plugin that created it
        """

        pluginProject:   PluginProject = loadProjectEvent.pluginProject

        pyutProject:     PyutProject = PyutProject(projectName=pluginProject.projectName, codePath=pluginProject.codePath)
        projectTreeRoot: TreeItemId  = self._projectTree.AppendItem(self._projectsRoot, pluginProject.projectName, data=pyutProject)

        pyutProject.projectTreeRoot = projectTreeRoot

        # self._treeRoot = self._projectTree.AppendItem(parent=self._projectsRoot, text=projectName, data=pyutProject)

        # Add the frames
        for pluginDocument in pluginProject.pluginDocuments.values():
            # document.addToTree(self._tree, self._treeRoot)
            diagramType:  PyutDiagramType = self._toPyutDiagramType(pluginDocument.documentType)
            pyutDocument: PyutDocument    = PyutDocument(diagramType=diagramType)
            pyutDocument.title = pluginDocument.documentTitle

            umlClassDiagramsFrame: UmlClassDiagramsFrame = UmlClassDiagramsFrame(parent=self._notebook)
            pyutDocument.diagramFrame = umlClassDiagramsFrame

            itemId: TreeItemId = self._projectTree.AppendItem(parent=projectTreeRoot, text=pyutDocument.title, data=pyutDocument)
            self._projectTree.SelectItem(item=itemId, select=True)

            pyutProject.documents.append(pyutDocument)
            self._layoutPluginDocument(pluginDocument=pluginDocument, umlFrame=umlClassDiagramsFrame)

        self._projectTree.Expand(projectTreeRoot)

        self._addProjectToNotebook(project=pyutProject)
        self._projects.append(pyutProject)

    def _onSelectedOglObjects(self, event: SelectedOglObjectsEvent):

        selectedObjects = self._currentFrame.GetSelectedShapes()
        callback: SelectedOglObjectsCallback = event.callback

        callback(selectedObjects)

    # noinspection PyUnusedLocal
    def _onRefreshFrame(self, event: RefreshFrameEvent):
        self._currentFrame.Refresh()
        wxYield()

    def _onFrameSize(self, event: FrameSizeEvent):

        frameSize: FrameSize = FrameSize()

        (frameW, frameH) = self._currentFrame.GetSize()
        frameSize.width  = frameW
        frameSize.height = frameH

        callback: FrameSizeCallback = event.callback

        callback(frameSize)

    def _onFrameInformation(self, event: FrameInformationEvent):

        frameInformation: FrameInformation = FrameInformation()

        if self._currentFrame is None:
            frameInformation.frameActive = False
        else:
            frameInformation.frameActive = True
            frameInformation.clientDC          = ClientDC(self._currentFrame)
            frameInformation.selectedOglObjects = self._currentFrame.GetSelectedShapes()

            treeItemId: TreeItemId = self._projectTree.GetFocusedItem()
            itemData = self._projectTree.GetItemData(treeItemId)
            pyutDocument: PyutDocument = cast(PyutDocument, itemData)
            frameInformation.diagramTitle = pyutDocument.title
            frameInformation.diagramType  = pyutDocument.diagramType.__str__()
            (width, height) = self._currentFrame.GetSize()

            frameSize: FrameSize = FrameSize(width=width, height=height)

            frameInformation.frameSize         = frameSize

        callback: FrameInformationCallback = event.callback

        callback(frameInformation)

    def _addProjectToNotebook(self, project: PyutProject) -> bool:

        success: bool = True
        try:
            # for document in project.getDocuments():
            for document in project.documents:
                diagramTitle: str = document.title
                # shortName:    str = self.__shortenNotebookPageFileName(diagramTitle)
                shortName:    str = diagramTitle
                self._notebook.AddPage(page=document.diagramFrame, text=shortName)

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

        # Callbacks
        # self._parent.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onNotebookPageChanged)
        self._topLevelFrame.Bind(EVT_TREE_SEL_CHANGED, self._onProjectTreeSelChanged)
        # self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self.__onProjectTreeRightClick)

    def _updateTreeNotebookIfPossible(self, project: PyutProject):

        # project.selectFirstDocument()

        # if len(project.getDocuments()) > 0:
        if len(project.documents) > 0:
            # self._currentFrame = project.getDocuments()[0].getFrame()
            self._currentFrame = project.documents[0].diagramFrame
            self._syncPageFrameAndNotebook(frame=self._currentFrame)

    def _syncPageFrameAndNotebook(self, frame):
        for i in range(self._notebook.GetPageCount()):
            pageFrame = self._notebook.GetPage(i)
            if pageFrame is frame:
                self._notebook.SetSelection(i)
                break

    def _toPyutDiagramType(self, documentType: PluginDocumentType) -> PyutDiagramType:

        if documentType == PyutDiagramType.CLASS_DIAGRAM:
            return PyutDiagramType.CLASS_DIAGRAM
        elif documentType == PyutDiagramType.USECASE_DIAGRAM:
            return PyutDiagramType.USECASE_DIAGRAM
        else:
            return PyutDiagramType.SEQUENCE_DIAGRAM

    def _onProjectTreeSelChanged(self, event: TreeEvent):
        """
        Callback for tree node selection changed

        Args:
            event:
        """
        itm:      TreeItemId   = event.GetItem()
        pyutData: TreeDataType = self._projectTree.GetItemData(itm)
        self.logger.debug(f'Clicked on: {itm=} `{pyutData=}`')

        # Use our own base type
        if isinstance(pyutData, PyutDocument):
            pyutDocument: PyutDocument = pyutData
            frame: UmlClassDiagramsFrame = cast(UmlClassDiagramsFrame, pyutDocument.diagramFrame)
            self._currentFrame = frame
            self._currentProject = self.getProjectFromFrame(frame)
            # self.__syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProject):
            project: PyutProject = pyutData
            projectFrames: List[UmlFrameType] = project.frames
            if len(projectFrames) > 0:
                self._currentFrame = projectFrames[0]
                self.__syncPageFrameAndNotebook(frame=self._currentFrame)
                # self._pluginAdapter.updateTitle()
            self._currentProject = project

    def __syncPageFrameAndNotebook(self, frame):

        for i in range(self._notebook.GetPageCount()):
            pageFrame = self._notebook.GetPage(i)
            if pageFrame is frame:
                self._notebook.SetSelection(i)
                break

    def _layoutPluginDocument(self, pluginDocument: PluginDocument, umlFrame: UmlFrameShapeHandler):
        """
        Loads a plugin's Ogl Objects
        TODO: Not complete.  No sequence diagrams or use cases or OglTexts
        Args:
            pluginDocument: The plugin document itself
            umlFrame:   The Uml Frame to display them one
        """
        for oglClass in pluginDocument.oglClasses:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglClass)

        self._layoutLinks(umlFrame=umlFrame, oglLinks=pluginDocument.oglLinks)

        for oglNote in pluginDocument.oglNotes:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglNote)

        for oglText in pluginDocument.oglTexts:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglText)

        for oglUseCase in pluginDocument.oglUseCases:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglUseCase)

        for oglActor in pluginDocument.oglActors:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglActor)

        for oglSDInstance in pluginDocument.oglSDInstances.values():
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglSDInstance)

        for oglSDMessage in pluginDocument.oglSDMessages.values():
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglSDMessage)

    def _layoutAnOglObject(self, umlFrame: UmlFrameShapeHandler, oglObject: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink]):
        x, y = oglObject.GetPosition()
        umlFrame.addShape(oglObject, x, y)

    def _layoutLinks(self, umlFrame: UmlFrameShapeHandler, oglLinks: OglLinks):

        umlDiagram = umlFrame.GetDiagram()

        for oglLink in oglLinks:
            x, y = oglLink.GetPosition()
            umlFrame.addShape(oglLink, x=x, y=y)

            if isinstance(oglLink, OglInterface2) is False:
                umlDiagram.AddShape(oglLink.sourceAnchor)
                umlDiagram.AddShape(oglLink.destinationAnchor)
                controlPoints = oglLink.GetControlPoints()
                for controlPoint in controlPoints:
                    umlDiagram.AddShape(controlPoint)
