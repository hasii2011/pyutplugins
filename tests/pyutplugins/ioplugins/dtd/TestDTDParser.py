
from typing import List

from unittest import main as unitTestMain
from unittest import TestSuite

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutField import PyutField

from pyutplugins.common.ElementTreeData import ElementTreeData
from pyutplugins.ioplugins.dtd.DTDParser import DTDParser

from tests.ProjectTestBase import ProjectTestBase


class TestDTDParser(ProjectTestBase):

    EXPECTED_CLASS_COUNT: int = 17
    EXPECTED_LINK_COUNT:  int = 14

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testBasicDTDProcessing(self):

        dtdParser: DTDParser = self._readDTD()

        actualClassCount: int = len(dtdParser.classTree)
        actualLinkCount:  int = len(dtdParser.links)

        self.assertEqual(TestDTDParser.EXPECTED_CLASS_COUNT, actualClassCount, 'Created class count does not match')
        self.assertEqual(TestDTDParser.EXPECTED_LINK_COUNT,  actualLinkCount,  'Incorrect number of links')

    def testPyutInformationPresent(self):

        dtdParser: DTDParser = self._readDTD()

        emailTreeData: ElementTreeData = dtdParser.classTree['email']
        phoneTreeData: ElementTreeData = dtdParser.classTree['phone']
        eventTreeData: ElementTreeData = dtdParser.classTree['event']

        self.assertIsNotNone(emailTreeData, 'Missing Pyut Information')
        self.assertIsNotNone(phoneTreeData, 'Missing Pyut Information')
        self.assertIsNotNone(eventTreeData, 'Missing Pyut Information')

    def testFieldPresence(self):

        dtdParser: DTDParser = self._readDTD()

        emailTreeData: ElementTreeData = dtdParser.classTree['email']
        phoneTreeData: ElementTreeData = dtdParser.classTree['phone']
        eventTreeData: ElementTreeData = dtdParser.classTree['event']

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
        fqFileName: str       = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, 'AllElements.dtd')

        dtdParser.open(fqFileName)

        return dtdParser


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestDTDParser))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
