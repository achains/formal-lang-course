from interprert_token import interpret_token
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.min_gql.interpreter.exceptions import NotImplementedException, GQLTypeError

import pytest


@pytest.mark.parametrize(
    "lhs, op, rhs, expected",
    [
        ("{1, 2, 3, 4, 5}", "&", "{2, 3, 4}", {2, 3, 4}),
        ("{1, 2, 3}", "|", "{4, 5, 6}", {1, 2, 3, 4, 5, 6}),
        ("{1, 2, 3}", "&", "{}", set()),
        ("{}", "|", "{}", set()),
    ],
)
def test_binary(lhs, op, rhs, expected):
    expression = lhs + op + rhs
    actual_set = interpret_token(expression, "expr")
    expected_set = GQLSet(expected)
    assert actual_set.data == expected_set.data


@pytest.mark.parametrize(
    "lhs, op, rhs",
    [
        ("{1, 2}", ".", "{1, 2, 3}"),
        ("{1, 2, 3}", "*", ""),
        ("", "not", "{1, 2, 3}")
    ],
)
def test_unsupported_op(lhs, op, rhs):
    expression = lhs + op + rhs
    with pytest.raises(NotImplementedException):
        interpret_token(expression, "expr")


@pytest.mark.parametrize(
    "range_expr, expected",
    [
        ("{1..5}", {1, 2, 3, 4, 5}),
        ("{1..1}", {1}),
    ],
)
def test_unsupported_op(range_expr, expected):
    actual_set = interpret_token(range_expr, "range_gql")
    assert actual_set.data == GQLSet(expected).data


def test_mismatched_types():
    lhs = '{1, 2, 3}'
    rhs = '{"1", "2", "3"}'
    expression = lhs + "&" + rhs
    with pytest.raises(GQLTypeError):
        interpret_token(expression, "expr")
