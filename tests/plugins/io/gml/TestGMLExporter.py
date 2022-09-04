
from logging import Logger
from logging import getLogger

from typing import List
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from os import remove as osRemove

from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink

from miniogl.AnchorPoint import AnchorPoint

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from core.types.Types import OglClasses

from plugins.io.gml.GMLExporter import GMLExporter

from tests.TestBase import TestBase


class TestGMLExporter(TestBase):

    NUMBER_OF_MOCK_CLASSES:   int = 2
    MOCK_CLASS_NAME_PREFIX:   str = 'ClassName_'
    MOCK_START_ID_NUMBER:     int = 42
    MOCK_ID_NUMBER_INCREMENT: int = 5
    MOCK_INIT_WIDTH:          float = 50.0
    MOCK_INIT_HEIGHT:         float = 50.0
    MOCK_INIT_POSITION_X:     float = 100.0
    MOCK_INIT_POSITION_Y:     float = 100.0
    MOCK_X_POSITION_INCREMENT: float = 75.0
    MOCK_Y_POSITION_INCREMENT: float = 100.0

    UNIT_TEST_FILENAME: str = 'UnitTest.gml'
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestGMLExporter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:   Logger      = TestGMLExporter.clsLogger
        self.exporter: GMLExporter = GMLExporter()
        self._linkIDGenerator = self._generateLinkId()

    def tearDown(self):
        osRemove(TestGMLExporter.UNIT_TEST_FILENAME)

    def testBasicCreation(self):

        umlObjects: List[MagicMock] = self._generateMockNodes(TestGMLExporter.NUMBER_OF_MOCK_CLASSES)

        self._addMockLinks(umlObjects)

        self.exporter.prettyPrint = True
        self.exporter.translate(cast(OglClasses, umlObjects))
        gml: str = self.exporter.gml

        self.assertIsNotNone(gml, 'Generate Something!!')
        self.logger.debug(f'Generated GML:\n{gml}')
        self.exporter.write(TestGMLExporter.UNIT_TEST_FILENAME)

    def _generateMockNodes(self, nbrToGenerate) -> List[MagicMock]:

        umlObjects: List[MagicMock] = []

        initId: int                 = TestGMLExporter.MOCK_START_ID_NUMBER
        mockX: float = TestGMLExporter.MOCK_INIT_POSITION_X
        mockY: float = TestGMLExporter.MOCK_INIT_POSITION_Y
        mockWidth:  float = TestGMLExporter.MOCK_INIT_WIDTH
        mockHeight: float = TestGMLExporter.MOCK_INIT_HEIGHT

        for x in range(nbrToGenerate):
            mockPyutClass: MagicMock = MagicMock(spec=PyutClass)
            mockPyutClass.getName.return_value = f'{TestGMLExporter.MOCK_CLASS_NAME_PREFIX}{x}'

            mockOglClass: MagicMock                 = MagicMock(spec=OglClass)
            mockOglClass.GetID.return_value         = initId
            mockOglClass.GetPosition.return_value   = (mockX, mockY)
            mockOglClass.GetSize.return_value       = (mockWidth, mockHeight)
            mockOglClass.getPyutObject.return_value = mockPyutClass
            umlObjects.append(mockOglClass)

            initId += TestGMLExporter.MOCK_ID_NUMBER_INCREMENT
            mockX  += TestGMLExporter.MOCK_X_POSITION_INCREMENT
            mockY  += TestGMLExporter.MOCK_Y_POSITION_INCREMENT

        return umlObjects

    def _addMockLinks(self, oglClasses: List[MagicMock]):

        currentIdx: int = 0
        while True:

            parentClass: MagicMock = oglClasses[currentIdx]
            childClass:  MagicMock = oglClasses[currentIdx + 1]

            self.logger.debug(f'parentID: {parentClass.GetID()} childID: {childClass.GetID()}')
            self.__createMockLink(parentClass, childClass)
            currentIdx += 2
            if currentIdx >= len(oglClasses):
                break

    def __createMockLink(self, src: MagicMock, dst: MagicMock) -> MagicMock:
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
        oglLink.GetID.return_value = linkId

        mockSourceAnchor:      MagicMock = MagicMock(spec=AnchorPoint)
        mockDestinationAnchor: MagicMock = MagicMock(spec=AnchorPoint)

        mockSourceAnchor.GetPosition.return_value = (22, 44)
        mockDestinationAnchor.GetPosition.return_value = (1024, 450)

        oglLink.sourceAnchor.return_value      = mockSourceAnchor
        oglLink.destinationAnchor.return_value = mockDestinationAnchor

        oglLink.getSourceShape.return_value      = src
        oglLink.getDestinationShape.return_value = dst
        #
        # PyutLink object simple enough so create real one
        pyutLink: PyutLink = PyutLink("", linkType=PyutLinkType.INHERITANCE, source=src.getPyutObject(), destination=dst.getPyutObject())

        src.getLinks.return_value  = [oglLink]
        dst.getLinks.return_value = [oglLink]

        mockPyutClass = src.getPyutObject()
        mockPyutClass.getLinks.return_value = [pyutLink]

        return oglLink

    def _generateLinkId(self):
        num: int = 1024
        while True:
            yield num
            num += 1


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGMLExporter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
