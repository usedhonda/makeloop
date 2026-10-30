---
description: "Analyze the current project in depth, pin down the work goal, and generate purpose-led loop choices with copyable native launch instructions"
argument-hint: "[goal hint (optional)]"
allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "Write", "Agent"]
---

# /makeloop — build a loop prompt for this project

Read `../skills/makeloop/SKILL.md` section **Final output contract** first, including on
the direct Claude command path. It is the single presentation contract for this command.

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
  Close the feedback path: each iteration targets an unmet requirement, predicts an observable
  result, compares it with reality, and uses that difference to choose the next action.
- **The three hearts of a real loop**:
  1. **Verify** — a *real* gate (a test/build/lint or an objective check), never the agent
     grading its own homework.
  2. **State** — a small record carried across iterations (done / failed / next) so the
     loop resumes instead of restarting and never repeats the same mistake.
  3. **Stop condition** — verified success or an explicit iteration/budget cap. Distinguish
     instruction-level limits from limits actually enforced by the selected native runtime.
- **The four conditions a loop must meet** to be worth building (vs. just one good prompt):
  the task repeats; bad output can be rejected automatically; the token budget can absorb
  retries; and "done" is objective, not a matter of taste. If these don't hold, say so.
- **maker != checker** — the model that wrote the change is too generous a grader; have the
  loop re-verify with fresh eyes (or a sub-agent) on risky changes.
- **The order that survives**: get ONE manual run reliable -> wrap it in a loop with a gate
  + stop condition -> only then schedule it.
  For a selected closed Goal, establish that reliable first work unit inside the Goal; this
  principle is not a requirement to select a manual-only launch before offering native Goal.
- **The metric that matters**: measured time/cost per *accepted outcome*, including failed
  attempts and review. Acceptance rate alone has no universal break-even threshold.
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
its state file, its kind, and every block you weren't asked to change. A copy/path-only refine does not rediscover the
project. If the request instead refreshes the whole remaining-work goal, reconcile its current
outcome and residual work from existing evidence without changing its accepted scope. Skip DISCOVER and the
interactive questions, run the Step 6 pre-save self-check, then output. If the named loop doesn't
exist, fall through to a normal build.

Extract whatever is present (natural phrasing, not strict flags — interpret intent):

| Directive | Example phrasings | Effect |
| --- | --- | --- |
| **Goal / scope** | "finish the auth refactor", "全テストを緑に", "complete the project" | Goal hint + scope; skip resolved scope/goal questions; show criteria without re-asking supplied decisions. |
| **Runtime** | "one iteration", "/goal", "self-paced", "interval 30m" / "30分ごと", "schedule", "CI/external resume", "ralph-loop" | Sets the runtime; omit its question, still apply Step 4 capability/stop rules. |
| **Loop kind** | open: "watch/monitor X", "notify me when", "poll", "alert on", "監視/通知/見張る"; closed: "finish", "complete", "get green", "fix all", "完成/緑に" | Sets KIND. If unspecified, classify in Step 1. On ambiguity default to **closed**. |
| **Iteration cap / budget** | "cap 20", "上限20", "max 20 iterations", "wall-clock 30min", "no-progress 3" | Sets N / wall-clock / no-progress; don't ask. |
| **Pause point (closed)** | "pause before human review", "変更と検証が揃ったら一度止めて" | Add an observable pause point without changing the original goal, required reviews or limits. |
| **Human handoff (closed)** | "leave a summary when you stop", "任せた作業の成果と残件を読めるように", "no handoff summary" | Select or explicitly omit the Handoff summary block; keep the existing state and original goal. |
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
purposes. When the purpose is clear, derive the concrete usable/delivered outcome and its
necessary remaining work first, then recommend the simplest available way to carry that same
contract through completion. Compare execution modes only when their practical difference matters
to this work or the user asks. Absence of native Goal does not impose a one-iteration limit;
do not claim persistence that has not been configured.

