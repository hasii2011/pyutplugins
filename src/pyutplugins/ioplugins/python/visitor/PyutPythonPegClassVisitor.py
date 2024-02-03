
from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClassName
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClasses
from pyutplugins.ioplugins.python.visitor.ParserTypes import VERSION

from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser

from pyutplugins.ioplugins.python.visitor.PyutBaseVisitor import PyutBaseVisitor


class PyutPythonPegClassVisitor(PyutBaseVisitor):
    """
    Simply does a scan to identify all the classes;   A separate
    is needed to do inheritance
    """

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutClasses:  PyutClasses = PyutClasses({})
        # self._parents:      Parents     = Parents({})
        # self._propertyMap:  PropertyMap = PropertyMap({})

    @property
    def pyutClasses(self) -> PyutClasses:
        return self._pyutClasses

    @pyutClasses.setter
    def pyutClasses(self, pyutClasses: PyutClasses):
        self._pyutClasses = pyutClasses

    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        """
        Visit a parse tree produced by PythonParser#class_def.

        Args:
            ctx:

        """
        className: PyutClassName = self._extractClassName(ctx=ctx)

        pyutClass: PyutClass = PyutClass(name=className)
        pyutClass.description = self._generateMyCredits()

        self._pyutClasses[className] = pyutClass

        return self.visitChildren(ctx)

    def visitPrimary(self, ctx: PythonParser.PrimaryContext):
        """
        Visit a parse tree produced by PythonParser#primary.
        Args:
            ctx:

        """
        primaryStr: str = ctx.getText()
        if primaryStr.startswith('NewType'):
            argumentsCtx: PythonParser.ArgumentsContext = ctx.arguments()
            if argumentsCtx is not None:

                argStr = ctx.children[2].getText()
                typeValueList = argStr.split(',')
                self.logger.debug(f'{typeValueList=}')

                className = typeValueList[0].strip("'").strip('"')
                self.logger.debug(f'{className}')

                pyutClass: PyutClass = PyutClass(name=className)

                pyutClass.description = self._generateMyCredits()
                pyutClass.stereotype  = PyutStereotype.TYPE

                self._pyutClasses[className] = pyutClass

        return self.visitChildren(ctx)

    def _generateMyCredits(self) -> str:
        """

        Returns:    Reversed Engineered by the one and only:
                    Gato Malo - Humberto A. Sanchez II
                    Generated: ${DAY} ${MONTH_NAME_FULL} ${YEAR}
                    Version: ${VERSION}

        """
        from datetime import date

        today: date = date.today()
        formatDated: str = today.strftime('%d %B %Y')

        hasiiCredits: str = (
            f'Reversed Engineered by the one and only:{osLineSep}'
            f'Gato Malo - Humberto A. Sanchez II{osLineSep}'
            f'Generated: {formatDated}{osLineSep}'
            f'Version: {VERSION}'
        )

        return hasiiCredits
