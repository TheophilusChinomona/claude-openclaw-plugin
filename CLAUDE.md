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
  commands/
    oc-*.md            # 14 slash commands
  skills/
    openclaw-*/
      SKILL.md         # Skill definition (YAML frontmatter + markdown)
      references/      # Supporting reference docs
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
