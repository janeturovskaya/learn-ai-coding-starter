from sloperator.runner import run_source


def test_while_with_initially_false_condition_does_not_run():
    result = run_source("ralph ❌ {\n    hallucinate(“never”)✨\n}")

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == ""
