
from typing import Dict
from typing import List
from typing import NewType
from typing import TYPE_CHECKING
from typing import Union

from wx import NewIdRef

if TYPE_CHECKING:
    from core.IOPluginInterface import IOPluginInterface
    from core.ToolPluginInterface import ToolPluginInterface

PluginName        = NewType('PluginName', str)
PluginExtension   = NewType('PluginExtension', str)
PluginDescription = NewType('PluginDescription', str)

PluginType = Union['ToolPluginInterface', 'IOPluginInterface']
#
#  Both of these hold the class types for the Plugins
#
PluginIDMap  = NewType('PluginIDMap', Dict[NewIdRef, PluginType])
PluginList   = NewType('PluginList',  List[PluginType])
