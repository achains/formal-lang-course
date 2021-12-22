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
        ("fun : 5", True),
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
        ("filter         ((fun : 5)   ,   p)", True),
    ],
)
def test_filter(text, accept):
    assert check_parser(text, "filter_gql") == accept
