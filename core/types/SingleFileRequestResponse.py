
from dataclasses import dataclass

from core.types.BaseRequestResponse import BaseRequestResponse


@dataclass
class SingleFileRequestResponse(BaseRequestResponse):
    fileName: str = ''
