from project.utils import automata_utils
from pyformlang.finite_automaton import Symbol


def test_is_deterministic():
    dfa = automata_utils.transform_regex_to_dfa("1*00*.1")

    assert dfa.is_deterministic()


def test_are_equal_regex_dfa():
    regex_str = "1* 0 0*"
    test_cases = [
        [Symbol("0")],
        [Symbol("1"), Symbol("1"), Symbol("1"), Symbol("0")],
        [Symbol("1"), Symbol("0"), Symbol("0")],
        [Symbol("0"), Symbol("0")],
    ]
    dfa = automata_utils.transform_regex_to_dfa(regex_str)

    assert all(dfa.accepts(word) for word in test_cases)
