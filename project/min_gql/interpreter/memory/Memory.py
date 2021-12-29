from project.min_gql.interpreter.memory.Variable import Variable

from typing import List, Dict


class Memory:
    def __init__(self):
        self.tables: List[Dict[str: Variable]] = [{}]

    def add(self, variable: Variable, level: int = -1):
        if level >= len(self.tables):
            for _ in range(level - len(self.tables) + 1):
                self.tables.append({})

        self.tables[level][variable.name] = variable.value


