from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglObjects

from tests.TestBase import TestBase

from pyutplugins.ioplugins.java.JavaWriter import JavaWriter


class TestJavaWriter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestJavaWriter.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:      Logger     = TestJavaWriter.clsLogger

        super().setUp()
        self._javaWriter: JavaWriter = JavaWriter(writeDirectory=f'{self._getTemporaryDirectory()}')

    def tearDown(self):
        super().tearDown()

    def testOneClassWrite(self):

        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='SingleClass.xml', documentName='SingleClass')
        self._javaWriter.write(oglObjects=cast(OglObjects, oglClasses))

        status: int = self._runDiff(goldenPackageName=TestBase.GOLDEN_JAVA_PACKAGE_NAME, baseFileName='SingleClass.java')
        self.assertEqual(0, status, 'Diff of single class failed;  Something changed')

        self._cleanupGenerated('SingleClass.java')

    def testComplexClass(self):
        """
        Test multiple classes with parameters and return plugintypes
        """
        generatedFileNames: List[str] = ['Account.java', 'ATM.java', 'Bank.java', 'CheckingAccount.java', 'Customer.java', 'SavingsAccount.java']

        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='ATM-Model.xml', documentName='Class Diagram')
        self._javaWriter.write(oglObjects=cast(OglObjects, oglClasses))

        for generatedFileName in generatedFileNames:
            status: int = self._runDiff(goldenPackageName=TestBase.GOLDEN_JAVA_PACKAGE_NAME, baseFileName=generatedFileName)
            self.assertEqual(0, status, f'Diff of {generatedFileName} file failed;  Something changed')

        for generatedFileName in generatedFileNames:
            self._cleanupGenerated(generatedFileName)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestJavaWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
