from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

__all__ = ["ECFGProduction"]


class ECFGProduction:
    def __init__(self, head: Variable, body: Regex):
        self._head = head
        self._body = body

    def __str__(self):
        return str(self._head) + " -> " + str(self._body)

    @property
    def head(self):
        """Get head"""
        return self._head

    @property
    def body(self):
        """Get body"""
        return self._body


