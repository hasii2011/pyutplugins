
from typing import cast

from logging import Logger
from logging import getLogger

from enum import Enum

from wx import App
from wx import CB_READONLY
from wx import ComboBox
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_COMBOBOX
from wx import ID_ANY
from wx import OK

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from pyutplugins.ioplugins.wximage.DlgWxImageOptions import DlgWxImageOptions
from pyutplugins.toolplugins.orthogonal.DlgLayoutSize import DlgLayoutSize
from pyutplugins.preferences.PluginPreferences import PluginPreferences

from tests.TestBase import TestBase


class DialogNamesEnum(Enum):

    DLG_LAYOUT_SIZE     = 'DlgLayoutSize'
    DLG_WXIMAGE_OPTIONS = 'DlgWxImageOptions'


class TestDialogs(App):

    NOTHING_SELECTED: int = -1

    def __init__(self, redirect: bool):

        TestBase.setUpLogging()

        self.logger:        Logger            = getLogger(__name__)
        self._preferences:  PluginPreferences = PluginPreferences()

        self._frame:       SizedFrame        = cast(SizedFrame, None)

        super().__init__(redirect)

    def OnInit(self):

        TestBase.setUpLogging()

        self._frame = SizedFrame(parent=None, id=ID_ANY, title="Test Plugin Dialogs", size=(300, 100), style=DEFAULT_FRAME_STYLE)

        self._frame.Show(False)
        self.SetTopWindow(self._frame)

        self._layoutSelectionControls(self._frame)
        self._frame.Show(True)

        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        # self._frame.Fit()
        # self._frame.SetMinSize(self._frame.GetSize())

        return True

    def _layoutSelectionControls(self, parentFrame: SizedFrame):

        sizedPanel: SizedPanel = parentFrame.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(expand=True, proportion=1)

        dialogChoices = []
        for dlgName in DialogNamesEnum:
            dialogChoices.append(dlgName.value)

        box: SizedStaticBox = SizedStaticBox(sizedPanel, ID_ANY, "Select Dialog to Test")
        box.SetSizerProps(expand=True, proportion=1)

        self._cmbDlgName: ComboBox = ComboBox(box, choices=dialogChoices, style=CB_READONLY)

        self._cmbDlgName.SetSelection(TestDialogs.NOTHING_SELECTED)

        parentFrame.Bind(EVT_COMBOBOX, self._onDlgNameSelectionChanged, self._cmbDlgName)

    def _onDlgNameSelectionChanged(self, event: CommandEvent):

        dialogName: str = event.GetString()

        dlgNamesEnum: DialogNamesEnum = DialogNamesEnum(dialogName)

        self.logger.warning(f'Selected dialog: {dlgNamesEnum}')

        match dlgNamesEnum:
            case DialogNamesEnum.DLG_WXIMAGE_OPTIONS:
                with DlgWxImageOptions(parent=self._frame) as dlg:
                    if dlg.ShowModal() == OK:
                        self.logger.info(f'{dlg.outputFileName} {dlg.imageFormat=}')
            case DialogNamesEnum.DLG_LAYOUT_SIZE:
                with DlgLayoutSize(parent=self._frame) as dlg:
                    msg: str = f'layout size: '
                    if dlg.ShowModal() == OK:
                        msg = f'New {msg} ({dlg.layoutWidth},{dlg.layoutHeight})'
                    else:
                        msg = f'Old {msg} ({dlg.layoutWidth},{dlg.layoutHeight})'
                    self.logger.info(f'{msg}')
            case _:
                self.logger.warning(f'Unhandled Dialog to test: {dlgNamesEnum}')


testApp: TestDialogs = TestDialogs(redirect=False)

testApp.MainLoop()
