---
name: openclaw-models
description: >
  Use when the user wants to change the AI model, configure model providers,
  set up API keys, add a custom provider, configure model failover, list
  available models, set up auth profiles, manage model selection, or
  configure image models in OpenClaw.
---

# OpenClaw Models & Providers

Guide the user through model selection, provider setup, failover, and per-agent model configuration.

## Model Selection

### Configuration

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
    },
  },
}
```

Model refs use `provider/model` format (e.g., `anthropic/claude-opus-4-6`).

### /model Command

Users can switch models in chat:
- `/model` — show current model
- `/model anthropic/claude-opus-4-6` — switch to a specific model
- `/model Sonnet` — switch using alias (if configured in catalog)

### Per-Agent Override

```json5
{
  agents: {
    list: [
      {
        id: "opus",
        model: { primary: "anthropic/claude-opus-4-6" },
      },
      {
        id: "fast",
        model: { primary: "anthropic/claude-haiku-4-5-20251001" },
      },
    ],
  },
}
```

## Provider Configuration

### Built-in Providers

OpenClaw supports many providers out of the box:
- **Anthropic** (claude-opus, claude-sonnet, claude-haiku)
- **OpenAI** (gpt-5.2, gpt-4.1, etc.)
- **OpenRouter** (unified gateway for multiple providers)
- **Amazon Bedrock**, **Google**, **Mistral**, **Ollama** (local), **vLLM** (local)
- And many more — see `openclaw onboard` for interactive setup

### Custom Providers

Add any OpenAI-compatible endpoint:
```json5
{
  models: {
    providers: {
      "my-custom": {
        apiKey: "${MY_API_KEY}",
        baseUrl: "https://api.example.com/v1",
      },
    },
  },
}
```

Then use as: `my-custom/model-name`.

### API Key Configuration

Three methods:
1. **Environment variable**: Set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.
2. **Config inline**: `models.providers.<name>.apiKey: "sk-..."`
3. **SecretRef** (recommended):
   ```json5
   {
     models: {
       providers: {
         openai: {
           apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
         },
       },
     },
   }
   ```

### Interactive Setup

```bash
openclaw onboard          # full setup with model selection
openclaw configure        # config wizard (model section)
```

## Auth Profiles

Per-agent auth profiles at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`:

- Each agent can have its own set of API keys
- Resolution order: per-agent auth profile → global config → environment

Auth profiles are **per-agent and never shared automatically**.

## Model Catalog / Allowlist

`agents.defaults.models` defines the catalog and acts as the allowlist for `/model`:

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
    },
  },
}
```

Users can only switch to models listed here via `/model`.

## Failover

Configure fallback models for reliability:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: [
          "openai/gpt-5.2",
          "openrouter/anthropic/claude-opus-4-6",
        ],
      },
    },
  },
}
```

- Failover triggers on provider errors, rate limits, or auth failures
- Endpoint health is tracked automatically
- Auth rotation happens transparently across configured providers

## Per-Provider Tool Policy

Restrict tools for specific providers:

```json5
{
  tools: {
    byProvider: {
      "google-antigravity": { profile: "minimal" },
      "openai/gpt-5.2": { allow: ["group:fs", "sessions_list"] },
    },
  },
}
```

Applied after base tool profile, before allow/deny lists — can only narrow the tool set.

## Image Model

```json5
{
  agents: {
    defaults: {
      imageModel: {
        primary: "anthropic/claude-sonnet-4-5",
      },
      imageMaxDimensionPx: 1200,  // downscale for vision-token savings
    },
  },
}
```

The image model is independent of the main chat model. Used for the `image` tool.

## Security Note

For tool-enabled agents, use the **strongest, latest-generation model**. Smaller/weaker models are significantly more susceptible to prompt injection and tool misuse.

See `references/provider-setup.md` for detailed per-provider examples.
