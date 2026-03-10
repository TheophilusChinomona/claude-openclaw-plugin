---
name: openclaw-autonomy-audit
description: Audit and score agent autonomy readiness. Scans SOUL.md, HEARTBEAT.md, AGENTS.md, cron jobs, heartbeat config, daemon setup, error handling, and monitoring to identify gaps preventing true autonomous operation.
trigger:
  - autonomy
  - passive
  - proactive
  - self-directed
  - idle
  - autonomous
  - agent not doing anything
  - agent waiting
  - agent won't act on its own
---

# Autonomy Audit (OpenClaw)

Assess whether an OpenClaw agent can operate independently between user interactions and produce a scored remediation plan.

## Canonical references

- Remediation patterns and templates: **Read** `references/autonomy-patterns.md`
- Cron/heartbeat setup: cross-reference **openclaw-automation** skill
- Agent workspace files: cross-reference **openclaw-agent-builder** skill
- Cron management command: `/oc-cron`

## The Five Critical Layers of Agent Autonomy

True autonomous operation requires all five layers working together. A gap in any single layer breaks the chain.

```
Layer 5: Monitoring        ← Can you tell if it's working?
Layer 4: Error Handling    ← Can it recover from failures?
Layer 3: Process Mgmt      ← Does it stay alive?
Layer 2: Decision Logic    ← Does it know what to do when idle?
Layer 1: Scheduling        ← Does anything wake it up?
```

| Layer | What It Provides | Key Files/Config |
|-------|-----------------|------------------|
| **1. Scheduling** | Periodic wake-up triggers | `openclaw cron list`, heartbeat config |
| **2. Decision Logic** | Explicit "when idle, do X" rules | `SOUL.md` — `## Autonomous Behavior` section |
| **3. Process Management** | Gateway stays alive without supervision | launchd / systemd / pm2 daemon config |
| **4. Error Handling** | Retry limits, cost caps, loop breakers | `AGENTS.md` — `## Cost Controls`, `SOUL.md` guardrails |
| **5. Monitoring** | Health checks, structured logging | Health-check cron job, `cron.runLog`, `memory/` directory |

## Autonomy Maturity Scoring Rubric

Score each item 0–2. Maximum score: 16.

| # | Check | 0 (Missing) | 1 (Partial) | 2 (Complete) |
|---|-------|-------------|-------------|--------------|
| 1 | **SOUL.md autonomous behavior rules** | No autonomous behavior section | Has section but vague ("be helpful") | Explicit idle triggers: "when idle, do X", "every N minutes, check Y" |
| 2 | **Scheduling mechanism** | No cron jobs, no heartbeat | Has cron OR heartbeat but not both | Cron for clockwork tasks + heartbeat for judgment-based tasks |
| 3 | **HEARTBEAT.md actionable checklist** | Empty or missing | Has content but no `- [ ]` checklist items | Mission-specific checklist items with clear done criteria |
| 4 | **Session clearing strategy** | No session reset config | Has reset but no retention policy | `session.reset` + `cron.sessionRetention` configured |
| 5 | **Gateway daemon persistence** | Manual `openclaw gateway start` only | Has daemon but no auto-restart | launchd/systemd/pm2 with auto-restart on failure |
| 6 | **Error handling / cost controls** | No limits anywhere | Has max-iteration OR retry limits | Max turns, max retries, explicit stop conditions, cost cap in AGENTS.md |
| 7 | **Health monitoring** | No health checks | Health check exists but interval > 5min | Health-check cron at <= 5min checking gateway + cron + channels |
| 8 | **Structured activity logging** | No logging config | Has `cron.runLog` OR `memory/` dir | `cron.runLog` enabled + agent writes daily `memory/YYYY-MM-DD.md` entries |

### Scoring Bands

| Band | Score | Meaning |
|------|-------|---------|
| **Idle** | 0–5 | Agent does nothing unless prompted. Essentially a chatbot. |
| **Reactive** | 6–10 | Some automation exists but agent can't self-direct or recover from failures. |
| **Semi-Autonomous** | 11–13 | Agent operates on schedule but has gaps in error handling, monitoring, or decision logic. |
| **Autonomous** | 14–16 | Agent operates independently with safety nets. Can self-direct, recover, and report status. |

