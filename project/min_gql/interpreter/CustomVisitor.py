from project.min_gql.grammar.MinGQLVisitor import MinGQLVisitor
from project.min_gql.grammar.MinGQLParser import MinGQLParser

from project.min_gql.interpreter.gqltypes.GQLType import GQLType
from project.min_gql.interpreter.gqltypes.GQLAutomata import GQLAutomata
from project.min_gql.interpreter.gqltypes.GQLFA import GQLFA
from project.min_gql.interpreter.gqltypes.GQLBool import GQLBool
from project.min_gql.interpreter.gqltypes.GQLSet import GQLSet
from project.min_gql.interpreter.gqltypes.GQLCFG import GQLCFG

from project.min_gql.interpreter.memory.Memory import Memory

from project.min_gql.interpreter.utils.runtime import get_graph_by_name
from project.min_gql.interpreter.exceptions import NotImplementedException
from project.min_gql.interpreter.exceptions import GQLTypeError

from antlr4 import ParserRuleContext
from typing import Union
from collections import namedtuple

import sys


Fun = namedtuple("Fun", ["params", "body"])


class CustomVisitor(MinGQLVisitor):
    def __init__(self):
        self.memory = Memory()

    def visitProg(self, ctx: ParserRuleContext):
        return self.visitChildren(ctx)

    def visitExpr(self, ctx: MinGQLParser.ExprContext) -> GQLType:
        binary_op = {"AND": "intersect", "OR": "union", "DOT": "dot", "IN": "find"}
        unary_op = {"NOT": "inverse", "KLEENE": "kleene"}
        for b_op in binary_op:
            if getattr(ctx, b_op)():
                lhs = self.visit(ctx.expr(0))
                rhs = self.visit(ctx.expr(1))
                if b_op == "IN":
                    lhs, rhs = rhs, lhs
                return getattr(lhs, binary_op[b_op])(rhs)
        for u_op in unary_op:
            if getattr(ctx, u_op)():
                lhs = self.visit(ctx.expr(0))
                return getattr(lhs, unary_op[u_op])()

        return self.visitChildren(ctx)

    def visitStmt(self, ctx: MinGQLParser.StmtContext):
        if ctx.PRINT():
            value = self.visit(ctx.expr())
            sys.stdout.write(str(value) + '\n')
        else:
            name = ctx.var().getText()
            value = self.visit(ctx.expr())
            self.memory.add(name, value)

    def visitString(self, ctx: MinGQLParser.StringContext):
        value = ctx.STRING().getText()
        return value

    def visitBoolean(self, ctx: MinGQLParser.BooleanContext):
        return GQLBool(ctx.TRUE() is not None)

    def visitVar(self, ctx: MinGQLParser.VarContext):
        name = ctx.IDENT().getText()
        return self.memory.find(name)

    def visitVertex(self, ctx: MinGQLParser.VertexContext):
        return int(ctx.INT().getText())

    def visitRange_gql(self, ctx: MinGQLParser.Range_gqlContext):
        start = int(ctx.INT(0).getText())
        end = int(ctx.INT(1).getText())
        return GQLSet(set(range(start, end + 1)))

    def visitVertices_set(self, ctx: MinGQLParser.Vertices_setContext):
        return GQLSet(set(map(lambda x: int(x.getText()), ctx.INT())))

    def visitLabel(self, ctx: MinGQLParser.LabelContext):
        return GQLFA.fromString(self.visit(ctx.string()))

    def visitLabels_set(self, ctx: MinGQLParser.Labels_setContext):
        labels_set = set()
        for label in ctx.STRING():
            labels_set.add(label.getText())

        return GQLSet(labels_set)

    def visitEdge(self, ctx: MinGQLParser.EdgeContext):
        vertex_from = self.visit(ctx.vertex(0))
        label = self.visit(ctx.label())
        vertex_to = self.visit(ctx.vertex(1))
        return vertex_from, label, vertex_to

    def visitCfg(self, ctx: MinGQLParser.CfgContext) -> GQLCFG:
        cfg_text = ctx.CFG().getText().strip('"""')
        return GQLCFG.fromText(cfg_text)

    def visitEdges(self, ctx: MinGQLParser.EdgesContext):
        return self.visitChildren(ctx)

    def visitEdges_set(self, ctx: MinGQLParser.Edges_setContext):
        edges_set = set()
        for edge in ctx.edge():
            edges_set.add(self.visitEdge(edge))

        return GQLSet(edges_set)

    def visitVariables(self, ctx: MinGQLParser.VariablesContext):
        lambda_context = {}
        for v in ctx.lambda_var():
            lambda_context[self.visitLambda_var(v)] = None

        return lambda_context

    def visitVar_edge(self, ctx: MinGQLParser.Var_edgeContext):
        pass

    def visitLambda_var(self, ctx: MinGQLParser.Lambda_varContext):
        if ctx.var():
            return ctx.var().getText()
        elif ctx.var_edge():
            raise NotImplementedException("Lambda doesn't support varEdge for now")

    def visitLambda_gql(self, ctx: MinGQLParser.Lambda_gqlContext) -> Fun:
        params = self.visitVariables(ctx.variables())
        body = ctx.expr()

        return Fun(params=params, body=body)

    def _apply_lambda(self, fun: Fun, value: GQLType) -> GQLType:
        key = next(iter(fun.params))
        self.memory = self.memory.nextScope()
        self.memory.add(key, value)
        result = self.visit(fun.body)
        self.memory = self.memory.removeLast()
        return result

    def _iter_method(self, ctx: Union[MinGQLParser.Map_gqlContext, MinGQLParser.Filter_gqlContext], method="map"):
        fun = self.visit(ctx.lambda_gql())
        iterable = self.visit(ctx.expr())
        if not isinstance(iterable, GQLSet):
            raise GQLTypeError(msg=f"Can not apply map on {type(iterable)} object. Set expected.")
        if len(iterable) == 0:
            return iterable
        first_elem = next(iter(iterable.data))
        param_count = len(first_elem.data) if isinstance(first_elem, GQLSet) else 1
        if len(fun.params) != param_count:
            raise GQLTypeError(msg=f"Lambda argument count mismatched: Expected {len(fun.params)} Got {param_count}")
        # TODO: Expecting that iterable consists of elements for 1-param lambda
        # TODO: Expand this for multi-params
        # TODO: Order of elements will be changed, think of frozen set?
        new_iterable = set()
        for elem in iterable.data:
            result = self._apply_lambda(fun, elem)
            if method == "map":
                new_iterable.add(result)
            elif method == "filter":
                if result:
                    new_iterable.add(elem)
            else:
                raise NotImplementedError(f"CustomVisitor._iter_method wrong method {method}")

        return GQLSet(internal_set=new_iterable)

    def visitMap_gql(self, ctx: MinGQLParser.Map_gqlContext):
        return self._iter_method(ctx, method="map")

    def visitFilter_gql(self, ctx: MinGQLParser.Filter_gqlContext):
        return self._iter_method(ctx, method="filter")

    def visitGraph_gql(self, ctx: MinGQLParser.Graph_gqlContext) -> GQLAutomata:
        return self.visitChildren(ctx)

    def visitLoad_graph(self, ctx: MinGQLParser.Load_graphContext):
        name = ctx.string().getText().strip('"')
        return get_graph_by_name(name)

    def _modify_states(self, ctx: Union[MinGQLParser.Set_startContext, MinGQLParser.Add_startContext,
                                        MinGQLParser.Set_finalContext, MinGQLParser.Add_finalContext],
                       modify_method=None):
        graph = self.visit(ctx.var(0)) if ctx.var(0) else self.visit(ctx.graph_gql())
        states = self.visit(ctx.var(1)) if ctx.var(1) else self.visit(ctx.vertices())
        getattr(graph, modify_method)(states)

        return graph

    def visitSet_final(self, ctx: MinGQLParser.Set_finalContext):
        return self._modify_states(ctx, modify_method="setFinal")

    def visitSet_start(self, ctx: MinGQLParser.Set_startContext):
        return self._modify_states(ctx, modify_method="setStart")

    def visitAdd_start(self, ctx: MinGQLParser.Add_startContext):
        return self._modify_states(ctx, modify_method="addStart")

    def visitAdd_final(self, ctx: MinGQLParser.Add_finalContext):
        return self._modify_states(ctx, modify_method="addFinal")

    def _get_graph_info(self, ctx: Union[MinGQLParser.Get_edgesContext, MinGQLParser.Get_labelsContext,
                                         MinGQLParser.Get_startContext, MinGQLParser.Get_finalContext,
                                         MinGQLParser.Get_verticesContext, MinGQLParser.Get_reachableContext],
                        info_method=None):
        graph = self.visit(ctx.var()) if ctx.var() else self.visit(ctx.graph_gql())
        return getattr(graph, info_method)

    def visitGet_edges(self, ctx: MinGQLParser.Get_edgesContext):
        return self._get_graph_info(ctx, info_method="edges")

    def visitGet_labels(self, ctx: MinGQLParser.Get_labelsContext):
        return self._get_graph_info(ctx, info_method="labels")

    def visitGet_start(self, ctx: MinGQLParser.Get_startContext):
        return self._get_graph_info(ctx, info_method="start")

    def visitGet_final(self, ctx: MinGQLParser.Get_finalContext):
        return self._get_graph_info(ctx, info_method="final")

    def visitGet_vertices(self, ctx: MinGQLParser.Get_verticesContext):
        return self._get_graph_info(ctx, info_method="vertices")

    def visitGet_reachable(self, ctx: MinGQLParser.Get_reachableContext):
        graph = self.visit(ctx.var()) if ctx.var() else self.visit(ctx.graph_gql())
        return graph.getReachable()
