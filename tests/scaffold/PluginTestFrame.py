
from typing import Callable

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from os import getcwd
from typing import List

from wx import ACCEL_CTRL
from wx import AcceleratorEntry
from wx import AcceleratorTable
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FileDialog
from wx import FileSelector
from wx import ICON_ERROR
from wx import ID_EXIT

from wx import Frame
from wx import ID_OK
from wx import ID_SELECTALL
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
from untanglepyut.UnTangler import UntangledOglLinks

from core.IOPluginInterface import IOPluginInterface
from core.ToolPluginInterface import ToolPluginInterface
from core.PluginManager import PluginManager

from core.types.PluginDataTypes import IOPluginMap
from core.types.PluginDataTypes import IOPluginMapType
from core.types.PluginDataTypes import PluginIDMap

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
        self._displayUmlFrame: DisplayUmlFrame = diagramFrame

        self._createApplicationMenuBar()

        self.__setupKeyboardShortCuts()

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

        editMenu.Append(ID_SELECTALL)

        self.Bind(EVT_MENU, self._onSelectAll, id=ID_SELECTALL)
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
        if response.cancelled is False:
            self._loadXmlFile(fqFileName=response.fileName)

    def _askForXMLFileToImport(self) -> RequestResponse:
        """
        Called to ask for a file to import

        Returns:  The request response named tuple
        """
        # file: str = FileSelector(
        #     message="Choose a file to import",
        #     default_path=getcwd(),
        #     default_extension='*.xml',
        #     flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR
        # )
        dlg = FileDialog(None, "Choose a file", getcwd(), "", "*.xml", FD_OPEN | FD_FILE_MUST_EXIST)

        response: RequestResponse = RequestResponse()
        if dlg.ShowModal() != ID_OK:
            dlg.Destroy()
            response.cancelled = True
        else:
            fileNames: List[str] = dlg.GetPaths()
            file:      str       = fileNames[0]

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

        self._communicator.umlFrame.Scroll(document.scrollPositionX, document.scrollPositionY)
        self._communicator.umlFrame.SetScrollRate(document.pixelsPerUnitX, document.pixelsPerUnitY)

        oglClasses: UntangledOglClasses = document.oglClasses
        oglLinks:   UntangledOglLinks   = document.oglLinks

        for oglClass in oglClasses:
            oglClass.SetDraggable(True)
            self._displayUmlFrame.addShape(oglObject=oglClass)

        for oglLink in oglLinks:
            self._displayUmlFrame.addShape(oglObject=oglLink)

        self._displayUmlFrame.Refresh()

    def _makeToolsMenu(self, toolsMenu: Menu) -> Menu:
        """
        Make the Tools submenu.
        """
        pluginMap: PluginIDMap = self._pluginManager.toolPluginsIDMap

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
        pluginMap: IOPluginMap = self._pluginManager.inputPluginsMap

        return self._makeIOSubMenu(pluginMap=pluginMap)

    def _makeExportSubMenu(self) -> Menu:
        """
        Returns:  The export submenu
        """
        pluginMap: IOPluginMap = self._pluginManager.outputPluginsMap

        return self._makeIOSubMenu(pluginMap=pluginMap)

    def _makeIOSubMenu(self, pluginMap: IOPluginMap) -> Menu:

        subMenu: Menu = Menu()

        pluginIDMap: PluginIDMap = pluginMap.pluginIdMap
        for wxId in pluginIDMap:
            clazz:          type = pluginIDMap[wxId]   # type: ignore
            pluginInstance: IOPluginInterface = clazz(None)

            if pluginMap.mapType == IOPluginMapType.INPUT_MAP:
                pluginName: str = pluginInstance.inputFormat.formatName
                subMenu = self.__makeSubMenuEntry(subMenu=subMenu, wxId=wxId, pluginName=pluginName, callback=self._onImport)
            elif pluginMap.mapType == IOPluginMapType.OUTPUT_MAP:
                pluginName = pluginInstance.outputFormat.formatName
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

        pluginMap: PluginIDMap = self._pluginManager.toolPluginsIDMap

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

        idMap: PluginIDMap              = self._pluginManager.outputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
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

    def __setupKeyboardShortCuts(self):
        lst = [
            (ACCEL_CTRL, ord('l'), self._loadXmlFileWxId),
            ]
        acc = []
        for el in lst:
            (el1, el2, el3) = el
            acc.append(AcceleratorEntry(el1, el2, el3))
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)
