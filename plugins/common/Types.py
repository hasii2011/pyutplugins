
from typing import cast
from typing import Dict
from typing import List
from typing import NewType

from dataclasses import dataclass

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink

from plugins.common.ElementTreeData import ElementTreeData

ClassTree  = NewType('ClassTree', Dict[str, ElementTreeData])    # string is ClassName
OglClasses = NewType('OglClasses', List[OglClass])
OglLinks   = NewType('OglLinks',  List[OglLink])
PyutLinks  = NewType('PyutLinks', List[PyutLink])


@dataclass
class ClassPair:

    pyutClass: PyutClass = cast(PyutClass, None)
    oglClass:  OglClass  = cast(OglClass, None)
