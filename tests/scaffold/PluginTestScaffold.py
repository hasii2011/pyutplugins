
from wx import App

from tests.scaffold.PluginTestFrame import PluginTestFrame


class PluginTestScaffold(App):

    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self):

        frameTop: PluginTestFrame = PluginTestFrame(title="Plugin Test Scaffold")
                                                    # size=(PluginTestScaffold.WINDOW_WIDTH, PluginTestScaffold.WINDOW_HEIGHT))
        frameTop.Show(True)

        # diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        # diagramFrame.SetSize((PluginTestScaffold.WINDOW_WIDTH, PluginTestScaffold.WINDOW_HEIGHT))
        # diagramFrame.SetScrollbars(10, 10, 100, 100)
        #
        # diagramFrame.Show(True)

        # self.SetTopWindow(diagramFrame)

        # self._diagramFrame: DiagramFrame = diagramFrame

        return True


testApp: App = PluginTestScaffold(redirect=False)

testApp.MainLoop()
