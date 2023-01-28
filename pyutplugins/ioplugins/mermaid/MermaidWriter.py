
from typing import List
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from os import linesep as eol

from datetime import datetime

from pathlib import Path

from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from ogl.OglLink import OglLink
from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglAggregation import OglAggregation
from ogl.OglInheritance import OglInheritance
from ogl.OglComposition import OglComposition

from pyutplugins.ExternalTypes import OglObjects


indent1: str = '    '
indent2: str = f'{indent1}    '
indent3: str = f'{indent2}    '
indent4: str = f'{indent3}    '
indent5: str = f'{indent4}    '

INHERITANCE_ARROW: str = '<|--'     # Points to parent class
AGGREGATION_LINK:  str = 'o--'      #
COMPOSITION_LINK:  str = '*--'      #


class MermaidWriter:
    VERSION: str = '0.5'

    def __init__(self, fqFileName: Path, writeCredits: bool = True):
        """

        Args:
            fqFileName:     Fully qualified file name to write to
            writeCredits:   We will always write credits.  Unit tests turn this off
            because of the time stamps
        """
        self.logger: Logger = getLogger(__name__)

        self._fqFileName: Path = fqFileName

        self._writeCredits(writeCredits=writeCredits)

    def translate(self, oglObjects: OglObjects):

        mermaidString: str = f'```mermaid{eol}'
        mermaidString = f'{mermaidString}classDiagram{eol}{indent1}direction RL{eol}'   # TODO: direction should be configurable

        linksStanza: str = self._generateLinksStanza(oglObjects=oglObjects)

        mermaidString = f'{mermaidString}{linksStanza}'

        for oglObject in oglObjects:
            match oglObject:
                case OglClass():
                    oglClass:  OglClass  = cast(OglClass, oglObject)
                    generatedString: str = self._generateClassStanza(oglClass)
                    mermaidString += f'{generatedString}'
                case OglLink():
                    pass
                case _:
                    self.logger.warning(f'Unknown Ogl element: {oglObject}')

        mermaidString += f'```{eol}'
        with self._fqFileName.open(mode='a') as fd:
            fd.write(f'{mermaidString}')

    def _generateClassStanza(self, oglObject: OglClass) -> str:
        """

        Args:
            oglObject:  A Pyut Class Definition

        Returns:  A Mermaid class definition
        """
        oglClass:  OglClass  = cast(OglClass, oglObject)
        pyutClass: PyutClass = oglClass.pyutObject

        methods:    List[PyutMethod] = pyutClass.methods
        methodsStr: str              = self._generateMethods(methods)

        if pyutClass.stereotype == PyutStereotype.NO_STEREOTYPE:
            stereotypeRefrain: str = ''
        else:
            stereotypeRefrain = f'{indent2}<<{pyutClass.stereotype.value}>>{eol}'

        generatedString: str = (
            f'{indent1}class {pyutClass.name} {{ {eol}'
            f'{stereotypeRefrain}'
            f'{methodsStr}'
            f'{indent1}}}{eol}'
        )
        return generatedString

    def _generateLinksStanza(self, oglObjects: OglObjects) -> str:
        """
        Make a pass through creating links
        Args:
            oglObjects:

        Returns:

        """
        linksStanza: str = f'{indent1}%% Links follow{eol}'

        for oglObject in oglObjects:
            linkRefrain: str = ''
            match oglObject:
                case OglInheritance():
                    oglLink:  OglLink  = cast(OglLink, oglObject)
                    pyutLink: PyutLink = oglLink.pyutObject

                    subClassName:  str = pyutLink.getSource().name
                    baseClassName: str = pyutLink.getDestination().name
                    self.logger.info(f'{subClassName=} {pyutLink.linkType=} {baseClassName=}')

                    linkRefrain = (
                        f'{indent1}{baseClassName}{INHERITANCE_ARROW}{subClassName}{eol}'
                    )
                case OglAggregation():
                    oglAggregation: OglAggregation = cast(OglAggregation, oglObject)
                    pyutLink:       PyutLink       = oglAggregation.pyutObject
                    aggregatorName: str = pyutLink.getSource().name
                    aggregatedName: str = pyutLink.getDestination().name

                    self.logger.info(f'{oglAggregation} {aggregatorName=} {aggregatedName=}')

                    aggregatorCardinality, aggregatedCardinality = self._getCardinalityStrings(pyutLink)
                    linkRefrain = (
                        f'{indent1}{aggregatorName} {aggregatorCardinality} {AGGREGATION_LINK} {aggregatedCardinality} {aggregatedName}{eol}'
                    )
                case OglComposition():
                    oglComposition: OglComposition = cast(OglComposition, oglObject)
                    pyutLink:       PyutLink       = oglComposition.pyutObject
                    composerName:   str            = pyutLink.getSource().name
                    composedName:   str            = pyutLink.getDestination().name
                    self.logger.info(f'{oglComposition} {composerName=} {composedName=}')

                    composerCardinality, composedCardinality = self._getCardinalityStrings(pyutLink)
                    linkRefrain = (
                        f'{indent1}{composerName} {composerCardinality} {COMPOSITION_LINK} {composedCardinality} {composedName}{eol}'
                    )

                case OglInterface2():
                    pass
                case _:
                    pass        # Ignore non links
            linksStanza += linkRefrain

        return linksStanza

    def _getCardinalityStrings(self, pyutLink) -> Tuple[str, str]:
        """

        Args:
            pyutLink:

        Returns: A tuple of source, destination cardinality strings

        """
        if pyutLink.sourceCardinality == '':
            sourceCardinality: str = ''
        else:
            sourceCardinality: str = f'"{pyutLink.sourceCardinality}"'
        if pyutLink.destinationCardinality == '':
            destinationCardinality: str = ''
        else:
            destinationCardinality = f'"{pyutLink.destinationCardinality}"'

        return sourceCardinality, destinationCardinality

    def _generateMethods(self, methods: List[PyutMethod]) -> str:

        retString: str = f''

        for method in methods:
            pyutMethod: PyutMethod = cast(PyutMethod, method)
            visibility: PyutVisibilityEnum = pyutMethod.visibility
            retType:    PyutType = pyutMethod.returnType

            parameterString: str = self._generateParameters(pyutMethod)
            methodString: str = (
                f'{indent2}{visibility.value}{retType.value} {pyutMethod.name}'
                f'('
                f'{parameterString}'
                f'){eol}'
            )
            retString += methodString
        return retString

    def _generateParameters(self, pyutMethod: PyutMethod) -> str:
        retString: str = ''

        for parameter in pyutMethod.parameters:
            pyutParameter: PyutParameter = cast(PyutParameter, parameter)
            parameterString: str = (
                f'{pyutParameter.name}, '
            )
            retString += parameterString
        return retString.strip(', ')

    def _writeCredits(self, writeCredits: bool):

        # ensure it is empty
        with self._fqFileName.open(mode='w') as fd:
            if writeCredits is True:

                fd.write(f'---{eol}')
                fd.write(f'Generated by Mermaid Writer Version: {MermaidWriter.VERSION}{eol}')

                now:      datetime = datetime.now()  # current date and time
                dateTime: str      = now.strftime('%d %b %Y, %H:%M:%S')

                fd.write(f'{dateTime}{eol}')
                fd.write(f'---{eol}')
            else:
                fd.write('')
