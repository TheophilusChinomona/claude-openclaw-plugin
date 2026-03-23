---
name: openclaw-persona-architect
description: Research, design, and build complete persona-driven OpenClaw agent workspaces from scratch — including live web research on world-class domain experts, persona mapping, soul architecture design, and full 5-file workspace generation (SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, GOALS.md). Use this skill whenever the user wants to build a new OpenClaw agent with a domain-specific persona, create an AI company or multi-agent team with differentiated personalities, design a soul architecture for an agent role, or asks to "research and build an agent" for any business function. Trigger when the user mentions building agents for sales, marketing, operations, development, SHEQ, finance, HR, content, or any specialist role — even if they don't explicitly say "persona" or "soul". This skill does the full job: researches the world's best practitioners in that domain, extracts their mental models, maps those frameworks onto an agent soul, and outputs production-ready workspace files ready to deploy into OpenClaw.
---

# OpenClaw Persona Architect

Research world-class domain experts, extract their mental models and philosophy, design a persona-driven soul architecture, and generate complete production-ready OpenClaw workspace files — all in one workflow.

## What This Skill Does

Most OpenClaw agents have generic souls. This skill builds agents with **domain-specific cognitive frameworks** drawn from the world's best practitioners in each role. A sales agent built with this skill doesn't just "help with sales" — it thinks like Alex Hormozi, closes like Jordan Belfort (ethical edition), and qualifies like a Straight Line practitioner. A dev agent doesn't just "write code" — it reasons like Elon Musk, applies first principles, and deletes before it builds.

**The output**: A complete, deployable OpenClaw workspace — 5 files, production-ready, tailored to the agent's role, persona, business context, and reporting structure.

---

## Three Entry Points

### Mode 1 — Full Build (research → persona → workspace)
User wants to build an agent from scratch. This skill researches the domain, maps personas, designs the soul, and generates all 5 files.

### Mode 2 — Team Build (org chart → all agents)
User wants a full multi-agent team. This skill designs the org chart, assigns personas, then builds each agent's workspace in sequence.

### Mode 3 — Persona Upgrade (existing agent → persona-enriched)
User has an existing agent with a generic soul. This skill researches an appropriate persona and rewrites the soul files.

---

## Stage 1: Discovery Interview

Before researching or writing, gather context. Adapt questions to what's already known — never ask what the conversation has already answered.

