
from wx import Size
from wx.lib.sized_controls import SizedPanel

from pyutplugins.common.ui.BaseEditDialog import BaseEditDialog
from pyutplugins.common.ui.preferences.PluginPreferencesPage import PluginPreferencesPage


class ScaffoldPreferencesDialog(BaseEditDialog):

    def __init__(self, parent):

        super().__init__(parent, title='Plugin Preferences', size=Size(width=350, height=400))

        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')

        self._pluginPreferencePage: PluginPreferencesPage = PluginPreferencesPage(parent=sizedPanel)

        self._layoutStandardOkCancelButtonSizer()
        # self.Fit()
        # self.SetMinSize(self.GetSize())
