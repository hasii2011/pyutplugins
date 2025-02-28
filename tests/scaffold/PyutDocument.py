
from typing import cast

from logging import Logger
from logging import getLogger

from tests.scaffold.PyutDiagramType import PyutDiagramType
from tests.scaffold.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame


class PyutDocument:

    def __init__(self, diagramType: PyutDiagramType = PyutDiagramType.CLASS_DIAGRAM):

        self._diagramType: PyutDiagramType = diagramType
        self.logger:       Logger          = getLogger(__name__)

        self._title:        str = cast(str, None)
        self._diagramFrame: UmlClassDiagramsFrame = cast(UmlClassDiagramsFrame, None)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, theNewValue: str):
        self._title = theNewValue

    @property
    def diagramType(self) -> PyutDiagramType:
        """
        Read-only property

        Returns:  The diagram type
        """
        return self._diagramType

    @property
    def diagramFrame(self) -> UmlClassDiagramsFrame:
        """
        Return the document's uml diagram frame

        Returns:    this document's frame
        """
        return self._diagramFrame

    @diagramFrame.setter
    def diagramFrame(self, umlClassDiagramsFrame: UmlClassDiagramsFrame):
        self._diagramFrame = umlClassDiagramsFrame
