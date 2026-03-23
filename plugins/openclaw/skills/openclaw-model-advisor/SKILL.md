---
name: openclaw-model-advisor
description: >
  Audit one or more OpenClaw agents, analyse what they require (complexity,
  tool use, context window, volume, autonomy, sensitivity), and recommend the
  best-fit OpenRouter models by pricing tier with ready-to-paste openclaw.json
  config snippets. Use when the user says "what model should I use", "recommend
  a model for my agent", "audit my agent models", "find a cheaper model",
  "openrouter model suggestions", "which model fits my agent", or invokes
  /openclaw-model-advisor.
---

# OpenClaw Model Advisor

Audit one or more OpenClaw agents and recommend the best-fit OpenRouter models
by pricing tier, based on what each agent actually needs.

---

## References

| Source | URL |
|--------|-----|
| OpenRouter Model Catalog | https://openrouter.ai/models |
| OpenRouter Tool-Calling Collection | https://openrouter.ai/collections/tool-calling-models |
| OpenRouter Free Models Collection | https://openrouter.ai/collections/free-models |
| OpenRouter Pricing Page | https://openrouter.ai/pricing |
| OpenRouter Tool-Calling Docs | https://openrouter.ai/docs/guides/features/tool-calling |
| OpenRouter Model Docs | https://openrouter.ai/docs/guides/overview/models |
| TeamDay Best Models Guide (Mar 2026) | https://www.teamday.ai/blog/top-ai-models-openrouter-2026 |
| TeamDay Free Models Guide (Mar 2026) | https://www.teamday.ai/blog/best-free-ai-models-openrouter-2026 |
| OpenRouter Pricing Calculator | https://costgoat.com/pricing/openrouter |
| Free Models That Work for Agents | https://brainroad.com/openrouter-free-models-which-ones-actually-work-for-ai-agents/ |
| LLM API Pricing Mar 2026 | https://www.tldl.io/resources/llm-api-pricing-2026 |
| AI API Pricing Comparison 2026 | https://intuitionlabs.ai/articles/ai-api-pricing-comparison-grok-gemini-openai-claude |

---

## OpenRouter Model Tiers (March 2026)

Prices are per million tokens (input / output). All models use OpenRouter's
`provider/model-id` format in openclaw.json.

### Tier 0 — Free (Rate-limited: 20 req/min, 200 req/day)

> Use for: development, low-volume personal agents, testing.
> **Not suitable for production or high-frequency autonomous agents.**

| Model | OpenRouter ID | Context | Strengths |
|-------|--------------|---------|-----------|
| Qwen3 Coder 480B | `qwen/qwen3-coder-480b-a35b-instruct:free` | 262K | Best free coding model; tool calling |
| Qwen3 235B A22B | `qwen/qwen3-235b-a22b:free` | 128K | MoE; reasoning + tool calling |
| NVIDIA Nemotron Nano 30B | `nvidia/nemotron-3-nano-30b-a3b:free` | 128K | Efficient MoE; agentic dev tasks |
| Gemma 3 27B | `google/gemma-3-27b-it:free` | 128K | Vision + tools |
| Llama 3.3 70B | `meta-llama/llama-3.3-70b-instruct:free` | 128K | GPT-4 level general quality |

**Free tier caveats**: Rate limits break autonomous loops. Never use `:free` models
as the primary in a heartbeat agent or cron-triggered workflow.

---

### Tier 1 — Budget (≤$0.30/M input)

> Use for: high-volume simple agents, summarisation, triage, notifications,
> memory-write agents.

