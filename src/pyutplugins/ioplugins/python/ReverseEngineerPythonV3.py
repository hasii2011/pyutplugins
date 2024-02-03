
from typing import Callable
from typing import Dict
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import sep as osSep
from os import linesep as osLineSep

from antlr4 import CommonTokenStream
from antlr4 import FileStream

from antlr4.error.ErrorListener import ErrorListener

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks

from pyutplugins.common.LinkMakerMixin import LinkMakerMixin

from pyutplugins.ioplugins.python.PythonParseException import PythonParseException

from pyutplugins.ioplugins.python.visitor.ParserTypes import Associates
from pyutplugins.ioplugins.python.visitor.ParserTypes import AssociationType
from pyutplugins.ioplugins.python.visitor.ParserTypes import Associations
from pyutplugins.ioplugins.python.visitor.ParserTypes import ChildName
from pyutplugins.ioplugins.python.visitor.ParserTypes import Children
from pyutplugins.ioplugins.python.visitor.ParserTypes import ParentName
from pyutplugins.ioplugins.python.visitor.ParserTypes import Parents
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClassName
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClasses
from pyutplugins.ioplugins.python.visitor.PyutPythonPegClassVisitor import PyutPythonPegClassVisitor

from pyutplugins.ioplugins.python.visitor.PyutPythonPegVisitor import PyutPythonPegVisitor

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
        eMsg: str = f'{line=}{osLineSep}{column=}{osLineSep}{msg}'
        raise PythonParseException(eMsg)


class ReverseEngineerPythonV3(LinkMakerMixin):

    def __init__(self):

        super().__init__()

        self.logger: Logger = getLogger(__name__)

        self._oglClassesDict: OglClassesDict  = OglClassesDict({})
        self._oglClasses:     OglClasses      = OglClasses([])
        self._oglLinks:       OglLinks        = OglLinks([])

        self._cumulativePyutClasses:  PyutClasses     = PyutClasses({})
        self._cumulativeParents:      Parents       = Parents({})
        self._cumulativeAssociations: Associations  = Associations({})

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

                updatedCumulativePyutClasses: PyutClasses = self._do1stPassPegBasedParser(fileName=fqFileName, cumulativePyutClasses=self._cumulativePyutClasses)

                self._cumulativePyutClasses = updatedCumulativePyutClasses

                visitor: PyutPythonPegVisitor = PyutPythonPegVisitor()

                visitor.pyutClasses  = self._cumulativePyutClasses
                visitor.parents      = self._cumulativeParents
                visitor.associations = self._cumulativeAssociations
                visitor.visit(tree)

                self._cumulativeParents      = visitor.parents
                self._cumulativeAssociations = visitor.associations

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

        self._generateInheritanceLinks(oglClassesDict)
        self._generateAssociationLinks(oglClassesDict)

    def _generateInheritanceLinks(self, oglClassesDict: OglClassesDict):

        parents: Parents = self._cumulativeParents

        for parentName in parents.keys():
            children: Children = parents[parentName]

            for childName in children:

                try:
                    parentOglClass: OglClass = oglClassesDict[parentName]
                    childOglClass:  OglClass = oglClassesDict[childName]
                    oglLink:        OglLink  = self.createLink(src=childOglClass, dst=parentOglClass, linkType=PyutLinkType.INHERITANCE)

                    self._oglLinks.append(oglLink)
                except KeyError as ke:  # Probably there is no parent we are tracking
                    self.logger.warning(f'Apparently we are not tracking this parent:  {ke}')
                    continue

    def _generateAssociationLinks(self, oglClassesDict: OglClassesDict):

        associations: Associations = self._cumulativeAssociations
        for className in associations:

            pyutClassName: PyutClassName = cast(PyutClassName, className)
            associates:    Associates    = associations[pyutClassName]

            for associate in associates:
                sourceClass:      OglClass = oglClassesDict[pyutClassName]
                destinationClass: OglClass = oglClassesDict[associate.associateName]

                pyutLinkType: PyutLinkType = self._toPyutLinkType(associationType=associate.associationType)
                oglLink: OglLink = self.createLink(src=sourceClass, dst=destinationClass, linkType=pyutLinkType)

                self._oglLinks.append(oglLink)

    def _generateOglClasses(self):

        for pyutClassName in self._cumulativePyutClasses:
            try:
                pyutClass: PyutClass = self._cumulativePyutClasses[pyutClassName]
                oglClass:  OglClass  = OglClass(pyutClass)

                self._oglClassesDict[pyutClassName] = oglClass

            except (ValueError, Exception) as e:
                self.logger.error(f"Error while creating class {pyutClassName},  {e}")

    def _toPyutLinkType(self, associationType: AssociationType) -> PyutLinkType:

        match associationType:
            case AssociationType.ASSOCIATION:
                pyutLinkType: PyutLinkType = PyutLinkType.ASSOCIATION
            case AssociationType.AGGREGATION:
                pyutLinkType = PyutLinkType.AGGREGATION
            case AssociationType.COMPOSITION:
                pyutLinkType = PyutLinkType.COMPOSITION
            case _:
                assert False, f'Unknown association type: {associationType.name}'

        return pyutLinkType

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

    def _do1stPassPegBasedParser(self, fileName: str, cumulativePyutClasses: PyutClasses) -> PyutClasses:

        tree:    PythonParser.File_inputContext = self._setupPegBasedParser(fqFileName=fileName)
        visitor: PyutPythonPegClassVisitor      = PyutPythonPegClassVisitor()

        visitor.pyutClasses = cumulativePyutClasses
        visitor.visit(tree)

        return visitor.pyutClasses
