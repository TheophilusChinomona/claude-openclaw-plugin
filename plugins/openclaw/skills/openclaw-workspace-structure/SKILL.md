---
name: openclaw-workspace-structure
description: >
  Use when the user wants to understand the OpenClaw workspace layout, inspect ~/.openclaw/ structure,
  audit agent workspaces, check workspace conventions, understand file-based orchestration,
  view agent directory organization, troubleshoot workspace paths, or set up a per-agent workspace.
---

# OpenClaw Workspace Structure

Explain and help the user navigate the standardized OpenClaw workspace layouts. Two levels exist:

1. **System-level layout** (`~/.openclaw/`) — Created by the OpenClaw CLI, holds global config and all agent workspaces
2. **Per-agent workspace layout** — The flatter pattern each agent uses inside its workspace directory

## Per-Agent Workspace Layout

Each agent workspace follows this flatter layout with bootstrap files at root:

```
<agent-workspace>/
  AGENTS.md              # Operating manual (safety rules, delegation, memory workflow)
  SOUL.md                # Personality, boundaries, communication style
  IDENTITY.md            # Name, role, avatar, vibe
  USER.md                # Who the agent serves (private sessions only)
  MEMORY.md              # Long-term curated knowledge (200-line budget)
  TOOLS.md               # Available tools, integration notes
  HEARTBEAT.md           # Proactive monitoring checklist
  GROUP_MEMORY.md        # Info safe for group contexts (optional)
  agents/                # Sub-agent directories (team workspace)
    <agent-id>/
      SOUL.md
      MEMORY.md
      logs/
      output/
  skills/                # Workspace-specific skills
  memory/                # Daily logs
    YYYY-MM-DD.md        # Raw session notes
    archive/             # Compressed logs older than 14 days
  team-memory/           # Shared cross-agent knowledge
    market-brief.md
    icp-profile.md
    brand-voice.md
  config/                # Local configuration
    security.json
  output/                # Agent work products
  logs/                  # Operational logs
```

> **Memory details:** See `openclaw-memory` skill for the four-layer memory model, bootstrap file loading order, daily log workflow, SCRIBE compression, shared memory patterns, and `/oc-memory` command.

## System-Level Layout (CLI-Managed)

```
~/.openclaw/
  openclaw.json              # Central configuration
  models.json                # Model registry
  workspace/                 # Shared collaboration space
    CLAUDE.md                # Shared instructions for all agents
    TASKS.json               # Task tracking (RACI schema)
    SPRINT_CURRENT.json      # Active sprint data
    SHARED_KNOWLEDGE.json    # Semantic memory layer
    IMPROVEMENT_BACKLOG.json # Continuous improvement items (min 5)
    agents-workspaces/       # Per-agent isolation
      <agent-id>/
        IDENTITY.md          # Agent role definition
        SOUL.md              # Behavioral instructions
        TOOLS.md             # Available capabilities
        auth-profiles.json   # Credentials (chmod 600)
    comms/                   # Async messaging
      <agent-id>/
        inbox/
        outbox/
      broadcast.md           # System announcements
    processes/
      PROCESSES.json         # 23 process definitions
    standards/               # Coding, quality, docs, research standards
  skills/                    # Reusable SKILL.md definitions
  memory/
    lancedb/                 # Vector embeddings store
```

## Agent IDs

Sixteen agents map to workspace directories:

| Agent | ID | Role |
|-------|-----|------|
| Cooper | main | Primary orchestrator |
| Pixel | debugger | Debugging specialist |
| Vault | cybersecurity | Security operations |
| Sage | solution-architect | Architecture design |
| Oracle | predictive-analyst | Predictive analysis |
| Nova | nova | General purpose |
| Mirror | metacognition | Self-reflection |
| Vista | business-analyst | Business analysis |
| Forge | implementation | Implementation work |
| Vex | tester | Testing specialist |
| Axon | devops | DevOps operations |
| Vigil | quality-assurance | QA enforcement |
| Anchor | content-specialist | Content creation |
| Muse | creativity | Creative tasks |
| Cipher | knowledge-curator | Knowledge management |
| Lens | multimodal | Multimodal processing |

## Memory Architecture

Three system-level memory types:
- **Episodic** -- Failures and RCA reports
- **Semantic** -- SHARED_KNOWLEDGE.json
- **Procedural** -- PROCESSES.json

Vector embeddings stored in `~/.openclaw/memory/lancedb/`.

> **Full guide:** See `openclaw-memory` skill for the four-layer memory model (bootstrap files, daily logs, session transcripts, retrieval index), shared memory access patterns, SCRIBE compression, and the `/oc-memory` command.

## Key Principles

- Never hardcode absolute paths
- Keep agent data within agent workspaces
- Place shared data in workspace root
- Secure sensitive files with appropriate permissions (chmod 600 for auth)
- Maintain self-contained skills with SKILL.md definitions
- Server parity via `/home/openclaw/` using Tailscale

## When Auditing

To inspect the workspace:

```bash
# Show top-level structure
ls -la ~/.openclaw/

# List agent workspaces
ls ~/.openclaw/workspace/agents-workspaces/

# Check a specific agent's files
ls -la ~/.openclaw/workspace/agents-workspaces/<agent-id>/

# Verify auth file permissions
stat ~/.openclaw/workspace/agents-workspaces/*/auth-profiles.json

# Check shared knowledge
cat ~/.openclaw/workspace/SHARED_KNOWLEDGE.json | head -50

# Inspect communication channels
find ~/.openclaw/workspace/comms/ -type f
```
