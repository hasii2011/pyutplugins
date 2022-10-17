
from logging import Logger
from logging import getLogger
from typing import Union
from typing import cast

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics

from core.types.Types import OglObjects
from core.types.Types import PluginProject

from tests.scaffoldv2.eventengine.Events import EventType
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine


class MediatorV2(IMediator):
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
    def umlFrame(self) -> DiagramFrame:
        return cast(DiagramFrame, None)

    @umlFrame.setter
    def umlFrame(self, newValue: DiagramFrame):
        pass

    @property
    def selectedOglObjects(self) -> OglObjects:
        return cast(OglObjects, None)

    def refreshFrame(self):
        pass

    def selectAllOglObjects(self):
        pass

    def deselectAllOglObjects(self):
        pass

    def addShape(self, shape: Union[OglObject, OglLink]):
        pass

    def loadProject(self, pluginProject: PluginProject):
        """
        In the plugin scaffold test program we support only single document projects

        Args:
            pluginProject:
        """
        self._eventEngine.sendEvent(eventType=EventType.LoadProjectEvent, pluginProject=pluginProject)
