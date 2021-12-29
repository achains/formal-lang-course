from project.min_gql.interpreter.gqltypes import GQLType


class Variable:
    def __init__(self, name: str, value: GQLType):
        self.name = name
        self.value = value

    def __str__(self):
        return f"'{self.name}' = {self.value}"
