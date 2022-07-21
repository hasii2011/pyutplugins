from time import sleep
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from miniogl.DiagramFrame import DiagramFrame
from pkg_resources import resource_filename

from wx import App

from pyutmodel.ModelTypes import Implementors
from ogl.OglClass import OglClass
from wx import Frame
from wx import ID_ANY

from plugins.io.java.ReverseJava import Extenders
from plugins.io.java.ReverseJava import InterfaceMap
from plugins.io.java.ReverseJava import ReverseJava
from plugins.io.java.ReverseJava import ReversedClasses


from tests.TestBase import TestBase

TEST_BASE_CLASS_NAME:  str = 'BaseModel'
TEST_INTERFACE_NAME_1: str = 'IModified'
TEST_INTERFACE_NAME_2: str = 'ICreated'
TEST_INTERFACE_NAME_3: str = 'Tenancy'


class BogusApp(App):
    def OnInit(self) -> bool:
        return True


class TestReverseJava(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestReverseJava.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger  = TestReverseJava.clsLogger
        self._app:   BogusApp = BogusApp()

        sleep(2)

        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

    def tearDown(self):
        self._app.OnExit()
        del self._app

    def testBasicClass(self):

        reverseJava: ReverseJava = ReverseJava()

        basicClassPath: str = resource_filename(TestBase.RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME, 'Tenant.java')

        reverseJava.parseFile(basicClassPath)

        # 2 because implements BaseModel
        self.assertEqual(2, len(reverseJava.reversedClasses))

    def testCorrectlyGeneratedSingleSubclassMap(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        expectedLength: int = 1
        actualLength:   int = len(reverseJava._subClassMap)
        self.assertEqual(expectedLength, actualLength, "More than one base class")

    def testCorrectlyGeneratedSubClassEntry(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        testBaseClass: OglClass = reverseJava.reversedClasses[TEST_BASE_CLASS_NAME]

        self.assertIn(testBaseClass, reverseJava._subClassMap, 'Not the correct base class')

    def testCorrectlyGeneratedSubClasses(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        testBaseClass: OglClass = reverseJava.reversedClasses[TEST_BASE_CLASS_NAME]

        extenders: Extenders = reverseJava._subClassMap[testBaseClass]

        expectedLength: int = 3     # Because Tenant also extends BaseModel
        actualLength:   int = len(extenders)

        self.assertEqual(expectedLength, actualLength, "Incorrect number of subclasses")

    def testCorrectlyGeneratedInterfaceMap(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        expectedLength: int = 3
        actualLength:   int = len(reverseJava.interfaceMap())
        self.assertEqual(expectedLength, actualLength, 'Incorrect number of interfaces detected')

    def testCorrectlyGeneratedInterfaceEntries(self):
        reverseJava: ReverseJava = self._createReversedOglClasses()

        reversedClasses: ReversedClasses = reverseJava.reversedClasses
        interfaceMap:    InterfaceMap    = reverseJava.interfaceMap()

        self._checkInterface(reversedClasses, interfaceMap, TEST_INTERFACE_NAME_1)
        self._checkInterface(reversedClasses, interfaceMap, TEST_INTERFACE_NAME_2)
        self._checkInterface(reversedClasses, interfaceMap, TEST_INTERFACE_NAME_3)

    def testCorrectlyGeneratedImplementors(self):

        reverseJava: ReverseJava = self._createReversedOglClasses()

        reversedClasses: ReversedClasses = reverseJava.reversedClasses
        interfaceMap:    InterfaceMap    = reverseJava.interfaceMap()

        self._checkImplementors(interfaceMap, reversedClasses, TEST_INTERFACE_NAME_1, TEST_BASE_CLASS_NAME)
        self._checkImplementors(interfaceMap, reversedClasses, TEST_INTERFACE_NAME_2, TEST_BASE_CLASS_NAME)
        self._checkImplementors(interfaceMap, reversedClasses, TEST_INTERFACE_NAME_3, 'Feature')

    def _createReversedOglClasses(self) -> ReverseJava:

        fileNames: List[str] = [f'{TEST_BASE_CLASS_NAME}.java', 'Feature.java', f'{TEST_INTERFACE_NAME_2}.java',
                                f'{TEST_INTERFACE_NAME_1}.java',
                                f'{TEST_INTERFACE_NAME_3}.java', 'Tenant.java', 'User.java'
                                ]
        reverseJava: ReverseJava = ReverseJava()
        for fileName in fileNames:
            testFileName: str = resource_filename(TestBase.RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME, fileName)
            reverseJava.parseFile(testFileName)

        return reverseJava

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
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReverseJava))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
