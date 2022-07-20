
from typing import Dict
from typing import List
from typing import NewType
from typing import Union
from typing import TYPE_CHECKING

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

from wx import NewIdRef

if TYPE_CHECKING:
    from core.IOPluginInterface import IOPluginInterface
    from core.ToolPluginInterface import ToolPluginInterface

PluginType = Union['ToolPluginInterface', 'IOPluginInterface']

#
#  Both of these hold the class types for the Plugins
#
PluginList   = NewType('PluginList',  List[PluginType])
PluginIDMap  = NewType('PluginIDMap', Dict[NewIdRef, PluginType])


def createPlugIdMapFactory() -> PluginIDMap:
    return PluginIDMap({})


PluginName        = NewType('PluginName', str)
FormatName        = NewType('FormatName', str)
PluginExtension   = NewType('PluginExtension', str)
PluginDescription = NewType('PluginDescription', str)


class IOPluginMapType(Enum):
    INPUT_MAP  = 'InputMap'
    OUTPUT_MAP = 'OutputMap'


@dataclass
class IOPluginMap:
    mapType:     IOPluginMapType = IOPluginMapType.INPUT_MAP
    pluginIdMap: PluginIDMap     = field(default_factory=createPlugIdMapFactory)
