from project.min_gql.grammar.MinGQLVisitor import MinGQLVisitor
from project.min_gql.grammar.MinGQLParser import MinGQLParser

from antlr4 import ParserRuleContext

import sys


# TODO: Returning bare values seems incorrect. Think about some abstract container.

class CustomVisitor(MinGQLVisitor):
    def __init__(self):
        self.memory = {}
        self.level = 0

    def visitProg(self, ctx: ParserRuleContext):
        return self.visitChildren(ctx)

    def visitExpr(self, ctx: ParserRuleContext):
        return self.visitChildren(ctx)

    def visitStmt(self, ctx: MinGQLParser.StmtContext):
        if ctx.PRINT():
            value = self.visit(ctx.expr())
            sys.stdout.write(str(value) + '\n')
        else:
            name = ctx.var().getText()
            value = self.visit(ctx.expr())
            self.memory[name] = value

    def visitString(self, ctx: MinGQLParser.StringContext):
        value = ctx.STRING().getText()
        return value

    def visitBoolean(self, ctx: MinGQLParser.BooleanContext):
        return ctx.TRUE() or False

    def visitVar(self, ctx: MinGQLParser.VarContext):
        name = ctx.IDENT().getText()
        if name in self.memory:
            return self.memory[name]
        raise KeyError("Wrong Variable Name")

    def visitVertex(self, ctx: MinGQLParser.VertexContext):
        return int(ctx.INT().getText())

    def visitRange_gql(self, ctx: MinGQLParser.Range_gqlContext):
        start = int(ctx.INT(0).getText())
        end = int(ctx.INT(1).getText())
        return set(range(start, end + 1))

    def visitVertices_set(self, ctx: MinGQLParser.Vertices_setContext):
        return set(map(lambda x: int(x.getText()), ctx.INT()))

    def visitLabel(self, ctx: MinGQLParser.LabelContext):
        return self.visit(ctx.string())

    def visitLabels_set(self, ctx: MinGQLParser.Labels_setContext):
        labels_set = set()
        for label in ctx.STRING():
            labels_set.add(label.getText())

        return labels_set

    def visitEdge(self, ctx: MinGQLParser.EdgeContext):
        # TODO: Create Edge Object
        vertex_from = self.visit(ctx.vertex(0))
        label = self.visit(ctx.label())
        vertex_to = self.visit(ctx.vertex(1))
        return vertex_from, label, vertex_to

    def visitEdges(self, ctx: MinGQLParser.EdgesContext):
        return self.visitChildren(ctx)

    def visitEdges_set(self, ctx: MinGQLParser.Edges_setContext):
        edges_set = set()
        for edge in ctx.edge():
            edges_set.add(self.visitEdge(edge))

        return edges_set

    def visitMap_gql(self, ctx: MinGQLParser.Map_gqlContext):
        fun = self.visit(ctx.lambda_gql())
        iterable = self.visit(ctx.expr())
        mapping_result = set()
        # TODO: Iterable should be Set object
        # TODO: Implement Lambda.apply
        for elem in iterable:
            mapping_result.add(fun.apply(elem))
        return mapping_result

    def visitLoad_graph(self, ctx: MinGQLParser.Load_graphContext):
        path = ctx.path().getText()


    def visitGraph_gql(self, ctx: MinGQLParser.Graph_gqlContext):
        if ctx.load_graph():
            return self.visit(ctx.load_graph())
