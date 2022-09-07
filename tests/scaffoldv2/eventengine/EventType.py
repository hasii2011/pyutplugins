

from enum import Enum


class EventType(Enum):
    """
    These should match the actual event definitions in Events
    """

    NewProject         = 'NewProject'
    AddProjectEvent    = 'AddProjectEvent'
    UpdateTreeItemName = 'UpdateTreeItemName'
