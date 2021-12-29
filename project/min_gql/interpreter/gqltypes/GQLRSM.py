from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata

from project.min_gql.interpreter.exceptions import NotImplementedException


class GQLRSM(GQLAutomata):
    def __init__(self):
        pass

    def intersect(self, other):
        raise NotImplementedException("Graph.intersect")

    def union(self, other):
        raise NotImplementedException("Graph.union")

    def dot(self, other):
        raise NotImplementedException("Graph.dot")

    def inverse(self):
        raise NotImplementedException("Graph.inverse")

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
