
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutplugincore.PluginInterface import PluginInterface
from pyutplugincore.ICommunicator import ICommunicator
from pyutplugincore.coretypes.Helper import OglClasses

from tests.TestBase import TestBase

# noinspection SpellCheckingInspection
"""
import the class you want to test here
from pyutplugincore.CoreTypes import BaseFormat
"""


class TestAbstractPlugin(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestAbstractPlugin.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestAbstractPlugin.clsLogger

    def tearDown(self):
        pass

    def testCannotInstantiate(self):

        self.assertRaises(TypeError, self._instantiateAbstractClass)

    def _instantiateAbstractClass(self):

        communicator: ICommunicator = cast(ICommunicator, None)
        oglObjects:   OglClasses    = cast(OglClasses, None)
        # noinspection PyUnusedLocal
        abc: PluginInterface = PluginInterface(communicator=communicator, oglClasses=oglObjects)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestAbstractPlugin))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
