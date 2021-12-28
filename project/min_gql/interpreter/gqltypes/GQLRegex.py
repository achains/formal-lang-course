from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.min_gql.interpreter.exceptions import NotImplementedException

from pyformlang.regular_expression import Regex
from project.utils.automata_utils import transform_regex_to_dfa


class GQLRegex(GQLType):
    def __init__(self, regex: Regex):
        self.regex = regex

    def intersect(self, other):
        raise NotImplementedException("Graph.intersect")

    def union(self, other):
        raise NotImplementedException("Graph.union")

    def dot(self, other):
        raise NotImplementedException("Graph.dot")

    def __str__(self):
        return "Some graph"
