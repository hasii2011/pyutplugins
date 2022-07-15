
from dataclasses import dataclass

from core.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class ImportDirectoryResponse(BaseRequestResponse):
    directoryName: str = ''
