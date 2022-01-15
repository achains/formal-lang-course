from project.min_gql.interpreter.gqltypes.GQLType import GQLType

from project.min_gql.interpreter.exceptions import NotImplementedException


class GQLBool(GQLType):
    def __init__(self, b: bool):
        self.b = b

    def intersect(self, other: 'GQLBool') -> 'GQLBool':
        return GQLBool(self.b and other.b)

    def union(self, other: 'GQLBool') -> 'GQLBool':
        return GQLBool(self.b or other.b)

    def dot(self, other: 'GQLBool'):
        raise NotImplementedException("Bool doesn't support '.' operation")

    def kleene(self):
        raise NotImplementedException("Bool doesn't support '*' operation")

    def inverse(self):
        return GQLBool(not self.b)

    def __bool__(self):
        return self.b

    def __eq__(self, other: 'GQLBool') -> bool:
        return self.b == other.b

    def __str__(self):
        return "true" if self.b else "false"
