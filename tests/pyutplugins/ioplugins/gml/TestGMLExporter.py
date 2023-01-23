
from logging import Logger
from logging import getLogger

from typing import List
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from os import remove as osRemove

from tests.MockGenerator import MockGenerator

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.ioplugins.gml.GMLExporter import GMLExporter

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
        self._mockGenerator: MockGenerator = MockGenerator()

    def tearDown(self):
        osRemove(TestGMLExporter.UNIT_TEST_FILENAME)

    def testBasicCreation(self):

        umlObjects: List[MagicMock] = self._mockGenerator.generateMockNodes(TestGMLExporter.NUMBER_OF_MOCK_CLASSES)

        self._mockGenerator.addMockLinks(umlObjects)

        self.exporter.prettyPrint = True
        self.exporter.translate(cast(OglObjects, umlObjects))
        gml: str = self.exporter.gml

        self.assertIsNotNone(gml, 'Generate Something!!')
        self.logger.debug(f'Generated GML:\n{gml}')
        self.exporter.write(TestGMLExporter.UNIT_TEST_FILENAME)
        

def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestGMLExporter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
