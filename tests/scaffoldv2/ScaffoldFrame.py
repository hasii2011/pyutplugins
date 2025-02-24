
from typing import Union
from typing import List
from typing import Callable

from logging import Logger
from logging import getLogger

from os import getcwd

from dataclasses import dataclass

from wx import ACCEL_CTRL
from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FRAME_FLOAT_ON_PARENT
from wx import ID_OK
from wx import ID_PREFERENCES
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
from wx import FileDialog
from wx import FileSelector

from wx import MessageDialog
from wx import NewIdRef

from oglio.Reader import Reader
from oglio.Types import OglProject

from pyutplugins.PluginManager import PluginDetails
from pyutplugins.PluginManager import PluginManager

from pyutplugins.plugintypes.PluginDataTypes import InputPluginMap
from pyutplugins.plugintypes.PluginDataTypes import OutputPluginMap
from pyutplugins.plugintypes.PluginDataTypes import PluginIDMap
from pyutplugins.plugintypes.PluginDataTypes import PluginMapType

from pyutplugins.plugininterfaces.IOPluginInterface import IOPluginInterface
from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from tests.scaffoldv2.PluginAdapterV2 import PluginAdapterV2
from tests.scaffoldv2.PyutDiagramType import PyutDiagramType
from tests.scaffoldv2.ScaffoldPreferencesDialog import ScaffoldPreferencesDialog
from tests.scaffoldv2.ScaffoldUI import ScaffoldUI
from tests.scaffoldv2.eventengine.EventEngine import EventEngine
from tests.scaffoldv2.eventengine.Events import EventType


@dataclass
class RequestResponse:
    cancelled: bool = False
    fileName:  str  = ''


