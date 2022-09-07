
import logging
import logging.config

import json


from click import command
from click import option
from click import version_option
from pkg_resources import resource_filename

from wx import App


__version__ = "2.0.0"

from tests.TestBase import JSON_LOGGING_CONFIG_FILENAME
from tests.TestBase import TestBase
from tests.scaffoldv2.ScaffoldFrame import ScaffoldFrame


class ScaffoldApp(App):

    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self) -> bool:

        ScaffoldApp.setUpLogging()

        self._frameTop: ScaffoldFrame = ScaffoldFrame()

        self._frameTop.Show(True)

        return True

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

    def loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: full qualified file name
        """
        self._frameTop.loadXmlFile(fqFileName=fqFileName)


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('-i', '--input-file', required=False, help='The input .xml file to preload on startup.')
def commandHandler(input_file: str):

    testApp: ScaffoldApp = ScaffoldApp(redirect=False)

    if input_file is not None:
        testApp.loadXmlFile(input_file)
    testApp.MainLoop()


if __name__ == "__main__":

    commandHandler()