## Cron vs Heartbeat Decision Matrix

Use this to advise which scheduling mechanism fits each task type.

| Task Type | Mechanism | Why |
|-----------|-----------|-----|
| "Check inbox every 30 minutes" | **Cron** | Fixed interval, no judgment needed |
| "Review pending PRs when idle" | **Heartbeat** | Requires context: is there anything pending? |
| "Send daily summary at 9 AM" | **Cron** | Clock-driven, deterministic |
| "Escalate if no response in 2 hours" | **Heartbeat** | Needs state awareness |
| "Run health check every 5 minutes" | **Cron** | Fixed interval, mechanical |
| "Decide whether to follow up on a lead" | **Heartbeat** | Requires judgment and memory |

**Rule of thumb:** Cron = clockwork (no thinking). Heartbeat = judgment (needs agent reasoning).

## Common Production Pitfalls

Warn the user about these when they score Semi-Autonomous or below:

1. **Context overflow** — Long-running autonomous sessions accumulate context until the model degrades. Fix: session clearing strategy + compaction config.
2. **Runaway costs** — No cost cap means an autonomous loop can burn through API credits. Fix: explicit max turns per cycle + daily cost ceiling.
3. **Silent failures** — Agent errors go unnoticed for hours/days. Fix: health monitoring cron + structured logging.
4. **Stale data** — Agent operates on cached/old information without refreshing. Fix: heartbeat checks for data freshness.
5. **Heartbeat state loss** — Session reset clears heartbeat context. Fix: persist heartbeat state to `HEARTBEAT.md` + `memory/`.
6. **Loop storms** — Error triggers retry, retry triggers error. Fix: exponential backoff + max retry count + circuit breaker in SOUL.md.
7. **Permission creep** — Autonomous agent gradually takes actions beyond its mandate. Fix: hard prohibitions in SOUL.md + ask-before-destructive rule.

## Remediation Priority Order

When presenting fixes, order by impact (highest first):

1. **Scheduling** — Without wake-up triggers, nothing else matters
2. **SOUL.md decision logic** — Agent needs to know what to do when woken
3. **HEARTBEAT.md checklist** — Gives heartbeat something actionable
4. **Gateway daemon** — Ensures the agent is actually running
5. **Error handling / cost controls** — Safety net for autonomous operation
6. **Session clearing** — Prevents context degradation
7. **Health monitoring** — Detect failures early
8. **Structured logging** — Audit trail and debugging

## Audit Procedure

When activated (either via skill trigger or `/oc-autonomy` command):

1. Identify target agent(s) — use `--agent <id>` or scan all agents in workspace
2. For each agent, run the 8-item checklist:
   - Read `SOUL.md` — look for `## Autonomous Behavior` or keywords: "proactively", "when idle", "periodically", "without being asked"
   - Run `openclaw cron list` + check `openclaw config get heartbeat`
   - Read `HEARTBEAT.md` — check for `- [ ]` checklist items
   - Check `openclaw config get session.reset` + `cron.sessionRetention`
   - Check daemon: `launchctl list | grep openclaw` / `systemctl status openclaw` / `pm2 list` / `openclaw gateway status`
   - Read `AGENTS.md` + `SOUL.md` for max-iteration, retry, cost, loop breaker patterns
   - Check cron list for health/status/monitor jobs with <= 5min intervals
   - Check `cron.runLog` config + `memory/` directory existence
3. Score each item 0–2
4. Calculate total and assign band
5. Present scorecard table
6. List remediations in priority order with specific commands/file changes
7. If `--fix` mode: iterate deficiencies, show proposed change, ask confirmation, apply

## Cross-references

- **openclaw-automation** — Cron, heartbeat, and webhook details
- **openclaw-agent-builder** — Workspace file generation (now includes autonomy interview)
- `/oc-cron` — Manage cron jobs directly
- `/oc-autonomy` — The command counterpart to this skill
