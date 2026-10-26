# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Run and validate

```bash
uv run sloperator.py examples/fib.slop
uv run sloperator.py --check path/to/program.slop
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

`--check` checks syntax without running the program. For the language, examples, and
error behavior, see the [SlopLang specification](docs/spec.md).

## Layout

- `sloperator.py`: command-line entrypoint
- `sloperator/lexer/`, `parser/`, `evaluator/`: interpreter stages
- `sloperator/runner.py`: runs source through the stages
- `examples/`: sample `.slop` programs
- `tests/`: pytest suite
- `playground/`: web server and editor

## Playground

```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.
