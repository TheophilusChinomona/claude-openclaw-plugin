# Outreach Agent Validation Checklist

Reference for the `/oc-outreach validate` command. Documents all checks performed during validation.

## 1. Required Files (16)

All paths relative to `team/outreach/` in the workspace root.

| # | File | Purpose |
|---|------|---------|
| 1 | `CLAUDE.md` | Full agent instructions |
| 2 | `AGENTS.md` | Agent role and handoff protocol |
| 3 | `SOUL.md` | Core identity and principles |
| 4 | `IDENTITY.md` | Name, role, vibe |
| 5 | `USER.md` | Owner preferences |
| 6 | `TOOLS.md` | Tool configuration |
| 7 | `HEARTBEAT.md` | Specialist stub |
| 8 | `MEMORY.md` | Long-term memory |
| 9 | `pipeline/verticals.md` | Target categories |
| 10 | `pipeline/tracker.json` | Pipeline state |
| 11 | `pipeline/templates/prospect-brief.md` | Research brief template |
| 12 | `pipeline/templates/email-sequence.md` | Email sequence template |
| 13 | `skills/cold-outreach/SKILL.md` | Copy frameworks |
| 14 | `skills/cold-outreach/human-voice.md` | Human voice standard |
| 15 | `skills/client-discovery/SKILL.md` | Qualification framework |
| 16 | `skills/proposal-writing/SKILL.md` | Proposal framework |

**Check:** Each file must exist and be non-empty.
**Result:** PASS (all exist) / FAIL (list missing files)

## 2. Email Skill Check

**Check A:** `imap-smtp-email` skill directory exists in the workspace.
- Look for `skills/imap-smtp-email/` in the workspace root
- Also check the path configured in `team/outreach/TOOLS.md`

**Check B:** Email `.env` is configured.
- Look for `.env` in the imap-smtp-email skill directory
- Verify it contains `SMTP_HOST`, `SMTP_USER`, `IMAP_HOST`, `IMAP_USER` keys (values don't need to be checked — just key presence)

**Result:**
- PASS — skill exists and `.env` has required keys
- WARN — skill exists but `.env` missing or incomplete (outreach will work for everything except actual sending)
- FAIL — skill directory not found

## 3. Config Consistency Check

**Check:** No leftover `{{PLACEHOLDER}}` values in any of the 16 required files.

Scan all files for the pattern `{{` followed by any text and `}}`. Common placeholders to check for:
- `{{BUSINESS_NAME}}`
- `{{BD_PERSON_NAME}}`
- `{{BD_TITLE}}`
- `{{OWNER_NAME}}`
- `{{OWNER_TIMEZONE}}`
- `{{SENDER_EMAIL}}`
- `{{DISPLAY_NAME}}`
- `{{WORKSPACE_ROOT}}`
- `{{EMAIL_SKILL_PATH}}`

**Result:**
- PASS — no `{{...}}` patterns found
- FAIL — list files and line numbers containing unresolved placeholders

## 4. Pipeline Health Check

### 4a. Tracker JSON Validity
**Check:** `pipeline/tracker.json` is valid JSON with the expected schema.
- Must parse as valid JSON
- Must have a `prospects` array (can be empty)
- Each prospect entry should have: `slug`, `company`, `status`

**Result:** PASS / FAIL with parse error or schema issue

### 4b. Verticals Defined
**Check:** `pipeline/verticals.md` contains at least one vertical definition.
- Look for `## Vertical` headers
- At least one vertical should have industry, geography, and pain point indicators defined

**Result:**
- PASS — at least one vertical defined
- WARN — file exists but no verticals configured yet (setup is complete but owner needs to add targeting)

## 5. Directory Structure Check

**Check:** Required directories exist:
- `team/outreach/pipeline/`
- `team/outreach/pipeline/templates/`
- `team/outreach/pipeline/prospects/`
- `team/outreach/skills/cold-outreach/`
- `team/outreach/skills/client-discovery/`
- `team/outreach/skills/proposal-writing/`
- `team/outreach/memory/`

**Result:** PASS / FAIL (list missing directories)

## Validation Output Format

```
Outreach Agent Validation
=========================

Files:          PASS  (16/16 present)
Email Skill:    WARN  (skill found, .env not configured)
Config:         PASS  (no unresolved placeholders)
Pipeline:       WARN  (tracker valid, no verticals configured)
Directories:    PASS  (7/7 present)

Overall: PASS with warnings

Suggestions:
- Configure email credentials in skills/imap-smtp-email/.env
- Add target verticals to team/outreach/pipeline/verticals.md
```

Severity levels:
- **PASS** — check passed completely
- **WARN** — non-blocking issue, agent will work but with reduced capability
- **FAIL** — blocking issue, must be fixed before the agent can operate
