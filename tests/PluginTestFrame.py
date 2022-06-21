
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU

from wx import Frame
from wx import ID_EXIT
from wx import Menu
from wx import MenuBar


class PluginTestFrame(Frame):

    FRAME_ID:      int = 0xDeadBeef

    def __init__(self, parent=None, wxId=FRAME_ID, size=(800, 600), title='Plugin Test Scaffold'):

        super().__init__(parent=parent, id=wxId,  size=size, style=DEFAULT_FRAME_STYLE, title=title)

        self._status = self.CreateStatusBar()
        self._status.SetStatusText('Ready!')

        self._createApplicationMenuBar()

    def _createApplicationMenuBar(self):

        menuBar:   MenuBar = MenuBar()
        fileMenu:  Menu = Menu()
        toolsMenu: Menu = Menu()

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(toolsMenu, 'Tools')

        self.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self.Close, id=ID_EXIT)

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    def onTools(self):
        pass
