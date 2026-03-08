---
description: Scaffold and manage an outreach agent in the workspace
argument-hint: <setup|show|validate>
allowed-tools: Bash, Read, Write
---

# /oc-outreach Command

Scaffold and manage a research-first outreach agent with cold email pipeline, human voice standard, and prompt injection protection.

## Subcommands

### `setup` — Interactive Scaffolding

Scaffold a complete outreach agent workspace under `team/outreach/`.

#### Steps

1. **Detect workspace root.** Look for `.openclaw/workspace-state.json` or `CLAUDE.md` in the current directory and parent directories. If not found, ask the user for the workspace path.

2. **Check prerequisites:**
   - `team/` directory exists (create if missing after confirming)
   - `skills/imap-smtp-email/` exists in workspace (warn if missing — outreach will work for everything except actual email sending)

3. **Collect configuration values interactively.** Ask the user for each value, showing the default in parentheses:
   - `BUSINESS_NAME` — Business domain/name for sign-offs (e.g. "theochinomona.tech")
   - `BD_PERSON_NAME` — Name the outreach agent signs emails as (e.g. "Zach")
   - `BD_TITLE` — Title in email sign-off (default: "Business Development")
   - `OWNER_NAME` — Workspace owner's first name (e.g. "Theo")
   - `OWNER_TIMEZONE` — Owner's timezone (e.g. "SAST (UTC+2)")
   - `SENDER_EMAIL` — Email address to send from (e.g. "zach@example.com")
   - `DISPLAY_NAME` — Display name on sent emails (e.g. "John Smith")
   - `EMAIL_SKILL_PATH` — Auto-detect from workspace, confirm with user

4. **Read all templates** from `skills/openclaw-outreach-setup/references/file-templates.md` in the plugin directory.

5. **Create the full directory structure:**
   ```
   team/outreach/
   team/outreach/memory/
   team/outreach/pipeline/
   team/outreach/pipeline/templates/
   team/outreach/pipeline/prospects/
   team/outreach/skills/cold-outreach/
   team/outreach/skills/client-discovery/
   team/outreach/skills/proposal-writing/
   ```

6. **Generate each file** from templates with all `{{PLACEHOLDER}}` values replaced with the collected config values. Also replace `{{WORKSPACE_ROOT}}` with the detected workspace root path and `{{EMAIL_SKILL_PATH}}` with the email skill path.

   Files to generate (16 total):
   - `team/outreach/CLAUDE.md`
   - `team/outreach/AGENTS.md`
   - `team/outreach/SOUL.md`
   - `team/outreach/IDENTITY.md`
   - `team/outreach/USER.md`
   - `team/outreach/TOOLS.md`
   - `team/outreach/HEARTBEAT.md`
   - `team/outreach/MEMORY.md`
   - `team/outreach/pipeline/verticals.md`
   - `team/outreach/pipeline/tracker.json`
   - `team/outreach/pipeline/templates/prospect-brief.md`
   - `team/outreach/pipeline/templates/email-sequence.md`
   - `team/outreach/skills/cold-outreach/SKILL.md`
   - `team/outreach/skills/cold-outreach/human-voice.md`
   - `team/outreach/skills/client-discovery/SKILL.md`
   - `team/outreach/skills/proposal-writing/SKILL.md`

7. **Report summary** showing all created files and directories, the config values used, and suggest running `/oc-outreach validate` to verify the setup.

### `show` — Pipeline Status

Display current outreach pipeline status.

1. Read `team/outreach/pipeline/tracker.json` from the workspace
2. If file doesn't exist or is empty, report "No pipeline data found. Run `/oc-outreach setup` first."
3. Display:
   - Total prospect count
   - Status breakdown (count per status)
   - Recent activity table showing prospects sorted by most recent date, with columns: Company | Status | Touches | Last Activity

### `validate` — Setup Completeness

Run validation checks against the outreach agent setup. Reference `skills/openclaw-outreach-setup/references/validation-checklist.md` in the plugin directory for the full checklist.

Checks to run:

1. **Files check** — Verify all 16 required files exist and are non-empty under `team/outreach/`
2. **Email skill check** — Verify `imap-smtp-email` skill directory exists and `.env` has required keys (SMTP_HOST, SMTP_USER, IMAP_HOST, IMAP_USER)
3. **Config consistency** — Scan all 16 files for leftover `{{...}}` placeholder patterns
4. **Pipeline health** — Verify `tracker.json` is valid JSON with `prospects` array; check `verticals.md` has at least one vertical defined
5. **Directory structure** — Verify all 7 required directories exist

Report results as:
```
Outreach Agent Validation
=========================

Files:          PASS/WARN/FAIL  (X/16 present)
Email Skill:    PASS/WARN/FAIL  (details)
Config:         PASS/FAIL       (details)
Pipeline:       PASS/WARN/FAIL  (details)
Directories:    PASS/FAIL       (X/7 present)

Overall: PASS/WARN/FAIL

Suggestions:
- ...
```

### No subcommand — Usage Help

If no subcommand is provided, show:

```
/oc-outreach — Outreach Agent Management

Commands:
  /oc-outreach setup      Scaffold a complete outreach agent with pipeline
  /oc-outreach show       Show pipeline status and prospect activity
  /oc-outreach validate   Validate setup completeness and config health

The outreach agent handles B2B prospecting, personalized cold email,
pipeline tracking, and autonomous response handling with prompt injection
protection. See the openclaw-outreach-setup skill for full documentation.
```
