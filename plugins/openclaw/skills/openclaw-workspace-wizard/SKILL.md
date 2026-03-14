---
name: openclaw-workspace-wizard
description: Full guided journey to create a complete OpenClaw agent workspace from scratch. Chains discovery, memory design, persona crafting, workspace scaffolding, and quality audit into a single orchestrated flow with checkpoints. Use when the user says "create my agent from scratch", "full agent setup", "build a complete agent", "new openclaw agent", "workspace wizard", "guided agent creation", or "walk me through creating an agent". This is the comprehensive path — for quick single-file edits use openclaw-agent-architect instead.
---

# OpenClaw Workspace Wizard

The full guided journey for creating a production-ready OpenClaw agent workspace. Chains six phases with user checkpoints between each, so you can pause, adjust, and resume at any point.

## Overview

This wizard orchestrates the complete lifecycle:

```
Phase 1: Discovery     → What agent do you need?
Phase 2: Memory Design → How should it remember?
Phase 3: Soul Design   → Who is this agent?
Phase 4: Workspace     → What files and structure?
Phase 5: Scaffolding   → Generate everything
Phase 6: Quality Audit → Score and improve
```

Each phase produces artifacts that feed the next. You can skip phases if you already have the artifacts (e.g., skip Discovery if you already know exactly what you want).

## Phase 0: Welcome and Setup

### Configuration

Determine workspace settings:

1. **Workspace name**: What should this agent be called? (working title — can change later)
2. **Workspace mode**: Single agent or multi-agent team?
3. **Workspace location**: Where to create the workspace?
   - Default: `~/.openclaw/workspace/` (single-agent)
   - Multi-agent: `~/.openclaw/agents-workspaces/<agent-id>/`
   - Custom path if user prefers

### Resume Detection

Check the workspace location for existing artifacts:
- Discovery reports, memory architecture docs, SOUL.md drafts
- If found, present them and offer: **[R]** Resume from last checkpoint, **[S]** Start fresh, **[P]** Pick a specific phase

### Welcome Message

"Welcome! Let's build your OpenClaw agent workspace step by step.

**Your settings:**
- Agent name: {name}
- Mode: {single/multi-agent}
- Output: {workspace path}

This journey has 6 phases. I'll check in with you between each one so you can adjust course. Ready?"

Wait for user confirmation.

---

## Phase 1: Discovery — What Agent Do You Need?

**Goal**: Understand what the agent does, who it serves, and what it needs.

### 1.1 Reference Templates

"Before we dive in — would you like to browse reference templates for common agent archetypes? I have templates for Software Architect, Code Reviewer, Security Engineer, Technical Writer, DevOps Automator, Sprint Prioritizer, UX Researcher, and Feedback Synthesizer.

**[RT]** Browse templates for inspiration, or just tell me about your agent."

If RT selected: Read and present `references/agent-templates/index.md`, let user browse individual templates, then return here.

### 1.2 Intent Discovery

Ask the user:
- What is this agent's primary job? What does it do when someone talks to it?
- Who are the people that will talk to this agent?
- Where do conversations happen? (Telegram, WhatsApp, Discord, Slack, etc.)
- Is this one agent or do you envision a team of specialized agents?

Probe deeper based on responses:
- How technical is the audience?
- Will it be public-facing, team-internal, or both?
- What should the agent absolutely NOT do? (refusal boundaries)

### 1.3 Use Cases

Walk through 3-5 concrete scenarios:
- "Someone sends your agent a message saying X. What should happen?"
- What tasks does it handle vs delegate vs refuse?

### 1.4 Requirements

Based on the conversation, determine:
- Which workspace files are needed (SOUL always, IDENTITY always, AGENTS always, others optional)
- Memory strategy recommendation (minimal / standard / comprehensive)
- Whether HEARTBEAT, BOOTSTRAP, or TOOLS files are needed
- For multi-agent: initial agent roster

### Discovery Checkpoint

"Phase 1 complete! Here's what I've captured:
- Agent: {name} — {one-line purpose}
- Audience: {who}
- Channels: {where}
- Mode: {single/multi}
- Files needed: {list}
- Memory: {strategy}

**[C]** Continue to Phase 2 (Memory Design)
**[R]** Revise something
**[M]** Save progress and stop here"

---

## Phase 2: Memory Design — How Should It Remember?

**Goal**: Design the memory architecture before building the persona.

### 2.1 Memory Strategy

Based on the discovery:

- **Minimal**: MEMORY.md only, no daily logs, manual curation. Good for simple/stateless agents.
- **Standard**: MEMORY.md + daily logs, weekly SCRIBE compression, 7-day active window. Good for most agents.
- **Comprehensive**: Full architecture with archival, promotion triggers, SCRIBE compression, 14-day active window. Good for agents managing complex ongoing work.

Discuss trade-offs and confirm the strategy.

### 2.2 Memory Categories

What categories should MEMORY.md have?
- User Profile (almost always)
- Projects (if managing ongoing work)
- Preferences (confirmed user preferences)
- People (contacts and relationships)
- Lessons Learned (important learnings)
- Custom categories based on agent role

### 2.3 Daily Log Format

If daily logs enabled:
- Decisions, Facts, Actions, Open Questions sections
- For multi-agent: shared vs per-agent memory, team-memory/ directory

### Memory Checkpoint

"Phase 2 complete! Memory architecture:
- Strategy: {minimal/standard/comprehensive}
- MEMORY.md categories: {list}
- Daily logs: {yes/no, format}
- Team memory: {if applicable}