State the kind, target, criteria/trigger, reaction boundary, gate, state and cap/run mode together.
Ask once only when a genuinely ambiguous, high-impact choice needs resolution. Use the host's
question UI if exposed, otherwise normal chat. Already supplied scope/runtime/cap/gate decisions
are not questions. For minimal interaction, state conservative assumptions; ambiguous CI intent
defaults to a closed loop with internal progress checkpoints unless the user explicitly wants a comparison first.

For closed work, derive strict SUCCESS CRITERIA from the accepted request and invariants, not
from what is easiest to pass. For greenfield work, use the user's spec (ask only missing material
requirements), then bootstrap a real gate. For open work, settle WATCH TARGET, objective TRIGGER,
notify/act scope, destination, dedup and run-indefinitely versus stop-on-event. A missing completion
gate is correct for a watcher; vague judgment without an observable signal is not a good loop.
Mature closed work with neither a rejecting check nor an accepted plan to build one may be
the wrong tool: explain that and propose a single guided prompt or an explicitly agreed objective
manual check, never an invented gate.

## Step 3 — Gate + stop condition, sized to the project (AskUserQuestion / propose)

Read `../references/feedback-design.md`. Bind the outcome, observations, allowed actions,
feedback decisions and resume state to this project. For closed work, save stable criterion IDs
with their checks, observation-validity conditions and evidence requirements. Specify what an
observable improvement means and how a failed hypothesis changes the next step. A plan or clean
review is not the completion criterion: reconcile uncovered requirements against the original goal.
Keep in-scope residual work in the loop; propose unrelated work separately after completion.
Bind the actual use/delivery path and target to the criteria and evidence. Seed provisional
pending work from the current gaps, not just the user's first task list or existing tests. A
necessary new task must explain which requested outcome remains unmet without it. Derive missing
objective checks within approved scope; never invent a command or silently change the goal,
acceptance standard or authority. Ask only when that material decision cannot be derived.

For closed work, bind a project-specific REMEDIATION SCOPE from existing user authorization,
project instructions, manifest/lockfile, runbook and existing scripts. Include only necessary
repairs/legitimate alternatives, their authorization source and real boundaries. Examples may
include restoring declared dependencies, using a verified tool path, fixing an in-scope script
or regenerating local artifacts; never presume all examples are allowed. Necessary authorized
recovery is part of this goal, not a separate request after a stop. Do not turn unavailable tools
or external-looking symptoms into terminal blockers before this assessment. Existing permission
for external/global work carries forward; absent permission is not created by contract generation.
Resolve only material unknown high-impact choices, not a ritual repair-approval questionnaire.
Materialize the template's strategy-switch trace against likely project impediments: name the
failed assumption, select a genuinely different authorized route, execute its next useful action,
and return to the original criterion. Repeating a command, listing options or receiving advice
is not recovery. Separate native interruption from project impasse; retain actionable work across
instruction refreshes and status replies without requiring another "continue" request.
During a narrow refine, change recovery scope only if requested; preserve existing state bytes.

For closed completion requests, outcome-first adaptive recovery and evidence-budgeted verification
are defaults, not optional wording the user must repeat. Materialize the template's DELIVERY POLICY
against the actual use/delivery path. Do not optimize a local component or test count while the
requested result remains missing. Save these policies, native lifecycle procedures and necessary
details in the Loop Markdown; do not require a long ritual invocation to get this behavior.
Default test stewardship includes both avoiding unnecessary new tests and actively pruning existing
excess in the area being worked on, without another user request. Materialize the DELIVERY POLICY's
pruning rules in the saved contract: evidence-backed consolidation/removal, preserved distinct
behavior and mandatory gates, local incremental scope and no deletion quotas or cleanup detour.
This is not permission to delete failing checks to manufacture success or to edit unrelated areas.
When completing a supplied plan, bind its authoritative reference and intended deliverable in
that Markdown. Carry original constraints and unmet outcomes, not just the plan's easiest tasks.

