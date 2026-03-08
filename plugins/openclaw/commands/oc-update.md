---
description: Update OpenClaw to latest version, run diagnostics, restart gateway
argument-hint:
allowed-tools: Bash, Read
---

# /oc-update Command

Update OpenClaw to the latest version, verify the installation, and restart the gateway.

## Execution

1. **Check current version:**
```bash
openclaw --version
```

2. **Detect package manager and update:**

Check how OpenClaw was installed and update accordingly:

```bash
# Check if installed via npm
which npm && npm list -g openclaw 2>/dev/null && echo "NPM_INSTALL"
```

Then run the appropriate update:

**npm (most common):**
```bash
npm install -g openclaw@latest
```

**Other package managers:** Inform the user to use their package manager's update command.

3. **Verify new version:**
```bash
openclaw --version
```

4. **Run diagnostics:**
```bash
openclaw doctor
```

If `doctor` reports issues, suggest running `openclaw doctor --fix`.

5. **Restart gateway:**
```bash
openclaw gateway restart
```

6. **Check status:**
```bash
openclaw status
```

## Output

Report each step's result:

```
Update Summary:
  Previous version: X.Y.Z
  New version:      A.B.C
  Doctor:           ✓ passed (or X issues found)
  Gateway:          ✓ restarted
  Status:           ✓ running
```

## If Already Up to Date

```
OpenClaw is already at the latest version (X.Y.Z).
Running diagnostics to verify health...
```

Still run `doctor` and `status` to confirm everything is healthy.

## If Update Fails

- Check if running as correct user (may need sudo for global npm)
- Check network connectivity
- Suggest manual update: `npm install -g openclaw@latest`
- If gateway won't restart after update: check `openclaw logs --tail 50`

## After Running

- Suggest running `openclaw security audit` after updates (new checks may be available)
- If breaking changes, suggest reviewing the changelog
- Remind about `/oc-backup` before major version updates
