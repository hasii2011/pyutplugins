
from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from ogl.OglPosition import OglPositions

from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.IPluginAdapter import ScreenMetrics

from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback
from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import OglObjectType

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
        return 'ScaffoldV2'

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    @property
    def currentDirectory(self) -> str:
        """
        Returns:  The current directory
        """
        return '/Users/humberto.a.sanchez.ii/pyut-diagrams'

    def getFrameSize(self, callback: FrameSizeCallback):
        self._eventEngine.sendEvent(EventType.FrameSize, callback=callback)

    def getFrameInformation(self, callback: FrameInformationCallback):
        self._eventEngine.sendEvent(EventType.FrameInformation, callback=callback)

    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        self._eventEngine.sendEvent(EventType.SelectedOglObjects, callback=callback)

    def getObjectBoundaries(self, callback: ObjectBoundaryCallback):
        """
        Request the boundaries around all the UML objects
        on the current frame

        Args:
            callback:  The callback that receives the boundaries
        """
        self._eventEngine.sendEvent(EventType.GetObjectBoundaries, callback=callback)

    def refreshFrame(self):
        self._eventEngine.sendEvent(EventType.RefreshFrame)

    def selectAllOglObjects(self):
        self._eventEngine.sendEvent(EventType.SelectAllShapes)
        wxYield()

    def deselectAllOglObjects(self):
        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)
        wxYield()

    def addShape(self, shape: OglObjectType):
        self._eventEngine.sendEvent(EventType.AddShape, shapeToAdd=shape)

    def loadProject(self, pluginProject: PluginProject):
        """
        In the plugin scaffold test program, we support only single document projects

        Args:
            pluginProject:
        """
        self._eventEngine.sendEvent(eventType=EventType.LoadProjectEvent, pluginProject=pluginProject)

    def requestCurrentProject(self, callback: CurrentProjectCallback):
        """
        Request the current project.   The adapter or its surrogate
        has to convert from a PyutProject to a PluginProject type
        """
        self._eventEngine.sendEvent(eventType=EventType.RequestCurrentProject, callback=callback)

    def indicatePluginModifiedProject(self):
        self._eventEngine.sendEvent(EventType.IndicatePluginModifiedProject)

    def deleteLink(self, oglLink: OglLink):
        self._eventEngine.sendEvent(EventType.DeleteLink, oglLink=oglLink)

    def createLink(self, linkType: PyutLinkType, path: OglPositions, sourceShape: OglObject, destinationShape: OglObject, callback: CreatedLinkCallback):
        self._eventEngine.sendEvent(EventType.CreateLink, linkType=linkType, path=path,
                                    sourceShape=sourceShape, destinationShape=destinationShape,
                                    callback=callback)
