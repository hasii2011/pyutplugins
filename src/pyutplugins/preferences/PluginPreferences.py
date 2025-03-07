
from logging import Logger
from logging import getLogger
from pathlib import Path

from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3
from codeallybasic.PassThroughInterpolation import PassThroughInterpolation

from pyutplugins.ioplugins.mermaid.MermaidDirection import MermaidDirection

from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize

MODULE_NAME:          str = 'pyutplugins'
PREFERENCES_FILENAME: str = f'{MODULE_NAME}.ini'


DEFAULT_ORTHOGONAL_LAYOUT_SIZE:     LayoutAreaSize   = LayoutAreaSize(512, 512)
DEFAULT_ORTHOGONAL_LAYOUT_SIZE_STR: str              = DEFAULT_ORTHOGONAL_LAYOUT_SIZE.__str__()
DEFAULT_MERMAID_DIRECTION:          MermaidDirection = MermaidDirection.RightToLeft
DEFAULT_MERMAID_DIRECTION_STR:      str              = DEFAULT_MERMAID_DIRECTION.value

DEFAULT_PDF_OUTPUT_PATH: Path       = Path('/tmp')

# TODO:  Remove pdfExportFilename when we stop using PyUmlDiagrams

SECTION_PYUT_PLUGINS: ValueDescriptions = ValueDescriptions(
    {
        KeyName('orthogonalLayoutSize'):   ValueDescription(defaultValue=DEFAULT_ORTHOGONAL_LAYOUT_SIZE_STR, deserializer=LayoutAreaSize.deSerialize),
        KeyName('wxImageFileName'):        ValueDescription(defaultValue='WxImageDump'),
        KeyName('pdfExportFileName'):      ValueDescription(defaultValue='PyutExport.pdf'),
        KeyName('sugiyamaStepByStep'):     ValueDescription(defaultValue='False',                                      deserializer=SecureConversions.secureBoolean),
        KeyName('mermaidLayoutDirection'): ValueDescription(defaultValue=DEFAULT_MERMAID_DIRECTION_STR, enumUseValue=True, deserializer=MermaidDirection),
    }
)

SECTION_PDF: ValueDescriptions = ValueDescriptions(
    {
        KeyName('outputPath'):     ValueDescription(defaultValue=str(DEFAULT_PDF_OUTPUT_PATH), deserializer=Path),
        KeyName('title'):          ValueDescription(defaultValue='Created by Pyut IOPdf Plugin'),
        KeyName('dateFormat'):     ValueDescription(defaultValue='%d %b %Y %H:%M'),
        KeyName('exportFileName'): ValueDescription(defaultValue='exportedByPyut.pdf'),
        KeyName('author'):         ValueDescription(defaultValue='Humberto A. Sanchez II'),
        KeyName('title'):          ValueDescription(defaultValue='Generated by Pyut'),
        KeyName('subject'):        ValueDescription(defaultValue='UML Diagram'),
        KeyName('annotationLeft'):         ValueDescription(defaultValue='20.0', deserializer=SecureConversions.secureFloat),
        KeyName('annotationWidth'):        ValueDescription(defaultValue='300.0', deserializer=SecureConversions.secureFloat),
        KeyName('annotationTopOffset'):    ValueDescription(defaultValue='2.0', deserializer=SecureConversions.secureFloat),
        KeyName('annotationHeight'):       ValueDescription(defaultValue='50.0', deserializer=SecureConversions.secureFloat),

    }
)

SECTION_DEBUG: ValueDescriptions = ValueDescriptions(
    {
        KeyName('debugTempFileLocation'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
    }
)


SECTION_FEATURES: ValueDescriptions = ValueDescriptions(
    {
        KeyName('diagnoseOrthogonalRouter'): ValueDescription(defaultValue='True', deserializer=SecureConversions.secureBoolean),
    }
)

PLUGIN_SECTIONS: Sections = Sections(
    {
        SectionName('PyutPlugins'): SECTION_PYUT_PLUGINS,
        SectionName('Pdf'):         SECTION_PDF,
        SectionName('Features'):    SECTION_FEATURES,
        SectionName('Debug'):       SECTION_DEBUG,
    }
)


class PluginPreferences(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):
        self._logger: Logger = getLogger(__name__)

        passThroughInterpolation: PassThroughInterpolation = PassThroughInterpolation(
            ['dateFormat']
        )

        super().__init__(baseFileName=f'{PREFERENCES_FILENAME}', moduleName=MODULE_NAME, sections=PLUGIN_SECTIONS, interpolation=passThroughInterpolation)

        self._configParser.optionxform = str  # type: ignore
