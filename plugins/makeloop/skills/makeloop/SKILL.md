---
name: makeloop
description: Design evidence-driven loops for a project goal or watcher, with progress, adaptation, interruption recovery and copyable host-native launches. Use to build or refine a loop contract, not to run the project work.
---

# makeloop — host-aware entrypoint

Identify the actual host from the exposed runtime/tools, not the model name. This skill may be
visible in both Claude Code and Codex. On Claude Code, route through the shared generator and
`../../references/claude-code.md`; do not apply Codex-only invocation or launch choices below.
On Codex, use `../../references/codex.md`. Do not alter user-level aliases or plugin installation.

Build the loop contract; do not do the project work. Read
`../../commands/makeloop.md` for the shared generator Steps 0-6. It is the canonical generation
logic, not a Claude-only runtime prescription. Do not fork it into this skill.

Use progressive disclosure:

- Steps 2/6: `../../references/output-guide.md` for purpose choices, explanations and copy format.
- Steps 3/6: `../../references/feedback-design.md` for outcome-to-evidence mapping, adaptive
  decisions, progress, attempt accounting and watcher effect recovery.
- Steps 4/6: the current host reference above for launch/stop/resume and capability boundaries.
- Step 5: `../../templates/loop-prompt.tmpl.md`; select exactly one core and only triggered blocks.

Preserve the three hearts (verify/trigger, state/cursor, stop/dedup), Project Profile,
closed/open distinction, first-VERIFY honesty, cold-start cursor, no-fake-done and maker != checker.
No self-grading, no gate weakening, no unbound output placeholders. Existing state must survive refine.
Judge progress by observed changes, including useful diagnosis; repeated commands alone are not
stalls. A finished plan or clear review must still be reconciled with every original requirement.

Codex invocation is `$makeloop:makeloop` when the plugin prefix is visible, or a discovered slash-menu
skill. Do not invent a Codex `/loop`, `/ralph-loop`, `codex-loop` runner, or a top-level `/makeloop` on Codex. CC may expose `/makeloop` or a namespaced plugin command;
use the actually discovered alias, never remove or duplicate user-level aliases here.

When purpose is ambiguous, explain concrete project-specific choices before writing executable
contracts for an unselected purpose. When purpose is clear, compare ways to run the same contract.
Preserve supplied choices. Ask only for material ambiguity; use a concise normal chat question if
its question UI is absent. Do not require ritual confirmation for decisions already supplied.

Save `.loop/<slug>.md`, seed closed `-state.md` or open `.cursor.json` only if absent, and maintain
`.loop/INDEX.md`. Hold launch commands and the full Loop body until saving/checks are complete.
In ONE final response: explanation/Loop brief and choices, paths/status/gaps, then short copyable
launch blocks at the very end. The saved contract is authoritative; show its full body only when
explicitly requested. Prefer short new slugs and project-relative paths; never insert a newline
inside a filename/path. Follow output-guide.md for copy-safe launches and existing long names.
Nothing follows the last launch fence.
On Codex use **Codex run options** for explained alternatives; use host-native choice labels on CC. Mark exactly one recommendation among ready proposals only. Manual tick
is a default only when no continuation choice was supplied. Shortening must preserve the original
goal, all residual work, continuation/stop mode, consumed/remaining budget with source/enforcement, authority, required
consultation/review and state/resume in the saved contract. An unavailable requested continuation
stays requested/unconfigured; do not silently turn it into one iteration or offer near-exhausted
budget as a fresh completion opportunity. Each executable
choice has its own fully resolved block, labeled with the paste destination. Keep unavailable or
unconfirmed capabilities in separate Conditional options without executable fences.
Complete the output guide's readiness check during this invocation, before presenting any launch.
Bundle necessary user decisions without assuming unanswered choices; if actual state/budget/ownership or host capability prevents
the requested execution, report no executable launch generated instead of a command plus a later
disclaimer. A normal "continue" message is not native continuation setup.
Do not invent a hard default cap. Internal counters trigger progress review/replanning with history
preserved, not count-only termination or extra-budget approval. User/platform limits and real
cost/safety boundaries still bind; read original records when a limit's provenance is unknown.

Explain outcome, actual actions, effects/scope, suitability, check/trigger, stop/cap/expiry, state
and resume for each candidate. Keep detailed criteria in the saved contract instead of repeating
them in the launch. State **generated / not configured / not started** truthfully.
Displaying choices does not start a goal, configure scheduling, select an unchosen runtime, reset
state, or authorize simultaneous writers. Do not create a runner or schedule here.
