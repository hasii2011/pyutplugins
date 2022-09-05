
from os import getcwd

from miniogl.DiagramFrame import DiagramFrame

from core.IMediator import IMediator
from core.IMediator import ScreenMetrics
from core.types.Types import PluginDocument
from core.types.Types import PluginProject


class ScaffoldMediator(IMediator):
    """
    Shortcut implement the version and screen metrics properties
    """

    def __init__(self, umlFrame: DiagramFrame, currentDirectory: str = ''):

        if currentDirectory is None or currentDirectory == '':
            self._currentDirectory: str = getcwd()
        else:
            self._currentDirectory = currentDirectory

        super().__init__(currentDirectory=currentDirectory, umlFrame=umlFrame)

        self._pyutVersion = 'Scaffold 1.0'

    @property
    def pyutVersion(self) -> str:
        return self._pyutVersion

    @pyutVersion.setter
    def pyutVersion(self, newVersion: str):
        self._pyutVersion = newVersion

    @property
    def screenMetrics(self) -> ScreenMetrics:
        return ScreenMetrics(dpiX=72, dpiY=72, screenWidth=250, screenHeight=1440)

    def addProject(self, pluginProject: PluginProject):
        """
        In the plugin scaffold test program we support only single document projects

        Args:
            pluginProject:
        """
        singlePluginDocument: PluginDocument = list(pluginProject.pluginDocuments.values())[0]

        for oglClass in singlePluginDocument.oglClasses:
            self.addShape(oglClass)

        for oglLink in singlePluginDocument.oglLinks:
            self.addShape(oglLink)

        for oglText in singlePluginDocument.oglTexts:
            self.addShape(oglText)

        for oglNote in singlePluginDocument.oglNotes:
            self.addShape(oglNote)

        self.refreshFrame()
