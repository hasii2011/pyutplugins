
from dataclasses import dataclass

from pyutplugincore.coretypes.BaseRequestResponse import BaseRequestResponse


@dataclass
class SingleFileRequestResponse(BaseRequestResponse):
    fileName: str = ''
