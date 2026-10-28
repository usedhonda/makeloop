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
- C1: <verifiable criterion 1>
- C2: <criterion 2>
- C3: <criterion 3 — include any hard invariant from profile D>

EVIDENCE MAP: <each criterion -> check, intended target/input, observation-validity condition,
pass rule, evidence location and invalidation; include required review/delivery>.
PROGRESS: <project-specific observable improvement or evidence that rules out a suspected cause>.
Keep criterion IDs and original scope stable. Missing proof remains an unmet requirement.

REMEDIATION SCOPE: <necessary allowed repairs and their existing authorization sources;
project-specific forbidden actions and genuine approval or physical-operation boundaries>.
Repair only prerequisites necessary for the original outcome. This records existing authority;
it grants no new access or permission and does not turn unrelated cleanup into required work.

DELIVERY POLICY:
- Optimize for the original usable/delivered result, not one component, a closed task list or
  test counts. Trace the actual use path across relevant implementation, integration and delivery;
  a locally green fragment does not replace the original outcome. Do not invent unrelated work.
- When an approach stalls, compare necessary authorized repair, alternative tools/paths and
  changes of hypothesis or work unit instead of remaining trapped in the same local subproblem.
  Verify the useful alternative, then return to the original result. Real boundaries still bind.
- Before each check, name the unmet criterion, concrete wrong-result scenario or next decision it
  can change. Prefer the smallest discriminating check; stop checking once sufficient current
  evidence exists and advance implementation, integration or delivery. Preserve mandatory gates
  and independent reviews; never weaken them to save time or make progress appear successful.
- No unchanged-green reruns, equivalent rechecks by another command, per-patch full suites or
  audits without a new decision. A full gate runs once per relevant checkpoint; repeat only for
  a relevant change, concrete counterevidence or an explicit acceptance/release requirement.
  A verification-only cycle needs an actual missing proof or discriminating diagnosis, not habit.
- Maintain a lean test suite as ordinary work, without a separate cleanup request. Do not add
  tests for test-count growth, reversible low-impact edits, or assertions that merely mirror the
  implementation. Reuse existing coverage; add a regression only for a concrete uncovered failure,
  observable behavior or protected contract after the implementation stabilizes.
- While working in the affected area, actively consolidate or remove existing redundant,
  implementation-mirroring, obsolete or no-longer-meaningful tests, fixtures and test-only helpers.
  Establish the reason first: name the retired behavior or map each still-required assertion to
  surviving coverage. Preserve distinct edge cases, security/acceptance checks and required gates;
  age, slowness, a failure or an assertion count alone is not grounds for deletion. Never prune to
  turn red green or conceal a regression. If a test is failing, diagnose the failure before pruning;
  if its value is uncertain, retain it and proceed with the original outcome.
  Keep pruning local and incremental, record the removed obligation or surviving coverage and use
  only the smallest affected check needed. No repository-wide audit, deletion quota, replacement
  test per deletion, extra review gate or repeated full-suite cleanup cycle; delivery stays primary.
- Keep execution/stop/resume procedures, criterion evidence, recovery authority, remaining work
  and cumulative limits in this contract/state. Surface the evidence needed by the actual native
  evaluator in conversation; a file pointer alone is not evidence of completion or a terminal wait.

VERIFY — the gate (run these; never self-grade):
- <verify command 1, e.g. npm run typecheck>   # fastest first
- <verify command 2, e.g. npm test>            # slower last
PASS = <exact pass condition, e.g. all tests green, 0 type errors, exit 0>
- Run the gate fastest -> slowest and STOP at the first red.

STATE FILE: .loop/state.md   (or existing state file from the project)
- Read it before starting. This is a resume, not a restart.
- Keep a compact current summary: goal/version, criteria/evidence, cumulative attempts, running
  work, recent failure signatures/approaches, progress delta, next decision and owner/stop status.
  Reuse existing pending work: each unresolved item keeps its relation to the original outcome,
  evidence of necessity, actual status (including approval/other-owner waits) and next action.
  The task list is provisional; completed-item history and original acceptance remain intact.
  Keep each impediment's symptom, diagnosis, authorized repair/alternative, observed result and
  next action or genuine unblock condition in this existing state; do not migrate its format.
  For each limit/checkpoint retain value/unit, source/evidence and enforcement; distinguish
  user/platform limits from agent-default review thresholds. Investigate unknown provenance.
  Append terse attempt records; keep full logs behind evidence pointers, outside the loaded summary.
