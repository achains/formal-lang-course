from project.utils import CFG_utils
from pyformlang.cfg import CFG, Production, Variable, Terminal

import pytest


@pytest.fixture
def default_cfg():
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


def test_cfg_to_wncf_is_normal(default_cfg):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(default_cfg)
    assert cfg_in_wncf.is_normal_form()


def test_cfg_to_wncf_productions(default_cfg, default_normal_form):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(default_cfg)
    assert cfg_in_wncf.productions == default_normal_form.productions


def test_cfg_to_wncf_start_symbol(default_cfg, default_normal_form):
    cfg_in_wncf = CFG_utils.transform_cfg_to_wcnf(default_cfg)
    assert cfg_in_wncf.start_symbol == default_normal_form.start_symbol


def test_cfg_from_file(default_cfg):
    filename = "tests/data/test_cfg.txt"
    cfg = CFG_utils.read_cfg_from_file(filename, "S")
    assert cfg.productions == default_cfg.productions


def test_corrupted_cfg():
    with pytest.raises(CFG_utils.CFGException):
        filename = "tests/data/test_cfg_corrupted.txt"
        CFG_utils.read_cfg_from_file(filename, "S")


def test_nonexistent_file():
    with pytest.raises(CFG_utils.CFGException):
        filename = "Whiteboards are remarkable"
        CFG_utils.read_cfg_from_file(filename, "S")
