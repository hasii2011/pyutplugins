
from core.coretypes.PluginDataTypes import PluginDescription
from core.coretypes.PluginDataTypes import PluginExtension
from core.coretypes.PluginDataTypes import PluginName

from core.coretypes.BaseFormat import BaseFormat


class OutputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, name: PluginName, extension: PluginExtension, description: PluginDescription):
        super().__init__(name, extension, description)

