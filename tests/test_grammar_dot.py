import sys

import pytest
import os

from pathlib import Path


if sys.platform.startswith("win"):
    pytest.skip("skipping", allow_module_level=True)
else:
    from project.parser import generate_dot

from antlr4.error.Errors import ParseCancellationException


def test_write_dot(tmpdir):
    text = """tmp = load_graph("sample");
g = set_start(set_final(tmp, get_vertices(tmp)), {1..100});
l1 = "l1" | "l2";
q1 = ("l3" | l1)*;
q2 = "l1" . "l5";
inter = g & q1;
start = get_start(g);
result = filter((fun v: v in start), map((fun ((u_g,u_q1),l,(v_g,v_q1)): u_g), get_edges(inter)));
"""
    path = generate_dot(text, Path("tests/data/test_grammar.dot"))
    assert path == Path("tests/data/test_grammar.dot")


def test_incorrect_text():
    text = """g = load graph "skos";
common_labels = (select lables from g) & (select labels from (load graph "graph.txt"));
print common_labels;"""
    with pytest.raises(ParseCancellationException):
        generate_dot(text, Path("test"))
