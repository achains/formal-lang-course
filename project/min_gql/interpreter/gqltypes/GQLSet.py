from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.min_gql.interpreter.gqltypes.GQLBool import GQLBool

from project.min_gql.interpreter.exceptions import GQLTypeError, NotImplementedException


class GQLSet(GQLType):
    def __init__(self, internal_set: set):
        self._internal_type = GQLSet.get_type(internal_set)
        self._internal_set = internal_set

    @staticmethod
    def get_type(set_obj: set) -> type:
        if len(set_obj) == 0:
            return type(None)
        iseq = iter(set_obj)
        return type(next(iseq))

    @staticmethod
    def _type_consistency(set_obj: set):
        if len(set_obj) == 0:
            return True
        iseq = iter(set_obj)
        t = type(next(iseq))
        return all(map(lambda x: isinstance(x, t), iseq))

    # TODO: Allow empty sets
    @classmethod
    def fromSet(cls, pyset: set):
        if not GQLSet._type_consistency(pyset):
            raise GQLTypeError
        return GQLSet(pyset)

    @property
    def t(self):
        return self._internal_type

    @property
    def data(self):
        return self._internal_set

    def __len__(self):
        return len(self._internal_set)

    def find(self, value):
        return GQLBool(value in self._internal_set)

    def intersect(self, other):
        if self.t != other.t:
            raise GQLTypeError(f"Types mismatched: {self.t} != {other.t}")
        return GQLSet(internal_set=self.data & other.data)

    def union(self, other):
        if self.t != other.t:
            raise GQLTypeError(f"Types mismatched: {self.t} != {other.t}")
        return GQLSet(internal_set=self.data | other.data)

    def dot(self, other):
        raise NotImplementedException("Set dot")

    def kleene(self):
        raise NotImplementedException("Set kleene")

    def inverse(self):
        raise NotImplementedException("Set inverse")

    def __str__(self):
        return "{" + ', '.join(map(lambda x: str(x), self.data)) + "}"
