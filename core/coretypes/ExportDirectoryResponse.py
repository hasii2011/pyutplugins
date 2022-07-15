
from dataclasses import dataclass

from core.coretypes.ImportDirectoryResponse import ImportDirectoryResponse


@dataclass
class ExportDirectoryResponse(ImportDirectoryResponse):
    """
    Syntactic Sugar
    """
