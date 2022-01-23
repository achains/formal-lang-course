from project.min_gql.interpreter.exceptions import (
    RunTimeException,
    ScriptPathException,
    ScriptExtensionException,
)
from project.min_gql.parser import parse
from project.min_gql.interpreter.CustomVisitor import CustomVisitor

from pathlib import Path

import sys


__all__ = ["interpreter"]


def interpreter(*argv):
    """
    MinGQL interpreter runner

    Parameters
    ----------
    argv:
        0 params - No Filename given, console mode. Write script right in console.
        1 params - Filename. Read script with .gql extension.
        Other Parameters: Ignored

    Returns
    -------
    code: int
        Interpreter exit code

    Raises
    ------
    RunTimeException
        One of the interpreter exceptions
    """
    if len(argv[0]) == 0:
        sys.stdout.write("No filename provided, console mode ON\n===========\n")
        program = "".join(sys.stdin.readlines())
    else:
        program = read_script(filename=Path(argv[0][0]))

    return __interpreter(program)


def read_script(filename: Path) -> str:
    """
    Read script with .gql extension

    Parameters
    ----------
    filename: str
        Name of the script *.gql

    Returns
    -------
    program: str
        Script text
    """
    try:
        script = filename.open()
    except FileNotFoundError as e:
        raise ScriptPathException(filename.name) from e

    if not filename.name.endswith(".gql"):
        raise ScriptExtensionException()

    return "".join(script.readlines())


def __interpreter(program: str):
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
