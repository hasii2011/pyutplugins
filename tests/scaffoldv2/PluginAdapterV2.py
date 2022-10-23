
from typing import Union

from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.IPluginAdapter import IPluginAdapter
from core.IPluginAdapter import ScreenMetrics
from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSizeCallback

from core.types.Types import PluginProject
from core.types.Types import SelectedOglObjectsCallback

from tests.scaffoldv2.eventengine.Events import EventType
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine


class PluginAdapterV2(IPluginAdapter):
    """

    """

    def __init__(self, eventEngine: IEventEngine):

        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._eventEngine: IEventEngine = eventEngine

    @property
    def pyutVersion(self) -> str:
        return 'MediatorV2'

    @pyutVersion.setter
    def pyutVersion(self, newValue: str):
        self.logger.warning(f'Unused {newValue}')

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    @property
    def currentDirectory(self) -> str:
        """
        Returns:  The current directory
        """
        return ''

    @currentDirectory.setter
    def currentDirectory(self, theNewValue: str):
        """
        TODO:  Should plugins be allowed to manipulate the application's current directory
        Args:
            theNewValue:
        """
        pass

    def getFrameSize(self, callback: FrameSizeCallback):
        self._eventEngine.sendEvent(EventType.FrameSize, callback=callback)

    def getFrameInformation(self, callback: FrameInformationCallback):
        self._eventEngine.sendEvent(EventType.FrameInformation, callback=callback)

    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        self._eventEngine.sendEvent(EventType.SelectedOglObjects, callback=callback)

    def refreshFrame(self):
        self._eventEngine.sendEvent(EventType.RefreshFrame)

    def selectAllOglObjects(self):
        self._eventEngine.sendEvent(EventType.SelectAllShapes)
        wxYield()

    def deselectAllOglObjects(self):
        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)
        wxYield()

    def addShape(self, shape: Union[OglObject, OglLink]):
        pass

    def loadProject(self, pluginProject: PluginProject):
        """
        In the plugin scaffold test program we support only single document projects

        Args:
            pluginProject:
        """
        self._eventEngine.sendEvent(eventType=EventType.LoadProjectEvent, pluginProject=pluginProject)