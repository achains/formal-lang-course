from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLFA import GQLFA
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.min_gql.interpreter.gqltypes.GQLRegex import GQLRegex

from pyformlang.cfg import CFG
from pyformlang.pda import PDA

from project.min_gql.interpreter.exceptions import NotImplementedException, ConversionException


class GQLCFG(GQLAutomata):
    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self.reachable = None

    @classmethod
    def fromText(cls, text: str):
        try:
            cfg = CFG.from_text(text=text)
            return cls(cfg=cfg)
        except ValueError as e:
            raise ConversionException("str", "CFG") from e


    def intersect(self, other):
        if isinstance(other, GQLFA):
            intersection = self.cfg.to_pda().intersection(other)
        elif isinstance(other, GQLRegex):
            fa = GQLRegex.fromString(other.regex_str)
            intersection = self.cfg.to_pda().intersection(fa.nfa)
        else:
            raise ConversionException("Can't intersect GQLCFG with", str(type(other)))

        return GQLCFG(cfg=intersection.to_cfg())

    def union(self, other):
        if isinstance(other, GQLCFG):
            return GQLCFG(cfg=self.cfg.union(other.cfg))

        raise NotImplementedException("Union is implemented only for GQLCFG types")

    def dot(self, other):
        if isinstance(other, GQLCFG):
            return GQLCFG(cfg=self.cfg.concatenate(other.cfg))

    def inverse(self):
        raise NotImplementedException("GQLCFG.inverse")

    def kleene(self):
        raise NotImplementedException("GQLCFG.kleene")

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
        return GQLSet(set(self.cfg.start_symbol.to_text()))

    @property
    def final(self):
        raise NotImplementedException("GQLCFG.final")

    @property
    def labels(self):
        raise NotImplementedException("GQLCFG.labels")

    @property
    def edges(self):
        raise NotImplementedException("GQLCFG.edges")

    @property
    def vertices(self):
        return GQLSet(set(self.cfg.variables))

    def getReachable(self):
        raise NotImplementedException("GQLCFG.reachable")
