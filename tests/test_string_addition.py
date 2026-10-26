import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("“” + “slop”", "slop"),
        ("“slop” + “”", "slop"),
        ("“café” + “✨”", "café✨"),
    ],
)
def test_string_addition(expression: str, expected: str):
    result = run_source(f"hallucinate({expression})✨")

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == f"{expected}\n"
