
from dataclasses import dataclass

from plugins.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class SingleFileRequestResponse(BaseRequestResponse):
    fileName: str = ''
