# Project agent instructions

## Git delivery

- Unless the user explicitly says not to publish, do not leave completed work
  only in the local working tree.
- Before committing, inspect `git status` and the complete diff. Never stage or
  publish `.env`, `data/`, credentials, secrets, logs, temporary files, or
  unrelated user changes.
- If the worktree contains unrelated changes, keep them out of the task commit.
  Use a dedicated branch/worktree or stage explicit paths instead of
  indiscriminately running `git add -A`.
- Create a branch named `codex/<short-task-name>` when starting publishable
  work. Reuse it only for the same task.
- For site changes, rebuild generated pages and exports, run the relevant smoke
  tests, and inspect the rendered result before committing.
- Commit the verified task changes with a concise message.
- Push the branch with `git push -u origin <branch>`.
- Create a pull request when tooling and authorization are available. If the
  GitHub CLI is unavailable, provide the direct GitHub compare URL for opening
  the pull request.
- In the final response, report the branch, commit SHA, push result, and pull
  request link or compare URL. Also include an exact copy-paste command for
  another clone to fetch and pull that pushed commit. Never claim a push or PR
  was created without a confirmed successful result.
