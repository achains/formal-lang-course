from project.min_gql.grammar.MinGQLVisitor import MinGQLVisitor
from project.min_gql.grammar.MinGQLParser import MinGQLParser

from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.min_gql.interpreter.gqltypes.GQLGraph import GQLGraph

from project.min_gql.interpreter.utils.runtime import get_graph_by_name

from antlr4 import ParserRuleContext

import sys


# TODO: Returning bare values seems incorrect. Think about some abstract container.

class CustomVisitor(MinGQLVisitor):
    def __init__(self):
        self.memory = {}
        self.level = 0

    def visitProg(self, ctx: ParserRuleContext):
        return self.visitChildren(ctx)

    def visitExpr(self, ctx: ParserRuleContext) -> GQLType:
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

    def visitLambda_var(self, ctx: MinGQLParser.Lambda_varContext):
        pass

    def visitLambda_gql(self, ctx: MinGQLParser.Lambda_gqlContext):
        pass

    def visitMap_gql(self, ctx: MinGQLParser.Map_gqlContext):
        fun = self.visit(ctx.lambda_gql())
        iterable = self.visit(ctx.expr())
        mapping_result = set()
        # TODO: Iterable should be Set object
        # TODO: Implement Lambda.apply
        for elem in iterable:
            mapping_result.add(fun.apply(elem))
        return mapping_result

    def visitFilter_gql(self, ctx: MinGQLParser.Filter_gqlContext):
        pass

    def visitGraph_gql(self, ctx: MinGQLParser.Graph_gqlContext) -> GQLGraph:
        return self.visitChildren(ctx)

    def visitLoad_graph(self, ctx: MinGQLParser.Load_graphContext):
        name = ctx.string().getText().strip('"')
        return get_graph_by_name(name)

    def visitSet_final(self, ctx: MinGQLParser.Set_finalContext):
        graph = self.visit(ctx.var(0)) or self.visit(ctx.graph_gql())
        final_states = self.visit(ctx.var(1)) or self.visit(ctx.vertices())
        graph.setFinal(final_states)
        return graph

    def visitSet_start(self, ctx: MinGQLParser.Set_startContext):
        pass

    def visitAdd_start(self, ctx: MinGQLParser.Add_startContext):
        pass

    def visitAdd_final(self, ctx: MinGQLParser.Add_finalContext):
        pass

    def visitGet_edges(self, ctx: MinGQLParser.Get_edgesContext):
        pass

    def visitGet_labels(self, ctx: MinGQLParser.Get_labelsContext):
        pass

    def visitGet_start(self, ctx: MinGQLParser.Get_startContext):
        graph = self.visit(ctx.var()) or self.visit(ctx.graph_gql())
        return graph.start

    def visitGet_final(self, ctx: MinGQLParser.Get_finalContext):
        graph = self.visit(ctx.var()) or self.visit(ctx.graph_gql())
        return graph.final

    def visitGet_vertices(self, ctx: MinGQLParser.Get_verticesContext):
        pass

    def visitGet_reachable(self, ctx: MinGQLParser.Get_reachableContext):
        pass
