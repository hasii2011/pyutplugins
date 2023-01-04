
from dataclasses import dataclass

from plugins.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class ImportDirectoryResponse(BaseRequestResponse):
    directoryName: str = ''
