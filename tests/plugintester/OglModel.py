
from dataclasses import field
from dataclasses import dataclass

from tests.plugintester.MiniDomToOgl import OglClasses
from tests.plugintester.MiniDomToOgl import OglLinks


@dataclass
class OglModel:
    """
    TODO:  Figure out how to properly annotate fields that are lists for dictionaries
    """
    oglClasses: OglClasses = field(default_factory=dict)    # type: ignore
    oglLinks:   OglLinks   = field(default_factory=list)    # type: ignore
