---
name: openclaw-docs
description: >
  Use when the user asks about OpenClaw documentation sources, how to access
  crawled docs, where to find official documentation, how the documentation
  sync system works, or when referencing OpenClaw product docs for any task.
---

# OpenClaw Documentation

The plugin maintains a local cache of official OpenClaw documentation from two upstream sources. This enables all skills and agents to reference authoritative, up-to-date product docs.

## Documentation Sources

### 1. docs.openclaw.ai (Primary)

The official documentation site. Provides a machine-readable index at:

```
https://docs.openclaw.ai/llms.txt
```

This `llms.txt` file lists ~431 pages using Markdown link syntax:
```
- [Cron Jobs](https://docs.openclaw.ai/automation/cron-jobs)
- [Telegram Setup](https://docs.openclaw.ai/channels/telegram)
```

**Categories:** automation, channels, cli, concepts, gateway, install, platforms, plugins, providers, reference, security, start, tools, web

### 2. GitHub Repository

Source code and docs at `https://github.com/openclaw/openclaw/tree/main/docs`.

Raw content available at:
```
https://raw.githubusercontent.com/openclaw/openclaw/main/docs/<path>
```

Useful for: release notes, contribution guides, source-level documentation not on the docs site.

## Local Storage

### Two-Tier Architecture

```
plugins/openclaw/
  docs/                              # Committed (metadata only)
    docs-manifest.json               # Tracks fetched pages, timestamps, hashes
    INDEX.md                         # Categorized index with fetch status
    FETCH-CONFIG.md                  # Source URLs, priority tiers, staleness rules
  .crawled/                          # Gitignored (regenerable content)
    docs.openclaw.ai/               # Fetched from docs site
      automation/
        cron-jobs.md
        webhooks.md
      channels/
        telegram.md
        whatsapp.md
      cli/
        commands.md
      ...
    github/                          # Fetched from GitHub
      docs/
        start/
        cli/
```

**Why two tiers?** The `docs/` directory is committed to git so marketplace installs know what documentation exists. The `.crawled/` directory is gitignored because it contains regenerable content that can be re-fetched with `/oc-docs sync`.

## Accessing Docs

To read a cached documentation page:
```
Read .crawled/docs.openclaw.ai/<category>/<filename>.md
```

Examples:
- Cron jobs: `Read .crawled/docs.openclaw.ai/automation/cron-jobs.md`
- Telegram setup: `Read .crawled/docs.openclaw.ai/channels/telegram.md`
- CLI commands: `Read .crawled/docs.openclaw.ai/cli/commands.md`

To find what's available:
- Check `docs/INDEX.md` for a categorized listing
- Check `docs/docs-manifest.json` for detailed metadata

## Priority Tiers

| Tier | Categories | Pages | When Fetched |
|------|-----------|-------|-------------|
| **1** | automation, channels, cli, concepts, gateway, security | ~148 | Default `/oc-docs sync` |
| **2** | install, providers, tools, platforms, reference, start | ~124 | `--full` or `--category` |
| **3** | web, plugins, root pages | ~13 | On explicit request only |

## When .crawled/ Is Empty

If `.crawled/` doesn't exist or has no content, suggest the user run:
```
/oc-docs sync
```

This fetches Tier 1 documentation (~148 core pages). For all pages:
```
/oc-docs sync --full
```

## How Other Skills Should Use Docs

When a skill needs authoritative OpenClaw documentation:
1. Check if the relevant page exists in `.crawled/docs.openclaw.ai/<category>/`
2. If it exists, read it for accurate, up-to-date information
3. If it doesn't exist, fall back to the skill's embedded `references/` content
4. If `.crawled/` is entirely empty, suggest `/oc-docs sync` before proceeding

This ensures skills provide the most current information while gracefully degrading when docs haven't been synced.
