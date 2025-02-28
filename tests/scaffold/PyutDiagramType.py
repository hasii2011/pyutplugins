from enum import Enum


class PyutDiagramType(Enum):

    CLASS_DIAGRAM    = 0
    SEQUENCE_DIAGRAM = 1
    USECASE_DIAGRAM  = 2
    UNKNOWN_DIAGRAM  = 3

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def toEnum(cls, strValue: str) -> 'PyutDiagramType':
        """
        Converts the input string to the correct diagram type
        Args:
            strValue:   A string value

        Returns:  The diagram type enumeration
        """
        canonicalStr: str = strValue.strip(' ').lower()

        match canonicalStr:
            case 'class_diagram':
                return PyutDiagramType.CLASS_DIAGRAM
            case 'sequence_diagram':
                return PyutDiagramType.SEQUENCE_DIAGRAM
            case 'usecase_diagram':
                return PyutDiagramType.USECASE_DIAGRAM
            case _:
                print(f'Warning: did not recognize this diagram type: {canonicalStr}')
                return PyutDiagramType.CLASS_DIAGRAM
