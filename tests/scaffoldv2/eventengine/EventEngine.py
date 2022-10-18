
from logging import Logger
from logging import getLogger
from typing import Callable

from wx import PostEvent
from wx import PyEventBinder
from wx import TreeItemId
from wx import Window

from core.types.Types import PluginProject
from core.types.Types import SelectedOglObjectsCallback

from tests.scaffoldv2.eventengine.Events import EventType
from tests.scaffoldv2.eventengine.Events import FrameSizeEvent
from tests.scaffoldv2.eventengine.Events import LoadProjectEvent
from tests.scaffoldv2.eventengine.Events import NewProjectEvent
from tests.scaffoldv2.eventengine.Events import SelectedOglObjectsEvent
from tests.scaffoldv2.eventengine.Events import UpdateTreeItemNameEvent

from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine

NEW_NAME_PARAMETER:       str = 'newName'
TREE_ITEM_ID_PARAMETER:   str = 'treeItemId'
PLUGIN_PROJECT_PARAMETER: str = 'pluginProject'
CALLBACK_PARAMETER:       str = 'callback'


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
            case EventType.SelectAll:
                self._simpleSendEvent(eventType=eventType)
            case EventType.RefreshFrame:
                self._simpleSendEvent(eventType=eventType)
            case EventType.SelectedOglObjects:
                self._sendSelectedOglObjectsEvent(**kwargs)
            case EventType.FrameSize:
                self._sendFrameSizeEvent(**kwargs)
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

    def _simpleSendEvent(self, eventType: EventType):
        eventToPost = eventType.commandEvent
        PostEvent(dest=self._listeningWindow, event=eventToPost)
