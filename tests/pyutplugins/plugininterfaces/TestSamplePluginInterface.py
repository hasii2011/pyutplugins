
from logging import Logger
from logging import getLogger

from sys import argv

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_CLOSE
from wx import EVT_MENU
from wx import ID_ANY

from wx import App
from wx import CommandEvent
from wx import Frame
from wx import Menu
from wx import MenuBar
from wx import MenuItem

from pyutplugins.coretypes.ImportDirectoryResponse import ImportDirectoryResponse
from pyutplugins.coretypes.MultipleFileRequestResponse import MultipleFileRequestResponse
from pyutplugins.coretypes.SingleFileRequestResponse import SingleFileRequestResponse

from tests.pyutplugins.coreinterfaces.SamplePluginInterface import SamplePluginInterface

from tests.pyutplugins.coreinterfaces.SampleIPluginAdapter import SampleIPluginAdapter

from tests.TestBase import TestBase


class TestSamplePluginInterface(App):
    """
    Manual test program.   Developer run this application
    to test the various message dialogs
    """

    FRAME_ID:      int = ID_ANY
    WINDOW_WIDTH:  int = 480
    WINDOW_HEIGHT: int = 240

    def __init__(self):
        App.__init__(self, redirect=False)

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)

        mediator: SampleIPluginAdapter = SampleIPluginAdapter()

        self._plugin: SamplePluginInterface = SamplePluginInterface(mediator)

    def OnInit(self):

        frameTop: Frame = Frame(parent=None,
                                id=TestSamplePluginInterface.FRAME_ID,
                                title="Test Abstract Plugin",
                                size=(TestSamplePluginInterface.WINDOW_WIDTH, TestSamplePluginInterface.WINDOW_HEIGHT),
                                style=DEFAULT_FRAME_STYLE)

        menuBar:     MenuBar = MenuBar()
        optionsMenu: Menu    = Menu()

        noUmlFrameItem:            MenuItem = optionsMenu.Append(ID_ANY, '&No Uml Frame\tF1')
        noSelectedOglObjectsItem:  MenuItem = optionsMenu.Append(ID_ANY, 'No &Selected UML\tF2')
        askForFileToImportItem:    MenuItem = optionsMenu.Append(ID_ANY, 'Ask for Import File\tF3')
        askForFileExportItem:      MenuItem = optionsMenu.Append(ID_ANY, 'Ask for Export File\tF4')
        askForImportDirectoryItem: MenuItem = optionsMenu.Append(ID_ANY, 'Ask for Import Directory\tF5')
        askForExportDirectoryItem: MenuItem = optionsMenu.Append(ID_ANY, 'Ask for Export Directory\tF6')

        askForMultipleImportFilesItem: MenuItem = optionsMenu.Append(ID_ANY, 'Ask for Multiple Import Files\tF7')

        menuBar.Append(optionsMenu, "&Options")

        frameTop.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self._displayNoUmlFrameDialog,  noUmlFrameItem)
        self.Bind(EVT_MENU, self._displayNoSelectionDialog, noSelectedOglObjectsItem)
        self.Bind(EVT_MENU, self._displayFileImportDialog,  askForFileToImportItem)
        self.Bind(EVT_MENU, self._displayFileExportDialog,  askForFileExportItem)

        self.Bind(EVT_MENU, self._displayMultipleFileImportDialog, askForMultipleImportFilesItem)

        self.Bind(EVT_MENU, self._displayImportDirectoryDialog, askForImportDirectoryItem)
        self.Bind(EVT_MENU, self._displayExportDirectoryDialog, askForExportDirectoryItem)

        frameTop.Bind(EVT_CLOSE, self._onCloseFrame)

        frameTop.Show(True)

        return True

    # noinspection PyUnusedLocal
    def _displayNoUmlFrameDialog(self, event: CommandEvent):
        SamplePluginInterface.displayNoUmlFrame()

    # noinspection PyUnusedLocal
    def _displayNoSelectionDialog(self, event: CommandEvent):
        SamplePluginInterface.displayNoSelectedOglObjects()

    # noinspection PyUnusedLocal
    def _displayFileImportDialog(self, event: CommandEvent):
        ans: SingleFileRequestResponse = self._plugin.askForFileToImport(startDirectory=None)
        self.logger.info(f'_displayFileImportDialog: `{ans}`')

    # noinspection PyUnusedLocal
    def _displayFileExportDialog(self, event: CommandEvent):
        ans: SingleFileRequestResponse = self._plugin.askForFileToExport()

        self.logger.info(f'_displayFileExportDialog: `{ans}`')

    # noinspection PyUnusedLocal
    def _displayMultipleFileImportDialog(self, event: CommandEvent):

        ans: MultipleFileRequestResponse = self._plugin.askToImportMultipleFiles(startDirectory='/tmp')

        self.logger.info(f'_displayMultipleFileImportDialog: `{ans}`')

    # noinspection PyUnusedLocal
    def _displayImportDirectoryDialog(self, event: CommandEvent):
        ans: ImportDirectoryResponse = self._plugin.askForImportDirectoryName()

        self.logger.info(f'_displayImportDirectoryDialog: `{ans}`')

    # noinspection PyUnusedLocal
    def _displayExportDirectoryDialog(self, event: CommandEvent):

        ans = self._plugin.askForExportDirectoryName(preferredDefaultPath=None)

        self.logger.info(f'_displayExportDirectoryDialog: `{ans}`')

    def _onCloseFrame(self, evt: CommandEvent):
        evt.Skip()


# noinspection PyUnusedLocal
def main(sysArgv):
    testApp: App = TestSamplePluginInterface()
    testApp.MainLoop()


if __name__ == "__main__":
    main(argv)
