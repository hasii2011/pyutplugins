from ogl.events.OglEventEngine import OglEventEngine

from tests.scaffoldv2.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class UmlClassDiagramsFrame(UmlDiagramsFrame):

    cdfDebugId: int = 0x000FF   # UML Class Diagrams Frame Debug ID

    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionality from UmlDiagramsFrame, but
    it knows the structure of a class diagram and it can load class diagram data.
    """
    def __init__(self, parent):
        """
        """

        self._cdfDebugId: int = UmlClassDiagramsFrame.cdfDebugId

        UmlClassDiagramsFrame.cdfDebugId += 1

        super().__init__(parent)
        self.clearDiagram()     # Used to be .newDiagram

        self._oglEventEngine: OglEventEngine = OglEventEngine(listeningWindow=self)

    @property
    def eventEngine(self) -> OglEventEngine:
        return self._oglEventEngine
