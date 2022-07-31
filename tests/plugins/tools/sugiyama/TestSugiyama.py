
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from plugins.common.Types import OglObjects
from tests.TestBase import TestBase

from plugins.tools.sugiyama.Sugiyama import Sugiyama


class TestSugiyama(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestSugiyama.clsLogger = getLogger(__name__)

    def setUp(self):
        super().setUp()

        self.logger: Logger = TestSugiyama.clsLogger

        self._sugiyama: Sugiyama = Sugiyama()

        self._oglObjects: OglObjects = self._xmlFileToOglObjects(filename='SugiyamaTest.xml', documentName='Sugiyama')

    def tearDown(self):
        pass

    def testCreateInterfaceOglALayout(self):

        self._debugPrintOglObjects(self._oglObjects)

        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)

        self.assertEqual(0, len(sugiyama._nonHierarchyGraphNodesList), 'Should not find non hierarchy nodes')
        self.assertEqual(0, len(sugiyama._nonHierarchyGraphNodesList), 'Should not find non hierarchy links')
        self.assertEqual(9, len(sugiyama._hierarchyGraphNodesList), 'Did not generate correct number of hierarchical graph nodes')

    def testName2(self):
        """Another test"""
        pass

    def _debugPrintOglObjects(self, oglObjects: OglObjects):

        for oglObject in oglObjects:
            self.logger.warning(f'{oglObject}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSugiyama))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
