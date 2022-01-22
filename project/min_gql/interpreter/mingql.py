from project.min_gql.interpreter.exceptions import RunTimeException
from project.min_gql.parser import parse
from project.min_gql.interpreter.CustomVisitor import CustomVisitor


__all__ = ["interpreter"]


def interpreter(program: str):
    parser = parse(text=program)
    tree = parser.prog()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise RunTimeException("Invalid syntax")

    visitor = CustomVisitor()
    visitor.visit(tree)

    return 0
