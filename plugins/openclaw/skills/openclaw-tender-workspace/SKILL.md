---
name: openclaw-tender-workspace
description: >
  Set up a multi-agent tender management workspace on OpenClaw for a construction or
  engineering company. Creates the full workspace structure with orchestrator agent,
  discovery, analysis, drafting, and compliance subagents, pre-populated with company
  knowledge. Use when the user says "set up tender workspace", "create tender agents",
  "build tender team", "openclaw tender setup", or wants to build an AI tendering
  system for a company.
---

# OpenClaw Tender Workspace Setup

Build a production-ready multi-agent tender management workspace for a construction, engineering, or professional services company. Based on the proven Tripli Tender Team architecture.

## What This Skill Creates

A complete OpenClaw workspace with 5 agents that autonomously discover, analyse, draft, and compliance-check government tenders:

```
workspace-{client}/                    ← Main workspace
├── SOUL.md                            ← Orchestrator agent (main WhatsApp contact)
├── AGENTS.md                          ← Delegation workflows
├── HEARTBEAT.md                       ← Periodic health checks
├── IDENTITY.md, USER.md, TOOLS.md
│
├── agents/                            ← Subagent workspaces
│   ├── scout/    (SOUL.md, AGENTS.md, skills/)  ← Portal scanning
│   ├── filter/   (SOUL.md, AGENTS.md, skills/)  ← Suitability scoring
│   ├── architect/ (SOUL.md, AGENTS.md, skills/) ← Proposal drafting
│   └── auditor/  (SOUL.md, AGENTS.md, skills/)  ← Compliance checking
│
├── skills/                            ← Shared skills (briefing, pipeline, certificates)
├── scripts/                           ← Utility scripts (PDF, email, downloads)
├── bid-library/                       ← Company knowledge
├── compliance/                        ← Certificate data
├── opportunities/                     ← Per-tender folders
├── partnerships/                      ← JV/subcontractor data
├── pricing/                           ← Rates and models
├── registers/                         ← Pipeline register
└── openclaw.json                      ← Multi-agent config
```

## Setup Flow

### Step 1: Gather Client Information

Ask the user for (or find in the project):

**Required:**
- Company legal name and trading name
- CIDB grading and categories (e.g., 6CE/6EP/6ME)
- B-BBEE level and ownership details
- Core disciplines and capabilities
- Target tender portals (eTenders, CIDB, municipal, etc.)
- Contact person for GO/NO-GO decisions (name, email, phone)
- Email address for tender briefings

**Important:**
- Company registration details (CIPC, VAT, Tax ref, CSD number)
- Certificate expiry dates (CIDB, B-BBEE, Tax, COIDA, ISO)
- Past project portfolio (names, clients, values, disciplines)
- JV partners (if any)
- Standard rates

**Nice to have:**
- Company profile document
- Certificate PDFs (for attaching to tenders)
- Previous winning tender responses
- Key personnel CVs
- SHEQ/quality policies

### Step 2: Create Workspace Structure

Create the directory tree. See [references/workspace-structure.md](references/workspace-structure.md) for the full template.

```bash
mkdir -p workspace-{client}/{agents/{scout,filter,architect,auditor},skills/{send-briefing,pipeline-status,certificate-check},scripts,bid-library/{company-profiles,certificates/{extracted,originals},reference-projects/profiles,cv-bank,methodology-templates,policies,forms,legal-docs},compliance/{cidb,b-bbee,tax,iso,coida,sheq,mandatory-returnables},opportunities,partnerships/{jv,subcontractors,suppliers},pricing/{pricing-models,rate-build-ups,boq,assumptions},registers/{tender-register,submission-checklists,lessons-learned},memory}
```

### Step 3: Write Agent Files

For each agent, create SOUL.md and AGENTS.md. See [references/agent-templates.md](references/agent-templates.md) for the templates.

**Orchestrator (main agent):**
- SOUL.md — lean, conversational, focused on delegation
- AGENTS.md — delegation workflows for every message type, quality gates, escalation rules
- HEARTBEAT.md — periodic checks (closing dates, certificate expiries, stalled pipeline)

**SCOUT:**
- SOUL.md — identity, search portals, keywords derived from client capabilities, CIDB filters
- AGENTS.md — step-by-step scan workflow, discovery record format, error handling

**FILTER:**
- SOUL.md — identity, 5-dimension scoring methodology
- AGENTS.md — scoring rules per dimension, experience matching logic specific to client's portfolio, decision thresholds

**ARCHITECT:**
- SOUL.md — identity, proposal structure, quality standards
- AGENTS.md — drafting workflow, how to address functionality criteria, quality checklist

**AUDITOR:**
- SOUL.md — identity, compliance methodology, expiry thresholds
- AGENTS.md — compliance check workflow, standing documents table, known gaps, common SA tender returnable patterns

### Step 4: Populate Knowledge Base

