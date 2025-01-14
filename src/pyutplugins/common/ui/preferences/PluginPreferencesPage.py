
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from wx import EVT_BUTTON
from wx import EVT_CHECKBOX
from wx import EVT_CHOICE
from wx import EVT_SPINCTRLDOUBLE
from wx import EVT_TEXT
from wx import ID_ANY
from wx import NB_FIXEDWIDTH
from wx import NB_TOP
from wx import TE_READONLY

from wx import Button
from wx import DirSelector
from wx import CommandEvent
from wx import Notebook
from wx import Size
from wx import SpinCtrlDouble
from wx import StaticText
from wx import TextCtrl
from wx import Window
from wx import CheckBox
from wx import Choice

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from codeallybasic.Dimensions import Dimensions

from codeallyadvanced.ui.widgets.DimensionsControl import DimensionsControl

from pyutplugins.ioplugins.mermaid.MermaidDirection import MermaidDirection

from pyutplugins.preferences.PluginPreferences import PluginPreferences

from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize

TEXT_CTRL_WIDTH:  int  = 125
TEXT_CTRL_HEIGHT: int  = 25
TEXT_CTRL_SIZE:   Size = Size(width=TEXT_CTRL_WIDTH, height=TEXT_CTRL_HEIGHT)

ANNOTATION_MIN_WIDTH:  float = 100.0
ANNOTATION_MAX_WIDTH:  float = 600.0
ANNOTATION_MIN_HEIGHT: float = 25.0
ANNOTATION_MAX_HEIGHT: float = 100.0

PDF_FILENAME_TOOLTIP:         str = 'The default pdf output file name'
PDF_TITLE_TOOLTIP:            str = 'Used as the annotation title and the pdf metadata title'
PDF_AUTHOR_TOOLTIP:           str = 'Used as the pdf metadata author'
PDF_SUBJECT_TOOLTIP:          str = 'Used as the pdf metadata subject'
PDF_ANNOTATION_WIDTH_TOOLTIP: str = 'The max width of the title '


