from tests.scaffold.umlframes.UmlDiagramsFrame import UmlDiagramsFrame


class UmlSequenceDiagramsFrame(UmlDiagramsFrame):
    cdfDebugId: int = 0x00FFF   # UML Sequence Diagrams Frame Debug ID

    def __init__(self, parent):
        """

        Args:
            parent:  The parent window
        """
        super().__init__(parent)

        self._cdfDebugId: int = UmlSequenceDiagramsFrame.cdfDebugId

        UmlSequenceDiagramsFrame.cdfDebugId += 1

        self.clearDiagram()
        self._cdInstances = []
