---
description: "Analyze the current project in depth, pin down the work goal, and generate a ready-to-run /loop prompt set to reach it"
argument-hint: "[goal hint (optional)]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "Write", "Task"]
---

# /makeloop — build a loop prompt for this project

You are about to **build a `/loop` prompt**, not run one. Your single deliverable is a
complete, paste-ready loop prompt that drives this project toward a clearly defined goal.
Do **not** start doing the project work itself — your job ends when the loop prompt is
generated, shown, and saved. Write your output in the **user's working language** (the
language of this conversation), not English by default — see Step 5 "Output language".

The user's request, if any: **$ARGUMENTS**

This command is grounded in loop-engineering practice. Keep these principles in mind the
whole way through; they decide whether the loop you generate actually helps or just burns
tokens:

- **The five phases of a loop**: DISCOVER -> PLAN -> EXECUTE -> VERIFY -> ITERATE.
- **The three hearts of a real loop**:
  1. **Verify** — a *real* gate (a test/build/lint or an objective check), never the agent
     grading its own homework.
  2. **State** — a small record carried across iterations (done / failed / next) so the
     loop resumes instead of restarting and never repeats the same mistake.
  3. **Stop condition** — success OR a hard iteration cap, so a stuck loop can't run all
     night spending money (the "Ralph Wiggum loop": exits too early or spins forever).
- **The four conditions a loop must meet** to be worth building (vs. just one good prompt):
  the task repeats; bad output can be rejected automatically; the token budget can absorb
  retries; and "done" is objective, not a matter of taste. If these don't hold, say so.
- **maker != checker** — the model that wrote the change is too generous a grader; have the
  loop re-verify with fresh eyes (or a sub-agent) on risky changes.
- **The order that survives**: get ONE manual run reliable -> wrap it in a loop with a gate
  + stop condition -> only then schedule it.
- **The metric that matters**: cost per *accepted* change. Below ~50% accept rate, a loop
  costs more than it returns.
- **Re-anchor, don't drift**: a long run loses its "do not touch" boundaries as context
  grows (rules tend to evaporate by ~turn 47). Make the loop *re-read its contract* (goal +
  criteria + rules) every iteration, and prefer many short fresh-context iterations over one
  long one.
- **The gate will be gamed** (Goodhart): if fooling the check is easier than doing the work,
  a loop drifts toward fooling it (stubs, matching the test instead of the spec, weakening
  assertions). Defend with holdout/rotating cases, properties over self-written example
  tests, and the occasional spot-check of a passing change against the *true* goal.

**A generic command can only produce a good loop if it actually understands this project.**
The depth and sophistication of the loop you generate must match what the project supports —
a project with a self-driving test harness and regression baselines deserves a richer loop
(two-stage gate, harness-failure detection, a labeled stop taxonomy) than a project with a
single `npm test`. Read first, then generate to fit.

That includes the project's **maturity**. Don't assume — judge it from the files. A
greenfield/empty repo needs a loop that *first builds its own verification* (scaffold +
acceptance tests) before it can drive anything; a mature repo reuses the gate it already
has; an in-between repo (code but no gate) may need to establish one along the way. The same
`/makeloop` adapts across all of these — read where the project sits on that spectrum and
generate accordingly.

Work through the steps below in order.

---

## Step 0 — Parse the request (treat $ARGUMENTS as goal + directives)

The trailing text after `/makeloop` is free-form natural language. Read it and extract
**both** a goal hint **and** any operational directives the user already decided. Whatever
they specified, **honor it and skip the matching question later** — only ask about what is
still missing and material. If the request is empty, run the full interactive flow.

**Refine an existing loop (fast path).** First check whether the request targets a loop that
already exists — `$ARGUMENTS` names or points at a `.loop/<slug>.md`, or says "tweak / adjust /
update the X loop". If so, this is a **refine**, not a fresh build: READ that loop file (plus its
state/cursor), apply ONLY the single requested delta (change the cap, swap the runtime, add or
remove one OPTIONAL block, tighten a criterion), and re-save under the **same slug** — preserve
its state file, its kind, and every block you weren't asked to change. Skip DISCOVER and the
interactive questions, run the Step 6 pre-save self-check, then output. If the named loop doesn't
exist, fall through to a normal build.

Extract whatever is present (natural phrasing, not strict flags — interpret intent):

| Directive | Example phrasings | Effect |
| --- | --- | --- |
| **Goal / scope** | "finish the auth refactor", "全テストを緑に", "complete the project" | Goal hint + scope; skip the scope/goal question if unambiguous (still confirm criteria). |
| **Runtime** | "self-paced", "interval 30m" / "30分ごと", "ralph-loop" | Sets the runtime; skip Step 4. |
| **Loop kind** | open: "watch/monitor X", "notify me when", "poll", "alert on", "監視/通知/見張る"; closed: "finish", "complete", "get green", "fix all", "完成/緑に" | Sets KIND. If unspecified, classify in Step 1. On ambiguity default to **closed**. |
| **Iteration cap / budget** | "cap 20", "上限20", "max 20 iterations", "wall-clock 30min", "no-progress 3" | Sets N / wall-clock / no-progress; don't ask. |
| **Success K** | "K=3 consecutive clean", "3連続で新問題ゼロ" | Sets the success streak. |
| **Verify gate** | "gate: npm test && tsc", "verify with cargo test" | Use as the gate verbatim. |
| **Blocks on/off** | "two-stage gate", "harness検知あり/なし", "no budget block", "with regression guard" | Force-include or exclude that optional block, overriding the profile default. |
| **Interaction level** | "質問は最小", "don't ask", "just generate", "auto" | Minimize questions: make sensible assumptions, note them, and ask ONLY if a choice is both ambiguous and high-impact. |

