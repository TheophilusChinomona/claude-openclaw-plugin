#!/usr/bin/env node
/**
 * Run all plugin validators.
 * Usage: node tests/run-all.js
 */
const { execSync } = require("child_process");
const path = require("path");

const tests = [
  "ci/validate-skills.js",
  "ci/validate-commands.js",
  "ci/validate-agents.js",
  "ci/validate-counts.js",
];

let passed = 0;
let failed = 0;

console.log("Running plugin validators...\n");

for (const test of tests) {
  const testPath = path.join(__dirname, test);
  try {
    const output = execSync(`node "${testPath}"`, { encoding: "utf8" });
    console.log(output.trim());
    passed++;
  } catch (err) {
    console.error(err.stdout || "");
    console.error(err.stderr || "");
    failed++;
  }
}

console.log(`\n${passed} passed, ${failed} failed out of ${tests.length} validators`);
process.exit(failed > 0 ? 1 : 0);
