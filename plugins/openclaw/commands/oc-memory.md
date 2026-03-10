---
description: Initialize, audit, flush, and search agent memory — bootstrap files, daily logs, shared memory
argument-hint: "<init|audit|flush|search|shared> [--agent <id>] [--query <text>]"
allowed-tools: Bash, Read, Write, Glob, Grep
---

# /oc-memory Command

Manage agent memory: initialize workspaces, audit health, flush important facts, search across memory, and manage shared memory.

## Arguments

The user provides: `$ARGUMENTS`

Parse the subcommand and optional flags:
- **Subcommand** (required): `init`, `audit`, `flush`, `search`, `shared`
- `--agent <id>` — target a specific agent (default: scan all agents)
- `--query <text>` — search query (required for `search` subcommand)
- `--namespace <name>` — namespace for shared memory operations

If no subcommand is given, show usage:
```
Usage: /oc-memory <init|audit|flush|search|shared> [options]

  init    [--agent <id>]              Initialize memory structure
  audit   [--agent <id>]              Check memory health
  flush   [--agent <id>]              Persist important facts
  search  --query <text> [--agent <id>]  Search across memory
  shared  [list|create|update] [--namespace <name>]  Manage team memory
```

## Subcommand: init

Initialize memory structure for an agent workspace.

```bash
# Find agent workspaces
WORKSPACE_ROOT="${HOME}/.openclaw/workspace/agents-workspaces"
```

If `--agent <id>` is given, target that agent. Otherwise, ask the user which agent to initialize.

### Steps

1. Create `memory/` directory if missing:
```bash
mkdir -p "$WORKSPACE_ROOT/$AGENT_ID/memory"
mkdir -p "$WORKSPACE_ROOT/$AGENT_ID/memory/archive"
```

2. Create empty MEMORY.md with header template if missing:
```markdown
# MEMORY.md

> 200-line budget. Updated weekly by SCRIBE compression.
> Only durable facts, decisions, and preferences belong here.

## Preferences

## Architecture Decisions

## Known Issues

## Key Facts
```

3. Seed today's daily log if missing:
```markdown
# YYYY-MM-DD

## Decisions

## Facts Learned

## Actions Taken

## Open Questions
```

4. If multiple agents detected, create `team-memory/` at workspace root:
```bash
AGENT_COUNT=$(ls "$WORKSPACE_ROOT" 2>/dev/null | wc -l)
if [ "$AGENT_COUNT" -gt 1 ]; then
  mkdir -p "$WORKSPACE_ROOT/../team-memory"
fi
```

5. Report what was created.

## Subcommand: audit

Check memory health and report a scorecard.

### Checks

For each agent (or the specified `--agent`):

| Check | PASS | WARN | FAIL |
|-------|------|------|------|
| AGENTS.md exists | Present | — | Missing |
| SOUL.md exists | Present | — | Missing |
| IDENTITY.md exists | Present | — | Missing |
| MEMORY.md exists | Present | — | Missing |
| MEMORY.md line count | <= 200 lines | 150-200 lines | > 200 lines |
| memory/ directory | Exists with recent logs | Exists but empty | Missing |
| Daily log freshness | Log from today or yesterday | Oldest log > 7 days | No logs at all |
| Stale daily logs | None > 14 days old | 1-3 stale logs | 4+ stale logs needing compression |
| Save rules in AGENTS.md | Contains "daily log" or "memory" mention | — | No memory workflow defined |

System-wide checks (always run):

| Check | PASS | WARN | FAIL |
|-------|------|------|------|
| team-memory/ exists (if multi-agent) | Present | — | Missing when >1 agent |
| LanceDB directory | Present with files | Present but empty | Missing |
| SHARED_KNOWLEDGE.json | Present | — | Missing when >1 agent |

### Output

```
Memory Health Audit
═══════════════════

Agent: <agent-id>
  AGENTS.md ............ PASS
  SOUL.md .............. PASS
  IDENTITY.md .......... PASS
  MEMORY.md ............ PASS (87/200 lines)
  memory/ directory .... PASS
  Daily log freshness .. WARN (last log: 3 days ago)
  Stale logs ........... PASS
  Save rules ........... PASS

System:
  team-memory/ ......... PASS
  LanceDB .............. WARN (directory empty)
  SHARED_KNOWLEDGE ..... PASS

Score: 9/11 PASS, 2 WARN, 0 FAIL
```

## Subcommand: flush

Interactively persist important facts from the current session.

### Steps

1. Ask the user: "What important facts from this session should be saved?"
2. Append facts to today's daily log (`memory/YYYY-MM-DD.md`)
3. For each fact, ask: "Is this a long-term durable fact (should go in MEMORY.md)?"
4. If yes, add to appropriate MEMORY.md section
5. Check MEMORY.md line count after additions — warn if approaching 200-line budget
6. Report what was saved and where

## Subcommand: search

Search across all memory files for a query.

### Steps

1. Require `--query <text>`
2. Search locations (in order):
   - `MEMORY.md` files in all agent workspaces (or specified agent)
   - Daily logs in `memory/` directories
   - Files in `team-memory/`
   - `SHARED_KNOWLEDGE.json`

3. Use Grep to find matches with context:
```bash
# Search MEMORY.md files
grep -rn --include="MEMORY.md" "$QUERY" "$WORKSPACE_ROOT/"

# Search daily logs
grep -rn "$QUERY" "$WORKSPACE_ROOT/*/memory/"

# Search team memory
grep -rn "$QUERY" "$WORKSPACE_ROOT/../team-memory/"
```

4. Show results with file path and surrounding context (2 lines before/after)

### Output

```
Memory Search: "<query>"
══════════════════════════

Found 3 matches:

1. agents-workspaces/vera/MEMORY.md:15
   > ICP response rate peaks Tuesday-Thursday 9-11am EST

2. team-memory/market-brief.md:8
   > Target segment shows 40% higher engagement on Tuesdays

3. agents-workspaces/herald/memory/2026-03-08.md:12
   > A/B test confirmed Tuesday morning sends outperform Friday
```

## Subcommand: shared

Manage team-memory/ shared files.

### `shared list`

List team-memory/ files with sizes and last modified dates:

```bash
ls -lh "$WORKSPACE_ROOT/../team-memory/" 2>/dev/null
```

Output:
```
Team Memory Files
═════════════════

  market-brief.md      2.1K  2026-03-10 14:30
  icp-profile.md       1.4K  2026-03-08 09:15
  brand-voice.md       0.9K  2026-03-05 11:20
  content-calendar.md  0.6K  2026-03-10 08:00

4 files, 5.0K total
```

### `shared create [--namespace <name>]`

Create a new team-memory file from template:

1. Ask for namespace if not provided (e.g., "market-brief", "tech-stack")
2. Create `team-memory/<namespace>.md` with template:

```markdown
# <Namespace Title>

Last updated: YYYY-MM-DD by <agent>

## Summary

## Details
```

### `shared update [--namespace <name>]`

Open an existing team-memory file for editing:

1. Show current content
2. Ask user what to update
3. Apply changes
4. Update the "Last updated" line

## After Running

- After `init`: suggest running `audit` to verify setup
- After `audit` with failures: suggest specific fixes, offer to run `init` for missing structure
- After `flush`: confirm saves, suggest running `audit` to check line budgets
- After `search`: if no results, suggest checking if daily logs exist or running `/oc-docs search` for documentation
- After `shared`: remind that team-memory files are accessible to all team agents per access control rules
