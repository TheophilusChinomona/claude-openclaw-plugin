---
name: openclaw-multi-agent-team-setup
description: >
  Use when the user wants to build a multi-agent team, set up agent
  collaboration, configure commander-specialist routing, orchestrate group
  chat with multiple agents, set up mention gating for agent teams,
  configure dual-channel multi-agent, or build an agent operating system
  in OpenClaw.
---

# Building a Multi-Agent Team in OpenClaw

End-to-end guide for turning a single OpenClaw gateway into a collaborative multi-agent operating system. Based on real-world patterns from production multi-agent deployments.

> **Prerequisite skills:** This guide builds on concepts from `openclaw-multi-agent` (config syntax, bindings), `openclaw-agent-teams` (SOUL.md authoring, hierarchy design, memory architecture), and `openclaw-sessions` (session mechanics). Reference those skills for deeper coverage of individual topics.

## Overview: What Is an "Agent OS"?

An Agent OS is a single OpenClaw gateway running multiple agents with:
- **Independent workspaces** — each agent has its own personality, rules, memory, and sessions
- **Deterministic routing** — messages reach the right agent via explicit bindings, not guesswork
- **Collaboration rules** — agents work together through structured protocols, not free-form chat
- **Dual-track governance** — config-layer hard constraints + prompt-layer behavioral guidance

Example 5-role team:

| Role | Responsibility | Model Tier | Tool Access |
|------|---------------|------------|-------------|
| **Commander** | Situational awareness, task decomposition, assignment, closing | High (claude-sonnet-4-6+) | Full |
| **Strategist** | Strategic analysis, risk prediction, scheme evaluation | High | Read-heavy |
| **Engineer** | Code implementation, system maintenance, technical execution | High | Full + exec |
| **Creator** | Content creation, expression optimization, external output | Mid | Write + web |
| **Think Tank** | Knowledge auditing, quality control, compliance checks | Mid | Read-only |

**Start with 3 roles**, validate the routing and collaboration patterns, then add incrementally. Going from 1 to 5 agents at once multiplies debugging surface.

## Architecture

```
Single Gateway Process
├── Channel Connectors (Discord, Telegram, ...)
│   └── Bindings (channel + accountId → agentId)
├── Agent 1: Commander
│   ├── Workspace (SOUL.md, AGENTS.md, rules, memory)
│   ├── State directory (auth, config)
│   └── Session store (isolated per scope)
├── Agent 2: Strategist
│   └── ... (independent workspace, state, sessions)
├── Agent 3: Engineer
│   └── ...
├── Agent 4: Creator
│   └── ...
└── Agent 5: Think Tank
    └── ...
```

**Why one gateway** (not 5 separate services):
- **Centralized maintenance** — one process to monitor, restart, update
- **Unified configuration** — single `openclaw.json` manages global strategy
- **Collaboration foundation** — agents in the same runtime can coordinate efficiently

## Step 1: Define Roles

Choose roles with **clear, non-overlapping responsibilities**. Each role should have a distinct expertise domain and a clear answer to "when does this agent get involved?"

Guidelines:
- Every role must have a unique value — if two roles overlap heavily, merge them
- Assign model tiers by cognitive demand (complex reasoning → higher tier)
- Tool access follows least privilege — only grant what the role needs
- Name roles by function, not personality (Commander, not "Bob")

## Step 2: Create Agents & Workspaces

Create each agent with its own workspace:

```bash
openclaw agents add commander
openclaw agents add strategist
openclaw agents add engineer
openclaw agents add creator
openclaw agents add thinktank
```

Each agent gets an independent workspace directory under `~/.openclaw/workspace/agents-workspaces/`. Verify:

```bash
openclaw agents list --bindings
```

In `openclaw.json`, the agents block looks like:

```json5
{
  agents: {
    list: {
      commander:  { workspace: "workspace-commander" },
      strategist: { workspace: "workspace-strategist" },
      engineer:   { workspace: "workspace-engineer" },
      creator:    { workspace: "workspace-creator" },
      thinktank:  { workspace: "workspace-thinktank" },
    }
  }
}
```

> See `openclaw-multi-agent` for full agent config options including sandbox mode, scope, and tool policies.

## Step 3: Routing with Bindings

