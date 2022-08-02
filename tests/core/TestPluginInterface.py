
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from core.PluginInterface import PluginInterface
from core.IMediator import IMediator

from tests.TestBase import TestBase


class TestPluginInterface(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPluginInterface.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestPluginInterface.clsLogger

    def tearDown(self):
        pass

    def testCannotInstantiate(self):

        self.assertRaises(TypeError, self._instantiateAbstractClass)

    def _instantiateAbstractClass(self):

        mediator: IMediator = cast(IMediator, None)
        # noinspection PyUnusedLocal
        abc: PluginInterface = PluginInterface(mediator=mediator, )


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPluginInterface))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
