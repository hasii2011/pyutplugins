
from typing import List
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from untanglepyut.XmlVersion import XmlVersion

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglObjects

from tests.ProjectTestBase import ProjectTestBase

from pyutplugins.ioplugins.java.JavaWriter import JavaWriter


class TestJavaWriter(ProjectTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self._javaWriter: JavaWriter = JavaWriter(writeDirectory=f'{ProjectTestBase.getTemporaryDirectory()}')

    def tearDown(self):
        super().tearDown()

    def testOneClassWrite(self):

        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='SingleClass.xml', documentName='SingleClass', xmlVersion=XmlVersion.V11)
        self._javaWriter.write(oglObjects=cast(OglObjects, oglClasses))

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_JAVA_PACKAGE_NAME, baseFileName='SingleClass.java')
        self.assertEqual(0, status, 'Diff of single class failed;  Something changed')

        ProjectTestBase.cleanupGenerated('SingleClass.java')

    def testComplexClass(self):
        """
        Test multiple classes with parameters and return plugintypes
        """
        generatedFileNames: List[str] = ['Account.java', 'ATM.java', 'Bank.java', 'CheckingAccount.java', 'Customer.java', 'SavingsAccount.java']

        oglClasses: OglClasses = self._xmlFileToOglClasses(filename='ATM-Model.xml', documentName='Class Diagram', xmlVersion=XmlVersion.V11)
        self._javaWriter.write(oglObjects=cast(OglObjects, oglClasses))

        for generatedFileName in generatedFileNames:
            status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_JAVA_PACKAGE_NAME, baseFileName=generatedFileName)
            self.assertEqual(0, status, f'Diff of {generatedFileName} file failed;  Something changed')

        for generatedFileName in generatedFileNames:
            self.cleanupGenerated(generatedFileName)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestJavaWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
