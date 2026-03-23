---
name: openclaw-agent-updater
description: Surgically update existing OpenClaw agent workspace files based on conversational change requests — without rewriting the soul, persona, or hard limits. Use this skill when the user says things like "update the agent", "tell NEXUS about the new client", "HUNTER's ICP has changed", "add this to APEX's memory", "RPS paid their invoice", "change SENTINEL's heartbeat", "update the goals", "the client list changed", "add a new cron job", "remove the stale goal", "SCRIBE needs to know about ISO 14001 scope change", or any request to change, add, remove, or refresh content in an existing agent's workspace files. Also trigger when business state changes (new client, lost client, invoice paid, tender outcome, staff change, new service, pricing update) that should be reflected in agent memory. This skill identifies which files and sections need changing, shows exactly what will change before touching anything, makes surgical edits that preserve the persona soul, and outputs ready-to-apply file patches.
---

# OpenClaw Agent Updater

Surgically update existing OpenClaw agent workspace files based on business changes, conversational requests, and evolving context — without touching the soul.

## What This Skill Does

Agents go stale. A new client is signed, an invoice is paid, a service is deprecated, a goal is completed, a cron job needs adjusting. This skill handles all of it — precisely, surgically, with a preview before any change is made.

**What it NEVER changes** (soul-protected):
- `## Core Values` in SOUL.md
- `## Boundaries` in SOUL.md
- `## Vibe` in SOUL.md
- `## Communication Style` philosophy in SOUL.md
- `IDENTITY.md` entirely
- Any hard limit (`NEVER` rule) in AGENTS.md

**What it CAN change:**
- `## Context` section in SOUL.md (business facts, reporting lines, tools)
- `MEMORY.md` — any section (add clients, update invoices, log lessons)
- `GOALS.md` — add goals, update status, move to completed, change priorities
- `AGENTS.md` — workflows, tool access, escalation rules, report formats
- `HEARTBEAT.md` — checklist items
- `USER.md` — owner preferences or contact details
- `openclaw.json` — model, heartbeat interval, cron jobs, bindings, channel config

---

## Change Classification

Before making any edit, classify the incoming request:

| Change Type | Affects | Example |
|---|---|---|
| **Business event** | MEMORY.md, GOALS.md | "RPS paid the invoice", "New client: Tivanathi Phase 2" |
| **Goal update** | GOALS.md | "Mark the IBS website goal complete", "Add P1 goal for new tender" |
| **Client update** | MEMORY.md (client file) | "RPS contact is now Thabo Dlamini", "Tripli scope expanded" |
| **Context change** | SOUL.md context section | "We now also offer R&D tax consulting", "Reporting to APEX changed" |
| **Operational change** | AGENTS.md | "HUNTER's follow-up cadence is now 21 days max", "Add PITCH to NEXUS's doc workflow" |
| **Infrastructure change** | openclaw.json, HEARTBEAT.md | "Change SENTINEL to check every 4h", "Add new cron job for EDGE" |
| **Memory add** | MEMORY.md | "Remember that Givemore prefers WhatsApp voice notes" |
| **Lesson learned** | MEMORY.md (lessons section) | "Add: always confirm RPS audit dates 2 weeks out" |
| **Stale cleanup** | GOALS.md, MEMORY.md | "Remove the completed ESK tender goal", "Archive Tripli invoice" |

---

## Stage 1: Parse the Change Request

Extract from the user's message:

```
CHANGE REQUEST PARSED:
Agent(s) affected: [list — or "unknown — need to identify"]
Change type: [from classification table above]
Specific change: [what exactly needs to change]
Files affected: [MEMORY.md / GOALS.md / SOUL.md context / AGENTS.md / HEARTBEAT.md / openclaw.json]
Urgency: [immediate / next session / batch with other changes]
```

If the affected agent is ambiguous ("update the sales agent"), confirm which agent (HUNTER) before proceeding.

If multiple agents are affected by one change (e.g. "new client Acme Corp" → NEXUS memory + HUNTER memory + SCRIBE context), flag all of them.

---

## Stage 2: Locate the Section

Identify the exact section to change. Never ask the user to find it — work it out from the change type:

| Change | File | Section |
|---|---|---|
| New/updated client | MEMORY.md | `## Active Client Files` → client subsection |
| Invoice paid/overdue | MEMORY.md | `## Invoice Tracker` |
| Goal completed | GOALS.md | Move from `## Active Goals` to `## Completed Goals` |
| New goal | GOALS.md | `## Active Goals` — insert at correct priority level |
| Goal status update | GOALS.md | Find goal by name, update Status and Next action |
| New contact | MEMORY.md | `## Key Contacts` |
| New service/offering | SOUL.md | `## Context` → Services subsection |
| Lesson learned | MEMORY.md | `## Lessons Learned` |
| Heartbeat interval | openclaw.json | `agents.list[].heartbeat.every` |
| New cron job | openclaw.json or cron CLI | New entry |
| Tool access change | AGENTS.md | `## Tool Access` table |
| Context fact change | SOUL.md | `## Context` relevant subsection |
| HEARTBEAT checklist | HEARTBEAT.md | Relevant checklist item |

