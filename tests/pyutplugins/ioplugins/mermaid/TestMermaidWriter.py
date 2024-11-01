
from typing import List
from typing import cast

from os import environ

from pathlib import Path

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler
from untanglepyut.XmlVersion import XmlVersion

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.ioplugins.mermaid.MermaidWriter import MermaidWriter

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.ProjectTestBase import ProjectTestBase

# The base file names
REALIZATION:       str = 'MermaidRealization'
COMPOSITION:       str = 'MermaidComposition'
AGGREGATION:       str = 'MermaidAggregation'
INHERITANCE:       str = 'MermaidInheritance'
SIMPLE:            str = 'MermaidSimpleClass'
BASIC_ASSOCIATION: str = 'MermaidBasicAssociation'
FIELDS:            str = 'MermaidFields'
NOTES:             str = 'MermaidNotes'
LOLLIPOPS:         str  = 'MermaidLollipopInterfaces'

SUFFIX_MARKDOWN: str = '.md'
SUFFIX_XML:      str = '.xml'
# File names to delete at end of tests
GENERATED_FILE_NAMES: List[str] = [f'{REALIZATION}{SUFFIX_MARKDOWN}',
                                   f'{COMPOSITION}{SUFFIX_MARKDOWN}',
                                   f'{AGGREGATION}{SUFFIX_MARKDOWN}',
                                   f'{INHERITANCE}{SUFFIX_MARKDOWN}',
                                   f'{SIMPLE}{SUFFIX_MARKDOWN}',
                                   f'{BASIC_ASSOCIATION}{SUFFIX_MARKDOWN}',
                                   f'{FIELDS}{SUFFIX_MARKDOWN}'
                                   ]


class TestMermaidWriter(ProjectTestBase):
    """
    """
    keep:      bool   = False

    @classmethod
    def setUpClass(cls):
        ProjectTestBase.setUpClass()

        if 'KEEP' in environ:
            keep: str = environ["KEEP"]
            if keep.lower().strip() == 'true':
                cls.keep = True
            else:
                cls.keep = False
        else:
            cls.clsLogger.debug(f'No need to keep data files')
            cls.keep = False

    @classmethod
    def tearDownClass(cls):
        ProjectTestBase.tearDownClass()
        cls.clsLogger.debug(f'tearDownClass {cls.keep=}')
        if cls.keep is False:
            for fileName in GENERATED_FILE_NAMES:
                cls.cleanupGenerated(fileName=fileName)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSimpleClass(self):
        baseFileName: str           = f'{SIMPLE}{SUFFIX_MARKDOWN}'
        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{SIMPLE}{SUFFIX_XML}', documentTitle='SimpleDiagram')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)

        self.assertEqual(0, status, 'Simple Mermaid generation failed')

    def testClassWithFields(self):
        baseFileName:  str           = f'{FIELDS}{SUFFIX_MARKDOWN}'
        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{FIELDS}{SUFFIX_XML}', documentTitle='Fields')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Mermaid field generation failed')

    def testSimpleInheritance(self):

        baseFileName:  str           = f'{INHERITANCE}{SUFFIX_MARKDOWN}'
        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{INHERITANCE}{SUFFIX_XML}', documentTitle='Inheritance')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Inheritance failed')

    def testSimpleAggregation(self):
        baseFileName:  str           = f'{AGGREGATION}{SUFFIX_MARKDOWN}'
        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{AGGREGATION}{SUFFIX_XML}', documentTitle='Aggregation')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Aggregation failed')

    def testSimpleComposition(self):
        baseFileName:  str           = f'{COMPOSITION}{SUFFIX_MARKDOWN}'
        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{COMPOSITION}{SUFFIX_XML}', documentTitle='Composition')
        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Aggregation failed')

    def testSimpleRealization(self):
        baseFileName:  str           = f'{REALIZATION}{SUFFIX_MARKDOWN}'
        fqFileName:    str           = self.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{REALIZATION}{SUFFIX_XML}', documentTitle='Realization')
        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Realization failed')

    def testBasicAssociation(self):
        baseFileName:  str           = f'{BASIC_ASSOCIATION}{SUFFIX_MARKDOWN}'

        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{BASIC_ASSOCIATION}{SUFFIX_XML}', documentTitle='Association')
        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Association failed')

    def testNotes(self):
        baseFileName:  str           = f'{NOTES}{SUFFIX_MARKDOWN}'

        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{NOTES}{SUFFIX_XML}', documentTitle='DiagramNotes')
        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Note Generation failed')

    def testLollipopInterfaces(self):
        baseFileName:  str           = f'{LOLLIPOPS}{SUFFIX_MARKDOWN}'

        fqFileName:    str           = ProjectTestBase.constructGeneratedName(baseFileName=baseFileName)
        mermaidWriter: MermaidWriter = MermaidWriter(Path(fqFileName), writeCredits=False)

        oglObjects: OglObjects = self._getTestObjects(baseXmlFileName=f'{LOLLIPOPS}{SUFFIX_XML}', documentTitle='SampleIFace', xmlVersion=XmlVersion.V11)
        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = ProjectTestBase.runDiff(goldenPackageName=ProjectTestBase.GOLDEN_MERMAID_PACKAGE_NAME, baseFileName=baseFileName)
        self.assertEqual(0, status, 'Lollipop Interface Generation failed')

    def _getTestObjects(self, baseXmlFileName: str, documentTitle: str, xmlVersion: XmlVersion = XmlVersion.V10) -> OglObjects:

        fqFileName: str = ProjectTestBase.getFullyQualifiedResourceFileName(ProjectTestBase.RESOURCES_TEST_MERMAID_PACKAGE_NAME, baseXmlFileName)

        untangler:  UnTangler = UnTangler(xmlVersion=xmlVersion)

        untangler.untangleFile(fqFileName=fqFileName)

        document:   Document   = untangler.documents[DocumentTitle(documentTitle)]
        oglObjects: OglObjects = self._toPluginOglObjects(document=document)
        self.logger.info(f'{oglObjects=}')

        return oglObjects

    def _toPluginOglObjects(self, document: Document) -> OglObjects:

        oglObjects: OglObjects = OglObjects([])
        oglObjects.extend(cast(OglObjects, document.oglClasses))
        oglObjects.extend(cast(OglObjects, document.oglLinks))
        oglObjects.extend(cast(OglObjects, document.oglNotes))
        oglObjects.extend(cast(OglObjects, document.oglTexts))

        return oglObjects


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestMermaidWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
