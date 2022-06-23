from logging import Logger
from logging import getLogger

from miniogl.DiagramFrame import DiagramFrame
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import ID_EXIT

from wx import Frame
from wx import Menu
from wx import MenuBar

from wx import BeginBusyCursor
from wx import EndBusyCursor

from pyutplugincore.ICommunicator import ICommunicator
from pyutplugincore.PluginManager import PluginManager
from pyutplugincore.ToolPluginInterface import ToolPluginInterface
from pyutplugincore.coretypes.PluginDataTypes import PluginIDMap
from tests.scaffold.ScaffoldCommunicator import ScaffoldCommunicator


class PluginTestFrame(Frame):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def __init__(self, parent=None, wxId=FRAME_ID, size=(800, 600), title='Plugin Test Scaffold'):

        super().__init__(parent=parent, id=wxId,  size=size, style=DEFAULT_FRAME_STYLE, title=title)

        diagramFrame: DiagramFrame = DiagramFrame(self)
        diagramFrame.SetSize((PluginTestFrame.WINDOW_WIDTH, PluginTestFrame.WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        diagramFrame.Show(True)

        self.logger:         Logger                = getLogger(__name__)
        self._pluginManager: PluginManager        = PluginManager()
        self._communicator:  ScaffoldCommunicator = ScaffoldCommunicator(umlFrame=diagramFrame)

        self._status = self.CreateStatusBar()
        self._status.SetStatusText('Ready!')

        self._createApplicationMenuBar()

    def _createApplicationMenuBar(self):

        menuBar:   MenuBar = MenuBar()
        fileMenu:  Menu = Menu()
        toolsMenu: Menu = Menu()

        toolsMenu = self._makeToolsMenu(toolsMenu)

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(toolsMenu, 'Tools')

        self.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self.Close, id=ID_EXIT)

    def _makeToolsMenu(self, toolsMenu: Menu) -> Menu:
        """
        Make the Tools submenu.
        """
        pluginMap: PluginIDMap = self._pluginManager.toolPluginsMenu

        for wxId in pluginMap:

            clazz: type = pluginMap[wxId]   # type: ignore

            pluginInstance: ToolPluginInterface = clazz(None)
            toolsMenu.Append(wxId, pluginInstance.menuTitle)

            self.Bind(EVT_MENU, self.onTools, id=wxId)

        return toolsMenu

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    def onTools(self, event):

        wxId: int = event.GetId()
        self.logger.warning(f'{wxId=}')

        pluginMap: PluginIDMap = self._pluginManager.toolPluginsMenu

        clazz: type = pluginMap[wxId]
        # Create a plugin instance
        pluginInstance: ToolPluginInterface = clazz(communicator=self._communicator)

        if pluginInstance.setOptions() is True:
            # Do plugin functionality
            BeginBusyCursor()
            try:
                pluginInstance.doAction()
                self.logger.debug(f"After tool plugin do action")
            except (ValueError, Exception) as e:
                # PyutUtils.displayError(An error occurred while executing the selected plugin"), "Error...")
                self.logger.error(f'{e}')
            EndBusyCursor()
