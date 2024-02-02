
from unittest import TestSuite
from unittest import main as unitTestMain

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from antlr4.error.ErrorListener import ConsoleErrorListener

from codeallybasic.UnitTestBase import UnitTestBase

from pyutplugins.ioplugins.python.pythonpegparser.PythonLexer import PythonLexer
from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser

from pyutplugins.ioplugins.python.visitor.ParserTypes import ParentName
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClasses

from pyutplugins.ioplugins.python.visitor.PyutPythonPegClassVisitor import PyutPythonPegClassVisitor

from tests.ProjectTestBase import TestBase


class PythonErrorListener(ConsoleErrorListener):
    pass


class TestPyutPythonPegClassVisitor(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo - Humberto A. Sanchez II
        Generated: 01 February 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testClassParsed(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('SimpleClass.py')
        visitor: PyutPythonPegClassVisitor      = PyutPythonPegClassVisitor()

        visitor.visit(tree)

        pyutClasses: PyutClasses = visitor.pyutClasses
        classNames = pyutClasses.keys()
        self.assertIn('SimpleClass', classNames, 'Missing class name')

    def testRetrieveClassNames(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('AssociationClasses.py')
        visitor: PyutPythonPegClassVisitor      = PyutPythonPegClassVisitor()

        visitor.visit(tree)
        #
        # 3 regular and 2 synthetic classes
        #
        self.assertEqual(5, len(visitor.pyutClasses), 'Oops class names parsed, mismatch')

    def testMultiClassFileWithInheritance(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('Opie.py')
        visitor: PyutPythonPegClassVisitor = PyutPythonPegClassVisitor()

        visitor.visit(tree)

        expectedParentName: str = 'Cat'
        expectedChildName:  str = 'Opie'

        self.assertTrue(expectedParentName in visitor.parents, 'Missing parent')

        actualChildName: str = visitor.parents[ParentName(expectedParentName)][0]

        self.assertEqual(expectedChildName, actualChildName, 'Missing child')

    def testMultipleInheritanceClass(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('MultipleInheritance.py')
        visitor: PyutPythonPegClassVisitor = PyutPythonPegClassVisitor()

        visitor.visit(tree)

        self.logger.info(f'{visitor.parents=}')

        expectedParentName1: str = 'Car'
        expectedParentName2: str = 'Flyable'

        self.assertTrue(expectedParentName1 in visitor.parents, f'Missing parent: {expectedParentName1}')
        self.assertTrue(expectedParentName2 in visitor.parents, f'Missing parent: {expectedParentName2}')

    def testMultipleInheritanceWithMetaClass(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('MultipleInheritanceWithMetaClass.py')
        visitor: PyutPythonPegClassVisitor      = PyutPythonPegClassVisitor()

        visitor.visit(tree)

        expectedParentName1: str = 'BaseWxCommand'
        expectedParentName2: str = 'MyMetaBaseWxCommand'

        self.assertTrue(expectedParentName1 in visitor.parents, f'Missing parent: {expectedParentName1}')
        self.assertTrue(expectedParentName2 in visitor.parents, f'Missing parent: {expectedParentName2}')

    def testSynthesizeType(self):

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser('AssociationClasses.py')
        visitor: PyutPythonPegClassVisitor = PyutPythonPegClassVisitor()

        visitor.visit(tree)

        pyutClasses: PyutClasses = visitor.pyutClasses

        classNames = pyutClasses.keys()
        self.assertIn('Pages',    classNames, 'Missing `Pages` class name')
        self.assertIn('Chapters', classNames, 'Missing `Chapters` class name')

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


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPyutPythonPegClassVisitor))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
