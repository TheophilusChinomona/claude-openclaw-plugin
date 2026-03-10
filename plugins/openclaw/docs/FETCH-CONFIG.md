# Documentation Fetch Configuration

## Sources

| Source | Index URL | Content Pattern |
|--------|-----------|-----------------|
| **docs.openclaw.ai** | `https://docs.openclaw.ai/llms.txt` | Direct page URLs from llms.txt |
| **GitHub** | `https://github.com/openclaw/openclaw/tree/main/docs` | `https://raw.githubusercontent.com/openclaw/openclaw/main/docs/<path>` |

## Fetch Methods

| Method | Speed | Use Case | Command |
|--------|-------|----------|---------|
| **Parallel HTTP** | Fast (~30s for 148 pages) | Default for docs.openclaw.ai | `oc-docs-fetch.py sync` |
| **GitHub Tarball** | Fast (~10s for all docs) | GitHub source docs | `oc-docs-fetch.py github` |
| **crawl4ai** | Slow (browser rendering) | JS-heavy pages, fallback | `crawl.py <url> --fit` |
| **WebFetch** | Slow (sequential) | Last-resort single page | Agent/command WebFetch tool |

### Parallel HTTP (default)

Uses `aiohttp` with `asyncio.Semaphore` for concurrent HTTP requests. Default concurrency is 10 simultaneous requests, configurable via `--concurrency N`.

Flow: Fetch llms.txt → parse entries → filter by tier/category → check staleness → parallel download → save with frontmatter → update manifest → regenerate INDEX.md.

### GitHub Tarball

Single `curl` call to download the entire repository tarball, then `tar` extraction of just the `docs/` directory. Fastest method for getting all GitHub-sourced documentation.

### crawl4ai Fallback

For pages that require JavaScript rendering (SPAs, dynamic content), use the crawl4ai plugin's headless browser:
```bash
python ~/.claude/plugins/crawl4ai-plugin/plugins/crawl4ai/scripts/crawl.py <url> --output-dir .crawled --fit
```

Supports `--url-list <file>` for batch fetching from a file of URLs.

## Priority Tiers

### Tier 1 — Core (default sync)

Fetched by default with `/oc-docs sync`. These cover the most commonly referenced topics.

| Category | Estimated Pages |
|----------|----------------|
| automation | ~23 |
| channels | ~31 |
| cli | ~52 |
| concepts | ~8 |
| gateway | ~15 |
| security | ~19 |
| **Total** | **~148** |

### Tier 2 — Extended (--full or --category)

Fetched with `/oc-docs sync --full` or `/oc-docs sync --category <name>`.

| Category | Estimated Pages |
|----------|----------------|
| install | ~28 |
| providers | ~35 |
| tools | ~18 |
| platforms | ~15 |
| reference | ~12 |
| start | ~16 |
| **Total** | **~124** |

### Tier 3 — On Request

Only fetched when explicitly requested by URL or category name.

| Category | Estimated Pages |
|----------|----------------|
| web | ~5 |
| plugins | ~5 |
| root pages | ~3 |
| **Total** | **~13** |

## Staleness Rules

- **Threshold:** 7 days — pages older than this are re-fetched on next sync.
- **Hash comparison:** After re-fetching, compare MD5 content hash. Only overwrite if content changed.
- **Force refresh:** Use `--force` flag to ignore staleness and re-fetch everything.

## Storage Paths

```
.crawled/
  docs.openclaw.ai/       # Pages from docs site, organized by category
    <category>/
      <page-slug>.md
  github/                  # Pages from GitHub raw content
    docs/
      <path>
```

## Manifest Schema

Each entry in `docs-manifest.json`:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title from llms.txt link text |
| `sourceUrl` | string | Original URL of the page |
| `localPath` | string | Relative path under plugin root |
| `source` | string | `"docs-site"` or `"github"` |
| `category` | string | Category extracted from URL path |
| `tier` | number | Priority tier (1, 2, or 3) |
| `fetchedAt` | string | ISO 8601 timestamp of last fetch |
| `contentHash` | string | MD5 hash of fetched content |
| `sizeBytes` | number | File size in bytes |
