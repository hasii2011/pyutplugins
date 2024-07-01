
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from miniogl.models.ShapeModel import ShapeModel

from miniogl.AnchorPoint import AnchorPoint
from miniogl.ControlPoint import ControlPoint
from miniogl.LineShape import ControlPoints

from ogl.OglAssociation import OglAssociation
from ogl.OglClass import OglClass
from ogl.OglInterface import OglInterface
from ogl.OglLink import OglLink
from ogl.OglLinkFactory import getOglLinkFactory
from ogl.OglPosition import OglPosition
from ogl.OglPosition import OglPositions

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import LinkInformation
from tests.scaffoldv2.eventengine.Events import CreateLinkEvent
from tests.scaffoldv2.eventengine.Events import DeleteLinkEvent
from tests.scaffoldv2.eventengine.Events import EVENT_CREATE_LINK
from tests.scaffoldv2.eventengine.Events import EVENT_DELETE_LINK
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine


class FrameHandler:
    def __init__(self, eventEngine: IEventEngine):

        self.logger: Logger = getLogger(__name__)

        self._eventEngine: IEventEngine = eventEngine

        self._eventEngine.registerListener(EVENT_DELETE_LINK, self._onDeleteLink)
        self._eventEngine.registerListener(EVENT_CREATE_LINK, self._onCreateLink)

    def _onDeleteLink(self, event: DeleteLinkEvent):

        oglLink: OglLink = event.oglLink

        if isinstance(oglLink, OglAssociation):
            oglAssociation: OglAssociation = cast(OglAssociation, oglLink)
            oglAssociation.centerLabel.Detach()
            oglAssociation.sourceCardinality.Detach()
            oglAssociation.destinationCardinality.Detach()

        oglLink.Detach()

    def _onCreateLink(self, event: CreateLinkEvent):

        linkInformation: LinkInformation     = event.linkInformation
        callback:        CreatedLinkCallback = event.callback

        self.logger.info(f'In Frame Handler')

        oglLink: OglLink = self._createOrthogonalLink(linkInformation=linkInformation)

        callback(oglLink)

    def _createOrthogonalLink(self, linkInformation: LinkInformation):

        linkType: PyutLinkType = linkInformation.linkType
        srcClass: OglClass     = cast(OglClass, linkInformation.sourceShape)
        dstClass: OglClass     = cast(OglClass, linkInformation.destinationShape)

        if linkType == PyutLinkType.INHERITANCE or linkType == PyutLinkType.NOTELINK:
            oglLink: OglLink = self._createGeneralLink(srcClass, dstClass, path=linkInformation.path, linkType=linkType)
        elif linkType == PyutLinkType.INTERFACE:
            oglLink = self._createGeneralLink(srcClass, dstClass, path=linkInformation.path, linkType=linkType)

            oglInterface: OglInterface = cast(OglInterface, oglLink)

            oglInterface.pyutObject.name = linkInformation.interfaceName
            oglInterface.updateLabels()

        elif linkType == PyutLinkType.AGGREGATION or linkType == PyutLinkType.ASSOCIATION or linkType == PyutLinkType.COMPOSITION:
            oglLink = self._createAssociationLink(linkInformation=linkInformation)
        else:
            assert False, 'Do not know about that link type'

        return oglLink

    def _createGeneralLink(self, child: OglClass, parent: OglClass, path: OglPositions, linkType: PyutLinkType) -> OglLink:
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
        oglLink:          OglLink   = getOglLinkFactory().getOglLink(child, pyutLink, parent, linkType)

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

    def _createAssociationLink(self, linkInformation: LinkInformation) -> OglLink:

        srcClass: OglClass = cast(OglClass, linkInformation.sourceShape)
        dstClass: OglClass = cast(OglClass, linkInformation.destinationShape)

        linkType: PyutLinkType = linkInformation.linkType

        pyutLink: PyutLink = PyutLink(name="", linkType=linkType, source=srcClass.pyutObject, destination=dstClass.pyutObject)

        pyutLink.name                   = linkInformation.associationName
        pyutLink.sourceCardinality      = linkInformation.sourceCardinality
        pyutLink.destinationCardinality = linkInformation.destinationCardinality
        # Call the factory to create OGL Link

        oglLinkFactory = getOglLinkFactory()
        oglLink: OglLink = oglLinkFactory.getOglLink(srcShape=srcClass, pyutLink=pyutLink, destShape=dstClass, linkType=linkType)

        self._placeAnchorsInCorrectPosition(oglLink=oglLink, path=linkInformation.path)

        controlPoints: ControlPoints = self._toControlPoints(path=linkInformation.path)

        self._createNeededControlPoints(oglLink=oglLink, controlPoints=controlPoints)

        srcClass.addLink(oglLink)  # add it to the source Ogl Linkable Object
        dstClass.addLink(oglLink)  # add it to the destination Ogl Linkable Object
        srcClass.pyutObject.addLink(pyutLink)  # add it to the source PyutClass

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

        srcModel: ShapeModel = srcAnchor.model
        dstModel: ShapeModel = dstAnchor.model

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
