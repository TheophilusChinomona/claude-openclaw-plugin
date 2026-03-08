---
name: openclaw-sandboxing
description: >
  Use when the user wants to configure Docker sandbox, set up sandboxed
  execution, configure container isolation, manage bind mounts, set up
  sandbox browser, debug sandbox issues, build custom sandbox images,
  or configure network isolation in OpenClaw.
---

# OpenClaw Sandboxing

Guide the user through Docker sandbox configuration for isolated tool execution.

Sandboxing runs tools inside Docker containers to reduce blast radius. The Gateway stays on the host; tool execution runs in an isolated sandbox. This is **optional** and controlled by configuration.

## Sandbox Modes

`agents.defaults.sandbox.mode`:

| Mode | Behavior |
|------|----------|
| `off` | No sandboxing (tools run on host) |
| `non-main` | Sandbox only non-main sessions (default for multi-user) |
| `all` | Every session runs in a sandbox |

`non-main` is based on `session.mainKey` (default `"main"`). Group/channel sessions use their own keys, so they count as non-main and will be sandboxed.

## Sandbox Scope

`agents.defaults.sandbox.scope`:

| Scope | Containers | Use Case |
|-------|-----------|----------|
| `session` (default) | One per session | Maximum isolation |
| `agent` | One per agent | Shared state within agent |
| `shared` | One for all sandboxed sessions | Resource-efficient |

## Workspace Access

`agents.defaults.sandbox.workspaceAccess`:

| Access | Behavior |
|--------|----------|
| `none` (default) | Sandbox workspace under `~/.openclaw/sandboxes` |
| `ro` | Agent workspace mounted read-only at `/agent` |
| `rw` | Agent workspace mounted read/write at `/workspace` |

With `ro`, write/edit/apply_patch tools are disabled in the sandbox.

## Docker Configuration

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none",           // none | bridge | host (blocked)
          env: { NODE_ENV: "sandbox" },
          setupCommand: "apt-get update && apt-get install -y nodejs",
          user: "1000:1000",
          readOnlyRoot: false,
          binds: ["/home/user/data:/data:ro"],
        },
      },
    },
  },
}
```

### Bind Mounts

Format: `host:container:mode` (e.g., `/home/user/source:/source:ro`)

- Global and per-agent binds are **merged** (not replaced)
- Under `scope: "shared"`, per-agent binds are ignored
- Blocked sources: `docker.sock`, `/etc`, `/proc`, `/sys`, `/dev`

### Network Modes

| Network | Security | Use Case |
|---------|----------|----------|
| `none` (default) | No egress | Maximum isolation |
| `bridge` | Outbound access | Package installs, API calls |
| `host` | **Blocked** | Security risk |
| `container:<id>` | **Blocked** (namespace join) | Break-glass only (`dangerouslyAllowContainerNamespaceJoin`) |

## Sandbox Browser

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          autoStart: true,
          autoStartTimeoutMs: 30000,
          network: "openclaw-sandbox-browser",  // dedicated Docker network
          cdpSourceRange: "172.21.0.1/32",      // CIDR allowlist for CDP
          allowHostControl: false,               // let sandboxed sessions target host browser
          binds: [],                             // browser-specific binds (replaces docker.binds)
        },
      },
    },
  },
}
```

- Sandbox browser uses a dedicated Docker network by default
- noVNC observer access is password-protected with short-lived tokens
- `allowHostControl` lets sandboxed sessions target the host browser explicitly

## Tool Policy Interaction

Tool allow/deny policies apply **before** sandbox rules:
- If a tool is denied globally or per-agent, sandboxing doesn't bring it back
- `tools.elevated` is an explicit escape hatch — runs `exec` on the host

```json5
{
  tools: {
    elevated: { enabled: true },   // allows host exec from sandbox
  },
}
```

**Elevated exec runs on the host and bypasses sandboxing.** Use with caution.

## Per-Agent Overrides

```json5
{
  agents: {
    list: [
      {
        id: "dev",
        sandbox: { mode: "off" },              // trusted, no sandbox
      },
      {
        id: "builder",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "rw",
          docker: { network: "bridge", setupCommand: "apt install -y nodejs npm" },
        },
        tools: { allow: ["exec", "read", "write"], deny: ["browser", "cron"] },
      },
      {
        id: "reporter",
        sandbox: { mode: "all", scope: "shared", workspaceAccess: "ro" },
        tools: { allow: ["read"], deny: ["exec", "write", "edit"] },
      },
    ],
  },
}
```

## Debugging

```bash
openclaw sandbox explain          # Inspect effective sandbox mode, tool policy, fix-it keys
docker ps --filter "name=openclaw"  # List running sandbox containers
```

## Building Images

### Default Image

```bash
scripts/sandbox-setup.sh
# Produces: openclaw-sandbox:bookworm-slim
```

### Common Image (with tooling)

```bash
scripts/sandbox-common-setup.sh
# Produces: openclaw-sandbox-common:bookworm-slim
# Includes: curl, jq, nodejs, python3, git
```

Then set: `agents.defaults.sandbox.docker.image: "openclaw-sandbox-common:bookworm-slim"`

### Browser Image

```bash
scripts/sandbox-browser-setup.sh
# Produces sandbox browser image with Chromium
```

## Common Patterns

### Development Sandbox (with network)

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        scope: "agent",
        workspaceAccess: "rw",
        docker: { network: "bridge", image: "openclaw-sandbox-common:bookworm-slim" },
      },
    },
  },
}
```

### Locked-Down Production

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        scope: "session",
        workspaceAccess: "none",
        docker: { network: "none", readOnlyRoot: true },
      },
      tools: { elevated: { enabled: false } },
    },
  },
}
```

## Cross-References

- **Per-agent sandbox config**: See `openclaw-multi-agent` for sandbox settings in multi-agent setups
- **Security implications**: See `openclaw-security` for hardening guidance

See `references/docker-setup.md` for image build details and troubleshooting.
