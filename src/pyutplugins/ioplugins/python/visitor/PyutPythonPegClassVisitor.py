from typing import List
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype

from pyutplugins.ioplugins.python.visitor.ParserTypes import ChildName
from pyutplugins.ioplugins.python.visitor.ParserTypes import Children
from pyutplugins.ioplugins.python.visitor.ParserTypes import ParentName
from pyutplugins.ioplugins.python.visitor.ParserTypes import Parents
from pyutplugins.ioplugins.python.visitor.ParserTypes import PropertyMap

from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClassName
from pyutplugins.ioplugins.python.visitor.ParserTypes import PyutClasses

from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser

from pyutplugins.ioplugins.python.visitor.ParserTypes import VERSION
from pyutplugins.ioplugins.python.visitor.PyutBaseVisitor import PyutBaseVisitor


class PyutPythonPegClassVisitor(PyutBaseVisitor):

    def __init__(self):
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._pyutClasses:  PyutClasses = PyutClasses({})
        self._parents:      Parents     = Parents({})
        self._propertyMap:  PropertyMap = PropertyMap({})

    @property
    def pyutClasses(self) -> PyutClasses:
        return self._pyutClasses

    @property
    def parents(self) -> Parents:
        return self._parents

    @parents.setter
    def parents(self, newValue: Parents):
        self._parents = newValue

    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        """
        Visit a parse tree produced by PythonParser#class_def.

        Args:
            ctx:

        """
        className: PyutClassName = self._extractClassName(ctx=ctx)

        self.logger.debug(f'visitClassdef: Visited class: {className}')

        argumentsCtx: PythonParser.ArgumentsContext = self._findArgListContext(ctx)
        if argumentsCtx is not None:
            self._createParentChildEntry(argumentsCtx, className)

        pyutClass: PyutClass = PyutClass(name=className)
        pyutClass.description = self._generateMyCredits()

        self._pyutClasses[className] = pyutClass
        #
        # Make an entry for this guy's properties
        #
        # self._propertyMap[className] = PropertyNames([])

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

    def _findArgListContext(self, ctx: PythonParser.Class_defContext) -> PythonParser.ArgumentsContext:

        argumentsCtx: PythonParser.ArgumentsContext = cast(PythonParser.ArgumentsContext, None)

        classDefRawContext: PythonParser.Class_def_rawContext = ctx.class_def_raw()
        for childCtx in classDefRawContext.children:
            if isinstance(childCtx, PythonParser.ArgumentsContext):
                argumentsCtx = childCtx
                break

        return argumentsCtx

    def _createParentChildEntry(self, argumentsCtx: PythonParser.ArgumentsContext, childName: Union[PyutClassName, ChildName]):

        args:       PythonParser.ArgsContext = argumentsCtx.args()
        parentName: ParentName               = ParentName(args.getText())
        self.logger.debug(f'Class: {childName} is subclass of {parentName}')

        multiParents = parentName.split(',')
        if len(multiParents) > 1:
            self._handleMultiParentChild(multiParents=multiParents, childName=childName)
        else:
            self._updateParentsDictionary(parentName=parentName, childName=childName)

    def _handleMultiParentChild(self, multiParents: List[str], childName: Union[PyutClassName, ChildName]):
        """

        Args:
            multiParents:
            childName:

        """
        self.logger.debug(f'handleMultiParentChild: {childName} -- {multiParents}')
        for parent in multiParents:
            # handle the special case
            if parent.startswith('metaclass'):
                splitParent: List[str] = parent.split('=')
                parentName: ParentName = ParentName(splitParent[1])
                self._updateParentsDictionary(parentName=parentName, childName=childName)
            else:
                parentName = ParentName(parent)
                self._updateParentsDictionary(parentName=parentName, childName=childName)

    def _updateParentsDictionary(self, parentName: ParentName, childName: Union[PyutClassName, ChildName]):
        """
        Update our dictionary of parents. If the parent dictionary
        does not have an entry, create one with the single child.

        Args:
            parentName:     The prospective parent
            childName:      Child class name

        """

        if parentName in self._parents:
            children: Children = self._parents[parentName]
            children.append(childName)
        else:
            children = [childName]

        self._parents[parentName] = children

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
