---
name: oc-autonomy
description: Audit agent autonomy readiness — score how well agents operate independently and suggest remediations
arguments:
  - name: --agent
    description: Audit a single agent by ID (default: all agents in workspace)
    required: false
  - name: --fix
    description: Offer to apply remediations interactively after scoring
    required: false
---

# /oc-autonomy — Agent Autonomy Audit

Score how well your OpenClaw agents operate autonomously and get actionable remediations.

## Before you begin

Load the **openclaw-autonomy-audit** skill for the full scoring rubric and remediation patterns:
- Scoring rubric: `plugins/openclaw/skills/openclaw-autonomy-audit/SKILL.md`
- Remediation templates: `plugins/openclaw/skills/openclaw-autonomy-audit/references/autonomy-patterns.md`

## Scan procedure

### Step 1: Identify target agents

If `--agent <id>` is provided, audit only that agent. Otherwise, discover all agents:

```bash
# List all configured agents
openclaw agent list
# Or scan workspace directories
ls -d */SOUL.md 2>/dev/null || ls -d */IDENTITY.md 2>/dev/null
```

### Step 2: Run the 8-item audit for each agent

For each agent, perform these checks and score 0–2 per item:

#### Check 1: SOUL.md autonomous behavior rules

```bash
# Read the agent's SOUL.md
cat <agent-workspace>/SOUL.md
```

**Score:**
- **0** — No `## Autonomous Behavior` section, no keywords like "proactively", "when idle", "periodically", "without being asked"
- **1** — Has section but rules are vague (e.g., "be helpful", "check things occasionally")
- **2** — Explicit idle triggers with specific actions: "when idle, do X", "every N minutes, check Y"

#### Check 2: Scheduling mechanism

```bash
openclaw cron list
openclaw config get heartbeat
```

**Score:**
- **0** — No cron jobs AND no heartbeat configured
- **1** — Has cron jobs OR heartbeat, but not both
- **2** — Cron for clockwork tasks + heartbeat for judgment-based tasks

#### Check 3: HEARTBEAT.md actionable checklist

```bash
cat <agent-workspace>/HEARTBEAT.md
```

**Score:**
- **0** — File missing or empty (only comments/placeholders)
- **1** — Has content but no `- [ ]` checklist items (just prose)
- **2** — Mission-specific `- [ ]` checklist items with clear done criteria

#### Check 4: Session clearing strategy

```bash
openclaw config get session.reset
openclaw config get cron.sessionRetention
```

**Score:**
- **0** — Neither session reset nor retention configured
- **1** — Has reset but no retention policy (or vice versa)
- **2** — Both `session.reset` and `cron.sessionRetention` configured

#### Check 5: Gateway daemon persistence

```bash
# Check platform-specific daemon managers
launchctl list 2>/dev/null | grep -i openclaw
systemctl status openclaw-gateway 2>/dev/null
pm2 list 2>/dev/null | grep -i openclaw
openclaw gateway status
```

**Score:**
- **0** — No daemon; gateway requires manual `openclaw gateway start`
- **1** — Has daemon config but no auto-restart on failure
- **2** — Daemon with auto-restart (launchd KeepAlive / systemd Restart=always / pm2)

#### Check 6: Error handling / cost controls

```bash
cat <agent-workspace>/AGENTS.md
cat <agent-workspace>/SOUL.md
```

Look for: max-iteration, max turns, retry limits, cost cap, loop breaker, circuit breaker, stop conditions.

**Score:**
- **0** — No error handling or cost controls anywhere
- **1** — Has max-iteration OR retry limits (but not comprehensive)
- **2** — Max turns + max retries + explicit stop conditions + cost cap documented

#### Check 7: Health monitoring

```bash
openclaw cron list
```

Look for cron jobs with names containing "health", "status", "monitor", "check" with intervals <= 5 minutes.

**Score:**
- **0** — No health monitoring cron jobs
- **1** — Health check exists but interval > 5 minutes
- **2** — Health-check cron at <= 5min checking gateway + cron status + channels

#### Check 8: Structured activity logging

```bash
openclaw config get cron.runLog
ls <agent-workspace>/memory/ 2>/dev/null
```

**Score:**
- **0** — No `cron.runLog` config AND no `memory/` directory
- **1** — Has `cron.runLog` OR `memory/` directory (but not both)
- **2** — `cron.runLog` enabled + agent writes daily `memory/YYYY-MM-DD.md` entries

### Step 3: Calculate score and assign band

Sum all 8 scores (max 16), then assign:

| Band | Score | Label |
|------|-------|-------|
| Idle | 0–5 | Agent does nothing unless prompted |
| Reactive | 6–10 | Some automation but can't self-direct |
| Semi-Autonomous | 11–13 | Operates on schedule but has gaps |
| Autonomous | 14–16 | Fully independent with safety nets |

### Step 4: Present results

#### Per-agent scorecard

```
Agent: <agent-name>
Band: <band-label> (<score>/16)

| # | Check                          | Score | Finding                    |
|---|-------------------------------|-------|---------------------------|
| 1 | SOUL.md autonomous rules      | X/2   | <specific finding>        |
| 2 | Scheduling (cron + heartbeat) | X/2   | <specific finding>        |
| 3 | HEARTBEAT.md checklist        | X/2   | <specific finding>        |
| 4 | Session clearing strategy     | X/2   | <specific finding>        |
| 5 | Gateway daemon persistence    | X/2   | <specific finding>        |
| 6 | Error handling / cost controls| X/2   | <specific finding>        |
| 7 | Health monitoring             | X/2   | <specific finding>        |
| 8 | Structured activity logging   | X/2   | <specific finding>        |
```

#### Remediation list (ordered by impact)

Present remediations for items scoring < 2, ordered by priority:

1. **Scheduling** — highest impact, nothing works without triggers
2. **SOUL.md decision logic** — agent needs to know what to do
3. **HEARTBEAT.md checklist** — gives heartbeat actionable items
4. **Gateway daemon** — ensures the agent is running
5. **Error handling / cost controls** — safety for autonomous operation
6. **Session clearing** — prevents context degradation
7. **Health monitoring** — early failure detection
8. **Structured logging** — audit trail

For each remediation, show:
- What's missing
- The specific fix (command or file edit)
- Reference to the relevant pattern in `autonomy-patterns.md`

#### Multi-agent summary (when auditing all agents)

```
| Agent          | Score | Band             | Top Gap            |
|---------------|-------|------------------|--------------------|
| <agent-1>     | X/16  | <band>           | <biggest gap>      |
| <agent-2>     | X/16  | <band>           | <biggest gap>      |
| ...           |       |                  |                    |
| **Average**   | X/16  | <overall-band>   |                    |
```

### Step 5: Fix mode (`--fix`)

When `--fix` is provided, after presenting the scorecard:

1. Iterate through deficiencies (score < 2) in priority order
2. For each deficiency:
   - Show the proposed change (file edit, config command, or cron addition)
   - Reference the specific pattern from `autonomy-patterns.md`
   - Ask "Apply this fix? (y/n/skip)"
3. If confirmed, apply the change
4. After all fixes applied, re-run the audit to show the new score

## Examples

```bash
# Audit all agents
/oc-autonomy

# Audit a specific agent
/oc-autonomy --agent outreach-bot

# Audit and fix interactively
/oc-autonomy --fix

# Audit specific agent and fix
/oc-autonomy --agent outreach-bot --fix
```