State back to the user a one-line summary of what you parsed, **leading with the loop kind**
(e.g. *"Parsed: kind=closed, goal=QA green, runtime=ralph-loop, cap=20"* or *"Parsed:
kind=open, watch=deploy status, runtime=/loop 5m, run=indefinitely"*) so they can correct it
before you proceed. Anything not specified falls through to its normal step below.

## Step 1 — DISCOVER: build a Project Profile (read-only, go deep)

**Session context first (if any).** You are running inside a live session — read the
conversation so far as a *primary* signal for what the user is actually working on: the goal
they've been pursuing, what they just asked for, decisions already made, errors they hit,
files they touched. This often reveals the in-flight goal better than git does. Reconcile it
with the project state below — the **conversation tells you the intent, git/files tell you the
reality**; when they disagree, surface it. If there's no relevant history (fresh session, or
it was compacted away), say so and fall back to the project state.

Then investigate the working directory thoroughly and fill in the **Project Profile** below.
Use read-only commands only. For a large or unfamiliar codebase, dispatch an `Explore`
subagent (or 2-3 in parallel) to fill sections B–E faster, then confirm key findings yourself
by reading one primary source each (don't take the summary on faith).

**A. Orientation**
- Git: `git status -s`, `git log --oneline -20`, `git diff --stat`, `git diff --stat HEAD`
  (in-flight + recent work). Note if not a repo.
- Project type, entry points, build & run commands (README, `package.json`,
  `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Package.swift`, etc.).

**B. Verification depth — this shapes the gate**
- Tests (unit/integration), typecheck, lint, build.
- Deeper checks: grep for `baseline`, `golden`, `snapshot`, `regression`, `parity`,
  `--audit`, `invariant`, `--drive-all`, e2e suites.
- Decide: is verification **single-stage** (one test command) or **multi-stage**
  (e.g. build -> drive -> audit/regression)? Record the exact commands and pass conditions.
- **If the loop is open (a watcher)**, reframe B: instead of "what gate exists", find **what
  SIGNAL can be observed and what predicate fires on it** (a log pattern, a status field, a
  queue/inbox, a PR/CI event) — and whether that signal covers **every terminal/failure state
  incl crash/hang/OOM** (the silent-harness check in C generalizes to dead-watcher coverage).

**C. Self-driving harness — this decides harness-failure handling**
- Look for drivers: Playwright, Cypress, Selenium, XCUITest, simulators (`xcrun simctl`),
  `scripts/*drive*`, `screencapture`, headless runners, `--drive`-style flags.
- Does the project emit observable artifacts (screenshots, state snapshots, logs) the loop
  must validate?
- Can the harness fail *silently* (blank capture, empty snapshot, frozen sim)? If so the
  loop needs an **observation-validity check** before trusting any result.

**D. Invariants, oracles & boundaries — feeds SUCCESS CRITERIA + RULES**
- Grep README/docs/test names for: `invariant`, `must not`, `read-only`, `parity`,
  `contract`, `do not modify`, `layout`, `idempotent`.
- Which properties must **never** break? What is off-limits to edit (vendored code, a
  read-only integration, UI layout, generated files)?

**E. Existing loop infrastructure — reuse, don't reinvent**
- Look for `.loop/`, `.loop-state.json`, `*state*.json`, `*FINDINGS*.md`, `*runbook*.md`,
  `scenarios/`, regression case dirs.
- If present, read them and **extend** the existing loop (reuse its state files, runbook,
  scenario format) rather than starting fresh.
- **List existing loops**: glob `.loop/*.md` (and read `.loop/INDEX.md` if present). If any loop
  files exist, show a one-line summary per loop (slug / goal / kind / launch line) so the user
  can choose **refresh/extend an existing loop** (→ the refine path in Step 0) vs **start a new
  one** before you spend turns profiling.

**F. Operational facts**
- Commit convention (conventional commits in the log? commitlint/husky? signing policy?
  files that must never be staged, e.g. `outputs/`, `dist/`, build artifacts).
- Run cost/time (heavy build? long CI?) -> informs the budget.
- Crash/flake surfaces.

Then **summarize the profile** for the user and state explicitly:
- **What the session shows you're working on** (if any) — the in-flight goal from the
  conversation, and whether it matches the git diff.
- **Loop kind** — **closed** (drive-to-done) or **open** (watch/react). Classify from two
  signals: (1) the goal's verb/tense — terminus verbs → closed ("finish/complete/get green/
  fix all/完成/緑に"), continuous/recurring → open ("watch/monitor/notify me when/poll/alert
  on/triage incoming/監視/通知/見張る"); (2) the **decisive test** (also your confirm line to
  the user): *"Can you write a SUCCESS CRITERION that becomes permanently true and ENDS the
  loop? Yes → closed. If the only 'criterion' is a condition you REACT to that RECURS →
  open."* On silence/conflict, **default to closed** (capped, stops) and state the assumption
  — misclassifying closed→open runs forever, the costlier error.
- **Maturity** (judge from the files, not a flag): where does it sit on the spectrum —
  *greenfield* (empty / only bootstrap files / no manifest / little-to-no git history) →
  *scaffolded but no gate* (code exists, but no tests/lint/build) → *mature* (a real gate
  already exists)?
