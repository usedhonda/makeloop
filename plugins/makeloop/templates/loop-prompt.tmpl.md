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
5. DECIDE: are ALL success criteria AND mandatory RULES/review requirements proved?
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
  Put every required independent review in SUCCESS CRITERIA. No FINAL until it is actually passed.
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
Each invocation runs one watcher tick; schedule setup is separate. Do not create duplicate schedules.

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
