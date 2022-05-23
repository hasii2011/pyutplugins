
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

from pyutplugincore.coretypes.Helper import OglClasses
from pyutplugincore.coretypes.ImportDirectoryResponse import ImportDirectoryResponse
from pyutplugincore.coretypes.MultipleFileRequestResponse import MultipleFileRequestResponse
from pyutplugincore.coretypes.SingleFileRequestResponse import SingleFileRequestResponse

from tests.pyutplugincore.SamplePluginInterface import SamplePluginInterface

from tests.pyutplugincore.SampleICommunicator import SampleICommunicator

from tests.TestBase import TestBase


class TestSampleAbstractPlugin(App):

    FRAME_ID:      int = ID_ANY
    WINDOW_WIDTH:  int = 480
    WINDOW_HEIGHT: int = 240

    def __init__(self):
        App.__init__(self, redirect=False)

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)

        oglObjects:   OglClasses          = OglClasses([])
        communicator: SampleICommunicator = SampleICommunicator()

        self._plugin: SamplePluginInterface = SamplePluginInterface(communicator, oglObjects)

    def OnInit(self):

        frameTop: Frame = Frame(parent=None,
                                id=TestSampleAbstractPlugin.FRAME_ID,
                                title="Test Abstract Plugin",
                                size=(TestSampleAbstractPlugin.WINDOW_WIDTH, TestSampleAbstractPlugin.WINDOW_HEIGHT),
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
        ans: SingleFileRequestResponse = self._plugin.askForFileToImport()
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

        ans = self._plugin.askForExportDirectoryName()

        self.logger.info(f'_displayExportDirectoryDialog: `{ans}`')

    def _onCloseFrame(self, evt: CommandEvent):
        evt.Skip()


# noinspection PyUnusedLocal
def main(sysArgv):
    testApp: App = TestSampleAbstractPlugin()
    testApp.MainLoop()


if __name__ == "__main__":
    main(argv)
