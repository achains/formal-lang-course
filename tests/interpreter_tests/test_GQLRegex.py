# from interprert_token import interpret_token
# from project.min_gql.interpreter.gqltypes.GQLRegex import GQLRegex
# from project.min_gql.interpreter.exceptions import NotImplementedException
#
# from project.utils.automata_utils import transform_regex_to_dfa
#
# import pytest
#
#
# @pytest.fixture
# def regex_lhs():
#     return '"l1" | "l2" & "l5"'
#
#
# @pytest.fixture
# def regex_rhs():
#     return '"l3"* | "l4"*'
#
#
# def test_intersection(regex_lhs, regex_rhs):
#     regex_left = interpret_token(regex_lhs, "expr")
#     print(regex_left)
#     regex_right = interpret_token(regex_rhs, "expr")
#     # regex_left.intersect(regex_right)
#     assert True
