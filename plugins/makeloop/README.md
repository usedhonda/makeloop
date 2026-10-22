# makeloop

A Claude Code slash command and Codex skill that **build loop prompts for you**.

Claude Code `/makeloop` or Codex `$makeloop:makeloop` reads your current project **and the session conversation**, figures out the work
goal, offers purpose-led choices and emits a complete, copyable loop contract —
goal, strict success criteria, observations, adaptive decisions, recoverable state and stopping,
**written in your working language**. It does **not** run the loop; it produces the prompt you
then feed to the host agent.

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

## Usage

Claude Code:

```
/makeloop                  # analyze the project and build a loop prompt
/makeloop finish the auth refactor   # optional: pass a goal hint
```

Codex:

```
$makeloop:makeloop                  # analyze the project and build a loop prompt
$makeloop:makeloop finish the auth refactor   # optional: pass a goal hint
```

In the Codex app, enabled skills may appear in the slash command list, so type `/` and choose
**makeloop** when it is shown. In Codex CLI, use `/skills` to browse skills or call
`$makeloop:makeloop` directly. Codex CLI does not currently accept a typed top-level `/makeloop`
command, and the legacy custom prompt form (`/prompts:makeloop`) is deprecated and may not appear
in current CLI slash completion. `scripts/install-codex-prompt-shim.mjs` is retained only for older
Codex builds that still load custom prompts.

### Inline directives

The text after `/makeloop` or `$makeloop:makeloop` is parsed for both a **goal** and **operational directives** —
anything you decide up front is honored and its question is skipped. Natural phrasing, not
strict flags:

```
/makeloop QA all green, ralph-loop, cap 20, with harness detection, ask minimally
/makeloop 全テストを緑に、30分ごと、上限15、質問は最小で
$makeloop:makeloop QA all green, cap 20, with harness detection, ask minimally
```

Recognized: goal/scope, runtime (`self-paced` / `interval 30m` / `ralph-loop`), iteration
cap & budget (`cap 20`, `wall-clock 30min`, `no-progress 3`), success streak (`K=3`), an
explicit verify gate (`gate: npm test && tsc`), forcing optional blocks on/off
(`two-stage gate`, `no budget block`, `harness off`), and interaction level
(`don't ask` / `just generate`). Anything you omit falls back to its normal question.
`/makeloop` echoes a one-line summary of what it parsed so you can correct it.

The generator asks only for material ambiguity, using one consolidated proposal rather than
separate scope/gate/runtime question rounds. It honors supplied decisions. The selected contract
is saved as `.loop/<slug>.md`, with closed `-state.md` or open `.cursor.json` seeded only if absent.
The final package explains the choices, shows the chosen Loop body, and ends with resolved launches.

Claude Code can offer `/goal` for closed completion, `/loop` for dynamic/fixed waiting and an
installed ralph-loop workflow. Codex can offer manual ticks, `/goal`, supported chat/project
scheduled tasks and exact-session `codex exec resume` for CI. Availability is verified per surface;
CLI alone is not a scheduler management interface. A normal message is the portable first-run path.

`FINAL` reports contract success; it does not cancel a native job. CC session loops expire after
seven days and self-paced wakeups are not restored on resume. Native goal evaluators do not
independently execute acceptance checks. The saved contract explains its real stop/restart behavior.
Use only one continuation owner for a shared state file.

## Depth that matches the project

`/makeloop` reads **two things**: the **live session conversation** (what you've been working
on, what you just asked for, decisions made, errors hit — the *intent*) and the **project
state** (git diff, code, tests — the *reality*), and reconciles them. From the project it
builds a read-only **Project Profile**: **maturity** (greenfield → scaffolded-but-no-gate →
mature), verification depth (single- vs multi-stage), whether there's a self-driving test
harness that can fail silently, hard invariants and off-limits boundaries, existing loop
infrastructure to extend, and commit conventions. It judges maturity from the files — no
flag — and adapts:

- **Greenfield / empty** — instead of declaring "no gate → loop is the wrong tool", the loop
  *bootstraps its own gate*: iteration 0 scaffolds the project and writes the acceptance
  criteria as failing tests, then drives red → green.
- **Mature** — reuses the gate the project already has.

It also judges the **loop kind** and shapes the prompt to match:

- **Closed (drive-to-done)** — a goal with a SUCCESS CRITERION that ends the loop: GOAL +
  VERIFY gate + iterate-to-green + `FINAL`. (The default.)
- **Open (watch / react)** — a monitor with no end-state: a WATCH TARGET + TRIGGER CONDITION +
  observe→evaluate→notify/act + dedup/cursor, runs indefinitely (or stop-on-event), **no
  FINAL**. For a watcher, "no completion gate" is correct — so the "loop is the wrong tool"
  warning is suppressed. On ambiguity it defaults to closed (the safer error).

The generated loop is also **sized to the profile** — it stays lean for a project with one
`npm test`, and grows the advanced blocks when the project supports them:

- **Two-stage gate** with an initial baseline and affected/final acceptance checks, with
  FREEZE-no-commit on regression. Expected repair failures are not poisoned baselines.
