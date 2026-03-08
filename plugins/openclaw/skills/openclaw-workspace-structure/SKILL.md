---
description: >
  Use when the user wants to understand the OpenClaw workspace layout, inspect ~/.openclaw/ structure,
  audit agent workspaces, check workspace conventions, understand file-based orchestration,
  view agent directory organization, or troubleshoot workspace paths.
---

# OpenClaw Workspace Structure

Explain and help the user navigate the standardized OpenClaw workspace layout rooted at `~/.openclaw/`.

## Core Directory Layout

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

Three memory types:
- **Episodic** -- Failures and RCA reports
- **Semantic** -- SHARED_KNOWLEDGE.json
- **Procedural** -- PROCESSES.json

Vector embeddings stored in `~/.openclaw/memory/lancedb/`.

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
