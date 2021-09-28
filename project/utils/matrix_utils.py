from scipy.sparse import dok_matrix, kron
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


class BooleanMatrix:
    """
    Representation of NFA as a Boolean Matrix

    Attributes
    ----------
    indexed_states: dict
        Renumbered (from 0) states of NFA
    start_states: set
        Start states of NFA
    final_states: set
        Final states of NFA
    bmatrix: dict
        Dictionary of boolean matrices.
        Keys are NFA labels
    block_size: int
        Size of a block in boolean matrix
    """

    def __init__(self):
        self.indexed_states = {}
        self.start_states = set()
        self.final_states = set()
        self.bmatrix = dict()
        self.block_size = 1

    @classmethod
    def from_nfa(cls, nfa: NondeterministicFiniteAutomaton):
        """
        Transforms NFA into BooleanMatrix

        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton
            NFA to transform
        Returns
        -------
        obj: BooleanMatrix
            BooleanMatrix object from NFA
        """
        obj = cls()
        obj.indexed_states = {state: idx for idx, state in enumerate(nfa.states)}
        obj.start_states, obj.final_states = nfa.start_states, nfa.final_states
        obj.bmatrix = obj._nfa_to_bmatrix(nfa)
        return obj

    def to_nfa(self):
        """
        Transforms BooleanMatrix into NFA

        Returns
        -------
        nfa: NondeterministicFiniteAutomaton
            Representation of BooleanMatrix as NFA
        """
        nfa = NondeterministicFiniteAutomaton()
        for label in self.bmatrix.keys():
            arr = self.bmatrix[label].toarray()
            for i in range(len(arr)):
                for j in range(len(arr)):
                    if arr[i][j]:
                        from_state = (
                            State((i // self.block_size, i % self.block_size))
                            if self.block_size > 1
                            else State(i)
                        )
                        to_state = (
                            State((j // self.block_size, j % self.block_size))
                            if self.block_size > 1
                            else State(j)
                        )
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
        """
        Computes transitive closure of boolean matrices

        Returns
        -------
        tc: dok_matrix
            Transitive closure of boolean matrices
        """
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
            for state_from, transitions in nfa_dict.items():
                if label in transitions:
                    states_to = (
                        transitions[label]
                        if isinstance(transitions[label], set)
                        else {transitions[label]}
                    )
                    for state_to in states_to:
                        tmp_matrix[
                            self.indexed_states[state_from],
                            self.indexed_states[state_to],
                        ] = True
            bmatrix[label] = tmp_matrix
        return bmatrix

    def intersect(self, other):
        """
        Computes intersection of self boolean matrix with other

        Parameters
        ----------
        other: BooleanMatrix
            Right-hand side boolean matrix
        Returns
        -------
        intersection: BooleanMatrix
            Intersection of two boolean matrices
        """
        intersection = BooleanMatrix()
        common_labels = self.bmatrix.keys() & other.bmatrix.keys()

        for label in common_labels:
            intersection.bmatrix[label] = kron(
                self.bmatrix[label], other.bmatrix[label], format="dok"
            )

        for s_fst, s_fst_idx in self.indexed_states.items():
            for s_snd, s_snd_idx in other.indexed_states.items():
                new_state = new_state_idx = (
                    s_fst_idx * len(other.indexed_states) + s_snd_idx
                )
                intersection.indexed_states[new_state] = new_state_idx

                if s_fst in self.start_states and s_snd in other.start_states:
                    intersection.start_states.add(new_state)

                if s_fst in self.final_states and s_snd in other.final_states:
                    intersection.final_states.add(new_state)

        return intersection
