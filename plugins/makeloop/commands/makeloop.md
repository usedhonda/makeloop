---
description: "Analyze the current project in depth, pin down the work goal, and generate purpose-led loop choices with copyable native launch instructions"
argument-hint: "[goal hint (optional)]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "Write", "Agent"]
---

# /makeloop — build a loop prompt for this project

You are about to **build a host-native loop contract**, not run one. Your single deliverable is a
file-backed loop contract with explained choices and complete, copyable launch instructions.
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
  grows. Make the loop consult its contract and ledger after continuation/compaction and before a new step;
  preserve the accepted scope rather than restarting discovery.
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
Use read-only commands only. Read only what changes the goal, gate or boundary decision. Use an `Explore`/`Agent`
subagent only when delegation is explicitly authorized and the tool is exposed; otherwise
collect evidence directly. Tool names and allowed-tools do not authorize delegation.

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
  one** before you spend turns profiling. If the new goal substantially matches an existing loop
  (same target + kind), default to **refining that loop** even when `$ARGUMENTS` never named it —
  don't spawn a near-duplicate (e.g. `qa-green-2`) or silently clobber the existing file.

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

## Step 2 — Choose the purpose, explain the choices

Read `../references/output-guide.md`. Reconcile the request with the profile; do not replace it.
If the purpose is unclear, offer concrete project-specific candidates, distinguishing closed
repair/milestone work from open observation. Do not write executable contracts for unselected
purposes. When the purpose is clear, compare ways to run that same contract instead of adding goals.

State the kind, target, criteria/trigger, reaction boundary, gate, state and cap/run mode together.
Ask once only when a genuinely ambiguous, high-impact choice needs resolution. Use the host's
question UI if exposed, otherwise normal chat. Already supplied scope/runtime/cap/gate decisions
are not questions. For minimal interaction, state conservative assumptions; ambiguous CI intent
defaults to a capped closed loop unless the user explicitly wants a comparison first.

For closed work, derive strict SUCCESS CRITERIA from the accepted request and invariants, not
from what is easiest to pass. For greenfield work, use the user's spec (ask only missing material
requirements), then bootstrap a real gate. For open work, settle WATCH TARGET, objective TRIGGER,
notify/act scope, destination, dedup and run-indefinitely versus stop-on-event. A missing completion
gate is correct for a watcher; vague judgment without an observable signal is not a good loop.
Mature closed work with no rejecting check may be the wrong tool: explain that and propose a
single guided prompt or an explicitly agreed objective manual check, never an invented gate.

## Step 3 — Gate + stop condition, sized to the project (AskUserQuestion / propose)

