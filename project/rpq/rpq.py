from networkx import MultiDiGraph
from typing import Set, Tuple

from project.utils.rsm_sparse import RSMMatrixSparse
from project.utils.automata_utils import transform_graph_to_nfa, transform_regex_to_dfa


def get_reachable(
    bmatrix: RSMMatrixSparse, query_bm: RSMMatrixSparse
) -> Set[Tuple[int, int]]:
    """

    Parameters
    ----------
    query_bm: RSMMatrixSparse
        Query boolean matrix
    bmatrix: RSMMatrixSparse
        Boolean matrix object
    Returns
    -------
        reachable: Set[Tuple[int, int]]
            All reachable nodes, according to start and final states
    """
    tc = bmatrix.get_transitive_closure()

    result = set()
    for state_from, state_to in zip(*tc.nonzero()):
        if state_from in bmatrix.start_states and state_to in bmatrix.final_states:
            result.add(
                (
                    state_from // len(query_bm.indexed_states),
                    state_to // len(query_bm.indexed_states),
                )
            )

    return result


def rpq(
    graph: MultiDiGraph, query: str, start_nodes: set = None, final_nodes: set = None
):
    """
    Computes Regular Path Querying from given graph language and regular expression language

    Parameters
    ----------
    graph: MultiDiGraph
       Labeled graph
    query: str
       Regular expression given as string
    start_nodes: set, default=None
       Start states in NFA
    final_nodes: set, default=None
       Final states in NFA

    Returns
    -------
    rpq: set
       Regular Path Querying
    """

    graph_bm = RSMMatrixSparse.from_nfa(
        transform_graph_to_nfa(graph, start_nodes, final_nodes)
    )
    query_bm = RSMMatrixSparse.from_nfa(transform_regex_to_dfa(query))

    intersection = graph_bm.intersect(query_bm)
    return get_reachable(bmatrix=intersection, query_bm=query_bm)