| Model | OpenRouter ID | Input | Output | Context | Strengths |
|-------|--------------|-------|--------|---------|-----------|
| MiMo-V2-Flash | `xiaomi/mimo-v2-flash` | $0.09 | $0.29 | 256K | #1 open-source; ~Claude Sonnet 4.5 quality at 3.5% cost; hybrid thinking; tool calling |
| Gemini Flash Lite | `google/gemini-2.5-flash-lite` | $0.10 | $0.40 | 1M | Fastest Gemini; high-volume tasks |
| Gemini 3.1 Flash Lite | `google/gemini-3.1-flash-lite` | $0.25 | $1.50 | 1M | Outperforms 2.5 Flash Lite; Google's fastest |
| Grok 4.1 Fast | `x-ai/grok-4.1-fast` | $0.20 | $0.50 | 2M | Best xAI tool-calling model; customer support & deep research |
| DeepSeek V3.2 | `deepseek/deepseek-v3.2` | $0.26 | $0.38 | 163K | ~90% of GPT-5.4 quality at 1/50th cost; strong agentic tool use |
| MiniMax M2.5 | `minimax/minimax-m2.5` | $0.20 | $1.17 | 196K | 80.2% SWE-Bench Verified; strong office/productivity agents |

---

### Tier 2 — Mid ($0.30–$3/M input)

> Use for: complex reasoning agents, code generation, multi-step workflows,
> agents that need reliable tool use at scale.

| Model | OpenRouter ID | Input | Output | Context | Strengths |
|-------|--------------|-------|--------|---------|-----------|
| Claude Haiku 4.5 | `anthropic/claude-haiku-4-5-20251001` | $1.00 | $5.00 | 200K | Fast; extended thinking; full tool/computer-use support |
| Gemini 2.5 Pro | `google/gemini-2.5-pro` | $1.25 | $10.00 | 1M | Strong reasoning; multimodal |
| GPT-5 | `openai/gpt-5` | $1.25 | $10.00 | 1M | Broad capability |
| GPT-5.4 | `openai/gpt-5.4` | $2.50 | $15.00 | 1M | Built-in computer use; unified Codex+GPT |
| Claude Sonnet 4.6 | `anthropic/claude-sonnet-4-6` | $3.00 | $15.00 | 200K | Best mid-tier agent model; iterative dev, codebase nav, computer use |

---

### Tier 3 — Premium ($3+/M input)

> Use for: mission-critical agents, long-running autonomous workflows, sensitive
> data, agents where errors are expensive.

| Model | OpenRouter ID | Input | Output | Context | Strengths |
|-------|--------------|-------|--------|---------|-----------|
| Grok 3 | `x-ai/grok-3` | $3.00 | $15.00 | 131K | Strong reasoning; real-time data |
| Claude Opus 4.6 | `anthropic/claude-opus-4-6` | $5.00 | $25.00 | 200K | Strongest Anthropic model; full agent workflows; security-hardened |
| GPT-5.4 Pro | `openai/gpt-5.4-pro` | $30.00 | $180.00 | 1M | Maximum capability; only for extreme use cases |

---

## Audit Procedure

### Step 1 — Discover Agents

Ask the user which agents to audit. Offer these options:
- **All agents**: scan `~/.openclaw/` for all workspace directories
- **Single agent**: user provides the path or agent ID
- **Active openclaw.json**: read model assignments from `~/.openclaw/openclaw.json`

For each agent found, locate:
- `SOUL.md` — role, personality, scope
- `AGENTS.md` — rules, tools, workflows, memory instructions
- `IDENTITY.md` — name, status
- `GOALS.md` — what it's trying to achieve (if present)
- `HEARTBEAT.md` — autonomous schedule (if present)
- `openclaw.json` or the global config — current model assignment

### Step 2 — Score Each Agent on 6 Requirement Dimensions

For each agent, score 1–5 on each dimension by reading SOUL.md and AGENTS.md:

#### 2a. Task Complexity (1–5)

| Score | Signal in workspace files |
|-------|--------------------------|
| 1 | Simple Q&A, FAQ lookup, single-step responses |
| 2 | Summarisation, triage, basic memory writes |
| 3 | Multi-step reasoning, research, drafting |
| 4 | Code generation, complex agentic workflows |
| 5 | Deep coding, system design, long-horizon planning |

