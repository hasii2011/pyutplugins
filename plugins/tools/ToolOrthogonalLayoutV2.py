
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from time import time

from miniogl.DiagramFrame import DiagramFrame
from ogl.OglNote import OglNote
from wx import ICON_ERROR
from wx import OK

from wx import MessageBox

from wx import Yield as wxYield

from miniogl.Shape import Shape
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from core.IMediator import IMediator

from core.ToolPluginInterface import ToolPluginInterface

from core.types.PluginDataTypes import PluginName
from plugins.common.Types import OglObjects

from plugins.tools.orthogonal.DlgLayoutSize import DlgLayoutSize
from plugins.tools.orthogonal.OrthogonalAdapter import LayoutAreaSize
from plugins.tools.orthogonal.OrthogonalAdapter import OglCoordinate
from plugins.tools.orthogonal.OrthogonalAdapter import OglCoordinates
from plugins.tools.orthogonal.OrthogonalAdapter import OrthogonalAdapter
from plugins.tools.orthogonal.OrthogonalAdapterException import OrthogonalAdapterException


class ToolOrthogonalLayoutV2(ToolPluginInterface):

    """
    Version 2 of this plugin.  Does not depend on python-tulip.  Instead, it depends on a homegrown
    version
    """
    def __init__(self, mediator: IMediator):

        super().__init__(mediator)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Orthogonal Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '2.1'

        self._menuTitle = 'Orthogonal Layout V2'

    def setOptions(self) -> bool:

        with DlgLayoutSize(self._mediator.umlFrame) as dlg:
            dlgLayoutSize: DlgLayoutSize = cast(DlgLayoutSize, dlg)
            if dlgLayoutSize.ShowModal() == OK:
                self.logger.warning(f'Retrieved data: layoutWidth: {dlgLayoutSize.layoutWidth} layoutHeight: {dlgLayoutSize.layoutHeight}')
                self._layoutWidth  = dlgLayoutSize.layoutWidth
                self._layoutHeight = dlgLayoutSize.layoutHeight
            else:
                self.logger.warning(f'Cancelled')

        return True

    def doAction(self):

        selectedObjects: OglObjects = self._mediator.selectedOglObjects

        try:
            orthogonalAdapter: OrthogonalAdapter = OrthogonalAdapter(umlObjects=selectedObjects)

            layoutAreaSize: LayoutAreaSize = LayoutAreaSize(self._layoutWidth, self._layoutHeight)
            orthogonalAdapter.doLayout(layoutAreaSize)
        except OrthogonalAdapterException as oae:
            MessageBox(f'{oae}', 'Error', OK | ICON_ERROR)
            return

        umlFrame: DiagramFrame = self._mediator.umlFrame

        if orthogonalAdapter is not None:
            self._reLayoutNodes(selectedObjects, umlFrame, orthogonalAdapter.oglCoordinates)
            self._reLayoutLinks(selectedObjects, umlFrame)

    def _reLayoutNodes(self, umlObjects: List[OglClass], umlFrame: DiagramFrame, oglCoordinates: OglCoordinates):
        """

        Args:
            umlObjects:
            umlFrame:
        """

        for umlObj in umlObjects:
            if isinstance(umlObj, OglClass) or isinstance(umlObj, OglNote):
                oglName: str = umlObj.pyutObject.name
                oglCoordinate: OglCoordinate = oglCoordinates[oglName]

                self._stepNodes(umlObj, oglCoordinate)
            self._animate(umlFrame)

    def _reLayoutLinks(self, umlObjects: List[OglClass], umlFrame: DiagramFrame):

        for oglObject in umlObjects:
            if isinstance(oglObject, OglLink):
                oglLink: OglLink = cast(OglLink, oglObject)
                oglLink.optimizeLine()
            self._animate(umlFrame)

    def _stepNodes(self, srcShape: Shape, oglCoordinate: OglCoordinate):

        oldX, oldY = srcShape.GetPosition()
        newX: int = oglCoordinate.x
        newY: int = oglCoordinate.y

        self.logger.info(f'{srcShape} - oldX,oldY: ({oldX},{oldY}) newX,newY: ({newX},{newY})')
        #
        srcShape.SetPosition(newX, newY)

    def _animate(self, umlFrame: DiagramFrame):
        """
        Does an animation simulation

        Args:
            umlFrame:
        """
        umlFrame.Refresh()
        self.logger.debug(f'Refreshing ...............')
        wxYield()
        t = time()
        while time() < t + 0.05:
            pass