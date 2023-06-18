
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import Window

from pyutplugins.PluginManager import PluginManager

from pyutplugins.IPluginAdapter import IPluginAdapter

from tests.scaffoldv2.PluginAdapterV2 import PluginAdapterV2
from tests.scaffoldv2.eventengine.EventEngine import EventEngine
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine

from tests.TestBase import TestBase


class TestPluginManager(TestBase):
    """
    Does not test any execution of the pyutplugins;  Only the interfaces needed by Pyut
    to set up menu times and test whether we actually dynamically loaded the pyutplugins
    """
    def setUp(self):
        super().setUp()

        eventEngine:   IEventEngine   = EventEngine(listeningWindow=cast(Window, None))       # don't use these in these tests
        pluginAdapter: IPluginAdapter = PluginAdapterV2(eventEngine=eventEngine)

        self.pluginManager: PluginManager = PluginManager(pluginAdapter=pluginAdapter)

    def tearDown(self):
        super().tearDown()

    def testInstantiated(self):
        self.assertIsNotNone(self.pluginManager, 'Trivial instantiation should pass')

    def testToolPluginsLoaded(self):
        """Another test"""
        toolPlugins = self.pluginManager.toolPlugins
        self.assertIsNotNone(toolPlugins, 'Where are my tool pyutplugins')

    def testToolPluginsProperty(self):
        toolPlugins = self.pluginManager.toolPlugins
        self.assertIsNotNone(toolPlugins, 'Oops')

    def testInputPluginsProperty(self):
        inputPlugins = self.pluginManager.inputPlugins
        self.assertIsNotNone(inputPlugins, 'Oh no !!')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPluginManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
