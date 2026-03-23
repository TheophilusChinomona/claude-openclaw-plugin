---
name: openclaw-agent-planner
description: Brainstorm, design, and document OpenClaw agents and multi-agent teams. Use this skill whenever the user wants to plan what agents to build, figure out what agents they need, design agent capabilities and permissions, plan a multi-agent architecture, decide how agents should work together, or create documentation for their agent team. Also trigger when the user says things like "what agents do I need", "help me plan my agents", "I want to set up multiple agents", "document my agent", "agent permissions", "agent roles", "agent team", or asks about agent capabilities, responsibilities, tool access, or inter-agent communication. This skill produces a comprehensive Agent Team Documentation package (markdown + optional .docx) covering every agent's role, persona, permissions, tools, boundaries, and team interaction rules.
---

# OpenClaw Agent Planner

Brainstorm, design, and fully document OpenClaw agents — from a single personal assistant to a coordinated multi-agent team.

## Why This Skill Exists

Most people start with one agent and eventually realize they need several — a personal assistant, a DevOps bot, a research agent, a sales development agent, etc. The hard part isn't installing them; it's **deciding what each one does, what it's allowed to do, and how they interact**. This skill walks through that design process and produces real documentation at the end.

## Workflow Overview

The skill runs in three stages:

```
Stage 1: Discovery    →  Understand the user's world (roles, tools, workflows, pain points)
Stage 2: Design       →  Brainstorm agents, define capabilities, draw boundaries
Stage 3: Document     →  Produce comprehensive Agent Team Documentation
```

Each stage is interactive — ask questions, listen, synthesize, confirm, iterate.

---

## Stage 1: Discovery — Understanding the User's World

Before proposing any agents, understand the landscape. Ask questions across these dimensions:

### 1.1 Role & Context

- What do you do? (job title, industry, daily responsibilities)
- What teams or people do you work with?
- What's your tech stack and tooling? (platforms, services, communication channels)
- What recurring workflows eat your time?

### 1.2 Pain Points & Automation Appetite

- What tasks do you wish someone else would handle?
- What falls through the cracks regularly?
- Where do you lose time to context-switching?
- What would you trust an AI agent to do unsupervised? What would you NOT trust it with?

### 1.3 Existing Setup

- Do you already have any OpenClaw agents running? If so, what do they do?
- What channels are you using? (WhatsApp, Telegram, Discord, iMessage, web)
- What tools/MCP servers do you have access to? (calendar, email, web search, file systems, APIs)
- Any existing automation (cron jobs, scripts, Zapier, n8n)?

### 1.4 Constraints

- Budget sensitivity? (model costs — Claude Opus vs Sonnet vs Haiku for different agents)
- Security requirements? (data handling, credential access, network boundaries)
- Uptime needs? (always-on vs on-demand)
- Who else will interact with these agents? (just you, your team, clients, public?)

Adapt the questions to what you already know about the user. Don't ask things you can infer from context. If the user has shared their background before, build on it rather than re-interviewing from zero.

---

## Stage 2: Design — Brainstorming & Defining Agents

Now synthesize Discovery into an agent architecture. This stage has sub-steps:

### 2.1 Agent Brainstorm

Based on what you learned, propose a list of potential agents. For each agent, provide:

- **Name**: A short, memorable name (not "Agent 1")
- **One-line role**: What this agent does in one sentence
- **Why it exists**: What pain point or workflow it addresses
- **Channel**: Where it lives (WhatsApp DM, group chat, Discord server, etc.)

Present the brainstorm as a table for easy scanning:

```
| Agent Name | Role | Why | Channel |
|------------|------|-----|---------|
| Atlas      | Personal assistant — calendar, tasks, daily briefing | Replaces manual morning routine | WhatsApp DM |
| Sentinel   | DevOps monitoring — alerts, deploys, health checks | Catches issues before they escalate | Discord #ops |
| Scout      | Sales lead research — prospect analysis, outreach drafts | Automates top-of-funnel research | WhatsApp DM |
```

Then discuss with the user:
- Which agents are must-haves vs nice-to-haves?
- Are any agents doing overlapping things? Should they merge?
- Are there gaps — workflows not covered by any agent?
- What's the priority order for building them?

### 2.2 Capability Mapping

For each confirmed agent, define its capabilities in detail:

**Tools & Permissions Matrix**

For every agent, specify:
- What tools it CAN use (web search, file system, calendar, email, shell commands, MCP servers, APIs)
- What tools it CANNOT use (explicit denials — just as important as grants)
- What actions require confirmation from the user before executing
- What actions it can take autonomously
- Rate limits or usage constraints

Format as a permission matrix:

