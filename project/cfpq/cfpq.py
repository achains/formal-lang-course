from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.grammars.hellings import hellings
from project.utils.CFG_utils import transform_cfg_to_wcnf

from scipy.sparse import dok_matrix

__all__ = ["cfpq_hellings", "cfpq_matrix"]


def cfpq_hellings(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start_var: Variable = Variable("S"),
) -> set:
    """
    Context-Free Path Querying based on Hellings Algorithm

    Parameters
    ----------
    graph: MultiDiGraph
        Labeled graph for the Path Querying task
    cfg: CFG
        Query given in Context Free Grammar form
    start_nodes: set, default=None
        Set of graph start nodes
    final_nodes: set, default=None
        Set of graph final nodes
    start_var: Variable, default=Variable("S")
        Start variable of a grammar

    Returns
    -------
    cfpq: set
        Context Free Path Querying
    """
    cfg._start_symbol = start_var
    wcnf = transform_cfg_to_wcnf(cfg)
    reach_pairs = {
        (u, v) for u, h, v in hellings(wcnf, graph) if h == wcnf.start_symbol.value
    }
    if start_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if u in start_nodes}
    if final_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if v in final_nodes}

    return reach_pairs


def cfpq_matrix(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start_var: Variable = Variable("S"),
) -> set:
    """
    Context-Free Path Querying based on Matrix Multiplication

    Parameters
    ----------
    graph: MultiDiGraph
        Labeled graph for the Path Querying task
    cfg: CFG
        Query given in Context Free Grammar form
    start_nodes: set, default=None
        Set of graph start nodes
    final_nodes: set, default=None
        Set of graph final nodes
    start_var: Variable, default=Variable("S")
        Start variable of a grammar

    Returns
    -------
    cfpq: set
        Context Free Path Querying
    """
    cfg._start_symbol = start_var
    wcnf = transform_cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}
    nodes_num = graph.number_of_nodes()
    matrices = {
        v.value: dok_matrix((nodes_num, nodes_num), dtype=bool) for v in wcnf.variables
    }

    for v_from, v_to, data in graph.edges(data=True):
        label = data["label"]
        for v in {p.head.value for p in term_productions if p.body[0].value == label}:
            matrices[v][v_from, v_to] = True

    for i in range(nodes_num):
        for v in eps_prod_heads:
            matrices[v][i, i] = True

    changed = True
    while changed:
        changed = False
        for p in var_productions:
            old_nnz = matrices[p.head.value].nnz
            matrices[p.head.value] += (
                matrices[p.body[0].value] @ matrices[p.body[1].value]
            )
            new_nnz = matrices[p.head.value].nnz
            changed = old_nnz != new_nnz

    reach_pairs = {(u, v) for u, v in zip(*matrices[wcnf.start_symbol.value].nonzero())}
    if start_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if u in start_nodes}
    if final_nodes:
        reach_pairs = {(u, v) for u, v in reach_pairs if v in final_nodes}

    return reach_pairs
