
from typing import List

from os import linesep as osLineSep

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutMethod import PyutMethod

from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from pyutplugins.ioplugins.python.PyutToPython import PyutToPython


class TestPyutToPython(UnitTestBase):

    def setUp(self):
        super().setUp()
        self.pyutToPython: PyutToPython = PyutToPython()

    def tearDown(self):
        super().tearDown()

    def testGetPublicFieldPythonCode(self):

        pyutType: PyutType = PyutType(value='')
        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("publicField", type=pyutType, defaultValue='', visibility=PyutVisibility.PUBLIC))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.publicField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{s}`')

    def testGetPrivateFieldPythonCode(self):

        pyutType: PyutType = PyutType(value='')

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("privateField", type=pyutType, defaultValue='', visibility=PyutVisibility.PRIVATE))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.__privateField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{s}`')

    def testGetProtectedFieldPythonCode(self):

        pyutType: PyutType = PyutType(value='')

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("protectedField", type=pyutType, defaultValue='', visibility=PyutVisibility.PROTECTED))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self._protectedField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protected field correctly: `{s}`')

    def testIndent(self):

        lst1: List[str] = ['a', '   b', 'c']
        expectedIndent: List[str] = ['    a', '       b', '    c']
        actualIndent: List[str] = self.pyutToPython.indent(lst1)
        self.assertEqual(expectedIndent, actualIndent, 'Indentation failed')

    def testGetOneMethodCodePublic(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='publicMethod', visibility=PyutVisibility.PUBLIC, returnType=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def publicMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{defCode}`')

    def testGetOneMethodCodePrivate(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='privateMethod', visibility=PyutVisibility.PRIVATE, returnType=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def __privateMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{defCode}`')

    def testGetOneMethodCodeProtected(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='protectedMethod', visibility=PyutVisibility.PROTECTED, returnType=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def -protectedMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate protected method correctly: `{defCode}`')

    def testDunderMethods(self):
        """
            def __hash__(self) -> int:
                return hash(self.id)
        """
        # pyutType: PyutType = PyutType(value='str')
        dunderMethod: PyutMethod = PyutMethod(name='__hash__', visibility=PyutVisibility.PUBLIC)
        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(dunderMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        expectedDeclaration: str = f'def __hash__(self):{osLineSep}'
        self.assertEqual(expectedDeclaration, defCode[0], 'Code generation must have changed')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPyutToPython))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
