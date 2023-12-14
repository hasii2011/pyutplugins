
from typing import List

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodelv2.PyutModelTypes import Implementors

from ogl.OglClass import OglClass

from pyutplugins.ioplugins.java.JavaReader import Extenders
from pyutplugins.ioplugins.java.JavaReader import InterfaceMap
from pyutplugins.ioplugins.java.JavaReader import JavaReader
from pyutplugins.ioplugins.java.JavaReader import ReversedClasses

from tests.TestBase import TestBase

TEST_BASE_CLASS_NAME:  str = 'BaseModel'
TEST_INTERFACE_NAME_1: str = 'IModified'
TEST_INTERFACE_NAME_2: str = 'ICreated'
TEST_INTERFACE_NAME_3: str = 'Tenancy'


class TestJavaReader(TestBase):
    """
    """
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testBasicClass(self):

        reverseJava: JavaReader = JavaReader()

        basicClassPath: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME, 'Tenant.java')

        reverseJava.parseFile(basicClassPath)

        # 2 because implements BaseModel
        self.assertEqual(2, len(reverseJava.reversedClasses))

    def testCorrectlyGeneratedSingleSubclassMap(self):

        reverseJava: JavaReader = self._createReversedOglClasses()

        expectedLength: int = 1
        actualLength:   int = len(reverseJava._subClassMap)
        self.assertEqual(expectedLength, actualLength, "More than one base class")

    def testCorrectlyGeneratedSubClassEntry(self):

        reverseJava: JavaReader = self._createReversedOglClasses()

        testBaseClass: OglClass = reverseJava.reversedClasses[TEST_BASE_CLASS_NAME]

        self.assertIn(testBaseClass, reverseJava._subClassMap, 'Not the correct base class')

    def testCorrectlyGeneratedSubClasses(self):

        reverseJava: JavaReader = self._createReversedOglClasses()

        testBaseClass: OglClass = reverseJava.reversedClasses[TEST_BASE_CLASS_NAME]

        extenders: Extenders = reverseJava._subClassMap[testBaseClass]

        expectedLength: int = 3     # Because Tenant also extends BaseModel
        actualLength:   int = len(extenders)

        self.assertEqual(expectedLength, actualLength, "Incorrect number of subclasses")

    def testCorrectlyGeneratedInterfaceMap(self):

        reverseJava: JavaReader = self._createReversedOglClasses()

        expectedLength: int = 3
        actualLength:   int = len(reverseJava.interfaceMap)
        self.assertEqual(expectedLength, actualLength, 'Incorrect number of interfaces detected')

    def testCorrectlyGeneratedInterfaceEntries(self):
        reverseJava: JavaReader = self._createReversedOglClasses()

        reversedClasses: ReversedClasses = reverseJava.reversedClasses
        interfaceMap:    InterfaceMap    = reverseJava.interfaceMap

        self._checkInterface(reversedClasses, interfaceMap, TEST_INTERFACE_NAME_1)
        self._checkInterface(reversedClasses, interfaceMap, TEST_INTERFACE_NAME_2)
        self._checkInterface(reversedClasses, interfaceMap, TEST_INTERFACE_NAME_3)

    def testCorrectlyGeneratedImplementors(self):

        reverseJava: JavaReader = self._createReversedOglClasses()

        reversedClasses: ReversedClasses = reverseJava.reversedClasses
        interfaceMap:    InterfaceMap    = reverseJava.interfaceMap

        self._checkImplementors(interfaceMap, reversedClasses, TEST_INTERFACE_NAME_1, TEST_BASE_CLASS_NAME)
        self._checkImplementors(interfaceMap, reversedClasses, TEST_INTERFACE_NAME_2, TEST_BASE_CLASS_NAME)
        self._checkImplementors(interfaceMap, reversedClasses, TEST_INTERFACE_NAME_3, 'Feature')

    def _createReversedOglClasses(self) -> JavaReader:

        fileNames: List[str] = [f'{TEST_BASE_CLASS_NAME}.java', 'Feature.java', f'{TEST_INTERFACE_NAME_2}.java',
                                f'{TEST_INTERFACE_NAME_1}.java',
                                f'{TEST_INTERFACE_NAME_3}.java', 'Tenant.java', 'User.java'
                                ]
        javaReader: JavaReader = JavaReader()
        for fileName in fileNames:
            testFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME, fileName)

            javaReader.parseFile(testFileName)

        return javaReader

    def _checkInterface(self, reversedClasses, interfaceMap, interfaceName: str):

        interfaces = interfaceMap.keys()

        interfaceClass: OglClass = reversedClasses[interfaceName]
        self.assertIn(interfaceClass, interfaces)

    def _checkImplementors(self, interfaceMap, reversedClasses, interfaceName, implementorName):

        interfaceClass:    OglClass     = reversedClasses[interfaceName]
        implementingClass: OglClass     = reversedClasses[implementorName]
        implementors:      Implementors = interfaceMap[interfaceClass]

        self.assertIn(implementingClass, implementors)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestJavaReader))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
