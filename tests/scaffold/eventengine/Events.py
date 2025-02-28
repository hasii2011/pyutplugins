
from enum import Enum

from wx.lib.newevent import NewEvent

#
# The constructor returns a Tuple; The first is the event,  The second is the binder
#
NewProjectEvent,         EVENT_NEW_PROJECT           = NewEvent()
NewDiagramEvent,         EVENT_NEW_DIAGRAM           = NewEvent()
LoadProjectEvent,        EVENT_LOAD_PROJECT          = NewEvent()
UpdateTreeItemNameEvent, EVENT_UPDATE_TREE_ITEM_NAME = NewEvent()
SelectAllShapesEvent,    EVENT_SELECT_ALL_SHAPES     = NewEvent()
DeSelectAllShapesEvent,  EVENT_DESELECT_ALL_SHAPES   = NewEvent()
AddShapeEvent,           EVENT_ADD_SHAPE             = NewEvent()

SelectedOglObjectsEvent, EVENT_SELECTED_OGL_OBJECTS  = NewEvent()
RefreshFrameEvent,       EVENT_REFRESH_FRAME         = NewEvent()
FrameSizeEvent,          EVENT_FRAME_SIZE            = NewEvent()
FrameInformationEvent,   EVENT_FRAME_INFORMATION     = NewEvent()
LoadOglProjectEvent,     EVENT_LOAD_OGL_PROJECT      = NewEvent()

GetObjectBoundariesEvent, EVENT_GET_OBJECT_BOUNDARIES = NewEvent()
DeleteLinkEvent,          EVENT_DELETE_LINK           = NewEvent()
CreateLinkEvent,          EVENT_CREATE_LINK           = NewEvent()

RequestCurrentProjectEvent,         EVENT_REQUEST_CURRENT_PROJECT          = NewEvent()
IndicatePluginModifiedProjectEvent, EVENT_INDICATE_PLUGIN_MODIFIED_PROJECT = NewEvent()

DrawOrthogonalRoutingPointsEvent, EVENT_DRAW_ORTHOGONAL_ROUTING_POINTS = NewEvent()


class EventType(Enum):

    NewProject         = 'NewProject'
    NewDiagram         = 'NewDiagram'
    LoadProjectEvent   = 'LoadProjectEvent'
    UpdateTreeItemName = 'UpdateTreeItemName'
    SelectAllShapes    = 'SelectAllShapes'
    DeSelectAllShapes  = 'DeSelectAllShapes'
    AddShape           = 'AddShape'
    SelectedOglObjects = 'SelectedOglObjects'
    RefreshFrame       = 'RefreshFrame'
    FrameSize          = 'FrameSize'
    FrameInformation   = 'FrameInformation'
    LoadOglProject     = 'LoadOglProject'
    DeleteLink         = 'DeleteLink'
    CreateLink         = 'CreateLink'

    GetObjectBoundaries = 'GetObjectBoundaries'

    RequestCurrentProject         = 'RequestCurrentProject'
    IndicatePluginModifiedProject = 'IndicatePluginModifiedProject'

    DrawOrthogonalRoutingPointsEvent = 'DrawOrthogonalRoutingPointsEvent'
