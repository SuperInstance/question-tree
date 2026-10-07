# HOOKS.md — pull, don't push

A hook is a documented phrase that tells the agent to fetch a capability
and install it into itself. No installation, no provisioning — read the
docs, say the phrase, watch it become.

## Format

`hook: <name>` — one line in chat.
The agent fetches the skill doc at the location below, reads it, and
adopts the capability (as a question-tree skill leaf, committed).

## Registry

### hook: jev
**Grabs:** the Jev (Typesafe) judgment skill — cheap, fast, System-1
calls for snap decomposition, scoring, and triage.
**Source:** `skills/jev/SKILL.md` in this repo (or the canonical URL).
**After:** the agent can spend Jev calls the way it spends words —
constantly, cheaply — and escalate to the LLM at collision points.

### hook: witness
**Grabs:** the witness-mark discipline — log where you stopped and why,
read marks before turning the crank.
**Source:** `WITNESS.md` in this repo.
**After:** the agent charts rocks, not just anchorages.

## Adding a hook

1. Write the SKILL.md (what it is, when to use it, how, what it won't do).
2. Add it to the registry above: phrase, source, after.
3. The phrase is the install button. Keep it short enough to say.
