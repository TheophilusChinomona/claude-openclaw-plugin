# Scripts Reference

All scripts live in `workspace-{client}/scripts/` and are copied to `~/.openclaw/scripts/` on the gateway during deployment.

Every script that uses Python auto-detects the venv at `~/.openclaw/venv/bin/python3`. Override with `OPENCLAW_PYTHON` env var. Override workspace with `OPENCLAW_WORKSPACE`.

## Script Summary

| Script | Used By | Purpose |
|--------|---------|---------|
| `new-tender.sh {ref}` | SCOUT | Create tender folder with duplicate detection |
| `download-file.sh {url} {path}` | SCOUT | Download file, follow redirects, report size |
| `pdf-to-text.sh {pdf}` | SCOUT | Extract PDF → .md (pdftotext → pymupdf → pdfminer) |
| `list-unprocessed.sh [type]` | ALL | Find tenders missing agent outputs |
| `check-expiries.sh [days]` | Orchestrator | Check certificate expiry dates (GREEN/AMBER/RED) |
| `send-email.sh --to --subject --body` | Orchestrator | Send email (msmtp → Resend → sendmail) |

## new-tender.sh

Creates `opportunities/{ref}/` with `downloads/` and `technical-proposal/` subdirectories. Exits silently if folder already exists (duplicate detection).

```bash
#!/bin/bash
set -euo pipefail

REF="${1:?Usage: new-tender.sh <reference_number>}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace-{client}}"
TENDER_DIR="$WORKSPACE/opportunities/$REF"

if [[ -d "$TENDER_DIR" ]]; then
  echo "DUPLICATE: Tender $REF already exists at $TENDER_DIR"
  exit 0
fi

mkdir -p "$TENDER_DIR/downloads"
mkdir -p "$TENDER_DIR/technical-proposal"
echo "Created tender folder: $TENDER_DIR"
```

## download-file.sh

Downloads a file from URL. If output path is a directory, preserves original filename. Uses curl (preferred) or wget (fallback).

```bash
#!/bin/bash
set -euo pipefail

URL="${1:?Usage: download-file.sh <url> <output_path>}"
OUTPUT="${2:?Usage: download-file.sh <url> <output_path>}"

if [[ -d "$OUTPUT" ]]; then
  FILENAME=$(basename "$URL" | sed 's/[?#].*//')
  OUTPUT="${OUTPUT%/}/${FILENAME}"
fi

mkdir -p "$(dirname "$OUTPUT")"

if command -v curl &>/dev/null; then
  HTTP_CODE=$(curl -fsSL -w '%{http_code}' -o "$OUTPUT" "$URL" 2>/dev/null || echo "FAIL")
  if [[ "$HTTP_CODE" == "FAIL" || ! -f "$OUTPUT" ]]; then
    echo "Error: Download failed (HTTP $HTTP_CODE)"
    rm -f "$OUTPUT"
    exit 1
  fi
elif command -v wget &>/dev/null; then
  wget -q -O "$OUTPUT" "$URL" || { echo "Error: Download failed"; rm -f "$OUTPUT"; exit 1; }
else
  echo "Error: Neither curl nor wget is available"
  exit 1
fi

SIZE=$(stat -c%s "$OUTPUT" 2>/dev/null || stat -f%z "$OUTPUT" 2>/dev/null || echo "?")
echo "Downloaded: $OUTPUT ($SIZE bytes)"
```

## pdf-to-text.sh

Extracts text from PDF to markdown. Three fallback methods: pdftotext (poppler) → pymupdf → pdfminer. Creates `{filename}.pdf.md` alongside the PDF.

```bash
#!/bin/bash
set -euo pipefail

PYTHON="${OPENCLAW_PYTHON:-${HOME}/.openclaw/venv/bin/python3}"
[[ -x "$PYTHON" ]] || PYTHON="python3"

PDF_PATH="${1:?Usage: pdf-to-text.sh <pdf_path>}"
MD_PATH="${PDF_PATH}.md"

# Option 1: pdftotext (poppler-utils) — fastest
if command -v pdftotext &>/dev/null; then
  pdftotext -layout "$PDF_PATH" - > "$MD_PATH" (with header)
  exit 0
fi

# Option 2: pymupdf (venv)
if $PYTHON -c "import fitz" 2>/dev/null; then
  $PYTHON -c "..." "$PDF_PATH" "$MD_PATH"
  exit 0
fi

# Option 3: pdfminer.six (venv)
if $PYTHON -c "from pdfminer.high_level import extract_text" 2>/dev/null; then
  $PYTHON -c "..." "$PDF_PATH" "$MD_PATH"
  exit 0
fi

echo "Error: No PDF extraction tool available."
exit 1
```

