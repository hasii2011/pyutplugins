
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import EVT_CLOSE
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import ID_CANCEL
from wx import ID_OK
from wx import OK
from wx import RESIZE_BORDER

from wx import Font
from wx import CheckBox
from wx import CommandEvent
from wx import STAY_ON_TOP
from wx import StaticText
from wx import StdDialogButtonSizer
from wx import Window

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pyutplugins.ExternalTypes import DiagnosticInformation
from pyutplugins.ExternalTypes import IntegerList
from pyutplugins.ExternalTypes import Points
from pyutplugins.ExternalTypes import Rectangle

from pyutplugins.IPluginAdapter import IPluginAdapter


class DlgDiagnoseLayout(SizedDialog):

    def __init__(self, parent: Window | None):

        style:   int  = DEFAULT_DIALOG_STYLE | RESIZE_BORDER | STAY_ON_TOP

        super().__init__(parent, title='Orthogonal Connector Routing Diagnosis', style=style)
        self.logger: Logger = getLogger(__name__)

        self._showRulers:          CheckBox = cast(CheckBox, None)
        self._showReferencePoints: CheckBox = cast(CheckBox, None)
        self._showRouteGrid:       CheckBox = cast(CheckBox, None)

        self._diagnosticInformation: DiagnosticInformation = cast(DiagnosticInformation, None)
        self._pluginAdapter:         IPluginAdapter        = cast(IPluginAdapter, None)

        self._doLayout(self.GetContentsPane())
        self._layoutStandardOkButtonSizer()

        self._bindCallbacks(parent=self)

        # self.Fit()
        # self.SetMinSize(self.GetSize())

    def _setDiagnosticInformation(self, diagnosticInformation: DiagnosticInformation):
        self._diagnosticInformation = diagnosticInformation

    def _setPluginAdapter(self, pluginAdapter: IPluginAdapter):
        self._pluginAdapter = pluginAdapter

    # noinspection PyTypeChecker
    diagnosticInformation = property(fget=None, fset=_setDiagnosticInformation, doc='Write only diagnostic information')
    # noinspection PyTypeChecker
    pluginAdapter         = property(fget=None, fset=_setPluginAdapter,         doc='Plugin Adapter')

    def _doLayout(self, parentPanel: SizedPanel):
        self._layoutAlgorithmLayers(sizedPanel=parentPanel)

    def _layoutAlgorithmLayers(self, sizedPanel: SizedPanel):
        container: SizedPanel = SizedPanel(sizedPanel)
        container.SetSizerType('vertical')
        # (["top", "left", "right"], 6))
        container.SetSizerProps(expand=True, proprtion=1, border=(["top"], 24))

        font:  Font       = Font(18, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        title: StaticText = StaticText(container, label='Algorithm Layers')
        title.SetFont(font)

        self._showRulers          = CheckBox(container, label='Rulers')
        self._showReferencePoints = CheckBox(container, label='Reference Points')
        self._showRouteGrid       = CheckBox(container, label='Route Grid')

    def _layoutStandardOkButtonSizer(self):
        """
        Call this last when creating controls; Will take care of
        adding callbacks for the Ok and Cancel buttons
        """
        buttSizer: StdDialogButtonSizer = self.CreateStdDialogButtonSizer(OK)

        self.SetButtonSizer(buttSizer)
        self.Bind(EVT_BUTTON, self._onOk,    id=ID_OK)
        self.Bind(EVT_BUTTON, self._onClose, id=ID_CANCEL)
        self.Bind(EVT_CLOSE,  self._onClose)

    def _bindCallbacks(self, parent):

        parent.Bind(EVT_CHECKBOX, self._onShowRulers,          self._showRulers)
        parent.Bind(EVT_CHECKBOX, self._onShowReferencePoints, self._showReferencePoints)
        parent.Bind(EVT_CHECKBOX, self._onShowRouteGrid,       self._showRouteGrid)

    # noinspection PyUnusedLocal
    def _onOk(self, event: CommandEvent):
        """
        Typically shown non modal
        """
        if self.IsModal() is True:
            self.EndModal(OK)
        else:
            self.Destroy()

    # noinspection PyUnusedLocal
    def _onClose(self, event: CommandEvent):
        """
        Typically shown non modal
1        """
        if self.IsModal() is True:
            self.EndModal(CANCEL)
        else:
            self.Destroy()

    def _onShowRulers(self, event: CommandEvent):

        self._ensureSetupOk()

        if event.IsChecked() is True:
            self._pluginAdapter.showRulers(show=True,
                                           horizontalRulers=self._diagnosticInformation.horizontalRulers,
                                           verticalRulers=self._diagnosticInformation.verticalRulers,
                                           diagramBounds=self._diagnosticInformation.diagramBounds)
        else:
            self._pluginAdapter.showRulers(show=False,
                                           verticalRulers=cast(IntegerList, None),
                                           horizontalRulers=cast(IntegerList, None),
                                           diagramBounds=cast(Rectangle, None)
                                           )

    def _onShowReferencePoints(self, event: CommandEvent):

        self._ensureSetupOk()

        if event.IsChecked() is True:
            self._pluginAdapter.showOrthogonalRoutingPoints(show=True, spots=self._diagnosticInformation.spots)
        else:
            self._pluginAdapter.showOrthogonalRoutingPoints(show=False, spots=cast(Points, None))

    def _onShowRouteGrid(self, event: CommandEvent):

        self._ensureSetupOk()
        if event.IsChecked() is True:
            pass
        else:
            pass

    def _ensureSetupOk(self):
        """
        I know, I know this does nothing when assertions are off;  But this is
        a developer demo and they will be on
        """
        assert self._pluginAdapter is not None, 'Developer error.  Forgot to inject the manager'
        assert self._diagnosticInformation is not None, 'Developer error.  Forgot to inject diagnostic information'
