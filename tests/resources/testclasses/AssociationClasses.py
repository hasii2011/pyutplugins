
from typing import List
from typing import NewType

TEST_CONSTANT: int = 66

TEST_ASSIGNMENT = 77


class Page:
    def __init__(self):

        self._pageNumber:  int = 0
        self._text:        str = ''
        self.initProperty: float = 0.0

    @property
    def text(self) -> str:
        return self._text


Pages = NewType('Pages', List[Page])


class Chapter:
    def __init__(self):
        self._pages: Pages = Pages([])

    @property
    def pages(self) -> Pages:
        return self._pages


Chapters = NewType("Chapters", List[Chapter])


class Book:
    def __init__(self):
        self._chapters: Chapters = Chapters(Pages([]))

    @property
    def chapters(self) -> Chapters:
        return self._chapters
