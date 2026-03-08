---
description: Manage OpenClaw cron jobs — list, add, run, view history
argument-hint: <list|add|run|runs|remove|status> [jobId]
allowed-tools: Bash, Read
---

# /oc-cron Command

Manage cron job scheduling — list jobs, create new ones, trigger manual runs, and view history.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **subcommand** (required): `status`, `list`, `add`, `run`, `runs`, `remove`
- **jobId** (required for `run`, `runs`, `remove`): the cron job identifier

## Subcommands

### `status`

Show scheduler status:
```bash
openclaw cron status
```

Report: enabled/disabled, number of configured jobs, currently running jobs, and `maxConcurrentRuns` setting.

### `list`

List all configured cron jobs:
```bash
openclaw cron list
```

Format output as a table with columns: Job ID, Schedule, Agent, Status (enabled/disabled), Last Run.

### `add`

Guide the user through creating a new cron job:

1. Ask for a **job ID** (lowercase slug, e.g., `daily-briefing`)
2. Ask for a **schedule** in crontab syntax (e.g., `0 8 * * *` for daily at 8am)
3. Ask for the **agent ID** (default: `main`)
4. Ask for the **task** description (what the agent should do)
5. Ask if the result should be **delivered** to a chat session

Then run:
```bash
openclaw cron add
```

Or help them add via config if CLI is unavailable.

### `run <jobId>`

Manually trigger a cron job:
```bash
openclaw cron run <jobId>
```

Report the run status and any immediate output.

### `runs <jobId>`

View run history for a specific job:
```bash
openclaw cron runs <jobId>
```

Format output showing: Run ID, Start Time, Duration, Status (success/error), and truncated output.

### `remove <jobId>`

Remove a cron job (with confirmation):

1. Show the job details first
2. Ask the user to confirm removal
3. Run:
```bash
openclaw cron remove <jobId>
```

### No subcommand or unrecognized

Show usage help:
```
Usage: /oc-cron <subcommand> [args]

  status           Scheduler status
  list             List all cron jobs
  add              Create a new cron job (guided)
  run <jobId>      Manually trigger a job
  runs <jobId>     View run history
  remove <jobId>   Remove a job (with confirmation)
```

## After Running

- For `add`: suggest testing with `/oc-cron run <jobId>` before relying on the schedule
- For `remove`: confirm the job was removed
- For errors: suggest checking `openclaw cron status` and `openclaw doctor`
- Remind: cron is a control-plane tool — for untrusted agents, deny it: `tools: { deny: ["cron"] }`
