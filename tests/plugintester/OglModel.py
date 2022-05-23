from dataclasses import dataclass

from tests.plugintester.MiniDomToOgl import OglClasses
from tests.plugintester.MiniDomToOgl import OglLinks


@dataclass
class OglModel:
    oglClasses: OglClasses = None
    oglLinks:   OglLinks   = None
