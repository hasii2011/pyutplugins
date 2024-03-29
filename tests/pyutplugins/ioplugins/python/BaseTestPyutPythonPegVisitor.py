
from typing import Dict
from typing import NewType

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyutmodelv2.PyutField import PyutField
from pyutmodelv2.PyutField import PyutFields
from pyutmodelv2.PyutMethod import PyutMethod

PyutFieldHashIndex  = NewType('PyutFieldHashIndex',  Dict[str, PyutField])


class BaseTestPyutPythonPegVisitor(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo - Humberto A. Sanchez II
        Generated: 04 February 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def _makeFieldIndex(self, pyutFields: PyutFields) -> PyutFieldHashIndex:

        fieldIndex: PyutFieldHashIndex = PyutFieldHashIndex({})
        for field in pyutFields:
            fieldIndex[field.name] = field

        return fieldIndex


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=BaseTestPyutPythonPegVisitor))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
