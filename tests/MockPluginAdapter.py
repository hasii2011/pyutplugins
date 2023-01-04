
from typing import cast

from unittest.mock import MagicMock

from miniogl.DiagramFrame import DiagramFrame

from plugins.CoreTypes import CurrentProjectCallback
from plugins.CoreTypes import FrameInformationCallback
from plugins.CoreTypes import FrameSizeCallback
from plugins.CoreTypes import OglObjectType
from plugins.CoreTypes import PluginProject
from plugins.CoreTypes import SelectedOglObjectsCallback

from plugins.core.IPluginAdapter import IPluginAdapter
from plugins.core.IPluginAdapter import ScreenMetrics

from tests.scaffoldv2.eventengine.EventEngine import EventEngine


class MockPluginAdapter(IPluginAdapter):
    """
    A simple mostly do nothing pluginAdapter for unit tests
    """

    # noinspection PyUnusedLocal
    def __init__(self):
        """
        """
        # ignore whatever comes in
        mockFrame: MagicMock = MagicMock(spec=DiagramFrame)

        super().__init__()

        self._pyutVersion = 'Mock Mediator 1.0'

    @property
    def pyutVersion(self) -> str:
        return self._pyutVersion

    @pyutVersion.setter
    def pyutVersion(self, newVersion: str):
        pass

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    @property
    def currentDirectory(self) -> str:
        return ''

    @currentDirectory.setter
    def currentDirectory(self, theNewValue: str):
        pass

    def getFrameSize(self, callback: FrameSizeCallback):
        pass

    def getFrameInformation(self, callback: FrameInformationCallback):
        pass

    @property
    def eventEngine(self) -> EventEngine:
        return cast(EventEngine, None)

    @eventEngine.setter
    def eventEngine(self, eventEngine: EventEngine):
        pass

    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        pass

    def refreshFrame(self):
        pass

    def selectAllOglObjects(self):
        pass

    def deselectAllOglObjects(self):
        pass

    def addShape(self, shape: OglObjectType):
        pass

    def loadProject(self, pluginProject: PluginProject):
        pass

    def requestCurrentProject(self, callback: CurrentProjectCallback):
        pass

    def indicatePluginModifiedProject(self):
        pass