See actual Tripli workspace `scripts/pdf-to-text.sh` for complete implementation.

## list-unprocessed.sh

Scans `opportunities/` for tenders missing specific agent outputs.

**Check types:**
- `unfiltered` — has discovery.md but no assessment.md (FILTER's work)
- `unchecked` — has assessment.md but no compliance.md (AUDITOR's work)
- `undrafted` — has GO status but no technical-proposal content (ARCHITECT's work)
- `unbriefed` — has assessment.md but no briefing.md (orchestrator's work)
- `all` — show all tenders and their status (default)

```bash
#!/bin/bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace-{client}}"
OPP_DIR="$WORKSPACE/opportunities"
CHECK="${1:-all}"

for dir in "$OPP_DIR"/*/; do
  [[ -d "$dir" ]] || continue
  REF=$(basename "$dir")

  HAS_DISCOVERY=$([[ -f "$dir/discovery.md" ]] && echo "Y" || echo "N")
  HAS_ASSESSMENT=$([[ -f "$dir/assessment.md" ]] && echo "Y" || echo "N")
  HAS_COMPLIANCE=$([[ -f "$dir/compliance.md" ]] && echo "Y" || echo "N")
  HAS_BRIEFING=$([[ -f "$dir/briefing.md" ]] && echo "Y" || echo "N")
  HAS_PROPOSAL=$([[ -n "$(ls -A "$dir/technical-proposal/" 2>/dev/null)" ]] && echo "Y" || echo "N")

  case "$CHECK" in
    unfiltered) [[ "$HAS_DISCOVERY" == "Y" && "$HAS_ASSESSMENT" == "N" ]] && echo "$REF" ;;
    unchecked)  [[ "$HAS_ASSESSMENT" == "Y" && "$HAS_COMPLIANCE" == "N" ]] && echo "$REF" ;;
    undrafted)  [[ "$HAS_ASSESSMENT" == "Y" && "$HAS_PROPOSAL" == "N" ]] && grep -qi "GO" "$dir/README.md" 2>/dev/null && echo "$REF" ;;
    unbriefed)  [[ "$HAS_ASSESSMENT" == "Y" && "$HAS_BRIEFING" == "N" ]] && echo "$REF" ;;
    all) echo "$REF  discovery=$HAS_DISCOVERY  assessment=$HAS_ASSESSMENT  compliance=$HAS_COMPLIANCE  briefing=$HAS_BRIEFING  proposal=$HAS_PROPOSAL" ;;
  esac
done
```

## check-expiries.sh

Reads `company-data.json` and checks certificate expiry dates. Uses Python for JSON parsing and date math.

**Output:** GREEN/AMBER/RED status per certificate, with counts and alerts.

**Customize:** The Python code reads specific JSON paths (`data.cidb.expiry`, `data.compliance.bbbee_expiry`, etc.). Adjust these paths to match the client's `company-data.json` structure.

```bash
#!/bin/bash
set -euo pipefail

PYTHON="${OPENCLAW_PYTHON:-${HOME}/.openclaw/venv/bin/python3}"
[[ -x "$PYTHON" ]] || PYTHON="python3"

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace-{client}}"
DATA_FILE="$WORKSPACE/bid-library/company-profiles/company-data.json"
WARN_DAYS="${1:-60}"
TODAY=$(date +%Y-%m-%d)

$PYTHON -c "
import json
from datetime import datetime, timedelta

# ... parse company-data.json, check each cert against today + warn_days
# Print GREEN/AMBER/RED per certificate
# Print summary alerts
"
```

See actual Tripli workspace `scripts/check-expiries.sh` for complete implementation.

## send-email.sh

Sends email with three fallback methods: msmtp → Resend API → sendmail.

**Usage:**
```bash
send-email.sh --to "email@example.com" --subject "Subject" --body "Body text"
send-email.sh --to "email@example.com" --subject "Subject" --body-file "/path/to/body.md"
```

**Configure one of:**
- msmtp: `~/.msmtprc` with SMTP credentials
- Resend: `RESEND_API_KEY` env var
- sendmail: system sendmail (if available)

## Required Packages on Gateway

```bash
# System packages
sudo apt-get install -y poppler-utils python3-venv

# Python venv
python3 -m venv ~/.openclaw/venv
~/.openclaw/venv/bin/pip install pdfplumber pypdf

# Email (choose one)
sudo apt-get install -y msmtp msmtp-mta  # Option A
# OR set RESEND_API_KEY env var           # Option B
```
