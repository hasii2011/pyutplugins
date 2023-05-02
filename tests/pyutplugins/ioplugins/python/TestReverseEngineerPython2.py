
from typing import Dict
from typing import List

from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import Mock
from unittest.mock import PropertyMock

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.DisplayMethodParameters import DisplayMethodParameters
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglLinks

from pyutplugins.ioplugins.python.PyutPythonVisitor import ClassName
from pyutplugins.ioplugins.python.PyutPythonVisitor import DataClassProperties
from pyutplugins.ioplugins.python.PyutPythonVisitor import DataClassProperty
from pyutplugins.ioplugins.python.PyutPythonVisitor import ExpressionText
from pyutplugins.ioplugins.python.PyutPythonVisitor import MultiParameterNames

from pyutplugins.ioplugins.python.PyutPythonVisitor import PyutPythonVisitor
from pyutplugins.ioplugins.python.ReverseEngineerPython2 import ReverseEngineerPython2

from tests.TestBase import TestBase


class TestReverseEngineerPython2(TestBase):
    """
    """
    PROPERTY_NAMES: List[str] = ['fontSize', 'verticalGap']

    def setUp(self):

        super().setUp()
        self.reverseEngineer: ReverseEngineerPython2 = ReverseEngineerPython2()

    def tearDown(self):
        super().tearDown()

    def testFullClassInput(self):

        from os import path as osPath
        from os.path import dirname

        fqFileName: str = TestBase.getFullyQualifiedResourceFileName(TestBase.RESOURCES_TEST_CLASSES_PACKAGE_NAME, 'SimpleClass.py')

        fileName:      str = osPath.basename(fqFileName)
        directoryName: str = dirname(fqFileName)
        files:         List[str] = ['GraphElement.py', fileName]
        self.reverseEngineer.reversePython(directoryName=directoryName, files=files, progressCallback=self._fakeProgressCallback)

        oglClasses: OglClasses = self.reverseEngineer.oglClasses
        oglLinks:   OglLinks   = self.reverseEngineer.oglLinks

        self.assertEqual(2, len(oglClasses), 'Should have gotten a simple class')
        self.assertEqual(1, len(oglLinks),   'There should be a single link')

    def testParseFieldToPyutMinimal(self):

        fieldDataMinimal: str = 'minVal=0'

        pyutField: PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataMinimal)

        self.assertEqual('minVal', pyutField.name, 'No match on name')
        self.assertEqual('0', pyutField.defaultValue, 'No match on default value')

    def testParseFieldToPyutComplex(self):

        fieldDataMinimal: str       = 'minVal:int = 0'
        pyutField:        PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataMinimal)

        expectedFieldVisibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        expectedFieldType: PyutType = PyutType('int')
        actualFieldType:   PyutType = pyutField.type

        self.assertEqual('minVal', pyutField.name, 'No match on name')
        self.assertEqual(expectedFieldVisibility, pyutField.visibility, 'Did not parse visibility correctly')
        self.assertEqual(expectedFieldType, actualFieldType, 'Did not parse field type correctly')
        self.assertEqual('0', pyutField.defaultValue, 'Did not parse field default value correctly')

    def testParseFieldMinimalEOLComment(self):

        fieldDataRegressionOne: str = "inc = None  # 'the first outgoing incident half-edge'"

        pyutField: PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataRegressionOne)

        self.assertEqual('inc', pyutField.name, 'No match on name')
        self.assertEqual('None', pyutField.defaultValue, 'No match on default value')

    def testParseFieldToPyutComplexEOLComplex(self):

        fieldDataMinimal: str       = "minVal:int = 0   # I am end of line comment"
        pyutField:        PyutField = self.reverseEngineer._parseFieldToPyut(fieldDataMinimal)

        expectedFieldVisibility: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

        expectedFieldType: PyutType = PyutType('int')
        actualFieldType:   PyutType = pyutField.type

        self.assertEqual('minVal', pyutField.name, 'No match on name')
        self.assertEqual(expectedFieldVisibility, pyutField.visibility, 'Did not parse visibility correctly')
        self.assertEqual(expectedFieldType, actualFieldType, 'Did not parse field type correctly')
        self.assertEqual('0', pyutField.defaultValue, 'Did not parse field default value correctly')

    def testCreateDataClassPropertiesAsFields(self):

        sampleDataClassProperties: DataClassProperties = [
            DataClassProperty(('DataTestClass', 'w="A String"')),                   # type: ignore
            DataClassProperty(('DataTestClass', 'x:float=0.0')),                    # type: ignore
            DataClassProperty(('DataTestClass', 'y:float=42.0')),                   # type: ignore
            DataClassProperty((ClassName('DataTestClass'), ExpressionText('z:int')))
        ]
        pyutClass: PyutClass = PyutClass(name='DataTestClass')

        self.reverseEngineer._createDataClassPropertiesAsFields(pyutClass=pyutClass, dataClassProperties=sampleDataClassProperties)

    def testCreatePropertiesNormal(self):

        PyutMethod.displayParameters = DisplayMethodParameters.WITH_PARAMETERS

        propName:     str       = 'fontSize'
        setterParams: List[str] = ['newSize:int']

        setter, getter = self.reverseEngineer._createProperties(propName=propName, setterParams=setterParams)
        PyutMethod.setStringMode(DisplayMethodParameters.WITH_PARAMETERS)

        self.logger.debug(f'setter={setter.__str__()} getter={getter.__str__()}')

        self.assertEqual('+fontSize(newSize: int)', setter.getString(), 'Incorrect setter generated')
        self.assertEqual('+fontSize(): int', getter.getString(), 'Incorrect getter generated')

    def testCreatePropertiesReadOnly(self):

        propName:      str = 'fontSize'
        setterParams: List[str] = []

        setter, getter = self.reverseEngineer._createProperties(propName=propName, setterParams=setterParams)
        PyutMethod.setStringMode(DisplayMethodParameters.WITH_PARAMETERS)

        self.assertIsNone(setter)
        self.assertIsNotNone(getter)

    def testGeneratePropertiesAsMethodsNormaCorrectCount(self):

        pyutClass: PyutClass = self._generateNormalMethods()

        pyutMethods:         List[PyutMethod] = pyutClass.methods
        expectedMethodCount: int = 4
        actualMethodCount:   int = len(pyutMethods)

        self.assertEqual(expectedMethodCount, actualMethodCount, 'Generated incorrect # of methods')

    def testGeneratePropertiesAsMethodsNormalDesignatedAsProperties(self):

        pyutClass: PyutClass = self._generateNormalMethods()

        pyutMethods: List[PyutMethod] = pyutClass.methods
        for pyutMethod in pyutMethods:
            self.assertTrue(pyutMethod.isProperty, 'Not correctly identified')

    def testGeneratePropertiesAsMethodsReadOnlyPropertiesCorrectCount(self):

        pyutClass: PyutClass = self._generateReadOnlyMethods()

        pyutMethods:         List[PyutMethod] = pyutClass.methods
        expectedMethodCount: int              = 3
        actualMethodCount:   int              = len(pyutMethods)

        self.assertEqual(expectedMethodCount, actualMethodCount, 'Generated incorrect # of methods')

    def testGeneratePropertiesAsMethodsReadOnlyPropertiesCorrectPyutMethods(self):

        pyutClass:   PyutClass = self._generateReadOnlyMethods()
        pyutMethods: List[PyutMethod] = pyutClass.methods

        for pyutMethod in pyutMethods:
            generatedMethodName: str = pyutMethod.name
            self.assertIn(member=generatedMethodName, container=TestReverseEngineerPython2.PROPERTY_NAMES)

    def testParametersComplexTypedAndDefaultValue(self):

        # multiParameterNames: MultiParameterNames = MultiParameterNames('param1,param2:float,param3=57.0,param4:float=42.0')
        multiParameterNames: MultiParameterNames = MultiParameterNames('param4:float=42.0')
        pyutParameters: List[PyutParameter] = self.reverseEngineer._generateParameters(multiParameterNames=multiParameterNames)
        self.logger.debug(f'{pyutParameters=}')

        pyutParameter: PyutParameter = pyutParameters[0]
        self.assertEqual('param4', pyutParameter.name, 'Name is incorrect')
        self.assertEqual(PyutType(value='float'), pyutParameter.type, 'We parsed the type incorrectly')
        self.assertEqual('42.0', pyutParameter.defaultValue, 'Did not default value correctly')

    def testGenerateParametersSimple(self):
        multiParameterNames: MultiParameterNames = MultiParameterNames('param')
        pyutParameters:      List[PyutParameter]     = self.reverseEngineer._generateParameters(multiParameterNames=multiParameterNames)

        pyutParameter: PyutParameter = pyutParameters[0]

        self.assertEqual('param', pyutParameter.name, 'Name is incorrect')
        self.assertEqual('', pyutParameter.defaultValue, 'Default value should be empty string')
        self.assertEqual(PyutType(''), pyutParameter.type, 'Should not have a type')

    def testGenerateParametersSimpleDefaultValue(self):
        multiParameterNames: MultiParameterNames = MultiParameterNames('param3=57.0')
        pyutParameters:      List[PyutParameter]     = self.reverseEngineer._generateParameters(multiParameterNames=multiParameterNames)

        pyutParameter: PyutParameter = pyutParameters[0]

        self.assertEqual('param3', pyutParameter.name, 'Name is incorrect')
        self.assertEqual('57.0', pyutParameter.defaultValue)
        self.assertEqual(PyutType(''), pyutParameter.type, 'Should not have a type')

    def testGenerateParametersTypedParameter(self):
        typedParameterName: MultiParameterNames = MultiParameterNames('param2:float')
        pyutParameters:      List[PyutParameter]     = self.reverseEngineer._generateParameters(multiParameterNames=typedParameterName)

        pyutParameter: PyutParameter = pyutParameters[0]
        self.assertEqual('param2', pyutParameter.name, 'Name is incorrect')

        expectedType: PyutType = PyutType(value='float')
        actualType:   PyutType = pyutParameter.type

        self.assertEqual(expectedType, actualType, 'Type not set correctly')

        self.assertEqual('', pyutParameter.defaultValue, 'There should be no default value')

    def _generateReadOnlyMethods(self):
        # Note the missing setter for fontSize
        getterProperties: Dict[str, List] = {'fontSize': [''], 'verticalGap': ['']}
        setterProperties: Dict[str, List] = {'verticalGap': ['newValue']}
        pyutClass:        PyutClass       = PyutClass(name='NormalPropertiesClass')

        self.__setMockVisitorPropertyNames()

        pyutClass = self.reverseEngineer._generatePropertiesAsMethods(pyutClass=pyutClass,
                                                                      getterProperties=getterProperties,
                                                                      setterProperties=setterProperties
                                                                      )
        return pyutClass

    def _generateNormalMethods(self):

        getterProperties: Dict[str, List] = {'fontSize': [''], 'verticalGap': ['']}
        setterProperties: Dict[str, List] = {'fontSize': ['newSize:int'], 'verticalGap': ['newValue']}

        pyutClass:   PyutClass = PyutClass(name='NormalPropertiesClass')
        self.__setMockVisitorPropertyNames()

        pyutClass = self.reverseEngineer._generatePropertiesAsMethods(pyutClass=pyutClass,
                                                                      getterProperties=getterProperties,
                                                                      setterProperties=setterProperties
                                                                      )
        return pyutClass

    def _fakeProgressCallback(self, currentFileCount: int, msg: str):
        self.logger.info(f'{currentFileCount} - {msg}')

    def __setMockVisitorPropertyNames(self):
        mockVisitor: Mock = Mock(spec=PyutPythonVisitor)
        type(mockVisitor).propertyNames = PropertyMock(return_value=TestReverseEngineerPython2.PROPERTY_NAMES)
        self.reverseEngineer.visitor = mockVisitor


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestReverseEngineerPython2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
