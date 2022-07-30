
from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglClass import OglClass
from ogl.OglLinkFactory import OglLinkFactory

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType


class LinkMakerMixin:
    """
    Used to aid the plugins when they need to create a link;  Usually not used
    directly by the plugin but by the supplementary classes used by the plugins

    """
    def __init__(self):

        self.logger: Logger = getLogger('LinkMakerMixin')

        self._oglLinkFactory: OglLinkFactory  = OglLinkFactory()

    def createLink(self, src: OglClass, dst: OglClass, linkType: PyutLinkType = PyutLinkType.INHERITANCE):
        """
        Add a paternity link between child and father.

        Args:
            src:  subclass
            dst: Base Class
            linkType:   The type of link

        Returns: an OglLink

        """
        sourceClass:      PyutClass = cast(PyutClass, src.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, dst.pyutObject)

        pyutLink: PyutLink = PyutLink("", linkType=linkType, source=sourceClass, destination=destinationClass)

        oglLink = self._oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        pyutClass: PyutClass = cast(PyutClass, src.pyutObject)
        pyutClass.addLink(pyutLink)

        return oglLink
