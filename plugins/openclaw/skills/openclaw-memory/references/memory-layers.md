# Memory Layers — Deep Dive

Detailed reference for each of the four memory layers in the OpenClaw agent memory model.

## Layer 1: Bootstrap Files

### What Loads When

| File | Load Trigger | Typical Size |
|------|-------------|-------------|
| AGENTS.md | Every session start (first file read) | 50-150 lines |
| SOUL.md | Every session start (after AGENTS.md) | 100-500 lines |
| IDENTITY.md | Every session start | 10-30 lines |
| USER.md | Private sessions only | 20-50 lines |
| MEMORY.md | Private sessions only | Up to 200 lines |
| TOOLS.md | On demand / when tool usage needed | 30-100 lines |
| HEARTBEAT.md | On heartbeat cron trigger | 5-20 lines |

### Sub-Agent Visibility

Sub-agents (spawned via `sessions_spawn`) receive a minimal context:
- **AGENTS.md** — Safety rules and delegation instructions
- **TOOLS.md** — Available tools and integration notes

They do **not** receive: SOUL.md, IDENTITY.md, USER.md, MEMORY.md, HEARTBEAT.md. This is intentional — sub-agents are task-focused and don't need full persona context.

**Implication:** Any rule that must be followed by sub-agents must live in AGENTS.md, not SOUL.md.

### Per-File Line Budgets

| File | Recommended Max | Hard Limit |
|------|----------------|------------|
| MEMORY.md | 200 lines | 200 lines (enforced by SCRIBE) |
| SOUL.md | 300 lines | 500 lines (dilutes focus beyond this) |
| AGENTS.md | 100 lines | 150 lines |
| IDENTITY.md | 30 lines | 50 lines |
| USER.md | 50 lines | 100 lines |

## Layer 1.5: Daily Logs

### Location

```
<agent-workspace>/memory/YYYY-MM-DD.md
```

### Structure

Each daily log follows this template:

```markdown
# YYYY-MM-DD

## Decisions
- <decision made and rationale>

## Facts Learned
- <new information discovered>

## Actions Taken
- <significant actions performed>

## Open Questions
- <unresolved items to revisit>
```

### Retention & Archival

- **Active window:** 7-14 days of daily logs in `memory/`
- **Archive:** Processed logs move to `memory/archive/YYYY-MM-DD.md`
- **Deletion:** Archives older than 90 days can be safely deleted (all durable content extracted to MEMORY.md)

## Layer 2: Session Transcript

### Location

```
~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl
```

### Compaction Behavior

The session transcript grows as the conversation continues. When it approaches the context window limit:

1. **Detection:** System detects >80% context usage
2. **Summarization:** Older messages are summarized into a compact representation
3. **Loss risk:** Details in the summarized portion may be lost

### Pre-Compaction Flush

To protect important information from compaction loss:

1. Monitor context usage (implicit — watch for signs of approaching limits)
2. When nearing capacity, explicitly save unsaved facts:
   ```
   Write critical facts to memory/YYYY-MM-DD.md
   Update MEMORY.md if facts are long-term durable
   ```
3. After saving, compaction can proceed safely

### Token Budget

Context window size depends on the model:
- Claude Sonnet: ~200K tokens
- Claude Haiku: ~200K tokens
- Claude Opus: ~200K tokens

Effective budget is lower due to system prompt, tools, and bootstrap files consuming initial tokens.

## Layer 3: Retrieval Index (LanceDB)

### Setup

LanceDB stores vector embeddings at `~/.openclaw/memory/lancedb/`.

```bash
# Verify LanceDB is initialized
ls ~/.openclaw/memory/lancedb/

# Check indexed content count
openclaw context list
```

### Embedding Model

Configured in `~/.openclaw/models.json` under the embeddings section. Default uses the configured provider's embedding model.

### Search

- **Type:** MIPS (Maximum Inner Product Search)
- **Tool:** `memory_search` (available to orchestrator only)
- **Query:** Natural language query → embedded → nearest neighbors returned
- **Results:** Ranked by relevance score with source file paths

### Indexing

Content automatically indexed:
- MEMORY.md changes
- team-memory/ file changes
- SHARED_KNOWLEDGE.json updates

Not indexed (by default):
- Daily logs (too volatile)
- Session transcripts (ephemeral)

## Memory Decay Comparison

How different systems handle memory decay:

| System | Strategy | Retention | Compression |
|--------|----------|-----------|-------------|
| **OpenClaw SCRIBE** | Weekly compression, 200-line budget | Indefinite for durable facts | Manual curation + budget cap |
| **CrewAI** | Half-life decay | Exponential fade | Automatic score reduction |
| **MemGPT** | Summarization tiers | Indefinite with summaries | Automatic recursive summarization |
| **Mem0** | TTL (Time-to-Live) | Configurable per-fact | Automatic expiration |
| **Claude Code** | 200-line MEMORY.md cap | Indefinite within cap | User/agent manual curation |

OpenClaw's SCRIBE approach combines the best of manual curation (quality) with a hard budget (preventing bloat). The weekly cycle provides natural review points.
