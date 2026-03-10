#!/usr/bin/env node
/**
 * SessionStart hook: Suggest /oc-docs sync if .crawled/ is empty or missing,
 * and check if recommended permissions are configured.
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const pluginRoot = path.resolve(__dirname, "..", "..");
const crawledDir = path.join(pluginRoot, ".crawled");
const messages = [];

// Check if .crawled/ exists and has content
try {
  const stat = fs.statSync(crawledDir);
  if (stat.isDirectory()) {
    const entries = fs.readdirSync(crawledDir).filter((e) => !e.startsWith("."));
    if (entries.length === 0) {
      messages.push(
        "OpenClaw docs not synced yet. Run `/oc-docs sync` to fetch core documentation (~148 pages)."
      );
    }
  }
} catch {
  messages.push(
    "OpenClaw docs not synced yet. Run `/oc-docs sync` to fetch core documentation (~148 pages)."
  );
}

// Check if recommended permissions are configured
try {
  const settingsPath = path.join(os.homedir(), ".claude", "settings.json");
  const settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));
  const allow = (settings.permissions && settings.permissions.allow) || [];

  const hasRead = allow.includes("Read");
  const hasBash = allow.some(
    (p) => p === "Bash(*)" || p === "Bash(openclaw *)" || p.startsWith("Bash(openclaw")
  );

  if (!hasRead || !hasBash) {
    messages.push(
      "Recommended: Run `node plugins/openclaw/scripts/setup-permissions.js` to auto-configure permissions for the OpenClaw plugin (avoids repeated approval prompts)."
    );
  }
} catch {
  // Settings file missing or unreadable — skip check
}

if (messages.length > 0) {
  console.error(
    JSON.stringify({
      result: "warn",
      message: messages.join("\n"),
    })
  );
}
