from scipy.sparse import dok_matrix, kron
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class BooleanMatrix:
    def __init__(self):
        self.indexed_states = {}
        self.start_states = set()
        self.final_states = set()
        self.bmatrix = dict()
        self.block_size = 1

    @classmethod
    def from_nfa(cls, nfa: NondeterministicFiniteAutomaton):
        obj = cls()
        obj.indexed_states = {state: idx for idx, state in enumerate(nfa.states)}
        obj.start_states, obj.final_states = nfa.start_states, nfa.final_states
        obj.bmatrix = obj._nfa_to_bmatrix(nfa)
        return obj

    def to_nfa(self):
        nfa = NondeterministicFiniteAutomaton()
        for label in self.bmatrix.keys():
            arr = self.bmatrix[label].toarray()
            for i in range(len(arr)):
                for j in range(len(arr)):
                    if arr[i][j]:
                        from_state = State((i // self.block_size, i % self.block_size))
                        to_state = State((j // self.block_size, j % self.block_size))
                        nfa.add_transition(
                            self.indexed_states[from_state],
                            label,
                            self.indexed_states[to_state],
                        )

        for start_state in self.start_states:
            nfa.add_start_state(self.indexed_states[State(start_state)])
        for final_state in self.final_states:
            nfa.add_final_state(self.indexed_states[State(final_state)])

        return nfa

    def transitive_closure(self):
        tc = sum(self.bmatrix.values())
        prev_nnz = tc.nnz
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            tc += tc @ tc
            prev_nnz, curr_nnz = curr_nnz, tc.nnz

        return tc

    def _nfa_to_bmatrix(self, nfa: NondeterministicFiniteAutomaton):
        """
        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton
            NFA to transform to matrix

        Returns
        -------
        bmatrix: dict
            Dict of boolean matrix for every automata label-key
        """
        bmatrix = dict()
        nfa_dict = nfa.to_dict()
        for label in nfa.symbols:
            tmp_matrix = dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
            for state_from in nfa_dict:
                if label in nfa_dict[state_from]:
                    for state_to in nfa_dict[state_from][label]:
                        tmp_matrix[
                            self.indexed_states[state_from], state_to.value
                        ] = True
            bmatrix[label] = tmp_matrix
        return bmatrix

    def intersect(self, other):
        intersection = BooleanMatrix()
        intersection.start_states = {
            (first, second)
            for first in self.start_states
            for second in other.start_states
        }
        intersection.final_states = {
            (first, second)
            for first in self.final_states
            for second in other.final_states
        }

        states = {
            (first, second)
            for first in self.indexed_states.keys()
            for second in other.indexed_states.keys()
        }
        intersection.indexed_states = {state: idx for idx, state in enumerate(states)}

        common_labels = self.bmatrix.keys() & other.bmatrix.keys()

        for label in common_labels:
            intersection.bmatrix[label] = kron(
                self.bmatrix[label], other.bmatrix[label]
            )

        intersection.block_size = len(other.indexed_states)

        return intersection
