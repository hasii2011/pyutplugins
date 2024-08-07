
from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import MagicMock

from codeallybasic.Position import Position
from codeallybasic.UnitTestBase import UnitTestBase

from ogl.OglObject import OglObject
from pyorthogonalrouting.enumerations.Side import Side

from pyutplugins.toolplugins.orthogonalrouting.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter


class TestOrthogonalAdapter(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 05 May 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

        self._mockOglObject: MagicMock = MagicMock(spec=OglObject)

        self._mockOglObject.GetPosition.return_value = (10, 10)
        self._mockOglObject.GetSize.return_value     = (40, 20)

    def tearDown(self):
        super().tearDown()

    def testTop(self):

        anchorPosition: Position = Position(x=40, y=10)
        expectedSide:   Side     = Side.TOP
        actualSide:     Side     = OrthogonalConnectorAdapter.whichConnectorSide(shape=self._mockOglObject, anchorPosition=anchorPosition)

        self.assertEqual(expectedSide, actualSide, 'Top computation is incorrect')

    def testBottom(self):

        anchorPosition: Position = Position(x=40, y=20)
        expectedSide:   Side     = Side.BOTTOM
        actualSide:     Side     = OrthogonalConnectorAdapter.whichConnectorSide(shape=self._mockOglObject, anchorPosition=anchorPosition)

        self.assertEqual(expectedSide, actualSide, 'Bottom computation is incorrect')

    def testLeft(self):

        expectedSide:   Side     = Side.LEFT
        anchorPosition: Position = Position(x=10, y=15)
        actualSide:     Side     = OrthogonalConnectorAdapter.whichConnectorSide(shape=self._mockOglObject, anchorPosition=anchorPosition)

        self.assertEqual(expectedSide, actualSide, 'Right computation is incorrect')

    def testRight(self):

        expectedSide:   Side     = Side.RIGHT
        anchorPosition: Position = Position(x=49, y=15)
        actualSide:     Side     = OrthogonalConnectorAdapter.whichConnectorSide(shape=self._mockOglObject, anchorPosition=anchorPosition)

        self.assertEqual(expectedSide, actualSide, 'Right computation is incorrect')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOrthogonalAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
