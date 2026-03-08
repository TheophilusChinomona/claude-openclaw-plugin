# Node Commands Reference

## Command Categories

### Canvas Commands

| Command | Description | Platforms |
|---------|-------------|-----------|
| `canvas.present` | Show WebView with URL/file | macOS, iOS |
| `canvas.hide` | Hide WebView | macOS, iOS |
| `canvas.navigate` | Navigate to URL | macOS, iOS |
| `canvas.eval` | Execute JavaScript | macOS, iOS |
| `canvas.snapshot` | Capture screenshot (returns image) | macOS, iOS |
| `canvas.a2ui_push` | Push A2UI content (v0.8 JSONL) | macOS, iOS |
| `canvas.a2ui_reset` | Reset A2UI state | macOS, iOS |

Notes:
- `canvas.present` accepts `--target` (URL or file), `--x`, `--y`, `--width`, `--height`
- `canvas.snapshot` supports `--format` (png/jpg), `--max-width`, `--quality`
- A2UI is v0.8 only (v0.9 `createSurface` is rejected)

### Camera Commands

| Command | Description | Platforms |
|---------|-------------|-----------|
| `camera.list` | List available cameras | macOS, iOS, Android |
| `camera.snap` | Take photo (returns image) | macOS, iOS, Android |
| `camera.clip` | Record video clip (returns mp4) | iOS, Android |

Notes:
- Node must be **foregrounded** for camera commands
- `camera.snap` defaults to both facings (2 images)
- `camera.clip` clamped to ≤60s
- Android prompts for CAMERA/RECORD_AUDIO permissions

### Screen Commands

| Command | Description | Platforms |
|---------|-------------|-----------|
| `screen.record` | Record screen (returns mp4) | macOS, iOS, Android |

Notes:
- Node must be foregrounded
- Duration clamped to ≤60s
- `--no-audio` disables microphone capture
- `--screen <index>` for multi-display
- Android shows system capture prompt

### Device Commands (Android)

| Command | Description |
|---------|-------------|
| `device.status` | Battery, connectivity, storage |
| `device.info` | Device model, OS, capabilities |
| `device.permissions` | Permission state map |
| `device.health` | System health metrics |

### Notification Commands

| Command | Description | Platforms |
|---------|-------------|-----------|
| `notifications.list` | List recent notifications | Android |
| `notifications.actions` | Interact with notification actions | Android |
| `system.notify` | Send notification | macOS |

`system.notify` supports:
- `--title`, `--body`
- `--priority` (`passive`, `active`, `timeSensitive`)
- `--delivery` (`system`, `overlay`, `auto`)

### Location Commands

| Command | Description | Platforms |
|---------|-------------|-----------|
| `location.get` | Get current location | macOS, iOS, Android |

Options: `--accuracy` (precise/coarse), `--max-age`, `--location-timeout`

Returns: lat/lon, accuracy (meters), timestamp. Location is **off by default**.

### System Commands

| Command | Description | Platforms |
|---------|-------------|-----------|
| `system.run` | Execute command | macOS, headless |
| `system.which` | Check command availability | headless |
| `system.notify` | Send notification | macOS |
| `system.execApprovals.get` | Get approval config | macOS, headless |
| `system.execApprovals.set` | Set approval config | macOS, headless |

`system.run` parameters:
- `command` — argv array
- `cwd` — working directory
- `env` — `KEY=VAL` entries
- `commandTimeoutMs` — command timeout
- `invokeTimeoutMs` — invoke timeout
- `needsScreenRecording` — request screen recording permission

### SMS Commands (Android)

| Command | Description |
|---------|-------------|
| `sms.send` | Send SMS message |

Requires SMS permission and telephony support.

### Personal Data Commands (Android)

| Command | Description |
|---------|-------------|
| `photos.latest` | Get recent photos |
| `contacts.search` | Search contacts |
| `contacts.add` | Add contact |
| `calendar.events` | List calendar events |
| `calendar.add` | Add calendar event |
| `motion.activity` | Activity recognition |
| `motion.pedometer` | Step counter |

## Platform Support Matrix

| Feature | macOS App | macOS Headless | iOS | Android |
|---------|-----------|---------------|-----|---------|
| Canvas | Yes | No | Yes | No |
| Camera | Yes | No | Yes | Yes |
| Screen record | Yes | No | Yes | Yes |
| Location | Yes | No | Yes | Yes |
| Notifications | Yes (send) | No | No | Yes (read) |
| System.run | Yes | Yes | No | No |
| System.which | No | Yes | No | No |
| SMS | No | No | No | Yes |
| Device info | No | No | No | Yes |
| Contacts | No | No | No | Yes |
| Calendar | No | No | No | Yes |

## Exec Approval File Format

`~/.openclaw/exec-approvals.json` on the node host:

```json
{
  "mode": "allowlist",
  "allowlist": [
    "/usr/bin/uname",
    "/usr/bin/sw_vers",
    "/usr/bin/whoami",
    "/usr/local/bin/node"
  ]
}
```

Modes: `deny`, `allowlist`, `full`

## SSH Tunnel Patterns

### Local Forwarding (Gateway Loopback)

```bash
# From node machine, forward to gateway
ssh -N -L 18790:127.0.0.1:18789 user@gateway-host

# Connect node via tunnel
export OPENCLAW_GATEWAY_TOKEN="<token>"
openclaw node run --host 127.0.0.1 --port 18790
```

### Tailscale Alternative

If both gateway and node are on the same Tailscale network:
```bash
openclaw node run --host <gateway-tailscale-ip> --port 18789
```

No SSH tunnel needed — Tailscale handles encrypted connectivity.

### TLS Connection

```bash
openclaw node run --host <gateway-host> --port 18789 --tls --tls-fingerprint <fingerprint>
```

## system.run Security Details

### Env Allowlist

For shell wrappers (`bash -c`, etc.), only these env vars pass through:
- `TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`

### Stripped Keys

Node hosts strip dangerous keys from all exec environments:
- `DYLD_*`, `LD_*` (library injection)
- `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT` (runtime injection)
- `SHELLOPTS`, `PS4` (shell injection)
- `PATH` overrides (use standard install locations instead)

### Wrapper Unwrapping

For allow-always in allowlist mode, known dispatch wrappers (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths. If unwrapping is unsafe, no entry is persisted.

### Windows Node Hosts

On Windows in allowlist mode, `cmd.exe /c` wrapper runs require separate approval. Allowlist entry alone does not auto-allow the wrapper form.
