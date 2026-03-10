#!/usr/bin/env node
/**
 * Validate all skills have required frontmatter fields and references/ directory.
 */
const fs = require("fs");
const path = require("path");

const skillsDir = path.resolve(__dirname, "../../plugins/openclaw/skills");
const errors = [];

const skillDirs = fs
  .readdirSync(skillsDir)
  .filter((d) => fs.statSync(path.join(skillsDir, d)).isDirectory());

for (const dir of skillDirs) {
  const skillMd = path.join(skillsDir, dir, "SKILL.md");
  const refsDir = path.join(skillsDir, dir, "references");

  // Check SKILL.md exists
  if (!fs.existsSync(skillMd)) {
    errors.push(`${dir}: missing SKILL.md`);
    continue;
  }

  // Parse YAML frontmatter
  const content = fs.readFileSync(skillMd, "utf8");
  const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) {
    errors.push(`${dir}: missing YAML frontmatter`);
    continue;
  }

  const frontmatter = fmMatch[1];

  if (!/^name:\s*.+/m.test(frontmatter)) {
    errors.push(`${dir}: missing 'name' in frontmatter`);
  }

  if (!/^description:\s*/m.test(frontmatter)) {
    errors.push(`${dir}: missing 'description' in frontmatter`);
  }

  // Check references/ directory exists
  if (!fs.existsSync(refsDir) || !fs.statSync(refsDir).isDirectory()) {
    errors.push(`${dir}: missing references/ directory`);
  }
}

if (errors.length > 0) {
  console.error(`FAIL: ${errors.length} skill validation error(s):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
} else {
  console.log(`PASS: All ${skillDirs.length} skills validated`);
}
