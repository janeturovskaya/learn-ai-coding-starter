---
description: Review and commit project changes, then rebase on origin/main
---

From the project root:

1. Review `git status --short`, `git diff`, `git diff --cached`, and any untracked project files before staging. Do not include generated files, secrets, or unrelated changes.
2. Stage the reviewed project changes with `git add`, then inspect `git diff --cached` to confirm what will be committed. If there is nothing to commit, stop and report it.
3. Commit the staged changes using $ARGUMENTS as the exact commit message. If the message is empty, ask for one rather than inventing it.
4. Only after the commit succeeds, run `git pull --rebase origin main`. If it fails or conflicts, stop and report the issue without discarding changes.
