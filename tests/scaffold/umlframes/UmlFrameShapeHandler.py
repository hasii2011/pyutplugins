
from typing import Union

from logging import Logger
from logging import getLogger

from wx import Brush
from wx import Pen
from wx import Window

from pyutmodelv2.PyutActor import PyutActor
from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutNote import PyutNote
from pyutmodelv2.PyutText import PyutText
from pyutmodelv2.PyutUseCase import PyutUseCase

from miniogl.DiagramFrame import DiagramFrame
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglActor import OglActor
from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglNote import OglNote
from ogl.OglObject import OglObject
from ogl.OglText import OglText
from ogl.OglUseCase import OglUseCase
from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglLink import OglLink
from ogl.OglTextFontFamily import OglTextFontFamily

from ogl.sd.OglSDInstance import OglSDInstance


class UmlFrameShapeHandler(DiagramFrame):

    def __init__(self, parent: Window):
        """

        Args:
            parent:  The window where we put the UML Diagram Frames
        """

        super().__init__(parent)

        self.logger:       Logger = getLogger(__name__)

    def createNewClass(self, x, y):
        """
        Add a new class at (x, y).

        @return PyutClass : the newly created PyutClass
        """
        # pyutClass: PyutClass = PyutClass(PyutPreferences().className)
        pyutClass: PyutClass = PyutClass('ClassName')
        oglClass:  OglClass  = OglClass(pyutClass)

        self.addShape(oglClass, x, y)
        self.Refresh()
        return pyutClass

    def createNewNote(self, x: int, y: int):
        """
        Add a new note at (x, y).

        Args:
            x:
            y:

        Returns:    the newly created PyutNote
        """
        # pyutNote: PyutNote = PyutNote(noteText=self._preferences.noteText)
        pyutNote: PyutNote = PyutNote(content='Note Text')
        oglNote:  OglNote  = OglNote(pyutNote)

        self.addShape(oglNote, x, y)
        self.Refresh()
        return pyutNote

    def createNewText(self, x: int, y: int):
        """
        Add some new text at (x, y)
        TODO:  the text attributes belong on the OGL object
        Args:
            x:
            y:

        Returns:  The newly created PyutText data model class
        """
        # preferences: PyutPreferences = self._preferences

        pyutText: PyutText = PyutText(content='I am a note')

        oglText: OglText       = OglText(pyutText)
        # oglText.textFontFamily = preferences.textFontFamily
        # oglText.textSize       = preferences.textFontSize
        # oglText.isBold         = preferences.textBold
        # oglText.isItalicized   = preferences.textItalicize
        oglText.textFontFamily = OglTextFontFamily.SWISS
        oglText.textSize       = 14
        oglText.isBold         = False
        oglText.isItalicized   = False

        self.addShape(oglText, x, y)
        self.Refresh()

        return pyutText

    def createNewActor(self, x, y):
        """
        Add a new actor at (x, y).

        @return PyutActor : the newly created PyutActor
        """
        # pyutActor: PyutActor = PyutActor(PyutPreferences().actorName)
        pyutActor: PyutActor = PyutActor('Actor')
        oglActor:  OglActor  = OglActor(pyutActor)

        self.addShape(oglActor, x, y)
        self.Refresh()
        return pyutActor

    def createNewUseCase(self, x, y):
        """
        Add a new use case at (x, y).

        @return PyutUseCase : the newly created PyutUseCase
        """
        # pyutUseCase: PyutUseCase = PyutUseCase(PyutPreferences().useCaseName)
        pyutUseCase: PyutUseCase = PyutUseCase('Use Case')
        oglUseCase:  OglUseCase  = OglUseCase(pyutUseCase)

        self.addShape(oglUseCase, x, y)
        self.Refresh()
        return pyutUseCase

    def addShape(self, shape: Union[OglObject, OglLink, OglInterface2, SelectAnchorPoint, OglAssociationLabel, OglSDInstance],
                 x: int, y: int,
                 pen: Pen = None,
                 brush: Brush = None,
                 withModelUpdate: bool = True):
        """
        Add a shape to the UmlFrame.

        Args:
            shape: the shape to add
            x: coord of the center of the shape
            y: coord of the center of the shape
            pen: pen to use
            brush:  brush to use
            withModelUpdate: if true the model of the shape will update from the shape (view) when added to the diagram.
        """
        shape.draggable = True
        shape.SetPosition(x, y)
        if pen is not None:
            shape.pen = pen
        if brush is not None:
            shape.brush = brush
        self._diagram.AddShape(shape, withModelUpdate)