```
| Capability | Access Level | Notes |
|-----------|-------------|-------|
| Web search | ✅ Autonomous | No limit |
| File read | ✅ Autonomous | Workspace only |
| File write | ⚠️ Confirm | Confirm before overwriting |
| File delete | ❌ Denied | Never — user does this manually |
| Send messages | ⚠️ Confirm | Confirm recipient + content |
| Shell commands | ⚠️ Confirm | Read-only commands autonomous; writes confirm |
| Calendar read | ✅ Autonomous | Full access |
| Calendar write | ⚠️ Confirm | Confirm before creating/modifying events |
| API calls | ✅ Autonomous | Rate limit: 10/minute |
```

Access levels:
- ✅ **Autonomous**: Agent can do this without asking
- ⚠️ **Confirm**: Agent must ask user before executing
- ❌ **Denied**: Agent must never do this
- 🔒 **Restricted**: Only during specific workflows or with specific triggers

**Behavioral Boundaries**

For each agent, define:
- What it should NEVER do (hard boundaries)
- What it should ALWAYS do (invariant behaviors)
- Escalation rules: when should it hand off to the user or another agent?
- Failure modes: what does it do when things go wrong?

### 2.3 Inter-Agent Design (Multi-Agent Teams)

If the user has multiple agents, define how they interact:

- **Communication**: Can agents message each other? Through what channel?
- **Delegation**: Can one agent spawn tasks for another? Which ones?
- **Shared context**: Do agents share a workspace? Separate workspaces? Shared AGENTS.md with unique SOUL.md files?
- **Conflict resolution**: If two agents have overlapping scope, who takes priority?
- **Information flow**: Draw the information flow between agents

Recommend the OpenClaw multi-agent pattern:
```json
{
  "agents": {
    "list": [
      { "id": "atlas", "workspace": "~/.openclaw/workspace-atlas" },
      { "id": "sentinel", "workspace": "~/.openclaw/workspace-sentinel" },
      { "id": "scout", "workspace": "~/.openclaw/workspace-scout" }
    ]
  }
}
```
Each agent gets its own workspace (and therefore its own SOUL.md, MEMORY.md, etc.) while sharing a common AGENTS.md for team-wide operating rules.

### 2.4 Model Selection

Help the user choose the right model for each agent based on task complexity and cost:

| Task Profile | Recommended Model | Why |
|-------------|------------------|-----|
| Complex reasoning, writing, strategy | Claude Opus | Highest capability, highest cost |
| General assistance, coding, daily tasks | Claude Sonnet | Best balance of capability and cost |
| Simple lookups, routing, triage | Claude Haiku | Fast, cheap, good for high-volume |
| Heartbeats, status checks | Claude Haiku | Minimal cost for periodic pings |

Agents can use different models. A personal assistant might use Opus for morning briefings but Haiku for heartbeats. Surface this option.

---

## Stage 3: Document — Agent Team Documentation

After Stage 2 is confirmed, produce a comprehensive **Agent Team Documentation** package. This is the primary deliverable of this skill.

### Documentation Structure

Generate a single markdown document (and optionally a .docx using the docx skill) with this exact structure:

```
# Agent Team Documentation
## Generated: [DATE]
## Owner: [USER NAME]

---

## 1. Team Overview

### 1.1 Purpose
[Why this agent team exists — what problem it solves for the user]

### 1.2 Architecture Diagram
[Text-based diagram showing agents, channels, and information flow]

### 1.3 Agent Roster
[Table: Agent Name | Role | Model | Channel | Status (Active/Planned)]

---

## 2. Agent Profiles

### 2.1 [Agent Name]

#### Role & Purpose
[2-3 sentences: what this agent does and why it exists]

#### Persona Summary
- **Personality**: [Key personality traits from SOUL.md design]
- **Communication style**: [How it talks]
- **Identity**: [Name, emoji, tagline from IDENTITY.md design]

#### Capabilities & Permissions

| Capability | Access Level | Conditions |
|-----------|-------------|------------|
| [Tool/action] | ✅/⚠️/❌/🔒 | [When/how] |

#### Behavioral Boundaries
- **NEVER**: [Hard prohibitions]
- **ALWAYS**: [Invariant behaviors]
- **ESCALATE WHEN**: [Handoff triggers]

#### Workflows
| Workflow | Trigger | Steps | Output |
|---------|---------|-------|--------|
| [Name] | [What triggers it] | [Key steps] | [What it produces] |

#### Memory Strategy
- **Remembers**: [What this agent tracks long-term]
- **Forgets**: [What it doesn't persist]
- **Shares**: [What context flows to/from other agents]

#### Goals
[Active goals this agent is responsible for tracking/advancing]

#### Configuration Snippet
```json
{
  "id": "[agent-id]",
  "workspace": "~/.openclaw/workspace-[id]",
  "model": "[model]",
  "heartbeat": { "every": "[interval]" }
}
```

[Repeat section 2.x for each agent]

---

## 3. Team Interaction Rules

### 3.1 Inter-Agent Communication
[How agents communicate — shared channels, delegation rules, message routing]

### 3.2 Shared vs Isolated Resources
[What's shared (AGENTS.md, tools) vs isolated (SOUL.md, MEMORY.md, workspaces)]

### 3.3 Conflict Resolution
[What happens when agents have overlapping scope]

### 3.4 Escalation Matrix
| Situation | Escalates To | Method |
|-----------|-------------|--------|
| [Scenario] | [Agent or User] | [How] |

---

## 4. Security & Governance

### 4.1 Permission Summary
[Consolidated permission matrix across all agents]

### 4.2 Data Handling Rules
[What data each agent can access, store, share, or transmit]

### 4.3 Credential Access
[Which agents have access to which credentials/API keys]

### 4.4 Audit & Monitoring
[How agent actions are logged and reviewed]

### 4.5 Hardening Recommendations
[chmod 444 on identity files, git backup, etc.]

---

## 5. Implementation Roadmap

### 5.1 Build Order
[Priority-ordered list of agents to build, with dependencies]

### 5.2 Phase 1: [First Agent]
- [ ] Create workspace
- [ ] Write SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, GOALS.md
- [ ] Configure openclaw.json
- [ ] Test in isolated channel
- [ ] Go live

### 5.3 Phase 2: [Second Agent]
[Same structure]

[Continue for each phase]

---

## 6. Appendix

### 6.1 OpenClaw Configuration Reference
[Relevant openclaw.json snippets for the full team setup]

### 6.2 Workspace File Map
[Directory tree showing all agent workspaces and their files]

### 6.3 Glossary
[Terms used in this document: agent, workspace, soul, heartbeat, skill, etc.]
```

