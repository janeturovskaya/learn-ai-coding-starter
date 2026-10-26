# Sloperator handoff

## Repository

- Personal fork: https://github.com/janeturovskaya/learn-ai-coding-starter
- `origin`: personal fork; `upstream`: https://github.com/bootdotdev/learn-ai-coding-starter
- Working branch: `main`.
- This checkpoint preserves the local interpreter, tests, examples, playground,
  and OpenCode workflows developed during the Boot.dev course.

## Project map

- `sloperator.py`: CLI; supports running programs and syntax-only `--check`.
- `sloperator/runner.py`: connects lexer, parser, and evaluator.
- `sloperator/lexer/`, `sloperator/parser/`, `sloperator/evaluator/`: language implementation.
- `docs/spec.md`: authoritative syntax and behavior reference.
- `tests/`, `examples/`: regression tests and runnable `.slop` programs.
- `playground/server.py`, `playground/index.html`: local web playground.
- `AGENTS.md`: repository instructions and validation requirements.

## Current state

The language includes mutable `slop` and immutable `loadbearing` bindings,
functions, conditionals, loops, arithmetic, comparisons, short-circuit logic,
unary negation and logical not, strings, and the variadic `hallucinate` built-in.
Regression coverage includes operator precedence, identifier digits, nested
calls, string addition, diagnostics, CLI behavior, and exact example output.

OpenCode configuration is in `opencode.jsonc`:

- Context7 MCP is configured; Notion MCP is disabled.
- Playwright MCP uses `bunx --bun @playwright/mcp@0.0.80 --isolated --browser chromium`.
- `.opencode/plugins/run-slop.ts` provides the `run_slop` tool.
- `.opencode/commands/playground.md` starts or locates the playground.
- `.opencode/package.json` and `bun.lock` preserve tooling dependencies.

The configured model/provider choices may need adjustment for another user's
available models. GitHub authentication is local to the machine, not stored in
this handoff or the OpenCode configuration.

## Run locally

Install Python/uv for the interpreter and Bun for the configured MCP command.
From the project root:

```bash
uv run sloperator.py examples/fib.slop
uv run sloperator.py --check examples/fib.slop
uv run playground/server.py
```

Open http://localhost:8080. Check for an existing server before starting a second
one. The playground appends JSON run results to `logs/runs.log`.

## Validation at this checkpoint

All checks passed before creating this handoff:

```bash
uv run pytest                    # 203 passed
uv run ruff format --check       # 44 files already formatted
uv run ruff check                # passed
uv run ty check                  # passed
```

After code changes, run `uv run ruff format` and repeat the checks above. Add a
regression test for bug fixes or behavior changes.

## Browser exercise and course progress

Playwright MCP opened the playground and ran:

```slop
hallucinate(“browser slop”, 42)✨
```

The output was `browser slop 42` followed by a newline. The corresponding local
log entry had empty stderr and exit code `0`. Boot.dev lesson **11.5 - Playwright
MCP** passed both checks using:

```bash
bootdev run -s e8cf46a0-3947-4c1a-a5ca-d3e8453724d4
```

Continue with the next lesson in the Boot.dev browser; no additional feature work
has been requested yet. Logs and `.playwright-mcp/` browser artifacts are ignored
and are not part of this checkpoint. `.DS_Store` is also ignored.
