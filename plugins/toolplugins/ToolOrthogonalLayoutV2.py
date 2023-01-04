
from typing import cast

from logging import Logger
from logging import getLogger

from time import time

from wx import ICON_ERROR
from wx import OK

from wx import MessageBox

from wx import Yield as wxYield

from miniogl.Shape import Shape

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote

from plugins.coreinterfaces.IPluginAdapter import IPluginAdapter
from plugins.coreinterfaces.ToolPluginInterface import ToolPluginInterface

from plugins.CoreTypes import OglObjects

from plugins.coretypes.PluginDataTypes import PluginName

from plugins.toolplugins.orthogonal.DlgLayoutSize import DlgLayoutSize
from plugins.toolplugins.orthogonal.OrthogonalAdapter import LayoutAreaSize
from plugins.toolplugins.orthogonal.OrthogonalAdapter import OglCoordinate
from plugins.toolplugins.orthogonal.OrthogonalAdapter import OglCoordinates
from plugins.toolplugins.orthogonal.OrthogonalAdapter import OrthogonalAdapter
from plugins.toolplugins.orthogonal.OrthogonalAdapterException import OrthogonalAdapterException


class ToolOrthogonalLayoutV2(ToolPluginInterface):

    """
    Version 2 of this plugin.  Does not depend on python-tulip.  Instead, it depends on a homegrown
    version
    """
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._layoutWidth:  int = 0
        self._layoutHeight: int = 0

        self._name      = PluginName('Orthogonal Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '2.1'

        self._menuTitle = 'Orthogonal Layout V2'

    def setOptions(self) -> bool:

        with DlgLayoutSize(None) as dlg:
            dlgLayoutSize: DlgLayoutSize = cast(DlgLayoutSize, dlg)
            if dlgLayoutSize.ShowModal() == OK:
                self.logger.warning(f'Retrieved data: layoutWidth: {dlgLayoutSize.layoutWidth} layoutHeight: {dlgLayoutSize.layoutHeight}')
                self._layoutWidth  = dlgLayoutSize.layoutWidth
                self._layoutHeight = dlgLayoutSize.layoutHeight
            else:
                self.logger.warning(f'Cancelled')

        return True

    def doAction(self):

        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)
        # selectedObjects: OglObjects = self._pluginAdapter.selectedOglObjects
        #
        # try:
        #     orthogonalAdapter: OrthogonalAdapter = OrthogonalAdapter(umlObjects=selectedObjects)
        #
        #     layoutAreaSize: LayoutAreaSize = LayoutAreaSize(self._layoutWidth, self._layoutHeight)
        #     orthogonalAdapter.doLayout(layoutAreaSize)
        # except OrthogonalAdapterException as oae:
        #     MessageBox(f'{oae}', 'Error', OK | ICON_ERROR)
        #     return
        #
        # umlFrame: DiagramFrame = self._pluginAdapter.umlFrame
        #
        # if orthogonalAdapter is not None:
        #     self._reLayoutNodes(selectedObjects, umlFrame, orthogonalAdapter.oglCoordinates)
        #     self._reLayoutLinks(selectedObjects, umlFrame)

    def _doAction(self, selectedObjects: OglObjects):

        try:
            orthogonalAdapter: OrthogonalAdapter = OrthogonalAdapter(umlObjects=selectedObjects)

            layoutAreaSize: LayoutAreaSize = LayoutAreaSize(self._layoutWidth, self._layoutHeight)
            orthogonalAdapter.doLayout(layoutAreaSize)
        except OrthogonalAdapterException as oae:
            MessageBox(f'{oae}', 'Error', OK | ICON_ERROR)
            return

        if orthogonalAdapter is not None:
            self._reLayoutNodes(selectedObjects, orthogonalAdapter.oglCoordinates)
            self._reLayoutLinks(selectedObjects)
            self._pluginAdapter.indicatePluginModifiedProject()

    def _reLayoutNodes(self, umlObjects: OglObjects, oglCoordinates: OglCoordinates):
        """

        Args:
            umlObjects:
        """

        for umlObj in umlObjects:
            if isinstance(umlObj, OglClass) or isinstance(umlObj, OglNote):
                oglName: str = umlObj.pyutObject.name
                oglCoordinate: OglCoordinate = oglCoordinates[oglName]

                self._stepNodes(umlObj, oglCoordinate)
            self._animate()

    def _reLayoutLinks(self, umlObjects: OglObjects):

        for oglObject in umlObjects:
            if isinstance(oglObject, OglLink):
                oglLink: OglLink = cast(OglLink, oglObject)
                oglLink.optimizeLine()
            self._animate()

    def _stepNodes(self, srcShape: Shape, oglCoordinate: OglCoordinate):

        oldX, oldY = srcShape.GetPosition()
        newX: int = oglCoordinate.x
        newY: int = oglCoordinate.y

        self.logger.info(f'{srcShape} - oldX,oldY: ({oldX},{oldY}) newX,newY: ({newX},{newY})')
        #
        srcShape.SetPosition(newX, newY)

    def _animate(self):
        """
        Does an animation simulation
        """
        # umlFrame.Refresh()
        self._pluginAdapter.refreshFrame()
        self.logger.debug(f'Refreshing ...............')
        wxYield()
        t = time()
        while time() < t + 0.05:
            pass
