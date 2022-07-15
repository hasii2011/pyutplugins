
from dataclasses import dataclass

from core.types.BaseRequestResponse import BaseRequestResponse


@dataclass
class ImportDirectoryResponse(BaseRequestResponse):
    directoryName: str = ''
