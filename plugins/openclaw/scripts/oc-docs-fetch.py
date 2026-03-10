#!/usr/bin/env python3
"""OpenClaw documentation fetcher — parallel HTTP, GitHub tarball, and status.

Usage:
    python oc-docs-fetch.py sync [--full] [--category NAME] [--force] [--concurrency N]
    python oc-docs-fetch.py github [--force]
    python oc-docs-fetch.py status
    python oc-docs-fetch.py fetch <url>
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Paths (relative to plugin root)
# ---------------------------------------------------------------------------

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
CRAWLED_DIR = PLUGIN_ROOT / ".crawled"
DOCS_SITE_DIR = CRAWLED_DIR / "docs.openclaw.ai"
GITHUB_DIR = CRAWLED_DIR / "github"
DOCS_DIR = PLUGIN_ROOT / "docs"
MANIFEST_PATH = DOCS_DIR / "docs-manifest.json"
INDEX_PATH = DOCS_DIR / "INDEX.md"

LLMS_TXT_URL = "https://docs.openclaw.ai/llms.txt"
GITHUB_TARBALL_URL = "https://api.github.com/repos/openclaw/openclaw/tarball/main"

STALENESS_DAYS = 7

# ---------------------------------------------------------------------------
# Tier map — category → tier
# ---------------------------------------------------------------------------

TIER_MAP = {
    # Tier 1 — Core
    "automation": 1, "channels": 1, "cli": 1, "concepts": 1,
    "gateway": 1, "security": 1,
    # Tier 2 — Extended
    "install": 2, "providers": 2, "tools": 2, "platforms": 2,
    "reference": 2, "start": 2,
    # Tier 3 — On request
    "web": 3, "plugins": 3,
}

DEFAULT_TIER = 3  # anything not in TIER_MAP


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_manifest() -> list:
    if MANIFEST_PATH.exists():
        try:
            data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_manifest(entries: list):
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def content_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def is_stale(entry: dict) -> bool:
    fetched = entry.get("fetchedAt")
    if not fetched:
        return True
    try:
        dt = datetime.fromisoformat(fetched.replace("Z", "+00:00"))
        age = datetime.now(timezone.utc) - dt
        return age.days >= STALENESS_DAYS
    except (ValueError, TypeError):
        return True


def parse_llms_txt(text: str) -> list:
    """Parse llms.txt markdown list into entries."""
    entries = []
    for line in text.splitlines():
        m = re.match(r"^-\s*\[(.+?)\]\((.+?)\)\s*$", line.strip())
        if not m:
            continue
        title = m.group(1)
        url = m.group(2)
        category = extract_category(url)
        tier = TIER_MAP.get(category, DEFAULT_TIER)
        entries.append({
            "title": title if title != "null" else "",
            "url": url,
            "category": category,
            "tier": tier,
        })
    return entries


def extract_category(url: str) -> str:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if parts:
        return parts[0]
    return "root"


def url_to_local_path(url: str) -> str:
    """Convert docs URL to relative local path under .crawled/docs.openclaw.ai/."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "index.md"
    # Remove existing extensions, then add .md
    path = re.sub(r"\.(html?|php|md)$", "", path)
    return path + ".md"


def make_frontmatter(url: str, title: str, word_count: int) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    safe_title = title.replace('"', '\\"')
    return (
        f"---\n"
        f'source_url: {url}\n'
        f'title: "{safe_title}"\n'
        f"crawled_at: {now}\n"
        f"word_count: {word_count}\n"
        f"---\n"
    )


# ---------------------------------------------------------------------------
# Fetch logic
# ---------------------------------------------------------------------------

