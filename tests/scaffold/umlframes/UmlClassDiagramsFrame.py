
from typing import List
from typing import NewType
from typing import cast

from dataclasses import dataclass

from wx import BLACK_PEN
from wx import Brush
from wx import Colour
from wx import DC
from wx import PENSTYLE_LONG_DASH

from wx import PaintDC
from wx import PaintEvent

from wx import Pen
from wx import PenInfo
from wx import Point

# I know it is there
# noinspection PyUnresolvedReferences
from wx.core import PenStyle

from miniogl.MiniOglColorEnum import MiniOglColorEnum

from ogl.events.OglEventEngine import OglEventEngine

from tests.scaffold.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

DEFAULT_WIDTH: int   = 16000
A4_FACTOR:     float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20

Points      = NewType('Points',      List[Point])
IntegerList = NewType('IntegerList', List[int])


@dataclass
class Rectangle:
    left:   int = 0
    top:    int = 0
    width:  int = 0
    height: int = 0


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

        self._showReferencePoints: bool        = False
        self._showRulers:          bool        = False
        self._referencePoints:     Points      = cast(Points, None)
        self._horizontalRulers:    IntegerList = cast(IntegerList, None)
        self._verticalRulers:      IntegerList = cast(IntegerList, None)
        self._diagramBounds:       Rectangle   = cast(Rectangle, None)

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
    def showRulers(self) -> bool:
        return self._showRulers

    @showRulers.setter
    def showRulers(self, value: bool):
        self._showRulers = value

    @property
    def referencePoints(self) -> Points:
        return self._referencePoints

    @referencePoints.setter
    def referencePoints(self, points: Points):
        self._referencePoints = points

    @property
    def horizontalRulers(self) -> IntegerList:
        return self._horizontalRulers

    @horizontalRulers.setter
    def horizontalRulers(self, newRulers: IntegerList):
        self._horizontalRulers = newRulers

    @property
    def verticalRulers(self):
        return self._verticalRulers

    @verticalRulers.setter
    def verticalRulers(self, newRulers: IntegerList):
        self._verticalRulers = newRulers

    @property
    def diagramBounds(self) -> Rectangle:
        return self._diagramBounds

    @diagramBounds.setter
    def diagramBounds(self, newBounds: Rectangle):
        self._diagramBounds = newBounds

    def OnPaint(self, event: PaintEvent):

        super().OnPaint(event=event)

        if self._showDiagnostics() is True:
            w, h = self.GetSize()

            mem: DC = self.CreateDC(False, w, h)
            mem.SetBackground(Brush(self.GetBackgroundColour()))
            mem.Clear()
            x, y = self.CalcUnscrolledPosition(0, 0)

            if self._showReferencePoints is True:
                self._drawReferencePoints(dc=mem)
            if self._showRulers is True:
                self._drawRulers(dc=mem)

            paintDC: PaintDC = PaintDC(self)
            self.Redraw(mem)
            paintDC.Blit(0, 0, w, h, mem, x, y)

    def _drawReferencePoints(self, dc: DC):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()

        dc.SetPen(BLACK_PEN)
        dc.SetBrush(Brush(MiniOglColorEnum.toWxColor(MiniOglColorEnum.ALICE_BLUE)))

        points: Points = self._referencePoints

        for pt in points:
            point: Point = cast(Point, pt)
            x, y = point.Get()
            dc.DrawCircle(x=x, y=y, radius=REFERENCE_POINT_RADIUS)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def _drawRulers(self, dc: DC):

        savePen:   Pen   = dc.GetPen()
        saveBrush: Brush = dc.GetBrush()
        #
        dc.SetPen(self._getRulerPen())

        horizontalRulers: IntegerList  = self._horizontalRulers
        verticalRulers:   IntegerList  = self._verticalRulers
        globalBounds:     Rectangle    = self._diagramBounds

        for y in horizontalRulers:
            dc.DrawLine(x1=0, y1=y, x2=globalBounds.width, y2=y)

        for x in verticalRulers:
            dc.DrawLine(x1=x, y1=0, x2=x, y2=globalBounds.height)

        dc.SetPen(savePen)
        dc.SetBrush(saveBrush)

    def _showDiagnostics(self) -> bool:

        show: bool = False

        if self._showReferencePoints is True or self._showRulers is True:
            show = True

        return show

    def _getRulerPen(self) -> Pen:
        gridLineColor: Colour = MiniOglColorEnum.toWxColor(MiniOglColorEnum.DARK_SLATE_BLUE)

        gridLineStyle: PenStyle = PENSTYLE_LONG_DASH
        pen: Pen = Pen(PenInfo(gridLineColor).Style(gridLineStyle).Width(1))

        return pen
