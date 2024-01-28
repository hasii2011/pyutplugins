
from typing import cast
from typing import Dict
from typing import List
from typing import NewType
from typing import Union

from logging import Logger
from logging import getLogger

from os import linesep as osLineSep

from dataclasses import dataclass

from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutMethod import PyutMethod
from pyutmodelv2.PyutMethod import PyutMethods
from pyutmodelv2.PyutParameter import PyutParameter
from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutType import PyutType
from pyutmodelv2.enumerations.PyutStereotype import PyutStereotype
from pyutmodelv2.enumerations.PyutVisibility import PyutVisibility

from pyutplugins.ioplugins.python.pythonpegparser.PythonParser import PythonParser

from pyutplugins.ioplugins.python.pythonpegparser.PythonParserVisitor import PythonParserVisitor

PyutClassName = NewType('PyutClassName', str)
MethodName    = NewType('MethodName', str)
PropertyName  = NewType('PropertyName', str)
ParentName    = NewType('ParentName', str)
ChildName     = NewType('ChildName',  str)

ClassNames    = NewType('ClassNames', List[PyutClassName])
MethodNames   = NewType('MethodNames',   List[MethodName])

Children   = List[Union[PyutClassName, ChildName]]

Parents       = NewType('Parents',       Dict[ParentName, Children])
Methods       = NewType('Methods',       List[MethodNames])

PropertyNames = NewType('PropertyNames', List[PropertyName])
CodeLine      = NewType('CodeLine',      str)
CodeLines     = NewType('CodeLines',     List[CodeLine])
MethodCode    = NewType('MethodCode',    Dict[MethodName,   CodeLines])

PropertyMap   = NewType('PropertyMap', Dict[PyutClassName, PropertyNames])

NO_CLASS_NAME: PyutClassName = PyutClassName('')

NO_CLASS_DEF_CONTEXT: PythonParser.Class_defContext = cast(PythonParser.Class_defContext, None)

NO_METHOD_CTX: PythonParser.AssignmentContext = cast(PythonParser.AssignmentContext, None)


PyutClasses = NewType('PyutClasses', Dict[PyutClassName, PyutClass])

# noinspection SpellCheckingInspection
MAGIC_DUNDER_METHODS:      List[str] = ['__init__', '__str__', '__repr__', '__new__', '__del__',
                                        '__eq__', '__ne__', '__lt__', '__gt__', '__le__', '__ge__'
                                        '__pos__', '__neg__', '__abs__', '__invert__', '__round__', '__floor__', '__floor__', '__trunc__',
                                        '__add__', '__sub__', '__mul__', '__floordiv__', '__div__', '__truediv__', '__mod__', '__divmod__', '__pow__',
                                        '__lshift__', '__rshift__', '__and__', '__or__', '__xor__',
                                        '__hash__',
                                        '__getattr__', '__setattr__', '__getattribute__', '__delattr__',
                                        '__len__', '__setitem__', '__delitem__', '__contains__', '__missing__',
                                        '__call__', '__enter__', '__exit__',
                                        '__bool__'
                                        ]

PARAMETER_SELF:      str = 'self'
PROTECTED_INDICATOR: str = '_'
PRIVATE_INDICATOR:   str = '__'
PROPERTY_DECORATOR:  str = 'property'

VERSION: str = '2.0'


@dataclass
class ParameterNameAndType:
    name:     str = ''
    typeName: str = ''


