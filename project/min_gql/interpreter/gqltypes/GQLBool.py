from project.min_gql.interpreter.gqltypes.GQLType import GQLType

from project.min_gql.interpreter.exceptions import NotImplementedException


class GQLBool(GQLType):
    """
    GQL boolean class

    Attributes
    ----------
    b: bool
        Internal boolean value
    """

    def __init__(self, b: bool):
        self.b = b

    def intersect(self, other: "GQLBool") -> "GQLBool":
        """
        'AND'
        Parameters
        ----------
        other: GQLBool
            RHS boolean object
        Returns
        -------
        intersection: GQLBool
            Logical 'AND'
        """
        return GQLBool(self.b and other.b)

    def union(self, other: "GQLBool") -> "GQLBool":
        """
        'OR'
        Parameters
        ----------
        other: GQLBool
            RHS boolean object
        Returns
        -------
        intersection: GQLBool
            Logical 'OR'
        """
        return GQLBool(self.b or other.b)

    def dot(self, other: "GQLBool"):
        raise NotImplementedException("Bool doesn't support '.' operation")

    def kleene(self):
        raise NotImplementedException("Bool doesn't support '*' operation")

    def inverse(self) -> "GQLBool":
        """
        'NOT'
        Returns
        -------
        complement: GQLBool
            Logical 'NOT'
        """
        return GQLBool(not self.b)

    def __bool__(self):
        return self.b

    def __eq__(self, other: "GQLBool") -> bool:
        return self.b == other.b

    def __str__(self):
        return "true" if self.b else "false"

    def __hash__(self):
        return hash(self.b)
