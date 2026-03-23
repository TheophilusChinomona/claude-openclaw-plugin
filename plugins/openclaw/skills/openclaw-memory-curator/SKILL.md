---
name: openclaw-memory-curator
description: Audit, clean, and curate OpenClaw agent memory — reading daily memory logs, extracting durable facts, removing stale or contradictory entries, promoting important patterns to MEMORY.md, and keeping agent knowledge sharp and current. Use this skill when the user wants to clean up agent memory, says the agent seems to be "forgetting" things or repeating itself, wants to consolidate daily logs into long-term memory, notices the agent has stale or incorrect information, or asks to "review the agent's memory", "clean up the memory", "update what the agent knows", or "curate the memory files". Also trigger on a scheduled quarterly review or when significant time has passed since agents were last deployed (2+ months).
---

# OpenClaw Memory Curator

Audit, clean, and curate agent memory — keeping MEMORY.md accurate, relevant, and lean as the business evolves.

## Why Memory Degrades

Agent memory goes stale in predictable ways:
- **Completed goals stay in Active** — nothing moves them to Completed
- **Old client data persists** — invoices that were paid still show "outstanding"
- **Daily logs accumulate** — valuable facts buried in chronological noise
- **Contradictions build up** — the agent was told X, then later told Y, both remain
- **Lessons get forgotten** — buried in daily logs, never promoted to MEMORY.md

This skill fixes all of it systematically.

---

## Stage 1: Memory Audit

For the agent(s) being curated, request or read:
1. `MEMORY.md` (if it exists)
2. Recent `memory/YYYY-MM-DD.md` daily logs (last 30-90 days)
3. `GOALS.md`

If files are on the server, user provides them as uploads or pastes.

**Audit checklist:**

```
MEMORY AUDIT — [Agent Name] — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEMORY.md:
□ Last updated date: [date]
□ Stale client entries: [list any clients with outdated status]
□ Stale invoice entries: [outstanding invoices older than 60 days]
□ Outdated contact details: [any contacts marked [TBC] or [confirm]]
□ Contradictions found: [any section where two facts conflict]
□ Sections that need adding: [what's missing that should be there]

DAILY LOGS:
□ Days reviewed: [n days]
□ Durable facts found: [facts worth promoting to MEMORY.md]
□ Completed goals found: [goals referenced as done but still in Active]
□ New lessons found: [lessons that should go to Lessons Learned]

GOALS.md:
□ Goals marked complete in conversation but still in Active
□ Goals with status "Not started" for 60+ days — still relevant?
□ Missing goals from recent work
□ Milestones table accurate?
```

---

## Stage 2: Extract Durable Facts from Daily Logs

Read daily logs and extract facts worth keeping in MEMORY.md:

**Promote to MEMORY.md when:**
- A new client relationship was established
- An invoice was paid or a financial decision was made
- A process lesson was learned from experience
- A contact's details or role changed
- A service was added, changed, or removed
- A preference was stated by Tino or a client
- A goal was completed

**Leave in daily logs (don't promote):**
- One-time status updates
- In-progress notes that resolved
- Conversational context
- Draft content that was superseded

**Format for promoted facts:**
```markdown
- [Fact]: [Context — enough to be actionable without reading the log]
  Source: daily log [YYYY-MM-DD]
```

---

## Stage 3: Produce the Curated Update

Present the full set of proposed changes before applying:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY CURATION REPORT — [AGENT NAME]
Logs reviewed: [date range]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CHANGES PROPOSED: [N total]

MEMORY.md CHANGES:
[1] UPDATE: Client: RPS Switchgear SA — Invoice status
    FROM: "Outstanding — invoice submitted March 2026"
    TO: "Paid — received April 2026"

[2] ADD: Lessons Learned
    "Always confirm Stage 2 audit date with client 2 weeks prior — RPS needed reminder"

[3] REMOVE: Stale entry
    "Tivanathi contact: [TBC]" — still unresolved after 60 days — flag to Tino

GOALS.md CHANGES:
[4] COMPLETE: "Build IBS Website" — referenced as live in log 2026-03-28
[5] ADD: "P1 — Secure second SHEQ retainer client by Q3 2026"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Confirm all? (yes / review individually / cancel)
```

---

## Stage 4: Apply Curated Updates

After confirmation, produce the complete updated sections — ready to paste into files.

Also produce a curation summary to log in the agent's MEMORY.md:

```markdown
## Memory Curation Log

| Date | Curated by | Changes | Notes |
|---|---|---|---|
| 2026-06-01 | Tino (via memory-curator skill) | 5 updates | RPS invoice marked paid; IBS website goal completed |
```

---

## Stage 5: Cross-Agent Consistency Check

When curating a team (multiple agents), check that shared facts are consistent:

```
CROSS-AGENT CONSISTENCY CHECK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CLIENT DATA:
- RPS Switchgear SA invoice status: APEX says "outstanding", NEXUS says "paid" ⚠️ CONFLICT
  → Update APEX to match NEXUS (paid April 2026)

CONTACT DATA:
- Givemore Chinomona contact: All agents consistent ✅

GOAL DATA:
- "ESK tender outcome" goal: APEX = monitoring, HUNTER = closed lost ⚠️ CONFLICT
  → Need Tino to confirm status before updating

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Any conflict requires Tino's confirmation before resolution.

---

## Curation Schedule Recommendation

| Frequency | Trigger |
|---|---|
| Monthly | EDGE monthly review includes memory health check |
| Quarterly | Full memory audit across all agents |
| On-demand | After a significant business event (new client, tender outcome, etc.) |
| On-deploy | Before any agent workspace is handed to a new person |

EDGE's GOALS.md should include a recurring goal:
```
### [P2] Monthly Memory Health Check
- Target: Ongoing — first Monday of each month
- Next action: Review MEMORY.md and daily logs for all active agents
```