- An attempt is one meaningful plan/action/evidence/decision cycle, not every tool call.
- Before each attempt's first action, reserve its ID and increment cumulative consumption; mark
  it running, then settle with the result. Include baseline checks and bootstrap. Interrupted
  attempts remain counted. Persist updates atomically when possible; never reset on resume.

EACH ITERATION:
1. READ the loop contract (GOAL + SUCCESS CRITERIA + RULES) and state. Reconcile goal version,
   repo/worktree, exact session/run handle, cancellation and surviving work; one writer per state.
   Settle any interrupted attempt against actual artifacts/receipts before new work. Check remaining
   user/platform limits before reserving the next attempt. Cancellation or their exhaustion prevents new project
   work; result reconciliation, checkpoint/reporting and exact native stopping remain necessary.
   On resume, first confirm whether the saved impediment is resolved; retain the original goal,
   limits and cumulative history rather than replaying the failed operation or creating a new Goal.
   If it is unchanged and no new authorized productive path exists, preserve the checkpoint,
   report the unchanged unblock condition once and apply actual host stop rules. Do not replay
   the failed project action merely because resume occurred; account for actual attempts and
   native turn/cost usage without resetting or concealing them.
2. OBSERVE the requested outcome through its actual use or delivery path. Compare current evidence
   with the original goal and criteria, not only the existing task list or suite. Update pending
   work with newly discovered necessary tasks and the requested outcome they serve. Acquire baseline
   evidence on first run; later reuse valid unaffected proof for the same target/input/environment.
   Replace missing/invalid proof; validate required collection/source access. Do not invent commands.
3. PLAN a meaningful step by dependency and impact: remove a blocker, implement/integrate, verify
   the use path, or perform required authorized delivery/review. Explain why the outcome needs it,
   record the hypothesis and expected result, and choose a discriminating experiment if uncertain.
   Derive missing objective checks within scope without weakening acceptance. Only proceed to the
   success decision when the original outcome has no unresolved work or missing evidence.
4. EXECUTE the smallest change or experiment that advances that step.
5. VERIFY the changed surface and unmet criteria; refresh affected/time-dependent evidence.
   Run required final acceptance checks once at the checkpoint. Record target, input/environment,
   result and evidence pointer in state. Do not repeat unaffected green checks.
6. DECIDE from expected vs actual result. Retain useful changes; repair a caused regression before
   unrelated work. Record the observed delta and next decision, not just a new wording of the plan.
   Reconcile the original usable/delivered outcome, ALL criteria, required reviews and delivery.
   A finished task list or clean review does not close uncovered aspects of the original request.
   Add work only if it serves that outcome, repairs a caused regression or obtains required proof;
   propose unrelated improvements separately. Preserve purpose, acceptance and authority boundaries.
   - Original outcome, every criterion and mandatory RULE/review proved; no unmet or unverified
     work remains -> print "<completion token>" and stop.
   - Evidence supports a next step -> record it; print "ITERATING" within the selected run mode.
     A work unit or this marker is not a return boundary. Unless an explicit bounded pass was
     selected, continue useful authorized work in the current execution. Cross-turn continuation
     requires the selected native mechanism; do not pretend an ordinary message configured it.
   - Failure persists -> narrow the failing unit or change the hypothesis/check; do not replay a
     failed approach without new evidence. Internal no-progress/oscillation thresholds trigger
     diagnosis/replanning, not count-only abandonment. Respect explicit user stop policies.
   - Impediment -> diagnose on the first failure and apply REMEDIATION SCOPE. A necessary safe,
     authorized repair is original-goal work, not an unrelated task needing a fresh instruction.
     Repair the prerequisite or use a verified permitted alternative, confirm the result, then
     return to the original pending work in the same run. A tool name or an external symptom
     alone does not prove an external dependency. If no authorized productive repair/alternative
     exists, continue independent authorized work. Only when neither remains, save an incomplete
     checkpoint with diagnosis, attempted repairs or concrete reasons they cannot be attempted,
     remaining work, the actual waiting party/input and the condition that would unblock it.
     Do not spin, clear the residuals or pretend project/native success. Follow actual host stop
     controls separately. Never turn uncertainty into completion.

