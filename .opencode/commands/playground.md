---
description: Start the local SlopLang web playground
---

Requested port: $ARGUMENTS

Use port 8080 if no port was provided. Verify that the port is a valid number before using it in a command.

Current TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Check whether a Sloperator playground server is already running before starting another one; inspect the listening process if needed. If it is, report its URL instead of starting a duplicate. If another process occupies the requested port, report the conflict. Otherwise, from the project root start `uv run playground/server.py <port>` in the background, substituting the chosen port, and confirm that it started. Report its URL or any startup error. Do not change project files.
