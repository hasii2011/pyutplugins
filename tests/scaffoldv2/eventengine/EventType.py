

from enum import Enum


class EventType(Enum):
    """
    These should match the actual event definitions in Events
    """

    NewProject         = 'NewProject'
    LoadProjectEvent   = 'LoadProjectEvent'
    UpdateTreeItemName = 'UpdateTreeItemName'