class ScaffoldFrame(Frame):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 1200
    WINDOW_HEIGHT: int = 600

    def __init__(self, parent=None, wxId=FRAME_ID, size=(WINDOW_WIDTH, WINDOW_HEIGHT), createEmptyProject: bool = True):

        super().__init__(parent=parent, id=wxId,  size=size, style=DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT, title='Test Scaffold for Plugins')

        self.logger:           Logger        = getLogger(__name__)
        self._loadXmlFileWxId: int           = NewIdRef()

        self._status = self.CreateStatusBar()
        self._status.SetStatusText('Ready!')

        self._eventEngine: EventEngine = EventEngine(listeningWindow=self)
        self._scaffoldUI:  ScaffoldUI  = ScaffoldUI(topLevelFrame=self, createEmptyProject=createEmptyProject)

        self._scaffoldUI.eventEngine = self._eventEngine

        self._pluginAdapter: PluginAdapterV2 = PluginAdapterV2(eventEngine=self._eventEngine)
        #
        # The plugin manager needs this to allow the pyutplugins to send us messages
        #
        self._pluginManager:   PluginManager = PluginManager(pluginAdapter=self._pluginAdapter)

        self._createApplicationMenuBar()

        self.__setupKeyboardShortCuts()

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    def loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: full qualified filename
        """
        self._loadXmlFile(fqFileName=fqFileName)

    def _createApplicationMenuBar(self):

        self._loadXmlFileWxId = NewIdRef()

        self._newClassDiagramWxId:    int = NewIdRef()
        self._newUseCaseDiagramWxId:  int = NewIdRef()
        self._newSequenceDiagramWxId: int = NewIdRef()

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

        newDiagramSubMenu: Menu = self._makeNewDiagramSubMenu()
        importSubMenu:     Menu = self._makeImportSubMenu()
        exportSubMenu:     Menu = self._makeExportSubMenu()

        fileMenu.AppendSubMenu(newDiagramSubMenu, 'New')
        fileMenu.AppendSubMenu(importSubMenu, 'Import')
        fileMenu.AppendSubMenu(exportSubMenu, 'Export')

        fileMenu.Append(ID_PREFERENCES, 'Preferences', 'Configure Me')

        self.Bind(EVT_MENU, self._onLoadXmlFile, id=self._loadXmlFileWxId)
        self.Bind(EVT_MENU, self._onPreferences, id=ID_PREFERENCES)

        return fileMenu

    def _makeNewDiagramSubMenu(self) -> Menu:
        subMenu: Menu = Menu()

        subMenu.Append(self._newClassDiagramWxId,    'Class Diagram')
        subMenu.Append(self._newUseCaseDiagramWxId,  'Use Case Diagram')
        subMenu.Append(self._newSequenceDiagramWxId, 'Sequence Diagram')

        self.Bind(EVT_MENU, self._onNewDiagram, id=self._newClassDiagramWxId)
        self.Bind(EVT_MENU, self._onNewDiagram, id=self._newUseCaseDiagramWxId)
        self.Bind(EVT_MENU, self._onNewDiagram, id=self._newSequenceDiagramWxId)
        return subMenu

    def _makeToolsMenu(self, toolsMenu: Menu) -> Menu:
        """
        Make the Tools submenu.
        """
        idMap: PluginIDMap = self._pluginManager.toolPluginsMap.pluginIdMap

        for wxId in idMap:

            clazz: type = idMap[wxId]

            pluginInstance: ToolPluginInterface = clazz(None)
            toolsMenu.Append(wxId, pluginInstance.menuTitle)

            self.Bind(EVT_MENU, self._onTools, id=wxId)

        return toolsMenu

    def _makeImportSubMenu(self) -> Menu:
        """
        Returns: The import submenu.
        """
        pluginMap: InputPluginMap = self._pluginManager.inputPluginsMap

        return self._makeIOSubMenu(pluginMap=pluginMap)

    def _makeExportSubMenu(self) -> Menu:
        """
        Returns:  The export submenu
        """
        pluginMap: OutputPluginMap = self._pluginManager.outputPluginsMap

        return self._makeIOSubMenu(pluginMap=pluginMap)

    def _makeIOSubMenu(self, pluginMap: Union[InputPluginMap, OutputPluginMap]) -> Menu | None:

        subMenu: Menu = Menu()

        for wxId in pluginMap.pluginIdMap.keys():
            clazz:          type = pluginMap.pluginIdMap[wxId]
            pluginInstance: IOPluginInterface = clazz(None)

            if pluginMap.mapType == PluginMapType.INPUT_MAP:
                pluginName: str = pluginInstance.inputFormat.formatName
                subMenu = self.__makeSubMenuEntry(subMenu=subMenu, wxId=wxId, pluginName=pluginName, callback=self._onImport)
            elif pluginMap.mapType == PluginMapType.OUTPUT_MAP:
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
        self._eventEngine.sendEvent(EventType.SelectAllShapes)

    def _onTools(self, event: CommandEvent):

        wxId:          int           = event.GetId()
        pluginDetails: PluginDetails = self._pluginManager.doToolAction(wxId=wxId)
        self.logger.info(f'Tools: {pluginDetails=}')

    def _onImport(self, event: CommandEvent):

        wxId:          int           = event.GetId()
        pluginDetails: PluginDetails = self._pluginManager.doImport(wxId=wxId)
        self.logger.info(f'Import: {pluginDetails=}')

    def _onExport(self, event: CommandEvent):

        wxId:          int           = event.GetId()
        pluginDetails: PluginDetails = self._pluginManager.doExport(wxId=wxId)
        self.logger.info(f'Export: {pluginDetails=}')

    # noinspection PyUnusedLocal
    def _onLoadXmlFile(self, event: CommandEvent):

        wildcard: str = (
            f'Extended Markup Language '
            f' (*, xml '
            f'|*.xml'
        )

        selectedFile: str = FileSelector("Choose a file to import", wildcard=wildcard, flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR)

        if selectedFile != '':
            self._loadXmlFile(selectedFile)

    def _onNewDiagram(self, event: CommandEvent):
        eventId: int = event.GetId()

        if eventId == self._newClassDiagramWxId:
            self._eventEngine.sendEvent(EventType.NewDiagram, diagramType=PyutDiagramType.CLASS_DIAGRAM)

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
            (ACCEL_CTRL, ord('a'), ID_SELECTALL),
            ]
        acc = []
        for el in lst:
            (el1, el2, el3) = el
            acc.append(AcceleratorEntry(el1, el2, el3))
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()

    def _loadXmlFile(self, fqFileName: str):

        reader: Reader = Reader()

        oglProject: OglProject = reader.readXmlFile(fqFileName=fqFileName)

        self._eventEngine.sendEvent(eventType=EventType.LoadOglProject, oglProject=oglProject)

    # noinspection PyUnusedLocal
    def _onPreferences(self, event: CommandEvent):

        with ScaffoldPreferencesDialog(parent=self) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'Ok')
            else:
                self.logger.info(f'Cancel')
