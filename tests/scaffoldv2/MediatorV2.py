from abc import ABC
from logging import Logger
from logging import getLogger

from core.IMediator import IMediator
from core.types.Types import PluginDocument
from core.types.Types import PluginProject


class MediatorV2(IMediator, ABC):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

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
