from logging import Logger
from logging import getLogger

from tests.resources.testclasses.GraphElement import GraphElement


class SimpleClass(GraphElement):
    """
    This class allows me to test visibility and parameter lists.  It also allows me to
    test that this text appears as part of the class description.  ;-)
    """

    def __init__(self):

        super().__init__(name='Ozzee')
        self.logger: Logger = getLogger(__name__)

    def simpleMethod(self):
        pass

    def methodReturningInt(self) -> int:
        """

        Returns:  A hard code zero
        """
        return 0

    def methodReturningFloat(self) -> float:
        return 0.0

    def methodReturningString(self) -> str:
        return 'Ozzee es el gato malo'

    def methodWithParameters(self, intParameter: int, floatParameter: float, stringParameter: str):
        pass

    def methodWithParametersAndDefaultValues(self, intParameter: int = 0, floatParameter: float = 42.0, stringParameter: str = ''):
        pass

    def _protectedMethod(self):
        pass

    def __privateMethod(self):
        pass

    def __str__(self) -> str:
        return 'I am a test class'
