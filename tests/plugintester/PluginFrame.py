
from typing import cast

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FRAME_EX_METAL
from wx import Frame
from wx import ID_ANY
from wx import ID_EXIT
from wx import Menu
from wx import MenuBar
from wx import MenuEvent

from wx import NewIdRef as wxNewIdRef

from tests.plugintester.DiagramLoader import DiagramLoader
from tests.plugintester.DisplayUmlFrame import DisplayUmlFrame
from tests.plugintester.MiniDomToOgl import OglClasses
from tests.plugintester.OglModel import OglModel


class TestPluginFrame(Frame):

    ID_LOAD_OGL:      int = wxNewIdRef()
    ID_LOAD_PYUT:     int = wxNewIdRef()
    ID_CLEAR_DIAGRAM: int = wxNewIdRef()

    def __init__(self):

        super().__init__(parent=None, id=ID_ANY, title="Test A Plugin", size=(1024, 768), style=DEFAULT_FRAME_STYLE | FRAME_EX_METAL)

        menuBar: MenuBar = MenuBar()

        fileMenu:  Menu = Menu()

        fileMenu.Append(ID_EXIT, "E&xit", "Exit Tester")
        fileMenu.Append(TestPluginFrame.ID_LOAD_OGL,  'Display O&gl',  'Display an Ogl Diagram')
        fileMenu.Append(TestPluginFrame.ID_LOAD_PYUT, 'Display &Pyut', 'Display a Pyut Diagram')
        fileMenu.AppendSeparator()
        fileMenu.Append(TestPluginFrame.ID_CLEAR_DIAGRAM, 'Clear Diagram', 'Remove shapes from Diagram')

        menuBar.Append(fileMenu,  "&File")

        self.Bind(EVT_MENU, self._displayOglDiagram,  id=TestPluginFrame.ID_LOAD_OGL)
        self.Bind(EVT_MENU, self._displayPyutDiagram, id=TestPluginFrame.ID_LOAD_PYUT)
        self.Bind(EVT_MENU, self._clearDiagram,       id=TestPluginFrame.ID_CLEAR_DIAGRAM)

        self.SetMenuBar(menuBar)

        self._displayUmlFrame: DisplayUmlFrame = cast(DisplayUmlFrame, None)

    @property
    def displayUmlFrame(self) -> DisplayUmlFrame:
        return self._displayUmlFrame

    @displayUmlFrame.setter
    def displayUmlFrame(self, newValue: DisplayUmlFrame):
        self._displayUmlFrame = newValue

    # noinspection PyUnusedLocal
    def _displayOglDiagram(self, event: MenuEvent):

        tdl:      DiagramLoader = DiagramLoader()
        oglModel: OglModel      = tdl.retrieveOglModel()

        self.__displayDiagram(oglModel=oglModel)

    # noinspection PyUnusedLocal
    def _displayPyutDiagram(self, event: MenuEvent):

        tdl:      DiagramLoader = DiagramLoader()
        oglModel: OglModel      = tdl.retrievePyutModel()

        self.__displayDiagram(oglModel=oglModel)

    # noinspection PyUnusedLocal
    def _clearDiagram(self, event: MenuEvent):
        self._displayUmlFrame.clearDiagram()

    def __displayDiagram(self, oglModel: OglModel):
        """
        Display the input model

        Args:
            oglModel:
        """

        oglClasses: OglClasses = oglModel.oglClasses

        for oglClass in oglClasses.values():
            self._displayUmlFrame.addShape(oglClass)

        self._displayUmlFrame.Refresh()