### Output Format Rules

- Generate the documentation as a markdown file saved to the workspace
- If the user wants a .docx, use the docx skill to produce a professionally formatted Word document with table of contents, headers, page numbers, and tables
- The document should be **self-contained** — someone unfamiliar with OpenClaw should be able to read it and understand the agent team
- Include the generation date and mark it as a living document that should be updated as agents evolve
- The architecture diagram should use simple ASCII/text art that renders in any markdown viewer

### Quality Checks Before Delivery

Before presenting the final documentation, verify:

1. **Completeness**: Every agent discussed in Stage 2 has a full profile in Section 2
2. **Consistency**: Permission levels match across the summary table and individual profiles
3. **No orphan references**: Every agent mentioned in team interaction rules is defined in Section 2
4. **Actionable roadmap**: Build order has concrete steps, not vague "set up agent" placeholders
5. **Security covered**: No agents have unconstrained permissions without justification
6. **Persona coherence**: Each agent's persona summary aligns with its role (a DevOps bot shouldn't have a "warm and bubbly" persona unless the user specifically wants that)

---

## Integration with openclaw-agent-architect

This skill designs the **what** and **why**. The `openclaw-agent-architect` skill builds the **how** — the actual SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, and GOALS.md files.

Recommended workflow:
1. Use **openclaw-agent-planner** (this skill) to brainstorm and document the agent team
2. Use **openclaw-agent-architect** to generate the workspace files for each agent, using the Agent Team Documentation as input

When handing off to openclaw-agent-architect, pass the relevant agent profile section so the architect skill has full context on the agent's role, persona, permissions, and goals.

---

## Examples

### Example 1: Solo Consultant

**Discovery**: SHEQ consultant, works with multiple clients, needs help with document management, lead generation, and daily scheduling.

**Brainstorm output**:
| Agent | Role | Why | Channel |
|-------|------|-----|---------|
| Nexus | Personal assistant — calendar, tasks, briefings, document drafts | Central coordination for daily workflow | WhatsApp DM |
| Hunter | Sales development — prospect research, outreach, lead tracking | Automates top-of-funnel BD across LinkedIn/email | WhatsApp DM |
| Watchdog | Infrastructure monitor — server health, deployment status | Catches Dokploy/server issues before they escalate | Discord #ops |

### Example 2: Small Development Team

**Discovery**: 4-person startup, building a SaaS product, needs help with code review, project management, and customer support.

**Brainstorm output**:
| Agent | Role | Why | Channel |
|-------|------|-----|---------|
| Archie | Engineering assistant — code review, PR summaries, tech debt tracking | Reduces review bottleneck | Discord #engineering |
| PM-Bot | Project management — sprint tracking, standup summaries, blocker alerts | Keeps team aligned without manual overhead | Discord #standups |
| Support | Customer support triage — ticket classification, draft responses, escalation | Handles L1 support, escalates complex issues | Discord #support |

---

## Handling Edge Cases

- **User only needs one agent**: That's fine — skip the multi-agent design sections, but still produce full documentation for the single agent. The documentation is valuable even for one agent.
- **User is unsure what they need**: Lean harder into Stage 1 Discovery. Ask more questions. Propose a minimal starter setup (1-2 agents) and note "future candidates" in the roadmap.
- **User already has agents running**: Start with an audit. Read their existing workspace files, map what exists, then identify gaps and propose additions/changes.
- **User wants to reorganize existing agents**: Treat as a refactoring exercise. Document the current state, propose the target state, and create a migration plan.
