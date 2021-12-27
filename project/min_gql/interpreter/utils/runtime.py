from project.utils.graph_utils import get_graph
from project.utils.graph_utils import GraphException

from networkx import MultiDiGraph

# TODO: Wrap in abstract container


def get_graph_by_name(name: str) -> MultiDiGraph:
    try:
        graph = get_graph(name=name)
    except GraphException as exc:
        raise