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
| **Goal / scope** | "finish the auth refactor", "全テストを緑に", "complete the project" | Goal hint + scope; skip resolved scope/goal questions; show criteria without re-asking supplied decisions. |
| **Runtime** | "one iteration", "/goal", "self-paced", "interval 30m" / "30分ごと", "schedule", "CI/external resume", "ralph-loop" | Sets the runtime; omit its question, still apply Step 4 capability/stop rules. |
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

## Step 1 — DISCOVER: build a bounded Project Profile

For a fresh contract, read `../references/project-profile.md`: reconcile live conversation intent
with repo reality, classify kind/maturity, find real checks/signals, invariants and existing loops.
Use only read-only discovery; inspect the evidence that can change this loop's decisions.
For refine, keep the fast path from Step 0; do not restart discovery or reset state.

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

### Canonical block source

Read `../templates/loop-prompt.tmpl.md` at assembly, selecting exactly one core and only optional
sections whose profile/directives apply. That file is the sole emitted scaffold, not a second
copy embedded here. Render prose in the user's language and bind every real value. Apply the
current host guide's launch/stop/resume instructions without introducing the other host's tools.

Mandatory safety remains in force in every generated contract:
- No self-grading. Never claim a criterion met without valid direct evidence.
- No fake done: never delete, skip, or weaken a check to make the gate green.
- maker != checker; Surgical changes only; Search before assuming.
- Intent deny-list: no force-push, mass-delete, secret-exfil, disable-logging, push-to-main or
  prod-deploy without explicit human sign-off. Match the actual action to project-bound authority.
- Security tax: unattended work retains the security checks, sanitized logs and explicit
  approval for irreversible actions; moving text does not relax its enforcement.

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

Only in the final response, after saving and checking: explanations/Loop brief, explained candidate
cards (Codex run options on Codex), paths/status/gaps, complete chosen Loop body once, then the
resolved launch blocks at the very end. Do not output launch commands or full Loop bodies during
progress or proposals. Nothing follows the final launch fence; see the output guide.
For unresolved purpose comparisons, explain choices and ask before writing executable loop files.

Stop after generation. Do not begin the project work, create an automation, or claim it is running.
