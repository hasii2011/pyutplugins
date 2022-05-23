
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutplugincore.coretypes.PluginDataTypes import PluginDescription
from pyutplugincore.coretypes.PluginDataTypes import PluginExtension
from pyutplugincore.coretypes.PluginDataTypes import PluginName

from pyutplugincore.coretypes.BaseFormat import BaseFormat

from pyutplugincore.exceptions.InvalidPluginExtensionException import InvalidPluginExtensionException
from pyutplugincore.exceptions.InvalidPluginNameException import InvalidPluginNameException

from tests.TestBase import TestBase


class TestBaseFormat(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestBaseFormat.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestBaseFormat.clsLogger

    def tearDown(self):
        pass

    def testBasicInstantiation(self):
        name:        PluginName        = PluginName('BasicPlugin')
        extension:   PluginExtension   = PluginExtension('put')
        description: PluginDescription = PluginDescription('I am a basic plugin')

        baseFormat: BaseFormat = BaseFormat(name, extension, description)

        self.assertIsNotNone(baseFormat, 'Oops how that this happen')

    def testBadExtension(self):
        self.assertRaises(InvalidPluginExtensionException, lambda: self._badExtension())

    def testFileNameContainsSingleQuote(self):
        nameToTest: PluginName = PluginName('Basic\'Plugin')
        self.assertRaises(InvalidPluginNameException, lambda: self.__testBadName(nameToTest))

    def testFileNameContainsDoubleQuote(self):
        nameToTest: PluginName = PluginName('Basic\"Plugin')
        self.assertRaises(InvalidPluginNameException, lambda: self.__testBadName(nameToTest))

    def testFileContainsOtherInvalid(self):
        nameToTest: PluginName = PluginName('Basic$Plugin')
        self.assertRaises(InvalidPluginNameException, lambda: self.__testBadName(nameToTest))

    def testAny(self):
        string = r"/\?%"
        test = "This is my string % my string ?"
        self.logger.debug(any(elem in test for elem in string))

        test2 = "Just a test string"
        self.logger.debug(any(elem in test2 for elem in string))

    def __testBadName(self, nameToTest: PluginName):
        extension:   PluginExtension   = PluginExtension('put')
        description: PluginDescription = PluginDescription('I am a basic plugin')

        # noinspection PyUnusedLocal
        baseFormat: BaseFormat = BaseFormat(nameToTest, extension, description)

    def _badExtension(self):
        name:        PluginName        = PluginName('BasicPlugin')
        extension:   PluginExtension   = PluginExtension('.put')
        description: PluginDescription = PluginDescription('I am a basic plugin')

        # noinspection PyUnusedLocal
        baseFormat: BaseFormat = BaseFormat(name, extension, description)

    def testSpecialBad(self):
        string = r"/\?%"
        test = "This is my string % my string ?"
        print(any(elem in test for elem in string))

        test2 = "Just a test string"
        print(any(elem in test2 for elem in string))

    def testSpecialGood(self):
        string = r"/\?%"
        test = "This is my string % my string ?"
        self.logger.warning(f"{string=} {test=} {self.containsSpecialCharacters(string, test)=}")

        test2 = "Just a test string"
        self.logger.warning(f"{self.containsSpecialCharacters(string, test2)=}")

    def containsSpecialCharacters(self, string: str, test: str) -> bool:
        for special in string:
            if special in test:
                return True
        return False


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestBaseFormat))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
