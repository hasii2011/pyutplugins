from typing import Dict
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from plugins.common.Types import OglObjects
from plugins.tools.sugiyama.Sugiyama import HierarchicalGraphNodes
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

    def testLevelFind(self):
        """
        """
        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        levelsFound: bool = sugiyama.levelFind()
        self.assertTrue(levelsFound, 'There should be no cyclical hierarchical links')

        self._debugPrintHierarchicalGraphNodes(sugiyama._hierarchyGraphNodesList)
        # NodeName, Level
        expectedResults: Dict[str, int] = {
            'Level1ClassA': 3,
            'Level2ClassA': 0,
            'Level2ClassB': 0,
            'Level2ClassC': 2,
            'Level3ClassA': 0,
            'Level3ClassB': 0,
            'Level3ClassC': 1,
            'Level4ClassA': 0,
            'Level4ClassB': 0
        }
        hierarchicalGraphNodes: HierarchicalGraphNodes = sugiyama._hierarchyGraphNodesList

        for hierarchicalGraphNode in hierarchicalGraphNodes:
            nodeName:      str = hierarchicalGraphNode.getName()
            actualLevel:   int = hierarchicalGraphNode.getLevel()
            try:
                expectedLevel: int = expectedResults[nodeName]
            except KeyError as ke:
                self.fail(f'Unknown node name {nodeName}')

            self.assertEqual(expectedLevel, actualLevel, f'Level incorrect for node {nodeName}')

    def testAddVirtualNodes(self):

        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        #
        # Level 0 should have 0 virtual nodes

        # Level 1 should have virtual nodes at indices 1-4
        # Level 2 should have virtual nodes at indices 1-2
        # Level 3 should have 0 virtual nodes

    def testBarycenter(self):
        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        sugiyama.barycenter()

    def _debugPrintOglObjects(self, oglObjects: OglObjects):
        for oglObject in oglObjects:
            self.logger.debug(f'{oglObject}')

    def _debugPrintHierarchicalGraphNodes(self, hierarchicalGraphNodes: HierarchicalGraphNodes):
        for hierarchicalGraphNode in hierarchicalGraphNodes:
            self.logger.debug(f'{hierarchicalGraphNode}')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestSugiyama))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
