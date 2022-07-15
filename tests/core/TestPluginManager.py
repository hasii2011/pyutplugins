
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from core.PluginManager import PluginManager
from core.coretypes.PluginDataTypes import PluginIDMap

from tests.TestBase import TestBase


class TestPluginManager(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPluginManager.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:        Logger        = TestPluginManager.clsLogger
        self.pluginManager: PluginManager = PluginManager()

    def tearDown(self):
        pass

    def testInstantiated(self):
        self.assertIsNotNone(self.pluginManager, 'Trivial instantiation should pass')

    def testToolPluginsLoaded(self):
        """Another test"""
        toolPlugins = self.pluginManager.toolPlugins
        self.assertIsNotNone(toolPlugins, 'Where are my tool plugins')

    def testToolPluginsProperty(self):
        toolPlugins = self.pluginManager.toolPlugins
        self.assertIsNotNone(toolPlugins, 'Oops')

    def testInputPluginsProperty(self):
        inputPlugins = self.pluginManager.inputPlugins
        self.assertIsNotNone(inputPlugins, 'Oh no !!')

    def testToolPluginsWxIdGenerated(self):

        pluginMap: PluginIDMap = self.pluginManager.toolPluginsMap
        self.assertIsNotNone(pluginMap, 'Where is my map')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPluginManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
