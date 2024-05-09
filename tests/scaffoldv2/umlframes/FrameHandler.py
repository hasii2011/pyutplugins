
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.LineShape import ControlPoints
from miniogl.ShapeModel import ShapeModel

from ogl.OglAssociation import OglAssociation
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglLinkFactory import getOglLinkFactory
from ogl.OglObject import OglObject
from ogl.OglPosition import OglPosition
from ogl.OglPosition import OglPositions

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from pyutplugins.ExternalTypes import CreatedLinkCallback
from tests.scaffoldv2.eventengine.Events import CreateLinkEvent
from tests.scaffoldv2.eventengine.Events import DeleteLinkEvent
from tests.scaffoldv2.eventengine.Events import EVENT_CREATE_LINK
from tests.scaffoldv2.eventengine.Events import EVENT_DELETE_LINK
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine


class FrameHandler:
    def __init__(self, eventEngine: IEventEngine):

        self.logger: Logger = getLogger(__name__)

        self._eventEngine: IEventEngine = eventEngine

        self._eventEngine.registerListener(EVENT_DELETE_LINK, self._deleteLink)
        self._eventEngine.registerListener(EVENT_CREATE_LINK, self._createLink)

    def _deleteLink(self, event: DeleteLinkEvent):

        oglLink: OglLink = event.oglLink

        if isinstance(oglLink, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, oglLink)
            oglAssociation.centerLabel.Detach()
            oglAssociation.sourceCardinality.Detach()
            oglAssociation.destinationCardinality.Detach()

        oglLink.Detach()

    def _createLink(self, event: CreateLinkEvent):

        linkType:         PyutLinkType        = event.linkType
        path:             OglPositions        = event.path
        sourceShape:      OglObject           = event.sourceShape
        destinationShape: OglObject           = event.destinationShape
        callback:         CreatedLinkCallback = event.callback

        self.logger.info(f'In Frame Handler')

        oglLink: OglLink = self._createOrthogonalLink(linkType=linkType, path=path, sourceShape=sourceShape, destinationShape=destinationShape)

        callback(oglLink)

    def _createOrthogonalLink(self, linkType: PyutLinkType, path: OglPositions, sourceShape: OglObject, destinationShape: OglObject):

        if linkType == PyutLinkType.INHERITANCE:
            srcClass: OglClass = cast(OglClass, sourceShape)
            dstClass: OglClass = cast(OglClass, destinationShape)

            oglLink: OglLink = self._createInheritanceLink(srcClass, dstClass, path=path)
        else:
            assert False, 'Do nt know about that link type'

        return oglLink

    def _createInheritanceLink(self, child: OglClass, parent: OglClass, path: OglPositions) -> OglLink:
        """
        Add a parent link between the child and parent objects.

        Args:
            child:  Child PyutClass
            parent: Parent PyutClass

        Returns:
            The inheritance OglLink
        """
        sourceClass:      PyutClass = cast(PyutClass, child.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, parent.pyutObject)
        pyutLink:         PyutLink  = PyutLink("", linkType=PyutLinkType.INHERITANCE, source=sourceClass, destination=destinationClass)
        oglLink:          OglLink   = getOglLinkFactory().getOglLink(child, pyutLink, parent, PyutLinkType.INHERITANCE)

        child.addLink(oglLink)
        parent.addLink(oglLink)

        self._placeAnchorsInCorrectPosition(oglLink=oglLink, path=path)

        controlPoints: ControlPoints = self._toControlPoints(path=path)
        self._createNeededControlPoints(oglLink=oglLink, controlPoints=controlPoints)
        # add it to the PyutClass
        childPyutClass:  PyutClass = cast(PyutClass, child.pyutObject)
        parentPyutClass: PyutClass = cast(PyutClass, parent.pyutObject)

        childPyutClass.addParent(parentPyutClass)

        return oglLink

    def _placeAnchorsInCorrectPosition(self, oglLink: OglLink, path: OglPositions):

        srcAnchor: AnchorPoint = oglLink.sourceAnchor
        dstAnchor: AnchorPoint = oglLink.destinationAnchor

        startPoint: OglPosition = path[0]
        endPoint:   OglPosition = path[-1]

        srcX: int = startPoint.x
        srcY: int = startPoint.y
        dstX: int = endPoint.x
        dstY: int = endPoint.y

        srcAnchor.SetPosition(x=srcX, y=srcY)
        dstAnchor.SetPosition(x=dstX, y=dstY)

        srcModel: ShapeModel = srcAnchor.GetModel()
        dstModel: ShapeModel = dstAnchor.GetModel()

        srcModel.SetPosition(x=srcX, y=srcY)
        dstModel.SetPosition(x=dstY, y=dstY)

    def _toControlPoints(self, path: OglPositions) -> ControlPoints:

        pathCopy: OglPositions = deepcopy(path)
        pathCopy.pop(0)     # remove start
        pathCopy = OglPositions(pathCopy[:-1])

        controlPoints: ControlPoints = ControlPoints([])
        for pt in pathCopy:
            point: OglPosition = cast(OglPosition, pt)
            controlPoint: ControlPoint = ControlPoint(x=point.x, y=point.y)

            controlPoints.append(controlPoint)

        return controlPoints

    def _createNeededControlPoints(self, oglLink: OglLink, controlPoints: ControlPoints):

        for controlPoint in controlPoints:
            oglLink.AddControl(control=controlPoint, after=None)