async def fetch_page(session, sem, entry: dict, force: bool, manifest_map: dict) -> dict:
    """Fetch a single page. Returns result dict."""
    import aiohttp

    url = entry["url"]
    local_rel = url_to_local_path(url)
    local_path = DOCS_SITE_DIR / local_rel

    # Check staleness
    if not force:
        existing = manifest_map.get(url)
        if existing and not is_stale(existing):
            return {"status": "skipped", "url": url, "reason": "fresh"}

    async with sem:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    return {"status": "failed", "url": url, "reason": f"HTTP {resp.status}"}
                text = await resp.text()
        except Exception as e:
            return {"status": "failed", "url": url, "reason": str(e)}

    if not text.strip():
        return {"status": "failed", "url": url, "reason": "empty response"}

    # Compute hash — skip write if unchanged
    new_hash = content_hash(text)
    existing = manifest_map.get(url)
    if existing and existing.get("contentHash") == new_hash and not force:
        # Content hasn't changed, just update timestamp
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return {
            "status": "unchanged",
            "url": url,
            "contentHash": new_hash,
            "fetchedAt": now,
            "localPath": f".crawled/docs.openclaw.ai/{local_rel}",
            "sizeBytes": existing.get("sizeBytes", len(text.encode("utf-8"))),
        }

    # Build output with frontmatter
    title = entry.get("title", "")
    word_count = len(text.split())
    frontmatter = make_frontmatter(url, title, word_count)
    full_content = frontmatter + "\n" + text

    # Write
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_path.write_text(full_content, encoding="utf-8")

    size = len(full_content.encode("utf-8"))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "status": "fetched",
        "url": url,
        "title": title,
        "category": entry["category"],
        "tier": entry["tier"],
        "localPath": f".crawled/docs.openclaw.ai/{local_rel}",
        "contentHash": new_hash,
        "fetchedAt": now,
        "sizeBytes": size,
    }


async def cmd_sync(args):
    import aiohttp

    # 1. Fetch llms.txt
    print("Fetching llms.txt index...", file=sys.stderr)
    async with aiohttp.ClientSession() as session:
        async with session.get(LLMS_TXT_URL, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                print(f"ERROR: Failed to fetch llms.txt (HTTP {resp.status})", file=sys.stderr)
                sys.exit(1)
            index_text = await resp.text()

    # 2. Parse entries
    entries = parse_llms_txt(index_text)
    print(f"Parsed {len(entries)} pages from llms.txt", file=sys.stderr)

    # 3. Filter by tier/category
    if args.category:
        entries = [e for e in entries if e["category"] == args.category]
        print(f"Filtered to category '{args.category}': {len(entries)} pages", file=sys.stderr)
    elif not args.full:
        entries = [e for e in entries if e["tier"] == 1]
        print(f"Tier 1 only: {len(entries)} pages (use --full for all)", file=sys.stderr)

    if not entries:
        print("No pages to fetch.", file=sys.stderr)
        return

    # 4. Load manifest for staleness
    manifest = load_manifest()
    manifest_map = {e["sourceUrl"]: e for e in manifest}

    # 5. Parallel fetch
    CRAWLED_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_SITE_DIR.mkdir(parents=True, exist_ok=True)

    sem = asyncio.Semaphore(args.concurrency)
    total = len(entries)

    fetched = 0
    skipped = 0
    unchanged = 0
    failed = 0
    failures = []

    print(f"\nFetching {total} pages (concurrency={args.concurrency})...\n", file=sys.stderr)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, sem, e, args.force, manifest_map) for e in entries]
        for i, coro in enumerate(asyncio.as_completed(tasks), 1):
            result = await coro
            status = result["status"]

            if status == "fetched":
                fetched += 1
                print(f"  [{i}/{total}] {result.get('category','')}/{Path(result['localPath']).name} ({result['sizeBytes']}B)", file=sys.stderr)
                # Update manifest
                manifest_map[result["url"]] = {
                    "title": result.get("title", ""),
                    "sourceUrl": result["url"],
                    "localPath": result["localPath"],
                    "source": "docs-site",
                    "category": result["category"],
                    "tier": result["tier"],
                    "fetchedAt": result["fetchedAt"],
                    "contentHash": result["contentHash"],
                    "sizeBytes": result["sizeBytes"],
                }
            elif status == "skipped":
                skipped += 1
            elif status == "unchanged":
                unchanged += 1
                # Update timestamp in manifest
                existing = manifest_map.get(result["url"])
                if existing:
                    existing["fetchedAt"] = result["fetchedAt"]
            elif status == "failed":
                failed += 1
                failures.append(f"  {result['url']}: {result['reason']}")

    # 6. Save manifest
    updated_manifest = list(manifest_map.values())
    save_manifest(updated_manifest)

    # 7. Regenerate INDEX.md
    regenerate_index(updated_manifest, entries)

    # 8. Summary
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Sync complete:", file=sys.stderr)
    print(f"  Fetched:   {fetched}", file=sys.stderr)
    print(f"  Unchanged: {unchanged}", file=sys.stderr)
    print(f"  Skipped:   {skipped} (fresh < {STALENESS_DAYS} days)", file=sys.stderr)
    print(f"  Failed:    {failed}", file=sys.stderr)
    if failures:
        print(f"\nFailures:", file=sys.stderr)
        for f_msg in failures:
            print(f_msg, file=sys.stderr)

    # JSON summary to stdout
    summary = {
        "fetched": fetched,
        "unchanged": unchanged,
        "skipped": skipped,
        "failed": failed,
        "total": total,
    }
    print(json.dumps(summary))

    sys.exit(0 if fetched + unchanged + skipped > 0 else 1)