**Core questions (ask only what's missing):**

```
1. What is this agent's primary role? (sales, marketing, ops, dev, SHEQ, finance, HR, etc.)
2. What business does it serve? (industry, size, geography, services)
3. What does "excellent" look like in this role? (any existing standards or benchmarks)
4. Who does this agent report to and who does it manage?
5. What tools/systems does it have access to?
6. What should it NEVER do? (hard limits)
7. What channel does it operate in? (WhatsApp, Telegram, Discord, web)
8. Is there a specific real-world practitioner the user already has in mind?
```

**If building a team:**
```
9. What departments/functions does the business need?
10. What services does the business offer?
11. Who is the human owner/operator (the person the CEO agent reports to)?
```

Confirm understanding before moving to research. State what you're about to research and why.

---

## Stage 2: Domain Research

**This stage is mandatory. Do not skip it. Do not rely solely on training knowledge.**

For each agent role, conduct live web research to identify:

### Research Targets (run web searches — minimum 2 per agent)

**Query templates:**
- `"world's best [role] mindset traits philosophy"`
- `"[known expert name] [role] mental models decision making"`
- `"top [role] practitioners 2024 2025 frameworks"`
- `"what makes a great [role] thinking approach"`

**For each role, research:**
- Who are the 2–3 most respected practitioners globally in this domain?
- What are their core mental models and decision-making frameworks?
- What do they believe that most people in their field get wrong?
- What is their philosophy on doing this work with excellence?
- What specific language, frameworks, or systems are they known for?

**Role → Persona mapping guide (use as starting point — always research to verify and enrich):**

Read `/references/persona-library.md` for the pre-researched persona reference library covering 20+ common business roles. For roles not in the library, conduct fresh research.

### Research Output Format

For each role, synthesise findings into:

```
ROLE: [title]
PRIMARY PERSONA: [Name] — [why this person's philosophy fits this role]
SECONDARY PERSONA: [Name] — [complementary framework]
KEY MENTAL MODELS:
  - [Model name]: [how it applies to this agent's work]
  - [Model name]: [how it applies]
  - [Model name]: [how it applies]
CORE BELIEF: [The one thing this persona believes that shapes everything else]
SIGNATURE FRAMEWORK: [Named process/system this person is known for]
ANTI-PATTERNS: [What this persona would NEVER do in this role]
```

---

## Stage 3: Soul Architecture Design

Map research findings onto the soul architecture. Before writing files, produce a **Soul Architecture Brief**:

```
AGENT: [Name] — [Role]
PERSONA: [Primary] × [Secondary]

CORE VALUES (5 — each a decision-making framework, not a platitude):
1. [Value — with specific application to this role]
2. [Value]
3. [Value]
4. [Value]
5. [Value]

COMMUNICATION STYLE:
- To [reporting agent]: [specific format and tone]
- To [managed agents]: [specific format and tone]
- Tone: [3 adjectives]
- Anti-patterns: [what this agent never says]

HARD LIMITS (NEVER):
- [Limit 1 — specific]
- [Limit 2 — specific]
- [Limit 3 — specific]

SIGNATURE PHRASES/MENTAL MODELS TO EMBED:
- [Specific quote or framework from persona research]
- [Specific quote or framework]

VIBE (one paragraph — the feeling of interacting with this agent):
[prose]
```

Present this brief to the user. Get confirmation or adjustments before writing files.

---

## Stage 4: Generate All 5 Workspace Files

After soul architecture is confirmed, generate all files in sequence. Follow the generation rules below precisely.

### SOUL.md Rules

- Under 2,000 words (every session loads this — bloat wastes tokens)
- Structure:
  ```
  # Identity
  [2-paragraph statement of who this agent is and what soul it's built from]

  ## Core Values
  [5 values — each as a bold titled principle with 2–4 sentences of specific application]

  ## Communication Style
  [Specific — per recipient, tone, format, anti-sycophancy rule]

  ## Boundaries
  [Hard limits — specific, not vague. "Never X" not "avoid X where possible"]

  ## Context
  [Domain knowledge, reporting structure, tools, business context]

  ## Vibe
  [One paragraph — personality, what it feels like to interact with this agent]
  ```
- Embed persona's actual mental models and frameworks — not paraphrases
- Be SPECIFIC. "When uncertain, name it directly" not "be honest"
- Include: "Skip filler phrases like 'Great question!' or 'Certainly!' — just act"
- Reference the persona by name in the Identity section — make the soul explicit

### IDENTITY.md Rules

```yaml
name: [AGENTNAME]
emoji: [single relevant emoji]
status: [Role title] — [one-line tagline that captures the soul]
context_dm: [mode name — what this agent is doing in direct messages]
context_group: [mode name — what this agent is doing in group channels]
tagline: "[Signature phrase — from persona research or synthesised from soul]"
```

### AGENTS.md Rules

- Structure with `##` sections: Role & Ownership, Workflows (one per domain), Memory Management, Safety Rules, Escalation Rules, Tool Access
- **Workflows are the core value** — each workflow gets:
  - Step-by-step process (numbered)
  - Format templates for all structured outputs (status updates, reports, briefs)
  - Decision rules (when to act vs escalate)
- Make it prescriptive — "follow these steps" not "consider doing this"
- Include a tool access table with: Tool | Access Level (✅ Autonomous / ⚠️ Confirm / ❌ Never) | Notes
- Report templates must be copy-paste ready — real format, real structure

### MEMORY.md Rules

- Pre-seed with all known context from the interview
- Structure: User Profile → Business Context → Active [Domain] Data → Key Contacts → Lessons Learned
- Use tables for structured data (client lists, pipelines, registries)
- Mark fields Tino needs to fill: `[Tino to confirm]`
- Include: timestamps, status fields, and "last updated" header

### GOALS.md Rules

- Note at top: "GOALS.md is a custom OpenClaw file — loaded because OpenClaw reads all .md files in workspace"
- Structure: Review Schedule → Active Goals → Milestones table → Completed Goals
- Each goal format:
  ```
  ### [P0/P1/P2/P3] Goal Title
  - **Target**: [date or quarter]
  - **Status**: [In Progress / Not started / Planned / Monitoring]
  - **Next action**: [specific immediate next step]
  - **Success metric**: [measurable — not vague]
  ```
- P0 = must-have for basic function; P1 = important; P2 = valuable; P3 = aspirational
- Include completed goals section — pre-populate with anything already done

---

## Stage 5: Package and Security

After all 5 files are generated:

1. Produce a deployment block:
```bash
mkdir -p ~/.openclaw/workspace-[agentid]
cp [agent]-workspace/* ~/.openclaw/workspace-[agentid]/
chmod 444 ~/.openclaw/workspace-[agentid]/SOUL.md
chmod 444 ~/.openclaw/workspace-[agentid]/IDENTITY.md
```

2. Produce an openclaw.json snippet:
```json
{
  "agents": {
    "list": [
      {
        "id": "[agentid]",
        "workspace": "~/.openclaw/workspace-[agentid]",
        "model": "[claude-opus-4-6 / claude-sonnet-4-6 / claude-haiku-4-5-20251001]",
        "heartbeat": {
          "every": "[interval]",
          "message": "[specific heartbeat instruction — what to check/do]"
        }
      }
    ]
  }
}
```

3. Model selection guidance:
   - Claude Opus: CEO/strategic agents requiring complex reasoning
   - Claude Sonnet: Department heads and specialists requiring strong capability
   - Claude Haiku: Monitoring agents, high-frequency agents, simple specialist tasks

4. Package all files into a zip named `[AGENTNAME]-workspace.zip`

---

## Team Build Mode (Multiple Agents)

When building a multi-agent team:

### Step 1: Design the org chart first

Produce a structured org chart showing:
- Tier 1: Command (CEO agent)
- Tier 2: Department heads
- Tier 3: Specialist agents
- Reporting lines
- Model assignment per agent
- Persona assignment per agent

Present the org chart for approval before building any workspaces.

### Step 2: Build in dependency order

Always build top-down:
1. CEO/orchestrator first (sets the standard all others calibrate to)
2. Infrastructure/monitoring second (watching from day one)
3. Operations backbone third
4. Department heads fourth (in business priority order)
5. Specialist agents last

### Step 3: Cross-reference memory

Each agent's MEMORY.md must be consistent with other agents:
- Agent registries match across agents
- Client data is consistent
- Reporting lines match in both directions
- No agent references another agent that hasn't been defined

### Step 4: Deliver a master deployment guide

After all agents are built, produce a single deployment guide:
```markdown
# [Company Name] AI Agent Ecosystem — Deployment Guide

## Build Order
[numbered list with rationale]

## Deploy Each Agent
[deployment commands per agent]

## Heartbeat Configuration
[openclaw.json with all agents]

## First-Run Checklist
- [ ] APEX activated and daily briefing flowing
- [ ] SENTINEL heartbeat confirmed
- [ ] NEXUS client files populated
- [ ] [etc.]
```

---

## Quality Standards

Before delivering any workspace:

**SOUL.md check:**
- [ ] Persona named explicitly in Identity section
- [ ] 5 core values are decision-making frameworks, not platitudes
- [ ] Communication style specifies format per recipient
- [ ] Hard limits are specific ("never X" not "avoid X")
- [ ] Vibe paragraph conveys a distinct personality
- [ ] Under 2,000 words

**AGENTS.md check:**
- [ ] All workflows have numbered steps
- [ ] All report formats are templates (copy-paste ready)
- [ ] Tool access table is complete
- [ ] Escalation rules specify conditions precisely

**MEMORY.md check:**
- [ ] Pre-seeded with all known context
- [ ] Fields marked for human input: `[User to confirm]`
- [ ] Consistent with other agents in team (if team build)

**GOALS.md check:**
- [ ] Custom file note present
- [ ] All goals have success metrics (measurable)
- [ ] Completed goals section populated

**Coherence check:**
- [ ] Does SOUL.md personality naturally produce the communication style described?
- [ ] Does IDENTITY.md tagline match the soul?
- [ ] Do AGENTS.md rules support (not contradict) the soul?
- [ ] Do GOALS.md goals make sense for this agent's role?

---

## Important Notes

- **Research is not optional** — generic souls produce generic agents. Always research before writing.
- **Token budget awareness** — SOUL.md and AGENTS.md load every session. Keep them tight. Long-term knowledge belongs in MEMORY.md.
- **Security** — Never include API keys, passwords, or tokens in any workspace file. Remind users to `chmod 444` SOUL.md and IDENTITY.md after deployment.
- **Iteration is normal** — The best SOUL.md files are rewritten after a week of use. After deployment, suggest: "Ask your agent: 'Based on our interactions, what would you change in your SOUL.md?'"
- **GOALS.md is custom** — Not part of default OpenClaw workspace. Works because OpenClaw loads all `.md` files in workspace directory.

Read `references/persona-library.md` for pre-researched personas across 20+ business roles before conducting fresh research — it may already have what you need.
