
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from antlr4.error.ErrorListener import ErrorListener

from pyutmodelv2.PyutClass import PyutClass

from ogl.OglClass import OglClass

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks

from pyutplugins.common.LinkMakerMixin import LinkMakerMixin

from pyutplugins.ioplugins.python.PythonParseException import PythonParseException

from pyutplugins.ioplugins.python.PyutPythonPegVisitor import ChildName
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import ParentName
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import Parents
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import PyutClassName
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import PyutClasses
from pyutplugins.ioplugins.python.PyutPythonPegVisitor import PyutPythonPegVisitor

from pyutplugins.ioplugins.python.pythonpegparser.PythonLexer import PythonLexer
from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser


OglClassesDict = NewType('OglClassesDict', Dict[Union[PyutClassName, ParentName, ChildName], OglClass])


class PythonErrorListener(ErrorListener):
    #
    # Provides a default instance of {@link ConsoleErrorListener}.
    #
    # INSTANCE = None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):

        # print("line " + str(line) + ":" + str(column) + " " + msg, file=sys.stderr)
        eMsg: str = f'{line=}: {column=} {msg}'
        raise PythonParseException(eMsg)


class ReverseEngineerPythonV3(LinkMakerMixin):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._pyutClasses:    PyutClasses     = PyutClasses({})
        self._oglClassesDict: OglClassesDict  = OglClassesDict({})
        self._oglClasses:     OglClasses      = OglClasses([])
        self._oglLinks:       OglLinks        = OglLinks([])
        self._onGoingParents: Parents         = Parents({})

    def reversePython(self,  directoryName: str, files: List[str], progressCallback: Callable):
        """
        Reverse engineering Python files to OglClass's

        Args:
            directoryName:  The directory name where the selected files reside
            files:          A list of files to parse
            progressCallback: The method to call to report progress
        """
        currentFileCount: int = 0
        for fileName in files:

            try:
                fqFileName: str = f'{directoryName}{osSep}{fileName}'
                self.logger.info(f'Processing file: {fqFileName}')

                progressCallback(currentFileCount, f'Processing: {directoryName}\n {fileName}')

                tree:    PythonParser.File_inputContext = self._setupPegBasedParser(fqFileName=fqFileName)
                if tree is None:
                    continue

                visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

                visitor.parents = self._onGoingParents

                visitor.visit(tree)

                self._pyutClasses = PyutClasses(self._pyutClasses | visitor.pyutClasses)

                self._onGoingParents = visitor.parents

            except (ValueError, Exception) as e:
                self.logger.error(e)
                raise PythonParseException(e)

        self._generateOglClasses()

    @property
    def oglClasses(self) -> OglClassesDict:
        return self._oglClassesDict

    @property
    def oglLinks(self) -> OglLinks:
        return self._oglLinks

    def generateLinks(self, oglClassesDict: OglClassesDict):
        pass

    def _generateOglClasses(self):

        for pyutClassName in self._pyutClasses:
            try:
                pyutClass: PyutClass = self._pyutClasses[pyutClassName]
                oglClass:  OglClass  = OglClass(pyutClass)

                self._oglClassesDict[pyutClassName] = oglClass

            except (ValueError, Exception) as e:
                self.logger.error(f"Error while creating class {pyutClassName},  {e}")

    def _setupPegBasedParser(self, fqFileName: str) -> PythonParser.File_inputContext:
        """
        May return None if there are syntax errors in the input file
        In that case the error listener will raise and PythonParseException exception
        with the appropriate detailed error message

        Args:
            fqFileName:

        Returns:  Returns a visitor
        """

        fileStream: FileStream  = FileStream(fqFileName)
        lexer:      PythonLexer = PythonLexer(fileStream)

        stream: CommonTokenStream = CommonTokenStream(lexer)
        parser: PythonParser      = PythonParser(stream)

        parser.removeParseListeners()
        parser.addErrorListener(PythonErrorListener())

        tree: PythonParser.File_inputContext = parser.file_input()
        if parser.getNumberOfSyntaxErrors() != 0:
            eMsg: str = f"File {fqFileName} contains {parser.getNumberOfSyntaxErrors()} syntax errors"
            self.logger.error(eMsg)
            tree = cast(PythonParser.File_inputContext, None)

        return tree
