---
name: openclaw-agent-teams
description: >
  Use when the user wants to design an agent team, write SOUL.md files, set up agent
  hierarchy, configure agent tools and permissions, understand memory architecture,
  set up cron schedules for agents, or follow best practices for organizing an
  OpenClaw agent team.
---

# Agent Team Design & Operations

Guide the user through designing, building, and operating a production agent team following ClawPort best practices.

## Hierarchy Design

Agent teams follow a three-tier hierarchy:

| Tier | Role | Example |
|------|------|---------|
| Orchestrator | Top-level coordinator. Routes work, holds team memory, delivers briefings. | **Jarvis** (`reportsTo: null`) |
| Team Lead | Owns a domain pipeline end-to-end. Manages a sub-team. | **VERA** (Strategy), **LUMEN** (SEO), **HERALD** (LinkedIn) |
| Specialist | Does one thing well. Reports up, never manages others. | **TRACE** (Market Research), **QUILL** (LinkedIn Writer) |

### Hierarchy Rules

1. **One root.** Exactly one agent has `"reportsTo": null` — the orchestrator.
2. **Team leads own pipelines.** Each lead runs end-to-end delivery for their domain.
3. **Leaf agents are specialists.** One job, no scope creep.
4. **Max depth of 3.** Deeper nesting adds latency with little benefit.
5. **Keep directReports consistent.** If B has `"reportsTo": "A"`, then A's `directReports` must include B.

## SOUL.md — Agent Character Documents

Every agent needs a `SOUL.md` that defines identity, expertise, constraints, and relationships.

```
# AGENT_NAME -- Role Title

## Identity
Who the agent is. Personality. Communication style.
First-person voice: "I am VERA, the Chief Strategy Officer."

## Expertise
Domains this agent knows deeply.
What it defers to other agents.

## Operating Rules
Hard constraints. What it must always/never do.
Output format requirements.

## Relationships
Reports to. Direct reports. Peer collaborators.

## Memory
What it remembers between sessions.
Where its persistent knowledge lives.
```

Guidelines:
- **Be specific about personality.** Distinct voices prevent agents from sounding the same.
- **Define what the agent does NOT do.** Negative constraints are as important as positive ones.
- **Include output format examples.** If the agent produces structured data, show the format.
- **Keep it under 500 lines.** Long SOUL files dilute focus.

## Naming Conventions

| Pattern | When to Use | Examples |
|---------|-------------|---------|
| UPPERCASE | Pipeline/team agents (callsign feel) | VERA, LUMEN, SCOUT, QUILL |
| Title Case | Standalone/personality agents, orchestrator | Jarvis, Robin, Pulse |

IDs are always lowercase slugs: `vera`, `lumen`, `herald`.

## Tool Assignment (Least Privilege)

| Tool | Purpose | Who Gets It |
|------|---------|-------------|
| `read` | Read workspace files | Almost everyone (base capability) |
| `write` | Write/create files | Content producers (WRITER, ANALYST) |
| `exec` | Run shell commands | Orchestrator + team leads only |
| `web_search` | Search the web | Research agents (TRACE, SCOUT, Pulse) |
| `web_fetch` | Fetch a URL | Scraper/monitor agents (ECHO, KAZE) |
| `message` | Send to other agents | Coordinators (Jarvis, Robin, Pulse) |
| `sessions_spawn` | Spawn sub-sessions | Orchestrator + team leads only |
| `memory_search` | Search team memory | Orchestrator only |

**Never give `exec` to leaf agents.** If a specialist needs a command run, it asks its team lead.

## Memory Architecture

Three tiers working together:

| Tier | What | Lifespan | Who Manages |
|------|------|----------|-------------|
| Daily Logs | Raw session output, timestamped | 7-14 days | Each agent writes its own |
| MEMORY.md | Curated persistent knowledge | Indefinite (updated weekly) | **SCRIBE** compresses weekly |
| Team Memory | Shared cross-agent knowledge | Indefinite | Team leads + orchestrator |

> **Full guide:** See `openclaw-memory` skill for the four-layer memory model, bootstrap file setup, shared memory access patterns, SCRIBE compression rules, failure mode defenses, retrieval setup, and the `/oc-memory` command.

## Agent Communication

Prefer **files over messages**:
1. **Upstream:** Agent writes output file, team lead reads it next run.
2. **Downstream:** Lead writes brief, specialist reads and executes.
3. **Cross-team:** Agents read from `team-memory/` shared files.

The `message` tool is for urgency only (e.g., Pulse alerting about a breaking trend).

## Cron Patterns

- **Assign to the right tier:** Research crons on leaf agents, pipeline crons on leads, briefing crons on orchestrator.
- **Stagger schedules:** Upstream agents finish before downstream agents read their output.
- **One cron, one job:** "Scan subreddits" is good. "Scan, analyze, write, and publish" is four crons pretending to be one.
- **Error isolation:** A failed cron only affects its own output. Stale data beats cascade failure.

## Design Principles

1. **Agents are characters, not functions.** Distinct names, personalities, expertise.
2. **Least privilege, always.** Start without a tool; add it when proven necessary.
3. **Files over messages.** Inspectable, diffable, persistent.
4. **One agent, one job.** If the description needs "and" twice, split into two agents.
5. **Depth of 3, max.** Add lateral agents instead of deeper nesting.
6. **Let SCRIBE handle memory.** Single responsibility for memory compression.

See `references/best-practices.md` for the full implementation guide with registry examples, SCRIBE workflow, cron schedules, and workspace setup scripts.
