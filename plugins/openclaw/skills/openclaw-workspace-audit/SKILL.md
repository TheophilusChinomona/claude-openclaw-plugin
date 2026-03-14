---
name: openclaw-workspace-audit
description: Comprehensive scored audit of an existing OpenClaw agent workspace. Evaluates SOUL.md, IDENTITY.md, AGENTS.md, MEMORY.md, openclaw.json, and daily logs across quality dimensions with a prioritized improvement plan. Use when the user says "audit my workspace", "review my agent", "check my agent quality", "score my agent", "improve my agent setup", "workspace health check", or "agent quality audit". Distinct from autonomy-audit which focuses only on autonomous operation readiness — this skill audits the full workspace quality including persona coherence, memory health, and configuration correctness.
---

# OpenClaw Workspace Audit

Perform a comprehensive, scored quality audit of an existing OpenClaw agent workspace. Evaluates every workspace file across specific quality dimensions and produces a prioritized improvement plan.

## When to Use

- User wants to know how good their agent workspace is
- User is experiencing inconsistent agent behavior
- User wants to improve an existing agent before deploying
- User completed agent creation and wants a quality check
- Distinct from `/oc-autonomy` which only scores autonomous operation readiness

## Audit Procedure

### Step 1: Locate Workspace

Ask the user for the workspace path. Common locations:
- `~/.openclaw/workspace/` (default single-agent)
- `~/.openclaw/agents-workspaces/<agent-id>/` (multi-agent)
- User-specified path

### Step 2: Inventory Scan

Scan the workspace directory for ALL OpenClaw files. Report what exists and what's missing:

| File | Status | Notes |
|------|--------|-------|
| SOUL.md | Found/Missing | |
| IDENTITY.md | Found/Missing | |
| AGENTS.md | Found/Missing | |
| USER.md | Found/Missing | Optional |
| MEMORY.md | Found/Missing | Optional but recommended |
| GOALS.md | Found/Missing | Optional |
| HEARTBEAT.md | Found/Missing | Optional |
| BOOTSTRAP.md | Found/Missing | Only for new agents |
| TOOLS.md | Found/Missing | Optional |
| openclaw.json | Found/Missing | System config |
| memory/ | Found/Missing | Daily logs directory |

### Step 3: SOUL.md Audit (0-50 points)

Score each dimension 0-10:

**Clarity (0-10)**: Is the identity statement specific? Does it say exactly what the agent does and for whom? A score of 0 = no identity statement. A score of 10 = crystal clear, one-sentence role that predicts behavior.

**Values (0-10)**: Are core values behavioral predictions, not platitudes? "Be helpful" = 0 points. "When uncertain, say so rather than guess" = 10 points. Each value should predict a specific behavior.

**Boundaries (0-10)**: Are refusal rules specific and actionable? "Be careful" = 0 points. "Never delete files without explicit confirmation" = 10 points. Must include: what requires confirmation, what's refused, fallback when uncertain.

**Voice (0-10)**: Is communication style defined with specifics? Must include: tone, default length, format preferences, and anti-patterns (what NOT to say). Vague descriptions like "friendly" score low.

**Token Efficiency (0-10)**: Is it under 2,000 words? Every word must earn its place. Redundant sections, generic filler, or overly verbose explanations reduce the score. SOUL.md is loaded on every prompt — bloat costs real tokens.

Present section-by-section findings with specific improvement suggestions.

### Step 4: IDENTITY.md Audit (0-30 points)

Score each dimension 0-10:

**Completeness (0-10)**: Has name, emoji, and status line at minimum. Optional: group_name, group_emoji for group chat contexts.

**Coherence (0-10)**: Does the identity match the SOUL.md personality? An agent with a playful soul should have a playful name/emoji, not a corporate one. Cross-reference with SOUL.md to check alignment.

**Engagement (0-10)**: Is the status line compelling and informative? Does it tell users what this agent does? Generic statuses like "Ready to help" score low.

### Step 5: AGENTS.md Audit (0-50 points)

Score each dimension 0-10:

**Memory Rules (0-10)**: Are write/remember/forget rules clearly defined? Must specify: when to write to daily logs, what to promote to MEMORY.md, what to forget. Vague rules = low score.

