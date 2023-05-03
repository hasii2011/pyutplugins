
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglActor import OglActor
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase

from wx import CLIP_CHILDREN
from wx import EVT_TREE_SEL_CHANGED
from wx import ICON_ERROR
from wx import ID_ANY
from wx import OK
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import ClientDC
from wx import Frame
from wx import Notebook
from wx import SplitterWindow
from wx import TreeCtrl
from wx import MessageDialog
from wx import TreeEvent
from wx import TreeItemId

from wx import Yield as wxYield

from miniogl.DiagramFrame import DiagramFrame
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.Diagram import Diagram

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from ogl.OglInterface2 import OglInterface2

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

from oglio.Types import OglDocument
from oglio.Types import OglProject

from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformation
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSize
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import HybridLinks
from pyutplugins.ExternalTypes import OglLinks
from pyutplugins.ExternalTypes import PluginDocument
from pyutplugins.ExternalTypes import PluginDocumentTitle
from pyutplugins.ExternalTypes import PluginDocumentType
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback

from tests.scaffoldv2.PyutDiagramType import PyutDiagramType
from tests.scaffoldv2.PyutDocument import PyutDocument
from tests.scaffoldv2.PyutProject import PyutProject
from tests.scaffoldv2.PyutProject import UmlFrameType

from tests.scaffoldv2.eventengine.EventEngine import EventEngine
from tests.scaffoldv2.eventengine.Events import AddShapeEvent
from tests.scaffoldv2.eventengine.Events import LoadOglProjectEvent
from tests.scaffoldv2.eventengine.Events import RequestCurrentProjectEvent
from tests.scaffoldv2.eventengine.Events import DeSelectAllShapesEvent
from tests.scaffoldv2.eventengine.Events import EVENT_ADD_SHAPE

from tests.scaffoldv2.eventengine.Events import EVENT_DESELECT_ALL_SHAPES
from tests.scaffoldv2.eventengine.Events import EVENT_FRAME_INFORMATION
from tests.scaffoldv2.eventengine.Events import EVENT_FRAME_SIZE
from tests.scaffoldv2.eventengine.Events import EVENT_NEW_DIAGRAM
from tests.scaffoldv2.eventengine.Events import EVENT_REFRESH_FRAME
from tests.scaffoldv2.eventengine.Events import EVENT_SELECT_ALL_SHAPES
from tests.scaffoldv2.eventengine.Events import EVENT_LOAD_PROJECT
from tests.scaffoldv2.eventengine.Events import EVENT_NEW_PROJECT
from tests.scaffoldv2.eventengine.Events import EVENT_SELECTED_OGL_OBJECTS
from tests.scaffoldv2.eventengine.Events import EventType

from tests.scaffoldv2.eventengine.Events import FrameSizeEvent
from tests.scaffoldv2.eventengine.Events import FrameInformationEvent
from tests.scaffoldv2.eventengine.Events import LoadProjectEvent
from tests.scaffoldv2.eventengine.Events import NewDiagramEvent
from tests.scaffoldv2.eventengine.Events import NewProjectEvent
from tests.scaffoldv2.eventengine.Events import RefreshFrameEvent
from tests.scaffoldv2.eventengine.Events import SelectAllShapesEvent
from tests.scaffoldv2.eventengine.Events import SelectedOglObjectsEvent

from tests.scaffoldv2.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from tests.scaffoldv2.umlframes.UmlDiagramsFrame import UmlDiagramsFrame
from tests.scaffoldv2.umlframes.UmlFrame import UmlFrame
from tests.scaffoldv2.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

PyutProjects = NewType('PyutProjects', List[PyutProject])

TreeDataType = Union[PyutProject, UmlClassDiagramsFrame]

