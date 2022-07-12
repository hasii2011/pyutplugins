
from wx import App

from tests.scaffold.PluginTestFrame import PluginTestFrame


class PluginTestScaffold(App):

    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self):

        frameTop: PluginTestFrame = PluginTestFrame(title="Plugin Test Scaffold")

        frameTop.Show(True)

        return True


testApp: App = PluginTestScaffold(redirect=False)

testApp.MainLoop()
