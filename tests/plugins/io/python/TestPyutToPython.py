
from typing import cast
from typing import List

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from unittest import TestSuite
from unittest import main as unitTestMain


from pyutmodel.PyutType import PyutType
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from plugins.ioplugins.python.PyutToPython import PyutToPython

from tests.TestBase import TestBase


class TestPyutToPython(TestBase):
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestPyutToPython.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger:       Logger       = TestPyutToPython.clsLogger
        self.pyutToPython: PyutToPython = PyutToPython()

    def tearDown(self):
        pass

    def testGetPublicFieldPythonCode(self):

        pyutType: PyutType = PyutType(value='')
        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("publicField", pyutType, '', PyutVisibilityEnum.PUBLIC))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.publicField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{s}`')

    def testGetPrivateFieldPythonCode(self):

        pyutType: PyutType = PyutType(value='')

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("privateField", pyutType, '', PyutVisibilityEnum.PRIVATE))

        unExpectedValue: int = -1
        actualValue:     int = s.find('self.__privateField')
        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{s}`')

    def testGetProtectedFieldPythonCode(self):

        pyutType: PyutType = PyutType(value='')

        s: str = self.pyutToPython.generateFieldPythonCode(PyutField("protectedField", pyutType, '', PyutVisibilityEnum.PROTECTED))

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
        publicMethod: PyutMethod = PyutMethod(name='publicMethod', visibility=PyutVisibilityEnum.PUBLIC, returnType=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def publicMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate public method correctly: `{defCode}`')

    def testGetOneMethodCodePrivate(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='privateMethod', visibility=PyutVisibilityEnum.PRIVATE, returnType=pyutType)

        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(publicMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        unExpectedValue: int = -1
        actualValue:     int = defCode.__contains__('def __privateMethod')

        self.assertNotEqual(unExpectedValue, actualValue, f'Did not code generate private method correctly: `{defCode}`')

    def testGetOneMethodCodeProtected(self):

        pyutType: PyutType = PyutType(value='str')
        publicMethod: PyutMethod = PyutMethod(name='protectedMethod', visibility=PyutVisibilityEnum.PROTECTED, returnType=pyutType)

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
        dunderMethod: PyutMethod = PyutMethod(name='__hash__', visibility=PyutVisibilityEnum.PUBLIC)
        defCode: List[str] = self.pyutToPython.generateASingleMethodsCode(dunderMethod, writePass=False)
        self.logger.info(f'Generated definition: {defCode}')
        expectedDeclaration: str = f'def __hash__(self):{osLineSep}'
        self.assertEqual(expectedDeclaration, defCode[0], 'Code generation must have changed')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestPyutToPython))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
