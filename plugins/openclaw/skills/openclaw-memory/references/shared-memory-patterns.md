# Shared Memory Patterns

Patterns for cross-agent knowledge sharing in OpenClaw multi-agent setups.

## Namespace Hierarchy

Four levels of memory scope, from broadest to narrowest:

| Level | Location | Scope | Format |
|-------|----------|-------|--------|
| System | `~/.openclaw/workspace/SHARED_KNOWLEDGE.json` | All agents | JSON key-value |
| Team | `team-memory/` | All team agents | Markdown files |
| Agent | `agents/<id>/MEMORY.md` | Single agent | Markdown |
| Group | `agents/<id>/GROUP_MEMORY.md` | Agent in group contexts | Markdown |

### When to Use Each Level

- **System:** Facts that every agent needs (company name, timezone, core product)
- **Team:** Domain knowledge shared by a working group (market data, ICP, brand voice)
- **Agent:** Private knowledge specific to one agent's role and history
- **Group:** Subset of agent knowledge safe to reference in shared channels

## Access Control by Agent Tier

| Tier | team-memory/ | SHARED_KNOWLEDGE.json | Other agents' MEMORY.md | Own MEMORY.md |
|------|-------------|----------------------|------------------------|---------------|
| Orchestrator | Read + Write | Read + Write | Read | Read + Write |
| Team Lead | Read all, Write own domain files | Read | No access | Read + Write |
| Specialist | Read-only | Read | No access | Read + Write |

### Enforcement

Access control is enforced via rules in each agent's SOUL.md:

```markdown
## Shared Memory Access
- I may read any file in team-memory/
- I may write to team-memory/market-brief.md and team-memory/icp-profile.md (my domain)
- I must not read other agents' MEMORY.md files
- I must not write to team-memory/ files outside my domain
```

## Conflict Resolution

### Facts (newest-wins)

When two agents write conflicting factual claims:
- The most recently timestamped entry wins
- The losing entry is removed or updated
- Example: Agent A says "ICP is Series B startups", Agent B later says "ICP expanded to include Series A" — Series A+B is the current truth

### Events (append-only)

Event logs are never overwritten:
- Each entry includes a timestamp and agent ID
- Conflicting events both remain (they represent different observations)
- Example: Agent A logged "email sent to prospect X", Agent B logged "prospect X replied" — both are true events

### Contradictions

When persistent contradictions exist:
- SCRIBE flags them during weekly compression
- Orchestrator or team lead resolves by choosing the authoritative source
- Resolution is logged in the daily log for transparency

## Example team-memory/ Files

### market-brief.md

```markdown
# Market Brief

Last updated: 2026-03-10 by TRACE

## Target Market
B2B SaaS companies, 50-500 employees, Series A-C

## Key Trends
- AI-first tooling adoption accelerating in developer segment
- Budget consolidation pushing toward platform plays
- Security and compliance increasingly table stakes

## Competitive Landscape
- Competitor A: Strong in enterprise, weak in SMB
- Competitor B: Developer-focused, limited enterprise features
```

### icp-profile.md

```markdown
# Ideal Customer Profile

Last updated: 2026-03-08 by VERA

## Primary ICP
- **Company size:** 50-500 employees
- **Stage:** Series A through Series C
- **Industry:** Technology, SaaS
- **Pain point:** Managing multiple AI providers, lack of gateway control

## Decision Makers
- CTO / VP Engineering (technical buyer)
- Head of AI / ML Engineering (champion)
- CISO (security approver)

## Engagement Signals
- Active GitHub contributors
- Using 2+ AI providers
- Recent headcount growth in engineering
```

### brand-voice.md

```markdown
# Brand Voice Guide

Last updated: 2026-03-05 by ANCHOR

## Tone
- Professional but approachable
- Technical accuracy over marketing fluff
- Concise — respect the reader's time

## Terminology
- "AI gateway" not "AI proxy" or "AI router"
- "Self-hosted" not "on-premises"
- "Agents" not "bots" or "assistants"

## Prohibited
- Hype language ("revolutionary", "game-changing")
- Unverified claims about performance
- Competitor disparagement
```

### content-calendar.md

```markdown
# Content Calendar

Last updated: 2026-03-10 by HERALD

## This Week
- Mon: LinkedIn post — AI gateway security best practices
- Wed: Blog draft — "Why self-hosted AI gateways matter"
- Fri: Newsletter issue #12

## Next Week
- Mon: Case study draft (Customer X)
- Thu: LinkedIn post — Team orchestration patterns
```

## Subscription Pattern (Optional)

For teams that need real-time awareness of shared memory changes:

### Cron-Based File Watching

```bash
# Check for team-memory changes every 30 minutes
openclaw cron add --agent orchestrator \
  --schedule "*/30 * * * *" \
  --command "check-team-memory-updates"
```

The cron job checks file modification times in team-memory/ and notifies relevant agents when files in their domain are updated.

### Promotion Workflow

1. Specialist agent writes output to `agents/<id>/output/`
2. Team lead reviews output during their next cycle
3. If output contains team-relevant knowledge, team lead copies/merges to `team-memory/`
4. Other agents see the update on their next read of team-memory/

This review step prevents low-quality or speculative data from polluting shared memory.
