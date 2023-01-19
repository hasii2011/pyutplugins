
from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CENTER

from wx import VERTICAL
from wx import EVT_BUTTON
from wx import EVT_CLOSE
from wx import ID_OK
from wx import OK

from wx import Sizer
from wx import BoxSizer

from wx import NewIdRef

from pyutplugins.common.ui.BaseDlgEdit import BaseDlgEdit
from pyutplugins.common.ui.DimensionsContainer import DimensionsContainer

from pyutplugins.preferences.PluginPreferences import PluginPreferences

from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize


class DlgLayoutSize(BaseDlgEdit):

    HORIZONTAL_GAP: int = 5

    DEFAULT_LAYOUT_WIDTH:  int = 1000
    DEFAULT_LAYOUT_HEIGHT: int = 1000

    DEFAULT_MAX_LAYOUT_WIDTH:  int = 3000
    DEFAULT_MAX_LAYOUT_HEIGHT: int = 3000

    def __init__(self, parent):

        self.__layoutWidthID:  int = NewIdRef()
        self.__layoutHeightID: int = NewIdRef()

        super().__init__(parent, title='Layout Size')

        self.logger:       Logger          = getLogger(__name__)

        self._preferences:  PluginPreferences = PluginPreferences()

        layoutAreaSize: LayoutAreaSize = self._preferences.orthogonalLayoutSize
        self._layoutWidth:  int = layoutAreaSize.width
        self._layoutHeight: int = layoutAreaSize.height

        hs:             Sizer               = self._createDialogButtonsContainer(buttons=OK | CANCEL)
        layoutControls: DimensionsContainer = self.__createLayoutSizeControls()

        mainSizer: BoxSizer = BoxSizer(orient=VERTICAL)

        mainSizer.Add(layoutControls, 0, CENTER)
        mainSizer.Add(hs, 0, CENTER)

        self.SetSizer(mainSizer)

        mainSizer.Fit(self)

        self.Bind(EVT_BUTTON, self._OnCmdOk, id=ID_OK)
        self.Bind(EVT_CLOSE,  self._OnClose)

    @property
    def layoutWidth(self) -> int:
        return self._layoutWidth

    @property
    def layoutHeight(self) -> int:
        return self._layoutHeight

    def __createLayoutSizeControls(self) -> DimensionsContainer:

        self._layoutSizeContainer: DimensionsContainer = DimensionsContainer(parent=self, displayText="Layout Width/Height",
                                                                             minValue=0,
                                                                             maxValue=4096,
                                                                             valueChangedCallback=self.__onSizeChange)

        layoutWidth:  int = self._layoutWidth
        layoutHeight: int = self._layoutHeight
        self._layoutSizeContainer.dimensions = LayoutAreaSize(width=layoutWidth, height=layoutHeight)
        return self._layoutSizeContainer

    def __onSizeChange(self, newValue: LayoutAreaSize):

        self._layoutWidth  = newValue.width
        self._layoutHeight = newValue.height

        self._preferences.orthogonalLayoutSize = newValue
