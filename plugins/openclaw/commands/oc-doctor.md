---
description: Run OpenClaw diagnostics and auto-fix config issues
argument-hint: [--fix]
allowed-tools: Bash, Read
---

# /oc-doctor Command

Run OpenClaw diagnostics to validate configuration and detect issues.

## Arguments

The user provides: `$ARGUMENTS`

Parse these arguments:
- **--fix**: Run `openclaw doctor --fix` to auto-repair fixable issues (interactive)
- **--yes**: Run `openclaw doctor --yes` to auto-repair without prompting
- No arguments: Run `openclaw doctor` in read-only mode

## Execution

```bash
openclaw doctor $ARGUMENTS
```

## After Running

1. Parse the output and present findings clearly
2. Group issues by severity (critical, warning, info)
3. For each issue, explain what it means and how to fix it
4. If `--fix` was not used and fixable issues were found, suggest running `/oc-doctor --fix`
5. If config validation failed, offer to help edit `~/.openclaw/openclaw.json`
