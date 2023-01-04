
from dataclasses import dataclass

from pyutplugins.coretypes.ImportDirectoryResponse import ImportDirectoryResponse


@dataclass
class ExportDirectoryResponse(ImportDirectoryResponse):
    """
    Syntactic Sugar
    """
