
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import PluginName

from core.types.BaseFormat import BaseFormat


class OutputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, name: PluginName, extension: PluginExtension, description: PluginDescription):
        super().__init__(name, extension, description)