STOP WHEN: The original outcome and every criterion are proved with no unmet/unverified work,
OR the recorded remediation assessment proves no authorized productive repair/alternative or
independent safe work remains (including only approval/other-owner waits such as required human
review, with waiting party and condition surfaced), OR cancellation,
a safety/security incident requires immediate halt, or an applicable user/platform limit is
reached. An authority boundary stops its affected action immediately, not independent authorized
work. Internal checkpoint counts alone do not end the goal.
ON STOP: summarize actual changes, proved criteria, unmet requirements and evidence. Cap/budget
exhaustion is an incomplete checkpoint, never success or a smaller replacement goal. Preserve the
original scope and cumulative counters. Apply the selected host stop procedure and record its
actual result separately from the report marker. Reconcile uncertain external effects; never resend.

RULES:
- Never call it done until the gate actually passes. No self-grading.
- First VERIFY counts only after reconciling the original requested use/delivery outcome: if every
  SUCCESS CRITERION has valid proof and no original-purpose work or evidence gap remains before
  any change, report FINAL honestly ("already satisfied, no loop work needed"). A green subset or
  a completed initial task list is insufficient; never fabricate or imply work that didn't happen.
- maker != checker: preserve independent checking for risky/spec-heavy changes; objective checks
  are real evidence, native evaluators are not tool-running checkers. Spawn only when explicitly
  authorized; otherwise record a required independent review as unmet, never self-approve it.
  Put every required independent review in SUCCESS CRITERIA. No FINAL until it is actually passed.
- A new or changed custom verifier needs representative acceptable and wrong/partial cases;
  reuse existing calibration evidence when valid. Independent review proves only dimensions
  actually inspected against the accepted rubric. Unsupported dimensions remain missing proof.
- Surgical changes only: every diff line must trace back to GOAL. <off-limits from profile D>
- Search before assuming: grep before claiming a thing is missing or reimplementing it — "it's not there" is only true after you've looked.
- No fake done: no placeholders/stubs/TODOs reported as complete; never delete, skip, or weaken a check to make the gate go green.
- Report compactly: a PASS is one line; a FAIL gives {expected / actual / what to fix}. Don't re-print an unchanged prior failure — it poisons the context.
- Re-verify the diff, not the world: establish criterion coverage, reuse valid unaffected proof,
  acquire missing proof and replace invalid/mismatched proof. External inputs/time can invalidate
  evidence without a git diff. A valid prior green is not a reason to repeat it.
- Retry by failure class for repeat-safe operations: rate-limit -> bounded backoff; validation ->
  diagnose from feedback; 5xx -> bounded retry; tool-unavailable -> diagnose and apply
  REMEDIATION SCOPE before classifying it as a terminal blocker. Reconcile
  an uncertain side effect before any retry. All retries remain inside the cumulative budget.
- Empty is not failure when the required observation is valid: no violations, an empty diff or a
  legitimate no-op can pass. Missing mandatory test collection, unreadable input or a partial/
  failed query is a verification gap, not success. Do not rerun a valid empty result by habit.
- Shrink the unit on repeat failure: the same subtask fails twice without evidenced progress ->
  investigate the smallest failing fragment (function/line/test) or change the hypothesis before
  escalating. Preserve the original goal and criteria while narrowing the next action.
- Do not ask routine questions mid-loop. Continue within accepted scope; a new unsafe or
  high-impact decision is a boundary, not permission to assume consent. Record impediments promptly,
  not an automatic blocked status. Never attempt a prohibited repair to prove it is prohibited.
  Reuse existing authorization, including explicitly approved external/global operations; do not
  demand it again. Unapproved access/permission changes, secret exposure, destructive effects,
  money movement or required physical authentication remain boundaries. Never manufacture turns
  to satisfy status thresholds or replace a stopped Goal to evade its native controls.
- Existing user authorization and host enforcement are distinct. If a necessary authorized
  repair is denied by sandbox/approval controls, record the exact runtime boundary and available
  legitimate approval/unblock control; do not replay the same denied operation without a relevant
  state change or change permission/sandbox settings to bypass it. Use existing authorized native
  approval mechanisms when available, otherwise identify only the minimum necessary user action.
  Continue independent authorized work; no possible repair implies a blocker only after assessment.


