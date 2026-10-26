import pytest

from sloperator.runner import run_source


def test_variable_with_digit_matches_issue_reproduction():
    source = """slop score2 = 40✨
score2 = score2 + 2✨
hallucinate(score2)✨"""
    result = run_source(source)
    assert (result.stdout, result.stderr, result.exit_code) == ("42\n", "", 0)


def test_function_and_parameter_names_can_contain_digits():
    source = """clanker add2(value2) {
    ship value2 + 2✨
}
hallucinate(add2(40))✨"""
    result = run_source(source)
    assert (result.stdout, result.stderr, result.exit_code) == ("42\n", "", 0)


@pytest.mark.parametrize(
    "source",
    [
        "slop 2score = 40✨",
        "clanker 2add(value) { ship value✨ }",
        "clanker add(2value) { ship 2value✨ }",
    ],
)
def test_identifiers_cannot_start_with_digits(source: str):
    result = run_source(source)
    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr.startswith("SlopLang syntax error at line 1:")
