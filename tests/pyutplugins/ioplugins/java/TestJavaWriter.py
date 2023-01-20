from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from os import system as osSystem
from os import sep as osSep

from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglObjects

from tests.TestBase import TestBase

from pyutplugins.ioplugins.java.JavaWriter import JavaWriter


class TestJavaWriter(TestBase):
    """
    """
    EXTERNAL_DIFF:         str = '/usr/bin/diff -w '
    EXTERNAL_CLEAN_UP_TMP: str = 'rm '

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestJavaWriter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:      Logger     = TestJavaWriter.clsLogger

        super().setUp()
        self._javaWriter: JavaWriter = JavaWriter(writeDirectory='/tmp')

    def tearDown(self):
        super().tearDown()

    def testOneClassWrite(self):

        self._cleanupGenerated('SingleClass.java')

        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='SingleClass.xml', documentName='SingleClass')
        self._javaWriter.write(oglObjects=cast(OglObjects, oglClasses))

        status: int = self._runDiff('SingleClass.java')
        self.assertEqual(0, status, 'Diff of single class failed;  Something changed')

    def testComplexClass(self):
        """
        Test multiple classes with parameters and return plugintypes
        """
        generatedFileNames: List[str] = ['Account.java', 'ATM.java', 'Bank.java', 'CheckingAccount.java', 'Customer.java', 'SavingsAccount.java']

        for generatedFileName in generatedFileNames:
            self._cleanupGenerated(generatedFileName)

        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='ATM-Model.xml', documentName='Class Diagram')
        self._javaWriter.write(oglObjects=cast(OglObjects, oglClasses))

        for generatedFileName in generatedFileNames:
            status: int = self._runDiff(generatedFileName)
            self.assertEqual(0, status, f'Diff of {generatedFileName} file failed;  Something changed')

    def _cleanupGenerated(self, fileName: str):

        generatedFileName: str = self._constructGeneratedName(fileName=fileName)

        osSystem(f'{TestJavaWriter.EXTERNAL_CLEAN_UP_TMP} {generatedFileName}')

    def _runDiff(self, fileName: str) -> int:

        baseFileName:      str = resource_filename(TestBase.RESOURCES_TEST_JAVA_BASE_FILES_PACKAGE_NAME, fileName)
        generatedFileName: str = self._constructGeneratedName(fileName=fileName)

        status: int = osSystem(f'{TestJavaWriter.EXTERNAL_DIFF} {baseFileName} {generatedFileName}')

        return status

    def _constructGeneratedName(self, fileName: str) -> str:

        generatedFileName: str = f'{osSep}tmp{osSep}{fileName}'
        return generatedFileName


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestJavaWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
