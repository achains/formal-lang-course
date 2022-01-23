from project.utils.graph_utils import get_graph
from project.utils.graph_utils import GraphException

from project.min_gql.interpreter.exceptions import LoadGraphException

from project.min_gql.interpreter.gqltypes.GQLFA import GQLFA


def get_graph_by_name(name: str) -> GQLFA:
    try:
        graph = get_graph(name=name)
    except GraphException as exc:
        raise LoadGraphException(name=name) from exc

    return GQLFA.fromGraph(graph)
