from click import option
from click import version_option
from wx import App

from click import command

from tests.TestBase import TestBase
from tests.scaffold.PluginTestFrame import PluginTestFrame


__version__ = "0.1.1"


class PluginTestScaffold(App):

    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self) -> bool:

        self._frameTop: PluginTestFrame = PluginTestFrame(title="Plugin Test Scaffold")

        self._frameTop.Show(True)

        TestBase.setUpLogging()
        return True

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

    testApp: PluginTestScaffold = PluginTestScaffold(redirect=False)

    if input_file is not None:
        testApp.loadXmlFile(input_file)
    testApp.MainLoop()


if __name__ == "__main__":

    commandHandler()
