
from core.PluginInterface import PluginInterface

from core.coretypes.PluginDataTypes import PluginDescription
from core.coretypes.PluginDataTypes import PluginExtension
from core.coretypes.PluginDataTypes import PluginName

from core.ICommunicator import ICommunicator
from core.coretypes.InputFormat import InputFormat
from core.coretypes.OutputFormat import OutputFormat


class SamplePluginInterface(PluginInterface):

    def __init__(self, communicator: ICommunicator):
        super().__init__(communicator)

    @property
    def name(self) -> str:
        """
        Returns:  The plugin name
        """
        return 'Unit Test Plugin'

    @property
    def author(self) -> str:
        """
        Returns:  The author's name
        """
        return 'Ozzee K. Sanchez'

    @property
    def version(self) -> str:
        """
        Returns: The plugin version string
        """
        return '1.0.0'

    @property
    def inputFormat(self) -> InputFormat:
        """
        Implementations need to override this

        Returns:
            The input format type
        """
        return InputFormat(PluginName('TestPlugin'), PluginExtension('xml'), PluginDescription('A Test Plugin'))

    @property
    def outputFormat(self) -> OutputFormat:

        """
        Implementations need to override this

        otherwise, return a tuple with
            name of the output format
            extension of the output format
            textual description of the plugin output format
        example:
            return ("Text", "txt", "Tabbed text...")

        Returns:
            Return a specification tuple.  None if the plugin can not write.
        """
        return OutputFormat(PluginName('TestPlugin'), PluginExtension('xml'), PluginDescription('A Test Plugin'))
