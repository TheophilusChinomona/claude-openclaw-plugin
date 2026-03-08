---
description: Backup OpenClaw configuration, credentials, and auth profiles
argument-hint: [path]
allowed-tools: Bash, Read
---

# /oc-backup Command

Create a backup archive of OpenClaw configuration, credentials, and auth profiles.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **path** (optional): destination path for the backup archive. Default: `~/openclaw-backup-<date>.tar.gz`

## Execution

1. **Check OpenClaw state directory exists:**
```bash
ls ~/.openclaw/
```

2. **Create backup archive:**
```bash
BACKUP_PATH="${ARGUMENTS:-$HOME/openclaw-backup-$(date +%Y%m%d-%H%M%S).tar.gz}"
tar czf "$BACKUP_PATH" \
  -C "$HOME" \
  .openclaw/openclaw.json \
  .openclaw/credentials/ \
  .openclaw/agents/*/agent/auth-profiles.json \
  .openclaw/secrets.json \
  .openclaw/node.json \
  2>/dev/null
echo "Backup created: $BACKUP_PATH"
ls -lh "$BACKUP_PATH"
```

Note: Some files may not exist (e.g., `secrets.json`, `node.json`). Suppress errors for missing files.

3. **Warn about sensitivity:**

Report to the user:
```
⚠ This backup contains sensitive data:
  - API keys and tokens (openclaw.json, auth-profiles.json)
  - Channel credentials (credentials/)
  - Secret store (secrets.json)

Recommendations:
  - Encrypt the backup: gpg -c <backup-file>
  - Store in a secure location (not cloud sync)
  - Delete after restoring
```

4. **Show backup contents:**
```bash
tar tzf "$BACKUP_PATH" | head -30
```

## Restore Instructions

After creating the backup, provide restore instructions:

```bash
# Restore (overwrites existing config):
tar xzf <backup-file> -C "$HOME"
openclaw doctor        # verify config
openclaw gateway restart  # apply changes
```

## After Running

- Suggest encrypting with GPG: `gpg -c <backup-file>`
- Remind that credentials should be rotated periodically regardless
- Suggest adding backup to a cron job for regular backups
- For full disaster recovery, also back up workspace directories (`~/.openclaw/workspace*`)
