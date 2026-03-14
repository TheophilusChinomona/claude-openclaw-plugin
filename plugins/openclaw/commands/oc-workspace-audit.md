---
description: Comprehensive scored audit of an OpenClaw agent workspace — evaluates SOUL, IDENTITY, AGENTS, memory, and config quality
argument-hint: "[workspace-path]"
allowed-tools: Read, Glob, Grep
---

# /oc-workspace-audit Command

Run a comprehensive quality audit on an OpenClaw agent workspace using the **openclaw-workspace-audit** skill.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **workspace-path** (optional): Path to the agent workspace. Default: `~/.openclaw/workspace`

## Skill Reference

Apply the full audit workflow from the **openclaw-workspace-audit** skill (under `skills/openclaw-workspace-audit/SKILL.md`).

1. Scan the workspace directory for all OpenClaw files
2. Audit SOUL.md across 5 dimensions (0-50 points)
3. Audit IDENTITY.md across 3 dimensions (0-30 points)
4. Audit AGENTS.md across 5 dimensions (0-50 points)
5. Audit memory architecture across 4 dimensions (0-40 points)
6. Audit configuration across 3 dimensions (0-30 points)
7. Generate scored report (0-200) with rating and prioritized recommendations

## Guidelines

- This is a read-only audit — do not modify files, only recommend changes
- Present findings constructively with specific improvement suggestions
- Suggest next skills to run based on lowest-scoring areas
- Complements `/oc-autonomy` which focuses on autonomous operation readiness