#### 2b. Tool Use Intensity (1–5)

| Score | Signal |
|-------|--------|
| 1 | No tools listed in AGENTS.md |
| 2 | 1–2 simple tools (search, send message) |
| 3 | 3–5 tools with conditional logic |
| 4 | 6+ tools, chained tool calls, external APIs |
| 5 | Computer use, bash execution, file system, browser |

#### 2c. Context Window Need (1–5)

| Score | Signal |
|-------|--------|
| 1 | Short conversations, no documents |
| 2 | Single document < 10K tokens |
| 3 | Multiple documents or long chat history |
| 4 | Whole codebase, large reports, 50K+ tokens |
| 5 | Multi-document, multi-session, 100K+ tokens |

#### 2d. Response Volume (1–5)

| Score | Signal |
|-------|--------|
| 1 | < 10 messages/day, manual trigger only |
| 2 | 10–50 messages/day |
| 3 | 50–200 messages/day |
| 4 | 200–1000 messages/day |
| 5 | 1000+ messages/day or high-frequency cron |

#### 2e. Autonomy Level (1–5)

| Score | Signal in HEARTBEAT.md / AGENTS.md |
|-------|-------------------------------------|
| 1 | Human-initiated only, supervised |
| 2 | Occasional autonomous tasks, human reviews output |
| 3 | Regular autonomous tasks with occasional check-ins |
| 4 | Full heartbeat schedule, minimal supervision |
| 5 | Fully autonomous 24/7, no human in loop |

#### 2f. Sensitivity (1–5)

| Score | Signal |
|-------|--------|
| 1 | Public info only, no private data |
| 2 | Business-internal data |
| 3 | Client data, business financials |
| 4 | Credentials, auth tokens, personal data |
| 5 | Highly sensitive: financial, medical, legal, security systems |

### Step 3 — Calculate Composite Score & Assign Tier

```
Composite = (Complexity × 2) + (Tool Use × 2) + Context + Volume + (Autonomy × 1.5) + (Sensitivity × 1.5)
Max = 60
```

| Composite Score | Recommended Tier |
|----------------|-----------------|
| 0–20 | Tier 0 (Free) or Tier 1 (Budget) |
| 21–35 | Tier 1 (Budget) |
| 36–45 | Tier 2 (Mid) |
| 46–60 | Tier 2–3 (Mid to Premium) |

**Override rules** (apply regardless of composite score):
- Sensitivity ≥ 4 → minimum **Tier 2**
- Sensitivity = 5 → minimum **Tier 3** (Claude Opus recommended)
- Autonomy = 5 → **never use free tier**; minimum **Tier 1**
- Tool Use ≥ 4 → must use a model with confirmed tool-calling support
- Context ≥ 4 → must use a model with ≥ 100K context window

### Step 4 — Select Recommended Models

For each tier, present:
1. **Best Fit** — optimal balance of capability and cost for this agent's profile
2. **Cheaper Alternative** — one tier down if the agent could manage
3. **Upgrade Option** — one tier up if reliability/quality needs to increase

Use the model table above. Prefer these combinations based on agent type:

