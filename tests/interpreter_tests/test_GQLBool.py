from interprert_token import interpret_token
from project.min_gql.interpreter.gqltypes.GQLBool import GQLBool
from project.min_gql.interpreter.exceptions import NotImplementedException

import pytest


@pytest.mark.parametrize(
    "lhs, op, rhs, expected",
    [
        ("true", "&", "false", False),
        ("true", "|", "false", True),
        ("false", "|", "false", False),
    ],
)
def test_binary_or_and(lhs, op, rhs, expected):
    expression = lhs + op + rhs
    assert interpret_token(expression, "expr") == GQLBool(expected)


@pytest.mark.parametrize(
    "lhs, expected",
    [
        ("true", False),
        ("false", True),
    ],
)
def test_inversion(lhs, expected):
    expression = "not " + lhs
    assert interpret_token(expression, "expr") == GQLBool(expected)


@pytest.mark.parametrize(
    "lhs, op, rhs",
    [
        ("true", ".", "true"),
        ("true", "*", None),
    ],
)
def test_unsupported_op(lhs, op, rhs):
    expression = lhs + op + rhs if rhs else lhs + op
    with pytest.raises(NotImplementedException):
        interpret_token(expression, "expr")
