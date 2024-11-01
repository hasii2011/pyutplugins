
from typing import List
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain
from unittest.mock import MagicMock

from tests.MockGenerator import MockGenerator

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.ioplugins.gml.GMLExporter import GMLExporter

from tests.ProjectTestBase import ProjectTestBase


class TestGMLExporter(ProjectTestBase):

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
    def setUp(self):
        super().setUp()

        self.exporter: GMLExporter = GMLExporter()
        self._mockGenerator: MockGenerator = MockGenerator()

    def tearDown(self):
        super().tearDown()

    def testBasicCreation(self):

        umlObjects: List[MagicMock] = self._mockGenerator.generateMockNodes(TestGMLExporter.NUMBER_OF_MOCK_CLASSES)

        self._mockGenerator.addMockLinks(umlObjects)

        self.exporter.prettyPrint = True
        self.exporter.translate(cast(OglObjects, umlObjects))
        gml: str = self.exporter.gml

        self.assertIsNotNone(gml, 'Generate Something!!')
        self.logger.debug(f'Generated GML:\n{gml}')

        fqFileName: str = ProjectTestBase.constructGeneratedName(baseFileName=TestGMLExporter.UNIT_TEST_FILENAME)

        self.exporter.write(fqFileName)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_GML_PACKAGE_NAME, baseFileName=TestGMLExporter.UNIT_TEST_FILENAME)

        self.assertEqual(0, status, 'Simple GML generation failed')

        self.cleanupGenerated(TestGMLExporter.UNIT_TEST_FILENAME)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestGMLExporter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
