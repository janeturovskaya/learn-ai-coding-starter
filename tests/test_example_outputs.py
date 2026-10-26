from pathlib import Path

from sloperator.runner import run_source


def test_equality_example_output():
    example = Path(__file__).resolve().parent.parent / "examples" / "equality.slop"
    result = run_source(example.read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "✅\n❌\n❌\n"


def test_short_circuit_example_output():
    example = Path(__file__).resolve().parent.parent / "examples" / "short-circuit.slop"
    result = run_source(example.read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "❌\n✅\n"
