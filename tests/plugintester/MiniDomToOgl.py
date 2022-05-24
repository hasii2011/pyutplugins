
from typing import cast
from typing import Dict
from typing import List
from typing import Union
from typing import NewType

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Element
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Text

from pyutmodel.ModelTypes import ClassName
from pyutmodel.ModelTypes import Implementors

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutMethod import SourceCode
from pyutmodel.PyutNote import PyutNote
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutModifier import PyutModifier
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum
from pyutmodel.PyutLinkType import PyutLinkType

from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.AttachmentLocation import AttachmentLocation

from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglClass import OglClass

from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglObject import OglObject
from ogl.OglPosition import OglPosition
from ogl.OglText import OglText
from ogl.OglAssociation import OglAssociation
from ogl.OglLinkFactory import getOglLinkFactory

from ogl.sd.OglSDInstance import OglSDInstance

from ogl.OglTextFontFamily import OglTextFontFamily

from tests.plugintester.MiniDomToOglUtils import PyutUtils
from tests.plugintester.OglToMiniDomConstants import OglToMiniDomConstants

OglObjects     = NewType('OglObjects',     Dict[int, OglObject])
OglClasses     = NewType('OglClasses',     Dict[int, OglClass])
OglNotes       = NewType('OglNotes',       Dict[int, OglNote])
PyutMethods    = NewType('PyutMethods',    List[PyutMethod])
PyutFields     = NewType('PyutFields',     List[PyutField])
ControlPoints  = NewType('ControlPoints',  List[ControlPoint])
Links          = NewType('Links',          Union[OglLink, OglSDInstance])   # type: ignore
OglLinks       = NewType('OglLinks',       List[Links])
OglInterfaces  = NewType('OglInterfaces',  List[OglInterface2])
OglTextShapes  = NewType('OglTextShapes',  List[OglText])


