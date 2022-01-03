from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLRegex import GQLFA, GQLRegex

from project.grammars.rsm import RSM
from project.utils.rsm_sparse import RSMMatrixSparse

from project.min_gql.interpreter.exceptions import NotImplementedException, ConversionException


class GQLRSM(GQLAutomata):
    def __init__(self, rsm: RSM):
        self.rsm = rsm

    def intersect(self, other):
        if isinstance(other, GQLFA) or isinstance(other, GQLRegex):
            raise ConversionException
        else:
            lhs = RSMMatrixSparse.from_rsm(self.rsm)
            rhs = RSMMatrixSparse.from_rsm(other.rsm)
            inter = lhs.intersect(rhs)

    def union(self, other):
        raise NotImplementedException("RSM.union")

    def dot(self, other):
        raise NotImplementedException("RSM.dot")

    def inverse(self):
        raise NotImplementedException("RSM.inverse")

    def kleene(self):
        raise NotImplementedException("RSM.kleene")

    def __str__(self):
        return "Some graph"

    def setStart(self, start_states):
        pass

    def setFinal(self, final_states):
        pass

    def addStart(self, start_states):
        pass

    def addFinal(self, final_states):
        pass

    @property
    def start(self):
        return

    @property
    def final(self):
        return

    @property
    def labels(self):
        return

    @property
    def edges(self):
        return

    @property
    def vertices(self):
        return

    def getReachable(self):
        return
