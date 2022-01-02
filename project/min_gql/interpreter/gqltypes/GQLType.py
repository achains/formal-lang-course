from abc import ABC, abstractmethod


class GQLType(ABC):
    """
    Base Interface class for Interpreter types
    """
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def intersect(self, other):
        pass

    @abstractmethod
    def union(self, other):
        pass

    @abstractmethod
    def dot(self, other):
        pass

    @abstractmethod
    def inverse(self):
        pass

    @abstractmethod
    def kleene(self):
        pass
