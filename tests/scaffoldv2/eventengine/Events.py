
from enum import Enum

from wx import CommandEvent
from wx import PyEventBinder

from wx.lib.newevent import NewEvent

#
# Constructor return Tuple; First is the event,  The second is the binder
#
NewProjectEvent,         EVENT_NEW_PROJECT           = NewEvent()
LoadProjectEvent,        EVENT_LOAD_PROJECT          = NewEvent()
UpdateTreeItemNameEvent, EVENT_UPDATE_TREE_ITEM_NAME = NewEvent()
SelectAllEvent,          EVENT_SELECT_ALL            = NewEvent()


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
    SelectAll          = ('SelectAll',          SelectAllEvent(),          EVENT_SELECT_ALL)
