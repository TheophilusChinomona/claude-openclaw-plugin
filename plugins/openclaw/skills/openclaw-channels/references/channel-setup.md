# Channel Setup Checklists

## Telegram

### Prerequisites
- Telegram account
- @BotFather bot token

### Steps
1. Chat with `@BotFather` (verify exact handle — beware imposters)
2. Send `/newbot`, follow prompts, save token (format: `123:abc...`)
3. Optional: `/setprivacy` to disable (allows bot to see all group messages)
4. Optional: `/setjoingroups` to control group add permissions

### Config
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",              // or SecretRef
      dmPolicy: "pairing",             // "pairing" | "allowlist" | "open" | "disabled"
      allowFrom: ["tg:123456789"],     // for allowlist policy

      // Group access
      groupPolicy: "allowlist",        // "open" | "allowlist" | "disabled"
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          requireMention: false,
          topics: {
            "1": { agentId: "main" },
            "3": { agentId: "coder" },
          },
        },
      },

      // Streaming
      streaming: "partial",           // "off" | "partial" | "block" | "progress"

      // Commands menu
      customCommands: [
        { command: "backup", description: "Git backup" },
      ],

      // Inline buttons
      capabilities: {
        inlineButtons: "allowlist",    // "off" | "dm" | "group" | "all" | "allowlist"
      },

      // Reactions
      reactionNotifications: "own",    // "off" | "own" | "all"
      reactionLevel: "minimal",        // "off" | "ack" | "minimal" | "extensive"
    },
  },
}
```

### Environment fallback
`TELEGRAM_BOT_TOKEN=...` (default account only)

### Webhook mode (optional)
```json5
{
  channels: {
    telegram: {
      webhookUrl: "https://example.com/telegram-webhook",
      webhookSecret: "secret-key",
      webhookPort: 8787,
    },
  },
}
```

### Network troubleshooting
```json5
{
  channels: {
    telegram: {
      proxy: "socks5://user:pass@proxy:1080",
      network: {
        autoSelectFamily: false,
        dnsResultOrder: "ipv4first",
      },
    },
  },
}
```

### Finding Group Chat ID
- Forward group message to `@userinfobot` or `@getidsbot`
- Read from `openclaw logs --follow`
- Inspect Bot API `getUpdates`

---

## WhatsApp

### Prerequisites
- WhatsApp account on phone
- Phone with WhatsApp installed
- WhatsApp plugin installed (unbundled as of v2026.3.22)

### Steps
1. Install the plugin:
```bash
openclaw plugins install @openclaw/whatsapp
```
2. Add WhatsApp config to `openclaw.json`
3. Start gateway — QR code appears
4. On phone: Settings > Linked Devices > Link a Device
5. Scan QR code
6. Approve first DM via pairing code

### Troubleshooting

**`plugin not found: whatsapp` after update:**
WhatsApp was unbundled in v2026.3.22. Runtime files were missing in v2026.3.22 and v2026.3.23 — fixed in v2026.3.23-2.
```bash
npm install -g openclaw@latest         # upgrade to get bundled runtime
openclaw gateway restart
# If still broken, install manually:
openclaw plugins install @openclaw/whatsapp
openclaw gateway restart
```

**Status 440 session conflict during re-link:**
The new QR session kicks out the old one — this is normal. Gateway auto-restarts in 5s. If it loops:
```bash
# On phone: Settings > Linked Devices > remove all stale "OpenClaw" entries
openclaw channels login --channel whatsapp   # fresh QR
```

**Messages received but agent never replies:**
Most common cause: number not in `allowFrom` when `dmPolicy: "allowlist"`. Messages are silently dropped — no pairing code, no error.
```bash
openclaw channels status --probe   # check allow: list
# Add the missing number:
openclaw config set channels.whatsapp.allowFrom '["+27xxxxxxxxx", "+27yyyyyyyyy"]'
openclaw gateway restart
```
Confirm fix: `openclaw logs --limit 100` should show `messagesHandled > 0` in the heartbeat after next message.

### Config
```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      accountNumber: "+1234567890",
      dmPolicy: "pairing",
      allowFrom: ["+15555550123"],

      groupPolicy: "disabled",
      groups: {
        "*": { requireMention: true },
      },
    },
  },
}
```

### Multi-account
```json5
{
  channels: {
    whatsapp: {
      accounts: {
        personal: { accountNumber: "+1..." },
        biz: { accountNumber: "+2..." },
      },
    },
  },
}
```

---

## Discord

### Prerequisites
- Discord account
- Discord Developer Portal access

### Steps
1. Go to discord.com/developers/applications
2. Create New Application > Add Bot
3. Enable **Message Content Intent** under Bot settings
4. Copy bot token
5. Generate invite URL with required permissions (Send Messages, Read Message History, etc.)
6. Invite bot to your server

### Config
```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "your-discord-bot-token",
      dmPolicy: "pairing",

      groupPolicy: "allowlist",
      guilds: {
        "123456789012345678": {
          channels: {
            "222222222222222222": {
              allow: true,
              requireMention: false,
            },
          },
        },
      },
    },
  },
}
```

---

## Slack

### Prerequisites
- Slack workspace admin access
- Slack API app

### Steps
1. Go to api.slack.com/apps > Create New App
2. Enable Socket Mode
3. Add Bot Token Scopes: `chat:write`, `app_mentions:read`, `im:history`, `im:read`, `im:write`
4. Install app to workspace
5. Copy Bot Token (`xoxb-...`) and App-Level Token (`xapp-...`)

### Config
```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dmPolicy: "pairing",
    },
  },
}
```

---

## Signal

### Prerequisites
- Signal account
- signal-cli installed

### Config
```json5
{
  channels: {
    signal: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}
```

---

## Google Chat

### Prerequisites
- Google Workspace account
- Google Chat API enabled

### Config
```json5
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountRef: { source: "file", provider: "filemain", id: "/path/to/sa.json" },
    },
  },
}
```

---

## DM Policy Details

### Pairing
- 8-char code, uppercase, no ambiguous chars (0O1I)
- Expires after 1 hour
- Bot only sends pairing message for new requests (~once/hour per sender)
- Pending requests capped at 3 per channel

### Pairing State Storage
- Pending: `~/.openclaw/credentials/<channel>-pairing.json`
- Approved: `~/.openclaw/credentials/<channel>-allowFrom.json`
- Multi-account: `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json`

### CLI Commands
```bash
openclaw pairing list <channel>
openclaw pairing list --channel <ch> --account <id>
openclaw pairing approve <channel> <CODE>
```

---

## Device Pairing (iOS/Android Nodes)

### Via Telegram (Recommended)
1. Message your bot: `/pair`
2. Bot replies with setup code (base64 JSON with gateway URL + pairing token)
3. On phone app: Settings > Gateway > paste setup code
4. In Telegram: `/pair approve`

### Via CLI
```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices approve --latest
```

### State Storage
- `~/.openclaw/devices/pending.json`
- `~/.openclaw/devices/paired.json`

---

## Running Multiple Channels

Channels run simultaneously. OpenClaw routes messages per chat automatically:
```json5
{
  channels: {
    telegram: { enabled: true, botToken: "..." },
    whatsapp: { enabled: true },
    discord: { enabled: true, botToken: "..." },
    slack: { enabled: true, botToken: "xoxb-...", appToken: "xapp-..." },
  },
}
```