class MiniDomToOgl:
    """
    This is a cut down version of the original V10 version from Pyut;
    TODO:  Come up with a common version that can be used by both
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def getOglClasses(self, xmlOglClasses: NodeList) -> OglClasses:
        """
        Loads to OGL objects
        Parse the XML elements given and build data model for the Pyut classes.

        Args:
            xmlOglClasses:   XML 'GraphicClass' elements

        Returns:
                The built dictionary uses an ID for the key and an OglClass for the value
        """
        oglObjects: OglClasses = cast(OglClasses, {})

        for element in xmlOglClasses:

            xmlOglClass: Element   = cast(Element, element)
            pyutClass:   PyutClass = PyutClass()

            # Some old files used float sizes and positions
            height: int = PyutUtils.strFloatToInt(xmlOglClass.getAttribute(OglToMiniDomConstants.ATTR_HEIGHT))
            width:  int = PyutUtils.strFloatToInt(xmlOglClass.getAttribute(OglToMiniDomConstants.ATTR_WIDTH))

            oglClass: OglClass = OglClass(pyutClass, width, height)

            xmlClass: Element = xmlOglClass.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_CLASS)[0]

            pyutClass.id = int(xmlClass.getAttribute(OglToMiniDomConstants.ATTR_ID))
            pyutClass.name = xmlClass.getAttribute(OglToMiniDomConstants.ATTR_NAME)
            pyutClass.description = xmlClass.getAttribute(OglToMiniDomConstants.ATTR_DESCRIPTION)
            if xmlClass.hasAttribute(OglToMiniDomConstants.ATTR_STEREOTYPE):
                pyutClass.setStereotype(PyutStereotype(xmlClass.getAttribute(OglToMiniDomConstants.ATTR_STEREOTYPE)))

            # adding display properties (cd)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(OglToMiniDomConstants.ATTR_SHOW_STEREOTYPE))
            pyutClass.setShowStereotype(value)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(OglToMiniDomConstants.ATTR_SHOW_METHODS))
            pyutClass.showMethods = value
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(OglToMiniDomConstants.ATTR_SHOW_FIELDS))
            pyutClass.showFields = value

            displayParametersStr: str = xmlClass.getAttribute(OglToMiniDomConstants.ATTR_DISPLAY_PARAMETERS)

            self.logger.info(f'{pyutClass.name=} -- {displayParametersStr=}')
            if displayParametersStr is None or displayParametersStr == '':
                pyutClass.displayParameters = PyutDisplayParameters.UNSPECIFIED
            else:
                displayParameters: PyutDisplayParameters = PyutDisplayParameters(displayParametersStr)
                pyutClass.displayParameters = displayParameters

            pyutClass.fileName = xmlClass.getAttribute(OglToMiniDomConstants.ATTR_FILENAME)

            pyutClass.methods    = self._getMethods(xmlClass)
            pyutClass.fields     = self._getFields(xmlClass)

            # Adding properties necessary to place shape on a diagram frame
            x = PyutUtils.strFloatToInt(xmlOglClass.getAttribute(OglToMiniDomConstants.ATTR_X))
            y = PyutUtils.strFloatToInt(xmlOglClass.getAttribute(OglToMiniDomConstants.ATTR_Y))

            oglClass.SetPosition(x, y)

            oglObjects[pyutClass.id] = oglClass

        return oglObjects

    def getOglInterfaces(self, xmlOglInterfaces: NodeList, oglClasses: OglClasses) -> OglInterfaces:

        oglInterfaces: OglInterfaces = cast(OglInterfaces, [])

        for xmlOglInterface in xmlOglInterfaces:

            xmlInterface:  Element = xmlOglInterface.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_INTERFACE)[0]

            pyutInterface: PyutInterface = PyutInterface()
            pyutInterface.name         = xmlInterface.getAttribute(OglToMiniDomConstants.ATTR_NAME)
            pyutInterface.description  = xmlInterface.getAttribute(OglToMiniDomConstants.ATTR_DESCRIPTION)
            pyutInterface.methods      = self._getMethods(xmlInterface)
            pyutInterface.implementors = self._getImplementors(xmlInterface)

            oglClass: OglClass = self._findImplementor(pyutInterface.implementors[0], oglClasses)

            anchorPoint: SelectAnchorPoint  = self._getAttachmentPoint(xmlOglInterface, oglClass)
            anchorPoint.setYouAreTheSelectedAnchor()
            oglClass.AddAnchorPoint(anchorPoint)

            oglInterface: OglInterface2 = OglInterface2(pyutInterface=pyutInterface, destinationAnchor=anchorPoint)

            oglInterfaces.append(oglInterface)

        return oglInterfaces

    def getOglLinks(self, xmlOglLinks: NodeList, oglClasses: OglObjects) -> OglLinks:
        """
        Extract the link for the OglClasses

        Args:
            xmlOglLinks:  A DOM node list of links
            oglClasses:  The OglClasses

        Returns:
            The OglLinks list
        """
        oglLinks: OglLinks = cast(OglLinks, [])

        for element in xmlOglLinks:
            # src and dst anchor position
            xmlLink: Element = cast(Element, element)

            sx = PyutUtils.strFloatToInt(xmlLink.getAttribute(OglToMiniDomConstants.ATTR_LINK_SOURCE_ANCHOR_X))
            sy = PyutUtils.strFloatToInt(xmlLink.getAttribute(OglToMiniDomConstants.ATTR_LINK_SOURCE_ANCHOR_Y))
            dx = PyutUtils.strFloatToInt(xmlLink.getAttribute(OglToMiniDomConstants.ATTR_LINK_DESTINATION_ANCHOR_X))
            dy = PyutUtils.strFloatToInt(xmlLink.getAttribute(OglToMiniDomConstants.ATTR_LINK_DESTINATION_ANCHOR_Y))

            spline: bool = PyutUtils.secureBoolean(xmlLink.getAttribute(OglToMiniDomConstants.ATTR_SPLINE))

            # get the associated PyutLink
            srcId, dstId, assocPyutLink = self._getPyutLink(xmlLink)

            try:
                src: OglClass = cast(OglClass, oglClasses[srcId])
                dst: OglClass = cast(OglClass, oglClasses[dstId])
            except KeyError as ke:
                self.logger.error(f'Developer Error -- srcId: {srcId} - dstId: {dstId}  error: {ke}')
                continue

            linkType:         PyutLinkType  = assocPyutLink.linkType
            sourceClass:      PyutClass = cast(PyutClass, src.pyutObject)
            destinationClass: PyutClass = cast(PyutClass, dst.pyutObject)
            pyutLink: PyutLink = PyutLink(name=assocPyutLink.name,
                                          linkType=linkType,
                                          cardSrc=assocPyutLink.sourceCardinality,
                                          cardDest=assocPyutLink.destinationCardinality,
                                          source=sourceClass, destination=destinationClass)

            oglLinkFactory = getOglLinkFactory()
            oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)
            src.addLink(oglLink)
            dst.addLink(oglLink)

            oglLinks.append(oglLink)

            oglLink.SetSpline(spline)

            # put the anchors at the right position
            srcAnchor = oglLink.GetSource()
            dstAnchor = oglLink.GetDestination()
            srcAnchor.SetPosition(sx, sy)
            dstAnchor.SetPosition(dx, dy)

            # add the control points to the line
            line   = srcAnchor.GetLines()[0]  # only 1 line per anchor in pyut
            parent = line.GetSource().GetParent()
            selfLink = parent is line.GetDestination().GetParent()

            controlPoints: ControlPoints = self._generateControlPoints(xmlLink)
            for controlPoint in controlPoints:
                line.AddControl(controlPoint)
                if selfLink:
                    x, y = controlPoint.GetPosition()
                    controlPoint.SetParent(parent)
                    controlPoint.SetPosition(x, y)

            if isinstance(oglLink, OglAssociation):
                self.__furtherCustomizeAssociationLink(xmlLink, oglLink)
            self._reconstituteLinkDataModel(oglLink)

        return oglLinks

    def getOglNotes(self, xmlOglNotes: NodeList) -> OglNotes:
        """
        Parse the XML elements given and build data layer for PyUt notes.

        Args:
            xmlOglNotes:        XML 'GraphicNote' elements

        Returns:
            The returned dictionary uses a generated ID for the key
        """
        oglNotes: OglNotes = cast(OglNotes, {})
        for xmlOglNote in xmlOglNotes:

            pyutNote: PyutNote = PyutNote()

            # Building OGL Note
            height: int = PyutUtils.strFloatToInt(xmlOglNote.getAttribute(OglToMiniDomConstants.ATTR_HEIGHT))
            width:  int = PyutUtils.strFloatToInt(xmlOglNote.getAttribute(OglToMiniDomConstants.ATTR_WIDTH))
            oglNote = OglNote(pyutNote, width, height)

            xmlNote: Element = xmlOglNote.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_NOTE)[0]

            pyutNote.id = int(xmlNote.getAttribute(OglToMiniDomConstants.ATTR_ID))

            content: str = xmlNote.getAttribute(OglToMiniDomConstants.ATTR_CONTENT)
            content = content.replace("\\\\\\\\", "\n")

            pyutNote.content = content

            pyutNote.fileName = xmlNote.getAttribute(OglToMiniDomConstants.ATTR_FILENAME)

            # Adding properties necessary to place shape on a diagram frame
            x: int = PyutUtils.strFloatToInt(xmlOglNote.getAttribute(OglToMiniDomConstants.ATTR_X))
            y: int = PyutUtils.strFloatToInt(xmlOglNote.getAttribute(OglToMiniDomConstants.ATTR_Y))

            oglNote.SetPosition(x, y)
            # Update the dictionary
            oglNotes[pyutNote.id] = oglNote

        return oglNotes

    def getOglTextShapes(self, xmlOglTextShapes: NodeList) -> OglTextShapes:

        oglTextShapes: OglTextShapes = cast(OglTextShapes, [])
        for xmlOglTextShape in xmlOglTextShapes:

            pyutText = self._getPyutText(xmlOglTextShape)

            width:  int = PyutUtils.strFloatToInt(xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_WIDTH))
            height: int = PyutUtils.strFloatToInt(xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_HEIGHT))

            oglText: OglText = OglText(pyutText=pyutText, width=width, height=height)

            x: int = PyutUtils.strFloatToInt(xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_X))
            y: int = PyutUtils.strFloatToInt(xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_Y))

            oglText.SetPosition(x=x, y=y)

            textSizeStr: str = xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_TEXT_SIZE)
            if textSizeStr is None or textSizeStr == '':
                oglText.textSize = 12       # TODO I do not want to pull in Preferences here
            else:
                oglText.textSize = int(textSizeStr)

            value = PyutUtils.secureBoolean(xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_IS_BOLD))
            oglText.isBold = value

            value = PyutUtils.secureBoolean(xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_IS_ITALICIZED))
            oglText.isItalicized = value

            value = xmlOglTextShape.getAttribute(OglToMiniDomConstants.ATTR_FONT_FAMILY)
            if value is not None and value != '':
                fontEnum: OglTextFontFamily = OglTextFontFamily(value)
                oglText.textFontFamily = fontEnum

            oglTextShapes.append(oglText)

        return oglTextShapes

    def _getPyutText(self, xmlOglTextShape):

        pyutText: PyutText = PyutText()

        xmlText: Element = xmlOglTextShape.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_TEXT)[0]

        pyutText.id = int(xmlText.getAttribute(OglToMiniDomConstants.ATTR_ID))
        content: str = xmlText.getAttribute(OglToMiniDomConstants.ATTR_CONTENT)

        pyutText.content = content.replace("\\\\\\\\", "\n")

        return pyutText

    def _getMethods(self, xmlClass: Element) -> PyutMethods:
        """
        Converts XML methods to `PyutMethod`s
        Args:
            xmlClass:  A DOM element that is a UML Class

        Returns:
            A list of `PyutMethod`s associated with the class
        """
        allMethods: PyutMethods = cast(PyutMethods, [])
        for xmlMethod in xmlClass.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_METHOD):

            pyutMethod: PyutMethod = PyutMethod(xmlMethod.getAttribute(OglToMiniDomConstants.ATTR_NAME))

            strVis: str = xmlMethod.getAttribute(OglToMiniDomConstants.ATTR_VISIBILITY)
            vis: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(strVis)
            pyutMethod.setVisibility(visibility=vis)

            returnElt:  Element  = xmlMethod.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_RETURN)[0]
            retTypeStr: str       = returnElt.getAttribute(OglToMiniDomConstants.ATTR_TYPE)
            pyutMethod.returnType = PyutType(retTypeStr)

            #
            #  Code supports multiple modifiers, but the dialog allows input of only one
            #
            modifiers: NodeList = xmlMethod.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_MODIFIER)
            for element in modifiers:
                xmlModifier: Element = cast(Element, element)
                modName:  str        = xmlModifier.getAttribute(OglToMiniDomConstants.ATTR_NAME)

                pyutModifier: PyutModifier = PyutModifier(modName)
                pyutMethod.addModifier(pyutModifier)

            methodParameters: PyutParameters = PyutParameters([])
            for xmlParam in xmlMethod.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_PARAM):
                methodParameters.append(self._getParam(xmlParam))

            pyutMethod.parameters = methodParameters

            sourceCodeXmlList: NodeList = xmlMethod.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_SOURCE_CODE)
            pyutMethod.sourceCode = self._getSourceCode(sourceCodeXmlList)

            allMethods.append(pyutMethod)

        return allMethods

    def _getImplementors(self, xmlClass: Element) -> Implementors:

        implementors: Implementors = Implementors([])
        for xmlImplementor in xmlClass.getElementsByTagName(OglToMiniDomConstants.ELEMENT_IMPLEMENTOR):
            className: ClassName = xmlImplementor.getAttribute(OglToMiniDomConstants.ATTR_IMPLEMENTING_CLASS_NAME)
            implementors.append(className)

        return implementors

    def _getParam(self, domElement: Element) -> PyutParameter:
        """

        Args:
            domElement:  The xml element tht is a parameter

        Returns:
            A parameter model object
        """
        paramTypeStr: str = domElement.getAttribute(OglToMiniDomConstants.ATTR_TYPE)
        paramType:    PyutType = PyutType(paramTypeStr)
        pyutParam: PyutParameter = PyutParameter(name=domElement.getAttribute(OglToMiniDomConstants.ATTR_NAME),
                                                 parameterType=paramType)

        if domElement.hasAttribute(OglToMiniDomConstants.ATTR_DEFAULT_VALUE):
            pyutParam.defaultValue = domElement.getAttribute(OglToMiniDomConstants.ATTR_DEFAULT_VALUE)

        return pyutParam

    def _getFields(self, xmlClass: Element) -> PyutFields:
        """
        Extracts fields from a DOM element that represents a UML class

        Args:
            xmlClass:
                The DOM version of a UML class

        Returns:
            PyutFields
        """
        pyutFields: PyutFields = cast(PyutFields, [])

        for element in xmlClass.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_FIELD):

            xmlField:   Element  = cast(Element, element)
            pyutField: PyutField = PyutField()

            strVis: str                = xmlField.getAttribute(OglToMiniDomConstants.ATTR_VISIBILITY)
            vis:    PyutVisibilityEnum = PyutVisibilityEnum.toEnum(strVis)

            pyutField.visibility = vis
            xmlParam: Element = xmlField.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_PARAM)[0]

            if xmlParam.hasAttribute(OglToMiniDomConstants.ATTR_DEFAULT_VALUE):
                pyutField.defaultValue = xmlParam.getAttribute(OglToMiniDomConstants.ATTR_DEFAULT_VALUE)
            pyutField.name = xmlParam.getAttribute(OglToMiniDomConstants.ATTR_NAME)

            pyutType: PyutType = PyutType(xmlParam.getAttribute(OglToMiniDomConstants.ATTR_TYPE))
            pyutField.type = pyutType

            pyutFields.append(pyutField)

        return pyutFields

    def _getSourceCode(self, sourceCodeXmlList: NodeList) -> SourceCode:

        xmlCode:    Element    = cast(Element, sourceCodeXmlList.item(0))
        sourceCode: SourceCode = SourceCode([])
        if xmlCode is not None:
            codeNodes:  NodeList   = xmlCode.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_CODE)

            for node in codeNodes:
                textNodeElement: Element = cast(Element, node)
                if len(textNodeElement.childNodes) > 0:
                    textNode:        Text    = textNodeElement.childNodes[0]
                    text:            str     = textNode.data
                    sourceCode.append(text)
        return sourceCode

    def _generateControlPoints(self, link: Element) -> ControlPoints:

        controlPoints: ControlPoints = cast(ControlPoints, [])

        for controlPoint in link.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_CONTROL_POINT):
            x = PyutUtils.strFloatToInt(controlPoint.getAttribute(OglToMiniDomConstants.ATTR_X))
            y = PyutUtils.strFloatToInt(controlPoint.getAttribute(OglToMiniDomConstants.ATTR_Y))
            controlPoints.append(ControlPoint(x, y))

        return controlPoints

    def _reconstituteLinkDataModel(self, oglLink: OglLink):
        """
        Updates one the following lists in a PyutLinkedObject:

        ._parents   for Inheritance links
        ._links     for all other link types

        Args:
            oglLink:       An OglLink
        """
        srcShape: OglClass = oglLink.getSourceShape()
        dstShape: OglClass = oglLink.getDestinationShape()
        self.logger.debug(f'source ID: {srcShape.GetID()} - destination ID: {dstShape.GetID()}')

        pyutLink: PyutLink = oglLink.pyutObject

        if pyutLink.linkType == PyutLinkType.INHERITANCE:
            childPyutClass:  PyutClass = cast(PyutClass, srcShape.pyutObject)
            parentPyutClass: PyutClass = cast(PyutClass, dstShape.pyutObject)
            childPyutClass.addParent(parentPyutClass)
        else:
            srcPyutClass:  PyutClass = cast(PyutClass, srcShape.pyutObject)
            srcPyutClass.addLink(pyutLink)

    def _findImplementor(self, implementor: str, oglClasses: OglClasses) -> OglClass:

        matchingOglClass: OglClass = cast(OglClass, None)

        for graphicClass in oglClasses.values():
            oglClass:  OglClass  = cast(OglClass, graphicClass)
            pyutClass: PyutClass = cast(PyutClass, oglClass.pyutObject)

            className: str = pyutClass.name
            if className == implementor:
                matchingOglClass = oglClass
                break

        assert matchingOglClass is not None, 'I really should find one'
        return matchingOglClass

    def _getPyutLink(self, obj: Element):
        """

        Args:
            obj:  The GraphicLink DOM element

        Returns:
            A tuple of a source ID, destination ID, and a PyutLink object
        """
        link: Element = obj.getElementsByTagName(OglToMiniDomConstants.ELEMENT_MODEL_LINK)[0]

        pyutLink: PyutLink = PyutLink()

        pyutLink.setBidir(bool(link.getAttribute(OglToMiniDomConstants.ATTR_BIDIRECTIONAL)))

        pyutLink.destinationCardinality = link.getAttribute(OglToMiniDomConstants.ATTR_CARDINALITY_DESTINATION)
        pyutLink.sourceCardinality      = link.getAttribute(OglToMiniDomConstants.ATTR_CARDINALITY_SOURCE)

        pyutLink.name = link.getAttribute(OglToMiniDomConstants.ATTR_NAME)

        strLinkType: str         = link.getAttribute(OglToMiniDomConstants.ATTR_TYPE)
        linkType:    PyutLinkType    = PyutLinkType.toEnum(strValue=strLinkType)
        pyutLink.linkType = linkType

        # source and destination will be reconstructed by _getOglLinks
        sourceId = int(link.getAttribute(OglToMiniDomConstants.ATTR_SOURCE_ID))
        dstId   = int(link.getAttribute(OglToMiniDomConstants.ATTR_DESTINATION_ID))

        return sourceId, dstId, pyutLink

    def _getAttachmentPoint(self, xmlOglInterface: Element, parent: OglClass) -> SelectAnchorPoint:

        attachmentPointStr: str             = xmlOglInterface.getAttribute(OglToMiniDomConstants.ATTR_LOLLIPOP_ATTACHMENT_POINT)
        attachmentPoint:    AttachmentLocation = AttachmentLocation.toEnum(attachmentPointStr)
        attachPosition:     OglPosition     = self._determineAttachmentPoint(attachmentPoint=attachmentPoint, oglClass=parent)

        anchorPoint: SelectAnchorPoint = SelectAnchorPoint(x=attachPosition.x, y=attachPosition.y, attachmentPoint=attachmentPoint, parent=parent)

        return anchorPoint

    def _determineAttachmentPoint(self, attachmentPoint: AttachmentLocation, oglClass: OglClass) -> OglPosition:

        oglPosition: OglPosition = OglPosition()

        dw, dh     = oglClass.GetSize()

        if attachmentPoint == AttachmentLocation.NORTH:
            northX: int = dw // 2
            northY: int = 0
            oglPosition.x = northX
            oglPosition.y = northY
        elif attachmentPoint == AttachmentLocation.SOUTH:
            southX = dw // 2
            southY = dh
            oglPosition.x = southX
            oglPosition.y = southY
        elif attachmentPoint == AttachmentLocation.WEST:
            westX: int = 0
            westY: int = dh // 2
            oglPosition.x = westX
            oglPosition.y = westY
        elif attachmentPoint == AttachmentLocation.EAST:
            eastX: int = dw
            eastY: int = dh // 2
            oglPosition.x = eastX
            oglPosition.y = eastY
        else:
            self.logger.warning(f'Unknown attachment point: {attachmentPoint}')
            assert False, 'Unknown attachment point'

        return oglPosition

    def __furtherCustomizeAssociationLink(self, xmlLink: Element, oglLink: OglAssociation):
        """
        Customize the visual aspects of an Association link
        Args:
            xmlLink:
            oglLink:
        """
        center: OglAssociationLabel = oglLink.centerLabel
        src:    OglAssociationLabel = oglLink.sourceCardinality
        dst:    OglAssociationLabel = oglLink.destinationCardinality

        self.__setAssociationLabelPosition(xmlLink, OglToMiniDomConstants.ELEMENT_ASSOC_CENTER_LABEL, center)
        self.__setAssociationLabelPosition(xmlLink, OglToMiniDomConstants.ELEMENT_ASSOC_SOURCE_LABEL, src)
        self.__setAssociationLabelPosition(xmlLink, OglToMiniDomConstants.ELEMENT_ASSOC_DESTINATION_LABEL, dst)

    def __setAssociationLabelPosition(self, xmlLink: Element, tagName: str, associationLabel: OglAssociationLabel):
        """

        Args:
            xmlLink:
            tagName:
            associationLabel:
        """
        label:  Element   = xmlLink.getElementsByTagName(tagName)[0]
        x: int = PyutUtils.strFloatToInt(label.getAttribute(OglToMiniDomConstants.ATTR_X))
        y: int = PyutUtils.strFloatToInt(label.getAttribute(OglToMiniDomConstants.ATTR_Y))

        self.logger.debug(f'tagName: {tagName} `{associationLabel.text=}`  pos: ({x:.2f},{y:.2f})')

        # associationLabel.x = x
        # associationLabel.y = y
        associationLabel.oglPosition.x = x
        associationLabel.oglPosition.y = y
