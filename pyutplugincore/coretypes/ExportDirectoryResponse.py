
from dataclasses import dataclass

from pyutplugincore.coretypes.ImportDirectoryResponse import ImportDirectoryResponse


@dataclass
class ExportDirectoryResponse(ImportDirectoryResponse):
    """
    Syntactic Sugar
    """
