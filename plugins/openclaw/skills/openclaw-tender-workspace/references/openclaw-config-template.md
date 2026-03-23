# openclaw.json Template

Merge this into the existing `~/.openclaw/openclaw.json` on the gateway.

Replace all `{placeholder}` values with client-specific data.

```json
{
  "_comment": "{company_short} Tender Team — Multi-Agent Config for OpenClaw",

  "agents": {
    "defaults": {
      "model": "{provider}/claude-sonnet-4-6",
      "contextTokens": 200000,
      "thinkingDefault": "low",
      "userTimezone": "{timezone}",
      "timeFormat": "24",
      "heartbeat": {
        "every": "0m"
      },
      "subagents": {
        "model": "{provider}/claude-sonnet-4-6",
        "maxConcurrent": 2,
        "runTimeoutSeconds": 900
      }
    },

    "list": [
      {
        "id": "{orchestrator_id}",
        "default": true,
        "name": "{agent_name}",
        "workspace": "~/.openclaw/workspace-{client}",
        "model": {
          "primary": "{provider}/claude-sonnet-4-6",
          "fallbacks": ["{fallback_provider}/anthropic/claude-sonnet-4-6"]
        },
        "identity": {
          "name": "{agent_name}",
          "emoji": "{emoji}"
        },
        "groupChat": {
          "mentionPatterns": ["@{orchestrator_id}", "@{agent_name}"],
          "requireMention": false
        },
        "tools": {
          "allow": ["read", "write", "exec", "web_search", "web_fetch"]
        },
        "heartbeat": {
          "every": "4h",
          "lightContext": true,
          "isolatedSession": true
        }
      },
      {
        "id": "scout",
        "name": "SCOUT",
        "workspace": "~/.openclaw/workspace-{client}/agents/scout",
        "model": {
          "primary": "{provider}/claude-sonnet-4-6",
          "fallbacks": ["{fallback_provider}/anthropic/claude-sonnet-4-6"]
        },
        "identity": {
          "name": "SCOUT",
          "emoji": "(magnifying glass)"
        },
        "groupChat": {
          "mentionPatterns": ["@scout", "@Scout", "@SCOUT"],
          "requireMention": true
        },
        "tools": {
          "allow": ["read", "write", "exec", "web_search", "web_fetch"]
        }
      },
      {
        "id": "filter",
        "name": "FILTER",
        "workspace": "~/.openclaw/workspace-{client}/agents/filter",
        "model": {
          "primary": "{provider}/claude-sonnet-4-6",
          "fallbacks": ["{fallback_provider}/anthropic/claude-sonnet-4-6"]
        },
        "identity": {
          "name": "FILTER",
          "emoji": "(chart)"
        },
        "groupChat": {
          "mentionPatterns": ["@filter", "@Filter", "@FILTER"],
          "requireMention": true
        },
        "tools": {
          "allow": ["read", "write"]
        }
      },
      {
        "id": "architect",
        "name": "ARCHITECT",
        "workspace": "~/.openclaw/workspace-{client}/agents/architect",
        "model": {
          "primary": "{provider}/claude-sonnet-4-6",
          "fallbacks": ["{fallback_provider}/anthropic/claude-sonnet-4-6"]
        },
        "identity": {
          "name": "ARCHITECT",
          "emoji": "(ruler)"
        },
        "groupChat": {
          "mentionPatterns": ["@architect", "@Architect", "@ARCHITECT"],
          "requireMention": true
        },
        "tools": {
          "allow": ["read", "write"]
        }
      },
      {
        "id": "auditor",
        "name": "AUDITOR",
        "workspace": "~/.openclaw/workspace-{client}/agents/auditor",
        "model": {
          "primary": "{provider}/claude-sonnet-4-6",
          "fallbacks": ["{fallback_provider}/anthropic/claude-sonnet-4-6"]
        },
        "identity": {
          "name": "AUDITOR",
          "emoji": "(checkmark)"
        },
        "groupChat": {
          "mentionPatterns": ["@auditor", "@Auditor", "@AUDITOR"],
          "requireMention": true
        },
        "tools": {
          "allow": ["read", "write"]
        }
      }
    ]
  },

  "bindings": [
    {
      "agentId": "{orchestrator_id}",
      "match": {
        "channel": "whatsapp",
        "accountId": "*"
      }
    }
  ],

  "channels": {
    "whatsapp": {
      "dmPolicy": "open",
      "textChunkLimit": 4000,
      "sendReadReceipts": true,
      "groups": {
        "*": {
          "requireMention": true
        }
      }
    }
  },

  "session": {
    "dmScope": "per-account-channel-peer",
    "reset": {
      "mode": "idle",
      "idleMinutes": 120
    }
  },

  "cron": {
    "jobs": [
      {
        "id": "scout-scan",
        "schedule": "0 */4 * * *",
        "agentId": "scout",
        "prompt": "Run your scheduled tender scan. Follow your SOUL.md search strategy. For each tender found, run new-tender.sh, download the PDF, extract text with pdf-to-text.sh, and write discovery.md. Check for duplicates first."
      },
      {
        "id": "filter-analysis",
        "schedule": "0 1,7,13,19 * * *",
        "agentId": "filter",
        "prompt": "Find tenders needing assessment (discovery.md exists but no assessment.md). For each, read the discovery.md and extracted tender text, score against the company profile following your SOUL.md methodology, and write assessment.md."
      },
      {
        "id": "{orchestrator_id}-briefing",
        "schedule": "30 5 * * *",
        "agentId": "{orchestrator_id}",
        "prompt": "Generate morning briefing. Check pipeline status, certificate expiries, and any new assessments. Compile briefing, update pipeline.md, and send email to {email}."
      }
    ]
  },

  "skills": {
    "load": {
      "extraDirs": ["~/.openclaw/workspace-{client}/skills"],
      "watch": true
    }
  },

  "tools": {
    "agentToAgent": {
      "enabled": false
    },
    "web": {
      "search": {
        "enabled": true,
        "maxResults": 10,
        "timeoutSeconds": 30
      },
      "fetch": {
        "enabled": true,
        "maxChars": 100000,
        "timeoutSeconds": 60
      }
    },
    "exec": {
      "timeoutSec": 300,
      "backgroundMs": 10000
    }
  },

  "messages": {
    "responsePrefix": "{emoji}",
    "queue": {
      "mode": "collect",
      "debounceMs": 2000
    }
  }
}
```

## Config Placeholders

| Placeholder | Example | Description |
|-------------|---------|-------------|
| `{provider}` | `codex` | Primary model provider |
| `{fallback_provider}` | `openrouter` | Fallback provider |
| `{timezone}` | `Africa/Johannesburg` | Client timezone |
| `{orchestrator_id}` | `nkosi` | Orchestrator agent ID (lowercase) |
| `{agent_name}` | `NKOSI` | Orchestrator display name |
| `{client}` | `tripli` | Workspace directory name |
| `{email}` | `tenders@tripli.co.za` | Briefing email address |
| `{emoji}` | (construction) | Response prefix emoji |

## Key Design Decisions

- **agentToAgent: false** — agents communicate through files, not direct messaging
- **dmScope: per-account-channel-peer** — each WhatsApp DM gets its own session
- **SCOUT + orchestrator get exec** — FILTER, ARCHITECT, AUDITOR are read+write only
- **heartbeat only on orchestrator** — subagents don't need periodic checks
- **extraDirs for shared skills** — workspace-level skills accessible to all agents
