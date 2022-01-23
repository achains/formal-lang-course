from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLCFG import GQLCFG
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.utils.automata_utils import (
    transform_graph_to_nfa,
    add_nfa_states,
    replace_nfa_states,
)
from project.utils.automata_utils import transform_regex_to_dfa, AutomataException
from project.utils.rsm_sparse import RSMMatrixSparse
from project.rpq.rpq import get_reachable


from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.min_gql.interpreter.exceptions import (
    NotImplementedException,
    ConversionException,
    GQLTypeError,
)


class GQLFA(GQLAutomata):
    """
    Representation of Finite-Automata

    Attributes
    ----------
    nfa: NondeterministicFiniteAutomaton
        Internal nfa object
    """

    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        self.nfa = nfa

    @classmethod
    def fromGraph(cls, graph: MultiDiGraph) -> "GQLFA":
        """

        Parameters
        ----------
        graph: MultiDiGraph
            Transform graph into automata

        Returns
        -------
        fa: GQLFA
            Automata transformed from graph
        """
        return cls(nfa=transform_graph_to_nfa(graph))

    @classmethod
    def fromString(cls, regex_str: str) -> "GQLFA":
        """

        Parameters
        ----------
        regex_str: str
            Transform regular-expression string into automata

        Returns
        -------
        fa: GQLFA
            Automata transformed from string

        Raises
        ------
        ConversionException
            If given string violates regular expression rules
        """
        try:
            return GQLFA(nfa=transform_regex_to_dfa(regex_str))
        except AutomataException as exc:
            raise ConversionException("Regular string", "str") from exc

    def __intersectFA(self, other: "GQLFA") -> "GQLFA":
        """
        Inner intersection (FA & FA) function

        Parameters
        ----------
        other: GQLFA
            Finite Automata

        Returns
        -------
        intersection: GQLFA
            Intersection of two FA
        """
        lhs = RSMMatrixSparse.from_nfa(self.nfa)
        rhs = RSMMatrixSparse.from_nfa(other.nfa)
        intersection = lhs.intersect(rhs)
        return GQLFA(nfa=intersection.to_nfa())

    def __intersectCFG(self, other: GQLCFG) -> GQLCFG:
        """
        Inner intersection (FA & CFG) function

        Parameters
        ----------
        other: GQLCFG
            Context Free Grammar
        Returns
        -------
        intersection: GQLCFG
            Intersection of FA with GQLCFG
        """
        intersection = other.intersect(self)
        return intersection

    def intersect(self, other: GQLAutomata) -> GQLAutomata:
        """
        Automata & Automata intersection

        Parameters
        ----------
        other: GQLCFG | GQLFA
            CFG or FA object

        Returns
        -------
        intersection: GQLAutomata
            cfg, IF 'other' is GQLCFG
            fa, IF 'other' is GQLFA

        Raises
        ------
        GQLTypeError
            If object does not represent FA or CFG
        """
        if isinstance(other, GQLFA):
            return self.__intersectFA(other=other)
        if isinstance(other, GQLCFG):
            return self.__intersectCFG(other=other)

        raise GQLTypeError(f"Expected GQLAutomata, got {str(type(other))} instead")

    def union(self, other: "GQLFA") -> "GQLFA":
        """

        Parameters
        ----------
        other: GQLFA
            rhs FA

        Returns
        -------
        union: GQLFA
            Union of two FA
        """
        return GQLFA(self.nfa.union(other.nfa).to_deterministic())

    def dot(self, other: "GQLFA") -> "GQLFA":
        """

        Parameters
        ----------
        other: GQLFA
            rhs FA

        Returns
        -------
        dot: GQLFA
            Dot of two FA
        """
        lhs = self.nfa.to_regex()
        rhs = other.nfa.to_regex()
        return GQLFA(lhs.concatenate(rhs).to_epsilon_nfa().to_deterministic())

    def inverse(self) -> "GQLFA":
        """
        Get complement of FA

        Returns
        -------
        complement: GQLFA
            Complement of FA
        """
        return GQLFA(self.nfa.get_complement().to_deterministic())

    def kleene(self) -> "GQLFA":
        """

        Returns
        -------
        kleene: GQLFA
            Kleene closure of FA
        """
        return GQLFA(nfa=self.nfa.kleene_star().to_deterministic())

    def __str__(self):
        return str(self.nfa.minimize().to_regex())

    def setStart(self, start_states: GQLSet) -> "GQLFA":
        nfa = replace_nfa_states(self.nfa, start_states=start_states.data)
        return GQLFA(nfa)

    def setFinal(self, final_states: GQLSet) -> "GQLFA":
        nfa = replace_nfa_states(self.nfa, final_states=final_states.data)
        return GQLFA(nfa)

    def addStart(self, start_states: GQLSet) -> "GQLFA":
        nfa = add_nfa_states(self.nfa, start_states=start_states.data)
        return GQLFA(nfa)

    def addFinal(self, final_states: GQLSet) -> "GQLFA":
        nfa = add_nfa_states(self.nfa, final_states=final_states.data)
        return GQLFA(nfa)

    @staticmethod
    def __getReachable(nfa: NondeterministicFiniteAutomaton) -> set:
        """
        Internal helper function to get reachable vertices set

        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton
            Finite Automata
        Returns
        -------
        reachable: set
            Reachable vertices set
        """
        bmatrix = RSMMatrixSparse.from_nfa(nfa)
        query = RSMMatrixSparse.from_nfa(transform_regex_to_dfa("epsilon"))
        return get_reachable(bmatrix, query)

    # TODO: start, final should be pretty-printed?

    def getReachable(self) -> GQLSet:
        """

        Returns
        -------
        reachable: GQLSet
            Reachable vertices set
        """
        return GQLSet(GQLFA.__getReachable(self.nfa))

    @property
    def start(self) -> GQLSet:
        return GQLSet(self.nfa.start_states)

    @property
    def final(self) -> GQLSet:
        return GQLSet(self.nfa.final_states)

    @property
    def labels(self) -> GQLSet:
        return GQLSet(self.nfa.symbols)

    @property
    def edges(self) -> GQLSet:
        raise NotImplementedException("GQLFA.edges")

    @property
    def vertices(self) -> GQLSet:
        return GQLSet(self.nfa.states)
