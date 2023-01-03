
from plugins.core.coretypes.PluginDataTypes import PluginDescription
from plugins.core.coretypes.PluginDataTypes import PluginExtension
from plugins.core.coretypes.PluginDataTypes import FormatName

from plugins.core.coretypes.BaseFormat import BaseFormat


class OutputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, formatName: FormatName, extension: PluginExtension, description: PluginDescription):
        super().__init__(formatName=formatName, extension=extension, description=description)
        super().__init__(formatName=formatName, extension=extension, description=description)

