
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
from pyutplugins.ExternalTypes import IntegerList
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import Points
from pyutplugins.ExternalTypes import Rectangle
from pyutplugins.ExternalTypes import Rectangles
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback

from tests.scaffold.PyutDiagramType import PyutDiagramType
from tests.scaffold.eventengine.Events import AddShapeEvent
from tests.scaffold.eventengine.Events import CreateLinkEvent
from tests.scaffold.eventengine.Events import DeSelectAllShapesEvent
from tests.scaffold.eventengine.Events import DeleteLinkEvent
from tests.scaffold.eventengine.Events import ShowOrthogonalRoutingPointsEvent

from tests.scaffold.eventengine.Events import EventType
from tests.scaffold.eventengine.Events import FrameInformationEvent
from tests.scaffold.eventengine.Events import FrameSizeEvent
from tests.scaffold.eventengine.Events import GetObjectBoundariesEvent
from tests.scaffold.eventengine.Events import LoadOglProjectEvent
from tests.scaffold.eventengine.Events import LoadProjectEvent
from tests.scaffold.eventengine.Events import NewDiagramEvent
from tests.scaffold.eventengine.Events import NewProjectEvent
from tests.scaffold.eventengine.Events import RefreshFrameEvent
from tests.scaffold.eventengine.Events import RequestCurrentProjectEvent
from tests.scaffold.eventengine.Events import SelectAllShapesEvent
from tests.scaffold.eventengine.Events import SelectedOglObjectsEvent
from tests.scaffold.eventengine.Events import ShowRouteGridEvent
from tests.scaffold.eventengine.Events import ShowRulersEvent
from tests.scaffold.eventengine.Events import UpdateTreeItemNameEvent

from tests.scaffold.eventengine.IEventEngine import IEventEngine

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
POINTS_PARAMETER:            str = 'points'
SHOW_PARAMETER:              str = 'show'
HORIZONTAL_RULERS_PARAMETER: str = 'horizontalRulers'
VERTICAL_RULERS_PARAMETER:   str = 'verticalRulers'
DIAGRAM_BOUNDS_PARAMETER:    str = 'diagramBounds'
ROUTE_GRID_PARAMETER:        str = 'routeGrid'


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
            case EventType.ShowOrthogonalRoutingPoints:
                self._sendShowOrthogonalRoutingPointsEvent(**kwargs)
            case EventType.ShowRouteGrid:
                self._sendShowRouteGridEvent(**kwargs)
            case EventType.ShowRulers:
                self._sendShowRulersEvent(**kwargs)
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

    def _sendShowOrthogonalRoutingPointsEvent(self, **kwargs):

        points: Points = kwargs[POINTS_PARAMETER]
        show:   bool   = kwargs[SHOW_PARAMETER]

        event:  ShowOrthogonalRoutingPointsEvent = ShowOrthogonalRoutingPointsEvent(points=points, show=show)

        PostEvent(dest=self._listeningWindow, event=event)

    def _sendShowRulersEvent(self, **kwargs):

        horizontalRulers: IntegerList = kwargs[HORIZONTAL_RULERS_PARAMETER]
        verticalRulers:   IntegerList = kwargs[VERTICAL_RULERS_PARAMETER]
        diagramBounds:    Rectangle   = kwargs[DIAGRAM_BOUNDS_PARAMETER]
        show:             bool        = kwargs[SHOW_PARAMETER]

        event:  ShowRulersEvent = ShowRulersEvent(horizontalRulers=horizontalRulers,
                                                  verticalRulers=verticalRulers,
                                                  diagramBounds=diagramBounds,
                                                  show=show)

        PostEvent(dest=self._listeningWindow, event=event)

    def _sendShowRouteGridEvent(self, **kwargs):

        routeGrid: Rectangles = kwargs[ROUTE_GRID_PARAMETER]
        show:      bool       = kwargs[SHOW_PARAMETER]

        event: ShowRouteGridEvent = ShowRouteGridEvent(routeGrid=routeGrid, show=show)

        PostEvent(dest=self._listeningWindow, event=event)
