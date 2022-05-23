
from logging import Logger
from logging import getLogger


class PyutUtils:
    """
    """

    clsLogger: Logger = getLogger(__name__)

    def __init__(self):

        PyutUtils.logger = getLogger(__name__)

    @staticmethod
    def strFloatToInt(floatValue: str) -> int:
        """
        Will fail during development with assertions turned on

        Args:
            floatValue:

        Returns:  An integer value
        """
        assert floatValue is not None, 'Cannot be None'
        assert floatValue != '', 'Cannot be empty string'
        assert floatValue.replace('.', '', 1).isdigit(), 'String must be numeric'

        integerValue: int = int(float(floatValue))

        return integerValue

    @staticmethod
    def secureBoolean(x: str):
        try:
            if x is not None:
                if x in [True, "True", "true", 1, "1"]:
                    return True
        except (ValueError, Exception) as e:
            PyutUtils.clsLogger.error(f'secureBoolean error: {e}')
        return False

