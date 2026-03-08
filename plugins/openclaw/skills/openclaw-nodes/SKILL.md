---
name: openclaw-nodes
description: >
  Use when the user wants to pair a device, manage companion nodes, set up
  remote execution, configure exec routing, control browser via node, set up
  headless node, connect iOS/Android/macOS devices, manage exec approvals,
  or run commands on remote nodes in OpenClaw.
---

# OpenClaw Nodes

Guide the user through node pairing, remote execution, device commands, and exec routing.

## Node Concept

A **node** is a companion device (macOS/iOS/Android/headless) that connects to the Gateway WebSocket with `role: "node"` and exposes commands (canvas, camera, device, notifications, system, location).

Key points:
- Nodes are **peripherals**, not gateways — they don't run the gateway service
- Messages land on the **gateway**, not on nodes
- Nodes connect via WebSocket (same port as operators)
- macOS can run in **node mode** via the menubar app

## Pairing Devices

### CLI Commands

```bash
openclaw devices list                        # List pending/approved devices
openclaw devices approve <requestId>         # Approve a device
openclaw devices reject <requestId>          # Reject a device
openclaw nodes status                        # Show connected nodes
openclaw nodes describe --node <idOrNameOrIp>  # Node details + permissions
```

### Telegram /pair Flow

1. User sends `/pair` in Telegram
2. Bot shows a pairing code
3. Approve on gateway: `openclaw devices approve <requestId>`

### Naming Nodes

- Set name on start: `openclaw node run --display-name "Build Node"`
- Rename from gateway: `openclaw nodes rename --node <id> --name "Build Node"`
- Name persists in `~/.openclaw/node.json` on the node

## Node Status

```bash
openclaw nodes status     # List all nodes with connection state
openclaw nodes describe --node <idOrNameOrIp>  # Detailed node info
```

`describe` shows: platform, device family, capabilities, permissions map, connection state.

## Exec Routing

### Configuration

`tools.exec.host` controls where exec commands run:

| Host | Behavior |
|------|----------|
| `sandbox` | Run in Docker sandbox (if enabled) |
| `gateway` | Run on gateway host |
| `node` | Run on a paired node |

```bash
openclaw config set tools.exec.host node
openclaw config set tools.exec.security allowlist
openclaw config set tools.exec.node "<id-or-name>"
```

### Per-Agent Override

```json5
{
  agents: {
    list: [
      {
        id: "remote",
        tools: { exec: { host: "node", node: "build-mac" } },
      },
    ],
  },
}
```

### Per-Session Override

```
/exec host=node security=allowlist node=<id-or-name>
```

## Node Commands

### Canvas (WebView)

```bash
openclaw nodes canvas present --node <id> --target https://example.com
openclaw nodes canvas hide --node <id>
openclaw nodes canvas navigate https://example.com --node <id>
openclaw nodes canvas eval --node <id> --js "document.title"
openclaw nodes canvas snapshot --node <id> --format png
openclaw nodes canvas a2ui push --node <id> --text "Hello"
openclaw nodes canvas a2ui reset --node <id>
```

### Camera

```bash
openclaw nodes camera list --node <id>
openclaw nodes camera snap --node <id>                 # both facings
openclaw nodes camera snap --node <id> --facing front
openclaw nodes camera clip --node <id> --duration 10s
```

### Screen Recording

```bash
openclaw nodes screen record --node <id> --duration 10s --fps 10
```

### Location

```bash
openclaw nodes location get --node <id>
openclaw nodes location get --node <id> --accuracy precise
```

Location is off by default and requires system permission.

### Notifications

```bash
openclaw nodes notify --node <id> --title "Ping" --body "Gateway ready"
# Supports --priority <passive|active|timeSensitive>
# Supports --delivery <system|overlay|auto>
```

### System Commands

```bash
openclaw nodes run --node <id> -- echo "Hello"
# Supports --cwd, --env KEY=VAL, --command-timeout
```

### Android-Specific

- `device.status`, `device.info`, `device.permissions`, `device.health`
- `notifications.list`, `notifications.actions`
- `photos.latest`, `contacts.search`, `contacts.add`
- `calendar.events`, `calendar.add`
- `sms.send` (requires SMS permission)

## Exec Approvals

Exec approvals are enforced **per node host** at `~/.openclaw/exec-approvals.json`.

```bash
# Add to allowlist
openclaw approvals allowlist add --node <id> "/usr/bin/uname"
openclaw approvals allowlist add --node <id> "/usr/bin/sw_vers"
```

Security modes:
- `deny` — block all exec
- `allowlist` — only pre-approved commands
- `full` — allow all (dangerous)

Shell wrappers (`bash -c`, etc.) require separate approval. Dangerous env keys are stripped (`DYLD_*`, `LD_*`, `NODE_OPTIONS`, etc.).

## Remote Node Host

### Start (Foreground)

```bash
openclaw node run --host <gateway-host> --port 18789 --display-name "Build Node"
```

### Start (Service)

```bash
openclaw node install --host <gateway-host> --port 18789 --display-name "Build Node"
openclaw node restart
```

### SSH Tunnel (Loopback Gateway)

If gateway binds to loopback:
```bash
# Terminal A: forward local port to gateway
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Terminal B: connect node through tunnel
export OPENCLAW_GATEWAY_TOKEN="<token>"
openclaw node run --host 127.0.0.1 --port 18790 --display-name "Build Node"
```

### Headless Mode (Cross-Platform)

```bash
openclaw node run --host <gateway-host> --port 18789
```

Exposes `system.run` / `system.which` only. Useful on Linux/Windows.

## Browser Control via Node

The gateway can proxy browser commands to a node. Same tailnet recommended for latency.

```json5
{
  // Browser tool with node target
  tools: {
    exec: { host: "node", node: "office-mac" },
  },
}
```

See `references/node-commands.md` for the full command reference and platform matrix.
