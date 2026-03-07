---
description: View OpenClaw gateway logs
argument-hint: [--lines N] [--level debug|info|warn|error]
allowed-tools: Bash, Read
---

# /oc-logs Command

View OpenClaw gateway logs with optional filtering.

## Arguments

The user provides: `$ARGUMENTS`

Parse these arguments:
- **--lines N** or **-n N**: Number of log lines to show (default: 50)
- **--level <level>**: Log level filter (debug, info, warn, error)
- **--follow** or **-f**: Follow logs in real-time (use with caution — will block)
- No arguments: Show last 50 lines

## Execution

Build the command based on arguments:

```bash
openclaw logs --tail ${lines:-50}
```

For debug-level output:
```bash
OPENCLAW_LOG_LEVEL=${level:-info} openclaw logs --tail ${lines:-50}
```

**Do NOT use `--follow` by default** — it blocks indefinitely. Only use if the user explicitly requests live/follow mode, and warn them it will block until interrupted.

## After Running

1. Parse the log output
2. Highlight any **errors** or **warnings** prominently
3. Look for common patterns:
   - `EADDRINUSE` — port conflict
   - `unauthorized` — auth mismatch
   - `pairing` — pending pairing requests
   - `mention required` — group mention policy
   - `refused to bind` — missing auth for non-loopback
4. Suggest next steps based on any errors found
5. If no errors, confirm the gateway appears healthy
