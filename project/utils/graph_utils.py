from collections import namedtuple
from typing import Tuple
from pathlib import Path
from networkx import MultiDiGraph

import cfpq_data
import networkx as nx

GraphInfo = namedtuple("GraphInfo", ["nodes", "edges", "labels"])


def get_graph_info(name: str) -> GraphInfo:
    """
    Show basic info of a graph with a given name

    Parameters
    ----------
    name : str
        Name of real-world graph from CFPQ_Data Dataset.

    Returns
    -------
    info : GraphInfo
        Namedtuple of (number of nodes, number of edges, set of edges' labels)
    """
    graph = cfpq_data.graph_from_dataset(name, verbose=False)
    return GraphInfo(
        graph.number_of_nodes(),
        graph.number_of_edges(),
        cfpq_data.get_labels(graph, verbose=False),
    )


def generate_two_cycles_graph(
    first_cycle_nodes_num: int,
    second_cycle_nodes_num: int,
    edge_labels: Tuple[str, str],
) -> MultiDiGraph:
    """
    Returns a graph with two cycles connected by one node.
    With labeled edges.

    Parameters
    ----------
    first_cycle_nodes_num : int
        Number of nodes in the first cycle
    second_cycle_nodes_num : int
        Number of nodes in the second cycle
    edge_labels : Tuple[str, str]
        Labels on the graph's edges

    Returns
    -------
    g : MultiDiGraph
        A graph with two cycles connected by one node.
    """
    return cfpq_data.labeled_two_cycles_graph(
        first_cycle_nodes_num,
        second_cycle_nodes_num,
        edge_labels=edge_labels,
        verbose=False,
    )


def save_to_dot(graph: MultiDiGraph, path_to_file: Path):
    """
    Saves graph to given path in DOT format

    Parameters
    ----------
    graph : MultiDiGraph
        Graph to save
    path_to_file : Path
        Path to file

    Returns
    -------
    p : Path
        Path to file
    """
    g = nx.drawing.nx_pydot.to_pydot(graph)
    g.write_raw(path_to_file)

    return Path(path_to_file).resolve()
