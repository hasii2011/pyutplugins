
from dataclasses import dataclass

from core.types.ImportDirectoryResponse import ImportDirectoryResponse


@dataclass
class ExportDirectoryResponse(ImportDirectoryResponse):
    """
    Syntactic Sugar
    """
