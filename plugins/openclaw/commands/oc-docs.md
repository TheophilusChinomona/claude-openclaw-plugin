---
description: Fetch, search, and manage OpenClaw documentation — sync from upstream, check status, search crawled docs
argument-hint: "[sync [--full] [--category <name>] [--force] | status | search <query> | fetch <url>]"
allowed-tools: Bash, Read, Write, WebFetch, Glob, Grep
---

# /oc-docs Command

Manage locally-cached OpenClaw documentation from docs.openclaw.ai and GitHub.

## Plugin Root

Determine the plugin root path:
```bash
PLUGIN_ROOT="$HOME/.claude/plugins/openclaw-plugin/plugins/openclaw"
```

## Subcommands

Parse the user's arguments to determine the subcommand:

### `sync` (default if no args)

Fetch and update documentation from upstream sources using parallel HTTP.

**Flags:**
- `--full` — Fetch all tiers (Tier 1 + 2 + 3, ~431 pages)
- `--category <name>` — Fetch only pages in the specified category
- `--force` — Re-fetch everything, ignore staleness
- `--concurrency N` — Max concurrent requests (default: 10)
- No flags — Fetch Tier 1 only (~148 core pages)

**Steps:**
1. Run the fetch script:
   ```bash
   cd "${PLUGIN_ROOT}" && python scripts/oc-docs-fetch.py sync [flags]
   ```
2. The script handles: fetching llms.txt, parsing entries, filtering by tier/category, parallel HTTP fetch, manifest updates, and INDEX.md regeneration.
3. Parse the JSON output from stdout for summary stats.
4. Report results to the user: pages fetched, unchanged, skipped, failed.

### `status`

Show documentation sync status.

**Steps:**
1. Run:
   ```bash
   cd "${PLUGIN_ROOT}" && python scripts/oc-docs-fetch.py status
   ```
2. Display the output directly to the user.

**Example output:**
```
OpenClaw Documentation Status
========================================
Total fetched: 148 pages
  docs-site:   148
  github:      0
Stale:         12 (> 7 days)
Storage:       2.3M

By Category:

  [Tier 1 - Core]
    automation       23 pages
    channels         31 pages
    cli              52 pages
    concepts          8 pages
    gateway          15 pages
    security         19 pages

  [Tier 2 - Extended]
    install           0 pages
    providers         0 pages
    ...
```

### `search <query>`

Search crawled documentation for a query string.

**Steps:**
1. Check if `.crawled/` exists and has content. If not, suggest `/oc-docs sync`.
2. Use Grep to search `.crawled/` for the query pattern.
3. Show matches with file path, line number, and surrounding context (3 lines).
4. Group results by category for readability.
5. Limit to 20 results by default, mention if more exist.

### `fetch <url>`

Fetch a single specific documentation page.

**Steps:**
1. Validate the URL starts with `https://`.
2. Run:
   ```bash
   cd "${PLUGIN_ROOT}" && python scripts/oc-docs-fetch.py fetch "<url>"
   ```
3. Report the result to the user.

### `github`

Download all docs from the GitHub repository via tarball.

**Steps:**
1. Run:
   ```bash
   cd "${PLUGIN_ROOT}" && python scripts/oc-docs-fetch.py github [--force]
   ```
2. Report number of extracted files.

## Empty State

If `.crawled/` doesn't exist or is empty, always display:
```
No documentation cached locally.
Run `/oc-docs sync` to fetch core documentation (~148 pages, Tier 1).
Run `/oc-docs sync --full` to fetch all documentation (~431 pages).
Run `/oc-docs github` to download docs from GitHub tarball.
```
