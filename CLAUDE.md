# OpenClaw Plugin for Claude Code

## Project Overview

This is a Claude Code plugin for managing OpenClaw, a self-hosted AI gateway. The plugin provides skills, commands, and an agent for setup, configuration, troubleshooting, and operations.

## Architecture

```
.claude-plugin/
  marketplace.json     # Marketplace metadata (name, owner, plugin entries)
plugins/openclaw/
  .claude-plugin/
    plugin.json        # Plugin manifest (version, agents, commands, skills)
  agents/
    openclaw-ops.md    # Operations agent (auto-triggers on OpenClaw questions)
    openclaw-docs-sync.md  # Documentation sync agent (fetches upstream docs)
  commands/
    oc-*.md            # Slash commands
  skills/
    openclaw-*/
      SKILL.md         # Skill definition (YAML frontmatter + markdown)
      references/      # Supporting reference docs
  docs/                # Committed metadata for documentation sync
    docs-manifest.json # Tracks fetched pages, timestamps, content hashes
    INDEX.md           # Generated categorized index with fetch status
    FETCH-CONFIG.md    # Source URLs, priority tiers, staleness rules
  .crawled/            # Gitignored — fetched documentation content
    docs.openclaw.ai/  # Pages from docs site, by category
    github/            # Pages from GitHub raw content
  README.md            # Plugin-level documentation
```

## Conventions

- **Skills**: YAML frontmatter (`name`, `description`, `trigger`) + markdown body. Each skill gets its own directory under `skills/`.
- **Commands**: Single markdown file per command in `commands/`. Filename = command name (e.g., `oc-status.md` for `/oc-status`).
- **Agents**: Markdown with YAML frontmatter (`name`, `model`, `color`, `description`, `allowed-tools`).
- **Versioning**: Bump version in both `plugin.json` and `marketplace.json` when releasing.

## Validation

```bash
claude plugin validate .
```
