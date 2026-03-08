# Docker Sandbox Setup Reference

## Image Build Scripts

### Default Image (`sandbox-setup.sh`)

```bash
scripts/sandbox-setup.sh
```

Produces `openclaw-sandbox:bookworm-slim` — minimal Debian image without Node or extra tooling.

### Common Image (`sandbox-common-setup.sh`)

```bash
scripts/sandbox-common-setup.sh
```

Produces `openclaw-sandbox-common:bookworm-slim` — includes `curl`, `jq`, `nodejs`, `python3`, `git`.

### Browser Image (`sandbox-browser-setup.sh`)

```bash
scripts/sandbox-browser-setup.sh
```

Produces sandbox browser image with Chromium and conservative startup defaults.

## Custom Dockerfile Template

```dockerfile
FROM openclaw-sandbox:bookworm-slim

# Install custom tooling
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Optional: install global packages
RUN npm install -g typescript
```

Build: `docker build -t openclaw-sandbox-custom:latest .`

Then set:
```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: { image: "openclaw-sandbox-custom:latest" },
      },
    },
  },
}
```

## Bind Mount Examples

### Read-Only Source + Data

```json5
{
  agents: {
    defaults: {
      sandbox: {
        docker: {
          binds: [
            "/home/user/source:/source:ro",
            "/var/data/myapp:/data:ro",
          ],
        },
      },
    },
  },
}
```

### Per-Agent Cache Mount

```json5
{
  agents: {
    list: [
      {
        id: "build",
        sandbox: {
          docker: {
            binds: ["/mnt/cache:/cache:rw"],
          },
        },
      },
    ],
  },
}
```

Global and per-agent binds are merged.

### Blocked Source Paths

These host paths are blocked for bind mounts:
- `/var/run/docker.sock` (Docker socket)
- `/etc` (system config)
- `/proc` (process info)
- `/sys` (kernel interface)
- `/dev` (devices)
- Parent mounts that would expose blocked paths

Override (dangerous): `agents.defaults.sandbox.docker.dangerouslyAllowExternalBindSources: true`

## Network Modes

| Mode | Description | Security |
|------|-------------|----------|
| `none` (default) | No network access | Maximum isolation. Package installs will fail. |
| `bridge` | Docker bridge network | Outbound access. Required for `setupCommand` with package installs. |
| `host` | Host network namespace | **Blocked by default.** Full host network access. |
| `container:<id>` | Join another container's namespace | **Blocked by default.** Requires `dangerouslyAllowContainerNamespaceJoin`. |

## Browser Sandbox Configuration

### Full Browser Sandbox Config

```json5
{
  agents: {
    defaults: {
      sandbox: {
        browser: {
          autoStart: true,
          autoStartTimeoutMs: 30000,
          network: "openclaw-sandbox-browser",
          cdpSourceRange: "172.21.0.1/32",
          allowHostControl: false,
          binds: [],
          // Custom browser allowlists:
          allowedControlUrls: [],
          allowedControlHosts: [],
          allowedControlPorts: [],
        },
      },
    },
  },
}
```

### Chromium Startup Defaults

The sandbox browser image applies conservative flags:
- `--no-sandbox` and `--disable-setuid-sandbox` (container context)
- `--disable-gpu`, `--disable-3d-apis`, `--disable-software-rasterizer`
- `--disable-dev-shm-usage`, `--disable-background-networking`
- `--disable-extensions`, `--no-first-run`, `--no-default-browser-check`
- `--renderer-process-limit=2`

Override via environment:
- `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` — enable WebGL/3D
- `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` — enable extensions
- `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>` — adjust renderer limit

## Elevated Tools Interaction

```json5
{
  tools: {
    elevated: {
      enabled: true,           // allow host exec from sandbox
    },
  },
  // Per-agent override:
  agents: {
    list: [
      {
        id: "trusted",
        tools: { elevated: { enabled: true } },
      },
      {
        id: "restricted",
        tools: { elevated: { enabled: false } },
      },
    ],
  },
}
```

Both global `tools.elevated` and per-agent `agents.list[].tools.elevated` must allow for elevated exec to work.

## setupCommand Details

`setupCommand` runs **once** after container creation (not every run). Executes via `sh -lc`.

Common pitfalls:
- Default network is `none` — package installs fail without `network: "bridge"`
- `readOnlyRoot: true` prevents writes — set `false` or bake a custom image
- `user` must be root for package installs (omit or set `"0:0"`)
- Sandbox exec does not inherit host `process.env` — use `docker.env` for API keys

## Troubleshooting

### Container Not Starting

```bash
# Check Docker is running
docker info

# Check for existing containers
docker ps -a --filter "name=openclaw"

# Check Docker logs
docker logs <container-id>
```

### Permission Errors

- Ensure `user` in sandbox config matches file ownership in mounted volumes
- Use `:ro` for source mounts to prevent write permission issues
- Check `readOnlyRoot` setting

### Network Unreachable

- Default network is `none` — no outbound access
- Set `docker.network: "bridge"` for outbound access
- Check `docker network ls` for the bridge network
- Browser sandbox uses `openclaw-sandbox-browser` network by default

### setupCommand Failures

```bash
# Test manually
docker run --rm -it openclaw-sandbox:bookworm-slim sh -lc "apt-get update"
```

If it hangs, likely a network issue (default `none`).

## Docker Gateway Deployments

For Docker-based gateway deployments:
```bash
OPENCLAW_SANDBOX=1 docker-setup.sh
```

Override socket: `OPENCLAW_DOCKER_SOCKET=/var/run/docker.sock`
