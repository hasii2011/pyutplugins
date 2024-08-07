
from typing import List

from logging import Logger
from logging import getLogger

from unittest.mock import MagicMock
from unittest.mock import PropertyMock

from miniogl.AnchorPoint import AnchorPoint
from miniogl.LinePoint import LinePoint

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutLink import PyutLink

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype


class MockGenerator:
    NUMBER_OF_MOCK_CLASSES:    int = 2
    MOCK_CLASS_NAME_PREFIX:    str = 'ClassName_'

    MOCK_ID_NUMBER_INCREMENT:  int = 5
    MOCK_INIT_WIDTH:           float = 50.0
    MOCK_INIT_HEIGHT:          float = 50.0
    MOCK_INIT_POSITION_X:      float = 100.0
    MOCK_INIT_POSITION_Y:      float = 100.0
    MOCK_X_POSITION_INCREMENT: float = 75.0
    MOCK_Y_POSITION_INCREMENT: float = 100.0

    def __init__(self, mockClassNamePrefix: str = MOCK_CLASS_NAME_PREFIX):

        self.logger: Logger = getLogger(__name__)

        self._mockClassNamePrefix: str = mockClassNamePrefix

        self._classIdGenerator = self._generateClassId()
        self._linkIDGenerator  = self._generateLinkId()

    def generateMockNodes(self, nbrToGenerate) -> List[MagicMock]:

        umlObjects: List[MagicMock] = []

        mockX: float = MockGenerator.MOCK_INIT_POSITION_X
        mockY: float = MockGenerator.MOCK_INIT_POSITION_Y
        mockWidth:  float = MockGenerator.MOCK_INIT_WIDTH
        mockHeight: float = MockGenerator.MOCK_INIT_HEIGHT

        for x in range(nbrToGenerate):

            classId:       int       = next(self._classIdGenerator)
            mockPyutClass: PyutClass = self._createMockPyutClass(classId)

            mockOglClass: MagicMock                 = MagicMock(spec=OglClass)
            mockOglClass.GetPosition.return_value   = (mockX, mockY)
            mockOglClass.GetSize.return_value       = (mockWidth, mockHeight)

            type(mockOglClass).id                   = PropertyMock(return_value=classId)
            type(mockOglClass).pyutObject           = PropertyMock(return_value=mockPyutClass)

            umlObjects.append(mockOglClass)

            mockX  += MockGenerator.MOCK_X_POSITION_INCREMENT
            mockY  += MockGenerator.MOCK_Y_POSITION_INCREMENT

        return umlObjects

    def addMockLinks(self, oglClasses: List[MagicMock]):

        currentIdx: int = 0
        while True:

            parentClass: MagicMock = oglClasses[currentIdx]
            childClass:  MagicMock = oglClasses[currentIdx + 1]

            self.logger.debug(f'parentID: {parentClass.id} childID: {childClass.id}')
            self._createMockLink(parentClass, childClass)
            currentIdx += 2
            if currentIdx >= len(oglClasses):
                break

    def _createMockPyutClass(self, classNumber: int) -> MagicMock:
        """

        Args:
            classNumber:
        Returns:
        """
        mockPyutClass: MagicMock = MagicMock(spec=PyutClass)
        className: str = f'{MockGenerator.MOCK_CLASS_NAME_PREFIX}{classNumber}'
        # mockPyutClass.getName.return_value = className

        type(mockPyutClass).name = PropertyMock(return_value=className)
        type(mockPyutClass).stereotype = PyutStereotype.TYPE

        return mockPyutClass

    def _createMockLink(self, src: MagicMock, dst: MagicMock) -> MagicMock:
        """
        pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

        oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        src.getPyutObject().addLink(pyutLink)

        Args:
            src:    Mock OglClass
            dst:   Mock OglClass

        Returns:
            Mocked OglLink
        """
        oglLink:  MagicMock = MagicMock(spec=OglLink)

        linkId = next(self._linkIDGenerator)

        type(oglLink).id = PropertyMock(return_value=linkId)

        mockSourceAnchor:      MagicMock = MagicMock(spec=AnchorPoint)
        mockDestinationAnchor: MagicMock = MagicMock(spec=AnchorPoint)

        mockSourceAnchor.GetPosition.return_value      = [22, 44]
        mockDestinationAnchor.GetPosition.return_value = [1024, 450]

        mockLinePointMiddle: MagicMock = MagicMock(spec=LinePoint)
        mockLinePointMiddle.GetPosition.return_value = [100, 100]

        oglLink.GetControlPoints.return_value  = [mockLinePointMiddle]
        type(oglLink).sourceAnchor      = PropertyMock(return_value=mockSourceAnchor)
        type(oglLink).destinationAnchor = PropertyMock(return_value=mockDestinationAnchor)

        type(oglLink).sourceShape      = PropertyMock(return_value=src)
        type(oglLink).destinationShape = PropertyMock(return_value=dst)
        #
        # PyutLink object simple enough so create real one
        pyutLink: PyutLink = PyutLink("", linkType=PyutLinkType.INHERITANCE, source=src.pyutObject, destination=dst.pyutObject)

        type(src).links = PropertyMock(return_value=[oglLink])
        type(dst).links = PropertyMock(return_value=[oglLink])

        mockPyutClass = src.pyutObject
        type(mockPyutClass).links = PropertyMock(return_value=[pyutLink])

        return oglLink

    def _generateClassId(self):
        classId: int = 10000
        while True:
            yield classId
            classId += 10

    def _generateLinkId(self):
        linkId: int = 1024
        while True:
            yield linkId
            linkId += 1
