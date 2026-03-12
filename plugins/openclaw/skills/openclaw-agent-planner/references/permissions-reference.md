# Permission & Capability Reference

Quick reference for common agent capability patterns. Use these as starting points when building permission matrices during Stage 2 design.

---

## Standard Capability Categories

### Communication
| Capability | Description |
|-----------|-------------|
| Send DM messages | Agent sends direct messages to users |
| Send group messages | Agent posts in group chats |
| Reply to messages | Agent responds to incoming messages |
| Initiate conversations | Agent starts conversations unprompted (heartbeat-driven) |
| Send media/files | Agent attaches images, documents, or files to messages |
| Read message history | Agent accesses prior messages in a channel |

### File System
| Capability | Description |
|-----------|-------------|
| File read (workspace) | Read files within its own workspace directory |
| File read (system) | Read files outside workspace |
| File write (workspace) | Create/modify files in workspace |
| File write (system) | Create/modify files outside workspace |
| File delete | Remove files |
| Directory listing | List contents of directories |

### Web & Research
| Capability | Description |
|-----------|-------------|
| Web search | Search the internet via Brave/Google/etc. |
| Web fetch | Retrieve full page content from URLs |
| API calls (read) | GET requests to external APIs |
| API calls (write) | POST/PUT/DELETE to external APIs |

### Calendar & Scheduling
| Capability | Description |
|-----------|-------------|
| Calendar read | View calendar events |
| Calendar create | Create new events |
| Calendar modify | Edit existing events |
| Calendar delete | Remove events |
| Send invites | Send calendar invitations to others |

### Email
| Capability | Description |
|-----------|-------------|
| Email read | Read incoming emails |
| Email draft | Compose draft emails |
| Email send | Send emails (requires careful governance) |
| Email delete/archive | Remove or archive emails |

### Shell & System
| Capability | Description |
|-----------|-------------|
| Shell read-only | Run commands that don't modify state (ls, cat, ps, df) |
| Shell write | Run commands that modify files or system state |
| Package management | Install/update packages |
| Service management | Start/stop/restart services |
| Docker operations | Manage containers, images, volumes |

### Memory & Knowledge
| Capability | Description |
|-----------|-------------|
| Memory read | Access MEMORY.md and daily memory logs |
| Memory write | Update MEMORY.md and create daily logs |
| Memory curate | Promote daily entries to long-term memory |
| Cross-agent memory | Access another agent's memory files |

---

## Common Agent Archetypes & Their Permission Profiles

### Personal Assistant (High Trust)
| Capability | Access | Notes |
|-----------|--------|-------|
| Web search | ✅ Autonomous | |
| Calendar read/write | ✅ Autonomous | |
| Email read | ✅ Autonomous | |
| Email send | ⚠️ Confirm | Show draft + recipient |
| File read/write (workspace) | ✅ Autonomous | |
| Shell read-only | ✅ Autonomous | |
| Shell write | ⚠️ Confirm | |
| Send messages | ✅ Autonomous | DM only |
| Memory read/write | ✅ Autonomous | |

### DevOps / Infrastructure Monitor
| Capability | Access | Notes |
|-----------|--------|-------|
| Shell read-only | ✅ Autonomous | Status, logs, metrics |
| Shell write | ⚠️ Confirm | Restarts, deploys |
| Docker operations | ⚠️ Confirm | Container management |
| Web search | ✅ Autonomous | Error lookup |
| File read (system) | 🔒 Restricted | Log files only |
| File write | ❌ Denied | No system file writes |
| Send messages | ✅ Autonomous | Alert channels only |
| Calendar | ❌ Denied | Not needed |
| Email | ❌ Denied | Not needed |

