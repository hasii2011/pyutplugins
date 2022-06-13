
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from unittest import main as unitTestMain
from unittest import TestSuite

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from wx import App

from plugins.io.common.ElementTreeData import ElementTreeData
from plugins.io.dtd.DTDParser import DTDParser

from tests.TestBase import TestBase


class TestDTDParser(TestBase):

    EXPECTED_CLASS_COUNT: int = 17
    EXPECTED_LINK_COUNT:  int = 14

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDTDParser.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestDTDParser.clsLogger
        self.app:    App    = App()

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testBasicDTDProcessing(self):

        dtdParser: DTDParser = self._readDTD()

        actualClassCount: int = len(dtdParser._classTree)
        actualLinkCount:  int = len(dtdParser._links)

        self.assertEqual(TestDTDParser.EXPECTED_CLASS_COUNT, actualClassCount, 'Created class count does not match')
        self.assertEqual(TestDTDParser.EXPECTED_LINK_COUNT,  actualLinkCount,  'Incorrect number of links')

    def testPyutInformationPresent(self):

        dtdParser: DTDParser = self._readDTD()

        emailTreeData: ElementTreeData = dtdParser._classTree['email']
        phoneTreeData: ElementTreeData = dtdParser._classTree['phone']
        eventTreeData: ElementTreeData = dtdParser._classTree['event']

        self.assertIsNotNone(emailTreeData, 'Missing Pyut Information')
        self.assertIsNotNone(phoneTreeData, 'Missing Pyut Information')
        self.assertIsNotNone(eventTreeData, 'Missing Pyut Information')

    def testFieldPresence(self):

        dtdParser: DTDParser = self._readDTD()

        emailTreeData: ElementTreeData = dtdParser._classTree['email']
        phoneTreeData: ElementTreeData = dtdParser._classTree['phone']
        eventTreeData: ElementTreeData = dtdParser._classTree['event']

        self._testFieldPresence(treeData=emailTreeData, fieldName='requiredAttr')
        self._testFieldPresence(treeData=phoneTreeData, fieldName='impliedAttr')
        self._testFieldPresence(treeData=eventTreeData, fieldName='fixedAttr')

    def _testFieldPresence(self, treeData: ElementTreeData, fieldName: str):
        """
        Assumes each class has a single attribute

        Args:
            treeData:
            fieldName:
        """
        pyutClass: PyutClass = treeData.pyutClass

        fields: List[PyutField] = pyutClass.fields
        for pyutField in fields:
            self.assertEqual(fieldName, pyutField.name, 'Where is my attribute')

    def _readDTD(self) -> DTDParser:

        dtdParser:  DTDParser = DTDParser()
        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'AllElements.dtd')

        dtdParser.open(fqFileName)

        return dtdParser


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDTDParser))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
