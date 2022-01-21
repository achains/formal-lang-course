from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLRSM import GQLRSM
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.utils.automata_utils import transform_graph_to_nfa, add_nfa_states, replace_nfa_states
from project.utils.automata_utils import transform_regex_to_dfa, AutomataException
from project.utils.rsm_sparse import RSMMatrixSparse
from project.rpq.rpq import get_reachable


from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.min_gql.interpreter.exceptions import NotImplementedException, ConversionException


class GQLFA(GQLAutomata):
    def __init__(self, nfa: NondeterministicFiniteAutomaton, reachable_set: set = None):
        self.nfa = nfa
        self.reachable_set = reachable_set or self.__getReachable(nfa=nfa)

    @classmethod
    def fromGraph(cls, graph: MultiDiGraph):
        return cls(nfa=transform_graph_to_nfa(graph))

    @classmethod
    def fromString(cls, regex_str: str):
        try:
            return GQLFA(nfa=transform_regex_to_dfa(regex_str))
        except AutomataException as exc:
            raise ConversionException from exc

    def __intersectFA(self, other: "GQLFA") -> "GQLFA":
        lhs = RSMMatrixSparse.from_nfa(self.nfa)
        rhs = RSMMatrixSparse.from_nfa(other.nfa)
        intersection = lhs.intersect(rhs)
        return GQLFA(nfa=intersection.to_nfa(), reachable_set=get_reachable(bmatrix=intersection))

    def __intersectRSM(self, other: GQLRSM) -> GQLRSM:
        lhs = RSMMatrixSparse.from_nfa(self.nfa)
        rhs = RSMMatrixSparse.from_rsm(other.rsm)
        intersection = lhs.intersect(rhs)
        return GQLRSM(rsm=intersection.to_rsm())

    def intersect(self, other):
        if isinstance(other, GQLFA):
            return self.__intersectFA(other=other)
        if isinstance(other, GQLRSM):
            return self.__intersectRSM(other=other)

        raise ConversionException

    def union(self, other):
        return GQLFA(self.nfa.union(other.nfa).to_deterministic())

    def dot(self, other):
        lhs = self.nfa.to_regex()
        rhs = other.nfa.to_regex()
        return GQLFA(lhs.concatenate(rhs).to_epsilon_nfa().to_deterministic())

    def inverse(self):
        return GQLFA(self.nfa.get_complement().to_deterministic())

    def kleene(self):
        return GQLFA(nfa=self.nfa.kleene_star().to_deterministic())

    def __str__(self):
        return str(self.nfa.minimize().to_regex())

    def setStart(self, start_states: GQLSet):
        self.nfa = replace_nfa_states(self.nfa, start_states=start_states.data)

    def setFinal(self, final_states: GQLSet):
        self.nfa = replace_nfa_states(self.nfa, final_states=final_states.data)

    def addStart(self, start_states: GQLSet):
        self.nfa = add_nfa_states(self.nfa, start_states=start_states.data)

    def addFinal(self, final_states: GQLSet):
        self.nfa = add_nfa_states(self.nfa, final_states=final_states.data)

    @staticmethod
    def __getReachable(nfa: NondeterministicFiniteAutomaton) -> set:
        bmatrix = RSMMatrixSparse.from_nfa(nfa)
        return get_reachable(bmatrix)

    # TODO: start, final should be pretty-printed?

    def getReachable(self):
        return GQLSet(self.reachable_set)

    @property
    def start(self):
        return GQLSet(self.nfa.start_states)

    @property
    def final(self):
        return GQLSet(self.nfa.final_states)

    @property
    def labels(self):
        return GQLSet(self.nfa.symbols)

    @property
    def edges(self):
        raise NotImplementedException("GQLFA.edges")

    @property
    def vertices(self):
        return GQLSet(self.nfa.states)