- Is there a real automated gate? Single- or multi-stage?
- Is there a self-driving harness that can fail silently?
- Any existing loop infra to extend?
- Any hard invariants / off-limits boundaries?

Read the **"no automated check"** finding *through kind first, then maturity*:
- **kind=open (a watcher)** → "no completion gate" is **correct, not a defect**. Do NOT run
  the four-conditions "done is objective" test or the Ralph-Wiggum warning — they are
  closed-loop axioms. An open loop's failure modes are *missed events (coverage gap), alert
  fatigue (no dedup), non-idempotent double-acting, silent death* — never "fails to
  terminate". The two branches below apply only when **kind=closed**.
- **Mature repo, still no gate** → a loop is likely the wrong tool; say so plainly (a single
  good prompt usually wins).
- **Greenfield / early** → "no gate" is expected, nothing's built yet. Do NOT call the loop a
  bad fit. The loop's *first job is to create its gate* (scaffold + a first failing acceptance
  test); see Step 3's bootstrap guidance and the Bootstrap block in Step 5.

## Step 2 — Goal: propose candidates, confirm scope (AskUserQuestion)

**Default interaction — propose the whole loop, confirm once.** Steps 2-4 are written as
separate question rounds, but by default do NOT ask them one at a time. After DISCOVER, assemble
a single consolidated proposal from the profile — **kind + goal + SUCCESS CRITERIA (or the
watcher's TRIGGER) + gate + iteration cap + runtime** — and ask ONE `AskUserQuestion` to *confirm
or edit* the whole thing. Branch into the granular per-step questions below ONLY for a choice
that is both genuinely ambiguous AND high-impact (closed-vs-open is unclear; a destructive gate
needs sign-off; success is a judgment call) — those still get their own dedicated question. This
collapses a routine loop from ~4 round-trips to 1 while keeping the sharp questions for the cases
that actually need them. (Honor Step 0: anything already specified is pre-filled and not
re-asked; if interaction level is minimal, state the assumptions and skip the confirm entirely.)

From the profile (and `$ARGUMENTS` if given), derive **2-3 concrete goal candidates**. For
the **"finish the in-flight work"** scope, lead with the *session-derived* goal — what the
conversation shows you've been doing — confirmed against the git diff; that's usually the
sharpest candidate.

**Bias candidates toward loop-appropriate work** — repetitive and machine-checkable: CI /
test-failure triage, dependency bumps, lint-and-fix passes, flaky-test reproduction, getting
a suite green, issue-to-PR on well-tested code. **Steer away from loop-hostile goals** where
"done" is a judgment call — architecture rewrites, auth/payments, production deploys, vague
product work. If the user's goal is one of those, say so plainly and recommend a single
guided prompt with a human in the chair instead of a loop.

Then ask the user with `AskUserQuestion`. Ask **scope** first — it changes everything:

- **A) Finish the in-flight work** — wrap up what's being worked on now / the dirty tree.
- **B) Reach the nearest milestone** — the next coherent checkpoint.
- **C) Complete the project to the end** — drive all the way to the finish line.

Fold your candidates into the options; if `$ARGUMENTS` carried a hint, make it the top
candidate. Then **draft strict SUCCESS CRITERIA** (3-5 bullets, each objectively
checkable — pull invariants from profile D where relevant) and confirm them with the user.

**Greenfield / early projects**: there's nothing in the code to infer a goal from, so treat
the goal as a *spec* and gather it from the user — what to build, the stack/language, and the
acceptance criteria that will *become the gate*. Read a `SPEC.md` / README intent if one
exists. Here the SUCCESS CRITERIA are the user's acceptance criteria, not something derived.

**Open (watcher) goals**: the above (scope A/B/C, SUCCESS CRITERIA) is the **closed** path.
If kind=open, don't ask for success criteria — instead confirm: **WATCH TARGET** (the signal
observed), **TRIGGER CONDITION** (the recurring predicate to react to), **REACTION**
(notify-only vs act), and **RUN MODE** (run-indefinitely vs stop-on-first-event). When a
surface goal is genuinely ambiguous ("handle CI failures" = drive *this* suite green [closed]
vs watch for *new* failures and triage [open]), present **both** framings and disambiguate
with the decisive test. Goal-fit for watchers: monitoring a discrete observable signal is
loop-appropriate; "watch and use judgment on vague output" is loop-hostile (alert fatigue, no
objective predicate) — recommend a human in the chair instead.

*Skip the scope question* if Step 0 already resolved scope/goal unambiguously; still show the
drafted SUCCESS CRITERIA for a quick confirm (unless interaction level is minimal, in which
case state your assumptions and proceed).

## Step 3 — Gate + stop condition, sized to the project (AskUserQuestion / propose)