**Safety Rules (0-10)**: Are destructive action confirmations specified? Must include: confirm before deleting, never expose credentials, handle ambiguous requests. Missing safety rules = 0.

**Group Chat Rules (0-10)**: Are group behavior rules defined? Must specify: when to respond vs stay quiet, mention-gating behavior, response length in groups vs DMs.

**Workflows (0-10)**: Are agent-specific workflows documented? What the agent does in common scenarios. Empty section = low score.

**Subagent Independence (0-10)**: Critical check — sub-agents only see AGENTS.md + TOOLS.md (NOT SOUL.md). Any safety rule or critical instruction needed by sub-agents MUST live in AGENTS.md, not just SOUL.md. Check that essential rules aren't hidden in SOUL.md where sub-agents can't see them.

**Token Check**: Is AGENTS.md under 150 lines? Over 150 = flag for trimming.

### Step 6: Memory Architecture Audit (0-40 points)

Score each dimension 0-10:

**MEMORY.md Structure (0-10)**: Is it properly categorized (User Profile, Projects, Preferences, People, Lessons Learned)? Are entries factual and concise? Is it under the 200-line hard limit?

**Curation Quality (0-10)**: Are there stale entries? Duplicates? Entries that belong in daily logs, not long-term memory? Does it show evidence of active curation (updated dates, removed outdated info)?

**Daily Logs (0-10)**: Do they exist? Are they recent? Are they structured (decisions, facts, actions, open questions)? Is there evidence of regular writing?

**Promotion Pipeline (0-10)**: Is there evidence that information flows from daily logs → MEMORY.md? Are old logs being archived (>14 days)? Is the SCRIBE compression cycle working?

### Step 7: Configuration Audit (0-30 points)

Score each dimension 0-10:

**openclaw.json Validity (0-10)**: Is it valid JSON? Are required fields present (model, provider)? For multi-agent: are agent bindings correct?

**Model Selection (0-10)**: Is the model appropriate for the agent's role? Complex reasoning agents should use stronger models. Simple response agents can use faster/cheaper models. Is failover configured?

**Routing (0-10)**: (Multi-agent only) Are routing rules defined? Mention triggers set? Default agent specified? Channel mappings correct? Single-agent workspaces score N/A here.

### Step 8: Generate Report

Calculate overall score:

| Category | Max Points | Score |
|----------|-----------|-------|
| SOUL.md | 50 | |
| IDENTITY.md | 30 | |
| AGENTS.md | 50 | |
| Memory Architecture | 40 | |
| Configuration | 30 | |
| **Total** | **200** | |

**Rating Scale**:
- 0-60: **Needs Major Work** — Critical files missing or fundamentally broken
- 61-120: **Functional But Improvable** — Works but has significant quality gaps
- 121-160: **Good** — Solid foundation, refinement opportunities
- 161-200: **Excellent** — Production-ready, well-crafted workspace

**Prioritized Recommendations**:

- **P0 (Critical)**: Missing required files, broken config, security gaps (no confirmation rules), sub-agent rule leaks
- **P1 (Important)**: Weak boundaries, vague values, memory bloat over 200 lines, missing daily logs
- **P2 (Nice to Have)**: Voice refinement, additional optional files, token optimization

**Quick Wins**: List 3-5 specific changes that would have the biggest impact for the least effort.

### Step 9: Offer Next Steps

Based on the audit results, suggest the appropriate next skill:

- Low SOUL.md score → "Run `/oc-architect` to redesign your agent's personality"
- Low Memory score → "Run `/oc-memory` to restructure your memory architecture"
- Low Autonomy → "Run `/oc-autonomy` for a focused autonomy assessment"
- Multi-agent routing issues → "Run the multi-agent routing workflow"
- Good score → "Your workspace is solid! Consider running `/oc-autonomy` for the autonomy-specific deep dive"

## Integration with Other Skills

This audit complements but does not replace:
- **openclaw-autonomy-audit** — Focuses specifically on autonomous operation readiness (scheduling, daemon, error handling). Use both for a complete picture.
- **openclaw-agent-architect** — Use to fix issues identified by this audit
- **openclaw-memory** — Use to restructure memory based on audit findings
