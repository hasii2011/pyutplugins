
from unittest import TestSuite
from unittest import main as unitTestMain

from hasiihelper.UnitTestBase import UnitTestBase

from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension

from pyutplugins.plugintypes.BaseFormat import BaseFormat

from pyutplugins.exceptions.InvalidPluginExtensionException import InvalidPluginExtensionException
from pyutplugins.exceptions.InvalidPluginNameException import InvalidPluginNameException


class TestBaseFormat(UnitTestBase):
    """
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testBasicInstantiation(self):
        name:        FormatName        = FormatName('BasicPlugin')
        extension:   PluginExtension   = PluginExtension('put')
        description: PluginDescription = PluginDescription('I am a basic plugin')

        baseFormat: BaseFormat = BaseFormat(name, extension, description)

        self.assertIsNotNone(baseFormat, 'Oops how that this happen')

    def testBadExtension(self):
        self.assertRaises(InvalidPluginExtensionException, lambda: self._badExtension())

    def testFileNameContainsSingleQuote(self):
        nameToTest: FormatName = FormatName('Basic\'Plugin')
        self.assertRaises(InvalidPluginNameException, lambda: self.__testBadName(nameToTest))

    def testFileNameContainsDoubleQuote(self):
        nameToTest: FormatName = FormatName('Basic\"Plugin')
        self.assertRaises(InvalidPluginNameException, lambda: self.__testBadName(nameToTest))

    def testFileContainsOtherInvalid(self):
        nameToTest: FormatName = FormatName('Basic$Plugin')
        self.assertRaises(InvalidPluginNameException, lambda: self.__testBadName(nameToTest))

    def testAny(self):
        string = r"/\?%"
        test = "This is my string % my string ?"
        self.logger.debug(any(elem in test for elem in string))

        test2 = "Just a test string"
        self.logger.debug(any(elem in test2 for elem in string))

    def __testBadName(self, nameToTest: FormatName):
        extension:   PluginExtension   = PluginExtension('put')
        description: PluginDescription = PluginDescription('I am a basic plugin')

        # noinspection PyUnusedLocal
        baseFormat: BaseFormat = BaseFormat(nameToTest, extension, description)

    def _badExtension(self):
        name:        FormatName        = FormatName('BasicPlugin')
        extension:   PluginExtension   = PluginExtension('.put')
        description: PluginDescription = PluginDescription('I am a basic plugin')

        # noinspection PyUnusedLocal
        baseFormat: BaseFormat = BaseFormat(name, extension, description)

    def testSpecialBad(self):
        string = r"/\?%"
        test = "This is my string % my string ?"
        self.logger.debug(any(elem in test for elem in string))

        test2 = "Just a test string"
        self.logger.debug(any(elem in test2 for elem in string))

    def testSpecialGood(self):
        string = r"/\?%"
        test = "This is my string % my string ?"
        self.logger.debug(f"{string=} {test=} {self.containsSpecialCharacters(string, test)=}")

        test2 = "Just a test string"
        self.logger.debug(f"{self.containsSpecialCharacters(string, test2)=}")

    def containsSpecialCharacters(self, string: str, test: str) -> bool:
        for special in string:
            if special in test:
                return True
        return False


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestBaseFormat))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
