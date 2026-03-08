---
description: Scan your OpenClaw setup and suggest improvements based on available skills and commands
argument-hint: [--focus <area>]
allowed-tools: Bash, Read, Glob, Grep
---

# /oc-improve Command

Scan your OpenClaw installation, cross-reference findings across areas, and suggest prioritized improvements mapped to specific skills and commands.

## Arguments

The user provides: `$ARGUMENTS`

Parse optional flags:
- `--focus <area>` — scan only one area. Valid: `channels`, `agents`, `sessions`, `security`, `sandbox`, `automation`, `models`, `memory`, `backup`, `workspace`
- No flag = scan all 10 areas

## Precondition

Check that OpenClaw is installed:
```bash
which openclaw 2>/dev/null || echo "NOT_FOUND"
```

If not found, report:
```
OpenClaw CLI not found. Run /oc-setup to install.
```
And stop.

## Data Gathering

Run each scan area below. If `--focus` was given, run only that area. Suppress errors with `2>/dev/null` throughout — missing components are expected and become findings, not errors.

### 1. Channels
```bash
openclaw channels status --probe 2>/dev/null
openclaw config get channels 2>/dev/null
```
Capture: channel count, channel names, DM policies per channel, probe results (connected/failing).

### 2. Agents
```bash
openclaw agents list --bindings 2>/dev/null
ls ~/.openclaw/workspace/agents-workspaces/ 2>/dev/null
```
For each agent workspace found:
```bash
ls ~/.openclaw/workspace/agents-workspaces/$AGENT/ 2>/dev/null
head -5 ~/.openclaw/workspace/agents-workspaces/$AGENT/IDENTITY.md 2>/dev/null
wc -l ~/.openclaw/workspace/agents-workspaces/$AGENT/SOUL.md 2>/dev/null
```
Capture: agent count, workspace existence, SOUL.md presence and line count, IDENTITY.md presence, bindings list.

### 3. Sessions
```bash
openclaw config get session 2>/dev/null
```
Capture: dmScope value (main, per-channel-peer, per-account-channel-peer, or unset).

### 4. Security
```bash
openclaw security audit 2>/dev/null
find ~/.openclaw/credentials/ -type f -exec stat -c '%a %n' {} \; 2>/dev/null
openclaw config get gateway.auth 2>/dev/null
openclaw config get gateway.listen 2>/dev/null
```
Capture: audit findings, file permissions, auth mode, listen address.

### 5. Sandbox
```bash
openclaw config get agents.defaults.sandbox 2>/dev/null
openclaw config get agents 2>/dev/null | grep -i sandbox 2>/dev/null
```
Capture: default sandbox mode, per-agent sandbox overrides.

### 6. Automation
```bash
openclaw cron list 2>/dev/null
openclaw config get hooks 2>/dev/null
openclaw config get heartbeat 2>/dev/null
```
Capture: cron job count, hooks presence, heartbeat configuration.

### 7. Models
```bash
openclaw config get agents.defaults.model 2>/dev/null
openclaw config get models.providers 2>/dev/null
openclaw config get models.fallback 2>/dev/null
```
Capture: default model, provider count, fallback chain presence.

### 8. Memory
```bash
ls ~/.openclaw/memory/lancedb/ 2>/dev/null
cat ~/.openclaw/workspace/SHARED_KNOWLEDGE.json 2>/dev/null | head -5
cat ~/.openclaw/workspace/IMPROVEMENT_BACKLOG.json 2>/dev/null | head -5
```
Capture: LanceDB presence, shared knowledge existence, improvement backlog existence.

### 9. Backup
```bash
ls ~/openclaw-backup-*.tar.gz 2>/dev/null
ls ~/.openclaw/backups/ 2>/dev/null
```
Capture: backup file existence and count.

### 10. Workspace
```bash
for f in openclaw.json models.json workspace/CLAUDE.md workspace/TASKS.json workspace/SPRINT_CURRENT.json workspace/SHARED_KNOWLEDGE.json workspace/IMPROVEMENT_BACKLOG.json; do
  [ -f ~/.openclaw/$f ] && echo "OK: $f" || echo "MISSING: $f"
done
```
Capture: core file presence/absence.

