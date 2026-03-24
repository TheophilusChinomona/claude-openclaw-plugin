---
name: openclaw-channels
description: >
  Use when the user wants to set up WhatsApp, configure Telegram, add Discord,
  connect Slack, pair a channel, manage OpenClaw channels, configure DM policies,
  set up group mention gating, or connect any messaging platform to OpenClaw.
---

# OpenClaw Channel Setup

Guide the user through connecting messaging platforms to their OpenClaw gateway.

## Supported Channels

**Built-in:** WhatsApp, Telegram, Discord, Slack, Signal, BlueBubbles, iMessage (legacy), IRC, Google Chat, WebChat

**Plugin channels:** Matrix, Mattermost, Microsoft Teams, Feishu, LINE, Nextcloud Talk, Nostr, Synology Chat, Tlon, Twitch, Zalo

**Fastest setup:** Telegram (simple bot token). **Most popular:** WhatsApp (QR pairing, more state on disk).

## DM Policies

Each channel has a `dmPolicy` controlling who can message the bot:

| Policy | Behavior |
|--------|----------|
| `pairing` | Unknown senders get 8-char code (expires 1hr). Owner approves via CLI. Default. |
| `allowlist` | Only sender IDs in `allowFrom` list. Requires at least one ID. |
| `open` | Any sender allowed. Requires `allowFrom: ["*"]`. |
| `disabled` | No DM processing. |

Manage pairing:
```bash
openclaw pairing list <channel>
openclaw pairing approve <channel> <CODE>
```

## Group Mention Gating

Groups require explicit configuration. Two controls apply together:

1. **Which groups** - Configure `groups` section (acts as allowlist)
2. **Which senders** - Set `groupPolicy` (open/allowlist/disabled)

By default, groups require `@mention` to respond:
```json5
{
  channels: {
    telegram: {
      groups: {
        "*": { requireMention: true },
      },
    },
  },
}
```

## Telegram Setup (BotFather + grammY)

1. Open Telegram, chat with `@BotFather`, run `/newbot`
2. Save the bot token (format: `123:abc...`)
3. Configure:
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```
4. Start gateway, approve first DM:
```bash
openclaw gateway restart
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

**Privacy mode:** Disable via `/setprivacy` in BotFather, or make bot a group admin. Remove and re-add bot to groups after changing.

## WhatsApp Setup (Baileys + QR)

1. Install the WhatsApp plugin (required as of v2026.3.22+):
```bash
openclaw plugins install @openclaw/whatsapp
```
2. Configure channel:
```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```
3. Start gateway — QR code appears in terminal or Control UI
4. Scan QR with WhatsApp on your phone (Settings > Linked Devices)
5. Approve DMs via pairing codes

### WhatsApp Troubleshooting

**Plugin not found after update (`plugin not found: whatsapp`):**
WhatsApp was unbundled from the main package in v2026.3.22 but the runtime files were missing in v2026.3.22 and v2026.3.23. Fixed in v2026.3.23-2. If on an affected version, upgrade:
```bash
npm install -g openclaw@latest
openclaw gateway restart
```
If still missing, install plugin manually:
```bash
openclaw plugins install @openclaw/whatsapp
openclaw gateway restart
```

**Session conflict (status 440):**
Happens when re-linking while the old session is still active. The gateway auto-recovers — wait for "Listening for personal WhatsApp inbound messages." in logs. If it doesn't recover:
```bash
openclaw channels login --channel whatsapp   # fresh QR scan
```

**Messages arriving but no reply (messagesHandled: 0):**
Check `dmPolicy` and `allowFrom`. With `dmPolicy: "allowlist"`, messages from numbers not in `allowFrom` are silently dropped — no pairing code is sent.
```bash
openclaw channels status --probe             # shows allowFrom list
openclaw config set channels.whatsapp.allowFrom '["+1234567890", "+0987654321"]'
openclaw gateway restart
```

**Verify channel health:**
```bash
openclaw channels status --probe             # running/connected + last inbound time
openclaw logs --limit 100                    # look for inbound/dispatch events
openclaw status --deep                       # full health check incl. WhatsApp
```

## Discord Setup (Bot API + Gateway)

1. Create app at discord.com/developers, add Bot, enable Message Content Intent
2. Generate bot token, invite to server with appropriate permissions
3. Configure:
```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "your-token",
      dmPolicy: "pairing",
    },
  },
}
```

## Slack Setup (Bolt SDK)

1. Create Slack app at api.slack.com/apps
2. Enable Socket Mode, add Bot Token Scopes
3. Configure:
```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
    },
  },
}
```

## Multi-Account Channels

Run multiple bots on the same channel:
```json5
{
  channels: {
    telegram: {
      defaultAccount: "main",
      accounts: {
        main: { botToken: "123:abc", dmPolicy: "pairing" },
        work: { botToken: "456:def", dmPolicy: "allowlist", allowFrom: ["111"] },
      },
    },
  },
}
```

## Channel Status

```bash
openclaw channels status           # All channels
openclaw channels status --probe   # Probe connections
```

See `references/channel-setup.md` for per-channel checklists with detailed config snippets.
