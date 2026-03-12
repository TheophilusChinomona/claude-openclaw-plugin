# Changelog

All notable changes to the OpenClaw Plugin for Claude Code.

## [0.8.0] - 2026-03-12

### Added
- **/oc-architect** command: Build or optimize agent workspace files (build | optimize, optional workspace path)
- **/oc-planner** command: Brainstorm, design, and document agent teams; produce Agent Team Documentation
- **openclaw-agent-architect** agent: Auto-triggers on agent persona, workspace files, scan/audit; applies openclaw-agent-architect skill
- **openclaw-agent-planner** agent: Auto-triggers on planning agents, multi-agent design, permissions; applies openclaw-agent-planner skill

### Changed
- plugin.json: 4 agents (added openclaw-agent-architect, openclaw-agent-planner)
- README: Agents 2 → 4; Commands 18 → 20; added new agents and commands to tables
- openclaw-ops: Skills list now includes openclaw-agent-architect and openclaw-agent-planner

## [0.7.0] - 2026-03-12

### Added
- **openclaw-agent-architect** skill: Build and optimize agent workspace files (SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, GOALS.md) via guided interview or scan-and-optimize; persona coherence and token-awareness
- **openclaw-agent-planner** skill: Brainstorm and document agent teams (Discovery → Design → Document); capability/permission matrices, inter-agent design, Agent Team Documentation package; references/permissions-reference.md for archetypes and access levels

### Changed
- README: Skills count 20 → 22; added openclaw-agent-architect and openclaw-agent-planner to skills table

## [0.6.0] - 2026-03-10

### Added
- **Hooks infrastructure**: 3 lifecycle hooks (pre-bash OpenClaw check, session docs check, post-config validator)
- **Permissions setup script**: `scripts/setup-permissions.js` auto-configures Claude Code allowlist
- **Test infrastructure**: Node.js validators for skills, commands, agents, and README counts
- **CHANGELOG.md**: Retrospective changelog from v0.1.0
- **CONTRIBUTING.md**: Contributor guide with naming conventions and PR process
- **package.json**: Enables `npm test` for CI
- **Agent examples**: `<example>` blocks on both agents for better triggering accuracy

### Fixed
- README.md counts corrected (17 -> 18 commands, 19 -> 20 skills)
- Missing `/oc-memory` command and `openclaw-memory` skill in README tables
- Missing `name` field in `openclaw-workspace-structure` SKILL.md frontmatter
- Missing `references/` directories for `openclaw-docs` and `openclaw-workspace-structure` skills
- `openclaw-ops` agent now lists all 20 skills (was missing 5)

## [0.5.0] - 2026-03-10

### Added
- `openclaw-memory` skill: Four-layer memory model, bootstrap files, shared memory, SCRIBE compression
- `/oc-memory` command: Initialize, audit, flush, and search agent memory
- Memory architecture documentation in workspace structure skill

## [0.4.0] - 2026-03-10

### Added
- `openclaw-docs` skill: Documentation sources, crawled doc access, sync system
- `/oc-docs` command: Fetch, search, and manage OpenClaw documentation
- `openclaw-docs-sync` agent: Autonomous documentation fetching from upstream sources
- `oc-docs-fetch.py` script: Parallel doc fetcher with content hashing and staleness detection
- Two-tier storage: committed metadata (`docs/`) + gitignored content (`.crawled/`)

## [0.3.0] - 2026-03-10

### Added
- `openclaw-autonomy-audit` skill: Audit and score agent autonomy readiness
- `/oc-autonomy` command: Scored autonomy assessment with improvement suggestions
- `openclaw-agent-builder` skill: End-to-end agent design with interview workflow

## [0.2.0] - 2026-03-08

### Added
- `openclaw-outreach-setup` skill: Outreach agent scaffolding, cold email pipeline
- `/oc-outreach` command: Scaffold and manage outreach agent
- `/oc-improve` command: Scan setup and suggest improvements
- `openclaw-multi-agent-team-setup` skill: Commander-specialist routing, mention gating
- 6 new skills: automation, sessions, models, security, sandboxing, nodes
- 4 new commands: `/oc-cron`, `/oc-security`, `/oc-backup`, `/oc-update`
- Multi-user workspaces skill with session isolation and trust model
- Agent teams skill with SOUL.md authoring and hierarchy design

## [0.1.0] - 2026-03-08

### Added
- Initial release with `openclaw-ops` agent
- Core skills: setup, config, channels, troubleshooting, multi-agent
- Core commands: `/oc-status`, `/oc-doctor`, `/oc-config`, `/oc-setup`, `/oc-channel`, `/oc-logs`, `/oc-team`, `/oc-workspace`, `/oc-structure`
- Marketplace registration for GitHub distribution
