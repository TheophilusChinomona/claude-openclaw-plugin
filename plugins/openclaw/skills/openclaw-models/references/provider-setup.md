# Provider Setup Reference

## Per-Provider Configuration Examples

### Anthropic

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-opus-4-6" },
    },
  },
  // API key via env: ANTHROPIC_API_KEY
  // Or via config:
  models: {
    providers: {
      anthropic: { apiKey: "${ANTHROPIC_API_KEY}" },
    },
  },
}
```

### OpenAI

```json5
{
  agents: {
    defaults: {
      model: { primary: "openai/gpt-5.2" },
    },
  },
  models: {
    providers: {
      openai: { apiKey: "${OPENAI_API_KEY}" },
    },
  },
}
```

### OpenRouter

```json5
{
  models: {
    providers: {
      openrouter: { apiKey: "${OPENROUTER_API_KEY}" },
    },
  },
  agents: {
    defaults: {
      model: {
        primary: "openrouter/anthropic/claude-opus-4-6",
        fallbacks: ["openrouter/openai/gpt-5.2"],
      },
    },
  },
}
```

### Custom (OpenAI-Compatible)

```json5
{
  models: {
    providers: {
      "my-endpoint": {
        apiKey: "${MY_API_KEY}",
        baseUrl: "https://api.example.com/v1",
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "my-endpoint/my-model" },
    },
  },
}
```

### Ollama (Local)

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://localhost:11434/v1",
      },
    },
  },
  agents: {
    defaults: {
      model: { primary: "ollama/llama3.3" },
    },
  },
}
```

## Auth Profile File Format

Location: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`

```json
{
  "anthropic": {
    "apiKey": "sk-ant-..."
  },
  "openai": {
    "apiKey": "sk-..."
  },
  "openrouter": {
    "apiKey": "sk-or-..."
  }
}
```

Per-agent auth profiles override global provider config for that agent only.

## Failover Examples

### Cross-Provider Failover

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

Failover sequence:
1. Try `anthropic/claude-opus-4-6`
2. On failure → try `openai/gpt-5.2`
3. On failure → try `openrouter/anthropic/claude-opus-4-6`

### Per-Agent Failover

```json5
{
  agents: {
    list: [
      {
        id: "critical",
        model: {
          primary: "anthropic/claude-opus-4-6",
          fallbacks: ["openai/gpt-5.2"],
        },
      },
      {
        id: "chat",
        model: {
          primary: "anthropic/claude-haiku-4-5-20251001",
          // no fallback — fast model, accept failures
        },
      },
    ],
  },
}
```

## SecretRef for API Keys

### Environment Source

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

### File Source

```json5
{
  models: {
    providers: {
      anthropic: {
        apiKey: { source: "file", provider: "filemain", id: "/models/providers/anthropic/apiKey" },
      },
    },
  },
}
```

File-backed secrets stored in `~/.openclaw/secrets.json`.

### Exec Source

```json5
{
  channels: {
    googlechat: {
      serviceAccountRef: {
        source: "exec",
        provider: "vault",
        id: "channels/googlechat/serviceAccount",
      },
    },
  },
}
```

## Model Alias Examples

```json5
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "anthropic/claude-haiku-4-5-20251001": { alias: "Haiku" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
    },
  },
}
```

Users can then type `/model Opus` instead of the full provider/model string.

## Per-Agent Model Overrides

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic/claude-sonnet-4-5" },
    },
    list: [
      {
        id: "deep-work",
        model: { primary: "anthropic/claude-opus-4-6" },
      },
      {
        id: "quick-chat",
        model: { primary: "anthropic/claude-haiku-4-5-20251001" },
      },
    ],
  },
}
```
