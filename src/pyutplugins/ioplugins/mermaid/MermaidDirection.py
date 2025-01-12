
from enum import Enum


class MermaidDirection(Enum):

    RightToLeft = 'direction RL'
    LeftToRight = 'direction LR'

    @classmethod
    def toEnum(cls, enumStr: str) -> 'MermaidDirection':

        assert (enumStr is not None) and (enumStr != ''), 'I need a real string dude'
        match enumStr:
            case MermaidDirection.RightToLeft.value:
                retEnum: MermaidDirection = MermaidDirection.RightToLeft
            case MermaidDirection.LeftToRight.value:
                retEnum = MermaidDirection.LeftToRight
            case _:
                print(f'Unknown enumeration string {enumStr}')
                retEnum = MermaidDirection.LeftToRight

        return retEnum
