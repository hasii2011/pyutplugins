
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from os import path as osPath

from wx import TreeItemId

from tests.scaffoldv2.PyutDocument import PyutDocument
from tests.scaffoldv2.umlframes.UmlClassDiagramsFrame import UmlClassDiagramsFrame
from tests.scaffoldv2.umlframes.UmlSequenceDiagramsFrame import UmlSequenceDiagramsFrame

PyutDocuments = NewType('PyutDocuments', List[PyutDocument])

UmlFrameType = Union[UmlClassDiagramsFrame, UmlSequenceDiagramsFrame]


class PyutProject:
    """
    This class is a rewrite of the original PyutProject class.  That class injected
    a bunch of UI elements into the class in order to effectuate changes in the user
    interface;

    This component separates UI interaction from state changes that it needs to make in
    the user interface.  It does this by using wxPython's event mechanism
    """
    DEFAULT_PROJECT_NAME: str = 'New Project'

    def __init__(self, fileName: str = '', codePath: str = ''):
        """

        Args:
            fileName:    The fully qualified filename; Is used as the file name when persisting a project
            codePath:    If reverse engineered this is where the code is
        """

        self._fileName:    str  = fileName
        self._codePath:    str  = codePath
        self._modified:    bool = False

        self.logger: Logger = getLogger(__name__)

        self._documents: PyutDocuments = PyutDocuments([])

        self._projectTreeRoot: TreeItemId = cast(TreeItemId, None)

    @property
    def fileName(self) -> str:
        return self._fileName

    @fileName.setter
    def fileName(self, newValue: str):
        self._fileName = newValue

    @property
    def projectName(self) -> str:
        """
        Truncates to just the file name and less the suffix.

        Returns:   Nice short hane
        """
        return self._justTheFileName(self._fileName)

    # @projectName.setter
    # def projectName(self, newValue: str):
    #     """
    #     Set the project's filename
    #
    #     Args:
    #         newValue:
    #     """
    #     self._projectName = newValue
    #     self.updateTreeText()

    @property
    def codePath(self) -> str:
        """

        Returns: The root path where the corresponding code resides.
        """
        return self._codePath

    @codePath.setter
    def codePath(self, codePath: str):
        """
        Set the root path where the corresponding code resides.

        Args:
            codePath:
        """
        self._codePath = codePath

    @property
    def documents(self) -> PyutDocuments:
        """
        Return the documents associated with this project

        Returns:  A list of documents
        """
        return self._documents

    @property
    def modified(self) -> bool:
        """
        Returns:  'True' if it has been else 'False'
        """
        return self._modified

    @modified.setter
    def modified(self, value: bool = True):
        """
        Set that the project has been modified

        Args:
            value:  'True' if it has been else 'False'
        """
        self._modified = value

    @property
    def projectTreeRoot(self) -> TreeItemId:
        """
        A piece of UI information needed to communicate with the UI component

        Returns: The opaque item where this project's documents are display on the UI Tree
        """
        return self._projectTreeRoot

    @projectTreeRoot.setter
    def projectTreeRoot(self, newValue: TreeItemId):
        self._projectTreeRoot = newValue

    @property
    def frames(self) -> List[UmlFrameType]:
        """
        Get all the project's frames

        Returns:
            List of frames
        """
        frameList = [document.diagramFrame for document in self._documents]
        return frameList

    def updateTreeText(self):
        pass

    def _justTheFileName(self, filename):
        """
        Return just the file name portion of the fully qualified path

        Args:
            filename:  file name to display

        Returns:
            A better file name
        """
        regularFileName: str = osPath.split(filename)[1]

        return regularFileName
