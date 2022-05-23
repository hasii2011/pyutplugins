
from logging import Logger
from logging import getLogger
from typing import TextIO
from typing import cast
from xml.dom.minidom import Element

from pkg_resources import resource_filename

from xml.dom.minidom import Document
from xml.dom.minidom import parseString

from tests.MiniDomToOglV10 import MiniDomToOgl
from tests.MiniDomToOglV10 import OglClasses
from tests.MiniDomToOglV10 import OglLinks
from tests.MiniDomToOglV10 import OglObjects
from tests.OglToMiniDomConstants import OglToMiniDomConstants


class TestDiagramLoader:

    RESOURCES_PACKAGE_NAME: str = 'tests.resources.testdata'
    OGL_FILE_NAME:          str = 'Ogl.xml'
    PYUT_FILE_NAME:         str = 'Pyut.xml'

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def retrieveOglObjects(self) -> OglObjects:

        oglXml:      str = self._loadDiagram(TestDiagramLoader.OGL_FILE_NAME)
        oglDocument: Document = parseString(oglXml)
        self.logger.info(f'{oglDocument}')

        root: Element = oglDocument.getElementsByTagName(OglToMiniDomConstants.TOP_LEVEL_ELEMENT)[0]
        assert root is not None, 'Something wrong with that XML file'
        version: int = int(root.getAttribute(OglToMiniDomConstants.ATTR_VERSION))
        assert version == 10, 'Incorrect version'

        oglObjects: OglObjects = cast(OglObjects, None)
        for element in oglDocument.getElementsByTagName(OglToMiniDomConstants.ELEMENT_DOCUMENT):

            documentNode: Element = cast(Element, element)
            docTypeStr:   str     = documentNode.getAttribute(OglToMiniDomConstants.ATTR_TYPE)

            self.logger.info(f'{docTypeStr=}')
            assert docTypeStr == 'CLASS_DIAGRAM', 'We only do class diagrams'

            oglObjects = self._extractOglObjects(documentNode=documentNode)

        assert oglObjects is not None, 'The test XML is FUBAR'
        return oglObjects

    def retrievePyutObjects(self):

        pyutXml:      str      = self._loadDiagram(TestDiagramLoader.PYUT_FILE_NAME)
        pyutDocument: Document = parseString(pyutXml)
        self.logger.debug(f'{pyutDocument}')

    def _loadDiagram(self, baseFileName: str) -> str:

        fqFileName = resource_filename(TestDiagramLoader.RESOURCES_PACKAGE_NAME, baseFileName)

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

    def _extractOglObjects(self, documentNode: Element) -> OglObjects:

        toOgl: MiniDomToOgl = MiniDomToOgl()

        oglClasses:       OglClasses = toOgl.getOglClasses(documentNode.getElementsByTagName(OglToMiniDomConstants.ELEMENT_GRAPHIC_CLASS))
        mergedOglObjects: OglObjects = cast(OglObjects, oglClasses.copy())
        oglLinks:         OglLinks   = toOgl.getOglLinks(documentNode.getElementsByTagName(OglToMiniDomConstants.ELEMENT_GRAPHIC_LINK), mergedOglObjects)

        return mergedOglObjects
