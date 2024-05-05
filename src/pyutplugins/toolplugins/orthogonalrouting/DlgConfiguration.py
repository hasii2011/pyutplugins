
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import BORDER_DEFAULT
from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_ANY
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import RESIZE_BORDER
from wx import Size
from wx import SpinCtrl
from wx import StaticText
from wx import StdDialogButtonSizer
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyorthogonalrouting.Configuration import Configuration
from pyorthogonalrouting.Rect import Rect

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.toolplugins.orthogonalrouting.LabelledSlider import LabelledSlider

from pyutplugins.ExternalTypes import ObjectBoundaries


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

    def __init__(self, parent: Window, pluginAdapter: IPluginAdapter):

        self._pluginAdapter: IPluginAdapter = pluginAdapter
        self._configuration: Configuration  = cast(Configuration, None)

        style:   int  = DEFAULT_DIALOG_STYLE | RESIZE_BORDER
        dlgSize: Size = Size(475, 300)

        super().__init__(parent, title='Orthogonal Connector Routing Configuration', size=dlgSize, style=style)
        self.logger: Logger = getLogger(__name__)

        self._left:   SpinCtrl = NO_SPIN_CTRL
        self._top:    SpinCtrl = NO_SPIN_CTRL
        self._width:  SpinCtrl = NO_SPIN_CTRL
        self._height: SpinCtrl = NO_SPIN_CTRL

        self._sizedPanel: SizedPanel = self.GetContentsPane()
        self._sizedPanel.SetSizerType('horizontal')

        self._pluginAdapter.getObjectBoundaries(callback=self._objectBoundariesCallback)
        #
        # Doing this since that it appears that using the above callback messes
        # with the layout
        #
        self.PostSizeEvent()

    def _objectBoundariesCallback(self, objectBoundaries: ObjectBoundaries):
        """
        Get the updated object boundaries

        Args:
            objectBoundaries:

        """
        self._configuration = Configuration()

        width:     int  = objectBoundaries.maxX - objectBoundaries.minX
        height:    int  = objectBoundaries.maxY - objectBoundaries.minY
        newBounds: Rect = Rect(top=objectBoundaries.minY, left=objectBoundaries.minX, width=width, height=height)

        self._configuration.globalBounds = newBounds

        self.logger.info(f'{self._configuration.globalBounds=}')
        self._doLayout()

    def _doLayout(self):

        self._layoutControls(parent=self._sizedPanel)
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

        localPanel: SizedPanel = SizedPanel(parent, style=BORDER_DEFAULT)
        localPanel.SetSizerType('vertical')
        localPanel.SetSizerProps(expand=True, proportion=2)

        shapeMargin:        LabelledSlider = LabelledSlider(sizedPanel=localPanel, label='Shape Margin',         value=22, minValue=0, maxValue=100, size=Size(325, height=-1))
        globalBoundsMargin: LabelledSlider = LabelledSlider(sizedPanel=localPanel, label='Global Bounds Margin', value=44, minValue=0, maxValue=100, size=Size(325, height=-1))

        shapeMargin.valueChangedHandler        = self._shapeMarginChanged
        globalBoundsMargin.valueChangedHandler = self._globalBoundsMarginChanged

        self._layoutGlobalBounds(parent=parent)

    def _layoutGlobalBounds(self, parent: SizedPanel):

        configuration: Configuration = self._configuration

        globalBoundsControls: GlobalBoundsControls = GlobalBoundsControls(
            [
                GlobalBoundsControl('Left:',    self._left,   configuration.globalBounds.left,   MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
                GlobalBoundsControl('Top: ',    self._top,    configuration.globalBounds.top,    MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
                GlobalBoundsControl('Width:',   self._width,  configuration.globalBounds.width,  MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
                GlobalBoundsControl('Height: ', self._height, configuration.globalBounds.height, MIN_GLOBAL_BOUND, MAX_GLOBAL_BOUND),
            ]
        )

        labelBox: SizedStaticBox = SizedStaticBox(parent=parent, label='Global Bounds')
        labelBox.SetSizerProps(expand=True, proportion=1)

        localPanel: SizedPanel = SizedPanel(labelBox)
        localPanel.SetSizerType('form')
        localPanel.SetSizerProps(expand=True)

        for c in globalBoundsControls:
            control: GlobalBoundsControl = cast(GlobalBoundsControl, c)
            StaticText(parent=localPanel, label=control.label)
            control.spinCtrl = SpinCtrl(localPanel, id=ID_ANY, size=(25, -1))
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

    def _shapeMarginChanged(self, event: CommandEvent):
        self._configuration.shapeMargin = event.GetInt()

    def _globalBoundsMarginChanged(self, event: CommandEvent):
        self._configuration.globalBoundsMargin = event.GetInt()
