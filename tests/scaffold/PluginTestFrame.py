
from typing import Callable

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from os import getcwd

from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FileSelector
from wx import ICON_ERROR
from wx import ID_EXIT

from wx import Frame
from wx import Menu
from wx import MenuBar

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MessageDialog

from wx import NewIdRef
from wx import OK
from wx import Yield as wxYield

from untanglepyut.UnTangler import Document
from untanglepyut.UnTangler import UnTangler
from untanglepyut.UnTangler import UntangledOglClasses

from pyutplugincore.IOPluginInterface import IOPluginInterface
from pyutplugincore.PluginManager import PluginManager
from pyutplugincore.ToolPluginInterface import ToolPluginInterface
from pyutplugincore.coretypes.PluginDataTypes import PluginIDMap
from tests.plugintester.DisplayUmlFrame import DisplayUmlFrame

from tests.scaffold.ScaffoldCommunicator import ScaffoldCommunicator


@dataclass
class RequestResponse:
    cancelled:     bool      = False
    fileName: str = ''


class PluginTestFrame(Frame):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def __init__(self, parent=None, wxId=FRAME_ID, size=(800, 600), title='Plugin Test Scaffold'):

        super().__init__(parent=parent, id=wxId,  size=size, style=DEFAULT_FRAME_STYLE, title=title)

        diagramFrame: DisplayUmlFrame = DisplayUmlFrame(self, self)
        diagramFrame.SetSize((PluginTestFrame.WINDOW_WIDTH, PluginTestFrame.WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        diagramFrame.Show(True)

        self.logger:         Logger               = getLogger(__name__)
        self._pluginManager: PluginManager        = PluginManager()
        self._communicator:  ScaffoldCommunicator = ScaffoldCommunicator(umlFrame=diagramFrame)

        self._status = self.CreateStatusBar()
        self._status.SetStatusText('Ready!')

        self._loadXmlFileWxId: int             = NewIdRef()
        self._selectAllWxId:   int             = NewIdRef()
        self._displayUmlFrame: DisplayUmlFrame = diagramFrame

        self._createApplicationMenuBar()

    def loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: full qualified file name
        """
        self._loadXmlFile(fqFileName=fqFileName)

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    def _createApplicationMenuBar(self):

        menuBar:   MenuBar = MenuBar()
        fileMenu:  Menu = Menu()
        editMenu:  Menu = Menu()
        toolsMenu: Menu = Menu()

        fileMenu  = self._makeFileMenu(fileMenu)
        editMenu  = self._makeEditMenu(editMenu)
        toolsMenu = self._makeToolsMenu(toolsMenu)

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(editMenu, 'Edit')
        menuBar.Append(toolsMenu, 'Tools')

        self.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self.Close, id=ID_EXIT)

    def _makeFileMenu(self, fileMenu: Menu) -> Menu:

        fileMenu.Append(self._loadXmlFileWxId, 'Load Xml Diagram')

        importSubMenu: Menu = self._makeImportSubMenu()
        exportSubMenu: Menu = self._makeExportSubMenu()

        fileMenu.AppendSubMenu(importSubMenu, 'Import')
        fileMenu.AppendSubMenu(exportSubMenu, 'Export')
        self.Bind(EVT_MENU, self._onLoadXmlFile, id=self._loadXmlFileWxId)

        return fileMenu

    def _makeEditMenu(self, editMenu: Menu) -> Menu:

        editMenu.Append(self._selectAllWxId, 'Select All')

        self.Bind(EVT_MENU, self._onSelectAll, id=self._selectAllWxId)
        return editMenu

    # noinspection PyUnusedLocal
    def _onSelectAll(self, event: CommandEvent):
        shapes = self._displayUmlFrame.GetDiagram().GetShapes()
        for shape in shapes:
            shape.SetSelected(True)
            self._displayUmlFrame.GetSelectedShapes()

        self._displayUmlFrame.SetSelectedShapes(shapes)
        self._displayUmlFrame.Refresh()

    # noinspection PyUnusedLocal
    def _onLoadXmlFile(self, event: CommandEvent):

        response: RequestResponse = self._askForXMLFileToImport()
        self.logger.info(f'{response=}')

        self._loadXmlFile(fqFileName=response.fileName)

    def _askForXMLFileToImport(self) -> RequestResponse:
        """
        Called to ask for a file to import

        Returns:  The request response named tuple
        """
        file: str = FileSelector(
            "Choose a file to import",
            default_path=getcwd(),
            default_extension='xml',
            flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR
        )
        response: RequestResponse = RequestResponse()
        if file == '':
            response.cancelled = True
            response.fileName = ''
        else:
            response.cancelled = False
            response.fileName = file

        return response

    def _loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: Fully qualified file name
        """
        untangler: UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

        assert untangler.documents is not None, 'Bug!'
        documentNames = list(untangler.documents.keys())
        document: Document = untangler.documents[documentNames[0]]
        oglClasses: UntangledOglClasses = document.oglClasses

        for oglClass in oglClasses:
            oglClass.SetDraggable(True)
            self._displayUmlFrame.addShape(oglObject=oglClass)

        self._displayUmlFrame.Refresh()

    def _makeToolsMenu(self, toolsMenu: Menu) -> Menu:
        """
        Make the Tools submenu.
        """
        pluginMap: PluginIDMap = self._pluginManager.toolPluginsMap

        for wxId in pluginMap:

            clazz: type = pluginMap[wxId]   # type: ignore

            pluginInstance: ToolPluginInterface = clazz(None)
            toolsMenu.Append(wxId, pluginInstance.menuTitle)

            self.Bind(EVT_MENU, self._onTools, id=wxId)

        return toolsMenu

    def _makeImportSubMenu(self) -> Menu:
        """
        Returns: The import submenu.
        """
        pluginMap: PluginIDMap = self._pluginManager.inputPluginsMap

        return self._makeIOSubMenu(pluginMap=pluginMap)

    def _makeExportSubMenu(self) -> Menu:
        """
        Returns:  The export submenu
        """
        pluginMap: PluginIDMap = self._pluginManager.outputPluginsMap

        return self._makeIOSubMenu(pluginMap=pluginMap)

    def _makeIOSubMenu(self, pluginMap: PluginIDMap) -> Menu:

        subMenu: Menu = Menu()

        for wxId in pluginMap:
            clazz:          type = pluginMap[wxId]   # type: ignore
            pluginInstance: IOPluginInterface = clazz(None)

            if pluginInstance.inputFormat is not None:
                pluginName: str = pluginInstance.inputFormat.name
                subMenu = self.__makeSubMenuEntry(subMenu=subMenu, wxId=wxId, pluginName=pluginName, callback=self._onImport)
            elif pluginInstance.outputFormat is not None:
                pluginName = pluginInstance.outputFormat.name
                subMenu = self.__makeSubMenuEntry(subMenu=subMenu, wxId=wxId, pluginName=pluginName, callback=self._onExport)
            else:
                assert False, 'Unknown Plugin Type'

        return subMenu

    def __makeSubMenuEntry(self, subMenu: Menu, wxId: int, pluginName: str, callback: Callable) -> Menu:

        subMenu.Append(wxId, pluginName)
        self.Bind(EVT_MENU, callback, id=wxId)

        return subMenu

    def _onTools(self, event: CommandEvent):

        wxId: int = event.GetId()
        self.logger.warning(f'{wxId=}')

        pluginMap: PluginIDMap = self._pluginManager.toolPluginsMap

        # TODO: Fix this later for mypy
        clazz: type = pluginMap[wxId]   # type: ignore
        # Create a plugin instance
        pluginInstance: ToolPluginInterface = clazz(communicator=self._communicator)

        if pluginInstance.setOptions() is True:
            # Do plugin functionality
            BeginBusyCursor()
            try:
                pluginInstance.doAction()
                self.logger.debug(f"After tool plugin do action")
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')
            EndBusyCursor()

    def _onImport(self, event: CommandEvent):

        wxId: int = event.GetId()
        self.logger.info(f'Import: {wxId=}')

        clazz:        type              = self._pluginManager.inputPluginsMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(communicator=self._communicator)
        self._doIOAction(methodToCall=plugInstance.executeImport)

    def _onExport(self, event: CommandEvent):

        wxId: int = event.GetId()
        self.logger.info(f'Export: {wxId=}')

        clazz:        type              = self._pluginManager.outputPluginsMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(communicator=self._communicator)
        self._doIOAction(methodToCall=plugInstance.executeExport)

    def _doIOAction(self, methodToCall: Callable):

        try:
            wxYield()
            methodToCall()
        except (ValueError, Exception) as e:
            self.logger.error(f'{e}')
            booBoo: MessageDialog = MessageDialog(parent=None,
                                                  message=f'An error occurred while executing the selected plugin - {e}',
                                                  caption='Error!', style=OK | ICON_ERROR)
            booBoo.ShowModal()
