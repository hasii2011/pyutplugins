
from typing import Dict
from typing import List
from typing import NewType

PluginName        = NewType('PluginName', str)
PluginExtension   = NewType('PluginExtension', str)
PluginDescription = NewType('PluginDescription', str)

#
#  Both of these hold the class types for the Plugins
#
PluginMap    = NewType('PluginMap',    Dict[int, type])
PluginList   = NewType('PluginList',   List[type])          # Plugin Classes are Callable
