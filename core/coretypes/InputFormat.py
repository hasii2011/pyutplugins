
from core.coretypes.PluginDataTypes import PluginDescription
from core.coretypes.PluginDataTypes import PluginExtension
from core.coretypes.PluginDataTypes import FormatName

from core.coretypes.BaseFormat import BaseFormat


class InputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, formatName: FormatName, extension: PluginExtension, description: PluginDescription):
        super().__init__(formatName=formatName, extension=extension, description=description)
