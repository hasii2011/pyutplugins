
from typing import Dict
from typing import List
from typing import NewType

from unittest import TestSuite
from unittest import main as unitTestMain

from antlr4 import CommonTokenStream
from antlr4 import FileStream
from antlr4.error.ErrorListener import ConsoleErrorListener

from codeallybasic.UnitTestBase import UnitTestBase

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from pyutplugins.ioplugins.python.pythonpegparser.PythonLexer import PythonLexer
from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser

from pyutplugins.ioplugins.python.PyutPythonPegVisitor import ParentName
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import PyutPythonPegVisitor
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import PyutClassName
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import PyutClasses

from tests.ProjectTestBase import TestBase

PyutMethodHashIndex = NewType('PyutMethodHashIndex', Dict[str, PyutMethod])


class PythonErrorListener(ConsoleErrorListener):
    pass


class TestPyutPythonPegVisitor(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo - Humberto A. Sanchez II
        Generated: 21 January 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testRetrieveClassNames(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('AssociationClasses.py')
        visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

        visitor.visit(tree)
        #
        # 3 regular and 2 synthetic classes
        #
        self.assertEqual(5, len(visitor.pyutClasses), 'Oops class names parsed, mismatch')

    def testMultiClassFileWithInheritance(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('Opie.py')
        visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

        visitor.visit(tree)

        expectedParentName: str = 'Cat'
        expectedChildName:  str = 'Opie'

        self.assertTrue(expectedParentName in visitor.parents, 'Missing parent')

        actualChildName: str = visitor.parents[ParentName(expectedParentName)][0]

        self.assertEqual(expectedChildName, actualChildName, 'Missing child')

    def testMultipleInheritanceClass(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('MultipleInheritance.py')
        visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

        visitor.visit(tree)

        self.logger.info(f'{visitor.parents=}')

        expectedParentName1: str = 'Car'
        expectedParentName2: str = 'Flyable'

        self.assertTrue(expectedParentName1 in visitor.parents, f'Missing parent: {expectedParentName1}')
        self.assertTrue(expectedParentName2 in visitor.parents, f'Missing parent: {expectedParentName2}')

    def testMultipleInheritanceWithMetaClass(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('MultipleInheritanceWithMetaClass.py')
        visitor: PyutPythonPegVisitor           = PyutPythonPegVisitor()

        visitor.visit(tree)

        expectedParentName1: str = 'BaseWxCommand'
        expectedParentName2: str = 'MyMetaBaseWxCommand'

        self.assertTrue(expectedParentName1 in visitor.parents, f'Missing parent: {expectedParentName1}')
        self.assertTrue(expectedParentName2 in visitor.parents, f'Missing parent: {expectedParentName2}')

    def testClassMethods(self):

        visitor: PyutPythonPegVisitor = self._setupSimpleClassVisitor()

        className:   PyutClassName = PyutClassName('SimpleClass')
        pyutClasses: PyutClasses = visitor.pyutClasses

        pyutClass:   PyutClass   = pyutClasses[className]
        pyutMethods: PyutMethods = pyutClass.methods

        methodNames: List[str] = []

        for method in pyutMethods:
            methodNames.append(method.name)

        self.assertIn('simpleMethod', methodNames, 'Missing known method')
        self.assertIn('methodWithParametersAndDefaultValues', methodNames, 'Missing known method')

    def testClassParsed(self):

        visitor: PyutPythonPegVisitor = self._setupSimpleClassVisitor()

        pyutClasses: PyutClasses = visitor.pyutClasses

        classNames = pyutClasses.keys()
        self.assertIn('SimpleClass', classNames, 'Missing class name')

    def testCorrectMethodCount(self):

        visitor: PyutPythonPegVisitor = self._setupSimpleClassVisitor()

        className:   PyutClassName = PyutClassName('SimpleClass')
        pyutClasses: PyutClasses = visitor.pyutClasses

        pyutClass:   PyutClass   = pyutClasses[className]
        pyutMethods: PyutMethods = pyutClass.methods

        self.assertEqual(10, len(pyutMethods), 'Mismatch in number of methods parsed')

    def testProtectedMethodVisibility(self):
        self._runVisibilityTest('_protectedMethod', PyutVisibility.PROTECTED)

    def testPrivateMethodVisibility(self):
        self._runVisibilityTest('__privateMethod', PyutVisibility.PRIVATE)

    def testDunderMethodVisibility(self):
        self._runVisibilityTest('__str__', PyutVisibility.PUBLIC)

    def testClassWithProperties(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('ClassWithProperties.py')
        visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

        visitor.visit(tree)

        className: PyutClassName = PyutClassName('ClassWithProperties')
        pyutClass: PyutClass = visitor.pyutClasses[className]

        self.assertEqual(2, len(pyutClass.fields), 'Not enough properties converted to fields')

    def testSynthesizeType(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('AssociationClasses.py')
        visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

        visitor.visit(tree)

        pyutClasses: PyutClasses = visitor.pyutClasses

        classNames = pyutClasses.keys()
        self.assertIn('Pages',    classNames, 'Missing `Pages` class name')
        self.assertIn('Chapters', classNames, 'Missing `Chapters` class name')

    def _runVisibilityTest(self, methodName, visibility: PyutVisibility):

        visitor: PyutPythonPegVisitor = self._setupSimpleClassVisitor()

        className:   PyutClassName  = PyutClassName('SimpleClass')
        pyutClasses: PyutClasses = visitor.pyutClasses

        pyutClass:   PyutClass   = pyutClasses[className]

        methodDict: PyutMethodHashIndex = self._buildMethodHashIndex(pyutMethods=pyutClass.methods)
        testMethod: PyutMethod          = methodDict[methodName]

        self.assertEqual(visibility, testMethod.visibility, 'Method visibility is incorrect')

    def _setupSimpleClassVisitor(self) -> PyutPythonPegVisitor:

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('SimpleClass.py')
        visitor: PyutPythonPegVisitor           = PyutPythonPegVisitor()

        visitor.visit(tree)

        return visitor

    # def testExtractMethodCode(self):
    #     tree:    PythonParser.File_inputContext = self._setupVisitor('Vertex.py')
    #     visitor: PyutPythonPegVisitor           = PyutPythonPegVisitor()
    #
    #     visitor.visit(tree)
    #
    #     parsedClasses: ParsedClasses = visitor.parsedClasses
    #
    #     className: PyutClassName = PyutClassName('Vertex')
    #     self.assertIn('Vertex', parsedClasses, 'Yikes missed the entire class')
    #
    #     parsedClass: ParsedClass = parsedClasses[className]
    #
    #     self.assertEqual(3, len(parsedClass.methodNames), 'Mismatch on names')
    #     self.assertEqual(3, len(parsedClass.methodCode),  'Mismatch on code')
    #
    #     codeLines: CodeLines = parsedClass.methodCode['surround_half_edges']
    #
    #     self.assertEqual(5, len(codeLines), 'Number of code lines mismatch')
    #
    def _setupPegBasedParser(self, fileName: str) -> PythonParser.File_inputContext:

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_CLASSES_PACKAGE_NAME, fileName)

        fileStream: FileStream  = FileStream(fqFileName)
        lexer:      PythonLexer = PythonLexer(fileStream)

        stream: CommonTokenStream = CommonTokenStream(lexer)
        parser: PythonParser      = PythonParser(stream)

        parser.removeParseListeners()
        parser.addErrorListener(PythonErrorListener())

        tree: PythonParser.File_inputContext = parser.file_input()
        if parser.getNumberOfSyntaxErrors() != 0:
            self.logger.error(f'File contains {parser.getNumberOfSyntaxErrors()} syntax errors')
            self.assertTrue(False, f'File contains {parser.getNumberOfSyntaxErrors()} syntax errors')

        return tree

    def _buildMethodHashIndex(self, pyutMethods: PyutMethods) -> PyutMethodHashIndex:

        methodDict: PyutMethodHashIndex = PyutMethodHashIndex({})
        for method in pyutMethods:
            methodDict[method.name] = method

        return methodDict


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPyutPythonPegVisitor))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