- **VERIFY gate**: build it from profile B. Always order checks **fastest -> slowest**
  (typecheck/lint before unit before integration before e2e) and stop at the first red — the
  cheapest check that can fail the work runs first. This "backpressure ladder" is the main
  lever on cost per accepted change.
  - Single-stage -> one gate command + pass condition.
  - Multi-stage -> a **two-stage gate**: establish the initial baseline once; after changes,
    run affected checks and the required final acceptance gate. Reuse only evidence that is
    valid for the same target, input and environment. Repair-target RED is expected; distinguish
    it from an invalid harness or a previously-green invariant regressing (FREEZE, no commit).
  - Acquire missing evidence and replace invalid or target-mismatched evidence even without a
    source diff. Refresh time-dependent/external observations. Do not repeat valid unaffected
    green checks or full suites at both ends of every iteration. Preserve every criterion's proof.
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
  - Cap exhaustion is an incomplete checkpoint, not success or permission to shrink scope.
    Use K consecutive successes only for a real repeat-stability criterion or explicit K request;
    different meaningful observations must justify repetition. Do not add K=3 by habit.
  - **Cost/time envelope (show before confirming N, so N isn't picked blind)**: if profile F has a
    measured gate runtime (from the Step 6 smoke-test or user-given), show the wall-clock band
    `~N x <gate seconds>`; otherwise show the formula only — `worst case = N x <gate command>`,
    actual time unknown until the first gate run. Do NOT fabricate a token/cost estimate (LLM
    figures are unreliable) — wall-clock from a measured gate is the only grounded number; flag a
    heavy gate so a big N is a conscious choice.

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

## Step 4 — Match the host-native runtime to the purpose

Read only the current host guide: `../references/claude-code.md` or
`../references/codex.md`. A Codex adapter changes the launch surface, not the common contract.
Honor explicit runtime choices. Offer one recommendation and meaningful alternatives with the
shared output guide. Separate documented, installed-help-confirmed, session-available and unknown.
Unconfirmed features get conditional explanation, not runnable copy blocks.

For risky/spec-heavy work, keep the independent completion check: a checker sees the spec + diff
and evidence, not the maker's reasoning. Native goal evaluators do not independently run the gate.
No self-grading: required objective checks and independent reviews remain required. A new checker
agent requires explicit authorization; an absent checker is a verification gap, not a soft pass.

FINAL is the closed contract's report marker, not proof the host stopped. Render native stop and
resume instructions from the chosen host guide. Open loops have no FINAL or completion evaluator;
stop-on-event may report TRIGGERED, then stop the exact native schedule if configured.
Generated/configured/started/finished are separate states. Do not create a runner or schedule here.

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

### Emitted scaffold

<!--
makeloop loop-prompt template (canonical).

Structure: pick ONE CORE — CLOSED (drive-to-done) or OPEN (watch/react) — by the loop kind,
then add OPTIONAL blocks that /makeloop includes only when the Project Profile (DISCOVER step)
triggers them. Ship the smallest loop the project supports — do not paste a two-stage gate for
a single `npm test`. Closed-only blocks never appear in an OPEN loop and vice versa.

completion report: FINAL for closed contracts; <promise>DONE</promise> for verified ralph-loop. Native stopping is a separate host action.

Output language: this scaffold is in English, but /makeloop renders the FINAL prompt in the
user's working language (the conversation's language). Keep only machine-significant literals
unchanged: shell/gate commands, file paths, JSON keys, FINAL / <promise>DONE</promise>, ITERATING.
-->

# ============ CLOSED CORE (kind=closed; drive-to-done) ============

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
- Run the gate fastest -> slowest and STOP at the first red.

STATE FILE: .loop/state.md   (or existing state file from the project)
- Read it before starting. This is a resume, not a restart.
- Each iteration, append: what you did / what passed or failed / the single next step.

EACH ITERATION:
1. READ the loop contract (GOAL + SUCCESS CRITERIA + RULES) and state. Reconcile goal version,
   repo/worktree, exact session/run handle, cancellation and surviving work; one writer per state.
   Acquire baseline evidence on first run; later reuse valid unaffected results for the same
   target/input/environment. Obtain missing proof and replace invalid or mismatched proof.
2. PLAN the single highest-impact next step (just one).
3. EXECUTE the smallest change that advances that step.
4. VERIFY the changed surface and unmet criteria; refresh affected/time-dependent evidence.
   Run required final acceptance checks once at the checkpoint. Record target, input/environment,
   result and evidence pointer in state. Do not repeat unaffected green checks.
5. DECIDE: are ALL success criteria met?
   - Yes -> print "<completion token>" and stop.
   - No  -> print "ITERATING" and continue, fixing the weakest criterion first.

STOP WHEN: VERIFY passes every criterion, OR <N> iterations are reached.
ON STOP: summarize actual changes, proved criteria, unmet requirements and evidence. Cap/budget
exhaustion is an incomplete checkpoint, never success or a smaller replacement goal. Preserve the
original scope and cumulative counters. Apply the selected host stop procedure and record its
actual result separately from the report marker. Reconcile uncertain external effects; never resend.

RULES:
- Never call it done until the gate actually passes. No self-grading.
- First VERIFY counts: if VERIFY already passes every SUCCESS CRITERION before any change, that is a real success -> report FINAL honestly ("already satisfied, no loop work needed"); never fabricate or imply work that didn't happen.
- maker != checker: preserve independent checking for risky/spec-heavy changes; objective checks
  are real evidence, native evaluators are not tool-running checkers. Spawn only when explicitly
  authorized; otherwise record a required independent review as unmet, never self-approve it.
- Surgical changes only: every diff line must trace back to GOAL. <off-limits from profile D>
- Search before assuming: grep before claiming a thing is missing or reimplementing it — "it's not there" is only true after you've looked.
- No fake done: no placeholders/stubs/TODOs reported as complete; never delete, skip, or weaken a check to make the gate go green.
- Report compactly: a PASS is one line; a FAIL gives {expected / actual / what to fix}. Don't re-print an unchanged prior failure — it poisons the context.
- Re-verify the diff, not the world: establish criterion coverage, reuse valid unaffected proof,
  acquire missing proof and replace invalid/mismatched proof. External inputs/time can invalidate
  evidence without a git diff. A valid prior green is not a reason to repeat it.
