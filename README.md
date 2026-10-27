# makeloop

A Claude Code and Codex plugin that **builds loop prompts for you**.

Claude Code `/makeloop` or Codex `$makeloop:makeloop` reads your current project **and the session conversation**, pins down the work
goal, offers purpose-led choices and emits a complete, copyable loop contract —
goal, strict success criteria, observations, adaptive decisions, recoverable state and stopping,
**written in your working language**. It generates the prompt; it does not run the loop.

## Loop engineering in makeloop

Design the feedback that makes each iteration advance the goal: **unmet requirement → hypothesis
and predicted result → small action → observed evidence → next decision**. The saved contract
defines what progress means, how to change approach when it stalls, and how to recover after an
interruption. A finished task list or a clear review leads back to the original requirements;
completion requires evidence for all of them, including any required delivery.

The design has two decisions: what to do next within an iteration, and whether the original goal
has been achieved. A passing check for one subtask does not erase the remaining requirements.
Once the goal is proved, the loop finishes; unrelated improvements do not extend it.

| Situation | Generated behavior |
| --- | --- |
| Same test command, improving results | Continue from the evidenced progress |
| Different commands, unchanged failure and no new evidence | Change the hypothesis or narrow the action; respect actual user/platform stop boundaries |
| Green gate, uncovered requirement or missing mandatory suite | Obtain the missing proof; no completion claim |
| Independent approval without evidence for a required dimension | Keep that dimension unproved; calibrate a new/custom verifier |
| Interrupted attempt | Keep its pre-reserved budget slot and reconcile existing work |
| Notification/action timed out | Preserve pending intent; reconcile receipts before any retry |
| Same worker crashes again | Use the new occurrence identity; do not dedup by worker alone |
| Budget exhausted | Preserve unmet scope and report an incomplete checkpoint; stop the native execution separately |

These rules fit the existing file-backed contract. They do not add a scheduler, execution engine
or database. The on-demand [feedback design guide](plugins/makeloop/references/feedback-design.md)
contains the generation decisions; only the relevant contract is carried into each run.

Optional planning, review cadence and context workarounds must have a current purpose. Reassess
them after model/host changes through comparable examples, preserving required checks and user
boundaries. Maintain the feedback system as well as the task it drives.