class PyutPythonPegVisitor(PythonParserVisitor):
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._parents:       Parents       = Parents({})
        self._pyutClasses:   PyutClasses   = PyutClasses({})

        self._propertyMap: PropertyMap = PropertyMap({})

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

        # self._classNames.append(className)
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
        self._propertyMap[className] = PropertyNames([])

        return self.visitChildren(ctx)

    def visitFunction_def(self, ctx: PythonParser.Function_defContext):
        """
        Visit a parse tree produced by PythonParser#function_def.

        Args:
            ctx:
        """
        classCtx: PythonParser.Class_defContext = self._extractClassDefContext(ctx)
        if classCtx != NO_CLASS_DEF_CONTEXT:

            className:     PyutClassName = self._extractClassName(ctx=classCtx)
            methodName:    MethodName    = self._extractMethodName(ctx=ctx.function_def_raw())
            returnTypeStr: str           = self._extractReturnType(ctx=ctx)

            pyutVisibility: PyutVisibility = PyutVisibility.PUBLIC
            if methodName in MAGIC_DUNDER_METHODS:
                pass
            elif methodName.startswith(PRIVATE_INDICATOR):
                pyutVisibility = PyutVisibility.PRIVATE
            elif methodName.startswith(PROTECTED_INDICATOR):
                pyutVisibility = PyutVisibility.PROTECTED

            if self._isProperty(ctx) is True:
                self._makePropertyEntry(className=className, methodName=methodName)
                self._makeAField(ctx=ctx)
            else:
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

        className:    PyutClassName    = self._extractClassName(ctx=classCtx)
        propertyName: PropertyName = self._extractPropertyName(ctx=methodCtx.function_def_raw())
        if self._isThisAParameterListForAProperty(className=className, propertyName=propertyName) is True:
            pass
        else:
            methodName: MethodName = self._extractMethodName(ctx=methodCtx.function_def_raw())
            self.logger.debug(f'{className=} {methodName=}')
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

    def visitAssignment(self, ctx: PythonParser.AssignmentContext):
        """
        Visit a parse tree produced by PythonParser#assignment.

        Args:
            ctx:

        """
        exprCtx: PythonParser.ExpressionContext = ctx.expression()

        if exprCtx is not None:
            self.logger.debug(f'{ctx.getText()=} {exprCtx.getText()=}')

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

    def _handleFullParameters(self, className: PyutClassName, methodName: MethodName, defaultContexts: List[PythonParser.Param_with_defaultContext]):
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

    def _handleTypeAnnotated(self, className: PyutClassName, methodName: MethodName, noDefaultContexts: List[PythonParser.Param_no_defaultContext]):

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

    def _createParentChildEntry(self, argumentsCtx: PythonParser.ArgumentsContext, childName: Union[PyutClassName, ChildName]):

        args:       PythonParser.ArgsContext = argumentsCtx.args()
        parentName: ParentName               = ParentName(args.getText())
        self.logger.info(f'Class: {childName} is subclass of {parentName}')

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

    def _extractClassDefContext(self, ctx: PythonParser.Function_defContext) -> PythonParser.Class_defContext:
        """
        Args:
            ctx:

        Returns:  Either a class definition context or the sentinel value NO_CLASS_DEF_CONTEXT
        """
        currentCtx: ParserRuleContext = ctx
        while currentCtx.parentCtx:
            if isinstance(currentCtx, PythonParser.Class_defContext):
                return currentCtx
            currentCtx = currentCtx.parentCtx

        return NO_CLASS_DEF_CONTEXT

    def _checkIfContextBelongsToClass(self, ctx: ParserRuleContext) -> bool:

        ans: bool = False

        currentCtx = ctx
        while currentCtx.parentCtx:
            if isinstance(currentCtx, PythonParser.Class_defContext):
                ans = True
            currentCtx = currentCtx.parentCtx

        return ans

    def _isProperty(self, ctx: PythonParser.Function_defContext) -> bool:
        """
        Used by the function definition visitor to determine if the current method name is marked as a property.

        Args:
            ctx:  The function's raw context

        Returns: If its annotated as a property.
        """
        ans: bool = False

        decorators: PythonParser.DecoratorsContext = ctx.decorators()
        if decorators is None:
            pass
        else:
            namedExpressions: List[PythonParser.Named_expressionContext] = decorators.named_expression()
            for ne in namedExpressions:
                self.logger.debug(f'{ne.getText()=}')
                if ne.getText() == PROPERTY_DECORATOR:
                    ans = True
                    break
        return ans

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

    def _extractPropertyName(self, ctx: PythonParser.Function_def_rawContext) -> PropertyName:

        propertyName: PropertyName = PropertyName(self._extractFunctionNameRawString(ctx=ctx))
        return propertyName

    def _extractMethodName(self, ctx: PythonParser.Function_def_rawContext) -> MethodName:

        methodName: MethodName       = MethodName(self._extractFunctionNameRawString(ctx=ctx))
        return methodName

    def _extractFunctionNameRawString(self, ctx: PythonParser.Function_def_rawContext) -> str:

        name: TerminalNodeImpl = ctx.NAME()
        return name.getText()

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

    def _updateModelMethodParameter(self, className: PyutClassName, methodName: MethodName, pyutParameter: PyutParameter):

        self.logger.debug(f'{pyutParameter=}')

        pyutClass:  PyutClass  = self._pyutClasses[className]
        pyutMethod: PyutMethod = self._findModelMethod(methodName=methodName, pyutClass=pyutClass)

        pyutMethod.addParameter(parameter=pyutParameter)

    def _makeAField(self, ctx: PythonParser.Function_defContext):
        """
        Turns methods annotated as property into an UML field

        Args:
            ctx:
        """

        classCtx:  PythonParser.Class_defContext    = self._findClassContext(ctx)
        methodCtx: PythonParser.Function_defContext = self._findMethodContext(ctx)

        className:    PyutClassName    = self._extractClassName(ctx=classCtx)
        propertyName: PropertyName = self._extractPropertyName(ctx=methodCtx.function_def_raw())
        self.logger.debug(f'{className} property name: {propertyName}')
        #
        # it is really a property name
        #
        typeStr: str = self._extractReturnType(ctx=ctx)

        pyutField: PyutField = PyutField(name=propertyName, type=PyutType(typeStr), visibility=PyutVisibility.PUBLIC)
        pyutClass: PyutClass = self._pyutClasses[className]
        pyutClass.fields.append(pyutField)

    def _makePropertyEntry(self, className: PyutClassName, methodName: MethodName):
        """
        Make an entry into the property map.  This ensures that we do not try to create
        arguments for an annotated method when we visit the method parameters

        Args:
            methodName:  A property name which we turn into a field

        """
        self._propertyMap[className].append(cast(PropertyName, methodName))

    def _isThisAParameterListForAProperty(self, className: PyutClassName, propertyName: PropertyName):
        ans: bool = False

        propertyNames: PropertyNames = self._propertyMap[className]
        if propertyName in propertyNames:
            ans = True

        return ans

    def _extractReturnType(self, ctx: PythonParser.Function_defContext) -> str:

        exprCtx: PythonParser.ExpressionContext = ctx.function_def_raw().expression()

        if exprCtx is None:
            returnTypeStr: str = ''
        else:
            returnTypeStr = exprCtx.getText()

        return returnTypeStr

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