# ============ OPEN CORE (kind=open; watch/react — no FINAL) ============

# WATCH: <short watch name>

WATCH TARGET: <signal observed — deploy status / app.log / PR comments / the queue>. <runbook if any>
INTENT: keep watching and react each time the trigger fires. No "done" — running until stopped is correct.

TRIGGER CONDITION (objective predicate over the observed signal; REPLACES a success gate):
- FIRE when: <predicate, e.g. line matches /ERROR|FATAL/; status == "failed"; a new unread item>
- A recurring condition to REACT to, not one that becomes permanently true. Precision matters.

CURSOR FILE: .loop/cursor.json   (last-seen marker + last-fire digest; NOT a done/failed/next ledger)
- COLD START (first run): seed the cursor to the signal's CURRENT end/latest so pre-existing items are already-seen and you fire only on what arrives AFTER launch; replay existing backlog only if the request explicitly asks (bounded, deduped pass, then advance).
- Bind <real occurrence identity or persisted recovery/failure transition> separately from the
  entity being watched. A later failure of the same entity is a new event, not a duplicate.
- Keep last_seen as the read frontier, last_fired_digest for confirmed reactions, and pending
  entries for unsettled effects. Preserve existing cursor/state on every restart.

EACH TICK (one interval, or one event):
1. OBSERVE: load cursor and unsettled effects, then read the current signal. Check source access,
   completeness and <project-specific validity condition>. A failed/partial read is not a quiet
   healthy tick: keep the frontier, record the observation gap and hand off under the stop policy.
   Apply cold-start only on the first valid observation, never again merely because of a restart.
2. RECONCILE pending/unknown effects using <concrete receipt lookup or authoritative observation>.
   Confirm completed reactions; retain definite failures for bounded retry under the same authority.
   An unknown result is not permission to resend or mark handled. If no lookup can resolve it,
   keep the item blocked with a local handoff; continue independent authorized observation.
   Select due, definitely-not-applied retries from pending independently of last_seen and route
   them to step 4 with the same occurrence key. Pending-in-flight/unknown effects are not retries.
3. EVALUATE + DEDUP: trigger true for a new occurrence beyond the read frontier? Already confirmed
   or pending for that occurrence? Do not duplicate it. A non-trigger requires no reaction.
4. RECORD intent before REACT: persist occurrence key, intended action and pending status. NOTIFY
   one message {what fired, evidence, where, when} to a CONCRETE
   project-bound channel (resolve <channel> to one real destination — a file always works in a
   bare runtime; PushNotification / issue / chat only if actually wired); or ACT with an
   idempotency key = <stable key over event id> so re-firing can't double-act.
5. SETTLE: save receipt/evidence and confirmed, definite-failure or unknown outcome. A key prevents
   duplicate side effects only when the destination enforces it; never promise exactly-once from
   the cursor alone. A timeout or interrupted pending action remains unknown until reconciled.
6. ADVANCE last_seen only after each observed occurrence is durably represented or intentionally
   ignored. Never discard unresolved effects when advancing. Update last_fired_digest only after
   confirmed reaction. Stop-on-event reports TRIGGERED only after that reaction is confirmed.

RUN MODE: <run-indefinitely>  # never prints a token   OR  <stop-on-event>  # confirmed reaction -> print "TRIGGERED", exit
RUNTIME: <one confirmed host-native observation mode>. Observe fresh signal on each tick.
Bind exact schedule/run identity, expiry and cancellation procedure in the saved contract.
Each invocation runs one watcher tick; schedule setup is separate. Do not create duplicate schedules.

LIVENESS/COVERAGE: trigger must cover every terminal/failure state (crash/hang/OOM) — "if it died now, would this emit?";
emit a slow heartbeat so alive vs dead is visible.

STOP WHEN: confirmed reaction [stop-on-event] / watch-target-gone / cancellation / host expiry /
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

## [explicit pause point · closed only] Pause point — fold into STOP WHEN and action boundaries
PAUSE WHEN: <user-requested milestone or before-action boundary, with its evidence>.
- Add this non-success halt to the selected STOP WHEN, including Extended STOP when used.
  Check after state reconciliation and before each new project action, including checks/review.
  At the reached boundary, stop the whole run's project work, not just one subtask. Reuse existing
  proof; do not run another check or independent task past the boundary just to finish the goal.
