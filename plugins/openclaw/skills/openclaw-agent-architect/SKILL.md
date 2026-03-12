---
name: openclaw-agent-architect
description: Create, optimize, and maintain OpenClaw agent workspace files — SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, and GOALS.md. Use this skill whenever the user mentions OpenClaw agent setup, agent personality, agent identity, agent workspace files, SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, GOALS.md, agent persona, "set up my agent", "configure my agent", "make my agent", or wants to scan/optimize/audit an existing OpenClaw workspace. Also trigger when the user wants to create a new agent from scratch, refine an agent's personality, add goals or memory structure, or review workspace files for consistency. This skill conducts targeted interviews, generates production-ready markdown files, and can scan existing workspaces to optimize them.
---

# OpenClaw Agent Architect

Build, configure, and optimize OpenClaw agent workspace files through guided interviews and workspace analysis.

## Overview

OpenClaw agents are defined by markdown files in a workspace directory (default: `~/.openclaw/workspace`). Each file serves a distinct purpose:

| File | Purpose | Loaded When |
|------|---------|-------------|
| **SOUL.md** | Behavioral philosophy, personality, values, communication style, boundaries | Every session (system prompt) |
| **IDENTITY.md** | External presentation — name, emoji, status line | Every session (display layer) |
| **AGENTS.md** | Operating instructions — memory rules, safety, group chat behavior, workflows | Every session + subagent sessions |
| **MEMORY.md** | Long-term persistent memory — learned facts, preferences, project context | Normal sessions only (optional) |
| **GOALS.md** | Active goals, milestones, priorities, progress tracking | Normal sessions (custom addition) |

SOUL.md defines *who* the agent is. IDENTITY.md defines *how it presents*. AGENTS.md defines *how it operates*. MEMORY.md defines *what it knows*. GOALS.md defines *what it's working toward*.

## Workflow

This skill operates in two modes:

### Mode 1: Build from Scratch (Interview → Generate)

When the user wants to create new agent files, conduct a **targeted interview** before generating anything. Do not dump a generic template — ask questions, listen, then craft files that reflect the user's actual needs.

#### Interview Protocol

Run the interview in **phases**. Each phase covers one file. Ask 3-5 focused questions per phase, wait for answers, then generate that file before moving to the next phase. The user can skip phases for files they don't need.

**Phase 1: SOUL.md — Who is your agent?**

Core questions to ask (adapt based on context):
1. What is your agent's primary role? (personal assistant, DevOps bot, research agent, team helper, etc.)
2. What personality traits should it have? (direct, warm, sarcastic, formal, casual, opinionated, cautious)
3. What are 3-5 core values that should guide its decisions? (e.g., "accuracy over speed", "ask before acting on anything destructive", "be concise")
4. What should it NEVER do? (boundaries and anti-patterns)
5. What communication style do you want? (length, tone, emoji usage, humor level, language)

Also ask about:
- Domain expertise the agent should project
- How opinionated vs neutral it should be
- Whether it should push back on the user or be agreeable
- Any anti-sycophancy rules ("skip the Great question!")

**Phase 2: IDENTITY.md — How does it present itself?**

1. What name should the agent use?
2. Should it have an emoji or avatar symbol?
3. What status line or tagline? (shown in chat interfaces)
4. Any identity overrides for specific contexts? (formal name in group chats, casual in DMs)

**Phase 3: AGENTS.md — How does it operate?**

1. What memory management rules should it follow? (when to write to memory, what to remember, what to forget)
2. What safety guardrails are needed? (confirm before deleting, never share credentials, etc.)
3. How should it behave in group chats vs DMs?
4. Are there specific workflows it should follow? (morning briefings, task tracking, report generation)
5. What tools does it have access to, and what rules govern their use?
6. Any operating rules for subagents?

**Phase 4: MEMORY.md — What does it already know?**

1. Who is the user? (name, timezone, role, preferences)
2. What projects or domains should it know about?
3. What preferences has it "learned"? (communication preferences, tool preferences, schedule)
4. Any people/contacts it should know about?
5. What historical context should it start with?

**Phase 5: GOALS.md — What is it working toward?**

1. What are the user's active goals? (professional, personal, project-based)
2. How should goals be structured? (OKR-style, simple checklist, milestone-based)
3. What timeframes matter? (daily, weekly, quarterly, long-term)
4. How should the agent track and report on goal progress?
5. Should the agent proactively nudge toward goals?

#### Generation Rules

After each interview phase, generate the file following these principles:

