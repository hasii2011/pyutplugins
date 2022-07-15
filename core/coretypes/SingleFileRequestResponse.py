
from dataclasses import dataclass

from core.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class SingleFileRequestResponse(BaseRequestResponse):
    fileName: str = ''
