
from pyutplugincore.coretypes.PluginDataTypes import PluginDescription
from pyutplugincore.coretypes.PluginDataTypes import PluginExtension
from pyutplugincore.coretypes.PluginDataTypes import PluginName

from pyutplugincore.coretypes.BaseFormat import BaseFormat


class OutputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, name: PluginName, extension: PluginExtension, description: PluginDescription):
        super().__init__(name, extension, description)

