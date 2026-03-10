#!/usr/bin/env node
/**
 * Validate all commands have required frontmatter fields.
 */
const fs = require("fs");
const path = require("path");

const commandsDir = path.resolve(__dirname, "../../plugins/openclaw/commands");
const errors = [];

const cmdFiles = fs
  .readdirSync(commandsDir)
  .filter((f) => f.endsWith(".md"));

for (const file of cmdFiles) {
  const filePath = path.join(commandsDir, file);
  const content = fs.readFileSync(filePath, "utf8");

  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) {
    errors.push(`${file}: missing YAML frontmatter`);
    continue;
  }

  const frontmatter = fmMatch[1];

  if (!/^description:\s*/m.test(frontmatter)) {
    errors.push(`${file}: missing 'description' in frontmatter`);
  }
}

if (errors.length > 0) {
  console.error(`FAIL: ${errors.length} command validation error(s):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
} else {
  console.log(`PASS: All ${cmdFiles.length} commands validated`);
}
