
from typing import cast

from logging import Logger
from logging import getLogger

from wx import OK

from ogl.OglObject import OglObject

from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.common.Common import NO_PARENT_WINDOW

from pyutplugins.plugininterfaces.IOPluginInterface import IPluginAdapter
from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.toolplugins.transforms.DlgTransforms import DlgTransforms


class ToolTransforms(ToolPluginInterface):
    """
     A plugin for making transformations : translation, rotations, ...

    TODO: Explore parameterizing x transform and adding other transforms
    """
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter=pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Transformations')
        self._author    = 'C.Dutoit/Humberto A. Sanchez II'
        self._version   = '1.5'

        self._menuTitle = 'Transformation X/Y'

        self._transformX: int = 0
        self._transformY: int = 0

    def setOptions(self) -> bool:

        with DlgTransforms(parent=NO_PARENT_WINDOW) as dlg:
            if dlg.ShowModal() == OK:
                self.logger.info(f'{dlg.transformX=} {dlg.transformY=}')
                self._transformX = dlg.transformX
                self._transformY = dlg.transformY
                proceed: bool = True
            else:
                proceed = False

        return proceed

    def doAction(self):

        selectedObjects: OglObjects = self._selectedOglObjects

        for obj in selectedObjects:
            oglObject: OglObject = cast(OglObject, obj)
            x, y = oglObject.GetPosition()
            newX: int = x + self._transformX
            newY: int = y + self._transformY

            self.logger.info(f'x,y: {x},{y} - {newX=} {newY=}')
            oglObject.SetPosition(newX, newY)

        self._pluginAdapter.indicatePluginModifiedProject()
        self._pluginAdapter.refreshFrame()
