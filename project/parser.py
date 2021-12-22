from antlr4.error.Errors import ParseCancellationException
from antlr4.tree.Tree import TerminalNodeImpl
from pydot import Dot, Node, Edge

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, ParserRuleContext

from project.min_gql.MinGQLLexer import MinGQLLexer
from project.min_gql.MinGQLParser import MinGQLParser
from project.min_gql.MinGQLListener import MinGQLListener

from pathlib import Path

__all__ = ["accept", "parse", "generate_dot"]


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


def generate_dot(text: str, path: Path):
    if not accept(text):
        raise ParseCancellationException("The word doesn't match the grammar")
    ast = parse(text).prog()
    tree = Dot("tree", graph_type="digraph")
    ParseTreeWalker().walk(DotTreeListener(tree, MinGQLParser.ruleNames), ast)
    tree.write(path)
    return path


class DotTreeListener(MinGQLListener):
    def __init__(self, tree: Dot, rules):
        self.tree = tree
        self.num_nodes = 0
        self.nodes = {}
        self.rules = rules
        super(DotTreeListener, self).__init__()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.tree.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.tree.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.tree.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.tree.add_node(Node(self.num_nodes, label=f"TERM: {node.getText()}"))