For unattended closed work, a **[handoff summary](plugins/makeloop/README.md#handoff-summary-claude-code-and-codex)**
leaves results, verification, remaining work and the next action in existing state. It applies
during the day as well as overnight and is updated at checkpoints and completion/interruption,
not at a fixed morning time. Ordinary interactive work does not acquire it just for being long.

## Choose by what you want to do

makeloop separates **purpose** from **execution mode**. If the goal is unclear, compare concrete
project-specific purposes before creating a contract. When clear, trace the usable/delivered
result and derive necessary remaining work first. The task list is provisional: as evidence
changes, the actor discovers further tasks needed for that same result, not unrelated improvements.
Recommend the simplest available execution; offer one or several choices only when useful or
requested, without a fixed menu size. Goal/no-Goal changes continuation, not required work/quality:

| Want to… | Choice | What the explanation covers |
| --- | --- | --- |
| Finish the accepted repair or milestone | Ordinary execution, or native Goal when cross-turn pursuit is needed and available | Necessary tasks, use-path evidence, authorized delivery/review, real limits and resume |
| Inspect one bounded step first | One manual iteration | What may change, what is checked, remaining work and how to continue |
| Watch for new events | Open watcher tick or supported cadence | Signal, new-event dedup, notification/action scope, cursor, expiry and cancellation |
| Continue from CI or a wrapper | Exact-session resume, when requested | Working directory, state ownership and uncertain-effect reconciliation |

Each choice explains when it fits **and when it does not**, its actual effects and permissions,
its saved state and its stopping condition. A watcher is not an alternative implementation of a
repair. Choices are derived from the project, not fixed presets or a menu padded with irrelevant tools.

For closed completion work on either host, the initial proposal includes a Goal-equipped launch when
available, recommended for requests to keep looping until completion. Explicit no-Goal or
bounded-pass choices still win. The generator binds the Goal lifecycle before presenting it;
not configured/not started is not the same as unavailable. Actual blocked-resume, ownership
and hard-limit constraints remain explicit.

When both modes are ready and no other runtime was selected, the initial package pairs
recommended Goal completion with ordinary current-execution completion. Both use the same
contract/state and project-derived REMEDIATION SCOPE: diagnose an impediment, perform necessary
authorized repairs, verify them and return to original work without a fresh repair request.
Only an evidenced lack of productive authorized recovery/independent work supports a blocker
stop. Real authority, authentication and native runtime boundaries remain; no auto-resume runner
or counter reset is introduced.

No-Goal does not mean one iteration: ordinary execution may pursue successive useful steps in
the current execution, but does not configure cross-turn persistence. An explicitly requested
single pass remains bounded. Green parser tests alone do not finish an app's CSV import/save
workflow; the contract traces input, display, save and read-back as required by the actual goal.

**Final-only output:** no launch commands or full Loop body during progress or questions. Once
files and checks are complete, one final response contains the explanations and candidate choices,
then the short saved-contract path (full body only on explicit request), then **all launch blocks
at the very end**. Nothing follows the last
launch block. Each block is independent and labeled by host and paste destination; explanations
and shell prompts stay outside, necessary shell quotes stay inside. Unknown features remain
conditional explanations without runnable blocks. This replaces the former launch-first ordering.
Use short, meaningful new filenames and project-relative paths. Put state, limits and authority
in the saved contract instead of repeating them in each launch. Existing paths/state are preserved.
Neither one physical line nor a code fence guarantees that selection-copy preserves line breaks.
Shortening must preserve the requested continuation, residual work, review and cumulative budget
in the saved contract. An unavailable goal stays unconfigured; a single pass is not an equivalent
replacement. User/platform budget exhaustion is not a fresh completion allowance.
Internal iteration counts instead trigger evidence review and replanning, not stopping at an
agent-invented 8 or asking permission for another batch. Preserve history and actual limits.
Launch readiness is resolved before copy blocks; an unusable requested mode yields no launch
block, not a convincing command followed by an unusable caveat.

**Generated is not started.** Displaying goal/schedule alternatives does not create them, replace
an existing goal, reset a cursor or authorize concurrent writers. Existing `.loop/` files are not
bulk-migrated; refining preserves unrelated choices and progress.

## Say where to stop

Use ordinary language: "pause once the changes and checks are ready, before human review" or
"work within 30 minutes, maximum 8 iterations; leave a checkpoint if unfinished". The final brief
summarizes **how it stops**, alongside the saved instructions. No new configuration format is needed.

An optional pause preserves the original goal and mandatory review; it does not declare them
complete. Explicit resume releases that one pause, not approvals or consumed limits. Without a
pause request, behavior is unchanged. Caps are not automatically extended, and a quiet watcher is
not a stalled repair. Native stopping is capability-checked; unsupported pause modes remain
unconfigured with a bounded manual alternative. A prompt alone is not an exact-time kill switch.

## Install

Claude Code:

```
/plugin marketplace add usedhonda/makeloop
/plugin install makeloop
```

Then:

```
/makeloop
/makeloop finish the auth refactor   # optional goal hint
```

Codex:

```
codex plugin marketplace add usedhonda/makeloop
codex plugin add makeloop@makeloop
```

In the Codex app, type `/` and choose **makeloop** from the slash menu when it appears. In Codex
CLI, use `/skills` to browse skills or call the same skill explicitly:

```
$makeloop:makeloop
$makeloop:makeloop finish the auth refactor   # optional goal hint
```

Codex CLI does not currently support a typed top-level `/makeloop` command. The legacy custom
prompt form (`/prompts:makeloop`) is deprecated by Codex and may not appear in current CLI slash
completion even when `~/.codex/prompts/makeloop.md` exists. The helper below is retained only for
older Codex builds that still load custom prompts:

```
node plugins/makeloop/scripts/install-codex-prompt-shim.mjs
```

## What you get

A loop prompt grounded in loop-engineering practice — built around the three things that
make a loop work instead of just burn tokens:

- **Verify** — a real gate (test / build / lint), never the agent grading its own homework.
- **State** — `.loop/<slug>-state.md` carries criterion evidence, consumed attempts, observed
  progress and the next decision across iterations.
- **Stop condition** — verified success or the configured cap, with native enforcement stated
  separately from an instruction in the contract.

`/makeloop` first builds a read-only **Project Profile** and **sizes the loop to it** — lean
for a single `npm test`, richer (two-stage gate, harness-failure detection, labeled stop
taxonomy, budget) when the project has a build + regression audit or a self-driving harness.

It judges the project's **maturity** too: for a greenfield/empty repo it generates a loop that
*bootstraps its own gate* (scaffold + failing acceptance tests, then drives red → green)
instead of calling a loop the wrong tool; for a mature repo it reuses the existing gate.

And it judges the **loop kind** — **closed** (drive-to-done: goal + verify gate + `FINAL`) vs
**open** (watch/react: a trigger condition + notify/act + dedup, runs indefinitely, no
`FINAL`). For an open watcher "no completion gate" is correct, so the wrong-tool warning is
suppressed; on ambiguity it defaults to closed.

The full contract is saved to `.loop/<slug>.md`, with progress/cursor and `.loop/INDEX.md`.
Chat presents explanations and the chosen Loop body only in the final package, with all
resolved launch blocks last and nothing after them. Select execution from the whole requested job,
not a default single iteration; explicit completion/cadence/CI intent
selects a supported native mode. Unsupported features are conditional explanations, not runnable
copy blocks. Generation does not start a loop, configure scheduling or overwrite existing state.
`makeloop` will also tell you when a loop is the wrong tool (no automated check -> a single good
prompt wins).

See [`plugins/makeloop/README.md`](plugins/makeloop/README.md) for details.

## Repository layout

```
.agents/plugins/marketplace.json    # Codex marketplace manifest (one plugin: makeloop)
.claude-plugin/marketplace.json   # marketplace manifest (one plugin: makeloop)
plugins/makeloop/
  .codex-plugin/plugin.json        # Codex plugin manifest
  .claude-plugin/plugin.json       # plugin manifest
  commands/makeloop.md             # shared generator and /makeloop entrypoint
  skills/makeloop/SKILL.md         # the $makeloop:makeloop Codex skill
  templates/loop-prompt.tmpl.md    # the generated loop-prompt template (canonical)
  references/                     # on-demand profile, output and host launch guides
  validation/                     # supplemental synthetic-output cases and checker
  eval/scenarios.md                # golden eval — objective quality gate for makeloop itself
  eval/codex-scenarios.md          # Codex-surface eval — skill/plugin launch contract
  scripts/install-codex-prompt-shim.mjs # optional local Codex slash-like prompt shim installer
  SELF-IMPROVEMENT.md              # governance contract for makeloop's self-strengthening loop
  AUTOMATION.md                    # operator runbook for the every-2-days self-improvement cron
  loop-engineering-notes.md        # technique catalog + self-improvement run history + fleet-mode roadmap
  README.md                        # plugin docs
```

## Self-improvement (for maintainers)

makeloop can strengthen itself on a schedule. A local cron runs one harvest → gate → apply cycle
every 2 days: it adopts community loop-engineering techniques that pass a **deterministic safety
gate** (`.githooks/gate.sh`) plus an adversarial fit-critic, and prunes to stay lean (homeostasis,
not bloat). Gate-passed **Tier-1** edits auto-commit and push to `main`; anything that changes core
behavior or weakens a constraint **escalates to a human** instead. The trust anchor is read-only to
the loop (enforced out-of-band by settings deny + a pre-commit hook + `chmod`). Governance lives in
[`plugins/makeloop/SELF-IMPROVEMENT.md`](plugins/makeloop/SELF-IMPROVEMENT.md); the operator runbook
(install, pause/resume, undo) in [`plugins/makeloop/AUTOMATION.md`](plugins/makeloop/AUTOMATION.md).
The system is opt-in; fresh clones ship **PAUSED** (enable after a watched run — see AUTOMATION.md).
Each run that changes a public file is logged in `loop-engineering-notes.md` § Self-improvement run
history, alongside `git log --author=makeloop-selfimprove`.

## License

MIT — see [LICENSE](LICENSE).
