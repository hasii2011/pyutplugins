
from logging import Logger
from logging import getLogger

from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3

from pyutplugins.ioplugins.mermaid.MermaidDirection import MermaidDirection
from pyutplugins.toolplugins.orthogonal.LayoutAreaSize import LayoutAreaSize

MODULE_NAME:          str = 'pyutplugins'
PREFERENCES_FILENAME: str = f'{MODULE_NAME}.ini'


DEFAULT_ORTHOGONAL_LAYOUT_SIZE:     LayoutAreaSize   = LayoutAreaSize(512, 512)
DEFAULT_ORTHOGONAL_LAYOUT_SIZE_STR: str              = DEFAULT_ORTHOGONAL_LAYOUT_SIZE.__str__()
DEFAULT_MERMAID_DIRECTION:          MermaidDirection = MermaidDirection.RightToLeft


SECTION_PYUT_PLUGINS: ValueDescriptions = ValueDescriptions(
    {
        KeyName('orthogonalLayoutSize'):   ValueDescription(defaultValue=DEFAULT_ORTHOGONAL_LAYOUT_SIZE_STR, deserializer=LayoutAreaSize.deSerialize),
        KeyName('wxImageFilename'):        ValueDescription(defaultValue='WxImageDump'),
        KeyName('pdfExportFilename'):      ValueDescription(defaultValue='PyutExport.pdf'),
        KeyName('sugiyamaStepByStep'):     ValueDescription(defaultValue='False',                                      deserializer=SecureConversions.secureBoolean),
        KeyName('mermaidLayoutDirection'): ValueDescription(defaultValue=DEFAULT_MERMAID_DIRECTION, enumUseValue=True, deserializer=MermaidDirection.toEnum),
    }
)


SECTION_DEBUG: ValueDescriptions = ValueDescriptions(
    {
        KeyName('debugTempFileLocation'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
    }
)


SECTION_FEATURES: ValueDescriptions = ValueDescriptions(
    {
    }
)

PLUGIN_SECTIONS: Sections = Sections(
    {
        SectionName('PyutPlugins'): SECTION_PYUT_PLUGINS,
        SectionName('Features'):    SECTION_FEATURES,
        SectionName('Debug'):       SECTION_DEBUG,
    }
)


class PluginPreferences(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):
        self._logger: Logger = getLogger(__name__)

        super().__init__(baseFileName=f'{PREFERENCES_FILENAME}', moduleName=MODULE_NAME, sections=PLUGIN_SECTIONS)
