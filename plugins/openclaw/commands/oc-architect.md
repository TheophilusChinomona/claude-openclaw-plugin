---
description: Build or optimize OpenClaw agent workspace files (SOUL, IDENTITY, AGENTS, MEMORY, GOALS) via guided interview or workspace scan
argument-hint: "<build|optimize> [workspace-path]"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /oc-architect Command

Build or optimize OpenClaw agent workspace files through the **openclaw-agent-architect** skill.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **Subcommand** (default: `build`): `build` or `optimize`
- **workspace-path** (optional): Path to the agent workspace. Default: `~/.openclaw/workspace`

If no subcommand is given, use `build`.

## Skill Reference

Apply the full workflow from the **openclaw-agent-architect** skill (under `skills/openclaw-agent-architect/SKILL.md`).

### build

Run **Mode 1: Build from Scratch**. Conduct the 5-phase interview (SOUL → IDENTITY → AGENTS → MEMORY → GOALS), then generate each file after its phase. Use templates as scaffolding only; customize from the user's answers. See `skills/openclaw-agent-architect/references/templates.md` for file structure.

- Phase 1: SOUL.md — role, personality, values, boundaries, communication style
- Phase 2: IDENTITY.md — name, emoji, status line
- Phase 3: AGENTS.md — memory rules, safety, workflows, tool rules
- Phase 4: MEMORY.md — user profile, projects, preferences, people
- Phase 5: GOALS.md — active goals, milestones, review schedule

Write files into the given workspace path. Keep SOUL.md under 2,000 words; ensure persona coherence across all files.

### optimize

Run **Mode 2: Scan & Optimize**. Read all existing workspace markdown files at the given path, then:

1. Audit for completeness (which files exist, which are missing or sparse)
2. Check consistency (SOUL vs AGENTS, GOALS vs MEMORY)
3. Check for bloat (SOUL over 2,000 words, redundancy)
4. Check for vagueness (generic instructions)
5. Check persona coherence
6. Propose specific improvements with before/after; show changes before writing

Preserve the user's intent; tighten language for token awareness.

## Guidelines

- Never include API keys, passwords, or tokens in any generated file
- Recommend `chmod 444` on SOUL.md and IDENTITY.md after finalizing
- GOALS.md is a custom addition (OpenClaw loads all .md from workspace)—mention this to the user
