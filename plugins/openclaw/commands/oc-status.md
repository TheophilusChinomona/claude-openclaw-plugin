---
description: Quick OpenClaw health check - gateway, channels, and service status
argument-hint:
allowed-tools: Bash, Read
---

# /oc-status Command

Run a quick health check on the OpenClaw gateway and connected channels.

## Execution

Run these commands in sequence and present a consolidated summary:

1. **Gateway status:**
```bash
openclaw status
```

2. **Service status:**
```bash
openclaw gateway status
```

3. **Channel connectivity:**
```bash
openclaw channels status --probe
```

## Output

Present a clean summary with:
- Gateway status (running/stopped, port, bind address)
- Connected channels and their state
- Any warnings or errors

If the gateway is not running, suggest:
- `openclaw gateway restart` to restart the service
- `openclaw doctor` to diagnose config issues
- `openclaw logs --follow` to check for errors
