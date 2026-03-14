---
description: Full guided journey to create a complete OpenClaw agent workspace — chains discovery, design, scaffolding, and audit
argument-hint: "[workspace-name]"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /oc-wizard Command

Run the complete OpenClaw workspace creation wizard using the **openclaw-workspace-wizard** skill.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **workspace-name** (optional): Working name for the agent. Will be prompted if not provided.

## Skill Reference

Apply the full orchestrated workflow from the **openclaw-workspace-wizard** skill (under `skills/openclaw-workspace-wizard/SKILL.md`).

Six phases with user checkpoints between each:

1. **Discovery** — What agent do you need? (intent, use cases, requirements)
2. **Memory Design** — How should it remember? (strategy, categories, daily logs)
3. **Soul Design** — Who is this agent? (identity, values, boundaries, voice)
4. **Workspace Design** — What files and structure? (IDENTITY, AGENTS, optional files)
5. **Scaffolding** — Generate all workspace files
6. **Quality Audit** — Score the workspace and fix issues

## Guidelines

- This is the comprehensive path — for quick single-file edits use `/oc-architect` instead
- Users can pause at any checkpoint and resume later
- Offer reference agent templates during Phase 1 for inspiration
- Each phase produces artifacts that feed the next
- Never include API keys, passwords, or tokens in generated files
