
from typing import List
from typing import NewType
from typing import cast

from wx import BLACK_PEN
from wx import Brush
from wx import DC

from wx import PaintDC
from wx import PaintEvent

from wx import Pen
from wx import Point

from miniogl.MiniOglColorEnum import MiniOglColorEnum

from ogl.events.OglEventEngine import OglEventEngine

from tests.scaffold.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

DEFAULT_WIDTH = 16000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20

Points = NewType('Points', List[Point])

REFERENCE_POINT_RADIUS: int = 4


class UmlClassDiagramsFrame(UmlDiagramsFrame):

    cdfDebugId: int = 0x000FF   # UML Class Diagrams Frame Debug ID

    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    """
    def __init__(self, parent):
        """
        """

        self._cdfDebugId: int = UmlClassDiagramsFrame.cdfDebugId

        UmlClassDiagramsFrame.cdfDebugId += 1

        super().__init__(parent)
        self.clearDiagram()

        self._oglEventEngine: OglEventEngine = OglEventEngine(listeningWindow=self)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        self._showReferencePoints: bool   = False
        self._referencePoints:     Points = cast(Points, None)

    @property
    def eventEngine(self) -> OglEventEngine:
        return self._oglEventEngine

    @property
    def showReferencePoints(self) -> bool:
        return self._showReferencePoints

    @showReferencePoints.setter
    def showReferencePoints(self, value: bool):
        self._showReferencePoints = value

    @property
    def referencePoints(self) -> Points:
        return self._referencePoints

    @referencePoints.setter
    def referencePoints(self, points: Points):
        self._referencePoints = points

    def OnPaint(self, event: PaintEvent):
        super().OnPaint(event=event)

        if self._showReferencePoints is True:

            dc: PaintDC = PaintDC(self)
            w, h = self.GetSize()
            mem = self.CreateDC(False, w, h)
            mem.SetBackground(Brush(self.GetBackgroundColour()))
            mem.Clear()
            x, y = self.CalcUnscrolledPosition(0, 0)

            self._drawReferencePoints(dc=mem)

            self.Redraw(mem)
            dc.Blit(0, 0, w, h, mem, x, y)

    def _drawReferencePoints(self, dc: DC):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(BLACK_PEN)
        dc.SetBrush(Brush(MiniOglColorEnum.toWxColor(MiniOglColorEnum.ALICE_BLUE)))

        points: Points = self._referencePoints

        for pt in points:
            # point: Point = self._computeShapeCenter(x=pt.x, y=pt.y, width=REFERENCE_POINT_WIDTH, height=REFERENCE_POINT_HEIGHT)
            # dc.DrawEllipse(x=point.x, y=point.y, width=REFERENCE_POINT_WIDTH, height=REFERENCE_POINT_HEIGHT)
            point: Point = cast(Point, pt)
            x, y = point.Get()
            dc.DrawCircle(x=x, y=y, radius=REFERENCE_POINT_RADIUS)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)
