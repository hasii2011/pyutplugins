
from typing import cast

from os import system as osSystem

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


class TestMermaidWriter(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMermaidWriter.clsLogger = getLogger(__name__)

    def setUp(self):
        # I need a wx.App
        super().setUp()

        self.logger: Logger = TestMermaidWriter.clsLogger

    def tearDown(self):
        pass

    def testSimpleClass(self):
        baseFileName: str = 'MermaidSimple.md'
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

    def testSimpleLinks(self):

        baseFileName: str = 'MermaidInheritance.md'
        mermaidWriter: MermaidWriter = MermaidWriter(Path(baseFileName), writeCredits=False)

        fqFileName: str = resource_filename(TestBase.RESOURCES_TEST_MERMAID_PACKAGE_NAME, 'MermaidInheritance.xml')
        untangler:  UnTangler = UnTangler()

        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle('Inheritance')]

        oglObjects: OglObjects = self._toPluginOglObjects(document=document)
        self.logger.info(f'{oglObjects[0]=}')

        mermaidWriter.translate(oglObjects=oglObjects)

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


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMermaidWriter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
