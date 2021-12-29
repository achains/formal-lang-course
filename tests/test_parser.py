import pytest
import platform

if platform.system() == "Windows":
    pytest.skip("skipping", allow_module_level=True)
else:
    from project.parser import parse


def check_parser(text, token: str) -> bool:
    parser = parse(text)
    parser.removeErrorListeners()
    getattr(parser, token)()
    return parser.getNumberOfSyntaxErrors() == 0


@pytest.mark.parametrize(
    "text, accept",
    [
        ("_123", True),
        ("123", False),
        ("graph", True),
        ("", False),
        ("GRAPH", True),
        ("__main__", True),
    ],
)
def test_var(text, accept):
    assert check_parser(text, "var") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("fun : 5", False),
        ("fun v: v in s", True),
        ("fun ((u_g,u_q2),l,(v_g,v_q1)) : u_g", True),
        ("fun {x, y, z} : 1", False),
        ("fun 1, 2, 3: 1", False),
        ("fun ((u_g,u_q2),l,(v_g,v_q1)), a, b : u_g & a", True),
    ],
)
def test_lambda(text, accept):
    assert check_parser(text, "lambda_gql") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("filter((fun x, y: x), a)", True),
        ("filter fun 1: 1 p", False),
        ("filter         ((fun : 5)   ,   p)", False),
        ("filter", False),
        ("filter(, x)", False),
        ("filter(fun x: x, )", False),
    ],
)
def test_filter(text, accept):
    assert check_parser(text, "filter_gql") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("true", True),
        ("false", True),
        ("True", False),
        ("False", False),
        ("{1..100}", True),
        ("(1..100)", False),
        ("{1, 2, 3}", True),
        ("{1, 2, 3)", False),
        ('(1, "l", 2)', True),
        ('("l", "k", "m")', False),
        ("{(1, 2), (3, 4), (5, 6)}", True),
        ("{(1, 2), ('l', 4), (5, 6)}", False),
        ('"label"', True),
        ("label", False),
        ('{"l1", "l2"}', True),
        ('{"l1", l2}', False),
        ("set_start(g, {1..100})", True),
        ("set_start(g, {1,,100})", False),
        ("set_final(g, {1..100})", True),
        ("add_start(g, {1, 2, 3})", True),
        ("add_final(g, labels1)", True),
        ("get_vertices(g)", True),
        ("get_start(g)", True),
        ("get(g)", False),
        ("get_labels(g)", True),
        ("get_start(1)", False),
        ("get_start()", False),
    ],
)
def test_val(text, accept):
    assert check_parser(text, "val") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("g1 & g2", True),
        ("g1", True),
        ("{2..100} & {1}", True),
        ("", False),
        ("(get_edges(g)) & {(1, 2)}", True),
        ("(& g) & {(1, 2)}", False),
        ("l1 . l2 . l3 | l4", True),
        ("(l1 & l2) | (l3 & l4)", True),
        ('"label1" . "label2" | "label3"', True),
        ("filter((fun (x, y): x in s), g)", True),
    ],
)
def test_expr(text, accept):
    assert check_parser(text, "expr") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        ("print g2", False),
        ("prnt g2", False),
        ("print {1..100}", False),
        ("print({1..100})", True),
        ("print", False),
        ('g1 = load_graph("wine")', True),
        ("g1 = load_graph", False),
        ("g1 = {1..100}", True),
    ],
)
def test_stmt(text, accept):
    assert check_parser(text, "stmt") == accept


@pytest.mark.parametrize(
    "text, accept",
    [
        (
            """
g = load_graph("wine");
new_g = set_start(g, {1..100});
g_labels = get_labels(new_g);
common_labels = g_labels & (load_graph("pizza"));

print(common_labels);
            """,
            True,
        ),
        (
            """
tmp = load_graph("sample");
g = set_start(set_final(tmp, get_vertices(tmp)), {1..100});
l1 = "l1" | "l2";
q1 = ("l3" | l1)*;
q2 = "l1" . "l5";
inter = g & q1;
start = get_start(g);
result = filter((fun v: v in start), map((fun ((u_g,u_q1),l,(v_g,v_q1)): u_g), get_edges(inter)));
            """,
            True,
        ),
        ("", False),
        ('g = load_graph("no_semicolon")', False),
    ],
)
def test_prog(text, accept):
    assert check_parser(text, "prog") == accept
