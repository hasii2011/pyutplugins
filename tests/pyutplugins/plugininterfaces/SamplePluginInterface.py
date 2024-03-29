
from logging import Logger
from logging import getLogger

from pyutplugins.plugininterfaces.BasePluginInterface import BasePluginInterface

from pyutplugins.IPluginAdapter import IPluginAdapter

from pyutplugins.plugintypes.PluginDataTypes import PluginName
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import FormatName

from pyutplugins.plugintypes.InputFormat import InputFormat
from pyutplugins.plugintypes.OutputFormat import OutputFormat


SAMPLE_PLUGIN_NAME: PluginName        = PluginName('Sample Plugin')
SAMPLE_FORMAT_NAME: FormatName        = FormatName('Unspecified Plugin Name')
SAMPLE_EXTENSION:   PluginExtension   = PluginExtension('sample')
SAMPLE_DESCRIPTION: PluginDescription = PluginDescription('Unspecified Plugin Description')


class SamplePluginInterface(BasePluginInterface):
    """
    TODO make this a Sample Tool Plugin
    """

    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name         = SAMPLE_PLUGIN_NAME
        self._author       = 'Ozzee D. Gato'
        self._version      = '1.0'
        self._inputFormat  = InputFormat(formatName=SAMPLE_FORMAT_NAME, extension=SAMPLE_EXTENSION, description=SAMPLE_DESCRIPTION)
        self._outputFormat = OutputFormat(formatName=SAMPLE_FORMAT_NAME, extension=SAMPLE_EXTENSION, description=SAMPLE_DESCRIPTION)
