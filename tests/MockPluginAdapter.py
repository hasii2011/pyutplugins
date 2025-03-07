
from typing import cast

from unittest.mock import MagicMock

from miniogl.DiagramFrame import DiagramFrame

from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import IntegerList
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.ExternalTypes import OglObjectType
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import Points
from pyutplugins.ExternalTypes import Rectangle
from pyutplugins.ExternalTypes import Rectangles
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.IPluginAdapter import ScreenMetrics

from tests.scaffold.eventengine.EventEngine import EventEngine


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

    def getObjectBoundaries(self, callback: ObjectBoundaryCallback):
        pass

    def deleteLink(self, oglLink: OglLink):
        pass

    def createLink(self, linkInformation: LinkInformation, callback: CreatedLinkCallback):
        pass

    def indicatePluginModifiedProject(self):
        pass

    def showOrthogonalRoutingPoints(self, show: bool, spots: Points):
        pass

    def showRulers(self, show: bool, horizontalRulers: IntegerList, verticalRulers: IntegerList, diagramBounds: Rectangle):
        pass

    def showRouteGrid(self, show: bool, routeGrid: Rectangles):
        pass