**[C]** Continue to Phase 3 (Soul Design)
**[R]** Revise something
**[M]** Save progress and stop here"

---

## Phase 3: Soul Design — Who Is This Agent?

**Goal**: Craft a coherent, opinionated, token-efficient SOUL.md.

### 3.1 Identity Statement

Craft collaboratively: "You are [NAME], a [ROLE] for [CONTEXT]."

One sentence. Specific. Predictive of behavior.

### 3.2 Core Values (3-5)

Each value needs:
- **Name**: Short label
- **Behavioral prediction**: What the agent DOES because of this value
- **What it means in practice**: Concrete example

Anti-patterns to avoid: "Be helpful" (too vague), "Ensure quality" (not actionable).

### 3.3 Boundaries

Probe for:
- What should the agent NEVER do? (hard refusals)
- What requires confirmation before action? (destructive operations)
- What's the fallback when uncertain? (ask vs guess vs refuse)

Each boundary must be specific and actionable.

### 3.4 Voice

Design the communication personality:
- Tone (direct/warm/casual/formal)
- Default response length
- Format preferences (bullets vs prose, emoji usage)
- Anti-patterns (phrases to never use, e.g., "Great question!")
- Optional vibe (2-3 sentences capturing personality flavor)

### 3.5 Token Budget Check

SOUL.md must be under 2,000 words. Present the complete draft and word count. If over, suggest specific cuts.

### Soul Checkpoint

Present the complete SOUL.md draft for review.

"Phase 3 complete! Your SOUL.md is {word_count} words.

**[C]** Continue to Phase 4 (Workspace Design)
**[R]** Revise something
**[M]** Save SOUL.md and stop here"

---

## Phase 4: Workspace Design — What Files and Structure?

**Goal**: Design IDENTITY.md and determine the complete file manifest.

### 4.1 IDENTITY.md

Create collaboratively:
- name: Agent display name
- emoji: Representative emoji
- status: Agent tagline

### 4.2 AGENTS.md Design

Design the operating manual:
- Memory management rules (write/remember/forget — informed by Phase 2)
- Safety rules (informed by SOUL.md boundaries from Phase 3)
- Group chat behavior rules
- Agent-specific workflows
- Tool rules and constraints
- Sub-agent rules (critical: any rule needed by sub-agents MUST be here)

### 4.3 Optional Files

For each file identified in Phase 1:
- USER.md: User profile template
- GOALS.md: Initial goal structure
- HEARTBEAT.md: Monitoring checklist (keep empty by default)
- BOOTSTRAP.md: First-run ritual
- TOOLS.md: Local environment notes

### 4.4 Multi-Agent Design (if applicable)

- Agent roster with per-agent directories
- Shared vs per-agent file decisions
- Routing rules and mention triggers
- Default agent and fallback behavior

### Workspace Checkpoint

"Phase 4 complete! Workspace manifest:
{list all files to generate}
{directory structure diagram}

**[C]** Continue to Phase 5 (Scaffolding)
**[R]** Revise something
**[M]** Save progress and stop here"

---

## Phase 5: Scaffolding — Generate Everything

**Goal**: Create all workspace files and validate them.

### 5.1 Create Directory Structure

For single-agent: flat structure at workspace path.
For multi-agent: per-agent directories with shared files.

### 5.2 Generate Files

Write each file using the design decisions from Phases 1-4:
1. SOUL.md (from Phase 3 draft)
2. IDENTITY.md (from Phase 4)
3. AGENTS.md (from Phase 4 design)
4. MEMORY.md (from Phase 2 template)
5. All optional files as designed
6. Daily log template (if applicable)
7. openclaw.json (if needed)

### 5.3 Validate

Run checks:
- SOUL.md under 2,000 words
- AGENTS.md under 150 lines
- MEMORY.md under 200 lines (if exists)
- All cross-references consistent
- Sub-agent critical rules live in AGENTS.md (not only in SOUL.md)
- No secrets or credentials in any workspace file

Report any issues.

### Scaffolding Checkpoint

"Phase 5 complete! Generated {N} files at {workspace_path}:
{file list with sizes}

**[C]** Continue to Phase 6 (Quality Audit)
**[R]** Fix something before audit
**[M]** Stop here — workspace is ready for use"

---

## Phase 6: Quality Audit — Score and Improve

**Goal**: Run a comprehensive quality audit on the generated workspace.

Invoke the `openclaw-workspace-audit` skill logic on the workspace we just created. This provides an independent quality check of everything we built.

Present the scored report and fix any issues identified.

### Completion

"Your OpenClaw workspace is ready!

**Workspace:** {path}
**Quality Score:** {score}/200 — {rating}
**Files:** {list}

**Next steps:**
1. Start a session to test your new agent
2. After a week of use, run `/oc-workspace-audit` to reassess quality
3. Run `/oc-autonomy` if you want to enable autonomous operation
4. Run `/oc-memory` if you want to fine-tune memory architecture

**Quick commands:**
- `/oc-architect` — Modify individual workspace files
- `/oc-workspace-audit` — Re-run quality audit anytime
- `/oc-autonomy` — Autonomy readiness assessment"

## Integration

This wizard uses content and patterns from:
- **openclaw-agent-architect** — File generation patterns and interview techniques
- **openclaw-agent-builder** — Guardrails checklist and autonomy design
- **openclaw-memory** — Four-layer memory model and SCRIBE compression
- **openclaw-workspace-audit** — Scored quality assessment
- **Reference agent templates** — Pre-built personas for inspiration (in `references/agent-templates/`)
