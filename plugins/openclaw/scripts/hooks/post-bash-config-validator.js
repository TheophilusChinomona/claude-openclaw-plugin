#!/usr/bin/env node
/**
 * PostToolUse/Bash hook: Remind to run `openclaw doctor` after config changes.
 */

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

// Only trigger after openclaw config set commands
if (!/\bopenclaw\s+config\s+set\b/.test(command)) {
  process.exit(0);
}

console.error(
  JSON.stringify({
    result: "warn",
    message:
      "Configuration changed. Run `openclaw doctor` to validate the new configuration.",
  })
);
