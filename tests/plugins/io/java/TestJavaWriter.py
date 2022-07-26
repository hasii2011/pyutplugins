
from typing import cast

from logging import Logger
from logging import getLogger

from os import system as osSystem
from os import sep as osSep

from pkg_resources import resource_filename

from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from plugins.common.Types import OglClasses

from tests.TestBase import TestBase

from plugins.io.java.JavaWriter import JavaWriter


class TestJavaWriter(TestBase):
    """
    """
    EXTERNAL_DIFF:         str = '/usr/bin/diff -w '
    EXTERNAL_CLEAN_UP_TMP: str = 'rm -v '

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
        self._javaWriter.write(oglObjects=oglClasses)

        status: int = self._runDiff('SingleClass.java')
        self.assertEqual(0, status, 'Diff of single class failed;  Something changed')

    def testComplexClass(self):
        """Another test"""
        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='ATM-Model.xml', documentName='Class Diagram')
        self._javaWriter.write(oglObjects=oglClasses)

    def _xmlFileToOglClasses(self, filename: str, documentName: str) -> OglClasses:

        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, filename)
        untangler:  UnTangler = UnTangler(fqFileName=fqFileName)
        untangler.untangle()

        document: Document = untangler.documents[DocumentTitle(documentName)]

        return OglClasses(document.oglClasses)

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
