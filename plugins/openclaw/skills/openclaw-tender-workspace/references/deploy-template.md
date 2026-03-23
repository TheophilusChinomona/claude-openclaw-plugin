# Deployment Guide Template

Replace `{client}`, `{server}`, `{email}`, etc. with client-specific values.

---

# Deployment Guide — {company_short} Tender Team to {server}

## Prerequisites

- SSH access to {server} as `openclaw` user
- OpenClaw gateway running on {server}
- WhatsApp already paired and working
- {provider} OAuth provider configured in existing openclaw.json

## Step 0: Install Required Packages

```bash
ssh openclaw@{server}

# System packages
sudo apt-get update && sudo apt-get install -y poppler-utils python3-venv

# Python virtual environment (Ubuntu 24.04 blocks system-wide pip)
python3 -m venv ~/.openclaw/venv
~/.openclaw/venv/bin/pip install pdfplumber pypdf

# Verify
~/.openclaw/venv/bin/python3 -c "import pdfplumber; print('pdfplumber OK')"
~/.openclaw/venv/bin/python3 -c "from pypdf import PdfReader; print('pypdf OK')"
pdftotext -v

# Email: Option A — msmtp
sudo apt-get install -y msmtp msmtp-mta

# Email: Option B — Resend API
# export RESEND_API_KEY="re_YOUR_KEY"

curl --version
```

**SECURITY: Agents must NOT run package installs at runtime.**

## Step 1: Copy workspace to server

```bash
rsync -avz --delete \
  "/path/to/workspace-{client}/" \
  openclaw@{server}:~/.openclaw/workspace-{client}/
```

## Step 2: Set up scripts

```bash
ssh openclaw@{server}

mkdir -p ~/.openclaw/scripts
cp ~/.openclaw/workspace-{client}/scripts/*.sh ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/*.sh

# Verify
ls -la ~/.openclaw/scripts/
~/.openclaw/scripts/check-expiries.sh
```

## Step 3: Set up email

**Option A: msmtp**
```bash
cat > ~/.msmtprc << 'EOF'
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        ~/.msmtp.log

account        {client}
host           smtp.gmail.com
port           587
from           {agent_email}
user           {email}
password       YOUR_APP_PASSWORD_HERE

account default : {client}
EOF
chmod 600 ~/.msmtprc
```

**Option B: Resend API**
```bash
export RESEND_API_KEY="re_YOUR_KEY_HERE"
```

**Test:**
```bash
~/.openclaw/scripts/send-email.sh \
  --to "{email}" \
  --subject "[{company_short} Tender Briefing] Test" \
  --body "{agent_name} is online. This is a test email."
```

## Step 4: Set up MCP servers (Smithery)

```bash
smithery auth login

# Search MCPs for SCOUT
smithery mcp add "https://server.smithery.ai/exa"
smithery mcp add "https://server.smithery.ai/brave"
smithery mcp add "https://server.smithery.ai/brightdata"

# Verify
smithery mcp list
```

**API keys:**
```bash
export EXA_API_KEY="your_exa_key"
export BRAVE_API_KEY="your_brave_key"
```

## Step 5: Merge agent config into openclaw.json

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-{client}
nano ~/.openclaw/openclaw.json
```

Merge from `workspace-{client}/openclaw.json`:
1. `agents.list` — all 5 agents
2. `bindings` — WhatsApp → orchestrator
3. `cron.jobs` — 3 cron jobs
4. `session` — dmScope
5. `skills.load.extraDirs` — workspace skills path

## Step 6: Verify

```bash
openclaw config validate
openclaw agents list --bindings
openclaw cron list
```

Expected:
- {agent_name} → workspace-{client} (default, WhatsApp bound)
- scout → workspace-{client}/agents/scout (cron 4h)
- filter → workspace-{client}/agents/filter (cron 6h)
- architect → workspace-{client}/agents/architect (on-demand)
- auditor → workspace-{client}/agents/auditor (on-demand)

## Step 7: Test

```bash
# Test SCOUT
openclaw cron run scout-scan

# Check output
ls ~/.openclaw/workspace-{client}/opportunities/

# Test via WhatsApp
# Send: "Status"
# Agent should respond with pipeline overview

# Test expiry check
# Send: "Check expiries"
# Agent should report certificate status
```

## Step 8: Monitor

```bash
openclaw logs -f
openclaw logs -f --agent scout
openclaw status
openclaw cron list --history
```

## Troubleshooting

| Issue | Check |
|-------|-------|
| SCOUT finds nothing | web_search/web_fetch enabled? MCP connections? `openclaw logs -f --agent scout` |
| PDF extraction fails | `~/.openclaw/venv/bin/python3 -c "import pdfplumber"` — if missing, re-run venv setup |
| Email not sending | `cat ~/.msmtp.log` or verify `RESEND_API_KEY` is set |
| Agent not on WhatsApp | `openclaw agents list --bindings` — orchestrator must be default |
| Cron not running | `openclaw cron list --history` — check timezone |
| Agent tries to install pkgs | Security issue — install manually, restart gateway |
