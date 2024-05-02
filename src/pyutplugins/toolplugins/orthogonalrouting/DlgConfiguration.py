
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from typing import cast

from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import Size
from wx import SpinCtrl
from wx import StaticText
from wx import StdDialogButtonSizer
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallyadvanced.ui.widgets.DialSelector import DialSelector
from codeallyadvanced.ui.widgets.DialSelector import DialSelectorParameters

from pyorthogonalrouting.Configuration import Configuration


@dataclass
class GlobalBoundsControl:
    label:        str
    spinCtrl:     SpinCtrl
    value:        int
    minValue:     int
    maxValue:     int


MIN_GLOBAL_BOUND: int = 0
MAX_GLOBAL_BOUND: int = 10000

GlobalBoundsControls = NewType('GlobalBoundsControls', List[GlobalBoundsControl])

NO_SPIN_CTRL: SpinCtrl = cast(SpinCtrl, None)


class DlgConfiguration(SizedDialog):

    def __init__(self, parent: Window):

        style:   int  = DEFAULT_DIALOG_STYLE
        dlgSize: Size = Size(475, 300)

        super().__init__(parent, title='Orthogonal Connector Routing Configuration', size=dlgSize, style=style)

        self.logger: Logger = getLogger(__name__)

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('horizontal')
        sizedPanel.SetSizerProps(proportion=1)

        configuration: Configuration = Configuration()

        self._left:   SpinCtrl = NO_SPIN_CTRL
        self._top:    SpinCtrl = NO_SPIN_CTRL
        self._width:  SpinCtrl = NO_SPIN_CTRL
        self._height: SpinCtrl = NO_SPIN_CTRL

        self._globalBoundsControls: GlobalBoundsControls = GlobalBoundsControls(
            [
                GlobalBoundsControl('Left:',    self._left,   configuration.globalBounds.left,   MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
                GlobalBoundsControl('Top: ',    self._top,    configuration.globalBounds.top,    MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
                GlobalBoundsControl('Width:',   self._width,  configuration.globalBounds.width,  MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
                GlobalBoundsControl('Height: ', self._height, configuration.globalBounds.height, MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
            ]
        )
        self._configuration: Configuration = configuration
        self._layoutControls(parent=sizedPanel)
        self._layoutStandardOkCancelButtonSizer()

    def _layoutStandardOkCancelButtonSizer(self):
        """
        Call this last when creating controls; Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        buttSizer: StdDialogButtonSizer = self.CreateStdDialogButtonSizer(OK | CANCEL)

        self.SetButtonSizer(buttSizer)
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    def _layoutControls(self, parent: SizedPanel):

        localPanel: SizedPanel = SizedPanel(parent)
        localPanel.SetSizerType('horizontal')
        localPanel.SetSizerProps(expand=True, proportion=2)

        shapeMarginParameters: DialSelectorParameters = DialSelectorParameters(minValue=1, maxValue=100, dialLabel='Shape Margin',
                                                                               formatValueCallback=self._formatShapeMargin,
                                                                               valueChangedCallback=self._shapeChanged)

        shapeMargin:           DialSelector = DialSelector(localPanel, parameters=shapeMarginParameters)
        shapeMargin.tickFrequency = 50
        shapeMargin.tickValue     = 2
        shapeMargin.value         = self._configuration.shapeMargin

        globalBoundsMarginParameters: DialSelectorParameters = DialSelectorParameters(minValue=1, maxValue=100, dialLabel='Global Bounds Margin',
                                                                                      formatValueCallback=self._formatGlobalBoundsMargin,
                                                                                      valueChangedCallback=self._globalBoundsMarginChanged)

        globalBoundsMargin:           DialSelector = DialSelector(localPanel, parameters=globalBoundsMarginParameters)
        globalBoundsMargin.tickFrequency = 50
        globalBoundsMargin.tickValue     = 2
        globalBoundsMargin.value         = self._configuration.globalBoundsMargin

        self._layoutGlobalBounds(parent=parent)

    def _layoutGlobalBounds(self, parent: SizedPanel):

        labelBox: SizedStaticBox = SizedStaticBox(parent=parent, label='Global Bounds')
        labelBox.SetSizerProps(expand=True, proportion=2)

        localPanel: SizedPanel = SizedPanel(labelBox)
        localPanel.SetSizerType('form')
        localPanel.SetSizerProps(expand=True, proportion=2)

        for c in self._globalBoundsControls:
            control: GlobalBoundsControl = cast(GlobalBoundsControl, c)
            StaticText(parent=localPanel, label=control.label)
            control.spinCtrl = SpinCtrl(localPanel, id=ID_ANY, size=(30, 25))
            control.spinCtrl.SetRange(MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND)
            control.spinCtrl.SetValue(control.value)
            control.spinCtrl.SetSizerProps(expand=True)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        """
        self.EndModal(OK)

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        """
        self.EndModal(CANCEL)

    def _shapeChanged(self, newValue: int):
        self._configuration.shapeMargin = newValue

    def _globalBoundsMarginChanged(self, newValue: int):
        self._configuration.globalBoundsMargin = newValue

    def _formatShapeMargin(self, valueToFormat: int):
        return f'{valueToFormat}'

    def _formatGlobalBoundsMargin(self, valueToFormat: int):
        return f'{valueToFormat}'