Copy client documents into the workspace:
- `bid-library/company-profiles/` — company-data.json, profile, contacts
- `bid-library/certificates/originals/` — PDF certificates
- `bid-library/certificates/extracted/` — OCR'd markdown of each certificate
- `bid-library/reference-projects/` — project portfolio summary + source documents
- `bid-library/policies/` — SOPs, SHEQ, quality policies
- `compliance/` — summary files per certificate with expiry dates
- `partnerships/jv/` — JV partner profiles
- `pricing/` — standard rates

Create `bid-library/INDEX.md` as the master knowledge index.

### Step 5: Create Scripts

Copy these utility scripts to `scripts/`:
- `pdf-to-text.sh` — PDF extraction (poppler → pymupdf → pdfminer fallback)
- `download-file.sh` — File download with redirects
- `new-tender.sh` — Create tender folder + duplicate detection
- `list-unprocessed.sh` — Find tenders missing agent outputs
- `check-expiries.sh` — Certificate expiry check against company-data.json
- `send-email.sh` — Email sending (msmtp → Resend → sendmail fallback)

### Step 6: Create Skills

**Shared skills** (workspace-level, accessible to all agents via `extraDirs`):
- `send-briefing/` — Compile + send daily briefing email
- `pipeline-status/` — Show current tender pipeline
- `certificate-check/` — Run expiry check and report

**Agent-specific skills:**
- `agents/scout/skills/scan-portals/` — Portal scanning procedure with search queries
- `agents/filter/skills/score-tender/` — Scoring methodology with experience matching
- All agents get `pdf-processing/` skill (davila7 — APPROVED, pure Python, no external calls)

### Step 7: Create openclaw.json

Generate the multi-agent config with:
- 5 agents: orchestrator (default, WhatsApp bound) + 4 subagents
- Agent workspaces: `workspace-{client}/agents/{name}`
- Bindings: WhatsApp → orchestrator
- Session: `per-account-channel-peer` for DM isolation
- Cron jobs: scout (4h), filter (6h offset), orchestrator briefing (07:30)
- Skills: `extraDirs` pointing to workspace skills
- Tools: orchestrator + scout get exec; filter, architect, auditor get read+write only
- Heartbeat: orchestrator only, every 4h, lightContext, isolatedSession

### Step 8: Create Deployment Guide

Write DEPLOY.md covering:
- Required packages (poppler-utils, python3, pdfplumber, pypdf, msmtp/Resend)
- Security: block pip/apt install in agent exec
- scp/rsync to gateway
- Script setup + permissions
- Email configuration
- MCP server connections (Smithery: Exa, Brave, Bright Data)
- Config merge into existing openclaw.json
- Verification steps
- Troubleshooting

## Key Design Decisions

### Agent Architecture
- **One workspace, agents as subdirectories** — not separate top-level workspaces
- **Orchestrator is lean** — SOUL.md under 100 lines, delegates everything
- **Subagent SOUL files contain only their specialty** — no cross-contamination
- **Skills load per-agent** — each agent's workspace/skills/ loads only for that agent

### File Structure
- **Tender-centric** — everything about a tender in `opportunities/{ref}/`
- **README.md as entry point** — status at a glance for any tender
- **Three-layer knowledge** — summaries (compliance/), extracted detail (certificates/extracted/), originals (certificates/originals/)

### Security
- **Least privilege tools** — only orchestrator + scout get exec
- **No package installs at runtime** — all deps installed during deployment
- **PDF skill reviewed** — davila7/pdf-processing only (pure Python, no shell commands, no external APIs)
- **Gen-PDF for internal docs only** — never send tender content to external PDF renderers

### Scoring
- **5-dimension model** — CIDB match (25), Experience (25), Value (20), Geographic (15), Competitive Edge (15)
- **Experience matching is strict** — "pipeline ≠ drainage", match against functionality criteria keywords exactly
- **Thresholds** — GO (75+), REVIEW (50-74), NO-GO (0-49)

## Customization Points

When setting up for a new client, these are the things that change:

| What | Where | What Changes |
|------|-------|-------------|
| Company identity | SOUL.md (orchestrator) | Agent name, company name, tone |
| CIDB grading | SOUL.md (scout, filter) | Grade limits, categories |
| Search keywords | SOUL.md (scout) | Derived from company capabilities |
| Experience matching | AGENTS.md (filter) | Project types that count as "relevant" |
| Scoring weights | SOUL.md (filter) | May adjust dimensions for different industries |
| Proposal structure | SOUL.md (architect) | Tailored to company's service type |
| Standing documents | AGENTS.md (auditor) | Company's specific certificate set |
| Email address | SOUL.md (orchestrator) | Client's tender email |
| Portal list | SOUL.md (scout) | Which portals to scan |
| Geographic priority | SOUL.md (scout, filter) | Company's operating provinces |
