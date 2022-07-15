
from core.types.PluginDataTypes import PluginDescription
from core.types.PluginDataTypes import PluginExtension
from core.types.PluginDataTypes import FormatName

from core.types.BaseFormat import BaseFormat


class OutputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, formatName: FormatName, extension: PluginExtension, description: PluginDescription):
        super().__init__(formatName=formatName, extension=extension, description=description)
        super().__init__(formatName=formatName, extension=extension, description=description)

