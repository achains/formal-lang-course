from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.min_gql.interpreter.gqltypes.GQLFA import GQLFA
from project.min_gql.interpreter.exceptions import ConversionException

from project.utils.automata_utils import transform_regex_to_dfa, AutomataException


class GQLRegex(GQLType):
    def __init__(self, regex_str: str):
        self.regex_str = regex_str

    @classmethod
    def fromString(cls, regex_str: str):
        try:
            return GQLFA(nfa=transform_regex_to_dfa(regex_str))
        except AutomataException as exc:
            raise ConversionException from exc

    def inverse(self):
        nfa = GQLRegex.fromString(self.regex_str)
        return nfa.inverse()

    def intersect(self, other):
        lhs = GQLRegex.fromString(self.regex_str)
        if isinstance(other, GQLRegex):
            rhs = GQLRegex.fromString(other.regex_str)
            return lhs.intersect(rhs)
        elif isinstance(other, GQLFA):
            return lhs.intersect(other)
        else:
            raise ConversionException(lhs="GQLRegex", rhs=str(other))

    def kleene(self):
        return GQLRegex(regex_str=f"({self.regex_str})*")

    def dot(self, other):
        return GQLRegex(regex_str=f"({self.regex_str}.{other.regex_str})")

    def union(self, other):
        return GQLRegex(regex_str=f"({self.regex_str}|{other.regex_str})")

    def __str__(self):
        str_regex = self.regex_str
        while str_regex[0] == '(' and str_regex[-1] == ')':
            str_regex = str_regex[1:-1]
        return str_regex