- Retry by failure class: rate-limit->backoff; validation->rewrite-from-feedback; 5xx->retry then move on; tool-unavailable->pause+notify.
- Empty is not failure: a check that runs cleanly and returns nothing (no matching lines, empty diff, no-op build) has genuinely passed -> record it as a real PASS, don't read silence as "try harder". Only a true error/failed assertion re-enters the retry ladder.
- Shrink the unit on repeat failure: same subtask fails twice -> re-scope to the smallest failing fragment (function/line/test); escalate only after that fails.
- Do not ask routine questions mid-loop. Continue within accepted scope; a new unsafe or
  high-impact decision is a boundary, not permission to assume consent. Record blockers immediately
  and continue independent authorized work. Never manufacture turns to satisfy status thresholds.


# ============ OPEN CORE (kind=open; watch/react — no FINAL) ============

# WATCH: <short watch name>

WATCH TARGET: <signal observed — deploy status / app.log / PR comments / the queue>. <runbook if any>
INTENT: keep watching and react each time the trigger fires. No "done" — running until stopped is correct.

TRIGGER CONDITION (objective predicate over the observed signal; REPLACES a success gate):
- FIRE when: <predicate, e.g. line matches /ERROR|FATAL/; status == "failed"; a new unread item>
- A recurring condition to REACT to, not one that becomes permanently true. Precision matters.

CURSOR FILE: .loop/cursor.json   (last-seen marker + last-fire digest; NOT a done/failed/next ledger)
- COLD START (first run): seed the cursor to the signal's CURRENT end/latest so pre-existing items are already-seen and you fire only on what arrives AFTER launch; replay existing backlog only if the request explicitly asks (bounded, deduped pass, then advance).

EACH TICK (one interval, or one event):
1. OBSERVE: read the current signal; load the cursor.
2. EVALUATE: trigger true for something NEW (beyond the cursor)? No -> do nothing, advance, wait. Yes -> 3.
3. DEDUP: already fired (digest / cooldown)? Skip. Edge-trigger, not level-trigger.
4. REACT (idempotent): NOTIFY one message {what fired, evidence, where, when} to a CONCRETE
   project-bound channel (resolve <channel> to one real destination — a file always works in a
   bare runtime; PushNotification / issue / chat only if actually wired); or ACT with an
   idempotency key = <stable key over event id> so re-firing can't double-act.
5. ADVANCE the cursor and continue.

RUN MODE: <run-indefinitely>  # never prints a token   OR  <stop-on-event>  # first fire -> NOTIFY, print "TRIGGERED", exit
RUNTIME: <one confirmed host-native observation mode>. Observe fresh signal on each tick.
Bind exact schedule/run identity, expiry and cancellation procedure in the saved contract.
Generate the contract only; do not configure a schedule from this text.

LIVENESS/COVERAGE: trigger must cover every terminal/failure state (crash/hang/OOM) — "if it died now, would this emit?";
emit a slow heartbeat so alive vs dead is visible.

STOP WHEN: event-fired [stop-on-event] / watch-target-gone / cancellation / host expiry /
budget (notify+exit), otherwise keep observing. Run-indefinitely is intent, not guaranteed uptime.
Reconcile real native run state before restarting; do not double-act or reset an existing cursor.

RULES:
- React to reality, don't grade your own work (correctness = coverage + precision).
- maker != checker: independently verify risky actions before their side effects; do not let
  the actor self-approve. New checker agents require explicit authorization; missing required
  independent proof is a blocker, not a passing observation.
- Surgical changes only: react only to what the trigger matched; don't fix unrelated things while you're here.
- Search before assuming: confirm the signal is real (read/grep the source) before firing — "nothing happened" is only true after you've looked.
- No fake done: never fabricate or suppress an observation to stay quiet, and never weaken the trigger to silence it — a fire must reflect a real event.
- Edge-trigger: one notification per NEW occurrence; suppress until change/cooldown.
- Idempotent actions; report compactly (a fire is one line; silence prints nothing).
- Do not ask routine questions mid-loop; note blockers in cursor and continue independent
  authorized observation. New unsafe actions require a boundary decision, not guessed consent.


