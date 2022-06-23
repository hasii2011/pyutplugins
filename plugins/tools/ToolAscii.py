
from logging import Logger
from logging import getLogger

from pyutplugincore.ToolPluginInterface import ToolPluginInterface
from pyutplugincore.coretypes.ExportDirectoryResponse import ExportDirectoryResponse
from pyutplugincore.coretypes.Helper import OglClasses

from pyutplugincore.ICommunicator import ICommunicator


class ToolAscii(ToolPluginInterface):

    def __init__(self, communicator: ICommunicator):

        super().__init__(communicator)

        self.logger: Logger = getLogger(__name__)

        self._name      = 'ASCII Class export'
        self._author    = 'Philippe Waelti <pwaelti@eivd.ch>'
        self._version   = '1.0'

        self._menuTitle = 'ASCII Class Export'

        self._exportDirectory: str = ''

    def setOptions(self) -> bool:

        response: ExportDirectoryResponse = self.askForExportDirectoryName()
        if response.cancelled is True:
            return False
        else:
            self._exportDirectory = response.directoryName
            self.logger.debug(f'selectedDir: {self._exportDirectory}')
            return True

    def doAction(self):
        """

        """
        selectedObjects = self._communicator.selectedOglObjects
        if len(selectedObjects) < 1:
            self.displayNoSelectedOglObjects()
            return
        self._write(selectedObjects)

    def _write(self, oglObjects: OglClasses):
        """
        Write the data to a file
        Args:
            oglObjects:   The objects to export
        """
