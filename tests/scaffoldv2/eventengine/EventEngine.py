
from logging import Logger
from logging import getLogger
from typing import Callable

from wx import MessageBox
from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from oglio.Types import OglProject

from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback

from tests.scaffoldv2.PyutDiagramType import PyutDiagramType
from tests.scaffoldv2.eventengine.Events import AddShapeEvent
from tests.scaffoldv2.eventengine.Events import CreateLinkEvent
from tests.scaffoldv2.eventengine.Events import DeSelectAllShapesEvent
from tests.scaffoldv2.eventengine.Events import DeleteLinkEvent

from tests.scaffoldv2.eventengine.Events import EventType
from tests.scaffoldv2.eventengine.Events import FrameInformationEvent
from tests.scaffoldv2.eventengine.Events import FrameSizeEvent
from tests.scaffoldv2.eventengine.Events import GetObjectBoundariesEvent
from tests.scaffoldv2.eventengine.Events import LoadOglProjectEvent
from tests.scaffoldv2.eventengine.Events import LoadProjectEvent
from tests.scaffoldv2.eventengine.Events import NewDiagramEvent
from tests.scaffoldv2.eventengine.Events import NewProjectEvent
from tests.scaffoldv2.eventengine.Events import RefreshFrameEvent
from tests.scaffoldv2.eventengine.Events import RequestCurrentProjectEvent
from tests.scaffoldv2.eventengine.Events import SelectAllShapesEvent
from tests.scaffoldv2.eventengine.Events import SelectedOglObjectsEvent
from tests.scaffoldv2.eventengine.Events import UpdateTreeItemNameEvent

from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine

NEW_NAME_PARAMETER:          str = 'newName'
TREE_ITEM_ID_PARAMETER:      str = 'treeItemId'
PLUGIN_PROJECT_PARAMETER:    str = 'pluginProject'
OGL_PROJECT_PARAMETER:       str = 'oglProject'
CALLBACK_PARAMETER:          str = 'callback'
DIAGRAM_TYPE_PARAMETER:      str = 'diagramType'
SHAPE_PARAMETER:             str = 'shapeToAdd'
OGL_LINK_PARAMETER:          str = 'oglLink'
LINK_TYPE_PARAMETER:         str = 'linkType'
PATH_PARAMETER:              str = 'path'
SOURCE_SHAPE_PARAMETER:      str = 'sourceShape'
DESTINATION_SHAPE_PARAMETER: str = 'destinationShape'
LINK_INFORMATION_PARAMETER:  str = 'linkInformation'


