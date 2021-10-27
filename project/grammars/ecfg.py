from typing import AbstractSet, Iterable

from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from pyformlang.cfg import CFG

from ecfg_production import ECFGProduction
from project.utils.CFG_utils import CFGException

__all__ = ["ECFG"]


class ECFG:
    def __init__(self, variables=None, start_symbol=None, productions=None):
        self._variables = variables or set()
        self._start_symbol = start_symbol
        self._productions = productions or set()

    @property
    def variables(self) -> AbstractSet[Variable]:
        """Get variables"""
        return self._variables

    @property
    def productions(self) -> AbstractSet[ECFGProduction]:
        """Get productions"""
        return self._productions

    @property
    def start_symbol(self) -> Variable:
        """Get start_symbol"""
        return self._start_symbol

    def to_text(self) -> str:
        """Returns a string representation of CFG"""
        return "\n".join(str(p) for p in self.productions)

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")) -> "ECFG":
        """Converts string representation of ECFG into ECFG class object"""
        variables = set()
        productions = set()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise CFGException(
                    "There should be only one production per line."
                )

            head_text, body_text = production_objects
            head = Variable(head_text.strip())

            if head in variables:
                raise CFGException(
                    "There should be only one production for each variable."
                )

            variables.add(head)
            body = Regex(body_text.strip())
            productions.add(ECFGProduction(head, body))

        return ECFG(
            variables=variables, start_symbol=start_symbol, productions=productions
        )

    @classmethod
    def from_pyformlang_cfg(cls, cfg: CFG):
        productions = dict()

        for p in cfg.productions:
            body = Regex(" ".join(cfg_obj.value for cfg_obj in p.body) if p.body else "$")
            if p.head not in productions:
                productions[p.head] = body
            else:
                productions[p.head] = productions.get(p.head).union(body)

        ecfg_productions = [
            ECFGProduction(head, body) for head, body in productions.items()
        ]

        return ECFG(
            variables=cfg.variables,
            start_symbol=cfg.start_symbol,
            productions=ecfg_productions,
        )
