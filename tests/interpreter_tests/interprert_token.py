from project.min_gql.parser import parse
from project.min_gql.interpreter.CustomVisitor import CustomVisitor
from project.min_gql.interpreter.gqltypes.GQLType import GQLType


def interpret_token(text: str, token: str) -> GQLType:
    parser = parse(text)
    parser.removeErrorListeners()
    tree = getattr(parser, token)()
    visitor = CustomVisitor()
    value = visitor.visit(tree)
    return value