| Agent Type | Best Fit | Cheaper Alt | Upgrade |
|------------|----------|-------------|---------|
| Simple assistant / FAQ | `xiaomi/mimo-v2-flash` | `qwen/qwen3-235b-a22b:free` | `anthropic/claude-haiku-4-5-20251001` |
| Triage / email classifier | `deepseek/deepseek-v3.2` | `xiaomi/mimo-v2-flash` | `anthropic/claude-haiku-4-5-20251001` |
| Research / summarisation | `deepseek/deepseek-v3.2` | `google/gemini-3.1-flash-lite` | `anthropic/claude-sonnet-4-6` |
| Productivity / office agent | `minimax/minimax-m2.5` | `deepseek/deepseek-v3.2` | `anthropic/claude-sonnet-4-6` |
| Code generation / dev agent | `anthropic/claude-sonnet-4-6` | `xiaomi/mimo-v2-flash` | `anthropic/claude-opus-4-6` |
| Agentic with tool chains | `x-ai/grok-4.1-fast` | `deepseek/deepseek-v3.2` | `anthropic/claude-sonnet-4-6` |
| Autonomous 24/7 heartbeat | `deepseek/deepseek-v3.2` | `x-ai/grok-4.1-fast` | `anthropic/claude-sonnet-4-6` |
| Sensitive data / security | `anthropic/claude-sonnet-4-6` | — | `anthropic/claude-opus-4-6` |
| Mission-critical / long-run | `anthropic/claude-opus-4-6` | `anthropic/claude-sonnet-4-6` | — |

### Step 5 — Generate openclaw.json Snippet

For each agent, produce a ready-to-paste config block:

```json5
// Agent: <agent-name>
// Role: <one-line role from SOUL.md>
// Tier: <tier> | Composite score: <score>/60
// Recommended: <model-id>
{
  agents: {
    list: [
      {
        id: "<agent-id>",
        model: {
          primary: "<recommended-model-id>",
          fallbacks: ["<cheaper-alt-id>"],
        },
      },
    ],
  },
}
```

If the agent is autonomous (Autonomy ≥ 4), also recommend adding at least one
paid-tier fallback — never leave a free model as the only fallback for a
heartbeat agent.

### Step 6 — Present Summary Report

Output a single table covering all audited agents:

```
## Model Advisor Report

| Agent | Complexity | Tool Use | Context | Volume | Autonomy | Sensitivity | Score | Tier | Recommended Model |
|-------|-----------|----------|---------|--------|----------|-------------|-------|------|-------------------|
| ...   |           |          |         |        |          |             |       |      |                   |

### Cost Estimate

Estimated monthly cost at current volume:
- <Agent A>: ~$X.XX/month at <tier> using <model>
- <Agent B>: ~$X.XX/month at <tier> using <model>

### Key Recommendations

1. ...
2. ...

### Next Steps

- To apply: paste the config snippets above into your openclaw.json
- To verify model availability: run `openclaw model list` or visit https://openrouter.ai/models
- To update the model live: `/model <provider/model-id>` in any chat session
- Pricing may change — always verify current rates at https://openrouter.ai/pricing
```

---

## Quick Reference — Model Selection Heuristic

```
Is the agent autonomous (heartbeat/cron)?
  YES → Never use :free tier
  NO  → Free tier OK for dev/low-volume

Does it use 4+ tools or computer use?
  YES → Claude Sonnet/Opus, Grok 4.1 Fast, or GPT-5.4
  NO  → DeepSeek V3.2 or MiMo-V2-Flash are excellent

Does it handle sensitive data (score ≥4)?
  YES → Claude Sonnet minimum; Opus for score 5
  NO  → Any tier appropriate to complexity

Is cost the primary concern?
  YES → DeepSeek V3.2 ($0.26/$0.38) gives best value/quality ratio
  NO  → Claude Sonnet 4.6 is the safest all-round choice

Need 1M+ context window?
  YES → Gemini 3.1 Flash Lite, Grok 4.1 Fast (2M), or GPT-5/5.4
```

---

## Integration with Other Skills

After running this audit:
- **Current model is wrong tier** → apply the generated snippets to `openclaw.json`
- **Agent has no tools but needs them** → run `openclaw-agent-architect` to redesign SOUL + AGENTS
- **Agent is autonomous but has no failover** → run `openclaw-config` to add failover config
- **Model spend too high across team** → consider `openclaw-multi-agent` to route cheaper models to simple agents

Always verify current pricing before committing to a model:
→ https://openrouter.ai/pricing
→ https://openrouter.ai/models
