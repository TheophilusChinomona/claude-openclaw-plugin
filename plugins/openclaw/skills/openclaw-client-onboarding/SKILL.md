---
name: openclaw-client-onboarding
description: Run the complete IBS OpenClaw client onboarding process — from scoping a new client's agent requirements, through designing their agent architecture, building their workspace files and openclaw.json, to producing a professional handover package. Use this skill when IBS is onboarding a new client onto OpenClaw, productising the agent deployment service, creating a client's first agent setup, or when the user says things like "onboard this client", "set up OpenClaw for a new client", "create an agent for our client", "deploy agents for [company]", or "build the OpenClaw setup for [client name]". This skill runs the full IBS OpenClaw product workflow: client interview, needs assessment, architecture design, workspace generation, openclaw.json configuration, deploy script, and professional handover documentation.
---

# OpenClaw Client Onboarding

Run the complete IBS OpenClaw client onboarding — from discovery interview through to a professional handover package the client can deploy in under 30 minutes.

## The IBS OpenClaw Product

IBS deploys isolated, self-hosted OpenClaw agent setups for SMB clients. Each client gets:
- Their own OpenClaw workspace(s) on their own server or IBS-managed hosting
- Persona-driven agents tailored to their business
- Pre-configured heartbeats, cron jobs, and channel routing
- A professional handover package with deployment instructions

---

## Stage 1: Client Discovery Interview

Run this interview before designing anything. Adapt to what's already known.

**Business context:**
```
1. Company name and industry
2. Primary services / products
3. Company size (employees, revenue band)
4. Geography (SA / SADC / international)
5. Existing tech stack (CRM, email platform, project management tools)
6. Technical capacity (does anyone manage their server/infrastructure?)
```

**Use case definition:**
```
7. What's the #1 problem they want an AI agent to solve?
8. What repetitive tasks eat the most time?
9. Who would use the agent day-to-day? (role, tech comfort level)
10. What channel do they use most? (WhatsApp / Telegram / Discord)
11. Are there any processes they want automated?
12. Is there a compliance or documentation need? (ISO, SHEQ, industry-specific)
```

**Deployment preference:**
```
13. Self-hosted on their server OR IBS-managed hosting?
14. What server/OS (if self-hosted)? [Ubuntu preferred]
15. Do they have Node 22+ installed?
16. Budget indicator (starter / standard / professional tier)
```

---

## Stage 2: Needs Assessment and Tier Recommendation

Based on the interview, recommend a tier:

### Starter (1-2 agents)
**Ideal for**: Solo operator, small business, single use case
**Agents**: 1 personal assistant + 1 specialist
**Setup**: Single workspace, simple openclaw.json
**Typical use case**: WhatsApp assistant that handles scheduling, reminders, and one core task

### Standard (3-5 agents)  
**Ideal for**: SMB, 5-50 employees, clear departmental needs
**Agents**: CEO/orchestrator + 2-4 specialists
**Setup**: Multi-agent routing, basic cron jobs
**Typical use case**: Operations assistant + sales researcher + document generator

### Professional (6+ agents)
**Ideal for**: Growing business, multiple departments, complex workflows
**Agents**: Full department coverage
**Setup**: Complete ecosystem with all features
**Typical use case**: Full AI company equivalent to the IBS 14-agent setup

Present the recommendation with rationale and let the client confirm before proceeding.

---

## Stage 3: Agent Architecture Design

Design the agent team based on the client's specific needs:

**Output: Client Agent Architecture Document**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[CLIENT NAME] — OpenClaw Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIER: [Starter / Standard / Professional]

AGENTS:
| Agent | Role | Model | Channel | Heartbeat |
|---|---|---|---|---|
| [name] | [role] | [model] | [channel] | [interval] |

CHANNEL ROUTING:
[which agent handles which channel/sender]

CRON JOBS:
[key automated tasks and schedules]

ESTIMATED MONTHLY API COST:
[rough estimate based on model usage and heartbeat frequency]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Client approves architecture before any files are built.

---

## Stage 4: Build the Workspace

