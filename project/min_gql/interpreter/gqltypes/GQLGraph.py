from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.utils.automata_utils import transform_graph_to_nfa, add_nfa_states, replace_nfa_states

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.min_gql.interpreter.exceptions import NotImplementedException


class GQLGraph(GQLType):
    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        self.nfa = nfa

    @classmethod
    def fromGraph(cls, graph: MultiDiGraph):
        return cls(nfa=transform_graph_to_nfa(graph))

    def intersect(self, other):
        raise NotImplementedException("Graph.intersect")

    def union(self, other):
        raise NotImplementedException("Graph.union")

    def dot(self, other):
        raise NotImplementedException("Graph.dot")

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
        raise NotImplementedException("Graph.edges")
