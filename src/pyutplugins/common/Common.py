
from typing import cast

from pathlib import Path

from wx import BITMAP_TYPE_PNG
from wx import Bitmap
from wx import ClientDC
from wx import Image
from wx import MemoryDC
from wx import NullBitmap
from wx import Window

# noinspection PyProtectedMember
from wx._core import BitmapType

from pyutplugins.ExternalTypes import FrameInformation

NO_PARENT_WINDOW:    Window         = cast(Window, None)


def createScreenImageFile(frameInformation: FrameInformation, imagePath: Path, imageType: BitmapType = BITMAP_TYPE_PNG) -> bool:
    """
    Create a screen image file
    Args:
        frameInformation:   Plugin frame information
        imagePath:          Where to write the image file to
        imageType:          Defaults to png

    Returns: 'True' for a successful creation else 'False'

    """

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
