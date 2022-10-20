
from enum import Enum

from wx import CommandEvent
from wx import PyEventBinder

from wx.lib.newevent import NewEvent

#
# The constructor returns a Tuple; First is the event,  The second is the binder
#
NewProjectEvent,         EVENT_NEW_PROJECT           = NewEvent()
LoadProjectEvent,        EVENT_LOAD_PROJECT          = NewEvent()
UpdateTreeItemNameEvent, EVENT_UPDATE_TREE_ITEM_NAME = NewEvent()
SelectAllShapesEvent,    EVENT_SELECT_ALL_SHAPES     = NewEvent()
DeSelectAllShapesEvent, EVENT_DESELECT_ALL_SHAPES    = NewEvent()

SelectedOglObjectsEvent, EVENT_SELECTED_OGL_OBJECTS  = NewEvent()
RefreshFrameEvent,       EVENT_REFRESH_FRAME         = NewEvent()
FrameSizeEvent,          EVENT_FRAME_SIZE            = NewEvent()
FrameInformationEvent,   EVENT_FRAME_INFORMATION     = NewEvent()


class EventType(str, Enum):
    """
    These should match the actual event definitions in Events
    """
    commandEvent:  CommandEvent
    pyEventBinder: PyEventBinder

    def __new__(cls, title: str, commandEvent: CommandEvent, binder: PyEventBinder) -> 'EventType':
        obj = str.__new__(cls, title)
        obj._value_ = title

        obj.commandEvent  = commandEvent
        obj.pyEventBinder = binder
        return obj

    NewProject         = ('NewProject',         NewProjectEvent(),         EVENT_NEW_PROJECT)
    LoadProjectEvent   = ('LoadProjectEvent',   LoadProjectEvent(),        EVENT_NEW_PROJECT)
    UpdateTreeItemName = ('UpdateTreeItemName', UpdateTreeItemNameEvent(), EVENT_UPDATE_TREE_ITEM_NAME)
    SelectAllShapes    = ('SelectAllShapes',    SelectAllShapesEvent(),    EVENT_SELECT_ALL_SHAPES)
    DeSelectAllShapes  = ('DeSelectAllShapes',  DeSelectAllShapesEvent(),  EVENT_DESELECT_ALL_SHAPES)
    SelectedOglObjects = ('SelectedOglObjects', SelectedOglObjectsEvent(), EVENT_SELECTED_OGL_OBJECTS)
    RefreshFrame       = ('RefreshFrame',       RefreshFrameEvent(),       EVENT_REFRESH_FRAME)
    FrameSize          = ('FrameSize',          FrameSizeEvent(),          EVENT_FRAME_SIZE)
    FrameInformation   = ('FrameInformation',   FrameInformationEvent(),   EVENT_FRAME_INFORMATION)