- **Observation-validity check** + `unrecoverable-harness` / `pinata` stops, for self-driving
  harnesses that emit screenshots/snapshots.
- **Regression-guard step** (one minimal case per fix) when `scenarios/`/golden files exist.
- **Budget** + a **labeled stop taxonomy** (`no-progress`, `oscillation`, `failure`,
  `scope-boundary`, …) for autonomous loops.

For large or unfamiliar codebases, exploration agents are used only when delegation is explicitly
authorized; otherwise discovery stays in the current conversation.

### Hardening built into every generated loop

Beyond the three hearts, each loop is shaped by lessons from loop-engineering practice:

- **Re-anchor every iteration** — re-read goal + criteria + rules, not just state, so a long
  run doesn't drift past its "do not touch" boundaries.
- **Backpressure ladder** — run checks fastest→slowest, stop at the first red.
- **Search before assuming**, **no fake done** (no stubs/TODOs as done, never weaken a check),
  and **compact feedback** (pass = 1 line, fail = expected/actual/fix).
- **Gate-will-be-gamed defense** — holdouts, properties over self-written tests, spot-checks.

Profile/directive-triggered blocks add a **no-progress circuit breaker**, **cross-run
learnings** (`.loop/learnings.md`), **escalation handoff** for unattended runs,
**scheduled-loop safety** (idempotency, one confirmed scheduler, tiered auto-approve, intent
deny-list), a **JSON done-ledger**, and **LLM-as-judge hardening**.

The technique catalog, the self-improvement run history, and the deferred fleet-mode roadmap live in
[`loop-engineering-notes.md`](loop-engineering-notes.md).

## Codex packaging

Codex uses a skill/plugin surface, not a custom prompt command as the primary interface:

```
plugins/makeloop/.codex-plugin/plugin.json
plugins/makeloop/skills/makeloop/SKILL.md
.agents/plugins/marketplace.json
```

The Codex skill reads the shared canonical generator and template, then adapts only the host
launch surface: no fake `/loop`, no `/ralph-loop`, and no hidden runner. The final package ends with
copyable launch blocks backed by `.loop/<slug>.md` plus state/cursor; none appear during progress.
When the loop needs a closer Codex analogue to CC's runtime choices, the skill also offers Codex
run options: `/goal` for closed continuation, thread/standalone Automations for cadence and
watchers, and `codex exec resume` for external orchestration. It describes these modes but does not
create unattended schedulers unless the user explicitly asks.

## Handoff summary (Claude Code and Codex)

Leave work running and return to a readable account of its results or why it stopped, whether
that happens during the day or at night. "Morning handoff" was the former name, not a clock-based
mode. No hour, dawn deadline or minimum duration is implied; long duration alone is not the trigger.

For unattended **closed** runs, or an explicit request to leave a human-readable result, makeloop
adds a compact receiving summary to the existing state and makes its saved/read-back proof part
of delivery. The final brief says exactly where to look. Ordinary interactive work, explicit
opt-outs and open watchers do not acquire this block; narrow refinements preserve unrelated choices.

The execution agent updates the summary with the current run, target and timestamp: **what changed,
what was verified (and not verified), what remains/why it stopped, and the next action**. It updates
alongside the ledger, not only at exit. Even an already-green/no-change run leaves an honest result.
Structured state keeps its schema; an incompatible destination is a storage gap, not a reason to
prepend Markdown to JSON or create another ledger.

A readable handoff is not project completion. Missing review, budget exhaustion, a pending pause
or failed summary storage remains explicit. Checkpoint handling cannot extend limits or resume
project work. A crash may leave only the last durable checkpoint, and real host stopping remains
separate. No automatic message, scheduler, commit, push or new state system is introduced.

## Why it's shaped this way (loop engineering)

The generated contract closes a feedback path: **requirement → hypothesis → action → evidence →
decision**. It maps every original criterion to valid observations, identifies useful progress,
and changes the next action when results disprove the current approach. Clearing a plan or a
review is followed by a check of the original goal and any remaining delivery requirements.

- **Progress** is an observed improvement or a useful eliminated cause. Repeating a test on an
  improved target is valid; changing command text while making no progress cannot evade the limit.
- **Verification** checks both the result and whether the intended source/suite was observed.
  Empty valid results may pass; missing coverage remains a gap. Required reviews bind to the target.
- **Recovery** reserves an attempt before work, keeps interrupted attempts counted, and reconciles
  results before new work. The current state summary stays compact with pointers to detailed logs.
- **Watcher feedback** distinguishes read frontier, occurrence identity, pending intent and
  confirmed effect. Uncertain notifications/actions are reconciled without blind resending.
- **Completion** requires current proof for the original goal. Budget/blocker checkpoints retain
  its unmet scope and are reported separately from task success and native runtime stopping.

See [feedback-design.md](references/feedback-design.md) for the generator's design questions and
short interruption/stall traces. The guide is loaded during generation; it is not pasted wholesale
into every emitted contract. Measured time/cost per accepted outcome guides efficiency; unmeasured
usage stays unknown, and gate duration is only one component of wall-clock time.

It will also tell you when a loop is the *wrong* tool — if there's no automated way to
reject bad output, a single good prompt usually beats a loop.
