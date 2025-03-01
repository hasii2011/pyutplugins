
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from codeallybasic.Position import Position

from miniogl.AnchorPoint import AnchorPoint

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from ogl.OglPosition import OglPosition
from ogl.OglPosition import OglPositions

from pyorthogonalrouting.OrthogonalConnectorByProduct import OrthogonalConnectorByProduct

from pyorthogonalrouting.Common import Integers

from pyorthogonalrouting.Point import Point
from pyorthogonalrouting.Point import Points
from pyorthogonalrouting.Rectangle import Rectangle
from pyorthogonalrouting.Rect import Rect
from pyorthogonalrouting.Configuration import Configuration
from pyorthogonalrouting.ConnectorPoint import ConnectorPoint
from pyorthogonalrouting.OrthogonalConnector import OrthogonalConnector
from pyorthogonalrouting.OrthogonalConnectorOptions import OrthogonalConnectorOptions

from pyorthogonalrouting.enumerations.Side import Side

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from pyutplugins.ExternalTypes import AssociationName
from pyutplugins.ExternalTypes import DestinationCardinality
from pyutplugins.ExternalTypes import DiagnosticInformation
from pyutplugins.ExternalTypes import InterfaceName
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import SourceCardinality

from pyutplugins.IPluginAdapter import IPluginAdapter

ANCHOR_POINT_ADJUSTMENT: int = 1    # because line end needs to look like it is right on the line


