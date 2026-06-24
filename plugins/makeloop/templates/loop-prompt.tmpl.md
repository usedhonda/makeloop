<!--
makeloop loop-prompt template (canonical).

Structure: a CORE block that is ALWAYS present, plus OPTIONAL blocks that /makeloop
includes only when the Project Profile (DISCOVER step) triggers them. Ship the smallest
loop the project supports — do not paste a two-stage gate for a single `npm test`.

completion token: FINAL for built-in /loop (self-paced/interval); <promise>DONE</promise> for ralph-loop.
-->

# ============ CORE (always) ============

# LOOP: <short goal name>

GOAL: <one sentence, objective, checkable>. <runbook path if one exists>

SUCCESS CRITERIA (strict, no soft passes):
- <verifiable criterion 1>
- <criterion 2>
- <criterion 3 — include any hard invariant from profile D>

VERIFY — the gate (run these; never self-grade):
- <verify command 1, e.g. npm test>
- <verify command 2, e.g. npm run typecheck>
PASS = <exact pass condition, e.g. all tests green, 0 type errors, exit 0>

STATE FILE: .loop/state.md   (or existing state file from the project)
- Read it before starting. This is a resume, not a restart.
- Each iteration, append: what you did / what passed or failed / the single next step.

EACH ITERATION:
1. READ state, then run VERIFY to see the current failures.
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
- maker != checker: on risky changes, re-verify with fresh eyes / a sub-agent.
- Surgical changes only: every diff line must trace back to GOAL. <off-limits from profile D>
- Do not ask questions mid-loop. Make a sensible assumption, note it in state, continue.


# ============ OPTIONAL blocks (include per profile) ============

## [multi-stage verify] Two-stage gate — replaces CORE VERIFY
VERIFY — two-stage gate (never self-grade):
- pre-gate  (start of iteration): <build> && <full check>
- post-gate (after the fix):      <full check>
PASS = <full check green + baseline/regression audit shows 0 regression>
- pre-gate RED  -> HALT  (stop_reason=poisoned-baseline)
- post-gate drops a previously-passing check -> FREEZE, do NOT commit (stop_reason=regression)

## [self-driving harness] Observation-validity check — into EACH ITERATION after driving
- After driving the harness, validate the observation BEFORE trusting it:
  blank/baseline-identical screenshot, empty snapshot, or frozen run
  -> HALT (stop_reason=unrecoverable-harness). A crash -> HALT (stop_reason=pinata).

## [baseline/golden/scenarios] Regression-guard — into EACH ITERATION after the fix
- Add ONE minimal regression case (<scenarios path>/<name>) that asserts the violated
  invariant, tied to the root-cause fix. One fix + one guard per commit.

## [autonomous loop] Budget — under STATE FILE
BUDGET (write into state): iteration cap <N> / wall-clock <T> / no-progress streak <P> /
token+cost cap <C> (soft-pause + notify at 85%, hard stop at 100%).

## [autonomous loop] No-progress circuit breaker — into EACH ITERATION
- Hash {tool name + args} per action, keep a short window. Same action repeated (3rd
  identical, or >85% similar plan/action across iterations) -> stop_reason=no-progress.

## [recurring loop] Cross-run learnings
LEARNINGS FILE: .loop/learnings.md  (re-read at the START of every run, before the contract)
- On any recurring failure, write ONE durable rule. Prefer category-level prevention (a rule
  folded into lint/AGENTS.md) over a single regression case.

## [unattended/scheduled] Escalation handoff — replaces silent death on a dead-end
ON DEAD-END (failure / budget / unrecoverable-harness): write a context-rich handoff (what
was tried, last error, where it stopped, run_id) to <inbox: file / issue / channel>. A run
that found nothing archives itself quietly. Escalation-to-human is a success path.

## [unattended/scheduled] Scheduled-loop safety
- Idempotency: stamp each side-effecting apply with an idempotency key (node re-runs from its
  start on resume; duplicate effects must be impossible).
- Durable schedule: drive from an EXTERNAL scheduler (cron / CI / Actions, per-loop
  concurrency group, cancel-in-progress=false); in-process timers die on restart.
- Auto-approve (tiered): safe reads auto; in-repo writes auto (git-reviewable); shell /
  external / out-of-repo / subagent-spawn gated. Trust boundary = this repo only.
- Intent deny-list (judge real impact): no force-push / mass-delete / secret-exfil /
  disable-logging / push-to-main / prod-deploy without explicit human sign-off.

## [many discrete criteria] JSON done-ledger — replaces the markdown success checklist
DONE LEDGER: .loop/done.json = [{ "criterion": "...", "status": "pass|fail",
"verified_by": "<gate output>" }]. status -> "pass" only with a real verified_by; done when
all "pass". (Models rewrite JSON less casually than a markdown [x].)

## [greenfield/early] Bootstrap block — prepend as ITERATION 0 (runs once)
ITERATION 0 — bootstrap the gate (run once, before the normal loop):
- Scaffold minimally: repo, package manager / project file, the stack's test runner — only
  what the SUCCESS CRITERIA require.
- Encode each SUCCESS CRITERION as a FAILING acceptance test; run and confirm RED.
- Commit scaffold + red tests. From here <test command> is the gate; the loop drives red -> green.

## [taxonomy] Extended STOP — replaces CORE "STOP WHEN" line; label every halt
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
