#!/usr/bin/env node
/**
 * Validate all agents have required frontmatter fields.
 */
const fs = require("fs");
const path = require("path");

const agentsDir = path.resolve(__dirname, "../../plugins/openclaw/agents");
const errors = [];
const required = ["name", "model", "description", "allowed-tools"];

const agentFiles = fs
  .readdirSync(agentsDir)
  .filter((f) => f.endsWith(".md"));

for (const file of agentFiles) {
  const filePath = path.join(agentsDir, file);
  const content = fs.readFileSync(filePath, "utf8");

  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) {
    errors.push(`${file}: missing YAML frontmatter`);
    continue;
  }

  const frontmatter = fmMatch[1];

  for (const field of required) {
    if (!new RegExp(`^${field}:\\s*`, "m").test(frontmatter)) {
      errors.push(`${file}: missing '${field}' in frontmatter`);
    }
  }
}

if (errors.length > 0) {
  console.error(`FAIL: ${errors.length} agent validation error(s):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
} else {
  console.log(`PASS: All ${agentFiles.length} agents validated`);
}
