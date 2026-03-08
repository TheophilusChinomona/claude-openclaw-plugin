---
description: Run security audit with findings grouped by severity, optional auto-fix
argument-hint: [--deep] [--fix]
allowed-tools: Bash, Read
---

# /oc-security Command

Run an OpenClaw security audit, group findings by severity, and optionally auto-fix issues.

## Arguments

The user provides: `$ARGUMENTS`

Parse optional flags:
- `--deep` — include live Gateway probe
- `--fix` — auto-fix supported findings
- `--json` — output raw JSON (for scripting)

## Execution

1. Run the security audit:
```bash
openclaw security audit $ARGUMENTS
```

2. Parse and group findings by severity:

### CRITICAL
Show critical findings first with red emphasis. For each:
- **Finding**: description of the issue
- **Risk**: why it matters
- **Fix**: exact command or config change to resolve

### WARNING
Show warnings next. Same format as critical but lower urgency.

### INFO
Show informational items last. Brief description + recommendation.

3. After showing findings, provide a summary:
```
Security Audit Summary:
  Critical: X findings
  Warning:  Y findings
  Info:     Z findings
```

4. If `--fix` was used, report which fixes were applied automatically.

## If No Findings

Report a clean audit:
```
✓ Security audit passed — no findings.
```

Suggest running `--deep` for a more thorough check.

## If OpenClaw Not Installed

Guide the user to install OpenClaw first:
```
OpenClaw CLI not found. Run /oc-setup to install.
```

## After Running

- For critical findings: urge immediate action, offer to apply fixes
- For `--fix`: verify fixes with a re-run: `openclaw security audit`
- Suggest scheduling periodic audits (e.g., after config changes or updates)
- For hardening guidance: reference the `openclaw-security` skill
