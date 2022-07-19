
from typing import Union
from typing import cast
from typing import Dict
from typing import List
from typing import NewType

from dataclasses import dataclass

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink

from plugins.common.ElementTreeData import ElementTreeData

ClassTree  = NewType('ClassTree',  Dict[str, ElementTreeData])    # string is ClassName
OglClasses = NewType('OglClasses', List[OglClass])
OglLinks   = NewType('OglLinks',   List[OglLink])
PyutLinks  = NewType('PyutLinks',  List[PyutLink])

OglObjects = Union[List[OglObject], OglClasses, OglLinks, List[OglInterface2]]


@dataclass
class ClassPair:

    pyutClass: PyutClass = cast(PyutClass, None)
    oglClass:  OglClass  = cast(OglClass, None)
