from project.min_gql.interpreter.mingql import read_script, interpreter
from project.min_gql.interpreter.exceptions import ScriptPathException, ScriptExtensionException

from pathlib import Path

import pytest


def test_invalid_file_path():
    with pytest.raises(ScriptPathException):
        read_script(filename=Path("blablabla").absolute())


def test_invalid_extension():
    with pytest.raises(ScriptExtensionException):
        read_script(filename=Path("tests/interpreter_tests/sample_scripts/invalid_extension.mgql"))


@pytest.mark.parametrize(
    "script_path",
    [
        "tests/interpreter_tests/sample_scripts/common_labels.gql",
        "tests/interpreter_tests/sample_scripts/common_labels_filter.gql",
        "tests/interpreter_tests/sample_scripts/regex_intersection.gql",
        "tests/interpreter_tests/sample_scripts/rpq.gql"
    ],
)
def test_correct_script(script_path):
    assert interpreter([Path(script_path)]) == 0