Use explicit bindings to map `channel + accountId → agentId`. This is the "triage desk" — the system decides who handles each message at the entry layer.

For a 5-agent team across Discord + Telegram (10 bindings):

```json5
{
  agents: {
    bindings: [
      // Discord bindings
      { channel: "discord", accountId: "account_commander",  agentId: "commander" },
      { channel: "discord", accountId: "account_strategist", agentId: "strategist" },
      { channel: "discord", accountId: "account_engineer",   agentId: "engineer" },
      { channel: "discord", accountId: "account_creator",    agentId: "creator" },
      { channel: "discord", accountId: "account_thinktank",  agentId: "thinktank" },
      // Telegram bindings
      { channel: "telegram", accountId: "account_commander",  agentId: "commander" },
      { channel: "telegram", accountId: "account_strategist", agentId: "strategist" },
      { channel: "telegram", accountId: "account_engineer",   agentId: "engineer" },
      { channel: "telegram", accountId: "account_creator",    agentId: "creator" },
      { channel: "telegram", accountId: "account_thinktank",  agentId: "thinktank" },
    ]
  }
}
```

**Why route at the entry layer?** If you let all agents hear every message and decide who responds, group chat becomes chaotic. Explicit bindings ensure deterministic routing.

> See `openclaw-multi-agent` for binding priority rules (peer match > parent peer > guild/roles > guild > team > account > channel > default).

## Step 4: Session Isolation

Set the recommended session scope for multi-agent, multi-account scenarios:

```json5
{
  session: {
    dmScope: "per-account-channel-peer"
  }
}
```

This isolates private chat context by three dimensions: **Account + Channel + Peer User**.

Why `per-account-channel-peer`:
- Same user contacting the same role via Discord and Telegram → contexts don't mix
- Different users contacting the same role → contexts completely isolated
- Multi-agent/multi-account scenarios → minimal cross-contamination risk

This is the official recommended strategy for multi-account scenarios.

> See `openclaw-sessions` for full session mechanics including reset modes, compaction, thread bindings, and identity links.

## Step 5: Group Chat Orchestration

This is the core collaboration pattern. The strategy: **Commander listens globally, specialists triggered by @mention**.

### Commander: Global Listener

```json5
{
  agents: {
    list: {
      commander: {
        requireMention: false,  // sees ALL group messages
        mentionPatterns: ["@Commander", "@commander", "@cmd"],
      }
    }
  }
}
```

The Commander acts as project manager — captures the situation, decomposes tasks, @mentions the right specialist, and closes the loop.

### Specialists: Mention-Gated

```json5
{
  agents: {
    list: {
      strategist: {
        requireMention: true,   // only responds when @mentioned
        mentionPatterns: ["@Strategist", "@strategist", "@strat"],
      },
      engineer: {
        requireMention: true,
        mentionPatterns: ["@Engineer", "@engineer", "@eng"],
      },
      creator: {
        requireMention: true,
        mentionPatterns: ["@Creator", "@creator"],
      },
      thinktank: {
        requireMention: true,
        mentionPatterns: ["@ThinkTank", "@thinktank", "@tt"],
      },
    }
  }
}
```

### Prevent Agent-to-Agent Loops

```json5
{
  agentToAgent: {
    maxPingPongTurns: 0   // prevents infinite "Thank you" / "You're welcome" loops
  }
}
```

This is **critical**. Without it, two agents can get stuck in an infinite loop of pleasantries. Setting to `0` means agents don't automatically ping each other — all inter-agent coordination goes through the Commander's explicit @mentions.

### The Collaboration Flow

1. User asks a question in the group
2. Commander captures the situation (global listener)
3. Commander decomposes the task and @mentions the relevant specialist
4. Specialist delivers their expertise
5. Commander closes the loop with a summary

Result: Group discussions become **controlled relay**, not free-form scattering.

## Step 6: Dual-Track Governance

You need **both** configuration-layer constraints and prompt-layer guidance. Models drift and forget rules — config prevents, prompts guide. Double insurance.

### Config Track (Hard Constraints)

These are platform-level controls that the model **cannot** override:

| Setting | Purpose |
|---------|---------|
| `groupPolicy` | Controls who can interact in groups (open, allowlist) |
| `dmPolicy` | Controls DM access |
| `requireMention` | Determines if agent needs @mention to respond |
| `bindings` | Deterministic message routing |
| `dmScope` | Session isolation granularity |
| `maxPingPongTurns` | Caps agent-to-agent loops |
| Tool policies | Per-agent tool restrictions |

### Prompt Track (Soft Guidance)

These are rule files inside each agent's workspace that shape behavior:

| File | Purpose |
|------|---------|
| **SOUL.md** | Role soul — personality, tone, responsibilities, quality floor |
| **AGENTS.md** | Operational manual — collaboration processes, memory standards, checklists |
| **ROLE-COLLAB-RULES.md** | Role-specific collaboration boundaries and red lines |
| **TEAM-RULEBOOK.md** | Unified hard rules for the team (shared across all roles) |
| **TEAM-DIRECTORY.md** | Maps role names to real account IDs to prevent @mention errors |

**Why both tracks?** The config track limits flow (who can talk, where, how often). The prompt track constrains action (what to say, how to behave, what quality means). Neither alone is sufficient.

## Step 7: DM vs Group Behavior

Define in each agent's `SOUL.md` how it behaves differently in DMs vs group chat. This is often overlooked but critical — a role should not act the same way in both contexts.

### DM Mode
- Agent acts as an **end-to-end expert** solving the user's problem
- No collaboration process needed — provide the full answer directly
- Standard: "one agent can handle it"

### Group Mode
- Follow **team relay protocol** — handle only your area of expertise
- Commander orchestrates, specialists deliver, Commander closes
- Each role contributes its specific value, not a full answer

### Per-Role Behavioral Examples

In SOUL.md, define sections for each mode:

```markdown
## DM Behavior
When in a direct message, you are the user's dedicated [role]. Provide
complete, end-to-end answers. You don't need to defer to other agents.

## Group Behavior
When in a group chat, follow the relay protocol:
- Wait for Commander's @mention before acting
- Handle ONLY your domain of expertise
- Keep responses focused and actionable
- Don't repeat what other agents have said
```

**Commander** specifics:
- DM: Full strategic advisor, handles everything
- Group: Stays observant by default, intervenes strongly only when necessary to avoid talking over specialists

**Engineer** specifics:
- DM: Full technical expert, complete solutions
- Group: Deliverables must be executable, verifiable, and rollback-capable — not just ideas

**Strategist** specifics:
- DM: Full analyst, covers all angles
- Group: Conclusions must include hypotheses and verification paths — not just guesses

**Think Tank** specifics:
- DM: Full auditor, comprehensive review
- Group: Audits must provide problem classification + repair plans — not just "there's a problem"

**Creator** specifics:
- DM: Full content expert, end-to-end output
- Group: Expression must not sacrifice authenticity or executability — shouldn't just "look good"

## Common Pitfalls

### Agent-to-Agent Infinite Loops
**Problem:** Two agents get stuck in an endless exchange of pleasantries.
**Fix:** Set `agentToAgent.maxPingPongTurns: 0` to suppress automatic back-and-forth.

### Context Cross-Contamination
**Problem:** User A's private chat leaks into User B's replies, or Discord context pollutes Telegram.
**Fix:** Use `session.dmScope: "per-account-channel-peer"` for full three-dimensional isolation.

### All Agents Responding in Groups
**Problem:** Every agent replies to every message, creating chaos.
**Fix:** Set `requireMention: true` for all specialists. Only the Commander should have `requireMention: false`.

### Workspace Pollution
**Problem:** Agent personality, memory, or rules bleed between agents.
**Fix:** Each agent must have an independent workspace. Never share workspace directories between agents.

### Starting with Too Many Agents
**Problem:** Debugging 5 agents at once is exponentially harder than debugging 3.
**Fix:** Start with 3 roles (e.g., Commander + 2 specialists). Validate routing and collaboration before adding more.

## Cross-References

- **`openclaw-multi-agent`** — Config syntax for agents, bindings, per-agent sandbox/scope/tool policies
- **`openclaw-agent-teams`** — SOUL.md authoring templates, hierarchy design patterns, memory architecture (daily logs → MEMORY.md → team memory)
- **`openclaw-sessions`** — Full session mechanics: dmScope options, reset modes, compaction, thread bindings, identity links
