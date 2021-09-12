from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


def transform_regex_to_dfa(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Transform regular expression into DFA

    Parameters
    ----------
    regex_str: str
        Regular expression represented as string
        https://pyformlang.readthedocs.io/en/latest/usage.html#regular-expression

    Returns
    -------
    dfa: DeterministicFiniteAutomaton
        Minimal DFA built on given regular expression
    """

    regex = Regex(regex_str)
    enfa = regex.to_epsilon_nfa()

    return enfa.minimize()
