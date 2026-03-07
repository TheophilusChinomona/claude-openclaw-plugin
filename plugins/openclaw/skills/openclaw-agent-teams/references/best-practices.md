# Agent Team Best Practices — Full Implementation Guide

Source: ClawPort best practices (www.clawport.dev/best-practices)

## Example Team Structure

```
Jarvis (Orchestrator)
  |
  +-- VERA (Strategy)
  |     +-- Robin (Field Intel)
  |           +-- TRACE (Market Research)
  |           +-- PROOF (Validation Design)
  |
  +-- LUMEN (SEO)
  |     +-- SCOUT (Content Scout)
  |     +-- ANALYST (SEO Analyst)
  |     +-- STRATEGIST (Content Strategy)
  |     +-- WRITER (Content Writer)
  |     +-- AUDITOR (Quality Gate)
  |
  +-- HERALD (LinkedIn)
  |     +-- QUILL (LinkedIn Writer)
  |     +-- MAVEN (LinkedIn Strategist)
  |
  +-- Pulse (Trend Radar)      -- standalone
  +-- ECHO (Community Voice)   -- standalone
  +-- SAGE (ICP Expert)        -- standalone
  +-- KAZE (Flight Monitor)    -- standalone
  +-- SPARK (Tech Discovery)   -- standalone
  +-- SCRIBE (Memory Architect)-- standalone
```

Standalone agents report directly to the orchestrator. Keep direct reports under 8-10 — group them under a team lead if the list grows.

## Step 1: Set Up the Workspace

```bash
mkdir -p $WORKSPACE_PATH/{agents,team-memory,clawport}

# Per-agent directories
for agent in jarvis vera robin trace proof lumen scout \
  analyst strategist writer auditor herald quill maven \
  pulse echo sage kaze spark scribe; do
  mkdir -p $WORKSPACE_PATH/agents/$agent/{logs,output}
  touch $WORKSPACE_PATH/agents/$agent/MEMORY.md
  touch $WORKSPACE_PATH/agents/$agent/SOUL.md
done

# Shared team memory files
touch $WORKSPACE_PATH/team-memory/{market-brief,icp-profile,competitor-map,brand-voice,content-calendar}.md

# Root memory (orchestrator long-term memory)
touch $WORKSPACE_PATH/MEMORY.md
```

## Step 2: Write the Agent Registry

Create `$WORKSPACE_PATH/clawport/agents.json`:

```json
[
  {
    "id": "jarvis",
    "name": "Jarvis",
    "role": "Orchestrator",
    "emoji": "brain",
    "reportsTo": null,
    "directReports": ["vera", "lumen"],
    "tools": ["exec", "read", "write", "message", "sessions_spawn", "memory_search"],
    "soulPath": "agents/jarvis/SOUL.md",
    "memoryPath": "agents/jarvis/MEMORY.md",
    "voiceId": "your-elevenlabs-voice-id"
  },
  {
    "id": "vera",
    "name": "VERA",
    "role": "Chief Strategy Officer",
    "emoji": "chart_with_upwards_trend",
    "reportsTo": "jarvis",
    "directReports": ["robin"],
    "tools": ["read", "write", "sessions_spawn"],
    "soulPath": "agents/vera/SOUL.md",
    "memoryPath": "agents/vera/MEMORY.md",
    "voiceId": null
  }
]
```

### Registry Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Lowercase slug, unique identifier |
| `name` | Yes | Display name (UPPERCASE or Title Case) |
| `role` | Yes | Role title shown in UI |
| `emoji` | No | Emoji shortcode for org map |
| `reportsTo` | Yes | Parent agent ID, or `null` for root |
| `directReports` | Yes | Array of child agent IDs |
| `tools` | Yes | Array of allowed tool names |
| `soulPath` | Yes | Relative path to SOUL.md |
| `memoryPath` | Yes | Relative path to MEMORY.md |
| `voiceId` | No | ElevenLabs voice ID or `null` |

## Step 3: Write SOUL.md Files

Template:

```markdown
# AGENT_NAME -- Role Title

## Identity
I am AGENT_NAME, the [Role Title]. [Personality traits].
[Communication style]. [First-person voice].

## Expertise
- Domain area 1
- Domain area 2
- What I defer to others

## Operating Rules
- Hard constraint 1
- Hard constraint 2
- Output format requirements

## Relationships
- Reports to: [Parent] ([Role])
- Manages: [Child1], [Child2]
- Collaborates with: [Peer1], [Peer2]

## Memory
- What I remember between sessions
- Where my persistent knowledge lives
```

Example (VERA):

