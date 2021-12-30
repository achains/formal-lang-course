from project.min_gql.interpreter.gqltypes.GQLType import GQLType


class GQLSet(GQLType):
    def __init__(self, internal_type: type):
        self._internal_type = internal_type
        self._internal_set = set()

    @staticmethod
    def _type_consistency(set_obj: set, t: type):
        return all(map(lambda x: isinstance(x, t), set_obj))

    # TODO: Think of Empty Set
    @classmethod
    def fromSet(cls, pyset: set):
        pass

    def __len__(self):
        return len(self._internal_set)

    def intersect(self, other):
        pass

    def union(self, other):
        pass

    def dot(self, other):
        pass

    def inverse(self):
        pass

    def __str__(self):
        pass
