
from logging import Logger
from logging import getLogger
import logging.config

from os import system as osSystem
from os import sep as osSep

from pathlib import Path

import json

from pkg_resources import resource_filename

from miniogl.DiagramFrame import DiagramFrame

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from wx import App
from wx import Frame
from wx import ID_ANY

from unittest import TestCase

from pyutplugins.ExternalTypes import OglClasses
from pyutplugins.ExternalTypes import OglObjects


JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class BogusApp(App):
    def OnInit(self) -> bool:
        return True


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:                      str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME:         str = f'{RESOURCES_PACKAGE_NAME}.testclasses'
    RESOURCES_TEST_DATA_PACKAGE_NAME:            str = f'{RESOURCES_PACKAGE_NAME}.testdata'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME:    str = f'{RESOURCES_PACKAGE_NAME}.testclasses.ozzee'

    RESOURCES_TEST_MERMAID_PACKAGE_NAME:        str = f'{RESOURCES_TEST_DATA_PACKAGE_NAME}.mermaid'

    # noinspection SpellCheckingInspection
    GOLDEN_JAVA_PACKAGE_NAME:    str = f'{RESOURCES_TEST_DATA_PACKAGE_NAME}.javagolden'
    # noinspection SpellCheckingInspection
    GOLDEN_MERMAID_PACKAGE_NAME: str = f'{RESOURCES_TEST_DATA_PACKAGE_NAME}.mermaidgolden'
    # noinspection SpellCheckingInspection
    GOLDEN_GML_PACKAGE_NAME:     str = f'{RESOURCES_TEST_DATA_PACKAGE_NAME}.gmlgolden'

    EXTERNAL_DIFF:         str = '/usr/bin/diff --normal --color=always '
    EXTERNAL_CLEAN_UP: str = 'rm '

    baseLogger: Logger = getLogger(__name__)

    def setUp(self):
        """
        Test classes that need to instantiate a wxPython App should super().setUp()
        """
        self._app:   BogusApp = BogusApp()
        baseFrame:   Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

    def tearDown(self):
        self._app.OnExit()

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """"""
        loggingConfigFilename: str = cls.findLoggingConfig()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def findLoggingConfig(cls) -> str:

        fqFileName = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

        return fqFileName

    @classmethod
    def runDiff(cls, goldenPackageName: str, baseFileName: str) -> int:
        """
        Assumes the caller use our ._constructGeneratedName method to get
        a fully qualified file name

        Args:
            goldenPackageName:  The package name where the gold file resides
            baseFileName:  The base file name

        Returns:  The results of the difference
        """
        goldenFileName:    str = resource_filename(goldenPackageName, baseFileName)
        generatedFileName: str = cls.constructGeneratedName(baseFileName=baseFileName)

        status: int = osSystem(f'{TestBase.EXTERNAL_DIFF} {goldenFileName} {generatedFileName}')

        return status

    @classmethod
    def cleanupGenerated(cls, fileName: str):

        generatedFileName: str = cls.constructGeneratedName(baseFileName=fileName)

        path: Path = Path(generatedFileName)

        cls.baseLogger.info(f'{path} - exists: {path.exists()}')
        if path.exists() is True:
            path.unlink()

    @classmethod
    def constructGeneratedName(cls, baseFileName: str) -> str:
        """
        Constructs a full path name for a file that will be used for a unit test.
        Currently, just uses /tmp

        Args:
            baseFileName:

        Returns:    Fully qualified file name

        """

        generatedFileName: str = f'{cls.getTemporaryDirectory()}{baseFileName}'
        return generatedFileName

    @classmethod
    def getTemporaryDirectory(cls) -> str:
        return f'{osSep}tmp{osSep}'

    def _xmlFileToOglClasses(self, filename: str, documentName: str) -> OglClasses:
        """
        The input file name must be in the test data package

        Args:
            filename:  The filename to read (Pyut XML format)
            documentName:  The document in the XML file

        Returns:  The untangled Ogl Classes;  May return an XX exception if the document name does not match
        """
        document: Document = self._getUntangledXmlDocument(filename=filename, documentName=documentName)

        return OglClasses(document.oglClasses)

    def _xmlFileToOglObjects(self, filename: str, documentName: str) -> OglObjects:
        """
        The input file name must be in the test data package;  This returns all the
        Ogl objects in the document

        Args:
            filename:  The filename to read (Pyut XML format)
            documentName:  The document in the XML file

        Returns:  The untangled Ogl Objects;  May return an XX exception if the document name does not match
        """
        document: Document = self._getUntangledXmlDocument(filename=filename, documentName=documentName)

        oglObjects: OglObjects = [item for lists in [document.oglClasses, document.oglLinks] for item in lists]  # type: ignore

        return oglObjects

    def _getUntangledXmlDocument(self, filename: str, documentName: str) -> Document:
        """

        Args:
            filename:  The filename to read (Pyut XML format)
            documentName:  The document in the XML file

        Returns:  The requested document;May return an XX exception if the document name does not match

        """
        fqFileName: str       = resource_filename(TestBase.RESOURCES_TEST_DATA_PACKAGE_NAME, filename)
        untangler:  UnTangler = UnTangler()
        untangler.untangleFile(fqFileName=fqFileName)

        document: Document = untangler.documents[DocumentTitle(documentName)]

        return document
