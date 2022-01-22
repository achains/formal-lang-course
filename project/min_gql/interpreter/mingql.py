from project.min_gql.interpreter.exceptions import RunTimeException
from project.min_gql.parser import parse
from project.min_gql.interpreter.CustomVisitor import CustomVisitor


__all__ = ["interpreter"]


def interpreter(program: str):
    """
    Interpreter function

    Parameters
    ----------
    program: str
        Program text

    Returns
    -------
    error_code: int
        0 - Success
    """
    parser = parse(text=program)
    tree = parser.prog()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise RunTimeException("Invalid syntax")

    visitor = CustomVisitor()
    visitor.visit(tree)

    return 0
