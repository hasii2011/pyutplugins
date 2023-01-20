
from pyutplugins.coretypes.PluginDataTypes import PluginDescription
from pyutplugins.coretypes.PluginDataTypes import PluginExtension
from pyutplugins.coretypes.PluginDataTypes import FormatName

from pyutplugins.coretypes.BaseFormat import BaseFormat


class InputFormat(BaseFormat):
    """
    Syntactic sugar
    """
    def __init__(self, formatName: FormatName, extension: PluginExtension, description: PluginDescription):
        super().__init__(formatName=formatName, extension=extension, description=description)
