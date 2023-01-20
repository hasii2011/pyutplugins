
from dataclasses import dataclass

from pyutplugins.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class ImportDirectoryResponse(BaseRequestResponse):
    directoryName: str = ''
