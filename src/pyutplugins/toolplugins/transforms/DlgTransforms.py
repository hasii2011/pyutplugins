
from typing import cast

from logging import Logger
from logging import getLogger

from wx.lib.sized_controls import SizedPanel

from codeallybasic.Position import Position

from codeallyadvanced.ui.widgets.PositionControl import PositionControl

from pyutplugins.common.ui.BaseEditDialog import BaseEditDialog


class DlgTransforms(BaseEditDialog):
    def __init__(self, parent):

        super().__init__(parent, title='Transform Values')

        self.logger: Logger = getLogger(__name__)

        self._transformX: int = 10
        self._transformY: int = 10

        self._transformControl: PositionControl = cast(PositionControl, None)

        self._layoutOffsetControl(parent=self.GetContentsPane())
        self._layoutStandardOkCancelButtonSizer()
        self.Fit()
        self.SetMinSize(self.GetSize())

    @property
    def transformX(self) -> int:
        return self._transformX

    @property
    def transformY(self) -> int:
        return self._transformY

    def _layoutOffsetControl(self, parent: SizedPanel):

        positionControl: PositionControl = PositionControl(sizedPanel=parent, displayText='X,Y Transform Increment',
                                                           minValue=5, maxValue=100,
                                                           valueChangedCallback=self._positionChanged,
                                                           setControlsSize=True)
        positionControl.position = Position(x=self._transformX, y=self._transformY)
        self._transformControl = positionControl

    def _positionChanged(self, newPosition: Position):
        self.logger.info(f'Position changed: {newPosition=}')
        self._transformX = newPosition.x
        self._transformY = newPosition.y
        self._valuesChanged = True
