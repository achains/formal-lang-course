from project.utils import rpq
from project.utils.graph_utils import generate_two_cycles_graph

import pytest


@pytest.fixture
def graph():
    return generate_two_cycles_graph("3", "2", "x", "y")


def test_full_rpq(graph):
    actual_rpq = rpq.rpq(graph, "x*|y")
    full_rpq = set((i, j) for i in range(4) for j in range(4))

    assert actual_rpq == full_rpq.union({(0, 4), (4, 5), (5, 0)})


@pytest.mark.parametrize(
    "regex_str,start_nodes,final_nodes,expected_rpq",
    [
        ("x*|y", {0}, {1, 2, 3, 4}, {(0, 1), (0, 2), (0, 3), (0, 4)}),
        ("x*|y", {4}, {4, 5}, {(4, 5)}),
        ("y", {0}, {0, 1, 2, 3}, set()),
        ("y*", {0}, {5, 4}, {(0, 5), (0, 4)}),
    ],
)
def test_rpq(graph, regex_str, start_nodes, final_nodes, expected_rpq):

    actual_rpq = rpq.rpq(graph, regex_str, start_nodes, final_nodes)
    assert actual_rpq == expected_rpq
