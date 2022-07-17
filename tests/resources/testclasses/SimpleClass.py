from logging import Logger
from logging import getLogger

from tests.resources.testclasses.GraphElement import GraphElement


class SimpleClass(GraphElement):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def simpleMethod(self):
        pass

    def methodReturningInt(self) -> int:
        return 0

    def methodReturningFloat(self) -> float:
        return 0.0

    def methodReturningString(self) -> str:
        return 'Ozzee es el gato malo'

    def methodWithParameters(self, intParameter: int, floatParameter: float, stringParameter: str):
        pass

    def methodWithParametersAndDefaultValues(self, intParameter: int = 0, floatParameter: float = 42.0, stringParameter: str = ''):
        pass