Use `openclaw-persona-architect` for each agent:
- Research world-class personas for each role
- Design soul architecture
- Generate all 5 workspace files

Use `openclaw-workspace-builder` for the openclaw.json:
- Complete agent list with model assignments
- Channel routing bindings
- Heartbeat configuration
- Cron job setup
- Deploy script

---

## Stage 5: Produce Handover Package

The handover package is a professional DOCX document the client receives. It contains everything they need to deploy and operate their agent setup without relying on IBS for day-to-day questions.

**Handover Package Contents:**

```
[CLIENT NAME]
OpenClaw AI Agent System — Handover Documentation
Prepared by: Integrated Business Strategies
Date: [date]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECTION 1: SYSTEM OVERVIEW
- What was built and why
- Agent roster (name, role, persona, channel)
- Architecture diagram

SECTION 2: DEPLOYMENT GUIDE
- Prerequisites (Node version, server requirements)
- Step-by-step deployment instructions
- The deploy.sh script with annotations

SECTION 3: CHANNEL SETUP
- How to link WhatsApp / Telegram / Discord
- Test checklist to confirm each channel is working

SECTION 4: HOW YOUR AGENTS WORK
- Per-agent: what it does, when it runs, what to expect
- Heartbeat schedule (when you'll receive briefings)
- Cron job schedule (automated tasks)

SECTION 5: CREDENTIALS AND SECURITY
- Which API keys are needed and how to add them
- Security checklist (chmod, private git, .gitignore)
- What to do if an agent behaves unexpectedly

SECTION 6: DAILY OPERATIONS
- How to message your agent
- How to update agent memory ("remember that...")
- How to pause or stop an agent
- How to check if everything is working

SECTION 7: SUPPORT AND UPDATES
- How to contact IBS for support
- How IBS updates agent workspaces (the openclaw-agent-updater workflow)
- When to expect agent reviews (quarterly recommended)

SECTION 8: PRICING AND ONGOING COSTS
- Anthropic API key setup and billing
- Estimated monthly cost range
- How to monitor usage
```

---

## Stage 6: Post-Deployment Checklist

After the client deploys:

```
DEPLOYMENT VERIFICATION CHECKLIST:
□ Gateway running: openclaw gateway status = "running"
□ All channels connected: openclaw channels status --probe
□ All agents listed: openclaw agents list --bindings
□ Heartbeat received on target channel (test message sent)
□ Cron jobs enabled: openclaw cron list (all enabled: true)
□ SOUL.md and IDENTITY.md are chmod 444
□ Workspace backed up to private git repo
□ Client successfully sent a test message and received a response
□ Client confirmed they understand how to update memory
```

Produce this checklist as a tickable PDF or DOCX the client completes and returns.

---

## Pricing Structure (IBS OpenClaw Product)

**IBS charges for the setup and configuration. Client pays Anthropic directly for API usage.**

| Tier | Setup Fee | What's Included |
|---|---|---|
| Starter | [Tino to set pricing] | 2 agents, 1 channel, basic cron, handover doc |
| Standard | [Tino to set pricing] | 5 agents, 2 channels, full cron suite, handover + 1 month support |
| Professional | [Tino to set pricing] | 10+ agents, all channels, full ecosystem, handover + quarterly review |

**Ongoing options:**
- Monthly agent maintenance retainer: [Tino to set pricing]
- Quarterly agent review and update: [Tino to set pricing]
- Ad hoc agent updates: [Tino to set pricing per hour]

Note: Pricing fields marked [Tino to set pricing] — confirm before quoting clients.

---

## Onboarding Timeline

| Stage | Typical Duration |
|---|---|
| Discovery interview | 1-2 hours |
| Architecture design + client approval | 1-2 days |
| Workspace and config build | 1-3 days depending on tier |
| Handover document production | 1 day |
| Client deployment + testing | 2-4 hours (client side) |
| **Total: Starter** | ~3-5 business days |
| **Total: Standard** | ~5-7 business days |
| **Total: Professional** | ~10-14 business days |
