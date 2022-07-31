
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglLink import OglLink

from core.ICommunicator import ICommunicator
from core.ToolPluginInterface import ToolPluginInterface

from core.types.PluginDataTypes import PluginName

from plugins.common.Types import OglClasses


class ToolArrangeLinks(ToolPluginInterface):

    def __init__(self, communicator: ICommunicator):

        super().__init__(communicator)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Arrange Links')
        self._author    = 'Cedric DUTOIT <dutoitc@shimbawa.ch>'
        self._version   = '1.1'

        self._menuTitle = 'Arrange links'

    def setOptions(self) -> bool:
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        Returns:
            If `False`, the import is cancelled.
        """
        return True

    def doAction(self):

        self._communicator.selectAllOglObjects()
        oglObjects: OglClasses = self._communicator.selectedOglObjects

        for oglObject in oglObjects:
            if isinstance(oglObject, OglLink):
                oglLink: OglLink = cast(OglLink, oglObject)
                self.logger.info(f"Optimizing: {oglLink}")
                oglLink.optimizeLine()
            else:
                self.logger.warning(f"No line optimizing for: {oglObject}")

        self._communicator.refreshFrame()
