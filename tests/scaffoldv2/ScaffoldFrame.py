from typing import List
from typing import cast
from typing import Callable

from logging import Logger
from logging import getLogger

from os import getcwd

from dataclasses import dataclass

from wx import ACCEL_CTRL
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FileDialog
from wx import ID_OK
from wx import OK
from wx import ICON_ERROR
from wx import ID_EXIT
from wx import ID_SELECTALL
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU

from wx import CommandEvent
from wx import Frame
from wx import Menu
from wx import MenuBar

from wx import AcceleratorEntry
from wx import AcceleratorTable
from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MessageDialog
from wx import NewIdRef

from wx import Yield as wxYield

from miniogl.DiagramFrame import DiagramFrame

from core.IOPluginInterface import IOPluginInterface
from core.PluginManager import PluginManager
from core.ToolPluginInterface import ToolPluginInterface

from core.types.PluginDataTypes import IOPluginMap
from core.types.PluginDataTypes import IOPluginMapType
from core.types.PluginDataTypes import PluginIDMap
from tests.scaffold.ScaffoldMediator import ScaffoldMediator
from tests.scaffoldv2.ScaffoldUI import ScaffoldUI


@dataclass
class RequestResponse:
    cancelled: bool = False
    fileName:  str  = ''


class ScaffoldFrame(Frame):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def __init__(self, parent=None, wxId=FRAME_ID, size=(800, 600)):

        super().__init__(parent=parent, id=wxId,  size=size, style=DEFAULT_FRAME_STYLE, title='Test Scaffold for Plugins')

        self.logger:           Logger           = getLogger(__name__)
        self._pluginManager:   PluginManager    = PluginManager()
        self._mediator:        ScaffoldMediator = ScaffoldMediator(umlFrame=cast(DiagramFrame, None))
        self._loadXmlFileWxId: int              = NewIdRef()

        self._status = self.CreateStatusBar()
        self._status.SetStatusText('Ready!')

        self._scaffoldUI: ScaffoldUI = ScaffoldUI(topLevelFrame=self)

        self._createApplicationMenuBar()

        self.__setupKeyboardShortCuts()

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    def loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: full qualified file name
        """
        # self._loadXmlFile(fqFileName=fqFileName)
        pass

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

        self._loadXmlFileWxId: int  = NewIdRef()

        self.Bind(EVT_MENU, self.Close, id=ID_EXIT)

    def _makeFileMenu(self, fileMenu: Menu) -> Menu:

        fileMenu.Append(self._loadXmlFileWxId, 'Load Xml Diagram')

        importSubMenu: Menu = self._makeImportSubMenu()
        exportSubMenu: Menu = self._makeExportSubMenu()

        fileMenu.AppendSubMenu(importSubMenu, 'Import')
        fileMenu.AppendSubMenu(exportSubMenu, 'Export')
        self.Bind(EVT_MENU, self._onLoadXmlFile, id=self._loadXmlFileWxId)

        return fileMenu

    # noinspection PyUnusedLocal
    def _onLoadXmlFile(self, event: CommandEvent):

        response: RequestResponse = self._askForXMLFileToImport()
        self.logger.info(f'{response=}')
        if response.cancelled is False:
            self._loadXmlFile(fqFileName=response.fileName)

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

    def _makeEditMenu(self, editMenu: Menu) -> Menu:

        editMenu.Append(ID_SELECTALL)

        self.Bind(EVT_MENU, self._onSelectAll, id=ID_SELECTALL)
        return editMenu

    # noinspection PyUnusedLocal
    def _onSelectAll(self, event: CommandEvent):
        # shapes = self._displayUmlFrame.GetDiagram().GetShapes()
        # for shape in shapes:
        #     shape.SetSelected(True)
        #     self._displayUmlFrame.GetSelectedShapes()
        #
        # self._displayUmlFrame.SetSelectedShapes(shapes)
        # self._displayUmlFrame.Refresh()
        pass

    # TODO  Start these belong in a separate class
    def _onTools(self, event: CommandEvent):

        wxId: int = event.GetId()
        self.logger.debug(f'{wxId=}')

        pluginMap: PluginIDMap = self._pluginManager.toolPluginsIDMap

        # TODO: Fix this later for mypy
        clazz: type = pluginMap[wxId]   # type: ignore
        # Create a plugin instance
        pluginInstance: ToolPluginInterface = clazz(mediator=self._mediator)

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

        idMap:        PluginIDMap       = self._pluginManager.inputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(mediator=self._mediator)
        self._doIOAction(methodToCall=plugInstance.executeImport)

    def _onExport(self, event: CommandEvent):

        wxId: int = event.GetId()
        self.logger.info(f'Export: {wxId=}')

        idMap:        PluginIDMap      = self._pluginManager.outputPluginsMap.pluginIdMap
        clazz:        type              = idMap[wxId]     # type: ignore
        plugInstance: IOPluginInterface = clazz(mediator=self._mediator)
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

    def _loadXmlFile(self, fqFileName: str):
        """
        This code belongs in another class
        Args:
            fqFileName: Fully qualified file name
        """
        # untangler: UnTangler = UnTangler(fqFileName=fqFileName)
        #
        # untangler.untangle()
        #
        # assert untangler.documents is not None, 'Bug!'
        #
        # documentNames = list(untangler.documents.keys())
        # document: Document = untangler.documents[documentNames[0]]
        #
        # self._mediator.umlFrame.Scroll(document.scrollPositionX, document.scrollPositionY)
        # self._mediator.umlFrame.SetScrollRate(document.pixelsPerUnitX, document.pixelsPerUnitY)
        #
        # oglClasses: UntangledOglClasses = document.oglClasses
        # oglLinks:   UntangledOglLinks   = document.oglLinks
        # oglNotes:   UntangledOglNotes   = document.oglNotes
        #
        # for oglClass in oglClasses:
        #     oglClass.SetDraggable(True)
        #     self._displayUmlFrame.addShape(oglObject=oglClass)
        #
        # for oglLink in oglLinks:
        #     if isinstance(oglLink, OglInterface2):
        #         self.__displayTheInterfaceLollipops(oglLink)
        #     else:
        #         self._displayUmlFrame.addShape(oglObject=oglLink)
        #         controlPoints = oglLink.GetControlPoints()
        #         for controlPoint in controlPoints:
        #             self._displayUmlFrame.addShape(controlPoint)
        #
        # for oglNote in oglNotes:
        #     self._displayUmlFrame.addShape(oglObject=oglNote)
        #
        # self._displayUmlFrame.Refresh()
        pass

    # TODO End these belong in a separate class

    def _askForXMLFileToImport(self) -> RequestResponse:
        """
        TODO: This belongs in another class

        Called to ask for a file to import

        Returns:  The request response named tuple
        """
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

    def __makeSubMenuEntry(self, subMenu: Menu, wxId: int, pluginName: str, callback: Callable) -> Menu:

        subMenu.Append(wxId, pluginName)
        self.Bind(EVT_MENU, callback, id=wxId)

        return subMenu

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
