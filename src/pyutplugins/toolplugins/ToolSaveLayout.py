
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from json import dumps as jsonDumps

from ogl.OglObject import OglObject

from pyutmodelv2.PyutObject import PyutObject

from pyutplugins.ExternalTypes import OglObjects

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.plugintypes.OutputFormat import OutputFormat
from pyutplugins.plugintypes.PluginDataTypes import FormatName
from pyutplugins.plugintypes.PluginDataTypes import PluginDescription
from pyutplugins.plugintypes.PluginDataTypes import PluginExtension

from pyutplugins.plugintypes.PluginDataTypes import PluginName

from pyutplugins.plugininterfaces.ToolPluginInterface import ToolPluginInterface
from pyutplugins.plugintypes.SingleFileRequestResponse import SingleFileRequestResponse


DEFAULT_FILE_NAME: str = 'DiagramLayout'     # TODO make a plugin option

FORMAT_NAME:        FormatName        = FormatName('Layout File')
PLUGIN_EXTENSION:   PluginExtension   = PluginExtension('json')
PLUGIN_DESCRIPTION: PluginDescription = PluginDescription('Save Diagram Layout')

NO_INTEGER = cast(int, None)


@dataclass
class Size:
    width:  int = NO_INTEGER
    height: int = NO_INTEGER


@dataclass
class Position:
    x: int = NO_INTEGER
    y: int = NO_INTEGER


def positionFactory() -> Position:
    return Position()


def sizeFactory() -> Size:
    return Size()


@dataclass
class Layout:
    name:     str      = cast(str, None)
    position: Position = field(default_factory=positionFactory)
    size:     Size     = field(default_factory=sizeFactory)


Layouts = NewType('Layouts', List[Layout])


def layoutsFactory() -> Layouts:
    return Layouts([])


@dataclass
class LayoutInformation:
    layouts: Layouts = field(default_factory=layoutsFactory)


class ToolSaveLayout(ToolPluginInterface):

    # noinspection SpellCheckingInspection
    def __init__(self, pluginAdapter: IPluginAdapter):

        super().__init__(pluginAdapter)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Save Layout')
        self._author    = 'Humberto A. Sanchez II'
        self._version   = '2.0'

        self._menuTitle = 'Save Layout'

        self._outputFormat = OutputFormat(formatName=FORMAT_NAME, extension=PLUGIN_EXTENSION, description=PLUGIN_DESCRIPTION)

        self._outputFileName: str = ''

    def setOptions(self) -> bool:
        """

        Returns:   True when user selects an output filename
        """

        response: SingleFileRequestResponse = self.askForFileToExport(defaultFileName=DEFAULT_FILE_NAME)

        if response.cancelled is True:
            return False
        else:
            self._outputFileName = response.fileName
            return True

    def doAction(self):
        self._pluginAdapter.selectAllOglObjects()
        self._pluginAdapter.getSelectedOglObjects(callback=self._doAction)

    def _doAction(self, oglObjects: OglObjects):

        layouts: Layouts = layoutsFactory()

        oglObject: OglObject = cast(OglObject, None)
        for el in oglObjects:
            if isinstance(el, OglObject):
                try:
                    oglObject = cast(OglObject, el)
                    pyutObject: PyutObject = oglObject.pyutObject

                    if pyutObject.name is None:
                        name: str = f'id: {pyutObject.id}'
                    else:
                        name = pyutObject.name
                    x, y = oglObject.GetPosition()
                    w, h = oglObject.GetSize()
                    position: Position = Position(x=x, y=y)
                    size:     Size     = Size(width=w, height=h)
                    layout: Layout = Layout(name=name, position=position, size=size)

                    layouts.append(layout)

                except (AttributeError, TypeError) as e:
                    self.logger.error(f'{e} - {oglObject=}')

        layoutInformation: LayoutInformation = LayoutInformation(layouts=layouts)
        with open(self._outputFileName, 'w') as fd:
            jsonStr: str = jsonDumps(asdict(layoutInformation), indent=4)
            fd.write(jsonStr)
