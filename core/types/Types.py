
from typing import Dict
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from dataclasses import dataclass
from dataclasses import field

from enum import Enum

from pyutmodel.PyutLink import PyutLink

from ogl.OglObject import OglObject
from ogl.OglInterface2 import OglInterface2
from ogl.OglActor import OglActor
from ogl.OglNote import OglNote
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage

OglClasses  = NewType('OglClasses',  List[OglClass])
OglLinks    = NewType('OglLinks',    List[OglLink])
OglNotes    = NewType('OglNotes',    List[OglNote])
OglTexts    = NewType('OglTexts',    List[OglText])
OglActors   = NewType('OglActors',   List[OglActor])
OglUseCases = NewType('OglUseCases', List[OglUseCase])

OglSDInstances = NewType('OglSDInstances', Dict[int, OglSDInstance])
OglSDMessages  = NewType('OglSDMessages',  Dict[int, OglSDMessage])

OglObjects = Union[OglClasses, OglLinks, OglNotes, OglTexts, OglActors, OglUseCases]


PyutLinks  = NewType('PyutLinks',   List[PyutLink])


def createPluginClassesFactory() -> OglClasses:
    """
    Factory method to create  the OglClasses data structure;

    Returns:  A new data structure
    """
    return OglClasses([])


def createPluginLinksFactory() -> OglLinks:
    """
    Factory method to create  the OglLinks data structure;

    Returns:  A new data structure
    """
    return OglLinks([])


def createPluginNotesFactory() -> OglNotes:
    return OglNotes([])


def createOglTextsFactory() -> OglTexts:
    return OglTexts([])


def createPluginActorsFactory() -> OglActors:
    return OglActors([])


def createPluginUseCasesFactory() -> OglUseCases:
    return OglUseCases([])


def createPluginSDInstances() -> OglSDInstances:
    return OglSDInstances({})


def createPluginSDMessages() -> OglSDMessages:
    return OglSDMessages({})


PluginDocumentTitle = NewType('PluginDocumentTitle', str)


class PluginDocumentType(Enum):

    CLASS_DIAGRAM    = 'Class Diagram'
    SEQUENCE_DIAGRAM = 'Sequence Diagram'
    USECASE_DIAGRAM  = 'Use Case Diagram'
    UNKNOWN_DIAGRAM  = 'Unknown'

    @classmethod
    def toEnum(cls, enumStr: str) -> 'PluginDocumentType':

        assert (enumStr is not None) and (enumStr != ''), 'I need a real string dude'
        # TODO use switch statement when we get to 3.10.x
        if enumStr == 'CLASS_DIAGRAM':
            retEnum: PluginDocumentType = PluginDocumentType.CLASS_DIAGRAM
        elif enumStr == 'SEQUENCE_DIAGRAM':
            retEnum = PluginDocumentType.SEQUENCE_DIAGRAM
        elif enumStr == 'USECASE_DIAGRAM':
            retEnum = PluginDocumentType.USECASE_DIAGRAM
        else:
            assert False, 'Unknown diagram type'

        return retEnum

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


@dataclass
class PluginDocument:
    """
    This is a plugin's version of a document
    """
    documentType:    PluginDocumentType  = PluginDocumentType.UNKNOWN_DIAGRAM
    documentTitle:   PluginDocumentTitle = PluginDocumentTitle('')
    scrollPositionX: int = -1
    scrollPositionY: int = -1
    pixelsPerUnitX:  int = -1
    pixelsPerUnitY:  int = -1
    oglClasses:      OglClasses     = field(default_factory=createPluginClassesFactory)
    oglLinks:        OglLinks       = field(default_factory=createPluginLinksFactory)
    oglNotes:        OglNotes       = field(default_factory=createPluginNotesFactory)
    oglTexts:        OglTexts       = field(default_factory=createOglTextsFactory)
    oglActors:       OglActors      = field(default_factory=createPluginActorsFactory)
    oglUseCases:     OglUseCases    = field(default_factory=createPluginUseCasesFactory)
    oglSDInstances:  OglSDInstances = field(default_factory=createPluginSDInstances)
    oglSDMessages:   OglSDMessages  = field(default_factory=createPluginSDMessages)


PluginDocuments     = NewType('PluginDocuments', dict[PluginDocumentTitle, PluginDocument])


def createPluginDocumentsFactory() -> PluginDocuments:
    return PluginDocuments({})


@dataclass
class PluginProject:
    """
    This is a plugin's version of a project
    """
    version:         str             = cast(str, None)
    codePath:        str             = cast(str, None)
    pluginDocuments: PluginDocuments = field(default_factory=createPluginDocumentsFactory)
