from project.utils import CFG_utils
from pyformlang.cfg import CFG, Production, Variable, Terminal, Epsilon

import pytest


def is_in_wncf(cfg_nf, cfg_old):
    for production in cfg_nf.productions:
        body = production.body
        if (
            not (
                (len(body) <= 2 and all(filter(lambda x: x in cfg_nf.variables, body)))
                or (len(body) == 1 and body[0] in cfg_nf.terminals)
                or (not body)
            )
            or cfg_nf.generate_epsilon() != cfg_old.generate_epsilon()
        ):
            return False
    return True


@pytest.fixture
def cfg_default():
    variables = {Variable("S"), Variable("B")}
    terminals = {Terminal("1"), Terminal("0")}
    start_symbol = Variable("S")
    productions = {
        Production(Variable("S"), [Terminal("1"), Terminal("0")]),
        Production(Variable("S"), [Terminal("1"), Variable("S"), Terminal("1")]),
        Production(Variable("S"), [Variable("B"), Terminal("1")]),
        Production(Variable("B"), [Terminal("1"), Terminal("1")]),
        Production(Variable("B"), [Variable("S"), Terminal("1")]),
    }
    return CFG(variables, terminals, start_symbol, productions)


@pytest.fixture
def cfg_epsilon():
    grammar = CFG.from_text(
        "S -> a S b S\n\
         S -> epsilon"
    )
    return grammar


@pytest.fixture
def default_normal_form():
    variables = {
        Variable("0#CNF#"),
        Variable("S"),
        Variable("C#CNF#1"),
        Variable("1#CNF#"),
        Variable("B"),
    }
    terminals = {Terminal("0"), Terminal("1")}
    productions = {
        Production(Variable("S"), [Variable("1#CNF#"), Variable("0#CNF#")]),
        Production(Variable("S"), [Variable("B"), Variable("1#CNF#")]),
        Production(Variable("S"), [Variable("1#CNF#"), Variable("C#CNF#1")]),
        Production(Variable("B"), [Variable("S"), Variable("1#CNF#")]),
        Production(Variable("B"), [Variable("1#CNF#"), Variable("1#CNF#")]),
        Production(Variable("0#CNF#"), [Terminal("0")]),
        Production(Variable("1#CNF#"), [Terminal("1")]),
        Production(Variable("C#CNF#1"), [Variable("S"), Variable("1#CNF#")]),
    }
    start_symbol = Variable("S")
    return CFG(variables, terminals, start_symbol, productions)


@pytest.mark.parametrize(
    "cfg_string,start_state",
    [
        (
            "S -> a S b S\n\
         S -> epsilon",
            "S",
        ),
        (
            "S -> A B\n\
         A -> a B c B\n\
         B -> d e f",
            "S",
        ),
        (
            "Expr -> Term | Expr AddOp Term | AddOp Term\n\
          Term -> Factor | Term MulOp Factor\n\
          Factor -> Primary | Factor pow Primary\n\
          Primary -> number | variable\n\
          AddOp -> add | sub\n\
          MulOp -> mul | div",
            "Expr",
        ),
        (
            "S -> A | epsilon\n\
          A -> a b | epsilon\n\
          B -> epsilon",
            "S",
        ),
        (
            "S -> A | a b\n\
          A -> B | epsilon\n\
          B -> C | c d",
            "S",
        ),
    ],
)
def test_is_wncf(cfg_string, start_state):
    cfg = CFG.from_text(cfg_string, start_state)
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(cfg)
    assert is_in_wncf(cfg_in_wncf, cfg)


def test_cfg_with_epsilon(cfg_epsilon, cfg_epsilon_from_text):
    normal_form = CFG_utils.transform_cfg_to_wcnf(cfg_epsilon_from_text)
    print("\nGrammar productions = ", cfg_epsilon_from_text.productions)
    print("NF productions = ", normal_form.productions)


def test_cfg_to_wncf_productions(cfg_default, default_normal_form):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(cfg_default)
    assert cfg_in_wncf.productions == default_normal_form.productions


def test_cfg_to_wncf_start_symbol(cfg_default, default_normal_form):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(cfg_default)
    assert cfg_in_wncf.start_symbol == default_normal_form.start_symbol


def test_cfg_from_file(cfg_default):
    filename = "tests/data/test_cfg.txt"
    cfg = CFG_utils.read_cfg_from_file(filename, "S")
    assert cfg.productions == cfg_default.productions


def test_corrupted_cfg():
    with pytest.raises(CFG_utils.CFGException):
        filename = "tests/data/test_cfg_corrupted.txt"
        CFG_utils.read_cfg_from_file(filename, "S")


def test_nonexistent_file():
    with pytest.raises(CFG_utils.CFGException):
        filename = "Whiteboards are remarkable"
        CFG_utils.read_cfg_from_file(filename, "S")
