from logging import Logger
from logging import getLogger

from core.IMediator import IMediator

from core.ToolPluginInterface import ToolPluginInterface

from core.types.PluginDataTypes import PluginName

from core.types.DataTypes import OglObjects


class ToolTransforms(ToolPluginInterface):
    """
     A plugin for making transformations : translation, rotations, ...

    TODO: Explore parameterizing x transform and adding other transforms
    """
    def __init__(self, mediator: IMediator):

        super().__init__(mediator)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Transformations')
        self._author    = 'C.Dutoit'
        self._version   = '1.1'

        self._menuTitle = 'Transformations'

    def setOptions(self) -> bool:
        return True

    def doAction(self):

        selectedObjects: OglObjects = self._mediator.selectedOglObjects

        (frameW, frameH) = self._mediator.umlFrame.GetSize()
        self.logger.warning(f'frameW: {frameW} - frameH: {frameH}')

        for obj in selectedObjects:
            x, y = obj.GetPosition()
            newX: int = frameW - x
            self.logger.info(f"x,y: {x},{y} - newX: {newX}")
            obj.SetPosition(newX, y)

        self._mediator.refreshFrame()
