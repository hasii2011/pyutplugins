
from typing import cast

from logging import Logger
from logging import getLogger

from wx import ICON_ERROR
from wx import MessageDialog
from wx import OK

from ogl.OglLink import OglLink

from pyutplugins.ExternalTypes import OglObjects
from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.common.Common import NO_PARENT_WINDOW

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface

from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.toolplugins.orthogonalrouting.DlgDiagnoseLayout import DiagnosticInformation
from pyutplugins.toolplugins.orthogonalrouting.DlgDiagnoseLayout import DlgDiagnoseLayout

from pyutplugins.toolplugins.orthogonalrouting.DlgOrthoRoutingConfig import DlgOrthoRoutingConfig
from pyutplugins.toolplugins.orthogonalrouting.OrthogonalConnectorAdapter import OrthogonalConnectorAdapter

FORMAT_NAME:        FormatName        = FormatName('Orthogonal Configuration')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('json')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Save Configuration')


class ToolOrthogonalRouting(ToolPluginInterface):

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Orthogonal Routing')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '1.0'

        self._menuTitle = 'Orthogonal Routing'

    def setOptions(self) -> bool:
        with DlgOrthoRoutingConfig(NO_PARENT_WINDOW, pluginAdapter=self._pluginAdapter) as dlg:
            if dlg.ShowModal() == OK:
                return True
            else:
                self.logger.warning(f'Cancelled')
                return False

    def doAction(self):
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):

        self.logger.info(f'_doAction')

        adapter: OrthogonalConnectorAdapter = OrthogonalConnectorAdapter(pluginAdapter=self._pluginAdapter)
        oglLink: OglLink = cast(OglLink, None)
        for el in oglObjects:
            if isinstance(el, OglLink):
                try:
                    oglLink = cast(OglLink, el)
                    success: bool = adapter.runConnector(oglLink=oglLink)
                    if success is False:
                        message: str = f'Could not find an orthogonal route for link: {oglLink}'
                        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Fail', style=OK | ICON_ERROR)
                        booBoo.ShowModal()
                        if self._pluginPreferences.diagnoseOrthogonalRouter is True:

                            dlg: DlgDiagnoseLayout     = DlgDiagnoseLayout(parent=None)
                            dlg.pluginAdapter         = self._pluginAdapter
                            dlg.diagnosticInformation = self._getDiagnosticInformation(adapter=adapter)
                            dlg.Show(True)
                            # with dlg:
                            #     if dlg.ShowModal() == OK:
                            #         self.logger.info('Ok')

                except (AttributeError, TypeError) as e:
                    self.logger.error(f'{e} - {oglLink=}')

    def _getDiagnosticInformation(self, adapter: OrthogonalConnectorAdapter) -> DiagnosticInformation:

        from pyorthogonalrouting.Point import Point
        from pyorthogonalrouting.Point import Points

        from pyutplugins.ExternalTypes import Point as DiagnosticPoint
        from pyutplugins.ExternalTypes import Points as DiagnosticPoints

        referencePoints:  Points           = adapter.referencePoints
        diagnosticPoints: DiagnosticPoints = DiagnosticPoints([])

        for pt in referencePoints:

            point: Point = cast(Point, pt)
            self.logger.info(f'{point=}')

            diagnosticPoint: DiagnosticPoint = DiagnosticPoint(x=point.x, y=point.y)
            diagnosticPoints.append(diagnosticPoint)

        diagnosticInformation: DiagnosticInformation = DiagnosticInformation(
            spots=diagnosticPoints
        )

        return diagnosticInformation
