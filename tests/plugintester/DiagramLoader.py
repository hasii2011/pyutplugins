
from logging import Logger
from logging import getLogger
from typing import TextIO
from typing import cast
from xml.dom.minidom import Element

from pkg_resources import resource_filename

from xml.dom.minidom import Document
from xml.dom.minidom import parseString

from tests.plugintester.MiniDomToOgl import MiniDomToOgl
from tests.plugintester.MiniDomToOgl import OglClasses
from tests.plugintester.MiniDomToOgl import OglLinks
from tests.plugintester.MiniDomToOgl import OglObjects
from tests.plugintester.OglToMiniDomConstants import OglToMiniDomConstants

from tests.plugintester.OglModel import OglModel


class DiagramLoader:

    RESOURCES_PACKAGE_NAME: str = 'tests.resources.testdata'
    OGL_FILE_NAME:          str = 'Ogl.xml'
    PYUT_FILE_NAME:         str = 'Pyut.xml'

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def retrieveOglModel(self) -> OglModel:
        oglModel: OglModel = self._retrieveModel(baseFileName=DiagramLoader.OGL_FILE_NAME)
        return oglModel

    def retrievePyutModel(self):
        oglModel: OglModel = self._retrieveModel(baseFileName=DiagramLoader.PYUT_FILE_NAME)
        return oglModel

    def _retrieveModel(self, baseFileName: str) -> OglModel:
        """

        Args:
            baseFileName:  The Pyut file name in XML format
        """
        oglXml:      str = self._readTheDiagramFile(baseFileName)

        oglDocument: Document = parseString(oglXml)
        self.logger.info(f'{oglDocument}')

        root: Element = oglDocument.getElementsByTagName(OglToMiniDomConstants.TOP_LEVEL_ELEMENT)[0]
        assert root is not None, 'Something wrong with that XML file'
        version: int = int(root.getAttribute(OglToMiniDomConstants.ATTR_VERSION))
        assert version == 10, 'Incorrect version'

        oglModel: OglModel = cast(OglModel, None)
        for element in oglDocument.getElementsByTagName(OglToMiniDomConstants.ELEMENT_DOCUMENT):

            documentNode: Element = cast(Element, element)
            docTypeStr:   str     = documentNode.getAttribute(OglToMiniDomConstants.ATTR_TYPE)

            self.logger.info(f'{docTypeStr=}')
            assert docTypeStr == 'CLASS_DIAGRAM', 'We only do class diagrams'

            oglModel = self._extractOglModel(documentNode=documentNode)

        assert oglModel is not None, 'The test XML is FUBAR'

        return oglModel

    def _readTheDiagramFile(self, baseFileName: str) -> str:
        """
        Does the actual I/O
        May throw exception

        Args:
            baseFileName:  The Pyut file name in XML forma
        """

        fqFileName = resource_filename(DiagramLoader.RESOURCES_PACKAGE_NAME, baseFileName)

        try:
            f: TextIO = open(fqFileName, 'r')
        except IOError as ioe:
            self.logger.error(f'{ioe}')
            raise ioe
        else:
            with f:
                xmlStr: str = f.read()
                f.close()
                return xmlStr

    def _extractOglModel(self, documentNode: Element) -> OglModel:

        toOgl: MiniDomToOgl = MiniDomToOgl()

        oglClasses:     OglClasses = toOgl.getOglClasses(documentNode.getElementsByTagName(OglToMiniDomConstants.ELEMENT_GRAPHIC_CLASS))
        oglObjectsCopy: OglObjects = cast(OglObjects, oglClasses.copy())
        oglLinks:       OglLinks   = toOgl.getOglLinks(documentNode.getElementsByTagName(OglToMiniDomConstants.ELEMENT_GRAPHIC_LINK), oglObjectsCopy)

        oglModel: OglModel = OglModel(oglClasses=oglClasses, oglLinks=oglLinks)

        return oglModel