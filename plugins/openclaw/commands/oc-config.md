---
description: View or edit OpenClaw configuration
argument-hint: <get|set|edit> [path] [value]
allowed-tools: Bash, Read, Write
---

# /oc-config Command

View or modify OpenClaw gateway configuration.

## Arguments

The user provides: `$ARGUMENTS`

Parse the subcommand:

### `get <path>`
Read a config value:
```bash
openclaw config get $path
```

### `set <path> <value>`
Set a config value. **Always confirm with the user before running:**
```bash
openclaw config set $path $value
```

After setting, inform the user whether a gateway restart is needed:
- Changes to `channels`, `agents`, `models`, `tools`, `hooks`, `cron`, `session` hot-apply (no restart)
- Changes to `gateway.*` (port, bind, auth) require restart (auto in hybrid mode)

### `edit`
Read and display the config file for editing:
```bash
cat ~/.openclaw/openclaw.json
```

Read the file, present its contents, and offer to make specific edits. After editing, the gateway will auto-reload if `gateway.reload.mode` is `"hybrid"` (default).

### No subcommand
If no arguments provided, show the full config:
```bash
openclaw config get .
```

## Important

- Config is at `~/.openclaw/openclaw.json` (JSON5 format)
- Always validate changes with `openclaw doctor` after significant edits
- Never expose secrets (tokens, passwords, API keys) in output — redact them