class OrthogonalConnectorAdapter:
    """
    TODO:  This adapter leaks some of the OrthogonalConnector data types.  Fix this before
    merging to the master branch
    Create a single property call diagnosticInformation

    """
    def __init__(self, pluginAdapter: IPluginAdapter):

        self.logger: Logger = getLogger(__name__)

        self._pluginAdapter: IPluginAdapter = pluginAdapter
        self._configuration: Configuration  = Configuration()

        self._byProducts:   OrthogonalConnectorByProduct = cast(OrthogonalConnectorByProduct, None)

    @property
    def diagnosticInformation(self) -> DiagnosticInformation:
        return self._getDiagnosticInformation()

    # noinspection PyTypeChecker
    @classmethod
    def whichConnectorSide(cls, shape: OglObject, anchorPosition: Position) -> Side:

        shapeX, shapeY           = shape.GetPosition()
        shapeWidth, shapeHeight  = shape.GetSize()

        minX: int = shapeX
        maxX: int = shapeX + shapeWidth - ANCHOR_POINT_ADJUSTMENT
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

    def runConnector(self, oglLink: OglLink) -> bool:
        """

        Args:
            oglLink:

        Returns:  `True` the algorithm found a route, else `False`
        """

        sourceSide, destinationSide = self._determineAttachmentSide(oglLink=oglLink)

        sourceRect:      Rect = self._shapeToRect(oglLink.sourceShape)
        destinationRect: Rect = self._shapeToRect(oglLink.destinationShape)

        sourceConnectorPoint:      ConnectorPoint = ConnectorPoint(shape=sourceRect,      side=sourceSide,      distance=self._configuration.sourceEdgeDistance)
        destinationConnectorPoint: ConnectorPoint = ConnectorPoint(shape=destinationRect, side=destinationSide, distance=self._configuration.destinationEdgeDistance)

        options: OrthogonalConnectorOptions = OrthogonalConnectorOptions()
        options.pointA = sourceConnectorPoint
        options.pointB = destinationConnectorPoint

        options.shapeMargin        = self._configuration.shapeMargin
        options.globalBoundsMargin = self._configuration.globalBoundsMargin
        options.globalBounds       = self._configuration.globalBounds

        path: Points     = OrthogonalConnector.route(options=options)

        self._byProducts = OrthogonalConnector.byProduct

        self.logger.info(f'{path}')

        if len(path) == 0:
            return False
        else:
            self._deleteTheOldLink(oglLink=oglLink)
            self._createOrthogonalLink(oldLink=oglLink, path=path)
            return True

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

        self._pluginAdapter.deleteLink(oglLink=oglLink)

    def _createOrthogonalLink(self, oldLink: OglLink, path: Points):

        linkType:         PyutLinkType = oldLink.pyutObject.linkType
        sourceShape:      OglObject    = oldLink.sourceShape
        destinationShape: OglObject    = oldLink.destinationShape

        oglPositions: OglPositions = self._toOglPositions(path=path)

        linkInformation: LinkInformation = LinkInformation()
        linkInformation.linkType         = linkType
        linkInformation.path             = oglPositions
        linkInformation.sourceShape      = sourceShape
        linkInformation.destinationShape = destinationShape

        if linkType == PyutLinkType.INTERFACE:
            linkInformation.interfaceName = InterfaceName(oldLink.pyutObject.name)
        elif linkType == PyutLinkType.ASSOCIATION or linkType == PyutLinkType.COMPOSITION or linkType == PyutLinkType.AGGREGATION:
            linkInformation.associationName        = AssociationName(oldLink.pyutObject.name)
            linkInformation.sourceCardinality      = SourceCardinality(oldLink.pyutObject.sourceCardinality)
            linkInformation.destinationCardinality = DestinationCardinality(oldLink.pyutObject.destinationCardinality)

        self._pluginAdapter.createLink(linkInformation=linkInformation, callback=self._createLinkCallback)

    def _createLinkCallback(self, newLink: OglLink):

        self._pluginAdapter.addShape(newLink)
        self._pluginAdapter.refreshFrame()

    def _toOglPositions(self, path: Points) -> OglPositions:

        oglPositions: OglPositions = OglPositions([])

        for pt in path:
            point:       Point       = cast(Point, pt)
            oglPosition: OglPosition = OglPosition(x=point.x, y=point.y)

            oglPositions.append(oglPosition)

        return oglPositions

    def _getDiagnosticInformation(self) -> DiagnosticInformation:
        """
        Don't leak OrthogonalConnector data types

        Returns:  Information that can be used to display why connection failed
        """

        from pyorthogonalrouting.Point import Point
        from pyorthogonalrouting.Point import Points

        from pyutplugins.ExternalTypes import Point as DiagnosticPoint
        from pyutplugins.ExternalTypes import Points as DiagnosticPoints
        from pyutplugins.ExternalTypes import Rectangle as DiagnosticRectangle
        from pyutplugins.ExternalTypes import IntegerList

        def toDiagnosticPoints(refPoints:  Points) -> DiagnosticPoints:

            diagnosticPts: DiagnosticPoints = DiagnosticPoints([])

            for pt in refPoints:
                point: Point = cast(Point, pt)
                self.logger.info(f'{point=}')

                diagnosticPoint: DiagnosticPoint = DiagnosticPoint(x=point.x, y=point.y)
                diagnosticPts.append(diagnosticPoint)

            return diagnosticPts

        def toDiagnosticRectangle(rectangle: Rectangle) -> DiagnosticRectangle:

            return DiagnosticRectangle(
                left=rectangle.left,
                top=rectangle.top,
                width=rectangle.width,
                height=rectangle.height
            )

        def toIntegerList(integers: Integers) -> IntegerList:

            integerList: IntegerList = IntegerList([])
            for integer in integers:
                integerList.append(integer)

            return integerList

        referencePoints:  Points           = self._byProducts.spots
        diagnosticPoints: DiagnosticPoints = toDiagnosticPoints(refPoints=referencePoints)

        diagnosticInformation: DiagnosticInformation = DiagnosticInformation(
            spots=diagnosticPoints,
            horizontalRulers=toIntegerList(self._byProducts.hRulers),
            verticalRulers=toIntegerList(self._byProducts.vRulers),
            diagramBounds=toDiagnosticRectangle(self._byProducts.diagramBounds),
        )

        return diagnosticInformation
