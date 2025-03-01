
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Frame

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import IntegerList
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.ExternalTypes import Points
from pyutplugins.ExternalTypes import Rectangle
from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.IPluginAdapter import ScreenMetrics

from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import OglObjectType
from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback

from tests.scaffold.eventengine.EventEngine import EventEngine


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

    def getObjectBoundaries(self, callback: ObjectBoundaryCallback):
        pass

    def deleteLink(self, oglLink: OglLink):
        pass

    def createLink(self, linkInformation: LinkInformation, callback: CreatedLinkCallback):
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

    def showOrthogonalRoutingPoints(self, show: bool, spots: Points):
        pass

    def showRulers(self, show: bool, horizontalRulers: IntegerList, verticalRulers: IntegerList, diagramBounds: Rectangle):
        pass
