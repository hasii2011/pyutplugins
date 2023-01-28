
from typing import List
from typing import cast

from os import system as osSystem
from os import environ

from pathlib import Path

from logging import Logger
from logging import getLogger

from pkg_resources import resource_filename

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.ioplugins.mermaid.MermaidWriter import MermaidWriter

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase


COMPOSITION_MD:         str = 'MermaidComposition.md'
MERMAID_AGGREGATION_MD: str = 'MermaidAggregation.md'
MERMAID_INHERITANCE_MD: str = 'MermaidInheritance.md'
MERMAID_SIMPLE_MD:      str = 'MermaidSimple.md'

# File names to delete at end of tests
GENERATED_FILE_NAMES: List[str] = [COMPOSITION_MD, MERMAID_AGGREGATION_MD, MERMAID_INHERITANCE_MD, MERMAID_SIMPLE_MD]


class TestMermaidWriter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)
    keep:      bool   = False

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMermaidWriter.clsLogger = getLogger(__name__)

        if 'KEEP' in environ:
            keep: str = environ["KEEP"]
            if keep.lower().strip() == 'true':
                cls.keep = True
            else:
                cls.keep = False
        else:
            cls.clsLogger.info(f'No need to keep data files')
            cls.keep = False

    @classmethod
    def tearDownClass(cls):
        if cls.keep is False:
            for fileName in GENERATED_FILE_NAMES:
                cls.cleanup(fileName)

    def setUp(self):
        # I need a wx.App
        super().setUp()

        self.logger: Logger = TestMermaidWriter.clsLogger

    def tearDown(self):
        pass

    def testSimpleClass(self):
        baseFileName: str = MERMAID_SIMPLE_MD
        mermaidWriter: MermaidWriter = MermaidWriter(Path(baseFileName), writeCredits=False)

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_MERMAID_PACKAGE_NAME, 'SimpleClass.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('SimpleDiagram')]

        oglObjects: OglObjects = self._toPluginOglObjects(document=document)
        self.logger.info(f'{oglObjects[0]=}')
        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = self._runDiff(baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Mermaid generation failed')

    def testSimpleInheritance(self):

        baseFileName: str = MERMAID_INHERITANCE_MD
        mermaidWriter: MermaidWriter = MermaidWriter(Path(baseFileName), writeCredits=False)

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_MERMAID_PACKAGE_NAME, 'MermaidInheritance.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Inheritance')]

        oglObjects: OglObjects = self._toPluginOglObjects(document=document)
        self.logger.info(f'{oglObjects[0]=}')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = self._runDiff(baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Inheritance failed')

    def testSimpleAggregation(self):
        baseFileName: str = MERMAID_AGGREGATION_MD
        mermaidWriter: MermaidWriter = MermaidWriter(Path(baseFileName), writeCredits=False)

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_MERMAID_PACKAGE_NAME, 'MermaidAggregation.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Aggregation')]
        oglObjects: OglObjects = self._toPluginOglObjects(document=document)
        self.logger.info(f'{oglObjects[0]=}')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = self._runDiff(baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Aggregation failed')

    def testSimpleComposition(self):
        baseFileName: str = COMPOSITION_MD
        mermaidWriter: MermaidWriter = MermaidWriter(Path(baseFileName), writeCredits=False)

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_MERMAID_PACKAGE_NAME, 'MermaidComposition.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Composition')]
        oglObjects: OglObjects = self._toPluginOglObjects(document=document)
        self.logger.info(f'{oglObjects[0]=}')

        mermaidWriter.translate(oglObjects=oglObjects)

        status: int = self._runDiff(baseFileName=baseFileName)
        self.assertEqual(0, status, 'Simple Aggregation failed')

    def _toPluginOglObjects(self, document: Document) -> OglObjects:

        oglObjects: OglObjects = OglObjects([])
        oglObjects.extend(cast(OglObjects, document.oglClasses))
        oglObjects.extend(cast(OglObjects, document.oglLinks))
        oglObjects.extend(cast(OglObjects, document.oglNotes))
        oglObjects.extend(cast(OglObjects, document.oglTexts))

        return oglObjects

    def _runDiff(self, baseFileName: str) -> int:

        goldenFileName:      str = resource_filename(TestBase.RESOURCES_TEST_GOLDEN_MERMAID_PACKAGE_NAME, baseFileName)

        status: int = osSystem(f'{TestBase.EXTERNAL_DIFF} {baseFileName} {goldenFileName}')

        return status

    @classmethod
    def cleanup(cls, baseFileName: str):
        path: Path = Path(baseFileName)

        if path.exists() is True:
            path.unlink()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMermaidWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