async def cmd_github(args):
    """Download docs from GitHub tarball."""
    print("Downloading GitHub tarball...", file=sys.stderr)

    GITHUB_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Download tarball
        result = subprocess.run(
            ["curl", "-sL", "-o", tmp_path, GITHUB_TARBALL_URL],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            print(f"ERROR: curl failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        # Check if tarball has docs/
        list_result = subprocess.run(
            ["tar", "tzf", tmp_path],
            capture_output=True, text=True, timeout=60,
        )
        doc_files = [
            line for line in list_result.stdout.splitlines()
            if "/docs/" in line and line.endswith(".md")
        ]

        if not doc_files:
            print("No docs/ markdown files found in tarball.", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(doc_files)} doc files in tarball", file=sys.stderr)

        # Extract docs directory
        # The tarball has a prefix like "openclaw-openclaw-abc1234/"
        # We need to strip that prefix and extract docs/ contents
        result = subprocess.run(
            ["tar", "xzf", tmp_path, "-C", str(GITHUB_DIR),
             "--strip-components=1", "--wildcards", "*/docs/*"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            # Try without --wildcards (not all tar implementations support it)
            result = subprocess.run(
                ["tar", "xzf", tmp_path, "-C", str(GITHUB_DIR),
                 "--strip-components=1"],
                capture_output=True, text=True, timeout=60,
            )

        # Update manifest
        manifest = load_manifest()
        manifest_map = {e["sourceUrl"]: e for e in manifest}
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        fetched_count = 0
        docs_root = GITHUB_DIR / "docs"
        if docs_root.exists():
            for md_file in docs_root.rglob("*.md"):
                rel = md_file.relative_to(GITHUB_DIR)
                file_content = md_file.read_text(encoding="utf-8", errors="replace")
                h = content_hash(file_content)
                source_url = f"https://raw.githubusercontent.com/openclaw/openclaw/main/{rel}"

                manifest_map[source_url] = {
                    "title": md_file.stem.replace("-", " ").title(),
                    "sourceUrl": source_url,
                    "localPath": f".crawled/github/{rel}",
                    "source": "github",
                    "category": str(rel.parts[1]) if len(rel.parts) > 1 else "root",
                    "tier": 2,
                    "fetchedAt": now,
                    "contentHash": h,
                    "sizeBytes": len(file_content.encode("utf-8")),
                }
                fetched_count += 1

        save_manifest(list(manifest_map.values()))
        print(f"\nExtracted {fetched_count} docs from GitHub tarball", file=sys.stderr)
        print(json.dumps({"fetched": fetched_count, "source": "github"}))

    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def cmd_status(_args):
    """Show documentation sync status."""
    manifest = load_manifest()

    if not manifest:
        print("No documentation synced yet.")
        print("Run: python oc-docs-fetch.py sync       # Tier 1 (~148 pages)")
        print("Run: python oc-docs-fetch.py sync --full # All tiers (~431 pages)")
        return

    # Count by category and source
    by_category = {}
    by_source = {"docs-site": 0, "github": 0}
    stale_count = 0
    total_bytes = 0

    for entry in manifest:
        cat = entry.get("category", "unknown")
        by_category.setdefault(cat, {"count": 0, "stale": 0, "tier": entry.get("tier", 3)})
        by_category[cat]["count"] += 1
        total_bytes += entry.get("sizeBytes", 0)

        source = entry.get("source", "unknown")
        by_source[source] = by_source.get(source, 0) + 1

        if is_stale(entry):
            stale_count += 1
            by_category[cat]["stale"] += 1

    # Disk usage
    disk_usage = "N/A"
    if CRAWLED_DIR.exists():
        try:
            result = subprocess.run(
                ["du", "-sh", str(CRAWLED_DIR)],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                disk_usage = result.stdout.split()[0]
        except (subprocess.TimeoutExpired, OSError):
            pass

    print(f"OpenClaw Documentation Status")
    print(f"{'='*40}")
    print(f"Total fetched: {len(manifest)} pages")
    print(f"  docs-site:   {by_source.get('docs-site', 0)}")
    print(f"  github:      {by_source.get('github', 0)}")
    print(f"Stale:         {stale_count} (> {STALENESS_DAYS} days)")
    print(f"Storage:       {disk_usage}")
    print()
    print(f"By Category:")

    # Sort: Tier 1 first, then tier 2, then 3; alphabetical within tier
    sorted_cats = sorted(by_category.items(), key=lambda x: (x[1]["tier"], x[0]))
    current_tier = None
    for cat, info in sorted_cats:
        if info["tier"] != current_tier:
            current_tier = info["tier"]
            tier_label = {1: "Tier 1 - Core", 2: "Tier 2 - Extended", 3: "Tier 3 - On Request"}.get(current_tier, f"Tier {current_tier}")
            print(f"\n  [{tier_label}]")
        stale_marker = f" ({info['stale']} stale)" if info["stale"] > 0 else ""
        print(f"    {cat:<15} {info['count']:>3} pages{stale_marker}")


async def cmd_fetch(args):
    """Fetch a single URL."""
    import aiohttp

    url = args.url
    if not url.startswith("https://"):
        print("ERROR: URL must start with https://", file=sys.stderr)
        sys.exit(1)

    category = extract_category(url)
    local_rel = url_to_local_path(url)

    print(f"Fetching {url}...", file=sys.stderr)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                print(f"ERROR: HTTP {resp.status}", file=sys.stderr)
                sys.exit(1)
            text = await resp.text()

    if not text.strip():
        print("ERROR: Empty response", file=sys.stderr)
        sys.exit(1)

    h = content_hash(text)
    word_count = len(text.split())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Determine output directory based on domain
    parsed = urlparse(url)
    if "github" in (parsed.hostname or ""):
        out_dir = GITHUB_DIR
    else:
        out_dir = DOCS_SITE_DIR

    out_path = out_dir / local_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)

    frontmatter = make_frontmatter(url, "", word_count)
    full_content = frontmatter + "\n" + text
    out_path.write_text(full_content, encoding="utf-8")

    size = len(full_content.encode("utf-8"))

    # Update manifest
    manifest = load_manifest()
    manifest_map = {e["sourceUrl"]: e for e in manifest}
    source = "github" if "github" in (parsed.hostname or "") else "docs-site"
    tier = TIER_MAP.get(category, DEFAULT_TIER)

    manifest_map[url] = {
        "title": "",
        "sourceUrl": url,
        "localPath": f".crawled/{'github' if source == 'github' else 'docs.openclaw.ai'}/{local_rel}",
        "source": source,
        "category": category,
        "tier": tier,
        "fetchedAt": now,
        "contentHash": h,
        "sizeBytes": size,
    }
    save_manifest(list(manifest_map.values()))

    print(f"Saved to .crawled/docs.openclaw.ai/{local_rel} ({size}B)", file=sys.stderr)
    print(json.dumps({"status": "fetched", "url": url, "path": str(out_path)}))


# ---------------------------------------------------------------------------
# INDEX.md generation
# ---------------------------------------------------------------------------

TIER_1_CATEGORIES = {"automation", "channels", "cli", "concepts", "gateway", "security"}
TIER_2_CATEGORIES = {"install", "providers", "tools", "platforms", "reference", "start"}
TIER_3_CATEGORIES = {"web", "plugins"}


def regenerate_index(manifest: list, all_entries: list = None):
    """Regenerate docs/INDEX.md from manifest data."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Count by category
    by_category = {}
    for entry in manifest:
        cat = entry.get("category", "unknown")
        by_category.setdefault(cat, 0)
        by_category[cat] += 1

    total_fetched = len(manifest)

    # Compute storage
    total_bytes = sum(e.get("sizeBytes", 0) for e in manifest)
    if total_bytes > 1_000_000:
        storage = f"{total_bytes / 1_000_000:.1f} MB"
    else:
        storage = f"{total_bytes / 1_000:.1f} KB"

    lines = [
        "# OpenClaw Documentation Index\n",
        "",
        "> Auto-generated by `/oc-docs sync`. Do not edit manually.",
        f"> Last updated: {now}",
        "",
        "## Status",
        "",
        f"- **Total known pages:** ~431 (from llms.txt)",
        f"- **Fetched:** {total_fetched} pages",
        f"- **Storage:** {storage}",
        "",
    ]

    def write_tier(label: str, categories: set):
        lines.append(f"### {label}")
        lines.append("")
        for cat in sorted(categories):
            count = by_category.get(cat, 0)
            marker = "x" if count > 0 else " "
            lines.append(f"- [{marker}] **{cat}** ({count} pages fetched)")
        lines.append("")

    write_tier("Tier 1 - Core", TIER_1_CATEGORIES)
    write_tier("Tier 2 - Extended", TIER_2_CATEGORIES)
    write_tier("Tier 3 - On Request", TIER_3_CATEGORIES)

    # Any extra categories not in the predefined sets
    known = TIER_1_CATEGORIES | TIER_2_CATEGORIES | TIER_3_CATEGORIES
    extra = {cat for cat in by_category if cat not in known}
    if extra:
        write_tier("Other", extra)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw documentation fetcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Subcommand")

    # sync
    p_sync = sub.add_parser("sync", help="Fetch docs from docs.openclaw.ai via parallel HTTP")
    p_sync.add_argument("--full", action="store_true", help="Fetch all tiers (not just Tier 1)")
    p_sync.add_argument("--category", type=str, help="Fetch only a specific category")
    p_sync.add_argument("--force", action="store_true", help="Re-fetch everything, ignore staleness")
    p_sync.add_argument("--concurrency", type=int, default=10, help="Max concurrent requests (default: 10)")

    # github
    p_github = sub.add_parser("github", help="Download docs from GitHub tarball")
    p_github.add_argument("--force", action="store_true", help="Re-extract even if already present")

    # status
    sub.add_parser("status", help="Show documentation sync status")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Fetch a single documentation page")
    p_fetch.add_argument("url", help="URL to fetch")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "sync":
        asyncio.run(cmd_sync(args))
    elif args.command == "github":
        asyncio.run(cmd_github(args))
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "fetch":
        asyncio.run(cmd_fetch(args))


if __name__ == "__main__":
    main()