### Sales Development / Lead Gen
| Capability | Access | Notes |
|-----------|--------|-------|
| Web search | ✅ Autonomous | Prospect research |
| Web fetch | ✅ Autonomous | Company pages, LinkedIn |
| API calls (read) | ✅ Autonomous | CRM lookups |
| API calls (write) | ⚠️ Confirm | CRM updates |
| Email draft | ✅ Autonomous | Draft outreach |
| Email send | ⚠️ Confirm | Always confirm before sending |
| Calendar | ❌ Denied | User handles scheduling |
| Shell | ❌ Denied | No system access needed |
| File write (workspace) | ✅ Autonomous | Research notes |

### Research / Knowledge Agent
| Capability | Access | Notes |
|-----------|--------|-------|
| Web search | ✅ Autonomous | Primary function |
| Web fetch | ✅ Autonomous | Full article retrieval |
| File write (workspace) | ✅ Autonomous | Research outputs |
| File read (system) | 🔒 Restricted | Reference documents only |
| Memory write | ✅ Autonomous | Research findings |
| Shell | ❌ Denied | |
| Email/Calendar | ❌ Denied | |
| Send messages | ✅ Autonomous | Report delivery |

### SHEQ / Compliance Agent
| Capability | Access | Notes |
|-----------|--------|-------|
| File read (workspace) | ✅ Autonomous | Audit docs, checklists |
| File write (workspace) | ✅ Autonomous | Generate reports, NCRs |
| Web search | ✅ Autonomous | Regulation lookup |
| Template generation | ✅ Autonomous | ISO documentation |
| Email draft | ✅ Autonomous | Client communications |
| Email send | ⚠️ Confirm | Always confirm |
| Shell | ❌ Denied | |
| Calendar read | ✅ Autonomous | Audit schedules |
| Calendar write | ⚠️ Confirm | Schedule audits |

---

## Access Level Definitions

| Level | Symbol | Meaning | When to Use |
|-------|--------|---------|-------------|
| Autonomous | ✅ | Agent acts without asking | Low-risk, reversible, frequent actions |
| Confirm | ⚠️ | Agent must ask user before executing | Irreversible actions, external communication, financial impact |
| Restricted | 🔒 | Available only in specific contexts | Sensitive data, special workflows, time-limited access |
| Denied | ❌ | Agent must never do this | Out-of-scope, dangerous, privacy-violating |

**Principle of least privilege**: Start with ❌ Denied for everything, then grant upward based on actual need. It's easier to loosen restrictions than to recover from an agent sending an email to the wrong person.

---

## Team Interaction Patterns

### Hub and Spoke
One central agent (the "hub") coordinates all others. Users interact primarily with the hub, which delegates to specialist agents.

```
        User
         |
       [Hub]
      /  |  \
  [A1] [A2] [A3]
```

Best for: Solo users who want a single point of contact.

### Peer Network
All agents operate independently on their own channels. No central coordinator.

```
  User --- [A1] (WhatsApp)
  User --- [A2] (Discord)
  User --- [A3] (Telegram)
```

Best for: Agents with clearly separated domains (personal vs work vs infrastructure).

### Hierarchical
Agents organized in tiers. Tier 1 handles triage, Tier 2 handles specialist work.

```
  User → [Triage Agent] → [Specialist A]
                         → [Specialist B]
                         → [Specialist C]
```

Best for: Teams with high message volume needing classification before routing.

---

## Model Cost Guidance

When recommending models per agent, consider:

| Factor | Opus | Sonnet | Haiku |
|--------|------|--------|-------|
| Complex reasoning | ✅ Best | Good | Limited |
| Creative writing | ✅ Best | Good | Basic |
| Code generation | ✅ Best | ✅ Great | Good |
| Simple Q&A | Overkill | Good | ✅ Best value |
| Heartbeats | Overkill | Overkill | ✅ Best value |
| Cost per message | $$$ | $$ | $ |
| Speed | Slower | Medium | ✅ Fastest |

**Cost optimization pattern**: Use Opus for the primary assistant (quality matters), Sonnet for specialist agents (good balance), Haiku for heartbeats and triage (cheap, fast).
