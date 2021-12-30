import sys

from antlr4 import InputStream, CommonTokenStream

from project.min_gql.grammar.MinGQLLexer import MinGQLLexer
from project.min_gql.grammar.MinGQLParser import MinGQLParser
from project.min_gql.interpreter.CustomVisitor import CustomVisitor


if __name__ == '__main__':
    input_stream = InputStream(''.join(sys.stdin.readlines()))
    # input_stream = InputStream(input())

    lexer = MinGQLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MinGQLParser(token_stream)
    tree = parser.prog()

    visitor = CustomVisitor()
    visitor.visit(tree)

