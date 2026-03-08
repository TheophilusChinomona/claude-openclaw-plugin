# Multi-Agent Team Configuration Example

Complete copy-paste configuration for a 5-agent team (Commander, Strategist, Engineer, Creator, Think Tank) across Discord + Telegram.

## Full `openclaw.json`

```json5
{
  // === Agents ===
  agents: {
    list: {
      commander: {
        workspace: "workspace-commander",
        requireMention: false,          // global listener in groups
        mentionPatterns: ["@Commander", "@commander", "@cmd"],
        model: "claude-sonnet-4-6",
        tools: { policy: "allow-all" },
      },
      strategist: {
        workspace: "workspace-strategist",
        requireMention: true,           // mention-gated
        mentionPatterns: ["@Strategist", "@strategist", "@strat"],
        model: "claude-sonnet-4-6",
        tools: {
          policy: "allow-list",
          allowed: ["memory_search", "memory_get", "web_search", "web_fetch"],
        },
      },
      engineer: {
        workspace: "workspace-engineer",
        requireMention: true,
        mentionPatterns: ["@Engineer", "@engineer", "@eng"],
        model: "claude-sonnet-4-6",
        tools: { policy: "allow-all" },
        sandbox: { mode: "non-main" },  // sandbox non-main branches
      },
      creator: {
        workspace: "workspace-creator",
        requireMention: true,
        mentionPatterns: ["@Creator", "@creator"],
        model: "claude-sonnet-4-6",
        tools: {
          policy: "allow-list",
          allowed: ["memory_search", "memory_get", "web_search", "web_fetch", "file_write"],
        },
      },
      thinktank: {
        workspace: "workspace-thinktank",
        requireMention: true,
        mentionPatterns: ["@ThinkTank", "@thinktank", "@tt"],
        model: "claude-haiku-4-5",      // lower tier for audit tasks
        tools: {
          policy: "allow-list",
          allowed: ["memory_search", "memory_get", "file_read"],
        },
      },
    },

    // === Bindings (5 roles × 2 channels = 10) ===
    bindings: [
      // Discord
      { channel: "discord", accountId: "acct_commander_discord",  agentId: "commander" },
      { channel: "discord", accountId: "acct_strategist_discord", agentId: "strategist" },
      { channel: "discord", accountId: "acct_engineer_discord",   agentId: "engineer" },
      { channel: "discord", accountId: "acct_creator_discord",    agentId: "creator" },
      { channel: "discord", accountId: "acct_thinktank_discord",  agentId: "thinktank" },
      // Telegram
      { channel: "telegram", accountId: "acct_commander_telegram",  agentId: "commander" },
      { channel: "telegram", accountId: "acct_strategist_telegram", agentId: "strategist" },
      { channel: "telegram", accountId: "acct_engineer_telegram",   agentId: "engineer" },
      { channel: "telegram", accountId: "acct_creator_telegram",    agentId: "creator" },
      { channel: "telegram", accountId: "acct_thinktank_telegram",  agentId: "thinktank" },
    ],
  },

  // === Session Isolation ===
  session: {
    dmScope: "per-account-channel-peer",  // isolate by account + channel + peer
  },

  // === Agent-to-Agent ===
  agentToAgent: {
    maxPingPongTurns: 0,  // prevent infinite loops between agents
  },

  // === Channel Policies ===
  channels: {
    discord: {
      groupPolicy: "open",       // flexible for collaboration
      dmPolicy: "open",
    },
    telegram: {
      groupPolicy: "allowlist",  // restricted production channel
      dmPolicy: "allowlist",
      requireMention: true,
    },
  },
}
```

## Workspace File Structure

Each agent workspace follows this standard skeleton:

```
~/.openclaw/workspace/agents-workspaces/
├── workspace-commander/
│   ├── SOUL.md                    # Role soul: personality, behavior, quality floor
│   ├── AGENTS.md                  # Operational manual: collaboration processes, standards
│   ├── ROLE-COLLAB-RULES.md       # Role-specific collaboration boundaries
│   ├── TEAM-RULEBOOK.md           # Shared hard rules (same across all agents)
│   ├── TEAM-DIRECTORY.md          # Role → account ID mapping
│   ├── IDENTITY.md                # Name, positioning, scope of ability
│   ├── USER.md                    # User preferences, goals, taboos
│   ├── TOOLS.md                   # Permitted tools and boundaries
│   ├── MEMORY.md                  # Long-term memory: stable preferences, decisions
│   ├── GROUP_MEMORY.md            # Group memory: reusable safe info for group context
│   ├── HEARTBEAT.md               # Periodic self-check state
│   └── memory/                    # Daily logs directory
│       ├── 2026-03-01.md
│       ├── 2026-03-02.md
│       └── ...
├── workspace-strategist/
│   └── ... (same skeleton)
├── workspace-engineer/
│   └── ...
├── workspace-creator/
│   └── ...
└── workspace-thinktank/
    └── ...
```

### Shared Files vs Per-Agent Files

| File | Shared? | Notes |
|------|---------|-------|
| TEAM-RULEBOOK.md | Yes — identical across all agents | Unified hard rules |
| TEAM-DIRECTORY.md | Yes — identical across all agents | Role-to-ID mapping |
| SOUL.md | No — unique per agent | Each agent has distinct personality |
| ROLE-COLLAB-RULES.md | No — unique per agent | Each agent has different boundaries |
| MEMORY.md | No — unique per agent | Independent memory stores |
| GROUP_MEMORY.md | No — unique per agent | Agent-specific group context |

## Memory Tiering Strategy

```
Daily Logs (memory/YYYY-MM-DD.md)
  ↓  consolidate stable patterns
Long-term Memory (MEMORY.md)
  ↓  extract group-safe information
Group Memory (GROUP_MEMORY.md)
  ↓  archive when stale
Cold Archive (memory/archive/)
```

**Rules:**
- Daily logs capture task processes, context fragments, and decisions for the day
- Only verified, stable information gets promoted to MEMORY.md
- GROUP_MEMORY.md contains **only** reusable, safe information — never private content
- Cold archive receives old data periodically to prevent active context bloating
- Use `memory_search` + `memory_get` for semantic recall — never load everything at once
- Treat context budget as a resource management problem: tokens are limited, every memory added occupies reasoning space

## Example Commander SOUL.md

```markdown
# Commander — SOUL.md

## Identity
You are the Commander, the central coordinator of a 5-agent collaborative
team. You are the project manager, situational awareness hub, and final
decision-maker.

## Core Responsibilities
- Global situational awareness across all team activities
- Task decomposition and assignment to specialist agents
- Quality control and loop closing after specialist delivery
- Conflict resolution between agents
- Progress tracking and status reporting

## DM Behavior
When in a direct message with a user:
- You are their dedicated strategic advisor
- Provide complete, end-to-end answers
- You don't need to defer to other agents
- Cover analysis, planning, and action items in full

## Group Behavior
When in a group chat:
- **Observe first.** Don't respond to every message
- Capture the situation and assess if collaboration is needed
- Decompose complex requests into specialist tasks
- @mention the right specialist: @Strategist for analysis,
  @Engineer for implementation, @Creator for content, @ThinkTank for audit
- After a specialist delivers, close the loop with a summary
- Intervene strongly only when necessary — don't talk over specialists

## Quality Floor
- Never assign a task without clear acceptance criteria
- Never close a loop without verifying the specialist's output
- Always provide actionable next steps, not vague guidance

## Collaboration Red Lines
- Never attempt technical implementation yourself — delegate to @Engineer
- Never produce external-facing content — delegate to @Creator
- Never skip the audit step for critical decisions — involve @ThinkTank
```
