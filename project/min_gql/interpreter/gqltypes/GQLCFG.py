from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet

from pyformlang.cfg import CFG
from project.grammars.ecfg import ECFG
from project.utils.cfg_utils import transform_ecfg_to_rsm
from project.utils.rsm_sparse import RSMMatrixSparse

from project.min_gql.interpreter.exceptions import NotImplementedException, ConversionException


class GQLCFG(GQLAutomata):
    def __init__(self, cfg: CFG):
        self.cfg = cfg

    @classmethod
    def fromText(cls, text: str):
        try:
            cfg = CFG.from_text(text=text)
            return cls(cfg=cfg)
        except ValueError as e:
            raise ConversionException("str", "CFG") from e

    def intersect(self, other):
        if not isinstance(other, GQLAutomata):
            raise ConversionException("Can't intersect GQLCFG with", str(type(other)))

        if isinstance(other, GQLCFG):
            raise ConversionException("Can't intersect GQLCFG with", "GQLCFG")

        intersection = self.cfg.intersection(other.nfa)

        return GQLCFG(cfg=intersection)

    def union(self, other):
        if isinstance(other, GQLCFG):
            return GQLCFG(cfg=self.cfg.union(other.cfg))

        raise NotImplementedException("Union is implemented only for GQLCFG types")

    def dot(self, other):
        if isinstance(other, GQLCFG):
            return GQLCFG(cfg=self.cfg.concatenate(other.cfg))

        raise NotImplementedException("Dot is implemented only for GQLCFG types")

    def inverse(self):
        raise NotImplementedException("GQLCFG.inverse")

    def kleene(self):
        raise NotImplementedException("GQLCFG.kleene")

    def __str__(self):
        return self.cfg.to_text()

    def setStart(self, start_states):
        raise NotImplementedException("Can't set start symbol to CFG after creation")

    def setFinal(self, final_states):
        raise NotImplementedException("Can't set final symbol to CFG")

    def addStart(self, start_states):
        raise NotImplementedException("Can't add more start symbols to CFG")

    def addFinal(self, final_states):
        raise NotImplementedException("Can't add final symbols to CFG")

    @property
    def start(self):
        return GQLSet(self.cfg.start_symbol.value)

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
        ecfg = ECFG.from_pyformlang_cfg(self.cfg)
        rsm = transform_ecfg_to_rsm(ecfg)
        rsm_bm = RSMMatrixSparse.from_rsm(rsm)
        tc = rsm_bm.get_transitive_closure()
        reachable = set()
        for i, j in zip(*tc.nonzero()):
            reachable.add((i, rsm_bm.get_nonterminals(i, j), j))

        return GQLSet(reachable)