- **VERIFY gate**: build it from profile B. Always order checks **fastest -> slowest**
  (typecheck/lint before unit before integration before e2e) and stop at the first red — the
  cheapest check that can fail the work runs first. This "backpressure ladder" is the main
  lever on cost per accepted change.
  - Single-stage -> one gate command + pass condition.
  - Multi-stage -> a **two-stage gate**: a *pre-gate* (e.g. `build` + a full check) run at
    the start of each iteration, and a *post-gate* (re-run the full check) after the fix.
    A red pre-gate means the baseline is already broken (HALT); a post-gate that drops a
    previously-passing check means the fix caused a regression (FREEZE, do not commit).
  - When example tests are the only oracle, prefer a **property / metamorphic check** where
    possible (an invariant true for all inputs, or a relation like "reordering inputs must
    not change the result") — a self-written example test shares the code's blind spots.
  - For **UI / web** work, add a "drive-and-capture" check: actually exercise the feature and
    capture an artifact (screenshot / GIF) as proof-of-use — synthetic interaction catches
    wiring/state bugs that unit tests miss, and the artifact doubles as evidence on the PR.
  - **Greenfield / early (no gate yet, but the goal is to build it):** don't refuse — make
    the loop *bootstrap its own gate*. Iteration 0 scaffolds the project (repo, package
    manager, the stack's test runner) and encodes the acceptance criteria as FAILING tests
    (confirm red); from then on that test command is the gate and the loop drives red → green.
    Add the **Bootstrap block** in Step 5.
- If **no automated check exists in a mature project**, warn clearly, help define an objective
  manual check, and ask whether to proceed anyway. If the gate must be an **LLM-as-judge**, harden it: use a
  *different model family* than the maker (self-enhancement bias makes a same-model judge
  wave through its own slop), a coarse pass/fail rubric (not a fine 1-10 scale), and escalate
  low-confidence verdicts to a human instead of guessing. Better still, pair the judge with a
  **deterministic assertion** (value-in-range / file-exists / schema-valid) as an AND-gate —
  mark done only if BOTH pass, and feed the failing check's message into the retry. Ground the
  rubric in the repo (let the judge read the code/conventions before scoring, not just the
  spec) and give it an explicit **anti-cheating axis** (flag test-weakening, mass-renames,
  dependency churn) and a **blast-radius axis** (penalize edits far wider than the goal).
- **STOP taxonomy**: at minimum success + a hard iteration cap **N** (default **8**). Add
  labeled stop reasons per the profile (see the mapping in Step 5). Confirm N and the
  **budget** (iteration cap / wall-clock / no-progress streak).
  - Size N from *diminishing returns*: most reachable gain lands in rounds 1-2 (≈50% then
    ≈25%), so ~5-6 is often right; past the ceiling the loop re-touches validated code and
    regresses (oscillation). When quality plateaus, add MORE distinct verifier *types*
    (tests + lint + self-review + property) — "wide, not deep" — not more iterations of one.

**If kind=open, this whole section changes** (everything above is the closed path):
- Replace the VERIFY gate with a **TRIGGER CONDITION** — an objective predicate over the
  *observed signal* (not a pass/fail on made work). Precision matters: a false fire trains the
  user to ignore alerts.
- Replace the STOP taxonomy with a **RUN MODE**: *run-indefinitely* (steady-state watcher) or
  *stop-on-event* (fire once, then exit). No success-or-cap.
- Confirm the **dedup policy** (edge-trigger / cooldown window) and, if the watcher **acts**,
  an **idempotency key** so re-firing on the same event can't double-act.
- The metric is **coverage + precision** (did it catch real events without crying wolf), not
  cost per accepted change.

*Honor Step 0*: if the request already gave a gate, cap, budget, success K, or forced a
block on/off, use those values and don't re-ask. Block on/off directives from Step 0
override the profile defaults in Step 5.

## Step 4 — Choose the loop runtime (AskUserQuestion)

- **Built-in `/loop` self-paced** — omit the interval; iterate until done. Best for
  goal-completion. (Recommended default.)
- **Built-in `/loop <interval>`** — e.g. `/loop 30m ...`; cadence-based. Ask for interval.
- **ralph-loop plugin `/ralph-loop`** — built-in stop machinery (`--max-iterations N`,
  `--completion-promise '<TAG>'`).

*Skip this question* if Step 0 already named the runtime (and interval, if given).

**Independent completion check** (the `/goal` pattern, **closed loops only**): "the gate
passes" is objective and self-grading is fine for it. But "the *goal* is met" should not be
decided by the maker when it can't be fully reduced to the gate — have a separate checker (a
sub-agent, ideally a different model, seeing the spec + diff but not the maker's reasoning)
confirm completion before the loop prints its completion token.

Completion token (closed only): `FINAL` for built-in `/loop`; `<promise>DONE</promise>` for
ralph-loop.

**If kind=open**: use `/loop <interval>` (cadence polling) or self-paced. **Drop the
completion token and the `/goal` check** — a watcher has no completion. The only token an open
loop may print is a `TRIGGERED` sentinel in *stop-on-event* mode. One hint for the loop body
(not a launch line makeloop can emit): for live-stream watching use the **Monitor** tool; for
wall-clock schedules use a **cron routine** — both are in-loop tool calls.

## Step 5 — ASSEMBLE: fill the template, include blocks the profile triggers

Pick the **CORE template that matches the loop kind** — **CLOSED CORE** (drive-to-done) or
**OPEN CORE** (watch/react) — then add each OPTIONAL block whose trigger fired in DISCOVER
(respect the kind-applicability column). Drop blocks that don't apply — don't ship a two-stage
gate for a project with one `npm test`. Replace every `<...>` placeholder.

**Output language**: render the generated loop prompt — and your chat-facing summaries — in
the **user's working language** (the language of this conversation / their request). Default
to *their* language, never default to English. Keep machine-significant literals unchanged:
shell / gate commands, file paths, JSON keys, the completion token (`FINAL` or
`<promise>DONE</promise>`), and `ITERATING`. The structural keywords and `stop_reason`
identifiers below may stay as stable labels, but translate every heading description,
instruction, and line of prose. The English template below is a scaffold to render in the
user's language, not text to copy verbatim.

**Profile signal -> block to include:**

| Profile signal (from Step 1) | Add this block |
| --- | --- |
| Multi-stage verify (build + audit/regression) | **Two-stage gate** (pre-gate / post-gate, FREEZE-no-commit on regression); stop reasons `poisoned-baseline`, `regression` |
| Self-driving harness emitting artifacts | **Observation-validity check**; stop reasons `unrecoverable-harness`, and `pinata` (crash) |
| Baseline / golden / `scenarios/` present | **Regression-guard step**: add one minimal regression case per fix, tied to root cause |
| Any autonomous (self-paced) loop | **Budget block** + stop reasons `no-progress`, `oscillation`, `failure`; **No-progress circuit breaker** |
| Hard invariants / off-limits boundaries (profile D) | Encode them in SUCCESS CRITERIA + RULES; stop reason `scope-boundary` |
| Existing loop infra (profile E) | Point STATE at the existing files + runbook; reuse scenario format |
| Repeats weekly / will run again (profile = recurring) | **Cross-run learnings** file so the loop gets smarter each run |
| Unattended / scheduled / overnight run | **Escalation handoff** + **Scheduled-loop safety** (idempotency, external scheduler, tiered auto-approve, intent deny-list, token/cost cap) |
| Many discrete pass/fail criteria | **JSON done-ledger** instead of a markdown checklist |
| Greenfield / early project (no gate yet) | **Bootstrap block** — iteration 0 scaffolds + writes the first failing acceptance tests, then the loop drives red → green |
| Open loop that ACTS (not notify-only) | **Scheduled-loop safety** (idempotency / deny-list / auto-approve) — an acting watcher is an unreviewed attack surface |
| Open loop, run-indefinitely | **Dedup/cursor block** + wire **Escalation handoff** on (a dying watcher must hand off, not vanish) |

**Kind applicability** (which blocks belong to which CORE):

| Block | CLOSED | OPEN |
| --- | --- | --- |
| Two-stage gate · Regression-guard · No-progress circuit breaker · JSON done-ledger · Bootstrap · Independent completion check | ✅ | ❌ (Bootstrap is **suppressed** when kind=open) |
| Budget · Cross-run learnings · Escalation handoff · Scheduled-loop safety | ✅ | ✅ |
| Observation-validity check | ✅ | ↳ folded into OPEN core's Liveness/Coverage |
| **Dedup/cursor** | ❌ | ✅ (open-only) |

### CLOSED CORE template (drive-to-done; use when kind=closed)

```
# LOOP: <short goal name>

GOAL: <one sentence, objective, checkable>. <runbook path if one exists>

SUCCESS CRITERIA (strict, no soft passes):
- <verifiable criterion 1>
- <criterion 2>
- <criterion 3 — include any hard invariant from profile D>

VERIFY — the gate (run these; never self-grade):
- <verify command 1, e.g. npm run typecheck>   # fastest first
- <verify command 2, e.g. npm test>            # slower last
PASS = <exact pass condition, e.g. all tests green, 0 type errors, exit 0>
- Run the gate fastest -> slowest and STOP at the first red (don't run the slow suite when
  typecheck is already failing).

STATE FILE: .loop/state.md   (or existing state file from profile E)
- Read it before starting. This is a resume, not a restart.
- Each iteration, append: what you did / what passed or failed / the single next step.

EACH ITERATION:
1. RE-READ the loop contract (GOAL + SUCCESS CRITERIA + RULES) AND state, then run VERIFY to
   see the current failures.
2. PLAN the single highest-impact next step (just one).
3. EXECUTE the smallest change that advances that step.
4. VERIFY by running the gate; record the result in state.
5. DECIDE: are ALL success criteria met?
   - Yes -> print "<completion token>" and stop.
   - No  -> print "ITERATING" and continue, fixing the weakest criterion first.

STOP WHEN: VERIFY passes every criterion, OR <N> iterations are reached.
ON STOP: summarize what changed, what still fails, and roughly the accept rate.

RULES:
- Never call it done until the gate actually passes. No self-grading.
- First VERIFY counts — don't fabricate work to justify the loop: if VERIFY already passes every
  SUCCESS CRITERION before you make any change, that is a real success — report FINAL honestly
  ("already satisfied; no loop work was needed") and do not invent or imply a change that never
  happened.
- maker != checker: on risky changes, re-verify with fresh eyes / a sub-agent.
- Surgical changes only: every diff line must trace back to GOAL. <off-limits from profile D>
- Search before assuming: grep the codebase before claiming a thing is missing or
  reimplementing it — "it's not there" is only true after you've looked.
- No fake done: no placeholders, stubs, or TODOs reported as complete; never delete, skip,
  or weaken a check to make the gate go green.
- Report compactly: a PASS is one line; a FAIL gives {expected / actual / what to fix}.
  Don't re-print an unchanged prior failure — it just poisons the context.
- Re-verify the diff, not the world: iteration 1 checks everything; later iterations re-check
  only the just-changed surface, not the whole output.
- Retry by failure class: rate-limit -> back off; validation fail -> rewrite from the
  feedback (no blind retry); transient 5xx -> retry once or twice then move on; tool
  unavailable -> pause and surface it (don't burn retries).
- Empty is not failure: a check that runs cleanly and returns nothing to act on (no matching
  lines, an empty diff, a no-op build) has genuinely passed — record that empty result as a
  real PASS and move on, don't read silence as "try harder". Only a true error or a failed
  assertion re-enters the retry ladder above.
- Shrink the unit on repeat failure: if the same subtask fails twice, don't retry it as-is
  and don't give up — re-scope to the smallest failing fragment (one function / line / test)
  and attempt that; escalate only after the fragment also fails.
- Do not ask questions mid-loop. Make a sensible assumption, note it in state, continue.
```

### OPEN CORE template (watch/react; use when kind=open — no FINAL, runs on cadence or event)

```
# WATCH: <short watch name>

WATCH TARGET: <signal observed — deploy status / app.log / PR #123 comments / the queue>. <runbook if any>
INTENT: keep watching and react each time the trigger fires. This loop has NO "done" —
running until stopped is correct, not a defect.

TRIGGER CONDITION (objective predicate over the observed signal — REPLACES a success gate;
you read reality, not grade your own work):
- FIRE when: <predicate, e.g. a line matching /ERROR|FATAL/ appears; status == "failed"; a new
  unread item; a new comment by someone other than me>
- A recurring condition to REACT to, not a criterion that becomes permanently true. Precision
  matters: a false fire trains the user to ignore alerts.

CURSOR FILE: .loop/cursor.json   (last-seen marker, NOT a done/failed/next ledger)
- Read before each tick. Holds last-seen <id|timestamp|status> + a digest of the last fire
  (for dedup). This is how you compute "what is NEW since the last tick".
- COLD START (first run): seed the cursor to the signal's CURRENT end/latest marker, so
  pre-existing items count as already-seen and you fire only on what arrives AFTER launch (no
  day-zero backlog false alarm). Replay existing backlog ONLY if the request explicitly asks
  ("process existing errors / replay backlog / backfill"): one bounded, deduped pass, then advance.

EACH TICK (one interval, or one event):
1. OBSERVE: read the current signal; load the cursor.
2. EVALUATE: is the trigger true for something NEW (beyond the cursor)?
   - No  -> do nothing; advance the cursor if needed; wait for the next tick. (Silence is normal.)
   - Yes -> go to 3.
3. DEDUP: already fired (cursor digest / cooldown window)? If yes -> skip. Edge-trigger, not
   level-trigger: do not re-fire while the same condition stays true.
4. REACT (idempotent):
   - NOTIFY: ONE message to <channel: PushNotification / .loop/alerts.md / a GitHub issue /
     chat> with {what fired, the evidence, where, timestamp}.
   - ACT (only if this watcher acts, e.g. auto-restart / file a ticket): stamp with an
     idempotency key = <stable key over the event id> so re-firing cannot duplicate the effect.
5. ADVANCE the cursor (last-seen marker + this fire's digest) and continue.

RUN MODE: <run-indefinitely>   # steady-state watcher; never prints a completion token
  # OR <stop-on-event>: the first time the trigger fires, NOTIFY then print "TRIGGERED" and exit.
There is NO FINAL and NO "all criteria met -> stop" — those are closed-loop notions.

RUNTIME: /loop <interval> for cadence polling. For live-stream watching use the Monitor tool;
for wall-clock schedules use a cron routine — those are in-loop tool calls, not launch lines.

LIVENESS / COVERAGE (a dead watcher looks identical to "all quiet"):
- The trigger must cover EVERY terminal/failure state incl crash / hang / OOM. Ask: "if the
  thing I watch died right now, would this loop emit anything?" If not, widen the predicate.
- Emit a slow heartbeat ("still watching, last tick OK at <time>") so alive vs dead is visible.

STOP WHEN (a watcher's stops — NOT success-or-cap):
- never              : run-indefinitely; stops only when user / scheduler stops it.
- event-fired        : stop-on-event mode handled the fire.            [stop-on-event only]
- watch-target-gone  : the thing watched no longer exists -> notify + exit.
- budget             : optional token/cost/wall-clock cap -> notify + exit (not a goal stop).

RULES:
- React to reality, don't grade your own work — correctness = coverage + precision.
- maker != checker: re-verify with fresh eyes / a sub-agent rather than trusting your own read —
  and if the watcher ACTS, verify the action before its side effect (don't let the actor wave
  through its own act).
- Surgical changes only: react only to what the trigger matched; don't "fix things while
  you're here".
- Search before assuming: confirm the signal is real (read/grep the source) before firing —
  "nothing happened" is only true after you've looked.
- No fake done: never fabricate or suppress an observation to stay quiet, and never weaken the
  trigger to silence it — a fire must reflect a real event.
- Edge-trigger, not level-trigger: one notification per NEW occurrence; suppress until the
  state CHANGES or the cooldown elapses.
- Idempotent actions: any side effect must be safe to re-run on the same event (no double
  file / restart / post).
- Report compactly: a fire is one line {trigger, evidence, where, when}; silence prints nothing.
- Do not ask questions mid-loop. Make a sensible assumption, note it in the cursor, continue.
```

### OPTIONAL blocks (include per the table above)

**Two-stage gate** (closed only) — replace the CLOSED CORE `VERIFY` block and fold these into EACH ITERATION:
```
VERIFY — two-stage gate (never self-grade):
- pre-gate  (start of iteration): <build> && <full check>
- post-gate (after the fix):      <full check>
PASS = <full check green + baseline/regression audit shows 0 regression>
- pre-gate RED  -> HALT  (stop_reason=poisoned-baseline)
- post-gate drops a previously-passing check -> FREEZE, do NOT commit (stop_reason=regression)
```

**Observation-validity check** — insert into EACH ITERATION right after driving the harness:
```
- After driving the harness, validate the observation BEFORE trusting it:
  blank/baseline-identical screenshot, empty snapshot, or frozen run
  -> HALT (stop_reason=unrecoverable-harness). A crash -> HALT (stop_reason=pinata).
```

**Regression-guard step** — insert into EACH ITERATION after the fix, before the post-gate:
```
- Add ONE minimal regression case (<scenarios path>/<name>) that asserts the violated
  invariant, tied to the root-cause fix. One fix + one guard per commit.
```

**Budget block** — add under STATE FILE:
```
BUDGET (write into state): iteration cap <N> / wall-clock <T> / no-progress streak <P> /
token+cost cap <C> (soft-pause + notify at 85%, hard stop at 100%).
```

**No-progress circuit breaker** — add to EACH ITERATION (mechanistic, complements the
no-progress stop reason):
```
- Hash {tool name + args} for each action this iteration and keep a short window. The same
  action repeated (3rd identical call, or >85% similar plan/action across iterations) means
  stuck -> stop_reason=no-progress. Don't keep paying for a spin.
```

**Cross-run learnings** — for loops that will run again; add a learnings file + steps:
```
LEARNINGS FILE: .loop/learnings.md  (re-read at the START of every run, before the contract)
  Two sections: ## DURABLE (corroborated rules the loop obeys) and ## UNVERIFIED (candidate
  lessons — read for context, NOT obeyed as rules yet). Default a new lesson to UNVERIFIED.
- On any recurring failure, write the lesson to UNVERIFIED first, tagged with an occurrence
  count + an evidence pointer (the run / iteration that showed it).
- Promote UNVERIFIED -> DURABLE only when a SECOND occurrence (or an independent fresh-context
  pass) confirms it — one atypical run may never mint a DURABLE rule it then obeys forever.
- A learning may never rewrite a SUCCESS CRITERION, a gate, or a stop condition: those change
  only by human edit, never from the loop's own notes.
- Prefer category-level prevention over a single regression case: a DURABLE rule that kills the
  whole class of bug, folded into lint/AGENTS.md where it can be enforced.
```

**Escalation handoff** — for unattended/scheduled runs; replaces silent death on a dead-end:
```
ON DEAD-END (failure / budget / unrecoverable-harness): do NOT die silently. Write a
context-rich handoff (what was tried, last error, where it stopped, run_id) to <inbox:
a file / GitHub issue / channel>. A run that found nothing actionable archives itself
quietly. Treat "escalate to human with full context" as a success path, not a failure.
```

**Scheduled-loop safety** — for cron / interval / overnight runs:
```
- Idempotency: stamp each side-effecting apply with an idempotency key; on resume, a node
  re-runs from its start, so duplicate effects must be impossible.
- Bind the placeholders — don't ship the boilerplate raw: replace the idempotency key and the
  allowed-action set with the project's REAL values (the stable event-id field; the ONE action
  this watcher may take). An unbound deny-list lists generic verbs but carries no
  project-specific authority check, so it blocks nothing concrete.
- Durable schedule: drive recurring runs from an EXTERNAL scheduler (OS cron / CI / Actions
  with a per-loop concurrency group, cancel-in-progress=false) — in-process timers die on
  restart and don't auto-recover.
- Auto-approve boundary (tiered): safe reads/search auto-run; in-repo file writes auto-run
  (reviewable via git); shell / external calls / out-of-repo writes / subagent spawns are
  gated. Default trust boundary = this git repo only.
- Intent deny-list (judge real impact, not surface text): never force-push, mass-delete,
  exfiltrate secrets, disable logging, install keys/cronjobs, push to main, or deploy to
  prod without explicit human sign-off. Anything the loop chose on its own is unauthorized.
- Security tax (unattended = an unreviewed attack surface): put security checks IN the gate
  (secret scan, dependency audit, SAST) so insecure code can't auto-merge; require a human
  approval gate before anything irreversible (merge to main, deploy, dependency changes).
- Hygiene: don't log credentials (sanitize loop logs); audit any skill/connector source
  before the loop uses it (prompt-injection vector); re-audit the loop's permissions on a
  cadence rather than letting scope creep accumulate.
```

**JSON done-ledger** — replace the markdown success checklist when criteria are many/discrete:
```
DONE LEDGER: .loop/done.json  = [{ "criterion": "...", "status": "pass|fail",
"verified_by": "<gate output / command>" }]
- Status may only go to "pass" with a real verified_by. The loop is done only when every
  status is "pass".
```

**Dedup/cursor block** (OPEN only) — the watcher's failure-mode defense; fold into the OPEN core:
```
- Edge-trigger suppression: keep a digest of the last fire in .loop/cursor.json; the same
  condition staying true must NOT re-fire — only a NEW occurrence (or after the cooldown) fires.
- Last-seen cursor: persist last id/timestamp/status so each tick computes "what is new".
- Idempotency key (if the watcher acts): a stable key over the event id; re-handling the same
  event must be a no-op (no double ticket / restart / post).
```

**Bootstrap block** — for greenfield/early projects (**closed only — suppressed when
kind=open**: a watcher has no acceptance tests to fail); prepend as ITERATION 0 (runs once):
```
ITERATION 0 — bootstrap the gate (run once, before the normal loop):
- Scaffold the project: init the repo, the package manager / project file, and the stack's
  standard test runner. Keep it minimal — only what the SUCCESS CRITERIA require.
- Encode each SUCCESS CRITERION as a FAILING acceptance test; run them and confirm RED
  (a gate that can't fail yet is not a gate).
- Commit the scaffold + red tests. From here, <test command> is the VERIFY gate and the
  normal loop drives red -> green.
```

**Extended STOP taxonomy** (closed only) — replace the CLOSED CORE `STOP WHEN` line; label every halt:
```
STOP WHEN (label each halt with stop_reason in the log):
- success              : <K consecutive clean iterations, e.g. K=3>
- no-progress          : <P> iterations new-nothing, or repeated tool-call/plan (circuit breaker)
- oscillation          : same problem-fix pair repeated 3x
- failure              : one problem fails to fix after 3 tries
- budget               : iteration / wall-clock / token+cost cap reached
- escalate             : dead-end handed off to a human with full context  [unattended only]
- regression           : post-gate dropped a previously-passing check   [two-stage only]
- poisoned-baseline    : pre-gate already red                            [two-stage only]
- unrecoverable-harness: blank/empty/frozen observation                  [harness only]
- pinata               : crash                                           [harness only]
- scope-boundary       : would touch an off-limits area / exceeds turn cap [invariants only]
```

`<completion token>` = `FINAL` for built-in `/loop`, or `<promise>DONE</promise>` for
ralph-loop. Use the exact `<N>`/`<K>`/`<P>`/`<T>` the user confirmed.

## Step 6 — OUTPUT (show + save)

### Pre-save self-check (run this before saving)

Before writing the files, run two read-only checks on what you assembled — both catch defects
that otherwise surface only *after* the user launches and burns tokens.

**Assembly lint** (always; a read-only pass over the assembled text):
- No leftover raw `<...>` placeholder survives anywhere — every one was filled with a real value.
- Exactly ONE CORE is present (CLOSED *or* OPEN, never both), and no closed-only block leaked
  into an open loop or vice versa (cross-check the Kind-applicability table).
- Kind-consistent: a **closed** loop has STATE + SUCCESS CRITERIA + a real VERIFY + a completion
  token; an **open** loop has WATCH TARGET + TRIGGER + cursor + RUN MODE and no completion token.
- The launch line points at the saved `.loop/<slug>.md`, and the state/cursor filename matches
  the kind (`-state.md` for closed, `.cursor.json` for open).
- Any block Step 0 forced on/off was honored.
Print a short PASS / gap list. On a gap, fix it and re-lint — do not save a loop carrying an
unbound placeholder or a leaked cross-kind block.

**Gate smoke-test** (closed loops with a deterministic gate command only):
- Behind a quick confirm, run the derived gate command ONCE to confirm it actually resolves
  (catches `npm test` vs `npm run test`, a missing binary) and report whether the baseline is
  already green or RED (a RED baseline is a `poisoned-baseline` worth knowing before looping).
  This is advisory only and never blocks the save; do not run it for open watchers or for any
  destructive / network / heavy gate.

0. Make sure the assembled prompt + state file are written in the **user's working language**
   (see Step 5), with only machine-significant literals left as-is.
1. Create `.loop/` if it doesn't exist (or reuse the existing loop dir from profile E).
2. Save the assembled prompt to `.loop/<slug>.md` — a short descriptive slug from the goal
   (e.g. `.loop/sources-harvest.md`, `.loop/qa-green.md`). Default to `loop-prompt.md` only
   for a project's sole loop; **if a loop file already exists, use a distinct slug so you don't
   clobber it** (a repo can hold several loops). Then append one row to `.loop/INDEX.md` (create
   it if absent) — `slug | goal | kind | gate | cap | runtime | ready-to-paste launch line` — so
   the repo's loops stay listable and re-runnable at a glance (this is the registry Step 1 reads).
3. Seed the state file if absent. **Closed** → `.loop/<slug>-state.md` (or the project's
   existing state file):
   ```
   # Loop state — <short goal name>

   ## Budget
   iteration cap <N> / wall-clock <T> / no-progress <P>   (omit if no budget block)

   ## Done
   (nothing yet)

   ## Failed / blocked
   (nothing yet)

   ## Next step
   <first concrete step toward the goal>
   ```
   **Open** → seed `.loop/<slug>.cursor.json` instead (last-seen marker, not a progress ledger).
   On the FIRST run the loop resolves `last_seen` to the signal's current end/latest marker (cold
   start: pre-existing items are already-seen, no day-zero backlog fire), unless the request asked
   to replay existing backlog:
   ```
   { "last_seen": null, "last_fired_digest": null, "note": "<watch target>" }
   ```
4. **Lead with the ready-to-paste launch line** — this is what the user actually runs, so put
   it first, in the user's working language, in **file-reference form** (point `/loop` at the
   saved file so the loop re-reads its contract each iteration — far kinder than pasting the
   whole prompt). Name the state/cursor file too. Templates:
   - self-paced (closed): `/loop <saved file> の手順に従って <short goal> を回して。state は <state file>。`
     (English: `/loop follow <saved file> to <short goal>; state in <state file>.`)
   - interval / open: `/loop <interval> <saved file> ... (cursor は <cursor file>)`.
   - ralph-loop: `/ralph-loop <saved file> の手順に従って ... --max-iterations <N> --completion-promise '<promise>DONE</promise>'`.
   Then, **below the launch line**, print the full assembled prompt for transparency/editing.
5. Close with the order that works and the cost note, **matched to the kind**:
   - **closed**: *prove one manual run -> loop it -> schedule it*; watch **cost per accepted
     change** — if you're tossing more than half the output, fix the gate before running again.
   - **open**: *prove the trigger fires on one real event -> wrap it with dedup -> schedule/
     persist it*; watch **coverage + false-positive rate** — a watcher that cries wolf gets
     muted, and one that goes silent is worse than none.

Stop here. Do not begin executing the loop — generating the prompt is the whole job.
