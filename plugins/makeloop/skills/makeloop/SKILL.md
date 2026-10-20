---
name: makeloop
description: Generate file-backed loop contracts with explained, copyable Codex launch choices for a project goal or watcher. Use to build or refine a loop, not to run the project work.
argument-hint: "[goal hint (optional)]"
---

# makeloop for Codex

Build the loop contract; do not do the project work. Read
`../../commands/makeloop.md` for the shared generator Steps 0-6. It is the canonical generation
logic, not a Claude-only runtime prescription. Do not fork it into this skill.

Use progressive disclosure:

- Steps 2/6: `../../references/output-guide.md` for purpose choices, explanations and copy format.
- Steps 4/6: `../../references/codex.md` for Codex launch/stop/resume and capability boundaries.
- Step 5: `../../templates/loop-prompt.tmpl.md`; select exactly one core and only triggered blocks.

Preserve the three hearts (verify/trigger, state/cursor, stop/dedup), Project Profile,
closed/open distinction, first-VERIFY honesty, cold-start cursor, no-fake-done and maker != checker.
No self-grading, no gate weakening, no unbound output placeholders. Existing state must survive refine.

Invocation is `$makeloop:makeloop` when the plugin prefix is visible, or a discovered slash-menu
skill. Do not invent a Codex `/loop`, `/ralph-loop`, `codex-loop` runner, or a top-level `/makeloop`.

When purpose is ambiguous, explain concrete project-specific choices before writing executable
contracts for an unselected purpose. When purpose is clear, compare ways to run the same contract.
Preserve supplied choices. Ask only for material ambiguity; use a concise normal chat question if
its question UI is absent. Do not require ritual confirmation for decisions already supplied.

Save `.loop/<slug>.md`, seed closed `-state.md` or open `.cursor.json` only if absent, and maintain
`.loop/INDEX.md`. Lead with a copyable fenced `text` launch message and a concrete **Loop brief**.
Use **Codex run options** for explained alternatives with exactly one recommendation. Manual tick
is the safe-first-run default; honor explicit goal/cadence/CI intent when supported. Each executable
choice has its own fully resolved block, labeled with the paste destination. Keep unavailable or
unconfirmed capabilities in separate Conditional options without executable fences.

Explain outcome, actual actions, effects/scope, suitability, check/trigger, stop/cap/expiry, state
and resume for each candidate. Keep detailed criteria and the full contract in saved files rather
than dumping them into chat. State **generated / not configured / not started** truthfully.
Displaying choices does not start a goal, configure scheduling, select an unchosen runtime, reset
state, or authorize simultaneous writers. Do not create a runner or schedule here.
