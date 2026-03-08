---
description: Inspect and audit the OpenClaw directory structure at ~/.openclaw/
argument-hint: [audit|agents|comms|memory]
allowed-tools: Bash, Read, Glob
---

# /oc-structure Command

Inspect the OpenClaw workspace directory layout at `~/.openclaw/`.

## Arguments

Parse from `$ARGUMENTS`:
- **audit** (default): Full workspace structure overview and health check
- **agents**: List agent workspaces and their contents
- **comms**: Show communication channels and recent messages
- **memory**: Inspect memory/lancedb and shared knowledge

## Execution

### audit (default)

```bash
# Show top-level structure
ls -la ~/.openclaw/ 2>/dev/null || echo "~/.openclaw/ not found — run /oc-setup first"

# Show workspace contents
ls -la ~/.openclaw/workspace/ 2>/dev/null

# Count agent workspaces
echo "Agent workspaces:"
ls ~/.openclaw/workspace/agents-workspaces/ 2>/dev/null || echo "  (none)"

# Check key files exist
echo ""
echo "Core files:"
for f in openclaw.json models.json workspace/CLAUDE.md workspace/TASKS.json workspace/SPRINT_CURRENT.json workspace/SHARED_KNOWLEDGE.json workspace/IMPROVEMENT_BACKLOG.json; do
  [ -f ~/.openclaw/$f ] && echo "  OK: $f" || echo "  MISSING: $f"
done

# Check auth file permissions
echo ""
echo "Auth file permissions:"
find ~/.openclaw/workspace/agents-workspaces/ -name "auth-profiles.json" -exec stat -c '%a %n' {} \; 2>/dev/null || echo "  (no auth files found)"
```

Present a summary of what exists, what's missing, and any permission issues.

### agents

```bash
# List all agent workspaces
ls -la ~/.openclaw/workspace/agents-workspaces/ 2>/dev/null || echo "No agent workspaces found"

# For each agent, show key files
for dir in ~/.openclaw/workspace/agents-workspaces/*/; do
  agent=$(basename "$dir")
  echo ""
  echo "--- $agent ---"
  ls "$dir" 2>/dev/null
  # Show role from IDENTITY.md first line
  head -3 "$dir/IDENTITY.md" 2>/dev/null
done
```

Present a table of agents with their roles and available files.

### comms

```bash
# Show communication structure
echo "Communication channels:"
find ~/.openclaw/workspace/comms/ -type f 2>/dev/null || echo "  (none)"

# Show broadcast messages
echo ""
echo "Broadcast:"
cat ~/.openclaw/workspace/comms/broadcast.md 2>/dev/null || echo "  (no broadcast messages)"

# Show recent inbox messages per agent
for dir in ~/.openclaw/workspace/comms/*/inbox/; do
  agent=$(basename "$(dirname "$dir")")
  count=$(ls "$dir" 2>/dev/null | wc -l)
  [ "$count" -gt 0 ] && echo "  $agent inbox: $count message(s)"
done
```

### memory

```bash
# Check LanceDB
echo "LanceDB store:"
ls -la ~/.openclaw/memory/lancedb/ 2>/dev/null || echo "  (not found)"

# Show shared knowledge summary
echo ""
echo "Shared Knowledge:"
cat ~/.openclaw/workspace/SHARED_KNOWLEDGE.json 2>/dev/null | head -30 || echo "  (not found)"

# Show improvement backlog
echo ""
echo "Improvement Backlog:"
cat ~/.openclaw/workspace/IMPROVEMENT_BACKLOG.json 2>/dev/null | head -20 || echo "  (not found)"
```

## After Inspection

1. Summarize findings: what exists, what's missing, any permission issues
2. If `~/.openclaw/` doesn't exist, suggest running `/oc-setup` first
3. Flag auth files with incorrect permissions (should be chmod 600)
4. If fewer than 5 items in IMPROVEMENT_BACKLOG.json, flag as non-compliant