- If every original criterion and required review already has current proof, report success
  without new work. Otherwise save stop_reason=checkpoint, reached condition/evidence, unmet
  criteria and the next step in the existing state; never emit the completion token for that
  incomplete handoff. Apply the selected host stop procedure and report its actual status.
- Keep this pause pending across ticks/restarts until the user explicitly resumes past it.
  Record that release so this one-time boundary does not immediately pause again. Releasing it
  does not grant pending review/approval, relax scope, or reset cumulative limits/deadlines.

## [autonomous loop] Budget — under STATE FILE
LIMITS / CHECKPOINTS (write into state): actual user/platform iteration, wall-clock or token/cost
limits, and internal progress-review thresholds if useful. For each: value/unit, source/evidence,
enforcement and response. Render only applicable entries; do not invent a hard default cap.
Keep cumulative counters across resume and mark unmeasured spend unknown. Internal thresholds
trigger evidence review/replanning inside scope, not stopping solely on count or requesting an
extension. Explicit user/platform exhaustion is incomplete; never shrink the goal or claim success.
This does not authorize unlimited spend or overriding a host-enforced limit.

## [autonomous loop] No-progress circuit breaker — into EACH ITERATION
- Keep a short window of criterion, target, failure signature, tested hypothesis and observed
  delta. Progress means a newly proved requirement, reduced reproducible failure, evidence that
  eliminates a cause and changes the plan, or confirmed delivery. Each must cite new evidence.
- Same command against improved inputs/results is valid work. Different commands, edits or
  paraphrased plans with no new evidence do not reset the no-progress streak. After two attempts
  at the same failure without evidenced progress, change approach or narrow the unit. A useful
  internal review threshold (for example three evaluated no-progress attempts) triggers a saved
  diagnosis and replan, not automatic goal termination. Only an explicit user stop policy makes
  that count a terminal no-progress condition. If no safe productive action exists, record the
  concrete blocker after considering necessary repairs under REMEDIATION SCOPE as productive
  work; do not keep replaying failed work or call a count-only halt success. Starting a repair
  alone is not evidence of progress; verify its effect or a new discriminating diagnosis.
- Count infrastructure retries/backoff separately; they neither prove progress nor reset the
  overall budget. Track oscillation by recurring failure and fix state, not plan wording.

## [recurring loop] Cross-run learnings
LEARNINGS FILE: .loop/learnings.md  (re-read at the START of every run, before the contract)
  Two sections: ## DURABLE (corroborated, applicable within this contract) and
  ## UNVERIFIED (candidate, read-not-obeyed).
- On any recurring failure, write the lesson to UNVERIFIED first, tagged with occurrence-count +
  an evidence pointer and applicability boundary. Promote only after a distinct corroborating
  occurrence or independent test verifies the lesson; rereading the same evidence is not
  corroboration. One atypical run may never mint a DURABLE rule.
- A learning may never rewrite a SUCCESS CRITERION / gate / stop condition (human edit only).
- Prefer category-level prevention (a DURABLE rule folded into lint/AGENTS.md) over a single
  regression case.

## [unattended or requested · closed only] Handoff summary — fold into STATE, VERIFY and ON STOP
HANDOFF LOCATION: <exact state path and existing summary section/field>.
DELIVERY CRITERION: <bound handoff criterion ID in SUCCESS CRITERIA and EVIDENCE MAP>.
This summary is time-of-day independent. Reuse the bound existing section/field, including legacy
names; do not rename state or infer a morning deadline from the former "Morning handoff" label.
- The execution agent maintains one compact receiving summary in the user's language as part of
  existing state updates, not a separate ledger or a task for the human to transcribe. Use the
  bound format; preserve frontmatter, history, counters, deadlines, pending effects and other fields.
- After initial reconciliation and before new project work, identify the current run/attempt and
  mark the summary in progress. A previous run's success is not current delivery. Refresh after
  settled attempts/meaningful checkpoints and on every controlled exit (success, pause, budget,
  failure or cancellation). Keep the actual checkpoint time/timezone; no invented final timestamp.