class EventEngine(IEventEngine):
    """
    The rationale for this class is to isolate the underlying implementation
    of events.  Currently, it depends on the wxPython event loop.  This leaves
    it open to other implementations;

    Get one of these for each Window you want to listen on
    """

    def __init__(self, listeningWindow: Window):

        self._listeningWindow: Window = listeningWindow
        self.logger: Logger = getLogger(__name__)

    def registerListener(self, event: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(event, callback)

    def sendEvent(self, eventType: EventType, **kwargs):

        match eventType:
            case EventType.UpdateTreeItemName:
                self._sendUpdateTreeItemNameEvent(**kwargs)
            case EventType.LoadProjectEvent:
                self._sendLoadProjectEvent(**kwargs)
            case EventType.NewProject:
                self._sendNewProjectEvent()
            case EventType.NewDiagram:
                self._sendNewDiagramEvent(**kwargs)
            case EventType.SelectAllShapes:
                self._sendSelectShapesAllEvent()
            case EventType.DeSelectAllShapes:
                self._sendDeSelectAllShapesEvent()
            case EventType.AddShape:
                self._sendAddShapeEvent(**kwargs)
            case EventType.RefreshFrame:
                self._sendRefreshFrameEvent()
            case EventType.SelectedOglObjects:
                self._sendSelectedOglObjectsEvent(**kwargs)
            case EventType.FrameInformation:
                self._sendFrameInformationEvent(**kwargs)
            case EventType.FrameSize:
                self._sendFrameSizeEvent(**kwargs)
            case EventType.RequestCurrentProject:
                self._sendRequestCurrentProjectEvent(**kwargs)
            case EventType.LoadOglProject:
                self._sendLoadOglProjectEvent(**kwargs)
            case EventType.GetObjectBoundaries:
                self._sendGetObjectBoundariesEvent(**kwargs)
            case EventType.DeleteLink:
                self._sendDeleteLinkEvent(**kwargs)
            case EventType.CreateLink:
                self._sendCreateLinkEvent(**kwargs)
            case EventType.IndicatePluginModifiedProject:
                MessageBox("Project Modified", caption="")
            case _:
                assert False, f'Unknown event type: `{eventType}`'

    def _sendUpdateTreeItemNameEvent(self, **kwargs):

        newName: str = kwargs[NEW_NAME_PARAMETER]
        treeItemId: TreeItemId = kwargs[TREE_ITEM_ID_PARAMETER]
        eventToPost: UpdateTreeItemNameEvent = UpdateTreeItemNameEvent(newName=newName, treeItemId=treeItemId)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewProjectEvent(self):
        eventToPost: NewProjectEvent = NewProjectEvent()
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendNewDiagramEvent(self, **kwargs):
        diagramType: PyutDiagramType = kwargs[DIAGRAM_TYPE_PARAMETER]
        eventToPost: NewDiagramEvent = NewDiagramEvent(diagramType=diagramType)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendLoadProjectEvent(self, **kwargs):

        pluginProject: PluginProject = kwargs[PLUGIN_PROJECT_PARAMETER]
        eventToPost: LoadProjectEvent = LoadProjectEvent(pluginProject=pluginProject)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendSelectedOglObjectsEvent(self, **kwargs):

        callback: SelectedOglObjectsCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: SelectedOglObjectsEvent = SelectedOglObjectsEvent(callback=callback)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendFrameSizeEvent(self, **kwargs):

        callback: SelectedOglObjectsCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: FrameSizeEvent = FrameSizeEvent(callback=callback)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendFrameInformationEvent(self, **kwargs):
        callback: SelectedOglObjectsCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: FrameInformationEvent = FrameInformationEvent(callback=callback)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendAddShapeEvent(self, **kwargs):
        shapeToAdd = kwargs[SHAPE_PARAMETER]
        eventToPost: AddShapeEvent = AddShapeEvent(shapeToAdd=shapeToAdd)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendRequestCurrentProjectEvent(self, **kwargs):
        callback: CurrentProjectCallback = kwargs[CALLBACK_PARAMETER]
        eventToPost: RequestCurrentProjectEvent = RequestCurrentProjectEvent(callback=callback)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendLoadOglProjectEvent(self, **kwargs):
        oglProject:  OglProject          = kwargs[OGL_PROJECT_PARAMETER]
        eventToPost: LoadOglProjectEvent = LoadOglProjectEvent(oglProject=oglProject)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendGetObjectBoundariesEvent(self, **kwargs):

        callback:    ObjectBoundaryCallback   = kwargs[CALLBACK_PARAMETER]
        eventToPost: GetObjectBoundariesEvent = GetObjectBoundariesEvent(callback=callback)
        PostEvent(dest=self._listeningWindow, event=eventToPost)

    def _sendDeleteLinkEvent(self, **kwargs):

        oglLink: OglLink         = kwargs[OGL_LINK_PARAMETER]
        event:   DeleteLinkEvent = DeleteLinkEvent(oglLink=oglLink)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendCreateLinkEvent(self, **kwargs):
        linkInformation: LinkInformation     = kwargs[LINK_INFORMATION_PARAMETER]
        callback:        CreatedLinkCallback = kwargs[CALLBACK_PARAMETER]

        event: CreateLinkEvent = CreateLinkEvent(linkInformation=linkInformation, callback=callback)
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendSelectShapesAllEvent(self):
        event: SelectAllShapesEvent = SelectAllShapesEvent()
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendDeSelectAllShapesEvent(self):
        event: DeSelectAllShapesEvent = DeSelectAllShapesEvent()
        PostEvent(dest=self._listeningWindow, event=event)

    def _sendRefreshFrameEvent(self):
        event: RefreshFrameEvent = RefreshFrameEvent()
        PostEvent(dest=self._listeningWindow, event=event)
