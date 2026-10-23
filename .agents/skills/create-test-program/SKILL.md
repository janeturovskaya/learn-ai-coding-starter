---
name: create-test-program
description: Given a SlopLang language feature, create a runnable example and an exact-output regression test
---

# Create a test program

Given a SlopLang language feature, work from the project root:

1. Read `docs/spec.md` for the feature's syntax, semantics, and expected output. Check existing programs in `examples/` so the new example does not duplicate one.
2. Write a focused, runnable `.slop` program in `examples/` that demonstrates the feature and prints a deterministic result. Follow the spec; do not change language behavior as part of this skill.
3. Add a pytest test in `tests/test_example_outputs.py` (create the file if needed). Read the new example as UTF-8, run it with `sloperator.runner.run_source`, and assert `exit_code == 0`, `stderr == ""`, and `stdout` equals the complete expected output, including spaces and trailing newlines. Set the expected output explicitly, not by computing it from the program's actual output.
4. Run `uv run ruff format` after code changes, then run `uv run pytest -q tests/test_example_outputs.py` from the project root. Report the example path, expected output, and test result.