class PluginPreferencesPage(SizedPanel):

    def __init__(self, parent: Window):
        self.logger: Logger = getLogger(__name__)

        super().__init__(parent)
        self.SetSizerType('vertical')
        # noinspection PyUnresolvedReferences
        self.SetSizerProps(expand=True, proportion=1)

        self._preferences: PluginPreferences = PluginPreferences()
        self._imageFileNameWxId: int = wxNewIdRef()

        self._pdfDirectoryWxId:        int = wxNewIdRef()
        self._pdfFileNameWxId:         int = wxNewIdRef()
        self._pdfTitleWxId:            int = wxNewIdRef()
        self._pdfAuthorWxId:           int = wxNewIdRef()
        self._pdfSubjectWxId:          int = wxNewIdRef()
        self._pdfAnnotationWidthWxId:  int = wxNewIdRef()
        self._pdfAnnotationHeightWxId: int = wxNewIdRef()

        self._directorySelectBtn:     Button            = cast(Button, None)
        self._selectedDirectory:      TextCtrl          = cast(TextCtrl, None)
        self._layoutSizeControls:     DimensionsControl = cast(DimensionsControl, None)
        self._stepSugiyama:           CheckBox          = cast(CheckBox, None)
        self._mermaidLayoutDirection: Choice            = cast(Choice, None)

        self._layoutTopLevel(self)

        self._setControlValues()
        parent.Bind(EVT_TEXT, self._onTextValueChange, id=self._pdfFileNameWxId)
        parent.Bind(EVT_TEXT, self._onTextValueChange, id=self._pdfTitleWxId)
        parent.Bind(EVT_TEXT, self._onTextValueChange, id=self._pdfAuthorWxId)
        parent.Bind(EVT_TEXT, self._onTextValueChange, id=self._pdfSubjectWxId)

        parent.Bind(EVT_CHECKBOX, self._onSugiyamaValueChanged,   self._stepSugiyama)
        parent.Bind(EVT_CHOICE,   self._onLayoutDirectionChanged, self._mermaidLayoutDirection)
        parent.Bind(EVT_SPINCTRLDOUBLE, self._onDoubleSpinnerChanged, id=self._pdfAnnotationWidthWxId)
        parent.Bind(EVT_SPINCTRLDOUBLE, self._onDoubleSpinnerChanged, id=self._pdfAnnotationHeightWxId)

        self.Bind(EVT_BUTTON, self._onDirectorySelectClick,   self._directorySelectBtn)

    @property
    def name(self) -> str:
        return 'Plugins'

    def _layoutTopLevel(self, sizedParentPanel: SizedPanel):
        """
        The top level is a 2 tab notebook page
        Args:
            sizedParentPanel:

        """

        style: int = NB_TOP | NB_FIXEDWIDTH
        book: Notebook = Notebook(sizedParentPanel, style=style)
        book.SetSizerProps(expand=True, proportion=1)

        generalSizedPanel: SizedPanel = SizedPanel(book)
        pdfOptionsPanel:   SizedPanel = SizedPanel(book)

        self._layoutGeneralPage(generalSizedPanel=generalSizedPanel)
        self._layoutPdfOptions(pdfOptionsPanel=pdfOptionsPanel)

        book.AddPage(generalSizedPanel, text='General',     select=False)
        book.AddPage(pdfOptionsPanel,   text='Pdf Options', select=True)

    def _layoutGeneralPage(self, generalSizedPanel: SizedPanel):

        self._stepSugiyama = CheckBox(generalSizedPanel, label='Step Sugiyama Layout')

        self._layoutMermaidPreferences(generalSizedPanel)

        self._layoutSizeControls = DimensionsControl(sizedPanel=generalSizedPanel, displayText="Orthogonal Layout Width/Height",
                                                     minValue=100, maxValue=4096,
                                                     valueChangedCallback=self._onLayoutSizeChanged,
                                                     setControlsSize=False)

        self._layoutSizeControls.SetSizerProps(proportion=2, expand=False)

        self._layoutImageNamePreference(parent=generalSizedPanel)

    def _layoutPdfOptions(self, pdfOptionsPanel: SizedPanel):

        sizedForm: SizedPanel = SizedPanel(pdfOptionsPanel)
        sizedForm.SetSizerType('form')
        sizedForm.SetSizerProps(proportion=1, expand=True)

        self._directorySelectBtn = Button(sizedForm, label="&Select Directory",)
        self._directorySelectBtn.SetSizerProps(valign='center')

        self._selectedDirectory = TextCtrl(sizedForm, id=self._pdfDirectoryWxId, value=str(self._preferences.outputPath), size=TEXT_CTRL_SIZE, style=TE_READONLY)
        self._selectedDirectory.SetSizerProps(expand=True)
        self._selectedDirectory.SetToolTip('Fully qualified name, Use left/right arrows keys to view path')

        self._layoutTextInput(sizedForm, wxId=self._pdfFileNameWxId, textLabel='PDF Filename:', textValue=self._preferences.exportFileName, toolTip=PDF_FILENAME_TOOLTIP)
        self._layoutTextInput(sizedForm, wxId=self._pdfTitleWxId,    textLabel='Title:',        textValue=self._preferences.title,          toolTip=PDF_TITLE_TOOLTIP)
        self._layoutTextInput(sizedForm, wxId=self._pdfAuthorWxId,   textLabel='Author:',       textValue=self._preferences.author,         toolTip=PDF_AUTHOR_TOOLTIP)
        self._layoutTextInput(sizedForm, wxId=self._pdfSubjectWxId,  textLabel='Subject:',      textValue=self._preferences.subject,        toolTip=PDF_SUBJECT_TOOLTIP)

        st = StaticText(sizedForm, ID_ANY, 'Annotation Width:')
        st.SetSizerProps(valign='center')
        SpinCtrlDouble(sizedForm,
                       id=self._pdfAnnotationWidthWxId,
                       min=ANNOTATION_MIN_WIDTH,
                       max=ANNOTATION_MAX_WIDTH,
                       value=str(self._preferences.annotationWidth),
                       inc=1.0)

        st = StaticText(sizedForm, ID_ANY, 'Annotation Height:')
        st.SetSizerProps(valign='center')
        SpinCtrlDouble(sizedForm,
                       id=self._pdfAnnotationHeightWxId,
                       min=ANNOTATION_MIN_HEIGHT,
                       max=ANNOTATION_MAX_HEIGHT,
                       value=str(self._preferences.annotationHeight),
                       inc=1.0)

    def _layoutMermaidPreferences(self, parent):

        directions: List[str] = [s.value for s in MermaidDirection]

        ssb: SizedStaticBox = SizedStaticBox(parent, label='Mermaid Diagram Layout Direction')
        ssb.SetSizerProps(proportion=2, expand=False)

        self._mermaidLayoutDirection = Choice(ssb, choices=directions)

    def _layoutImageNamePreference(self, parent: SizedPanel):

        sizedForm: SizedPanel = SizedPanel(parent)
        sizedForm.SetSizerType('form')
        sizedForm.SetSizerProps(proportion=2)

        self._layoutTextInput(sizedForm, wxId=self._imageFileNameWxId, textLabel='Image FileName:', textValue=self._preferences.wxImageFileName)

    def _layoutTextInput(self, sizedForm: SizedPanel, wxId: int, textLabel: str, textValue: str, toolTip: str = ''):
        """
        Layout one line of a text input form
        Args:
            sizedForm:  The parent
            wxId:       The text controls ID (for the callback)
            textLabel:  The left hand label
            textValue:  The current value
        """

        st: StaticText = StaticText(sizedForm, ID_ANY, textLabel)
        st.SetSizerProps(valign='center')
        txt: TextCtrl = TextCtrl(sizedForm, id=wxId, value=textValue, size=TEXT_CTRL_SIZE)
        txt.SetSizerProps(expand=True)
        txt.SetToolTip(toolTip)

    def _setControlValues(self):
        layoutDimensions: Dimensions = Dimensions()
        layoutDimensions.width  = self._preferences.orthogonalLayoutSize.width
        layoutDimensions.height = self._preferences.orthogonalLayoutSize.height

        self._layoutSizeControls.dimensions = layoutDimensions

        self._stepSugiyama.SetValue(self._preferences.sugiyamaStepByStep)

    def _onDoubleSpinnerChanged(self, event: CommandEvent):

        eventID:  int = event.GetId()
        newValue: str = event.GetString()

        match eventID:
            case self._pdfAnnotationWidthWxId:
                self._preferences.annotationWidth = newValue

            case self._pdfAnnotationHeightWxId:
                self._preferences.annotationHeight = newValue
            case _:
                self.logger.error(f'Unknown spinner event id')

    def _onTextValueChange(self, event: CommandEvent):
        """
        Generic handler for any text controls
        Args:
            event:
        """

        eventID:  int = event.GetId()
        newValue: str = event.GetString()

        match eventID:
            case self._imageFileNameWxId:
                self._preferences.wxImageFileName = newValue
            case self._pdfFileNameWxId:
                self._preferences.exportFileName = newValue
            case self._pdfTitleWxId:
                self._preferences.title = newValue
            case self._pdfAuthorWxId:
                self._preferences.author = newValue
            case self._pdfSubjectWxId:
                self._preferences.subject = newValue
            case _:
                self.logger.error(f'Unknown text change event id')

    def _onLayoutSizeChanged(self, newValue: Dimensions):
        layoutAreaSize: LayoutAreaSize = LayoutAreaSize(width=newValue.width, height=newValue.height)
        self._preferences.orthogonalLayoutSize = layoutAreaSize
        self._valuesChanged = True

    def _onSugiyamaValueChanged(self, event: CommandEvent):

        newValue: bool = event.IsChecked()
        self._preferences.sugiyamaStepByStep = newValue

    # noinspection PyUnusedLocal
    def _onLayoutDirectionChanged(self, event: CommandEvent):
        idx:     int = self._mermaidLayoutDirection.GetSelection()
        enumStr: str = self._mermaidLayoutDirection.GetString(idx)

        prefValue: MermaidDirection = MermaidDirection.toEnum(enumStr=enumStr)

        self._preferences.mermaidLayoutDirection = prefValue

    # noinspection PyUnusedLocal
    def _onDirectorySelectClick(self, event: CommandEvent):

        selectedDirectory: str = DirSelector('Choose a PDF output folder', default_path=str(self._preferences.outputPath))

        self.logger.info(f'{selectedDirectory}')

        if selectedDirectory != '':
            self._preferences.outputPath = selectedDirectory
            self._selectedDirectory.SetValue(selectedDirectory)
