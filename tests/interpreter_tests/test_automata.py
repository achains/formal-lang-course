from interprert_token import interpret_token
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.min_gql.interpreter.gqltypes.GQLFA import GQLFA

from project.utils.automata_utils import transform_regex_to_dfa

import pytest


@pytest.mark.parametrize(
    "lhs, op, rhs, expected",
    [
        ('"l1" & "l1"', "&", '"l1" | "l1"', '"l1"'),
        ('"l1" | "l2"', "|", '"l2" | "l3"', '"l1" | "l2" | "l3"'),
    ],
)
def test_FA_FA_intersection(lhs, op, rhs, expected):
    expression = lhs + ' ' + op + ' ' + rhs
    actual: GQLFA = interpret_token(expression, "expr")
    expected = transform_regex_to_dfa(expected)
    assert actual.nfa.is_equivalent_to(expected)
