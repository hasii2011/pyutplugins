
from typing import List
from typing import Union

from logging import Logger
from logging import getLogger

from core.IMediator import IMediator
from core.ToolPluginInterface import ToolPluginInterface

from core.types.PluginDataTypes import PluginName

from core.types.DataTypes import OglClasses

from plugins.tools.sugiyama.RealSugiyamaNode import RealSugiyamaNode
from plugins.tools.sugiyama.Sugiyama import Sugiyama
from plugins.tools.sugiyama.SugiyamaLink import SugiyamaLink
from plugins.tools.sugiyama.VirtualSugiyamaNode import VirtualSugiyamaNode


class ToolSugiyama(ToolPluginInterface):
    """
    ToSugiyama : Automatic layout algorithm based on Sugiyama levels.
    """
    def __init__(self, mediator: IMediator):

        super().__init__(mediator)

        self.logger: Logger = getLogger(__name__)

        self._name      = PluginName('Sugiyama Automatic Layout')
        self._author    = 'Nicolas Dubois <nicdub@gmx.ch>'
        self._version   = '1.1'

        self._menuTitle = 'Sugiyama Automatic Layout'

        #
        # TODO Move to separate class
        #
        # Sugiyama nodes and links
        self.__realSugiyamaNodesList: List[RealSugiyamaNode] = []   # List of all RealSugiyamaNode
        self.__sugiyamaLinksList:     List[SugiyamaLink]     = []   # List of all SugiyamaLink

        #  Hierarchy graph
        #  List of Real and Virtual Sugiyama nodes that take part in hierarchy
        self.__hierarchyGraphNodesList:    List[Union[RealSugiyamaNode, VirtualSugiyamaNode]] = []
        #  List of Sugiyama nodes that are not in hierarchy
        self.__nonHierarchyGraphNodesList: List[VirtualSugiyamaNode] = []
        self.__nonHierarchyGraphLinksList: List[SugiyamaLink]        = []

        #  All nodes of the hierarchy are assigned to a level.
        #  A level is a list of nodes (real or virtual).
        self.__levels: List = []  # List of levels

    def setOptions(self) -> bool:
        """
        Prepare for the tool action.
        This can be used to ask some questions to the user.

        Returns: If False, the import should be cancelled.  'True' to proceed
        """
        return True

    def doAction(self):
        selectedObjects: OglClasses = self._mediator.selectedOglObjects

        self.logger.info(f'Begin Sugiyama algorithm')

        sugiyama: Sugiyama = Sugiyama(mediator=self._mediator)
        sugiyama.createInterfaceOglALayout(oglObjects=selectedObjects)
        sugiyama.levelFind()
        sugiyama.addVirtualNodes()
        sugiyama.barycenter()

        # self.logger.info(f'Number of hierarchical intersections: {sugiyama._getNbIntersectAll()}')

        sugiyama.addNonHierarchicalNodes()
        sugiyama.fixPositions()

        self._mediator.refreshFrame()

        self.logger.info('End Sugiyama algorithm')
