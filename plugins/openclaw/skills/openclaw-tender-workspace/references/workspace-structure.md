# Workspace Structure Template

Replace `{client}` with the client's short name (lowercase, no spaces).

## Create Directory Tree

```bash
mkdir -p workspace-{client}/{agents/{scout/{skills/{scan-portals,pdf-processing}},filter/{skills/{score-tender,pdf-processing}},architect/{skills/pdf-processing},auditor/{skills/pdf-processing}},skills/{send-briefing,pipeline-status,certificate-check},scripts,bid-library/{company-profiles,certificates/{extracted,originals},reference-projects/profiles,cv-bank,methodology-templates,policies,forms,legal-docs},compliance/{cidb,b-bbee,tax,iso,coida,sheq,mandatory-returnables},opportunities,partnerships/{jv,subcontractors,suppliers},pricing/{pricing-models,rate-build-ups,boq,assumptions},registers/{tender-register,submission-checklists,lessons-learned},memory}
```

## File Map

```
workspace-{client}/
├── SOUL.md                  ← Orchestrator persona (<100 lines)
├── AGENTS.md                ← Delegation workflows + quality gates
├── HEARTBEAT.md             ← Silent periodic checks
├── IDENTITY.md              ← Display identity (name + emoji)
├── USER.md                  ← Human team profiles
├── TOOLS.md                 ← Tool reference + scripts
├── DEPLOY.md                ← Deployment guide
│
├── agents/
│   ├── scout/               ← Portal scanning agent
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── skills/{scan-portals,pdf-processing}/SKILL.md
│   ├── filter/              ← Suitability scoring agent
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── skills/{score-tender,pdf-processing}/SKILL.md
│   ├── architect/           ← Proposal drafting agent
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── skills/pdf-processing/SKILL.md
│   └── auditor/             ← Compliance checking agent
│       ├── SOUL.md
│       ├── AGENTS.md
│       └── skills/pdf-processing/SKILL.md
│
├── skills/                  ← Shared (loaded via extraDirs)
│   ├── send-briefing/
│   ├── pipeline-status/
│   └── certificate-check/
│
├── scripts/                 ← Bash utilities
│   ├── new-tender.sh        ← Create tender folder + duplicate check
│   ├── download-file.sh     ← Download file from URL
│   ├── pdf-to-text.sh       ← PDF → markdown (pdftotext → pymupdf → pdfminer)
│   ├── list-unprocessed.sh  ← Find tenders missing agent outputs
│   ├── check-expiries.sh    ← Certificate expiry check
│   └── send-email.sh        ← Email (msmtp → Resend → sendmail)
│
├── bid-library/             ← Company knowledge
│   ├── INDEX.md
│   ├── company-profiles/{company-data.json, COMPANY-PROFILE.md, contacts.md}
│   ├── certificates/{extracted/, originals/}
│   ├── reference-projects/{project-history.md, profiles/}
│   ├── cv-bank/
│   ├── methodology-templates/
│   ├── policies/
│   ├── forms/
│   └── legal-docs/
│
├── compliance/{cidb,b-bbee,tax,iso,coida,sheq}/
├── opportunities/{ref}/{README,discovery,assessment,compliance,briefing}.md
├── partnerships/{jv,subcontractors,suppliers}/
├── pricing/{pricing-models,rate-build-ups,boq}/
├── registers/tender-register/pipeline.md
├── memory/
└── openclaw.json
```

## Design Principles

1. **Tender-centric** — everything about a tender in `opportunities/{ref}/`
2. **Agent workspaces are subdirectories** — not separate top-level workspaces
3. **Skills are per-agent** — each agent's `skills/` loads only for that agent
4. **INDEX.md is the knowledge entry point** — agents start here
5. **Scripts use venv** — auto-detect `~/.openclaw/venv/bin/python3`
6. **Orchestrator is lean** — SOUL.md <100 lines, delegation in AGENTS.md
7. **Three-layer knowledge** — summaries, extracted detail, originals
