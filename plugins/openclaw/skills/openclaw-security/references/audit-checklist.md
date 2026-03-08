# Security Audit Checklist

## Audit Findings by Severity

### Critical

| checkId | Description | Fix |
|---------|-------------|-----|
| `fs.state_dir.perms_world_writable` | `~/.openclaw` world-writable | `chmod 700 ~/.openclaw` |
| `fs.config.perms_writable` | Config writable by others | `chmod 600 ~/.openclaw/openclaw.json` |
| `fs.config.perms_world_readable` | Config readable by others | `chmod 600 ~/.openclaw/openclaw.json` |
| `gateway.bind_no_auth` | Remote bind without auth | Set `gateway.auth.mode` to `token` or `password` |
| `gateway.loopback_no_auth` | Reverse-proxied loopback unauthenticated | Configure `gateway.auth.*` |
| `gateway.tailscale_funnel` | Public internet exposure | Change `gateway.tailscale.mode` to `serve` |
| `gateway.control_ui.allowed_origins_required` | Non-loopback Control UI without origin allowlist | Set `gateway.controlUi.allowedOrigins` |
| `gateway.control_ui.device_auth_disabled` | Device identity check disabled | Remove `dangerouslyDisableDeviceAuth` |
| `sandbox.dangerous_network_mode` | Sandbox uses `host` or `container:*` network | Change `sandbox.docker.network` |
| `security.exposure.open_groups_with_elevated` | Open groups + elevated tools | Lock down groups or disable elevated |
| `security.exposure.open_groups_with_runtime_or_fs` | Open groups can reach shell/file tools | Add sandbox, tool deny, or group allowlists |

### Warning

| checkId | Description | Fix |
|---------|-------------|-----|
| `gateway.http.no_auth` | HTTP APIs reachable without auth | Set `gateway.auth.mode` |
| `gateway.tools_invoke_http.dangerous_allow` | Dangerous tools re-enabled over HTTP | Remove from `gateway.tools.allow` |
| `gateway.nodes.allow_commands_dangerous` | High-impact node commands enabled | Review `gateway.nodes.allowCommands` |
| `gateway.real_ip_fallback_enabled` | X-Real-IP fallback enabled | Set `gateway.allowRealIpFallback: false` |
| `gateway.control_ui.host_header_origin_fallback` | Host-header origin fallback | Remove `dangerouslyAllowHostHeaderOriginFallback` |
| `gateway.control_ui.insecure_auth` | Insecure-auth toggle enabled | Remove `allowInsecureAuth` |
| `discovery.mdns_full_mode` | mDNS advertises metadata on LAN | Set `discovery.mdns.mode` to `disabled` |
| `config.insecure_or_dangerous_flags` | Dangerous debug flags enabled | See finding detail for specific keys |
| `hooks.token_too_short` | Hook token too short | Use a longer token (32+ chars) |
| `hooks.request_session_key_enabled` | External callers can choose sessionKey | Set `allowRequestSessionKey: false` |
| `hooks.request_session_key_prefixes_missing` | No bound on external session key shapes | Add `allowedSessionKeyPrefixes` |
| `logging.redact_off` | Sensitive values leak to logs | Set `logging.redactSensitive: true` |
| `sandbox.docker_config_mode_off` | Sandbox config present but mode is off | Set `sandbox.mode` to `non-main` or `all` |
| `tools.exec.host_sandbox_no_sandbox_defaults` | `exec host=sandbox` runs on host (sandbox off) | Enable sandbox or change `tools.exec.host` |
| `tools.exec.host_sandbox_no_sandbox_agents` | Per-agent `exec host=sandbox` resolves to host | Enable per-agent sandbox |
| `tools.exec.safe_bins_interpreter_unprofiled` | Interpreter bins in safeBins without profiles | Add `tools.exec.safeBinProfiles` |
| `skills.workspace.symlink_escape` | Skill resolves outside workspace root | Fix workspace symlinks |
| `security.trust_model.multi_user_heuristic` | Multi-user config with personal-assistant trust | Split trust boundaries or harden |
| `tools.profile_minimal_overridden` | Agent overrides bypass global minimal profile | Review per-agent `tools.profile` |
| `plugins.tools_reachable_permissive_policy` | Plugin tools reachable in permissive contexts | Tighten `tools.profile` and deny lists |
| `models.small_params` | Small models with unsafe tool surfaces | Use stronger models or add sandbox |

## Insecure Flags Reference

| Flag | What It Disables | Risk | When Acceptable |
|------|-----------------|------|-----------------|
| `gateway.controlUi.allowInsecureAuth` | Secure-context requirements | Auth downgrade | Break-glass debugging only |
| `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback` | Origin validation | DNS rebinding | Never in production |
| `gateway.controlUi.dangerouslyDisableDeviceAuth` | Device identity checks | Full auth bypass | Break-glass debugging only |
| `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` | Private network SSRF protection | SSRF attacks | Trusted-network-only testing |
| `channels.*.dangerouslyAllowNameMatching` | Strict sender matching | Impersonation | Legacy compatibility only |
| `agents.*.sandbox.docker.dangerouslyAllowContainerNamespaceJoin` | Container namespace isolation | Container escape | Advanced Docker networking |
| `agents.*.sandbox.docker.dangerouslyAllowExternalBindSources` | Bind source validation | Host path exposure | Specific mount requirements |
| `agents.*.sandbox.docker.dangerouslyAllowReservedContainerTargets` | Reserved target protection | System container access | Specialized Docker setups |
| `hooks.*.allowUnsafeExternalContent` | Content safety wrapping | Prompt injection | Tightly scoped debugging |
| `tools.exec.applyPatch.workspaceOnly=false` | Workspace-only patch restriction | Arbitrary file writes | Cross-workspace patching |

## Incident Response Playbook

### Phase 1: Contain (Minutes)

```bash
# Stop the gateway immediately
openclaw gateway stop
# or: systemctl stop openclaw

# If SSH access compromised:
# Firewall the machine, revoke SSH keys
```

### Phase 2: Rotate (Hours)

```bash
# Generate new gateway token
export NEW_TOKEN=$(openssl rand -hex 32)
openclaw config set gateway.auth.token "$NEW_TOKEN"

# Rotate all API keys
# - Anthropic dashboard: console.anthropic.com
# - OpenAI dashboard: platform.openai.com
# - Other providers: respective dashboards

# Revoke unknown device pairings
openclaw devices list
openclaw devices reject <suspicious-request-id>

# Rotate channel tokens
# - Telegram: @BotFather -> /revoke
# - Discord: Developer Portal -> Bot -> Reset Token
# - Slack: App Settings -> Reinstall
```

### Phase 3: Audit (Hours)

```bash
# Run deep audit
openclaw security audit --deep --json > audit-$(date +%Y%m%d).json

# Check recent logs for suspicious activity
openclaw logs --tail 500 | grep -i "error\|denied\|unauthorized\|suspicious"

# Review session history for unusual commands
ls -lt ~/.openclaw/agents/*/sessions/
```

### Phase 4: Collect (Days)

```bash
# Version and status snapshot
openclaw --version > incident-report.txt
openclaw status >> incident-report.txt

# Configuration snapshot (redact secrets!)
openclaw config get >> incident-report.txt

# Permissions snapshot
ls -la ~/.openclaw/ >> incident-report.txt
ls -la ~/.openclaw/credentials/ >> incident-report.txt
```
