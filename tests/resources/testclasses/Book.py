
from typing import List
from typing import NewType


class Page:
    def __init__(self):

        self._pageNumber: int = 0


Pages = NewType('Pages', List[Page])


class Book:
    def __init__(self):

        self._pages: Pages = Pages([])