## Contextual Cross-Reference Rules

After gathering data, apply these IF/THEN rules. These compare results **across** scan areas — this is what differentiates `/oc-improve` from `/oc-doctor`.

### CRITICAL

| Condition | Finding |
|-----------|---------|
| agents > 1 AND no bindings configured | Multiple agents exist but no message routing bindings. All messages go to the default agent — other agents are unreachable. |
| agents > 1 AND dmScope is "main" or unset | Multiple agents share one session. Users and agents see each other's context. Session isolation is required. |
| gateway listen address is non-loopback AND auth is "none" or unset | Gateway is network-exposed with no authentication. Anyone on the network can send commands. |

### RECOMMENDED

| Condition | Finding |
|-----------|---------|
| channels > 1 AND any channel has dmPolicy "open" alongside a channel with "pairing" | Mixed DM policies — one channel requires pairing while another is open. An attacker could bypass pairing via the open channel. |
| agents > 1 AND sandbox mode is off or unset | Multiple agents without sandboxing. A compromised agent conversation could affect the host system. |
| config has been customized (non-default) AND no backups found | Custom configuration with no backups. A failed update or disk issue could lose your setup. |
| single model provider AND no fallback chain | Single provider with no failover. If the provider goes down, your gateway stops working. |
| any SOUL.md exists but has < 3 lines | SOUL.md files are present but nearly empty. Agents without behavioral guidance produce generic responses. |
| agents > 1 AND no IDENTITY.md in any workspace | Multi-agent setup without identity definitions. Agents won't know their role or boundaries. |

### NICE-TO-HAVE

| Condition | Finding |
|-----------|---------|
| no cron jobs AND no hooks configured | No automation configured. Cron jobs and hooks can automate maintenance, health checks, and workflows. |
| nodes paired (device list non-empty) but no exec routing configured | Nodes are paired but exec routing isn't set up. Paired devices can't receive remote commands. |
| no LanceDB directory AND agents > 1 | Multi-agent setup without vector memory. Shared semantic memory improves coordination. |

## Suggestion-to-Reference Mapping

For every finding, include the relevant skill and command using this mapping:

| Area | Skill | Command |
|------|-------|---------|
| Channels | `openclaw-channels` | `/oc-channel` |
| Agent setup | `openclaw-multi-agent`, `openclaw-agent-teams` | `/oc-team` |
| Team orchestration | `openclaw-multi-agent-team-setup` | `/oc-team` |
| Sessions | `openclaw-sessions` | `/oc-workspace sessions` |
| Security | `openclaw-security` | `/oc-security` |
| Sandbox | `openclaw-sandboxing` | `/oc-security` |
| Automation | `openclaw-automation` | `/oc-cron` |
| Models | `openclaw-models` | `/oc-config` |
| Memory | `openclaw-agent-teams` | `/oc-structure memory` |
| Backup | — | `/oc-backup` |
| Workspace | `openclaw-workspace-structure` | `/oc-structure audit` |

## Output Format

Present findings grouped by severity, highest first.

### CRITICAL (if any)
For each finding:
- **Finding**: what was detected
- **Context**: why it matters given *this specific setup* (reference actual values from scans)
- **Fix**: exact command or config change to resolve it
- **Reference**: skill name + slash command

### RECOMMENDED (if any)
Same format as CRITICAL.

### NICE-TO-HAVE (if any)
Same format but briefer — one-line context is sufficient.

### Summary Footer
```
Setup Scan Complete:
  Critical:     X finding(s)
  Recommended:  Y finding(s)
  Nice-to-have: Z finding(s)

Top priority: [describe the single most important action]
```

## If No Findings

Report a clean scan:
```
Your OpenClaw setup looks solid — no improvements found.
```

Suggest re-running after making configuration changes.

## After Running

- If critical findings exist: strongly recommend addressing them immediately, offer to help with the top item
- Suggest running `/oc-doctor` for automated fixes where available
- Mention re-running `/oc-improve` after changes to verify improvements
- If `--focus` was used, suggest a full scan to check for cross-area issues