**SOUL.md generation:**
- Keep under 2,000 words (loaded into every prompt — bloat wastes tokens)
- Start with `# Identity` section (one-line role statement)
- Include `## Core Values` (3-5 values as decision-making frameworks, not platitudes)
- Include `## Communication Style` (explicit tone, length, anti-pattern instructions)
- Include `## Boundaries` (what the agent must NOT do)
- Include `## Context` (persistent domain knowledge the agent needs every session)
- Optionally include `## Vibe` for personality flavor
- Be SPECIFIC. "Be helpful" is useless. "When the user asks a vague question, propose 2-3 interpretations rather than guessing" is useful.
- Anti-sycophancy by default: include "Skip filler phrases like 'Great question!' or 'I'd be happy to help!' — just help."

**IDENTITY.md generation:**
- Use YAML-style key-value pairs
- Keep minimal — name, emoji, status, optional per-context overrides
- Format:
```
name: AgentName
emoji: 🦞
status: Your tagline here
```

**AGENTS.md generation:**
- Structure with clear `##` sections: Memory Management, Safety Rules, Group Chat Behavior, Workflows, Tool Rules
- Memory section should define: when to write, what to remember, what to forget, file naming for daily logs
- Safety section should define: confirmation requirements, data handling, escalation rules
- Be prescriptive — these are operating instructions, not suggestions

**MEMORY.md generation:**
- Structure as knowledge categories: `## User Profile`, `## Projects`, `## Preferences`, `## People`, `## Lessons Learned`
- Use bullet points for scannable facts
- Include timestamps where relevant
- Keep factual and concise — this is a reference document, not prose

**GOALS.md generation:**
- Structure as: `## Active Goals`, `## Milestones`, `## Completed` (archive section)
- Each goal gets: description, priority (P0-P3), target date, current status, next action
- Include a `## Review Schedule` section defining when the agent should check in on goals
- Format goals for easy parsing:
```
### [P1] Goal Title
- **Target**: YYYY-MM-DD
- **Status**: In Progress | Blocked | Complete
- **Next action**: Specific next step
- **Progress**: Brief notes
```

### Mode 2: Scan & Optimize (Existing Workspace)

When the user has existing workspace files, read them all first, then:

1. **Audit for completeness** — check which files exist, which are missing, which are sparse
2. **Check for consistency** — does SOUL.md personality match AGENTS.md operating rules? Do GOALS.md goals align with MEMORY.md context?
3. **Check for bloat** — is SOUL.md over 2,000 words? Are there redundant instructions across files?
4. **Check for vagueness** — flag any instructions that are too generic to produce specific behavior
5. **Check persona coherence** — does the agent have a consistent voice across all files?
6. **Propose improvements** — present specific, actionable suggestions with before/after examples

When optimizing, always:
- Show the user what you're changing and why before writing
- Preserve the user's intent — don't flatten personality into corporate blandness
- Tighten language — every word in SOUL.md costs tokens on every message
- Add missing sections rather than rewriting existing good content
- Ensure GOALS.md reflects the current state (move completed goals to archive)

### Persona Injection

Whether building from scratch or optimizing, the agent's persona should feel **cohesive**. After generating all files, do a final coherence check:

- Does SOUL.md personality naturally produce the communication style described?
- Does IDENTITY.md name/emoji match the personality?
- Do AGENTS.md rules support (not contradict) the soul?
- Does MEMORY.md contain the context the agent needs to fulfill its role?
- Do GOALS.md goals make sense given the agent's purpose?

If anything is misaligned, flag it and propose fixes.

## File Templates

For quick reference, see [references/templates.md](references/templates.md) — contains starter templates for all five files. Use these as scaffolding, never as final output. Every file should be customized through the interview process.

## Important Notes

- **Token budget awareness**: SOUL.md and AGENTS.md are loaded into EVERY prompt. Keep them tight. Long-term knowledge belongs in MEMORY.md or skills, not in the soul.
- **Git-friendly**: All files are plain markdown — encourage users to version-control their workspace.
- **Security**: Never include API keys, passwords, or tokens in any workspace file. SOUL.md and MEMORY.md are common targets for prompt injection attacks (see the ClawHavoc campaign). Recommend `chmod 444` on SOUL.md and IDENTITY.md after finalizing.
- **GOALS.md is custom**: This file is not part of the default OpenClaw workspace. It works because OpenClaw loads all `.md` files from the workspace. Mention this to the user so they understand it's a custom addition that leverages OpenClaw's workspace loading behavior.
- **Iteration is normal**: The best SOUL.md files are rewritten 5-10 times. After a week of use, suggest the user ask their agent: "Based on our interactions, suggest improvements to your SOUL.md."
