
from typing import cast

from logging import Logger
from logging import getLogger

from wx import OK
from wx import Window


from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface
from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.toolplugins.forcedirectedlayout.DlgConfiguration import DlgConfiguration


NO_PARENT_WINDOW = cast(Window, None)


class ToolForceDirectedLayout(ToolPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):
        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Force Directed Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '1.0'

        self._menuTitle = 'Force Directed Layout'

    def setOptions(self) -> bool:

        with DlgConfiguration(NO_PARENT_WINDOW) as dlg:
            if dlg.ShowModal() == OK:
                return True
            else:
                self.logger.warning(f'Cancelled')
                return False

    def doAction(self):
        self._pluginAdapter.selectAllOglObjects()
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):
        pass