```markdown
# VERA -- Chief Strategy Officer

## Identity
I am VERA, the Chief Strategy Officer. I think in
frameworks, speak in recommendations, and always tie
analysis back to business impact. I am deliberate and precise.

## Expertise
- Go-to-market strategy and positioning
- Competitive analysis and market sizing
- Strategic planning and OKR design

## Operating Rules
- Always recommend, never just describe
- Include confidence levels on forecasts
- Defer to TRACE for raw market data
- Defer to SAGE for ICP questions

## Relationships
- Reports to: Jarvis (Orchestrator)
- Manages: Robin (Field Intel)
- Collaborates with: LUMEN, HERALD
```

## Step 4: SCRIBE Memory Compression Workflow

SCRIBE runs weekly to compress daily logs into curated MEMORY.md files:

```
SCRIBE weekly compression workflow:

1. For each agent in registry:
   a. Read agents/<id>/logs/*.md from the past 7 days
   b. Read agents/<id>/MEMORY.md (current state)
   c. Extract durable patterns, decisions, facts
   d. Discard session-specific noise
   e. Write updated MEMORY.md (keep under 200 lines)
   f. Archive processed logs to agents/<id>/logs/archive/

2. For team memory:
   a. Read all agents' latest output files
   b. Update team-memory/ files with fresh data
   c. Resolve contradictions (newest wins)
```

The 200-line budget is the simplest form of memory decay. When the file is full, less important entries get displaced by new ones.

## Step 5: Staggered Cron Schedule

```
# Monday - Research agents run first
06:00  ECHO       community-scan     # Subreddit monitoring
08:00  SCOUT      content-scan       # Topic discovery
10:00  TRACE      market-research    # Market intel

# Tuesday - Analysis layer reads research output
06:00  Pulse      trend-radar        # Cross-reference trends
08:00  ANALYST    seo-analysis       # Analyze SCOUT's topics

# Wednesday - Strategy layer reads analysis
06:00  STRATEGIST content-strategy   # Plan from ANALYST output
08:00  MAVEN      editorial-calendar # LinkedIn content plan

# Thursday - Production layer reads strategy
06:00  WRITER     content-draft      # Write from STRATEGIST brief
08:00  QUILL      linkedin-draft     # Write from MAVEN brief

# Friday - Quality + compression
06:00  AUDITOR    quality-gate       # Review WRITER output
08:00  SCRIBE     memory-compress    # Weekly memory compression
10:00  Jarvis     weekly-briefing    # Orchestrator summary

# Daily
09:00  KAZE       flight-monitor     # Flight price check
```

Key principle: upstream agents finish before downstream agents read their output.

## Tool Assignment Examples

```
// SAGE -- read-only knowledge agent
"tools": ["read"]

// SCOUT -- web researcher
"tools": ["web_search", "web_fetch", "read"]

// WRITER -- content producer
"tools": ["read", "write"]

// HERALD -- team lead running a pipeline
"tools": ["web_search", "web_fetch", "read", "write", "message", "exec"]

// Jarvis -- orchestrator with full access
"tools": ["exec", "read", "write", "edit", "web_search", "tts", "message", "sessions_spawn", "memory_search"]
```

## Memory Decay Comparison

| System | Decay? | Mechanism |
|--------|--------|-----------|
| CrewAI | Yes | Exponential half-life: `0.5^(age_days / 30)`. Composite score blends similarity (0.5), recency (0.3), importance (0.2). |
| MemGPT / Letta | Implicit | Recursive summarization. Older info diluted through compression. No explicit scoring. |
| Mem0 | Yes | TTL + relevance scoring. Auto-prunes low-signal memories. |
| OpenAI Agents SDK | Partial | Timestamp-based Top-K. LLM consolidation prunes stale notes. |
| LangChain | No | Sliding window or LLM summarization. No time/relevance awareness. |
| Claude Code | No | 200-line cap on MEMORY.md. Manual editorial judgment. |
| AutoGen | No | Memories persist until `clear()`. No pruning or compression. |
| Zep (Graphiti) | No | Bi-temporal invalidation. Contradictions mark old facts invalid but never delete. |
| **ClawPort** | Implicit | SCRIBE compression. Weekly cron is the half-life. No scoring formula needed. |

## Step 6: Launch ClawPort

```bash
# Install globally
npm install -g clawport-ui

# Auto-detect your OpenClaw config
clawport setup

# Launch the dashboard
clawport dev
```

ClawPort reads `agents.json`, renders the org map, connects to the OpenClaw gateway for chat, and displays memory files from your workspace.

## Voice System

- **Give voices to conversational agents** (Jarvis, VERA, Pulse) — agents you chat with.
- **Skip voices for pipeline workers** (SCOUT, ANALYST, WRITER) — they rarely need to speak.
- Set `voiceId` to `null` for agents without voice. The UI hides the TTS button.

## Quick Tips

- Start with 3 agents (orchestrator + one lead + one specialist) to validate patterns.
- Add agents when you find real needs, not because the org chart looks sparse.
- If you need more aggressive memory decay, shorten SCRIBE's compression window (e.g., every 3 days).
- Add a line budget to each agent's MEMORY.md for simple prioritization.