NO_DIAGRAM_FRAME: UmlDiagramsFrame = cast(UmlDiagramsFrame, None)


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

        self._projectsRoot: TreeItemId   = cast(TreeItemId, None)
        self._projects:     PyutProjects = PyutProjects([])

        self._initializeUIElements()

        self._notebookCurrentPage: int = -1
        self._currentProject:      PyutProject      = cast(PyutProject, None)
        self._currentFrame:        UmlDiagramsFrame = cast(UmlDiagramsFrame, None)

        if createEmptyProject is True:
            self.createEmptyProject()

        self._topLevelFrame.Bind(EVT_TREE_SEL_CHANGED,      self._onProjectTreeSelectionChanged)

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

    def _setEventEngine(self, eventEngine: EventEngine):
        """
        Write only property used to inject the event engine
        Once we get the event engine we can register our listeners

        Args:
            eventEngine:
        """
        self._eventEngine = eventEngine
        self._eventEngine.registerListener(EVENT_NEW_PROJECT,          self._onNewProject)
        self._eventEngine.registerListener(EVENT_NEW_DIAGRAM,          self._onNewDiagram)
        self._eventEngine.registerListener(EVENT_LOAD_PROJECT,         self._onLoadProject)
        self._eventEngine.registerListener(EVENT_SELECT_ALL_SHAPES,    self._onSelectAll)
        self._eventEngine.registerListener(EVENT_DESELECT_ALL_SHAPES,  self._onDeSelectAll)
        self._eventEngine.registerListener(EVENT_SELECTED_OGL_OBJECTS, self._onSelectedOglObjects)
        self._eventEngine.registerListener(EVENT_REFRESH_FRAME,        self._onRefreshFrame)
        self._eventEngine.registerListener(EVENT_FRAME_SIZE,           self._onFrameSize)
        self._eventEngine.registerListener(EVENT_FRAME_INFORMATION,    self._onFrameInformation)
        self._eventEngine.registerListener(EVENT_ADD_SHAPE,            self._onAddShape)

        self._eventEngine.registerListener(EventType.LoadOglProject.pyEventBinder, self._onLoadOglProject)

        self._eventEngine.registerListener(EventType.RequestCurrentProject.pyEventBinder, self._onRequestCurrentProject)

    eventEngine    = property(fset=_setEventEngine)

    def createEmptyProject(self):
        self._onNewProject(cast(NewProjectEvent, None))

    def _onProjectTreeSelectionChanged(self, event: TreeEvent):
        """
        Called when the selection in the project changes

        Args:
            event:
        """
        itm:      TreeItemId   = event.GetItem()
        pyutData: TreeDataType = self._projectTree.GetItemData(itm)
        self.logger.debug(f'Clicked on: {itm=} `{pyutData=}`')

        # Use our own base type
        if isinstance(pyutData, PyutDocument):
            pyutDocument: PyutDocument          = cast(PyutDocument, pyutData)
            frame:        UmlClassDiagramsFrame = pyutDocument.diagramFrame

            self.currentFrame    = frame
            self.currentDocument = pyutDocument

            self._syncPageFrameAndNotebook(frame=frame)

        elif isinstance(pyutData, PyutProject):
            project: PyutProject = pyutData
            self.currentProject = project
            projectFrames: List[UmlFrameType] = project.frames
            if len(projectFrames) > 0:
                self.currentFrame = projectFrames[0]
            else:
                self.currentFrame = NO_DIAGRAM_FRAME

            self._syncPageFrameAndNotebook(frame=self.currentFrame)
            self.currentProject = project

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

        shapes = self._currentFrame.diagram.GetShapes()
        for shape in shapes:
            shape.selected = selected

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

        pyutProject:     PyutProject = PyutProject(fileName=pluginProject.projectName, codePath=pluginProject.codePath)
        projectTreeRoot: TreeItemId  = self._projectTree.AppendItem(self._projectsRoot, pluginProject.projectName, data=pyutProject)

        pyutProject.projectTreeRoot = projectTreeRoot

        # Add the frames
        for pluginDocument in pluginProject.pluginDocuments.values():

            diagramType:  PyutDiagramType = self._toPyutDiagramType(pluginDocument.documentType)
            pyutDocument: PyutDocument    = self._newDiagram(diagramType=diagramType)
            pyutDocument.title = pluginDocument.documentTitle

            itemId: TreeItemId = self._projectTree.AppendItem(parent=projectTreeRoot, text=pyutDocument.title, data=pyutDocument)
            self._projectTree.SelectItem(item=itemId, select=True)

            pyutProject.documents.append(pyutDocument)
            self._layoutPluginDocument(pluginDocument=pluginDocument, umlFrame=pyutDocument.diagramFrame)

        self._projectTree.Expand(projectTreeRoot)

        self._addProjectToNotebook(project=pyutProject)
        self._projects.append(pyutProject)
        self._currentProject = pyutProject
        self._synchronizeWithSelectedTreeItem()

    def _onLoadOglProject(self, event: LoadOglProjectEvent):
        oglProject: OglProject = event.oglProject
        pyutProject: PyutProject = PyutProject(fileName=oglProject.fileName, codePath=oglProject.codePath)
        projectTreeRoot: TreeItemId  = self._projectTree.AppendItem(self._projectsRoot, pyutProject.projectName, data=pyutProject)

        pyutProject.projectTreeRoot = projectTreeRoot

        # Add the frames
        for document in oglProject.oglDocuments.values():
            oglDocument:  OglDocument     = cast(OglDocument, document)
            diagramType:  PyutDiagramType = PyutDiagramType.toEnum(oglDocument.documentType)
            pyutDocument: PyutDocument    = self._newDiagram(diagramType=diagramType)
            pyutDocument.title            = oglDocument.documentTitle

            itemId: TreeItemId = self._projectTree.AppendItem(parent=projectTreeRoot, text=pyutDocument.title, data=pyutDocument)
            self._projectTree.SelectItem(item=itemId, select=True)

            pyutProject.documents.append(pyutDocument)
            self._layoutOglDocument(oglDocument=oglDocument, umlFrame=pyutDocument.diagramFrame)

        self._projectTree.Expand(projectTreeRoot)

        self._addProjectToNotebook(project=pyutProject)
        self._projects.append(pyutProject)
        self._currentProject = pyutProject

        self.logger.info(f'{oglProject=}')
        self._synchronizeWithSelectedTreeItem()

    def _onNewDiagram(self, newDiagramEvent: NewDiagramEvent):

        diagramType: PyutDiagramType = newDiagramEvent.diagramType
        self.logger.info(f"{diagramType=}")

        pyutProject: PyutProject = self._currentProject
        pyutDocument: PyutDocument = self._newDiagram(diagramType=diagramType)

        projectTreeRoot = pyutProject.projectTreeRoot

        itemId: TreeItemId = self._projectTree.AppendItem(parent=projectTreeRoot, text=pyutDocument.title, data=pyutDocument)
        self._projectTree.SelectItem(item=itemId, select=True)

        self._notebook.AddPage(page=pyutDocument.diagramFrame, text=pyutDocument.title)

        pyutProject.documents.append(pyutDocument)

    def _newDiagram(self, diagramType: PyutDiagramType) -> PyutDocument:
        """
        Create the appropriate PyutDocument
        Args:
            diagramType:

        Returns:  The PyutDocument
        """
        pyutDocument: PyutDocument = PyutDocument(diagramType=diagramType)
        pyutDocument.title = 'New Diagram'

        umlClassDiagramsFrame: UmlClassDiagramsFrame = UmlClassDiagramsFrame(parent=self._notebook)
        pyutDocument.diagramFrame = umlClassDiagramsFrame

        self._currentFrame = umlClassDiagramsFrame
        umlClassDiagramsFrame.Refresh()
        return pyutDocument

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

    def _onAddShape(self, event: AddShapeEvent):
        shapeToAdd: OglObject = event.shapeToAdd

        umlFrame: UmlDiagramsFrame = self._currentFrame

        match shapeToAdd:
            case OglLink() as shapeToAdd:
                self._layoutOglLink(umlFrame=umlFrame, link=cast(OglLink, shapeToAdd))
            case OglSDInstance() as shapeToAdd:
                self._layoutOglSDInstance(diagram=umlFrame.getDiagram(), oglSDInstance=cast(OglSDInstance, shapeToAdd))
            case OglSDMessage() as shapeToAdd:
                self._layoutOglSDMessage(diagram=umlFrame.getDiagram(), oglSDMessage=cast(OglSDMessage, shapeToAdd))
            case _:
                self._layoutAnOglObject(umlFrame=umlFrame, oglObject=shapeToAdd)

    def _onRequestCurrentProject(self, event: RequestCurrentProjectEvent):
        """
        Has to return a PluginProject
        Args:
            event:
        """
        pluginProject: PluginProject = PluginProject()

        cb:          CurrentProjectCallback = event.callback
        pyutProject: PyutProject            = self._currentProject

        pluginProject.projectName = pyutProject.projectName
        pluginProject.fileName    = pyutProject.projectName
        pluginProject.codePath    = pyutProject.codePath

        for document in pyutProject.documents:
            pyutDocument:   PyutDocument = cast(PyutDocument, document)
            pluginDocument: PluginDocument = PluginDocument()

            pluginDocument.documentType  = PluginDocumentType.toEnum(pyutDocument.diagramType.name)
            pluginDocument.documentTitle = PluginDocumentTitle(pyutDocument.title)

            diagramFrame: UmlFrame = pyutDocument.diagramFrame
            scrollPosX, scrollPosY = diagramFrame.GetViewStart()
            xUnit, yUnit = diagramFrame.GetScrollPixelsPerUnit()

            pluginDocument.scrollPositionX = scrollPosX
            pluginDocument.scrollPositionY = scrollPosY
            pluginDocument.pixelsPerUnitX  = xUnit
            pluginDocument.pixelsPerUnitY  = yUnit
            for umlObject in diagramFrame.umlObjects:
                match umlObject:
                    case OglInterface2():
                        oglInterface2: OglInterface2 = cast(OglInterface2, umlObject)
                        pluginDocument.oglLinks.append(oglInterface2)
                    case OglSDInstance():
                        oglSDInstance: OglSDInstance = cast(OglSDInstance, umlObject)
                        pluginDocument.oglSDInstances[oglSDInstance.pyutObject.id] = oglSDInstance
                    case OglSDMessage():
                        oglSDMessage: OglSDMessage = cast(OglSDMessage, umlObject)
                        pluginDocument.oglSDMessages[oglSDMessage.pyutObject.id] = oglSDMessage
                    case OglClass():
                        pluginDocument.oglClasses.append(umlObject)
                    case OglLink():
                        pluginDocument.oglLinks.append(umlObject)
                    case OglNote():
                        pluginDocument.oglNotes.append(umlObject)
                    case OglText():
                        pluginDocument.oglTexts.append(umlObject)
                    case OglActor():
                        pluginDocument.oglActors.append(umlObject)
                    case OglUseCase():
                        pluginDocument.oglUseCases.append(umlObject)
                    case _:
                        self.logger.error(f'Unknown umlObject: {umlObject=}')

            pluginProject.pluginDocuments[pluginDocument.documentTitle] = pluginDocument

        cb(pluginProject)

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

        if len(project.documents) > 0:

            self._currentFrame = project.documents[0].diagramFrame
            self._syncPageFrameAndNotebook(frame=self._currentFrame)

    def _synchronizeWithSelectedTreeItem(self):

        selectedItem: TreeItemId = self._projectTree.GetSelection()
        data = self._projectTree.GetItemData(selectedItem)

        selectedDocument: PyutDocument = cast(PyutDocument, data)
        assert isinstance(data, PyutDocument), 'Oops not pyut document'

        activeFrame: UmlClassDiagramsFrame = selectedDocument.diagramFrame
        self._syncPageFrameAndNotebook(frame=activeFrame)

    def _syncPageFrameAndNotebook(self, frame: UmlClassDiagramsFrame):
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

    def _layoutPluginDocument(self, pluginDocument: PluginDocument, umlFrame: UmlDiagramsFrame):
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

    def _layoutOglDocument(self, oglDocument: OglDocument, umlFrame: UmlDiagramsFrame):
        for oglClass in oglDocument.oglClasses:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglClass)
        self._layoutLinks(umlFrame=umlFrame, oglLinks=cast(OglLinks, oglDocument.oglLinks))
        for oglNote in oglDocument.oglNotes:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglNote)
        for oglText in oglDocument.oglTexts:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglText)

        for oglUseCase in oglDocument.oglUseCases:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglUseCase)

        for oglActor in oglDocument.oglActors:
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglActor)

        for oglSDInstance in oglDocument.oglSDInstances.values():
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglSDInstance)

        for oglSDMessage in oglDocument.oglSDMessages.values():
            self._layoutAnOglObject(umlFrame=umlFrame, oglObject=oglSDMessage)

    def _layoutLinks(self, umlFrame: UmlDiagramsFrame, oglLinks: OglLinks):

        # umlDiagram = umlFrame.GetDiagram()

        for oglLink in oglLinks:
            self._layoutOglLink(umlFrame=umlFrame, link=oglLink)
            # x, y = oglLink.GetPosition()
            # umlFrame.addShape(oglLink, x=x, y=y)
            #
            # if isinstance(oglLink, OglInterface2) is False:
            #     umlDiagram.AddShape(oglLink.sourceAnchor)
            #     umlDiagram.AddShape(oglLink.destinationAnchor)
            #     controlPoints = oglLink.GetControlPoints()
            #     for controlPoint in controlPoints:
            #         umlDiagram.AddShape(controlPoint)

    def _layoutOglLink(self, umlFrame: UmlDiagramsFrame, link: HybridLinks):

        self._layoutAnOglObject(umlFrame=umlFrame, oglObject=link)
        # TODO:
        # This is bad mooky here. The Ogl objects were created withing having a Diagram
        # The legacy code deserialized the object while adding them to a frame. This
        # new code deserializes w/o reference to a frame
        # If we don't this the AnchorPoints are not on the diagram and lines ends are not
        # movable.
        if isinstance(link, OglInterface2) is False:
            oglLink: OglLink = cast(OglLink, link)
            umlDiagram = umlFrame.diagram

            umlDiagram.AddShape(oglLink.sourceAnchor)
            umlDiagram.AddShape(oglLink.destinationAnchor)
            controlPoints = oglLink.GetControlPoints()
            for controlPoint in controlPoints:
                umlDiagram.AddShape(controlPoint)

    def _layoutOglSDInstance(self, diagram: Diagram, oglSDInstance: OglSDInstance):
        diagram.AddShape(oglSDInstance)

    def _layoutOglSDMessage(self, diagram: Diagram, oglSDMessage: OglSDMessage):
        diagram.AddShape(oglSDMessage)

    def _layoutAnOglObject(self, umlFrame: UmlFrameShapeHandler, oglObject: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink]):
        x, y = oglObject.GetPosition()
        umlFrame.addShape(oglObject, x, y)
