
from typing import cast

from logging import Logger
from logging import getLogger

from tests.scaffoldv2.PyutDiagramType import PyutDiagramType
from tests.scaffoldv2.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class PyutDocument:

    def __init__(self, diagramType: PyutDiagramType =  PyutDiagramType.CLASS_DIAGRAM):

        self._diagramType: PyutDiagramType = diagramType
        self.logger:       Logger          = getLogger(__name__)

        self._title:        str = cast(str, None)
        self._diagramFrame: UmlDiagramsFrame = cast(UmlDiagramsFrame, None)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, theNewValue: str):
        self._title = theNewValue

    @property
    def diagramFrame(self) -> UmlDiagramsFrame:
        """
        Return the document's uml diagram frame

        Returns:    this document's frame
        """
        return self._diagramFrame

    @diagramFrame.setter
    def diagramFrame(self, umlDiagramsFrame: UmlDiagramsFrame):
        self._diagramFrame = umlDiagramsFrame
