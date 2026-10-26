import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
INTERPRETER = ROOT / "sloperator.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INTERPRETER), *args],
        capture_output=True,
        encoding="utf-8",
        timeout=5,
    )


def test_runs_a_file():
    completed = run_cli(str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 0
    assert completed.stdout == "hello, slop\n"
    assert completed.stderr == ""


def test_error_goes_to_stderr_after_earlier_output(tmp_path: Path):
    program = tmp_path / "boom.slop"
    program.write_text("hallucinate(“before”)✨\nhallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == "before\n"
    assert completed.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
    assert "Traceback" not in completed.stderr


def test_division_by_zero_reports_runtime_error_without_traceback(tmp_path: Path):
    program = tmp_path / "division_by_zero.slop"
    program.write_text("hallucinate(1 / 0)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert completed.stderr == "SlopLang runtime error at line 1: division by zero\n"
    assert "Traceback" not in completed.stderr


def test_missing_file_and_usage():
    assert run_cli().returncode == 2
    missing = run_cli(str(ROOT / "nope.slop"))
    assert missing.returncode == 2
    assert "could not read" in missing.stderr


@pytest.mark.parametrize(
    "source",
    [
        "",
        "hallucinate(“must not print”)✨",
        "hallucinate(missing)✨",
        "hallucinate(1 / 0)✨",
        "ralph ✅ { }",
        "loadbearing LIMIT = 100✨\nLIMIT = 200✨",
    ],
)
def test_check_checks_syntax_without_executing(source: str, tmp_path: Path):
    program = tmp_path / "check.slop"
    program.write_text(source, encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


def test_check_flag_can_follow_file():
    completed = run_cli(str(ROOT / "examples/hello.slop"), "--check")
    assert completed.returncode == 0
    assert completed.stdout == ""
    assert completed.stderr == ""


@pytest.mark.parametrize(
    ("invalid_source", "diagnostic"),
    [
        ("@", "lexical error at line 2: unexpected character '@'"),
        (
            "slop x✨",
            "syntax error at line 2: expected '=' after variable name, "
            "an initializer is required, found '✨'",
        ),
    ],
)
def test_check_reports_errors_without_executing_earlier_statements(
    invalid_source: str, diagnostic: str, tmp_path: Path
):
    program = tmp_path / "invalid.slop"
    program.write_text(f"hallucinate(“must not print”)✨\n{invalid_source}", encoding="utf-8")
    completed = run_cli("--check", str(program))
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert completed.stderr == f"SlopLang {diagnostic}\n"


def test_check_missing_file_and_usage():
    assert run_cli("--check").returncode == 2
    missing = run_cli("--check", str(ROOT / "nope.slop"))
    assert missing.returncode == 2
    assert missing.stdout == ""
    assert "could not read" in missing.stderr


def test_unknown_flag_is_a_usage_error():
    completed = run_cli("--unknown", str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "unrecognized arguments" in completed.stderr
