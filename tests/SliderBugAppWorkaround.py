
from typing import cast

from wx import App
from wx import BoxSizer
from wx import DEFAULT_FRAME_STYLE
from wx import EXPAND
from wx import FRAME_FLOAT_ON_PARENT
from wx import VERTICAL
from wx import ID_ANY
from wx import SL_AUTOTICKS
from wx import SL_HORIZONTAL
from wx import SL_LABELS
from wx import Slider
from wx import Panel

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

WINDOW_WIDTH:  int = 400
WINDOW_HEIGHT: int = 200


class SliderBugApp(App):

    def __init__(self):
        super().__init__()
        self._frameTop: SizedFrame = cast(SizedFrame, None)

    def OnInit(self) -> bool:

        title:          str        = 'Demo Buggy Workaround Slider'
        frameStyle:     int        = DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT

        self._frameTop = SizedFrame(parent=None, id=ID_ANY, size=(WINDOW_WIDTH, WINDOW_HEIGHT), style=frameStyle, title=title)

        sizedPanel:   SizedPanel = self._frameTop.GetContentsPane()
        sliderPanel: Panel      = Panel(sizedPanel)
        sizer:        BoxSizer   = BoxSizer(VERTICAL)

        sliderStyle: int   = SL_HORIZONTAL | SL_AUTOTICKS | SL_LABELS
        slider:     Slider = Slider(sliderPanel, id=ID_ANY, value=100, minValue=25, maxValue=100, style=sliderStyle)

        sizer.Add(slider, 1, EXPAND, 0)
        sliderPanel.SetSizer(sizer)

        self._frameTop.Show(True)

        return True


testApp = SliderBugApp()

testApp.MainLoop()
