from project.utils.graph_utils import get_graph
from project.utils.graph_utils import GraphException

from networkx import MultiDiGraph

from project.min_gql.interpreter.exceptions import LoadGraphException

from project.min_gql.interpreter.gqltypes.GQLGraph import GQLGraph


def get_graph_by_name(name: str) -> GQLGraph:
    try:
        graph = get_graph(name=name)
    except GraphException as exc:
        raise LoadGraphException(name=name) from exc

    return GQLGraph.fromGraph(graph)
