
from pathlib import Path

from wx import BITMAP_TYPE_PNG
from wx import Bitmap
from wx import ClientDC
from wx import Image
from wx import MemoryDC
from wx import NullBitmap

# noinspection PyProtectedMember
from wx._core import BitmapType

from pyutplugins.ExternalTypes import FrameInformation


def createScreenImageFile(frameInformation: FrameInformation, imagePath: Path) -> bool:
    """
    Create a screen image file
    Args:
        frameInformation:   Plugin frame information
        imagePath:          Where to write the image file to

    Returns: 'True' for a successful creation else 'False'

    """

    imageType: BitmapType = BITMAP_TYPE_PNG
    context:   ClientDC   = frameInformation.clientDC
    memory:    MemoryDC   = MemoryDC()

    x: int = frameInformation.frameSize.width
    y: int = frameInformation.frameSize.height
    emptyBitmap: Bitmap = Bitmap(x, y, -1)

    memory.SelectObject(emptyBitmap)
    memory.Blit(source=context, xsrc=0, height=y, xdest=0, ydest=0, ysrc=0, width=x)
    memory.SelectObject(NullBitmap)

    img: Image = emptyBitmap.ConvertToImage()

    status: bool = img.SaveFile(str(imagePath), imageType)

    return status
