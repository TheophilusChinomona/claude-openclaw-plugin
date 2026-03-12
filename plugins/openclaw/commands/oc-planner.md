---
description: Brainstorm, design, and document OpenClaw agent teams (Discovery, Design, Document) and produce Agent Team Documentation
argument-hint: "[output-path]"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /oc-planner Command

Run the **openclaw-agent-planner** skill to brainstorm, design, and document OpenClaw agent teams, then produce Agent Team Documentation.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **output-path** (optional): Where to write the generated markdown document. If omitted, write to the current workspace or ask the user.

## Skill Reference

Apply the full workflow from the **openclaw-agent-planner** skill (under `skills/openclaw-agent-planner/SKILL.md`).

### Stage 1: Discovery

Understand the user's world: role & context, pain points & automation appetite, existing setup, constraints. Ask focused questions; don't re-ask what you can infer.

### Stage 2: Design

- **2.1 Agent brainstorm**: Propose a table of agents (Name, Role, Why, Channel). Refine with the user (must-haves, overlaps, gaps, priority).
- **2.2 Capability mapping**: For each agent, build a permission matrix (Autonomous / Confirm / Restricted / Denied). Use **references/permissions-reference.md** in the planner skill for capability categories and archetype profiles (Personal Assistant, DevOps, Sales Dev, Research, SHEQ).
- **2.3 Inter-agent design**: If multiple agents, define communication, delegation, shared vs isolated resources, conflict resolution. Recommend the OpenClaw multi-agent pattern (per-agent workspace, shared AGENTS.md).
- **2.4 Model selection**: Recommend Opus/Sonnet/Haiku per agent based on task and cost.

### Stage 3: Document

Generate the **Agent Team Documentation** with the exact structure in the skill: Team Overview, Agent Profiles (per agent: role, persona, capabilities, boundaries, workflows, memory strategy, goals, config snippet), Team Interaction Rules, Security & Governance, Implementation Roadmap, Appendix.

Save as markdown at the given output path. If the user wants .docx, use the docx skill to produce a formatted Word document.

## Quality Checks

Before delivery, verify: every agent has a full profile; permission levels are consistent; no orphan agent references; roadmap has concrete steps; security covered; persona aligns with role.

## Guidelines

- Document is self-contained for someone unfamiliar with OpenClaw
- Include generation date; mark as a living document
- Architecture diagram: simple ASCII/text that renders in any markdown viewer
