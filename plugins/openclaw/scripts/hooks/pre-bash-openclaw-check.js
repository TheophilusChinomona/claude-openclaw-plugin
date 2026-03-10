#!/usr/bin/env node
/**
 * PreToolUse/Bash hook: Warn if `openclaw` CLI is not installed
 * when the bash command references openclaw gateway commands.
 */
const { execSync } = require("child_process");

const input = (() => {
  try {
    const chunks = [];
    const fd = require("fs").openSync("/dev/stdin", "r");
    const buf = Buffer.alloc(4096);
    let n;
    while ((n = require("fs").readSync(fd, buf)) > 0) chunks.push(buf.slice(0, n));
    require("fs").closeSync(fd);
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    return {};
  }
})();

const command = (input.tool_input && input.tool_input.command) || "";

// Only check when the command references openclaw
const openclawPatterns = [
  /\bopenclaw\s+(status|doctor|gateway|channels?|config|logs|pairing|agents?|cron|security|nodes|devices|backup|update)/,
  /\bopenclaw\b/,
];

const isOpenClawCommand = openclawPatterns.some((p) => p.test(command));
if (!isOpenClawCommand) {
  process.exit(0);
}

// Check if openclaw is installed
try {
  execSync("which openclaw", { stdio: "pipe" });
} catch {
  console.error(
    JSON.stringify({
      result: "warn",
      message:
        "OpenClaw CLI is not installed. Install it with: npm install -g openclaw@latest\nThen run: /oc-setup",
    })
  );
  process.exit(0);
}
