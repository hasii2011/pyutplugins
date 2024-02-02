
from logging import Logger
from logging import getLogger

from antlr4.tree.Tree import TerminalNodeImpl

from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser
from pyutplugins.ioplugins.python.pythonpegparser.PythonPegParserVisitor import PythonPegParserVisitor

from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClassName


class PyutBaseVisitor(PythonPegParserVisitor):

    def __init__(self):

        self.baseLogger: Logger = getLogger(__name__)

    def _extractClassName(self, ctx: PythonParser.Class_defContext) -> PyutClassName:
        """
        Get a class name from a Class_defContext
        Args:
            ctx:

        Returns:    A class name
        """

        child:     PythonParser.Class_def_rawContext = ctx.class_def_raw()
        name:      TerminalNodeImpl                  = child.NAME()
        className: PyutClassName                     = name.getText()

        return className