**Human handoff (closed only).** Select the **Handoff summary** block for unattended
closed work or an explicit human-handoff request; honor an explicit opt-out. A narrow refine adds
it only when that is the requested change. Daytime unattended work and overnight work use the same rule; elapsed duration alone does not select this block. There is no
night/dawn threshold or automatic morning deadline. Continue to accept legacy "morning handoff"
requests and opt-outs. When selected, add a delivery criterion (e.g.
`C-HANDOFF`) to SUCCESS CRITERIA and EVIDENCE MAP: the receiving summary is saved, read back and
consistent with the current ledger/evidence. The user need not say "acceptance criterion" again.
Bind its exact location in the existing state and its format; default to a named section near the
start of Markdown state, after any frontmatter/title. Reuse an existing summary section even
if it has a legacy name; do not rename or migrate state for this wording change. Keep a separate
JSON done-ledger as evidence, not a second summary to maintain. For structured state use only an existing supported summary
field/view; never prepend Markdown to JSON or change its schema. If no compatible, writable, durable,
recipient-readable location exists, explain the storage gap before offering an executable run.
Generation preserves existing state bytes; new state is marked not started, never completed work.

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
  - For a new/changed custom verifier, bind representative acceptable and plausible wrong/partial
    outcomes to its pass rule. Use existing calibration evidence when valid; otherwise plan that
    check in the contract. Generation must not execute the project to manufacture proof.
    An explicitly requested verifier repair with objective expected outcomes can build that
    rejecting check first within the accepted scope. Preserve existing criteria and project setup;
    an uncalibrated green result cannot establish completion.
  - For **UI / web** work, add a "drive-and-capture" check: actually exercise the feature and
    capture an artifact (screenshot / GIF) as proof-of-use — synthetic interaction catches
    wiring/state bugs that unit tests miss, and the artifact doubles as evidence on the PR.
  - **Greenfield / early (no gate yet, but the goal is to build it):** don't refuse — make
    the loop *bootstrap its own gate*. Iteration 0 scaffolds the project (repo, package
    manager, the stack's test runner) and encodes the acceptance criteria as FAILING tests
    (confirm red); from then on that test command is the gate and the loop drives red → green.
    Add the **Bootstrap block** in Step 5.
- If **no automated check exists in a mature project**, warn clearly, help define an objective
  manual check, and ask whether to proceed anyway. If the gate must be an **LLM-as-judge**, use an
  independent checker with a concrete pass/fail/unknown rubric calibrated against reference
  examples and the user's criteria. A different model family alone does not establish reliability;
  do not assume another model or delegation is available. Require inspected evidence for each
  dimension and escalate unresolved judgments instead of guessing. Pair the judge with a
  **deterministic assertion** (value-in-range / file-exists / schema-valid) as an AND-gate —
  mark done only if BOTH pass, and feed the failing check's message into the retry. Ground the
  rubric in the repo (let the judge read the code/conventions before scoring, not just the
  spec) and give it an explicit **anti-cheating axis** (flag test-weakening, mass-renames,
  dependency churn) and a **blast-radius axis** (penalize edits far wider than the goal).
- **STOP taxonomy and counter provenance**: completion, cancellation, actual safety/authority
  boundaries and user/platform limits stop work. Do not invent a hard iteration cap (including
  a default 8). For each existing limit or checkpoint, save its value/unit, source (user,
  platform, or agent-default), evidence and enforcement (instruction/native hard limit versus
  internal review threshold) in the contract and state. Unknown provenance requires reading
  the original instruction/state, not assuming either exhaustion or unlimited permission.
  Internal attempt/no-progress thresholds trigger progress review and replanning inside the
  approved scope, not a new user approval ritual. Preserve history; never reset it to hide work.
  Do not repeat a failed approach without new evidence. This does not authorize unbounded spend.
  Ask only about a genuinely material unresolved cost/time/authority decision.
  - User/platform cap exhaustion is an incomplete checkpoint, not success or permission to shrink scope.
    Use K consecutive successes only for a real repeat-stability criterion or explicit K request;
    different meaningful observations must justify repetition. Do not add K=3 by habit.
  - **Cost/time envelope**: when profile F has a measured gate duration, `N x gate seconds`
    estimates only that gate's contribution if it runs once per attempt. Editing, reasoning,
    review, I/O and backoff add time; this is not a worst-case wall-clock bound. Otherwise mark
    duration unknown. Record actual token/cost usage only if exposed, and keep the explicit
    wall-clock limit separate. Do not run a gate solely to invent an estimate for generation.

**Optional pause point (closed only).** Only when the user asks to stop at a milestone or before
an action, bind the condition to concrete evidence and include the **Pause point** block. A required
review by itself is not a request to pause. Keep the full goal and required review in SUCCESS
CRITERIA; a pause with unmet criteria is an incomplete handoff, not success. Do not turn a vague
"be flexible" into a new pause, a larger cap or automatic extensions. User/platform caps remain binding; an agent-default review horizon is not such a cap.
Reuse the existing state format rather than adding a policy language.
For a time limit, save its start/deadline at first execution and preserve it across resume. Explain
instruction-level timing versus confirmed host enforcement; do not invent remaining usage data.

**If kind=open, this whole section changes** (everything above is the closed path):
- Replace the VERIFY gate with a **TRIGGER CONDITION** — an objective predicate over the
  *observed signal* (not a pass/fail on made work). Precision matters: a false fire trains the
  user to ignore alerts.
- Replace the STOP taxonomy with a **RUN MODE**: *run-indefinitely* (steady-state watcher) or
  *stop-on-event* (fire once, then exit). No success-or-cap.
- Confirm the **dedup policy** (edge-trigger / cooldown window) and, if the watcher **acts**,
  an **idempotency key** so re-firing on the same event can't double-act.
- Bind occurrence identity separately from the watched entity, and specify pending intent,
  confirmed receipt, definite failure and unknown outcome. Notifications are effects too.
  Reading past an event must not lose an unsettled reaction; a restart must not blindly repeat it.
- The metric is **coverage + precision** (did it catch real events without crying wolf), not
  cost per accepted change.

*Honor Step 0*: if the request already gave a gate, cap, budget, success K, or forced a
block on/off, use those values and don't re-ask. Block on/off directives from Step 0
override the profile defaults in Step 5.

## Step 4 — Match the host-native runtime to the purpose

Read only the current host guide: `../references/claude-code.md` or
`../references/codex.md`. A Codex adapter changes the launch surface, not the common contract.
Honor explicit runtime choices. Offer a recommendation and alternatives only for ready proposals with the
shared output guide. Separate documented, installed-help-confirmed, session-available and unknown.
Unconfirmed features get conditional explanation, not runnable copy blocks.
On both hosts, closed completion proposals include an available Goal-equipped version from the start;
recommend native Goal for a request to keep looping until completion. Honor explicit no-Goal or
bounded execution instead when supplied. Bind fresh-Goal creation, continuation, evidenced
completion and actual non-success transitions using the current host guide before classifying readiness.
Not configured/not started does not mean not runnable. Missing lifecycle wording is assembly work
to finish here, not a generic "stop conditions need connecting" excuse to suppress the proposal.
Use the entrypoint SKILL.md Final output contract for mode selection: when both modes are ready,
default to Goal first and ordinary completion second unless an explicit exclusive choice applies.
A request to use Goal selects the recommendation; it does not by itself mean "Goal only". Both reference
the same outcome, state and REMEDIATION SCOPE; they are alternatives, never simultaneous writers.
Ordinary completion is not a single bounded tick. Do not add a watcher to pad these choices.
For compact/reissued launches, read the actual contract/state and retain the original goal,
all remaining work, continuation mode, stop conditions, used/remaining budget with source/enforcement, authority,
forbidden scope, consultation/review and state/resume identity in the saved contract. Apply the
output guide's meaning-preservation check. A blocked backend without a resume control is an
unconfigured continuation, not a reason to select one iteration or reset budget. Surface nearly
exhausted user/platform limits before presenting a launch as able to pursue the whole goal.

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
| Explicit user-requested pause point (closed only) | **Pause point**; stop reason `checkpoint`; omit when not requested |
| Any autonomous (self-paced) loop | **Budget block** + stop reasons `no-progress`, `oscillation`, `failure`; **No-progress circuit breaker** |
| Hard invariants / off-limits boundaries (profile D) | Encode them in SUCCESS CRITERIA + RULES; stop reason `scope-boundary` |
| Existing loop infra (profile E) | Point STATE at the existing files + runbook; reuse scenario format |
| Repeats weekly / will run again (profile = recurring) | **Cross-run learnings** file so the loop gets smarter each run |
| Unattended / scheduled / overnight run | **Escalation handoff** + **Scheduled-loop safety** (idempotency, external scheduler, tiered auto-approve, intent deny-list, token/cost cap) |
| Unattended closed work (day or night), or explicit human-handoff request | **Handoff summary** + delivery criterion/evidence; honor opt-out and narrow-refine scope |
| Many discrete pass/fail criteria | **JSON done-ledger** instead of a markdown checklist |
| Greenfield / early project (no gate yet) | **Bootstrap block** — iteration 0 scaffolds + writes the first failing acceptance tests, then the loop drives red → green |
| Open loop that ACTS (not notify-only) | **Scheduled-loop safety** (idempotency / deny-list / auto-approve) — an acting watcher is an unreviewed attack surface |
| Open loop, run-indefinitely | **Dedup/cursor block** + wire **Escalation handoff** on (a dying watcher must hand off, not vanish) |

**Kind applicability** (which blocks belong to which CORE):

| Block | CLOSED | OPEN |
| --- | --- | --- |
| Two-stage gate · Regression-guard · No-progress circuit breaker · JSON done-ledger · Bootstrap · Independent completion check · Pause point · Handoff summary | ✅ | ❌ (Bootstrap is **suppressed** when kind=open) |
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

Final presentation follows the entrypoint SKILL.md Final output contract. Fill host launch
templates, then check the actual final text for mode count, host/destination labels, no lifecycle
repetition and no text after the last fence. File checks alone do not validate this presentation.

Resolve execution readiness inside this invocation using the output guide before emitting any
launch. Reconcile actual request/contract/state, remaining budget, run ownership and exposed
start/resume/stop capability. Bundle concrete high-impact user decisions; do not assume unanswered choices before saving
and presenting; never use a normal "continue" message as evidence that continuation is configured.
If readiness cannot be established, preserve the requested outcome, report that no executable
launch for that mode was generated, and omit runnable blocks. No command-first/caveat-later output.

Read `../references/output-guide.md` and the current host launch guide. Before writing, inspect
assembled output: exactly one core; correct kind-only blocks; no unbound scaffold placeholders;
all forced directives honored; every criterion mapped to real evidence; launch path and state
agree; copy blocks have the right destination and contain no explanation or other candidate.
Walk the applicable short traces in `../references/feedback-design.md`: does the observed outcome
change the next decision, does interruption preserve consumed attempts and pending effects, and
does a declared stop actually end the chosen native execution? Check both useful repetition and
stalled activity. For closed work, explicitly test both a green subset with original-purpose gaps
(continue needed work) and an already-delivered result with all current proof (skip PLAN/EXECUTE,
report no-change success). Keep this positive branch in every generated closed contract, not only
in an already-green example. Check each final native launch against the current host's success
and non-success stop rules; a saved incomplete checkpoint must not become Codex native success.
For a fresh supported Goal with no owner conflict, verify the initial package includes the Goal
launch with its bound lifecycle even though nothing has been configured or started. Contrast an
actually blocked existing Goal without resume support: preserve it and report that specific gap.
A keyword/structure check alone cannot establish these behavioral properties.
For recovery, walk a repairable missing prerequisite, an actual authentication/authority boundary,
two unchanged failures needing a new approach, and resume after repair. The next decision must
repair/continue when possible, not demand a fresh repair request or stop solely on a count.
For CC, a bare "only blockers remain" exit is insufficient: surface the remediation assessment
and why no productive authorized path remains in conversation before treating that exit as met.
For a requested pause, check that the brief, STOP WHEN and native launch agree, a reached pause
prevents further project actions, and explicit resume does not reset limits or approve pending
review/actions. Do not migrate unrelated blocks or state in a narrow refine.
For a selected handoff, check its criterion/evidence mapping, exact location, runtime updates and
read-back before success, including already-green and no-change runs. Exercise budget/pause and
write-failure paths: no new project work past a boundary and no invented delivery. Match the
receiving location in the final brief to the saved contract; do not present a seed as run evidence.
An unavailable check is an unresolved verification gap. Do not treat it as a passing criterion.
Fix assembly defects before saving. State any unresolved acceptance gap without claiming success.

Generation is not project execution. Do not run the project's test/build gate merely to write a
prompt. If the user explicitly authorized a lightweight baseline check, run it once, reuse valid
existing evidence, and distinguish expected repair RED from a harness error. Do not run destructive,
network or heavy gates just for a smoke test.

Save the chosen contract as `.loop/<slug>.md`, using a short, meaningful slug (for example `ui`
or `auth`) and a distinct slug for a different purpose. Long filenames amplify copy/wrap failures;
follow output-guide.md rather than treating one physical line as sufficient. Preserve existing
paths on refine unless a rename is explicitly in scope; preserve state and update references if renamed.
Refine a matching existing contract instead of creating a duplicate; preserve its kind/state and
all unrelated blocks. Seed `.loop/<slug>-state.md` (closed) or `.loop/<slug>.cursor.json` (open)
only if absent. Never reinitialize existing progress, evidence, cancellation, or cursor history.
Closed state holds original goal/version, criterion/evidence map, cumulative reserved attempts,
running/interrupted work, observed progress, recent failed approaches, next decision and evidence
pointers. Keep its current summary small; reference history instead of replaying full tool logs.
Open cursor starts at EOF/latest on the first tick; pre-existing matches do not fire unless bounded
replay was explicitly requested. Cursor keys include last_seen, last_fired_digest and pending
effect outcomes. Reserve before acting and settle with evidence; initialize only new state files.

Update `.loop/INDEX.md`: slug, purpose, kind, gate/trigger, cap/run mode, chosen runtime (or
unselected), saved paths and launch message. Showing alternatives does not select an unchosen
runtime or start anything. Keep one writer and reconcile real run/session ownership before resume.

Only in the final response, after saving and checking: a short outcome sentence, saved path and
truthful readiness, a brief mode distinction if needed, then resolved paste blocks at the end.
The saved Markdown carries detailed scope, recovery, evidence, limits and native lifecycle rules;
do not reproduce them in long chat cards or launch messages. Keep visible any real unresolved
high-impact choice, capability gap or unusual effect needed to choose/run safely. Use localized
"実行方法" for Japanese mode comparisons (English "Codex run options" remains valid).
The saved file is authoritative; show its complete body only on explicit request.
Use a direct final heading such as **貼り付けるプロンプトはこれです**. Before that group, say to copy
one whole code block to its labeled input; explanations and saved design paths are not to paste.
Do not call a saved path alone "the prompt" or replace the execution prompt with a bare resume
control. Keep the selected task, correct target and saved-contract binding inside the paste unit.
Do not output launch commands or full Loop bodies during
progress or proposals. Nothing follows the final launch fence; see the output guide.
For unresolved purpose comparisons, explain choices and ask before writing executable loop files.

Stop after generation. Do not begin the project work, create an automation, or claim it is running.
