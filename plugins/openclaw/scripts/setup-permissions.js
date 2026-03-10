#!/usr/bin/env node
/**
 * Setup recommended permissions for the OpenClaw plugin.
 * Run: node plugins/openclaw/scripts/setup-permissions.js
 *
 * Adds Read, Edit, Write, Glob, Grep and common Bash patterns to the user's
 * ~/.claude/settings.json allowlist so Claude doesn't prompt on every action.
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const settingsPath = path.join(os.homedir(), ".claude", "settings.json");

const RECOMMENDED = [
  "Read",
  "Edit",
  "Write",
  "Glob",
  "Grep",
  "Bash(git *)",
  "Bash(ls *)",
  "Bash(node *)",
  "Bash(npm *)",
  "Bash(npx *)",
  "Bash(python *)",
  "Bash(which *)",
  "Bash(uname *)",
  "Bash(mkdir *)",
  "Bash(claude *)",
  "Bash(openclaw *)",
];

let settings;
try {
  settings = JSON.parse(fs.readFileSync(settingsPath, "utf8"));
} catch {
  settings = {};
}

if (!settings.permissions) settings.permissions = {};
if (!Array.isArray(settings.permissions.allow)) settings.permissions.allow = [];

const existing = new Set(settings.permissions.allow);
const added = [];

for (const perm of RECOMMENDED) {
  if (!existing.has(perm)) {
    settings.permissions.allow.push(perm);
    added.push(perm);
  }
}

if (added.length === 0) {
  console.log("All recommended permissions are already configured.");
  process.exit(0);
}

fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + "\n");
console.log(`Added ${added.length} permission(s) to ${settingsPath}:`);
for (const p of added) {
  console.log(`  + ${p}`);
}
console.log("\nRestart Claude Code for changes to take effect.");
