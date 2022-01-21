from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.utils.automata_utils import transform_graph_to_nfa, add_nfa_states, replace_nfa_states
from project.utils.automata_utils import transform_regex_to_dfa, AutomataException
from project.utils.rsm_sparse import RSMMatrixSparse


from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.min_gql.interpreter.exceptions import NotImplementedException, ConversionException


class GQLFA(GQLAutomata):
    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        self.nfa = nfa
        self.reachable = None

    @classmethod
    def fromGraph(cls, graph: MultiDiGraph):
        return cls(nfa=transform_graph_to_nfa(graph))

    @classmethod
    def fromString(cls, regex_str: str):
        try:
            return GQLFA(nfa=transform_regex_to_dfa(regex_str))
        except AutomataException as exc:
            raise ConversionException from exc

    def intersect(self, other):
        if not isinstance(other, GQLFA):
            raise ConversionException("GQLFA", str(type(other)))
        lhs = RSMMatrixSparse.from_nfa(self.nfa)
        rhs = RSMMatrixSparse.from_nfa(other.nfa)
        intersection = lhs.intersect(rhs).to_nfa()
        return GQLFA(intersection)

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

    def getReachable(self):
        raise NotImplementedException("Graph.Reachable")

    # TODO: start, final should be pretty-printed?

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
