
from logging import Logger
from logging import getLogger

from wx import App

from tests.TestBase import TestBase
from tests.plugintester.TestPluginFrame import TestPluginFrame
from tests.plugintester.UmlTestFrame import UmlTestFrame


class TestAPlugin(App):

    MINI_GAP:         int = 3
    NOTHING_SELECTED: int = -1

    def OnInit(self):

        TestBase.setUpLogging()
        self.logger: Logger = getLogger(__name__)

        pluginFrame: TestPluginFrame = TestPluginFrame()
        pluginFrame.Show(False)

        self.SetTopWindow(pluginFrame)

        pluginFrame.SetAutoLayout(True)
        # pluginFrame.SetSizer(mainSizer)

        self._umlTestFrame: UmlTestFrame = UmlTestFrame(parent=pluginFrame, frame=pluginFrame)
        pluginFrame.Show(True)

        return True


testApp: App = TestAPlugin(redirect=False)
testApp.MainLoop()
