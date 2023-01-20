
from dataclasses import dataclass

from pyutplugins.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class SingleFileRequestResponse(BaseRequestResponse):
    fileName: str = ''
