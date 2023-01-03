
from typing import Dict
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from plugins.core.coretypes.Types import OglObjects

from plugins.toolplugins.sugiyama.RealSugiyamaNode import RealSugiyamaNode
from plugins.toolplugins.sugiyama.Sugiyama import HierarchicalGraphNodes
from plugins.toolplugins.sugiyama.Sugiyama import NodeList
from plugins.toolplugins.sugiyama.VirtualSugiyamaNode import VirtualSugiyamaNode
from plugins.toolplugins.sugiyama.Sugiyama import Sugiyama

from tests.MockPluginAdapter import MockPluginAdapter
from tests.TestBase import TestBase


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

        mockMediator: MockPluginAdapter = MockPluginAdapter()
        self._sugiyama: Sugiyama = Sugiyama(pluginAdapter=mockMediator)

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
            nodeName:      str = hierarchicalGraphNode.getName()    # type: ignore
            actualLevel:   int = hierarchicalGraphNode.getLevel()   # type: ignore
            try:
                expectedLevel: int = expectedResults[nodeName]
            except KeyError:
                self.fail(f'Unknown node name {nodeName}')

            self.assertEqual(expectedLevel, actualLevel, f'Level incorrect for node {nodeName}')

    def testAddVirtualNodes(self):

        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()

        self._testLevel0Nodes(sugiyama.levels[0])
        self._testLevel1Nodes(sugiyama.levels[1])
        self._testLevel2Nodes(sugiyama.levels[2])
        self._testLevel3Nodes(sugiyama.levels[3])

    def testBarycenter(self):
        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        sugiyama.barycenter()

        self.logger.info(f'Number of hierarchical intersections: {sugiyama._getNbIntersectAll()}')

        sugiyama.addNonHierarchicalNodes()

    def testAddNonHierarchicalNodes(self):
        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        sugiyama.barycenter()

        self.logger.info(f'Number of hierarchical intersections: {sugiyama._getNbIntersectAll()}')

        sugiyama.addNonHierarchicalNodes()

    def testFixPositions(self):

        sugiyama: Sugiyama = self._sugiyama
        sugiyama.createInterfaceOglALayout(oglObjects=self._oglObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        sugiyama.barycenter()

        self.logger.info(f'Number of hierarchical intersections: {sugiyama._getNbIntersectAll()}')

        sugiyama.addNonHierarchicalNodes()

        sugiyama.fixPositions()

    def _testLevel0Nodes(self, level0Nodes: NodeList):
        """
        Level 0 should have 0 virtual nodes
        Args:
            level0Nodes:
        """
        for level0Node in level0Nodes:
            self.assertTrue(isinstance(level0Node, RealSugiyamaNode), 'No virtual nodes at level 0')

    def _testLevel1Nodes(self, level1Nodes: NodeList):
        """
        Level 1 should have virtual nodes at indices 1-4

        Args:
            level1Nodes:
        """
        level1Node1 = level1Nodes[1]
        self.assertTrue(isinstance(level1Node1, VirtualSugiyamaNode), 'Missing virtual node')

        level1Node2 = level1Nodes[2]
        self.assertTrue(isinstance(level1Node2, VirtualSugiyamaNode), 'Missing virtual node')

    def _testLevel2Nodes(self, level2Nodes: NodeList):
        """
        Level 2 should have virtual nodes at indices 1-2
        Args:
            level2Nodes:
        """
        level2Node1 = level2Nodes[1]
        self.assertTrue(isinstance(level2Node1, VirtualSugiyamaNode), 'Missing virtual node')

        level2Node2 = level2Nodes[1]
        self.assertTrue(isinstance(level2Node2, VirtualSugiyamaNode), 'Missing virtual node')

    def _testLevel3Nodes(self, level3Nodes: NodeList):
        """
        Level 3 should have 0 virtual nodes
        Args:
            level3Nodes:
        """
        for level3Node in level3Nodes:
            self.assertTrue(isinstance(level3Node, RealSugiyamaNode), 'No virtual nodes at level 0')

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
