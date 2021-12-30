from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.utils.automata_utils import transform_graph_to_nfa, add_nfa_states, replace_nfa_states
from project.utils.rsm_sparse import RSMMatrixSparse

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.min_gql.interpreter.exceptions import NotImplementedException


class GQLFA(GQLAutomata):
    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        self.nfa = nfa

    @classmethod
    def fromGraph(cls, graph: MultiDiGraph):
        return cls(nfa=transform_graph_to_nfa(graph))

    def intersect(self, other):
        return GQLFA(self.nfa.get_intersection(other))

    def union(self, other):
        return GQLFA(self.nfa.union(other).to_deterministic())

    def dot(self, other):
        lhs = self.nfa.to_regex()
        rhs = other.nfa.to_regex()
        return GQLFA(lhs.concatenate(rhs).to_epsilon_nfa().to_deterministic())

    def inverse(self):
        inv_nfa = self.nfa.copy()
        for state in inv_nfa.states:
            inv_nfa.add_final_state(state)
        for state in self.nfa.final_states:
            inv_nfa.remove_final_state(state)
        return GQLFA(nfa=inv_nfa)

    def __str__(self):
        return "Some graph"

    def setStart(self, start_states):
        self.nfa = replace_nfa_states(self.nfa, start_states=start_states)

    def setFinal(self, final_states):
        self.nfa = replace_nfa_states(self.nfa, final_states=final_states)

    def addStart(self, start_states):
        self.nfa = add_nfa_states(self.nfa, start_states=start_states)

    def addFinal(self, final_states):
        self.nfa = add_nfa_states(self.nfa, final_states=final_states)

    def getReachable(self):
        raise NotImplementedException("Graph.Reachable")

    @property
    def start(self):
        return self.nfa.start_states

    @property
    def final(self):
        return self.nfa.final_states

    @property
    def labels(self):
        return self.nfa.symbols

    @property
    def edges(self):
        raise self.nfa.states

    @property
    def vertices(self):
        return self.nfa.states
