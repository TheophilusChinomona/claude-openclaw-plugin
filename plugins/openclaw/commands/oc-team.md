---
description: Scaffold and manage agent team workspace
argument-hint: <init|soul|validate|show> [agent-id]
allowed-tools: Bash, Read, Write
---

# /oc-team Command

Manage agent team workspace — scaffold directories, generate SOUL.md templates, validate registry, show team structure.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **subcommand** (required): `init`, `soul`, `validate`, or `show`
- **agent-id** (required for `soul`): lowercase slug identifier for the agent

## Subcommands

### `init`

Scaffold the agent team workspace directory structure.

1. Ask the user for the workspace path (default: current directory).
2. Ask for a comma-separated list of agent IDs to create (or use a sensible default like `jarvis`).
3. Create the directory structure:

```bash
WORKSPACE="<path>"
mkdir -p "$WORKSPACE"/{agents,team-memory,clawport}

for agent in <agent-list>; do
  mkdir -p "$WORKSPACE/agents/$agent"/{logs,output}
  touch "$WORKSPACE/agents/$agent/MEMORY.md"
  touch "$WORKSPACE/agents/$agent/SOUL.md"
done

touch "$WORKSPACE/team-memory"/{market-brief,icp-profile,competitor-map,brand-voice,content-calendar}.md
touch "$WORKSPACE/MEMORY.md"
```

4. Create a starter `clawport/agents.json` with the first agent as orchestrator (`reportsTo: null`) and the rest as direct reports.
5. Report what was created.

### `soul <agent-id>`

Generate a SOUL.md template for the given agent.

1. If `clawport/agents.json` exists, read it to get the agent's name, role, reports-to, and direct-reports.
2. Generate a SOUL.md template using this structure:

```markdown
# AGENT_NAME -- Role Title

## Identity
I am AGENT_NAME, the [Role Title]. [Describe personality and communication style].

## Expertise
- [Domain 1]
- [Domain 2]

## Operating Rules
- [Constraint 1]
- [Constraint 2]

## Relationships
- Reports to: [Parent Agent] ([Role])
- Manages: [Child agents, if any]
- Collaborates with: [Peer agents]

## Memory
- Persistent knowledge lives at agents/<id>/MEMORY.md
- Daily logs written to agents/<id>/logs/
```

3. Write the template to `agents/<agent-id>/SOUL.md`.
4. Tell the user to customize the personality, expertise, and constraints.

### `validate`

Read `clawport/agents.json` and check hierarchy rules:

1. **One root:** Exactly one agent has `"reportsTo": null`.
2. **Consistent relationships:** If B has `"reportsTo": "A"`, then A's `directReports` includes B's id, and vice versa.
3. **Max depth of 3:** No chain from root to leaf exceeds 3 levels.
4. **Valid tool assignment:** Leaf agents should not have `exec` or `sessions_spawn`. Flag violations as warnings.
5. **Required fields:** Every agent has `id`, `name`, `role`, `reportsTo`, `directReports`, `tools`, `soulPath`, `memoryPath`.
6. **Unique IDs:** No duplicate agent IDs.
7. **No dangling references:** Every ID in `reportsTo` and `directReports` refers to an existing agent.

Report results with pass/fail per check. For failures, explain what's wrong and how to fix it.

### `show`

Read `clawport/agents.json` and print an ASCII org tree:

1. Find the root agent (`reportsTo: null`).
2. Recursively render the tree using `directReports`.
3. Format:

```
Jarvis (Orchestrator)
  +-- VERA (Strategy)
  |     +-- Robin (Field Intel)
  |           +-- TRACE (Market Research)
  |           +-- PROOF (Validation Design)
  +-- LUMEN (SEO)
  |     +-- SCOUT (Content Scout)
  |     +-- WRITER (Content Writer)
  +-- Pulse (Trend Radar)
```

4. Below the tree, show a summary: total agents, max depth, number of teams.

### No subcommand or unrecognized

Show usage help:
```
Usage: /oc-team <subcommand> [args]

  init              Scaffold agent team workspace
  soul <agent-id>   Generate SOUL.md template
  validate          Check agents.json hierarchy rules
  show              Print ASCII org tree
```

## After Running

- For `init`: suggest running `/oc-team soul <id>` for each agent to fill in SOUL.md files.
- For `soul`: remind the user to customize the generated template.
- For `validate`: if all checks pass, suggest launching ClawPort with `clawport dev`.
- For `show`: if the tree looks unbalanced (>10 direct reports on root), suggest grouping agents under team leads.
