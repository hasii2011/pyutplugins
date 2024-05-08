from copy import deepcopy
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.Position import Position

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.LineShape import ControlPoints
from miniogl.ShapeModel import ShapeModel

from ogl.OglAssociation import OglAssociation
from ogl.OglClass import OglClass
from ogl.OglLinkFactory import getOglLinkFactory
from ogl.OglObject import OglObject
from ogl.OglLink import OglLink

from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.Configuration import Configuration
from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnector import OrthogonalConnector
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions

from pyorthogonalrouting.enumerations.Side import Side

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from pyutplugins.IPluginAdapter import IPluginAdapter


class OrthogonalConnectorAdapter:
    def __init__(self, pluginAdapter: IPluginAdapter):

        self.logger: Logger = getLogger(__name__)

        self._pluginAdapter: IPluginAdapter = pluginAdapter
        self._configuration: Configuration  = Configuration()

    @classmethod
    def whichConnectorSide(cls, shape: OglObject, anchorPosition: Position) -> Side:

        shapeX, shapeY           = shape.GetPosition()
        shapeWidth, shapeHeight  = shape.GetSize()

        minX: int = shapeX
        maxX: int = shapeX + shapeWidth
        minY: int = shapeY

        if anchorPosition.x == minX and anchorPosition.y >= minY:
            side: Side = Side.LEFT
        elif anchorPosition.x == maxX and anchorPosition.y >= minY:
            side = Side.RIGHT
        elif anchorPosition.x > minX and anchorPosition.y == minY:
            side = Side.TOP
        elif anchorPosition.x > minX and anchorPosition.y >= minY:
            side = Side.BOTTOM
        else:
            assert False, 'My algorithm has failed.  boo, hoo hoo'

        return side

    def runConnector(self, oglLink: OglLink):

        sourceSide, destinationSide = self._determineAttachmentSide(oglLink=oglLink)

        sourceRect:      Rect = self._shapeToRect(oglLink.sourceShape)
        destinationRect: Rect = self._shapeToRect(oglLink.destinationShape)

        sourceConnectorPoint:      ConnectorPoint = ConnectorPoint(shape=sourceRect,      side=sourceSide,      distance=0.5)
        destinationConnectorPoint: ConnectorPoint = ConnectorPoint(shape=destinationRect, side=destinationSide, distance=0.5)

        options: OrthogonalConnectorOptions = OrthogonalConnectorOptions()
        options.pointA = sourceConnectorPoint
        options.pointB = destinationConnectorPoint

        options.shapeMargin        = self._configuration.shapeMargin
        options.globalBoundsMargin = self._configuration.globalBoundsMargin
        options.globalBounds       = self._configuration.globalBounds

        path: Points    = OrthogonalConnector.route(options=options)

        self.logger.info(f'{path}')

        linkType:         PyutLinkType = oglLink.pyutObject.linkType
        sourceShape:      OglObject    = oglLink.sourceShape
        destinationShape: OglObject    = oglLink.destinationShape

        self._deleteTheOldLink(oglLink=oglLink)
        newLink: OglLink = self._createOrthogonalLink(linkType=linkType, path=path, sourceShape=sourceShape, destinationShape=destinationShape)

        # umlFrame.Refresh()
        self._pluginAdapter.addShape(newLink)
        self._pluginAdapter.refreshFrame()

    def _shapeToRect(self, oglObject: OglObject) -> Rect:

        shapeX, shapeY           = oglObject.GetPosition()
        shapeWidth, shapeHeight  = oglObject.GetSize()

        rect: Rect = Rect()

        rect.left   = shapeX
        rect.top    = shapeY
        rect.width  = shapeWidth
        rect.height = shapeHeight

        return rect

    def _determineAttachmentSide(self, oglLink: OglLink) -> Tuple[Side, Side]:

        sourceShape      = oglLink.sourceShape
        destinationShape = oglLink.destinationShape

        sourceAnchorPoint:      AnchorPoint = oglLink.sourceAnchor
        destinationAnchorPoint: AnchorPoint = oglLink.destinationAnchor

        sourcePosition:      Tuple[int, int] = sourceAnchorPoint.GetPosition()
        destinationPosition: Tuple[int, int] = destinationAnchorPoint.GetPosition()
        self.logger.info(f'{sourcePosition=} {destinationPosition=}')

        sourceSide:      Side = OrthogonalConnectorAdapter.whichConnectorSide(shape=sourceShape,      anchorPosition=Position(x=sourcePosition[0], y=sourcePosition[1]))
        destinationSide: Side = OrthogonalConnectorAdapter.whichConnectorSide(shape=destinationShape, anchorPosition=Position(x=destinationPosition[0], y=destinationPosition[1]))

        self.logger.info(f'{sourceSide=} {destinationSide=}')

        return sourceSide, destinationSide

    def _deleteTheOldLink(self, oglLink: OglLink):

        if isinstance(oglLink, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, oglLink)
            oglAssociation.centerLabel.Detach()
            oglAssociation.sourceCardinality.Detach()
            oglAssociation.destinationCardinality.Detach()

        oglLink.Detach()

    def _createOrthogonalLink(self, linkType: PyutLinkType, path: Points, sourceShape: OglObject, destinationShape: OglObject):

        if linkType == PyutLinkType.INHERITANCE:
            srcClass: OglClass = cast(OglClass, sourceShape)
            dstClass: OglClass = cast(OglClass, destinationShape)

            oglLink: OglLink = self._createInheritanceLink(srcClass, dstClass, path=path)

        return oglLink

    def _createInheritanceLink(self, child: OglClass, parent: OglClass, path: Points) -> OglLink:
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

    def _placeAnchorsInCorrectPosition(self, oglLink: OglLink, path: Points):

        srcAnchor: AnchorPoint = oglLink.sourceAnchor
        dstAnchor: AnchorPoint = oglLink.destinationAnchor

        startPoint: Point = path[0]
        endPoint:   Point = path[-1]
        # srcX, srcY = self._srcPoint.Get()
        # dstX, dstY = self._dstPoint.Get()

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

    def _createNeededControlPoints(self, oglLink: OglLink, controlPoints: ControlPoints):

        for controlPoint in controlPoints:
            oglLink.AddControl(control=controlPoint, after=None)

    def _toControlPoints(self, path: Points) -> ControlPoints:

        pathCopy: Points = deepcopy(path)
        pathCopy.pop(0)     # remove start
        pathCopy = Points(pathCopy[:-1])

        controlPoints: ControlPoints = ControlPoints([])
        for pt in pathCopy:
            point: Point = cast(Point, pt)
            controlPoint: ControlPoint = ControlPoint(x=point.x, y=point.y)

            controlPoints.append(controlPoint)

        return controlPoints
