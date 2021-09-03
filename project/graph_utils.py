import cfpq_data
from collections import namedtuple
from typing import Tuple
import networkx

GraphInfo = namedtuple("GraphInfo", ["vertices", "edges", "labels"])


def get_graph_info(graph) -> GraphInfo:
    """Returns namedtuple consisted of number of vertices, edges and labels of given graph"""
    return GraphInfo(
        graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_labels(graph)
    )


def generate_and_save_two_cycle(
    num_first: int, num_second: int, edge_labels: Tuple[str, str], filename: str
):
    """Generates two cycle graph and saves it to <filename> in DOT format"""
    g = cfpq_data.labeled_two_cycles_graph(
        num_first, num_second, edge_labels=edge_labels, verbose=False
    )
    graph = networkx.drawing.nx_pydot.to_pydot(g)
    graph.write_raw(filename)
