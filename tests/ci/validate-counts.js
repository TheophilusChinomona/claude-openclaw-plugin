#!/usr/bin/env node
/**
 * Validate that README counts match actual file/directory counts.
 */
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const pluginRoot = path.join(root, "plugins/openclaw");
const errors = [];

// Count actual files
const skillCount = fs
  .readdirSync(path.join(pluginRoot, "skills"))
  .filter((d) => fs.statSync(path.join(pluginRoot, "skills", d)).isDirectory()).length;

const commandCount = fs
  .readdirSync(path.join(pluginRoot, "commands"))
  .filter((f) => f.endsWith(".md")).length;

const agentCount = fs
  .readdirSync(path.join(pluginRoot, "agents"))
  .filter((f) => f.endsWith(".md")).length;

// Parse README
const readme = fs.readFileSync(path.join(root, "README.md"), "utf8");

const skillMatch = readme.match(/### Skills \((\d+)\)/);
const cmdMatch = readme.match(/### Slash Commands \((\d+)\)/);
const agentMatch = readme.match(/### Agents \((\d+)\)/);

if (skillMatch && parseInt(skillMatch[1]) !== skillCount) {
  errors.push(
    `README says ${skillMatch[1]} skills but found ${skillCount}`
  );
}

if (cmdMatch && parseInt(cmdMatch[1]) !== commandCount) {
  errors.push(
    `README says ${cmdMatch[1]} commands but found ${commandCount}`
  );
}

if (agentMatch && parseInt(agentMatch[1]) !== agentCount) {
  errors.push(
    `README says ${agentMatch[1]} agents but found ${agentCount}`
  );
}

// Also check marketplace.json description
const marketplace = JSON.parse(
  fs.readFileSync(path.join(root, ".claude-plugin/marketplace.json"), "utf8")
);
const desc = marketplace.plugins[0].description;
const mktMatch = desc.match(/(\d+)\s+agents?\s*\+\s*(\d+)\s+commands?\s*\+\s*(\d+)\s+skills?/);
if (mktMatch) {
  if (parseInt(mktMatch[1]) !== agentCount) {
    errors.push(`marketplace.json says ${mktMatch[1]} agents but found ${agentCount}`);
  }
  if (parseInt(mktMatch[2]) !== commandCount) {
    errors.push(`marketplace.json says ${mktMatch[2]} commands but found ${commandCount}`);
  }
  if (parseInt(mktMatch[3]) !== skillCount) {
    errors.push(`marketplace.json says ${mktMatch[3]} skills but found ${skillCount}`);
  }
}

if (errors.length > 0) {
  console.error(`FAIL: ${errors.length} count mismatch(es):`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
} else {
  console.log(
    `PASS: Counts match (${agentCount} agents, ${commandCount} commands, ${skillCount} skills)`
  );
}