# ============ OPTIONAL blocks (include per profile) ============

## [multi-stage verify] Two-stage gate — replaces CORE VERIFY
VERIFY — two-stage gate (never self-grade):
- pre-gate: establish <build + baseline check> once for this target/input/environment;
  reuse valid unaffected results. Repair-target RED is expected, not poisoned-baseline.
- post-gate: <affected checks + required final acceptance audit> after relevant changes.
PASS = <all acceptance criteria proved + previously-green invariants show 0 regression>
- Invalid harness or unexplained baseline failure -> HALT (stop_reason=poisoned-baseline).
- Previously-green invariant regresses -> FREEZE, do NOT commit (stop_reason=regression).
- Acquire missing or invalid/mismatched proof; never repeat a valid unaffected green merely
  because another iteration began. Keep full criterion coverage and required release gates.

## [self-driving harness] Observation-validity check — into EACH ITERATION after driving
- After driving the harness, validate the observation BEFORE trusting it:
  blank/baseline-identical screenshot, empty snapshot, or frozen run
  -> HALT (stop_reason=unrecoverable-harness). A crash -> HALT (stop_reason=pinata).

## [baseline/golden/scenarios] Regression-guard — into EACH ITERATION after the fix
- Add ONE minimal regression case (<scenarios path>/<name>) that asserts the violated
  invariant, tied to the root-cause fix. One fix + one guard per commit.

## [autonomous loop] Budget — under STATE FILE
BUDGET (write into state): iteration cap <N> / wall-clock <T> / no-progress streak <P> /
token+cost cap <C> when measurable (notify at 85%, stop at 100%).
Keep cumulative counters across resume, distinguish prompt/native limits, and mark unmeasured
spend unknown. Budget exhaustion is incomplete; never claim task success or shrink the objective.

## [autonomous loop] No-progress circuit breaker — into EACH ITERATION
- Hash {tool name + args} per action, keep a short window. Same action repeated (3rd
  identical, or >85% similar plan/action across iterations) -> stop_reason=no-progress.

## [recurring loop] Cross-run learnings
LEARNINGS FILE: .loop/learnings.md  (re-read at the START of every run, before the contract)
  Two sections: ## DURABLE (corroborated, obeyed) and ## UNVERIFIED (candidate, read-not-obeyed).
- On any recurring failure, write the lesson to UNVERIFIED first, tagged with occurrence-count +
  an evidence pointer. Promote to DURABLE only on a 2nd occurrence or an independent pass — one
  atypical run may never mint a DURABLE rule.
- A learning may never rewrite a SUCCESS CRITERION / gate / stop condition (human edit only).
- Prefer category-level prevention (a DURABLE rule folded into lint/AGENTS.md) over a single
  regression case.

## [unattended/scheduled] Escalation handoff — replaces silent death on a dead-end
ON DEAD-END (failure / budget / unrecoverable-harness): write a context-rich handoff (what
was tried, last error, where it stopped, run_id) to <inbox: file / issue / channel>. A run
that found nothing archives itself quietly. Escalation-to-human is a success path.

## [unattended/scheduled] Scheduled-loop safety
- Idempotency: stamp each side-effecting apply with an idempotency key (node re-runs from its
  start on resume; duplicate effects must be impossible).
