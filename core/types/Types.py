
from typing import List
from typing import NewType
from typing import Union

from pyutmodel.PyutLink import PyutLink

from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from ogl.OglInterface2 import OglInterface2

OglClasses = NewType('OglClasses',  List[OglClass])
OglLinks   = NewType('OglLinks',    List[OglLink])
PyutLinks  = NewType('PyutLinks',   List[PyutLink])
OglObjects = Union[List[OglObject], OglClasses, OglLinks, List[OglInterface2]]
