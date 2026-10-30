---
name: makeloop
description: Design evidence-driven loops for a project goal or watcher, with progress, adaptation, interruption recovery and copyable host-native launches. Use to build or refine a loop contract, not to run the project work.
---

# makeloop — host-aware entrypoint

## Final output contract — presentation source of truth

This section governs final presentation; references supply execution semantics, not a second
presentation policy. Apply explicit user format/mode choices first, then these defaults:

1. Briefly state the outcome, saved design path and actual generated/configured/started status.
   Keep material unresolved choices or capability gaps visible; do not print the full contract
   unless requested. The saved path is a design reference, not the paste prompt.
2. For a ready closed completion, show Goal completion first (recommended) and ordinary
   current-execution completion second, sharing the same contract/state. Asking to use Goal
   selects the recommendation, not "Goal only". Only an explicit exclusive choice ("Goal only",
   "Goalだけ", no-Goal, bounded pass or another runtime), or real readiness limits overrides
   the pair. Open watchers and unavailable Goal controls do not get fabricated alternatives.
3. End with **貼り付けるプロンプトはこれです** (or the user's language). Before the group say
   to copy one block and not run both. Each label names mode, host and actual paste destination.
   Nothing follows the last fence. Use **実行方法** for Japanese comparisons.
4. Fill the current host guide's launch templates; do not freely compose a setup paragraph.
   Substitute the actual contract path and user's language. Keep native syntax/conditions that
   the host actually requires, but keep Goal lookup/reuse, criterion IDs, state paths, omitted
   budgets, consultation, remediation and history procedures in the saved contract, not repeated
   in the paste block. Explicit required native budget arguments remain on the launch.
5. Before release, compare the assembled final answer to 1–4. A long launch that restates the
   saved lifecycle must be replaced with the template, not excused as "self-contained". Check
   the selected mode count, labels and last-fence rule on the actual final text, not just the file.


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
contracts for an unselected purpose. When clear, derive the usable/delivered result and evidenced
remaining work first. Keep tasks provisional and linked to that result in existing state. Select
the simplest usable execution; the Final output contract above determines completion alternatives.
Preserve supplied choices. Ask only for material ambiguity; use a concise normal chat question if
its question UI is absent. Do not require ritual confirmation for decisions already supplied.

Save `.loop/<slug>.md`, seed closed `-state.md` or open `.cursor.json` only if absent, and maintain
`.loop/INDEX.md`. Hold launch commands and the full Loop body until saving/checks are complete.
Follow the Final output contract above; output-guide.md supplies readiness and copy hygiene.
Outcome-first adaptive recovery and minimum sufficient verification are default closed-loop policy;
the user need not repeat instructions to avoid siloed work, premature blocker stops or test churn.
Default to lean test stewardship too: avoid unnecessary new tests and incrementally consolidate or
remove evidenced redundant/obsolete existing tests in the affected area without a separate request.
Carry the template's preservation, diagnosis and scope rules; never weaken required checks to pass.
The saved contract is authoritative; show its full body only when
explicitly requested. Prefer short new slugs and project-relative paths; never insert a newline
inside a filename/path. Follow output-guide.md for copy-safe launches and existing long names.
For either host's closed completion requests, include the available Goal-equipped launch from the first
proposal; recommend it for requested looping/cross-turn continuation, unless an explicit different
mode wins. Bind the fresh Goal lifecycle from the current host guide during generation. Not configured/not
started is not unavailable; finish stop/lifecycle assembly instead of deferring it as a condition.
Select alternatives by the Final output contract above. They share the same contract/state and
project-derived REMEDIATION SCOPE. Diagnose impediments, perform necessary authorized repairs
and return to original work before considering a terminal blocker; preserve genuine boundaries.
Do not default completion requests to one iteration: no-Goal can pursue successive useful steps
in the current execution, without promising unconfigured cross-turn persistence. A single pass
is bounded only when explicitly selected. Shortening must preserve the original
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