- Bind the placeholders (don't ship raw): set the idempotency key + the allowed-action set to the
  project's REAL values (stable event-id; the ONE permitted action). An unbound deny-list lists
  generic verbs with no project-specific authority check — it blocks nothing concrete.
- Durable schedule: choose ONE confirmed native scheduler or explicitly requested external
  scheduler (cron / CI / Actions with per-loop concurrency). Never duplicate continuation.
  Bind exact job/session, scope, cancellation and expiry; in-process timers die on restart.
- Auto-approve (tiered): safe reads auto; in-repo writes auto (git-reviewable); shell /
  external / out-of-repo / subagent-spawn gated. Trust boundary = this repo only.
- Intent deny-list (judge real impact): no force-push / mass-delete / secret-exfil /
  disable-logging / push-to-main / prod-deploy without explicit human sign-off.
- Security tax (unattended = unreviewed attack surface): security checks IN the gate
  (secret scan / dependency audit / SAST); human approval before anything irreversible;
  sanitize logs (no credentials); audit skill/connector sources; re-audit permissions on a cadence.

## [many discrete criteria] JSON done-ledger — replaces the markdown success checklist
DONE LEDGER: .loop/done.json = [{ "criterion": "...", "status": "pass|fail",
"verified_by": "<gate output>" }]. status -> "pass" only with a real verified_by; done when
all "pass".

## [open only] Dedup/cursor block — fold into the OPEN core
- Edge-trigger suppression: keep a digest of the last fire in .loop/cursor.json; the same
  condition staying true must NOT re-fire — only a NEW occurrence (or post-cooldown) fires.
- Last-seen cursor: persist last id/timestamp/status so each tick computes "what is new".
- Idempotency key (if the watcher acts): stable key over the event id; re-handling is a no-op.

## [greenfield/early · closed only — suppressed when kind=open] Bootstrap block — prepend as ITERATION 0 (runs once)
ITERATION 0 — bootstrap the gate (run once, before the normal loop):
- Scaffold minimally: repo, package manager / project file, the stack's test runner — only
  what the SUCCESS CRITERIA require.
- Encode each SUCCESS CRITERION as a FAILING acceptance test; run and confirm RED.
- Commit scaffold + red tests. From here <test command> is the gate; the loop drives red -> green.

## [taxonomy] Extended STOP — replaces CORE "STOP WHEN" line; label every halt
STOP WHEN (label each halt with stop_reason in the log):
- success              : all original criteria proved; K repeats only if explicitly requested
                         or required by a meaningful stability criterion
- no-progress          : <P> iterations new-nothing, or repeated tool-call/plan (circuit breaker)
- oscillation          : same problem-fix pair repeated 3x
- failure              : one problem fails to fix after 3 tries
- budget               : iteration / wall-clock / token+cost cap reached
- escalate             : dead-end handed off to a human with full context  [unattended only]
- regression           : post-gate dropped a previously-passing check   [two-stage only]
- poisoned-baseline    : invalid harness/unexplained baseline failure                            [two-stage only]
- unrecoverable-harness: blank/empty/frozen observation                  [harness only]
- pinata               : crash                                           [harness only]
- scope-boundary       : would touch an off-limits area / exceeds turn cap [invariants only]


## Step 6 — Validate, save, explain, and provide copyable launches

Read `../references/output-guide.md` and the current host launch guide. Before writing, inspect
assembled output: exactly one core; correct kind-only blocks; no unbound scaffold placeholders;
all forced directives honored; every criterion mapped to real evidence; launch path and state
agree; copy blocks have the right destination and contain no explanation or other candidate.
An unavailable check is an unresolved verification gap. Do not treat it as a passing criterion.
Fix assembly defects before saving. State any unresolved acceptance gap without claiming success.

Generation is not project execution. Do not run the project's test/build gate merely to write a
prompt. If the user explicitly authorized a lightweight baseline check, run it once, reuse valid
existing evidence, and distinguish expected repair RED from a harness error. Do not run destructive,
network or heavy gates just for a smoke test.

Save the chosen contract as `.loop/<slug>.md`, using a distinct slug for a different purpose.
Refine a matching existing contract instead of creating a duplicate; preserve its kind/state and
all unrelated blocks. Seed `.loop/<slug>-state.md` (closed) or `.loop/<slug>.cursor.json` (open)
only if absent. Never reinitialize existing progress, evidence, cancellation, or cursor history.
Closed state holds original goal/version, cumulative budget, done/failed/next and evidence pointers.
Open cursor starts at EOF/latest on the first tick; pre-existing matches do not fire unless bounded
replay was explicitly requested. Cursor keys include last_seen and last_fired_digest.

Update `.loop/INDEX.md`: slug, purpose, kind, gate/trigger, cap/run mode, chosen runtime (or
unselected), saved paths and launch message. Showing alternatives does not select an unchosen
runtime or start anything. Keep one writer and reconcile real run/session ownership before resume.

Output in the user's language: recommended launch block first, concrete Loop brief, explained
candidate cards (Codex run options on Codex), saved paths and remaining gaps. The complete prompt
lives in its saved file, not a chat dump. Each usable alternative has its own resolved copy block.
For unresolved purpose comparisons, explain choices and ask before writing executable loop files.

Stop after generation. Do not begin the project work, create an automation, or claim it is running.
