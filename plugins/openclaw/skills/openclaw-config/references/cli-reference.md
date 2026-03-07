# OpenClaw CLI Reference

## Config Management

```bash
openclaw onboard                           # Interactive setup wizard
openclaw onboard --install-daemon          # Setup + install service
openclaw configure                         # Re-run config wizard
openclaw configure --section web           # Configure specific section

openclaw config get <path>                 # Read config value (JSON output)
openclaw config set <path> <value>         # Set config value
openclaw config unset <path>               # Delete config key
```

**RPC config operations:**
```bash
openclaw gateway call config.apply --params '{"raw": "...", "baseHash": "<hash>"}'
openclaw gateway call config.patch --params '{"raw": "...", "baseHash": "<hash>"}'
```
Rate limited: 3 requests per 60 seconds per device+IP.

## Validation & Diagnostics

```bash
openclaw doctor                            # Validate config, show errors
openclaw doctor --fix                      # Auto-repair fixable issues
openclaw doctor --yes                      # Auto-repair without prompting
openclaw doctor --generate-gateway-token   # Generate token if missing

openclaw health                            # Detailed health check
openclaw status                            # Current status overview
openclaw logs                              # View logs (default: tail + follow)
openclaw logs --follow                     # Real-time log stream
openclaw logs --tail 50                    # Last N lines
```

## Gateway Control

```bash
openclaw gateway                           # Start gateway (foreground)
openclaw gateway --port 18789              # Start on specific port
openclaw gateway status                    # Service status
openclaw gateway status --deep             # Detailed status
openclaw gateway status --json             # JSON output
openclaw gateway restart                   # Restart service
openclaw gateway stop                      # Stop service
openclaw gateway install --force           # Reinstall service

openclaw daemon start                      # Start daemon
openclaw daemon stop                       # Stop daemon

openclaw dashboard                         # Open Control UI in browser
```

## Channel Management

```bash
openclaw channels status                   # Channel connectivity
openclaw channels status --probe           # Probe channel connections
openclaw channels login --channel <ch> --account <id>  # Auth a channel

openclaw pairing list <channel>            # List pending pairing requests
openclaw pairing list --channel <ch> --account <id>
openclaw pairing approve <channel> <CODE>  # Approve pairing request
```

## Agent & Session Management

```bash
openclaw agents list                       # List all agents
openclaw agents list --bindings            # List agents with routing bindings
openclaw agents add <name>                 # Create new agent
openclaw agent <id> info                   # Agent details

openclaw sessions list                     # List sessions
openclaw sessions preview <key>            # Preview session content
openclaw sessions clear                    # Clear all sessions
```

## Device Management

```bash
openclaw devices list                      # List paired devices
openclaw devices list --json               # JSON output
openclaw devices approve [requestId]       # Approve pending device
openclaw devices approve --latest          # Approve latest request
openclaw devices reject <requestId>        # Reject device
openclaw devices remove <deviceId>         # Remove paired device
openclaw devices clear --yes               # Clear all devices
openclaw devices rotate --device <id> --role <role>  # Rotate token
openclaw devices revoke --device <id> --role <role>  # Revoke access
```

## Model Management

```bash
openclaw models list                       # List available models
openclaw models show <model>               # Model details
```

## Automation

```bash
openclaw cron list                         # List cron jobs
openclaw cron status                       # Scheduler status
openclaw cron create <name>                # Create cron job
openclaw cron run <jobId>                  # Manually run job
openclaw cron runs --id <jobId> --limit 20 # Job run history
openclaw cron logs <jobId>                 # Job logs

openclaw hooks list                        # List webhook mappings
openclaw hooks test                        # Test webhook endpoint
```

## Security

```bash
openclaw security audit                    # Quick security check
openclaw security audit --deep             # Deep audit
openclaw security audit --fix              # Auto-fix findings
openclaw security audit --json             # JSON output
```

## Utilities

```bash
openclaw qr                                # Generate QR code
openclaw message send --channel <ch> --target <id> --message "text"
openclaw reset                             # Reset config to defaults
openclaw --version                         # Show version
```

## Node Management

```bash
openclaw nodes status                      # Node status
openclaw nodes describe --node <id>        # Node details
openclaw nodes pending                     # Pending node pairings
openclaw approvals get --node <id>         # Exec approvals for node
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENCLAW_HOME` | Override home directory |
| `OPENCLAW_STATE_DIR` | Override state directory |
| `OPENCLAW_CONFIG_PATH` | Override config file path |
| `OPENCLAW_LOG_LEVEL` | Override log level (debug, trace, etc.) |
| `OPENCLAW_LOAD_SHELL_ENV` | Enable login-shell env import |