- Include four short parts: (1) actual changes and artifact/diff pointers, explicitly no change
  when appropriate; (2) checks/reviews with results, evidence pointers and not-run/unknown items;
  (3) unmet original criteria, blockers and stop_reason; (4) the next concrete action or human
  decision, including where to resume without releasing a pause or resetting limits.
  Identify repo/worktree/branch, revision AND any uncommitted changes, run/attempt and update time
  from the ledger; mark unavailable identities unknown/not applicable, never invent them.
  Distinguish work verified, handoff saved, and native stop requested/confirmed/unknown.
- Before a normal completion claim, save then read back the summary from HANDOFF LOCATION;
  check its identity and content against current ledger/evidence and resolve the cited local
  artifacts. Missing, stale, unreadable or mismatched proof stays missing. Writing the summary
  alone is not proof of the project criteria, review approval, or a stopped native job.
- Include this delivery proof even when the project was already green or no changes were needed;
  reuse valid tests rather than rerunning them. A quiet escalation rule does not suppress this
  local summary. Reuse it for an escalation with required error/attempt context, not duplicate state.
- At a reached user/platform cap or requested pause, only bounded checkpoint/read-back/native-stop handling remains; do not
  restart tests, reviews or project work to improve the summary. Reserve room for this handling
  within existing limits; saving failure must not extend them or cause an endless report retry.
  Report failed/unknown delivery and the last confirmed saved checkpoint; never emit FINAL while
  required delivery is unproved. Preserve original unmet criteria even if the summary is ready.
- A crash can leave only the last durable checkpoint. On resume reconcile interrupted work first;
  do not relabel stale/in-flight evidence as final. No new database/schema, automatic notification,
  commit/push/upload or schedule is authorized by this block. Do not put secrets in the summary.

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
"verified_by": "<gate output>", "target": "<verified revision/input/environment>",
"evidence": "<artifact pointer>" }]. status -> "pass" only with valid criterion-specific proof;
done when all original criteria, mandatory reviews and delivery have current proof. Invalidate
affected entries after relevant changes, including external input changes without a source diff.

## [open only] Dedup/cursor block — fold into the OPEN core
- Edge-trigger suppression: keep a digest of the last fire in .loop/cursor.json; the same
  condition staying true must NOT re-fire — only a NEW occurrence (or post-cooldown) fires.
- Last-seen cursor: persist last id/timestamp/status so each tick computes "what is new".
- Idempotency key: real occurrence ID, not just entity ID. Preserve pending/unknown reactions and
  their receipt lookups separately from the read frontier; notify-only reactions need this too.

## [greenfield/early · closed only — suppressed when kind=open] Bootstrap block — prepend as ITERATION 0 (runs once)
ITERATION 0 — bootstrap the gate (run once, before the normal loop):
- Reserve and count this attempt before scaffolding; an interrupted bootstrap still consumes its
  slot. Resume existing artifacts instead of overwriting them or allocating the same attempt twice.
- Scaffold minimally: repo, package manager / project file, the stack's test runner — only
  what the SUCCESS CRITERIA require.
- Encode each SUCCESS CRITERION as a FAILING acceptance test; run and confirm RED.
- Commit scaffold + red tests. From here <test command> is the gate; the loop drives red -> green.

## [taxonomy] Extended STOP — replaces CORE "STOP WHEN" line; label every halt
STOP WHEN (label each halt with stop_reason in the log):
For closed work, apply these labels only when the CLOSED STOP WHEN condition actually holds.
An exhausted operation-level retry allowance is not whole-goal impasse while a productive
authorized repair/alternative remains. Overall user/platform limits and real incidents still bind.
- success              : all original criteria proved; K repeats only if explicitly requested
                         or required by a meaningful stability criterion
- no-progress          : explicit user stop policy reached, or no productive safe path after diagnosis; internal threshold alone means replan
- oscillation          : explicit user stop policy or diagnosed lack of a safe productive path; internal repeat threshold means change approach
- failure              : non-retryable error or failure-class retry allowance exhausted
- budget               : applicable user/platform iteration / wall-clock / token+cost limit reached
- escalate             : dead-end handed off to a human with full context  [unattended only]
- regression           : post-gate dropped a previously-passing check   [two-stage only]
- poisoned-baseline    : invalid harness/unexplained baseline failure                            [two-stage only]
- unrecoverable-harness: blank/empty/frozen observation                  [harness only]
- pinata               : crash                                           [harness only]
- scope-boundary       : would touch an off-limits area / exceeds turn cap [invariants only]
