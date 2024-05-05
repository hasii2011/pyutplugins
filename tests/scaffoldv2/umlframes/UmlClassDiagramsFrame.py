from ogl.events.OglEventEngine import OglEventEngine

from tests.scaffoldv2.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

DEFAULT_WIDTH = 16000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20


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

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

    @property
    def eventEngine(self) -> OglEventEngine:
        return self._oglEventEngine
