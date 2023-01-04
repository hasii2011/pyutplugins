
from plugins.coretypes.PluginDataTypes import PluginDescription
from plugins.coretypes.PluginDataTypes import PluginExtension
from plugins.coretypes.PluginDataTypes import FormatName

from plugins.coretypes.BaseFormat import BaseFormat


class OutputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, formatName: FormatName, extension: PluginExtension, description: PluginDescription):
        super().__init__(formatName=formatName, extension=extension, description=description)
