

simpleAssignment: int = 0


def standAloneMethod():
    print('I should not appear in a class')


class SimpleClassWithCode:

    def __init__(self):
        self._age:           int   = 3
        self._publicEars:    float = 2
        self._protectedTail: bool  = True

    def publicMethod(self, param1: float = 23.0) -> bool:
        ans: bool = False
        if param1 > 23:
            ans = False

        return ans
