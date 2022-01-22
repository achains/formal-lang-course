from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet

from pyformlang.cfg import CFG
from project.grammars.ecfg import ECFG
from project.utils.cfg_utils import transform_ecfg_to_rsm
from project.utils.rsm_sparse import RSMMatrixSparse

from project.min_gql.interpreter.exceptions import (
    NotImplementedException,
    ConversionException,
    GQLTypeError,
)


class GQLCFG(GQLAutomata):
    """
    Representation of Context-Free-Grammar

    Attributes
    ----------
    cfg: CFG
        Internal CFG object
    """

    def __init__(self, cfg: CFG):
        self.cfg = cfg

    @classmethod
    def fromText(cls, text: str):
        """

        Parameters
        ----------
        text: str
            String given in terms of CFG
            E.g. 'S -> a S
                  S -> epsilon'
        Returns
        -------
        cfg: GQLCFG
            Object transformed from text

        Raises
        ------
        ConversionException
            If text violates CFG format
        """
        try:
            cfg = CFG.from_text(text=text)
            return cls(cfg=cfg)
        except ValueError as e:
            raise ConversionException("str", "CFG") from e

    def intersect(self, other: GQLAutomata) -> "GQLCFG":
        """

        Parameters
        ----------
        other: GQLFA
            Finite automata (regular expression)

        Returns
        -------
        intersection: GQLCFG
            Intersection of CFG and FA

        Raises
        ------
        GQLTypeError
            If 'other' type is not GQLFA
        """
        if not isinstance(other, GQLAutomata):
            raise GQLTypeError(
                f"Expected finite automata, got {str(type(other))} instead"
            )

        if isinstance(other, GQLCFG):
            raise GQLTypeError(f"Can't intersect CFG with another CFG")

        intersection = self.cfg.intersection(other.nfa)

        return GQLCFG(cfg=intersection)

    def union(self, other: GQLAutomata) -> "GQLCFG":
        """

        Parameters
        ----------
        other: GQLAutomata
            Automata object

        Returns
        -------
        union: GQLCFG
            Union of CFG with 'other'
        """
        if isinstance(other, GQLCFG):
            return GQLCFG(cfg=self.cfg.union(other.cfg))

        raise NotImplementedException("Union is implemented only for GQLCFG types")

    def dot(self, other: GQLAutomata) -> "GQLCFG":
        """
        Concatenation of CFG with another automata

        Parameters
        ----------
        other: GQLAutomata
            Automata object
        Returns
        -------
        concatenation: GQLCFG
            Concatenation of CFG and 'other'
        """
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
    def start(self) -> GQLSet:
        return GQLSet(self.cfg.start_symbol.value)

    @property
    def final(self) -> GQLSet:
        return GQLSet(set(self.cfg.get_reachable_symbols()))

    @property
    def labels(self) -> GQLSet:
        return GQLSet(set(self.cfg.terminals))

    @property
    def edges(self) -> GQLSet:
        raise NotImplementedException("GQLCFG.edges")

    @property
    def vertices(self) -> GQLSet:
        return GQLSet(set(self.cfg.variables))

    def getReachable(self) -> GQLSet:
        """
        Get reachable vertices from the start

        Returns
        -------
        reachable: GQLSet
            Set of reachable vertices
        """
        ecfg = ECFG.from_pyformlang_cfg(self.cfg)
        rsm = transform_ecfg_to_rsm(ecfg)
        rsm_bm = RSMMatrixSparse.from_rsm(rsm)
        tc = rsm_bm.get_transitive_closure()
        reachable = set()
        for i, j in zip(*tc.nonzero()):
            reachable.add((i, rsm_bm.get_nonterminals(i, j), j))

        return GQLSet(reachable)
