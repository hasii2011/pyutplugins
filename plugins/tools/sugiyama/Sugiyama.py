
from typing import List
from typing import Union

from logging import Logger
from logging import getLogger

from ogl.OglInheritance import OglInheritance
from ogl.OglInterface import OglInterface
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from plugins.tools.sugiyama.RealSugiyamaNode import RealSugiyamaNode
from plugins.tools.sugiyama.SugiyamaLink import SugiyamaLink
from plugins.tools.sugiyama.VirtualSugiyamaNode import VirtualSugiyamaNode


class Sugiyama:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        # Sugiyama nodes and links
        self.__realSugiyamaNodesList: List[RealSugiyamaNode] = []   # List of all RealSugiyamaNode
        self.__sugiyamaLinksList:     List[SugiyamaLink]     = []   # List of all SugiyamaLink

        #  Hierarchy graph
        #  List of Real and Virtual Sugiyama nodes that take part in hierarchy
        self._hierarchyGraphNodesList:    List[Union[RealSugiyamaNode, VirtualSugiyamaNode]] = []
        #  List of Sugiyama nodes that are not in hierarchy
        self._nonHierarchyGraphNodesList: List[VirtualSugiyamaNode] = []
        self._nonHierarchyGraphLinksList: List[SugiyamaLink]        = []

        #  All nodes of the hierarchy are assigned to a level.
        #  A level is a list of nodes (real or virtual).
        self.__levels: List = []  # List of levels

    def createInterfaceOglALayout(self, oglObjects):
        """
        Create the interface between oglObjects and Automatic Layout
        structure. A RealSugiyamaNode is created for each class, and a
        SugiyamaLink is created for each relation in the UML diagram.

        Args:
            oglObjects:  The Ogl Objects in the diagram
        """
        # Dictionary for oglObjects fast research
        # Key = OglObject, Value = RealSugiyamaNode
        dictOgl     = {}
        # Dictionary for RealSugiyamaNode that takes part in hierarchy
        # Key = OglObject, Value = None
        dictSugiyamaHierarchy = {}

        def createSugiyamaNode(theOglObject, theDictOgl):
            """
            Internal function for creating a RealSugiyamaNode and add it to
            self.__realSugiyamaNodesList and to dictOgl
            Args:
                theOglObject:
                theDictOgl:
            """
            # Create RealSugiyamaNode only if not already done
            if theOglObject not in theDictOgl:
                node = RealSugiyamaNode(theOglObject)
                self.__realSugiyamaNodesList.append(node)
                theDictOgl[theOglObject] = node

        def addNode2HierarchyGraph(theSugiyamaNode, theDictSugiyamaHierarchy):
            """
            Internal function for adding nodes that take part in hierarchy in
            the __hierarchyGraphNodesList.

            Args:
                theSugiyamaNode:
                theDictSugiyamaHierarchy:
            """
            if theSugiyamaNode not in theDictSugiyamaHierarchy:
                theDictSugiyamaHierarchy[theSugiyamaNode] = None
                self._hierarchyGraphNodesList.append(theSugiyamaNode)

        # For each OglObject or OglLink, create a specific interface
        for oglObject in oglObjects:

            # Class or Note :
            if isinstance(oglObject, OglObject):
                createSugiyamaNode(oglObject, dictOgl)
            # Links
            elif isinstance(oglObject, OglLink):

                # Get source and destination oglObject
                srcOglClass = oglObject.getSourceShape()
                dstOglClass = oglObject.getDestinationShape()

                # If the classes have not a RealSugiyamaNode attributed yet
                createSugiyamaNode(srcOglClass, dictOgl)
                createSugiyamaNode(dstOglClass, dictOgl)

                # Fix relations between nodes
                link = SugiyamaLink(oglObject)
                self.__sugiyamaLinksList.append(link)
                srcSugiyamaNode = dictOgl[srcOglClass]
                dstSugiyamaNode = dictOgl[dstOglClass]
                link.setSource(srcSugiyamaNode)
                link.setDestination(dstSugiyamaNode)

                # If hierarchical link
                if isinstance(oglObject, OglInheritance) or isinstance(oglObject, OglInterface):

                    srcSugiyamaNode.addParent(dstSugiyamaNode, link)
                    dstSugiyamaNode.addChild(srcSugiyamaNode, link)

                    # Add nodes in list of hierarchical nodes
                    addNode2HierarchyGraph(srcSugiyamaNode, dictSugiyamaHierarchy)
                    addNode2HierarchyGraph(dstSugiyamaNode, dictSugiyamaHierarchy)

                # Non-hierarchical links
                else:

                    # Add link between source and destination interface
                    srcSugiyamaNode.addNonHierarchicalLink(dstSugiyamaNode, link)
                    dstSugiyamaNode.addNonHierarchicalLink(srcSugiyamaNode, link)

                    # Add link into non-hierarchical links' list
                    self._nonHierarchyGraphLinksList.append(link)

        # Create list of non-hierarchical nodes

        # For each class or note
        for sugiyamaNode in list(dictOgl.values()):
            # If not in hierarchy
            if sugiyamaNode not in dictSugiyamaHierarchy:
                self._nonHierarchyGraphNodesList.append(sugiyamaNode)
