# Contributing to OpenClaw Plugin

## Project Structure

```
.claude-plugin/
  marketplace.json          # Marketplace metadata
plugins/openclaw/
  .claude-plugin/plugin.json  # Plugin manifest
  agents/                     # Agent definitions (.md)
  commands/                   # Slash commands (.md)
  skills/                     # Skill directories
    <skill-name>/
      SKILL.md                # Skill definition
      references/             # Supporting reference docs
  hooks/hooks.json            # Lifecycle hooks (auto-loaded)
  scripts/                    # Hook and utility scripts
tests/                        # Validators (node tests/run-all.js)
```

## Adding a Skill

1. Create `plugins/openclaw/skills/<skill-name>/SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: <skill-name>
   description: >
     Use when the user wants to... Triggers on "keyword1", "keyword2".
   ---
   ```
2. Create `plugins/openclaw/skills/<skill-name>/references/` (add `.gitkeep` if empty)
3. Update the skill list in `plugins/openclaw/agents/openclaw-ops.md`
4. Add a row to the Skills table in `README.md`
5. Update counts in `README.md` and `marketplace.json`

## Adding a Command

1. Create `plugins/openclaw/commands/oc-<name>.md` with YAML frontmatter:
   ```yaml
   ---
   description: Short description of what the command does
   ---
   ```
2. Add a row to the Slash Commands table in `README.md`
3. Update counts in `README.md` and `marketplace.json`

## Adding a Hook

1. Create script in `plugins/openclaw/scripts/hooks/<hook-name>.js`
2. Add entry to `plugins/openclaw/hooks/hooks.json`
3. Do NOT add `"hooks"` field to `plugin.json` — it's auto-loaded by convention

## Naming Conventions

- Skills: `openclaw-<domain>` (e.g., `openclaw-security`)
- Commands: `oc-<action>` (e.g., `oc-status`)
- Agents: `openclaw-<role>` (e.g., `openclaw-ops`)
- Hook scripts: descriptive kebab-case (e.g., `pre-bash-openclaw-check.js`)

## Version Bumping

Update version in both:
- `plugins/openclaw/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

Update description counts in `marketplace.json` when adding components.

## Validation

```bash
# Run all tests
npm test

# Validate plugin structure
claude plugin validate .
```

## PR Process

1. Run `npm test` — all validators must pass
2. Run `claude plugin validate .` — plugin structure must be valid
3. Update CHANGELOG.md with your changes
4. Keep PR focused on a single feature or fix
