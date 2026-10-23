# Repository notes

## Project layout

- `sloperator.py` is the CLI entrypoint; `sloperator/runner.py` connects the lexer, parser, and evaluator in `sloperator/`.
- `tests/` contains the test suite, `examples/` contains SlopLang programs, and `playground/` contains the web editor and server.

## Validation

After any code changes, run `uv run ruff format` from the project root.

Run from the project root:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

## Regression tests

Add a regression test when fixing a bug or changing behavior. The test should cover the failing case and assert the expected result.

Run comparison tests from the project root with `uv run pytest -q tests/test_comparisons.py`.

## Language behavior

Use [docs/spec.md](docs/spec.md) as the reference for SlopLang syntax and behavior.
