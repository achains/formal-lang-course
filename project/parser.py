from antlr4 import InputStream, CommonTokenStream

from project.min_gql.MinGQLLexer import MinGQLLexer
from project.min_gql.MinGQLParser import MinGQLParser

__all__ = ["accept", "parse"]


def parse(text: str) -> MinGQLParser:
    input_stream = InputStream(text)
    lexer = MinGQLLexer(input_stream)
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    parser = MinGQLParser(stream)

    return parser


def accept(text: str) -> bool:
    parser = parse(text)
    parser.removeErrorListeners()
    parser.prog()

    return parser.getNumberOfSyntaxErrors() == 0
