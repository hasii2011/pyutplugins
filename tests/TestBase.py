
import json

import logging
import logging.config

from pkg_resources import resource_filename

from miniogl.DiagramFrame import DiagramFrame

from wx import App
from wx import Frame
from wx import ID_ANY

from unittest import TestCase

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
