
from logging import Logger
from logging import getLogger

from wx import App
from wx import BOTTOM
from wx import BoxSizer
from wx import EXPAND
from wx import VERTICAL

from tests.TestBase import TestBase
from tests.plugintester.PluginFrame import TestPluginFrame
from tests.plugintester.DisplayUmlFrame import DisplayUmlFrame


class PluginTester(App):

    MINI_GAP:         int = 3
    NOTHING_SELECTED: int = -1

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)

        pluginFrame: TestPluginFrame = TestPluginFrame()
        pluginFrame.Show(False)

        self.SetTopWindow(pluginFrame)

        displayUmlFrame: DisplayUmlFrame = DisplayUmlFrame(parent=pluginFrame, frame=pluginFrame)

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        mainSizer.Add(displayUmlFrame, 1, EXPAND | BOTTOM, 10)
        pluginFrame.SetSizer(mainSizer)

        pluginFrame.displayUmlFrame = displayUmlFrame

        pluginFrame.Show(True)

        return True


testApp: App = PluginTester(redirect=False)
testApp.MainLoop()
