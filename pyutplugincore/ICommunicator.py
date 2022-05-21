
from typing import cast

from wx import Frame

from pyutplugincore.coretypes.Helper import OglClasses


class ICommunicator:
    """
    This the interface specification that allows the plugins to manipulate the Pyut UML Frame
    The Pyut application must implement this
    """

    def refreshFrame(self):
        pass

    def deselectAllOglObjects(self):
        pass

    @property
    def currentDirectory(self) -> str:
        return ''

    @currentDirectory.setter
    def currentDirectory(self, newValue: str):
        pass

    @property
    def umlFrame(self) -> Frame:
        return cast(Frame, None)

    @property
    def selectedOglObjects(self) -> OglClasses:
        return cast(OglClasses, None)
