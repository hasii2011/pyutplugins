
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import Window

from pyutplugins.PluginManager import PluginManager

from pyutplugins.coreinterfaces.IPluginAdapter import IPluginAdapter

from tests.TestBase import TestBase
from tests.scaffoldv2.PluginAdapterV2 import PluginAdapterV2
from tests.scaffoldv2.eventengine.EventEngine import EventEngine
from tests.scaffoldv2.eventengine.IEventEngine import IEventEngine


class TestPluginManager(TestBase):
    """
    Does not test any execution of the pyutplugins;  Only the interfaces needed by Pyut
    to set up menu times and test whether we actually dynamically loaded the pyutplugins
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPluginManager.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:        Logger        = TestPluginManager.clsLogger

        eventEngine: IEventEngine = EventEngine(listeningWindow=cast(Window, None))       # don't use these in these tests

        pluginAdapter: IPluginAdapter = PluginAdapterV2(eventEngine=eventEngine)

        self.pluginManager: PluginManager = PluginManager(pluginAdapter=pluginAdapter)

    def tearDown(self):
        pass

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
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPluginManager))

    return testSuite


if __name__ == '__main__':
    unitTestMain()