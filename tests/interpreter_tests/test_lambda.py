from interprert_token import interpret_token
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.min_gql.interpreter.gqltypes.GQLBool import GQLBool

import pytest


@pytest.mark.parametrize(
    "initial_set, fun, expected_set",
    [
        ("{1, 2}", "fun x: x in {2}", {GQLBool(True), GQLBool(False)}),
        ("{1, 2, 3}", "fun x: 5", {5})
    ],
)
def test_map(initial_set, fun, expected_set):
    expression = f"map({fun}, {initial_set})"
    actual = interpret_token(expression, "map_gql")
    assert actual.data == expected_set


@pytest.mark.parametrize(
    "initial_set, fun, expected_set",
    [
        ("{1, 2, 3, 4, 5}", "fun x: x in {2..4}", "{2, 3, 4}"),
    ],
)
def test_filter(initial_set, fun, expected_set):
    expression = f"filter({fun}, {initial_set})"
    actual = interpret_token(expression, "filter_gql")
    expected = interpret_token(expected_set, "vertices")
    assert actual.data == expected.data
