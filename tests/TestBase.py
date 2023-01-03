
import json

import logging
import logging.config

from pkg_resources import resource_filename

from miniogl.DiagramFrame import DiagramFrame

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import DocumentTitle
from untanglepyut.UnTangler import UnTangler

from wx import App
from wx import Frame
from wx import ID_ANY

from unittest import TestCase

from core.coretypes.Types import OglClasses
from core.coretypes.Types import OglObjects

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

    RESOURCES_TEST_JAVA_BASE_FILES_PACKAGE_NAME: str = f'{RESOURCES_TEST_DATA_PACKAGE_NAME}.javabasefiles'

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
