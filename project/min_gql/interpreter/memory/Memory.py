from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.min_gql.interpreter.exceptions import VariableNotFoundException

from typing import List, Dict


class Memory:
    def __init__(self):
        self.tables: List[Dict[str:GQLType]] = [{}]

    def add(self, name: str, value: GQLType, level: int = -1):
        if level >= len(self.tables):
            for _ in range(level - len(self.tables) + 1):
                self.tables.append({})

        self.tables[level][name] = value

    def nextScope(self):
        new_table = Memory()
        new_table.tables = self.tables.copy()
        new_table.tables.append({})
        return new_table

    def removeLast(self):
        new_table = Memory()
        new_table.tables = self.tables.copy()
        new_table.tables = new_table.tables[:-1]
        return new_table

    def find(self, name: str):
        scope_level = len(self.tables) - 1
        while scope_level >= 0:
            value = self.tables[scope_level].get(name)
            if value is not None:
                return value
            scope_level -= 1
        raise VariableNotFoundException(name=name)
