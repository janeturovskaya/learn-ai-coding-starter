import pytest

from sloperator.runner import run_source


def test_not_flips_booleans_and_can_be_repeated():
    result = run_source("hallucinate(!✅, !❌, !!✅)✨")

    assert (result.stdout, result.stderr, result.exit_code) == ("❌ ✅ ✅\n", "", 0)


def test_not_binds_tighter_than_equality_and_logical_operators():
    result = run_source("hallucinate(!✅ == ❌, !❌ && ✅, !(✅ == ❌))✨")

    assert (result.stdout, result.stderr, result.exit_code) == ("✅ ✅ ✅\n", "", 0)


@pytest.mark.parametrize(
    ("value", "type_name"),
    [("0", "number"), ("1", "number"), ("“text”", "string")],
)
def test_not_rejects_non_booleans(value: str, type_name: str):
    result = run_source(f"hallucinate(!{value})✨")

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        f"SlopLang runtime error at line 1: operand of unary '!' "
        f"must be a boolean, got {type_name}\n"
    )
