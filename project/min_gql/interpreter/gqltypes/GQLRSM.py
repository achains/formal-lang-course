from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLFA import GQLFA
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet

from project.grammars.rsm import RSM
from project.grammars.ecfg import ECFG
from project.utils.cfg_utils import transform_ecfg_to_rsm

from pyformlang.cfg import CFG

from project.min_gql.interpreter.exceptions import NotImplementedException, ConversionException


class GQLRSM(GQLAutomata):
    def __init__(self, rsm):
        self.rsm = rsm
        self.reachable = None

    @classmethod
    def fromText(cls, text: str):
        try:
            ecfg = ECFG.from_text(text=text)
            return cls(rsm=transform_ecfg_to_rsm(ecfg))
        except ValueError as e:
            raise ConversionException("str", "ECFG") from e

    def intersect(self, other):
        if isinstance(other, GQLFA):
            intersection = self.rsm.to_pda().intersection(other)
        else:
            raise ConversionException("Can't intersect GQLRSM with", str(type(other)))

        return GQLRSM(rsm=intersection.to_cfg())

    def union(self, other):
        if isinstance(other, GQLRSM):
            return GQLRSM(rsm=self.rsm.union(other.rsm))

        raise NotImplementedException("Union is implemented only for GQLRSM types")

    def dot(self, other):
        if isinstance(other, GQLRSM):
            return GQLRSM(rsm=self.rsm.concatenate(other.rsm))

    def inverse(self):
        raise NotImplementedException("GQLRSM.inverse")

    def kleene(self):
        raise NotImplementedException("GQLRSM.kleene")

    def __str__(self):
        return self.cfg.to_text()

    def setStart(self, start_states):
        pass

    def setFinal(self, final_states):
        pass

    def addStart(self, start_states):
        pass

    def addFinal(self, final_states):
        pass

    @property
    def start(self):
        return GQLSet(set(self.rsm.start_symbol.to_text()))

    @property
    def final(self):
        raise NotImplementedException("GQLRSM.final")

    @property
    def labels(self):
        raise NotImplementedException("GQLRSM.labels")

    @property
    def edges(self):
        raise NotImplementedException("GQLRSM.edges")

    @property
    def vertices(self):
        return GQLSet(set(self.rsm.variables))

    def getReachable(self):
        raise NotImplementedException("GQLRSM.reachable")
