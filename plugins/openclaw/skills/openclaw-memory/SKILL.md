---
name: openclaw-memory
description: >
  Use when the user wants to set up memory, understand memory architecture, bootstrap files,
  configure shared memory, write MEMORY.md, set up daily logs, understand SCRIBE compression,
  fix memory retrieval, debug memory failure modes, set up team memory, configure agent memory,
  understand memory layers, or use memory compression patterns.
---

# Agent Memory Architecture (OpenClaw)

Memory is the most fragile part of an agent system. Three failure modes kill agent memory:
1. **Never stored** — the agent saw it but never persisted it
2. **Compaction destroyed it** — context compaction summarized away the detail
3. **Pruning trimmed it** — MEMORY.md grew past budget and lost the entry

This skill teaches the four-layer memory model, bootstrap file setup, shared memory patterns, and defenses against each failure mode.

## The Four Memory Layers

| Layer | Name | Persistence | Scope | Example |
|-------|------|-------------|-------|---------|
| 1 | Bootstrap files | Permanent (committed) | Per-agent | AGENTS.md, SOUL.md, MEMORY.md |
| 1.5 | Daily logs | Semi-permanent (7-14 days) | Per-agent | memory/2026-03-10.md |
| 2 | Session transcript | Temporary (session lifetime) | Per-session | ~/.openclaw/agents/<id>/sessions/*.jsonl |
| 3 | Retrieval index | Permanent (vector DB) | System-wide | ~/.openclaw/memory/lancedb/ |

See `references/memory-layers.md` for deep dives on each layer including token budgets, eviction order, and LanceDB setup.

## Bootstrap Files (Layer 1)

Every agent workspace should contain these files, loaded at session start:

| File | Purpose | Loaded When | Sub-agent Visibility |
|------|---------|-------------|---------------------|
| AGENTS.md | Operating manual, safety rules, delegation rules | Always (first) | Yes — essential rules here |
| SOUL.md | Personality, boundaries, communication style | Always | No (main agent only) |
| IDENTITY.md | Name, role, avatar, vibe | Always | No |
| USER.md | User profile, preferences, timezone | Private sessions only | No |
| MEMORY.md | Long-term curated knowledge (200-line budget) | Private sessions only | No |
| TOOLS.md | Available tools, integration notes | On demand | Yes |
| HEARTBEAT.md | Proactive monitoring checklist | On heartbeat cron | No |

**Sub-agent visibility rule:** Sub-agents only receive AGENTS.md + TOOLS.md. Keep essential safety rules in AGENTS.md, not SOUL.md.

## Daily Logs (Layer 1.5)

Location: `memory/YYYY-MM-DD.md`

Daily logs are raw session notes — decisions made, facts learned, actions taken. They serve as the input buffer for SCRIBE compression.

```markdown
# 2026-03-10

## Decisions
- Chose Sonnet for outreach agent (cost vs quality tradeoff)

## Facts Learned
- ICP response rate peaks Tuesday-Thursday 9-11am EST

## Actions Taken
- Created VERA agent workspace with Operator autonomy level
```

**Retention:** Keep 7-14 days of daily logs before SCRIBE compression. Older uncompressed logs move to `memory/archive/`.

## SCRIBE Compression

Weekly cycle (typically Sunday or Monday):

1. **Read** all daily logs from the past 7 days
2. **Extract** durable patterns — facts that remain true, decisions that still apply, preferences confirmed multiple times
3. **Update** MEMORY.md with extracted patterns (respect the 200-line budget)
4. **Archive** processed daily logs to `memory/archive/`

The 200-line budget is **implicit decay** — information that doesn't survive compression is effectively forgotten. This is intentional: not everything deserves permanence.

### SCRIBE Rules

- **Merge, don't append.** If a new fact updates an existing MEMORY.md entry, replace the old one.
- **Prefer patterns over incidents.** "User prefers Sonnet for content agents" survives; "used Sonnet on Tuesday" doesn't.
- **Keep structure.** MEMORY.md should have clear sections (## Preferences, ## Architecture Decisions, ## Known Issues, etc.)
- **Never exceed 200 lines.** If you must add, remove something less durable.

## Memory Failure Modes & Defenses

| Failure Mode | Cause | Defense |
|-------------|-------|---------|
| Never stored | Agent saw information but didn't write it to daily log or MEMORY.md | **Explicit save rules** in AGENTS.md: "After every decision, log it to today's daily log" |
| Compaction destroyed | Context window compaction summarized away important detail | **Pre-compaction flush**: detect >80% context usage, save critical facts to daily log before compaction triggers |
| Pruning trimmed | MEMORY.md exceeded 200 lines, older entries dropped | **MEMORY.md curation**: weekly SCRIBE review, promote truly durable facts, demote stale entries |

### Pre-Compaction Flush Procedure

When context usage approaches 80%:
1. Identify facts in the current conversation not yet saved
2. Write them to today's daily log (`memory/YYYY-MM-DD.md`)
3. If any are long-term durable, update MEMORY.md
4. Allow compaction to proceed — the important data is now persisted

## Shared Memory

Three patterns for cross-agent knowledge sharing:

### Pattern 1: team-memory/ Directory

Shared files accessible to all team agents:

```
team-memory/
  market-brief.md       # Market intelligence, ICP data
  icp-profile.md        # Ideal customer profile
  brand-voice.md        # Tone, style, terminology
  content-calendar.md   # Planned content schedule
  tech-stack.md         # Architecture decisions
```

Naming convention: `<domain>-<type>.md` (e.g., `market-brief.md`, `content-calendar.md`).

### Pattern 2: GROUP_MEMORY.md

Per-agent file containing only information safe for group contexts. Unlike MEMORY.md (private), GROUP_MEMORY.md is visible when the agent operates in shared channels.

### Pattern 3: SHARED_KNOWLEDGE.json

System-level semantic memory at `~/.openclaw/workspace/SHARED_KNOWLEDGE.json`. Structured key-value pairs for machine-readable facts shared across all agents.

See `references/shared-memory-patterns.md` for access control tables, conflict resolution rules, and example team-memory files.

## Shared Memory Access Control

| Agent Tier | team-memory/ | SHARED_KNOWLEDGE.json | Other agent's MEMORY.md |
|-----------|-------------|----------------------|------------------------|
| Orchestrator | Read + Write all | Read + Write | Read (for coordination) |
| Team Lead | Read all, Write own domain | Read | No access |
| Specialist | Read-only | Read | No access |

Access control is enforced via SOUL.md rules — each agent's SOUL.md states what shared resources it can read and write.

## Namespace Conventions

- Files in team-memory/ follow `<domain>-<type>.md` naming
- Agent output that should be shared gets promoted: agent writes to `output/`, team lead reviews and copies to `team-memory/`
- **Newest-wins** for factual conflicts: if two agents write conflicting facts, the most recent timestamp wins
- **Append-only** for events: event logs are never overwritten, only appended
- SCRIBE resolves persistent contradictions during weekly compression

## Memory Retrieval

### Track A: Built-in (LanceDB)

- Vector store at `~/.openclaw/memory/lancedb/`
- Tool: `memory_search` (available to orchestrator)
- Embedding model: configured in `models.json`
- Search type: MIPS (Maximum Inner Product Search)
- Diagnostic: `openclaw context list` to verify indexed content

### Track B: External

- Obsidian vault integration
- QMD (Quick Memory Database)
- Custom retrieval via `web_fetch` to local endpoints

## Setup Checklist

When setting up memory for a new agent or team:

- [ ] Create bootstrap files (AGENTS.md, SOUL.md, IDENTITY.md, USER.md) with save rules in AGENTS.md
- [ ] Create `memory/` directory for daily logs
- [ ] Create `MEMORY.md` with section headers and 200-line budget note
- [ ] Set up daily log workflow (agent writes to `memory/YYYY-MM-DD.md` each session)
- [ ] Configure SCRIBE compression schedule (weekly cron or manual)
- [ ] Create `team-memory/` directory if multi-agent setup
- [ ] Verify LanceDB is initialized (`ls ~/.openclaw/memory/lancedb/`)
- [ ] Run `/oc-memory audit` to validate setup

## Cross-References

- **Workspace layout**: See `openclaw-workspace-structure` skill for directory structure
- **Team design**: See `openclaw-agent-teams` skill for hierarchy, SOUL.md authoring, communication patterns
- **Agent building**: See `openclaw-agent-builder` skill for end-to-end agent creation workflow
- **Memory command**: Use `/oc-memory` for init, audit, flush, search, and shared memory management
