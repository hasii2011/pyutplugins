
from typing import cast
from typing import TextIO

from logging import Logger
from logging import getLogger

from math import floor
from math import ceil

from os import sep as osSep

from ogl.OglClass import OglClass

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutStereotype import PyutStereotype

from core.types.PluginDataTypes import PluginName

from plugins.common.Types import OglClasses

from core.ToolPluginInterface import ToolPluginInterface

from core.IMediator import IMediator

from core.types.ExportDirectoryResponse import ExportDirectoryResponse


class ToolAscii(ToolPluginInterface):
    """
    UML objects to an ASCII representation
    """

    def __init__(self, mediator: IMediator):

        super().__init__(mediator)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('ASCII Class Export')
        self._author    = 'Philippe Waelti <pwaelti@eivd.ch>'
        self._version   = '1.0'

        self._menuTitle = 'ASCII Class Export'

        self._exportDirectory: str = ''

    def setOptions(self) -> bool:

        response: ExportDirectoryResponse = self.askForExportDirectoryName()
        if response.cancelled is True:
            return False
        else:
            self._exportDirectory = response.directoryName
            self.logger.debug(f'selectedDir: {self._exportDirectory}')
            return True

    def doAction(self):
        """

        """
        selectedObjects: OglClasses = self._communicator.selectedOglObjects
        if len(selectedObjects) < 1:
            self.displayNoSelectedOglObjects()
            return
        self._write(selectedObjects)

    def _write(self, oglObjects: OglClasses):
        """
        Write the data to a file
        Args:
            oglObjects:   The objects to export
        """

        for oglObject in oglObjects:

            if not isinstance(oglObject, OglClass):
                continue

            pyutClass: PyutClass = cast(PyutClass, oglObject.pyutObject)
            filename:  str       = pyutClass.name

            fqFileName: str = f'{self._exportDirectory}{osSep}{filename}.acl'

            file: TextIO = open(f'{fqFileName}', "w")

            base = [pyutClass.name]
            pyutStereotype: PyutStereotype = pyutClass.getStereotype()
            if pyutStereotype is not None and pyutStereotype.name != '':
                base.append(str(pyutClass.getStereotype()))

            fields = [str(x) for x in pyutClass.fields]
            methods = [str(x) for x in pyutClass.methods]

            lineLength = max([len(x) for x in base + fields + methods]) + 4

            file.write(lineLength * "-" + "\n")

            for line in base:
                spaces = lineLength - 4 - len(line)
                file.write("| " + int(floor(spaces / 2.0)) * " " + line + int(ceil(spaces / 2.0)) * " " + " |\n")

            file.write("|" + (lineLength - 2) * "-" + "|\n")

            for line in fields:
                file.write("| " + line + (lineLength - len(line) - 4) * " " + " |\n")

            file.write("|" + (lineLength - 2) * "-" + "|\n")

            for line in methods:
                file.write("| " + line + (lineLength - len(line) - 4) * " " + " |\n")

            file.write(lineLength * "-" + "\n\n")

            file.write(pyutClass.description)

            file.close()
