
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Frame

from miniogl.DiagramFrame import DiagramFrame

from pyutplugins.coreinterfaces.IPluginAdapter import IPluginAdapter
from pyutplugins.coreinterfaces.IPluginAdapter import ScreenMetrics

from pyutplugins.CoreTypes import CurrentProjectCallback
from pyutplugins.CoreTypes import FrameInformationCallback
from pyutplugins.CoreTypes import FrameSizeCallback
from pyutplugins.CoreTypes import OglObjectType
from pyutplugins.CoreTypes import OglObjects
from pyutplugins.CoreTypes import PluginProject
from pyutplugins.CoreTypes import SelectedOglObjectsCallback

from tests.scaffoldv2.eventengine.EventEngine import EventEngine


class SampleIPluginAdapter(IPluginAdapter):

    def __init__(self):

        super().__init__()
        self.logger:            Logger = getLogger(__name__)
        self._currentDirectory: str    = ''
        self._pyutVersion:      str    = 'Sample Mediator'

    @property
    def currentDirectory(self) -> str:
        return self._currentDirectory

    @property
    def umlFrame(self) -> Frame:
        return cast(Frame, None)

    @umlFrame.setter
    def umlFrame(self, newValue: DiagramFrame):
        pass

    @property
    def pyutVersion(self) -> str:
        return self._pyutVersion

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    @property
    def eventEngine(self) -> EventEngine:
        return cast(EventEngine, None)

    @eventEngine.setter
    def eventEngine(self, eventEngine: EventEngine):
        pass

    @property
    def selectedOglObjects(self) -> OglObjects:
        return cast(OglObjects, None)

    def getFrameSize(self, callback: FrameSizeCallback):
        pass

    def getFrameInformation(self, callback: FrameInformationCallback):
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