from abc import ABC, abstractmethod

from project.min_gql.interpreter.gqltypes.GQLType import GQLType


class GQLAutomata(GQLType, ABC):
    """
    Base class for Automata (RSM, FA)
    """

    @abstractmethod
    def setStart(self, start_states):
        pass

    @abstractmethod
    def setFinal(self, final_states):
        pass

    @abstractmethod
    def addStart(self, start_states):
        pass

    @abstractmethod
    def addFinal(self, final_states):
        pass

    @abstractmethod
    def getReachable(self):
        pass

    @property
    @abstractmethod
    def start(self):
        pass

    @property
    @abstractmethod
    def final(self):
        pass

    @property
    @abstractmethod
    def labels(self):
        pass

    @property
    @abstractmethod
    def edges(self):
        pass

    @property
    @abstractmethod
    def vertices(self):
        pass
