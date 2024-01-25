from dataclasses import dataclass
from typing import cast
from typing import Dict
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger

from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

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

Parents       = NewType('Parents',       Dict[ParentName, Children])
Methods       = NewType('Methods',       List[MethodNames])

PropertyNames = NewType('PropertyNames', List[PropertyName])
CodeLine      = NewType('CodeLine',      str)
CodeLines     = NewType('CodeLines',     List[CodeLine])
MethodCode    = NewType('MethodCode',    Dict[MethodName,   CodeLines])

NO_CLASS_NAME: ClassName = ClassName('')

NO_METHOD_CTX: PythonParser.AssignmentContext = cast(PythonParser.AssignmentContext, None)


PyutClasses = NewType('PyutClasses', Dict[ClassName, PyutClass])


PARAMETER_SELF:      str = 'self'
PROTECTED_INDICATOR: str = '_'
PRIVATE_INDICATOR:   str = '__'

@dataclass
class ParameterNameAndType:
    name:     str = ''
    typeName: str = ''


class PyutPythonPegVisitor(PythonParserVisitor):
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._parents:       Parents       = Parents({})
        self._pyutClasses:   PyutClasses   = PyutClasses({})

    @property
    def pyutClasses(self) -> PyutClasses:
        return self._pyutClasses

    @property
    def parents(self) -> Parents:
        return self._parents

    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        """
        Visit a parse tree produced by PythonParser#class_def.

        Args:
            ctx:

        """
        className: ClassName = self._extractClassName(ctx=ctx)

        # self._classNames.append(className)
        self.logger.debug(f'visitClassdef: Visited class: {className}')

        argumentsCtx: PythonParser.ArgumentsContext = self._findArgListContext(ctx)
        if argumentsCtx is not None:
            self._createParentChildEntry(argumentsCtx, className)

        self._pyutClasses[className] = PyutClass(name=className)

        return self.visitChildren(ctx)

    def visitFunction_def(self, ctx: PythonParser.Function_defContext):
        """
        Visit a parse tree produced by PythonParser#function_def.

        Args:
            ctx:
        """
        className: ClassName = self._checkIfMethodBelongsToClass(ctx, PythonParser.Class_defContext)
        if className != NO_CLASS_NAME:

            methodName: MethodName = self._extractMethodName(ctx=ctx.function_def_raw())

            exprCtx: PythonParser.ExpressionContext = ctx.function_def_raw().expression()
            if exprCtx is None:
                returnTypeStr: str = ''
            else:
                returnTypeStr = exprCtx.getText()

            pyutVisibility: PyutVisibility = PyutVisibility.PUBLIC
            if methodName.startswith(PROTECTED_INDICATOR):
                pyutVisibility = PyutVisibility.PROTECTED
            elif methodName.startswith(PRIVATE_INDICATOR):
                pyutVisibility = PyutVisibility.PRIVATE

            if not self._isProperty(methodName):
                self.logger.debug(f'visitFunction_def: {methodName=}')
                if className not in self._pyutClasses:
                    assert False, 'This should not happen'
                else:
                    pyutClass:  PyutClass  = self._pyutClasses[className]
                    pyutMethod: PyutMethod = PyutMethod(name=methodName, returnType=PyutType(returnTypeStr), visibility=pyutVisibility)
                    pyutClass.methods.append(pyutMethod)

        return self.visitChildren(ctx)

    def visitParameters(self, ctx: PythonParser.ParametersContext):
        """
        Visit a parse tree produced by PythonParser#parameters.

        parameters
            : slash_no_default param_no_default* param_with_default* star_etc?
            | slash_with_default param_with_default* star_etc?
            | param_no_default+ param_with_default* star_etc?
            | param_with_default+ star_etc?
            | star_etc;

        Args:
            ctx:

        Returns:
        """
        classCtx:  PythonParser.Class_defContext    = self._findClassContext(ctx)
        methodCtx: PythonParser.Function_defContext = self._findMethodContext(ctx)

        className:  ClassName  = self._extractClassName(ctx=classCtx)
        methodName: MethodName = self._extractMethodName(ctx=methodCtx.function_def_raw())

        self.logger.info(f'{className=} {methodName=}')
        noDefaultContexts: List[PythonParser.Param_no_defaultContext]   = ctx.param_no_default()
        defaultContexts:   List[PythonParser.Param_with_defaultContext] = ctx.param_with_default()

        ctx2 = ctx.slash_no_default()
        ctx3 = ctx.slash_with_default()

        if len(defaultContexts) != 0:
            self._handleFullParameters(className=className, methodName=methodName, defaultContexts=defaultContexts)
        elif len(noDefaultContexts) != 0:
            self._handleTypeAnnotated(className=className, methodName=methodName, noDefaultContexts=noDefaultContexts)
        elif ctx2 is not None:
            self.logger.error(f'{ctx2.getText()}')
            assert False, f'Unhandled {ctx2.getText()}'
        elif ctx3 is not None:
            self.logger.error(f'{ctx3.getText()}')
            assert False, f'Unhandled {ctx3.getText()}'

        return self.visitChildren(ctx)

    def _handleFullParameters(self, className: ClassName, methodName: MethodName, defaultContexts: List[PythonParser.Param_with_defaultContext]):
        """
        Handles these type:
            fullScale(self, intParameter: int = 0, floatParameter: float = 42.0, stringParameter: str = ''):
        """

        for withDefaultCtx in defaultContexts:

            paramCtx:          PythonParser.ParamContext              = withDefaultCtx.param()
            nameAndType:       ParameterNameAndType                   = self._extractParameterNameAndType(paramCtx=paramCtx)
            defaultAssignment: PythonParser.Default_assignmentContext = withDefaultCtx.default_assignment()
            expr:               str                                   = defaultAssignment.children[1].getText()

            pyutParameter: PyutParameter = PyutParameter(name=nameAndType.name, type=PyutType(nameAndType.typeName), defaultValue=expr)
            self._updateModelMethodParameter(className=className, methodName=methodName, pyutParameter=pyutParameter)

    def _handleTypeAnnotated(self, className: ClassName, methodName: MethodName, noDefaultContexts: List[PythonParser.Param_no_defaultContext]):

        for noDefaultCtx in noDefaultContexts:
            paramCtx:    PythonParser.ParamContext = noDefaultCtx.param()
            nameAndType: ParameterNameAndType      = self._extractParameterNameAndType(paramCtx=paramCtx)

            if nameAndType.name == PARAMETER_SELF:
                continue

            pyutParameter: PyutParameter = PyutParameter(name=nameAndType.name, type=PyutType(nameAndType.typeName))

            self._updateModelMethodParameter(className=className, methodName=methodName, pyutParameter=pyutParameter)

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

    def _checkIfMethodBelongsToClass(self, node: PythonParser.Function_defContext, classType) -> ClassName:

        while node.parentCtx:
            if isinstance(node, classType):
                return self._extractClassName(ctx=node)
            node = node.parentCtx

        return NO_CLASS_NAME

    def _isProperty(self, methodName: MethodName) -> bool:
        """
        Used by the function definition visitor to determine if the current method name is marked as a property.

        Args:
            methodName:  The method name to check

        Returns: True if it is in our known list of property names.
        """
        ans: bool = False

        # propertyName: PropertyName = PropertyName(methodName)
        # if propertyName in self._propertyNames:
        #     ans = True

        return ans

    def _extractClassName(self, ctx: PythonParser.Class_defContext) -> ClassName:

        child:     PythonParser.Class_def_rawContext = ctx.class_def_raw()
        name:      TerminalNodeImpl                  = child.NAME()
        className: ClassName                         = name.getText()

        return className

    def _extractMethodName(self, ctx: PythonParser.Function_def_rawContext) -> MethodName:
        """

        Args:
            ctx:

        Returns:

        """

        name:       TerminalNodeImpl = ctx.NAME()
        methodName: MethodName       = MethodName(name.getText())

        return methodName

    def _extractParameterNameAndType(self, paramCtx: PythonParser.ParamContext) -> ParameterNameAndType:

        terminalNode:  TerminalNodeImpl = paramCtx.children[0]
        if len(paramCtx.children) > 1:
            annotationCtx: PythonParser.AnnotationContext = paramCtx.children[1]
            exprCtx:       PythonParser.ExpressionContext = annotationCtx.children[1]
            typeStr: str = exprCtx.getText()
        else:
            typeStr = ''

        paramName: str = terminalNode.getText()

        return ParameterNameAndType(name=paramName, typeName=typeStr)

    def _findClassContext(self, ctx: ParserRuleContext) -> PythonParser.Class_defContext:
        currentCtx: ParserRuleContext = ctx

        while isinstance(currentCtx, PythonParser.Class_defContext) is False:
            currentCtx = currentCtx.parentCtx
            if currentCtx is None:
                assert False, 'Unsupported stand alone method'

        return cast(PythonParser.Class_defContext, currentCtx)

    def _findMethodContext(self, ctx: ParserRuleContext) -> PythonParser.Function_defContext:

        currentCtx: ParserRuleContext = ctx

        while isinstance(currentCtx, PythonParser.Function_defContext) is False:
            currentCtx = currentCtx.parentCtx
            if currentCtx is None:
                break

        if currentCtx is not None:
            raw: PythonParser.Function_def_rawContext = cast(PythonParser.Function_defContext, currentCtx).function_def_raw()
            self.logger.debug(f'Found method: {raw.NAME()}')

        return cast(PythonParser.Function_defContext, currentCtx)

    def _findModelMethod(self, pyutClass: PyutClass, methodName: MethodName) -> PyutMethod:

        foundMethod: PyutMethod = cast(PyutMethod, None)

        pyutMethods: PyutMethods = pyutClass.methods
        for method in pyutMethods:
            pyutMethod: PyutMethod = cast(PyutMethod, method)
            if pyutMethod.name == methodName:
                foundMethod = pyutMethod
                break

        return foundMethod

    def _updateModelMethodParameter(self, className: ClassName, methodName: MethodName, pyutParameter: PyutParameter):

        self.logger.info(f'{pyutParameter=}')

        pyutClass:  PyutClass  = self._pyutClasses[className]
        pyutMethod: PyutMethod = self._findModelMethod(methodName=methodName, pyutClass=pyutClass)

        pyutMethod.addParameter(parameter=pyutParameter)
