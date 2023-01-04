
from dataclasses import dataclass

from plugins.coretypes.ImportDirectoryResponse import ImportDirectoryResponse


@dataclass
class ExportDirectoryResponse(ImportDirectoryResponse):
    """
    Syntactic Sugar
    """
