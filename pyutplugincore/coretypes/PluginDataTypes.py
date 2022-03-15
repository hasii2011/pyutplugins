from typing import Dict
from typing import NewType

PluginName        = NewType('PluginName', str)
PluginExtension   = NewType('PluginExtension', str)
PluginDescription = NewType('PluginDescription', str)

PluginMap    = NewType('PluginMap',    Dict[int, type])
