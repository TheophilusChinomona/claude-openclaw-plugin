---
name: openclaw-agent-builder
description: Build high-performing OpenClaw agents end-to-end. Use when you want to design a new agent (persona + operating rules) and generate the required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Also use to iterate on an existing agent's behavior, guardrails, autonomy model, heartbeat plan, and skill roster.
---

# Agent Builder (OpenClaw)

Design and generate a complete **OpenClaw agent workspace** with strong defaults and advanced-user-oriented clarifying questions.

## Canonical references

- Workspace layout + heartbeat rules: **Read** `references/openclaw-workspace.md`
- File templates/snippets: **Read** `references/templates.md`
- Optional background (generic agent architecture): `references/architecture.md`

## Workflow: build an agent from scratch

### Phase 1 — Interview (ask clarifying questions)

Ask only what you need; keep it tight. Prefer multiple short rounds over one giant questionnaire.

Minimum question set (advanced):

1) **Job statement**: What is the agent's primary mission in one sentence?
2) **Surfaces**: Which channels (Telegram/WhatsApp/Discord/iMessage)? DM only vs groups?
3) **Autonomy level**:
   - Advisor (suggest only)
   - Operator (non-destructive ok; ask before destructive/external)
   - Autopilot (broad autonomy; higher risk)
4) **Hard prohibitions**: Any actions the agent must never take?
5) **Memory**: Should it keep curated `MEMORY.md`? What categories matter?
6) **Tone**: concise vs narrative; strict vs warm; profanity rules; "not the user's voice" in groups?
7) **Tool posture**: tool-first vs answer-first; verification requirements.
8) **Autonomy model** (skip for Advisor):
   - Proactive check-in frequency? (e.g., every 30m, twice daily, never)
   - Idle behavior? (check inbox, review tasks, wait for prompts)
   - Cost guardrails? (max turns per autonomous cycle, max retries)
   - Health-check cron? (recommended for Operator/Autopilot)

### Phase 2 — Generate workspace files

Generate these files (minimum viable OpenClaw agent):

- `IDENTITY.md`
- `SOUL.md`
- `AGENTS.md`
- `USER.md`
- `HEARTBEAT.md` (often empty by default)

Optionals:

- `MEMORY.md` (private sessions only)
- `memory/YYYY-MM-DD.md` seed (today) with a short "agent created" entry
- `TOOLS.md` starter (if the user wants per-environment notes)

> For memory setup details (daily logs, MEMORY.md curation, shared memory, SCRIBE compression),
> see `openclaw-memory` skill. Use `/oc-memory init` to scaffold the memory structure.

Use templates from `references/templates.md` but tailor content to the answers.

### Phase 2.5 — Autonomy configuration (Operator/Autopilot only)

If the agent's autonomy level is Operator or Autopilot, generate these additional configurations based on the Phase 1 autonomy model answers:

1. **`## Autonomous Behavior` section in SOUL.md** — Explicit idle triggers, proactive check rules, frequency, and boundaries (see `openclaw-autonomy-audit` skill, Pattern A)
2. **Populate HEARTBEAT.md** — Mission-specific `- [ ]` checklist items based on the agent's job statement and idle behavior preferences
3. **Propose cron jobs** — Generate `openclaw cron add` commands for scheduled tasks (health checks, inbox scans, summaries) matching the stated frequency
4. **`## Cost Controls` section in AGENTS.md** — Max turns per cycle, max retries, stop conditions, circuit breaker rules, daily budget (see `openclaw-autonomy-audit` skill, Pattern E)

### Phase 3 — Guardrails checklist

Ensure the generated agent includes:

- Explicit ask-before-destructive rule.
- Explicit ask-before-outbound-messages rule.
- Stop-on-CLI-usage-error rule.
- Max-iteration / loop breaker guidance.
- Group chat etiquette.
- Sub-agent note: essential rules live in `AGENTS.md`.

### Phase 4 — Acceptance tests (fast)

Provide 5–10 short scenario prompts to validate behavior, e.g.:

- "Draft but do not send a message to X; ask me before sending."
- "Summarize current workspace status without revealing secrets."
- "You hit an unknown flag error; show how you recover using --help."
- "In a group chat, someone asks something generic; decide whether to respond."

## Workflow: iterate on an existing agent

When improving an existing agent, ask:

1) What are the top 3 failure modes you've seen? (loops, overreach, verbosity, etc.)
2) What autonomy changes do you want?
3) Any new safety boundaries?
4) Any changes to heartbeat behavior?
5) Is the agent autonomous enough? Too autonomous?
   Run `/oc-autonomy --agent <id>` for a scored assessment.

Then propose targeted diffs to:

- `SOUL.md` (persona/tone/boundaries)
- `AGENTS.md` (operating rules + memory + delegation)
- `HEARTBEAT.md` (small checklist)
- Cron job additions/removals (if autonomy level changing)

Keep changes minimal and surgical.
