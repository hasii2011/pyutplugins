
from dataclasses import dataclass

from pyutplugincore.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class ImportDirectoryResponse(BaseRequestResponse):
    directoryName: str = ''
