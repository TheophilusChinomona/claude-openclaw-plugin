---
description: Manage OpenClaw messaging channels
argument-hint: <channel> [setup|status|config|pair]
allowed-tools: Bash, Read, Write
---

# /oc-channel Command

Manage OpenClaw messaging channel integrations.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **channel** (required): Channel name (telegram, whatsapp, discord, slack, signal, etc.)
- **subcommand** (optional): setup, status, config, pair

## Subcommands

### `<channel> setup`
Guide through channel-specific setup. Use the openclaw-channels skill knowledge for step-by-step instructions.

**Telegram:** Create bot via @BotFather, get token, add to config.
**WhatsApp:** Configure channel, scan QR code.
**Discord:** Create app, enable intents, get token, invite bot.
**Slack:** Create app, enable Socket Mode, get tokens.

### `<channel> status`
Check channel connectivity:
```bash
openclaw channels status --probe
```

### `<channel> config`
Show current channel configuration:
```bash
openclaw config get channels.$channel
```

### `<channel> pair`
List and manage pairing requests:
```bash
openclaw pairing list $channel
```

If the user provides a pairing code to approve:
```bash
openclaw pairing approve $channel <CODE>
```

### No subcommand
Show channel status by default:
```bash
openclaw channels status --probe
```

## After Running

- Present results clearly with channel state and any issues
- If a channel is not configured, offer to guide through setup
- If pairing requests are pending, offer to approve them
