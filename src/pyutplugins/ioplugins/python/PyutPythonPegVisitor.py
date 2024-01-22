
from typing import Dict
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger
from typing import cast

from antlr4.tree.Tree import TerminalNodeImpl

from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser

from pyutplugins.ioplugins.python.pythonpegparser.PythonParserVisitor import PythonParserVisitor

ClassName    = NewType('ClassName',  str)
MethodName   = NewType('MethodName', str)
PropertyName = NewType('PropertyName', str)
ParentName   = NewType('ParentName', str)
ChildName    = NewType('ChildName',  str)

ClassNames    = NewType('ClassNames',    List[ClassName])
MethodNames   = NewType('MethodNames',   List[MethodName])

Children   = List[Union[ClassName, ChildName]]

Parents       = NewType('Parents',       Dict[ParentName,   Children])
Methods       = NewType('Methods',       Dict[ClassName,    MethodNames])
PropertyNames = NewType('PropertyNames', Dict[PropertyName, ClassName])

NO_CLASS_NAME: ClassName = ClassName('')


class PyutPythonPegVisitor(PythonParserVisitor):
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._classNames:   ClassNames = ClassNames([])
        self._classMethods: Methods    = Methods({})

        self._parents:       Parents       = Parents({})
        self._propertyNames: PropertyNames = PropertyNames({})

    @property
    def classNames(self) -> ClassNames:
        return self._classNames

    @property
    def classMethods(self) -> Methods:
        return self._classMethods

    @property
    def parents(self) -> Parents:
        return self._parents

    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        """
        Visit a parse tree produced by PythonParser#class_def.

        Args:
            ctx:

        """

        # child:     PythonParser.Class_def_rawContext = ctx.class_def_raw()
        # name:      TerminalNodeImpl                  = child.NAME()
        className: ClassName = self._extractClassName(ctx=ctx)

        self._classNames.append(className)
        self.logger.debug(f'visitClassdef: Visited class: {className}')

        argumentsCtx: PythonParser.ArgumentsContext = self._findArgListContext(ctx)
        if argumentsCtx is not None:
            self._createParentChildEntry(argumentsCtx, className)

        return super().visitChildren(ctx)

    def visitFunction_def(self, ctx: PythonParser.Function_defContext):
        """
        Visit a parse tree produced by PythonParser#function_def.

        Args:
            ctx:
        """
        className = self._checkIfMethodBelongsToClass(ctx, PythonParser.Class_defContext)
        if className != NO_CLASS_NAME:

            methodName = self._extractMethodName(ctx=ctx.function_def_raw())

            if not self._isProperty(methodName):
                self.logger.debug(f'visitFunction_def: {methodName=}')
                if className not in self.classMethods:
                    self.classMethods[className] = MethodNames([methodName])
                else:
                    self.classMethods[className].append(methodName)

                # self.__getMethodCode(methodName, ctx)

        return super().visitChildren(ctx)

    def _findArgListContext(self, ctx: PythonParser.Class_defContext) -> PythonParser.ArgumentsContext:

        argumentsCtx: PythonParser.ArgumentsContext = cast(PythonParser.ArgumentsContext, None)

        classDefRawContext: PythonParser.Class_def_rawContext = ctx.class_def_raw()
        for childCtx in classDefRawContext.children:
            if isinstance(childCtx, PythonParser.ArgumentsContext):
                argumentsCtx = childCtx
                break

        return argumentsCtx

    def _createParentChildEntry(self, argumentsCtx: PythonParser.ArgumentsContext, childName: Union[ClassName, ChildName]):

        args:       PythonParser.ArgsContext = argumentsCtx.args()
        parentName: ParentName               = ParentName(args.getText())
        self.logger.info(f'Class: {childName} is subclass of {parentName}')

        multiParents = parentName.split(',')
        if len(multiParents) > 1:
            self._handleMultiParentChild(multiParents=multiParents, childName=childName)
        else:
            self._updateParentsDictionary(parentName=parentName, childName=childName)

    def _handleMultiParentChild(self, multiParents: List[str], childName: Union[ClassName, ChildName]):
        """

        Args:
            multiParents:
            childName:

        """
        self.logger.info(f'handleMultiParentChild: {childName} -- {multiParents}')
        for parent in multiParents:
            # handle the special case
            if parent.startswith('metaclass'):
                splitParent: List[str] = parent.split('=')
                parentName: ParentName = ParentName(splitParent[1])
                self._updateParentsDictionary(parentName=parentName, childName=childName)
            else:
                parentName = ParentName(parent)
                self._updateParentsDictionary(parentName=parentName, childName=childName)

    def _updateParentsDictionary(self, parentName: ParentName, childName: Union[ClassName, ChildName]):
        """
        Update our dictionary of parents.  If the parent dictionary
        does not have an entry, create one with the single child.

        Args:
            parentName:     Prospective parent
            childName:      Child class name

        """

        if parentName in self._parents:
            children: Children = self._parents[parentName]
            children.append(childName)
        else:
            children = [childName]

        self._parents[parentName] = children

    def _checkIfMethodBelongsToClass(self, node: PythonParser.Function_defContext, classType) -> ClassName:

        while node.parentCtx:
            if isinstance(node, classType):
                return self._extractClassName(ctx=node)
            node = node.parentCtx

        return NO_CLASS_NAME

    def _isProperty(self, methodName: MethodName) -> bool:
        """
        Used by the function definition visitor to determine if the method name that is being
        visited has been marked as a property.

        Args:
            methodName:  The method name to check

        Returns: True if it is in our known list of property names
        """
        ans: bool = False

        propertyName: PropertyName = PropertyName(methodName)
        if propertyName in self._propertyNames:
            ans = True

        return ans

    def _extractClassName(self, ctx: PythonParser.Class_defContext) -> ClassName:

        child:     PythonParser.Class_def_rawContext = ctx.class_def_raw()
        name:      TerminalNodeImpl                  = child.NAME()
        className: ClassName                         = name.getText()

        return className

    def _extractMethodName(self, ctx: PythonParser.Function_def_rawContext) -> MethodName:

        name:       TerminalNodeImpl = ctx.NAME()
        methodName: MethodName       = MethodName(name.getText())

        return methodName