---

## Stage 3: Preview Before Patching

**Always show the before/after before writing anything.**

Format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHANGE PREVIEW — [AGENT NAME] / [FILE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECTION: [section name]
ACTION: [Replace / Add / Remove / Update field]

BEFORE:
[existing content — or "Section does not exist yet" for additions]

AFTER:
[new content]

Soul-protected: [None affected / list any soul-adjacent edits flagged]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Confirm? (yes / adjust / cancel)
```

Wait for explicit confirmation before writing. Never auto-apply.

---

## Stage 4: Apply the Patch

After confirmation, output the complete updated section (not just the diff — full section text ready to paste):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PATCH APPLIED — [AGENT NAME] / [FILE]
Section: [name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Full updated section — ready to copy-paste into the file]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To apply on server:
  nano ~/.openclaw/workspace-[agentid]/[FILE.md]
  [or] openclaw config set [field] "[value"]  (for openclaw.json changes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For `openclaw.json` changes, produce the CLI command where possible:
```bash
openclaw config set agents.list[?(@.id=="sentinel")].heartbeat.every "4h"
# OR if complex: edit ~/.openclaw/openclaw.json directly — provide the exact JSON5 block
```

---

## Batch Updates

When multiple changes hit at once (e.g. "weekly catchup — here's what happened this week"), batch them:

1. Parse all changes from the message
2. Group by agent and file
3. Show all previews together (one block per file per agent)
4. Single confirmation covers all
5. Output all patches in sequence

Batch preview format:
```
━━━ BATCH UPDATE — [N] changes across [M] agents ━━━

[1/N] NEXUS / MEMORY.md — Update RPS invoice status
[2/N] NEXUS / GOALS.md — Mark ESK tender goal complete
[3/N] HUNTER / MEMORY.md — New lesson learned
[4/N] APEX / GOALS.md — Update pipeline target status

Confirm all? (yes / review individually / cancel)
```

---

## Common Update Patterns

### Client invoice paid
```
MEMORY.md → Invoice Tracker
Change: status from "Outstanding" to "Paid — [date]"
Also check: any GOALS.md goal about this invoice → mark complete
```

### New client onboarded
```
MEMORY.md → Active Client Files → add new client subsection
GOALS.md → may need new goal for client delivery
SOUL.md context → only if client changes the agent's operating context
Also update: NEXUS (ops), HUNTER (won deal), SCRIBE (if SHEQ client)
```

### Goal completed
```
GOALS.md:
1. Remove from ## Active Goals
2. Add to ## Completed Goals: "- [COMPLETE] [goal title] — [completion date]"
Also: update any Milestones table entry to ✅ Complete
```

### Lesson learned
```
MEMORY.md → ## Lessons Learned
Add: "- [lesson]: [context with enough detail to be actionable]"
```

### Heartbeat interval change
```
openclaw.json: agents.list[id=agentid].heartbeat.every = "new-interval"
CLI: openclaw config set ... OR direct file edit
```

### New cron job
```
Output: complete openclaw cron add CLI command, ready to run
Include: --name, --cron/--every, --tz, --agent, --session, --message, --model, delivery flags
```

---

## Multi-Agent Cascade

Some business events ripple across multiple agents. Always check:

| Event | Agents to update |
|---|---|
| New client signed | NEXUS (client file), HUNTER (won deal + pipeline), SCRIBE (if SHEQ), APEX (goals) |
| Invoice paid | NEXUS (invoice tracker + goals), APEX (revenue/goals) |
| Tender submitted | NEXUS (tender tracker), HUNTER (pipeline), APEX (goals) |
| Tender won | All of the above + SIGNAL (case study potential), SCRIBE (scope confirmed) |
| Tender lost | HUNTER (lost reason log), EDGE (loss analysis) |
| New service launched | SOUL.md context (all relevant agents), SIGNAL (content), HUNTER (offer) |
| Staff/contact change | MEMORY.md key contacts (all agents that held the contact) |
| Infrastructure change | SENTINEL (monitoring scope), APEX (context), openclaw.json |

When a cascade is detected, list all affected agents and let the user choose which to update in this session.

---

## Safety Rules

- **Preview always required** — never auto-apply any change
- **Soul-protected sections are absolute** — if a requested change would touch Core Values, Boundaries, or Vibe, refuse and explain why
- **Preserve existing structure** — don't reorganise sections while updating content
- **Preserve voice** — edits must match the agent's established tone and style
- **One confirmation per batch** — don't ask N times for N changes in the same request
- **Flag ambiguity** — if unclear which agent or section, ask once before proceeding
