# Design the feedback, then the repetition

Read in Step 3 for fresh closed contracts and watchers, and use the relevant checks in Step 6.
For a narrow refine, inspect only the part affected by the requested change. Keep the existing
goal, authority and state. This guide designs a contract; it does not introduce a runner.

Loop engineering connects a goal to observations that change the next decision. Design the unit
of work, the evidence it produces, the response to that evidence, and the state needed to resume.
A scheduler supplies another opportunity to act; the contract supplies the decision about what
that opportunity is for. Ship the smallest version that closes this feedback path.

## Closed work: make the next decision depend on evidence

Before assembly, resolve these five items from the request and Project Profile:

| Item | Bind to this project |
| --- | --- |
| Outcome | Original goal, explicit non-goals, stable criterion IDs and required delivery/review |
| Observation | For each criterion: check, valid target/input, pass rule, evidence location and what invalidates it |
| Action | Smallest useful change or experiment, the criterion it serves, and the expected observable result |
| Feedback | What constitutes progress; when to retain a change, investigate, change approach, or stop |
| Continuity | One owner, attempt reservation, compact current state, evidence pointers and exact resume/stop behavior |

Write the criterion-to-evidence mapping into the saved contract, not only the generation chat.
Tests that all pass while a requested outcome has no check leave an acceptance gap. Verify the
observation itself: the intended source was read, required tests were collected, and the check
applies to the current target. A valid zero-violation result can pass; an undiscovered mandatory
suite or unreadable source cannot. Mark missing proof explicitly without changing the criteria.

**Check a new or changed verifier.** Explain why a representative acceptable outcome passes and a
plausible wrong or partial outcome fails, using existing fixtures or reference examples when
available. Successful execution and complete collection do not establish that the check measures
the criterion. Put needed calibration into the contract; do not execute it during generation.
For judgment-based review, bind a concrete rubric to inspected evidence; unobserved dimensions
remain unknown. A different checker or model family alone does not establish grading quality.
Diagnose disputed grades against the original requirement without relaxing its acceptance rule.

Plan one useful step ahead. Choose a small change when the cause is known; choose a discriminating
experiment when it is not. Before acting, state the expected observable result. Afterwards,
compare it with the actual result and use the difference to select the next step. A disproved
hypothesis can be useful progress when new evidence rules out a cause and changes the plan.

**Measure progress through evidence.** Use newly proved criteria, a reduced reproducible failure,
an eliminated cause, or confirmed delivery. Identify which observation demonstrates the change.
Do not count changed lines, commits, tool calls, paraphrased plans or a repeated assertion of
learning. Re-running the same test against an improved target is normal. Changing command text
while reproducing the same state is not progress. A finite diagnostic branch may advance once;
restating it cannot keep resetting the streak.

**Make adaptation bounded.** Track a short window of criterion + failure signature + attempted
approach + observed delta. After two attempts at the same failure without evidenced progress,
narrow the failing unit or change the hypothesis/check. An internal review threshold (for example,
three evaluated no-progress attempts) triggers a saved diagnosis and replan, not count-only
termination. An explicit user stop policy remains binding. If no productive safe action exists,
record the concrete blocker and resume condition rather than repeating failed work.
Record retryable infrastructure
errors and wait/backoff separately; neither creates progress nor resets the cumulative budget.
Count a recurring failure after a reverted fix as oscillation even when the wording changes.

**Reconcile the whole goal after each useful result.** A cleared plan or a review with no findings
is evidence about that plan/review. Before completion, inspect all original criteria, required
delivery and uncovered behavior. Admit a next task only when it addresses an unmet criterion,
repairs a caused regression, or obtains missing proof. Prioritize by impact and dependencies.
Once all original criteria and required reviews have current proof, finish. Unrelated improvements
belong in a separate proposal; they do not extend this loop's goal or budget.

## Keep state useful through interruption

Use the existing state format; do not install a database or migrate files merely for these fields.
Keep a compact current summary (goal/version, criteria/evidence, cumulative attempts, pending work,
recent failed approaches, selected next step, owner and stop status). For each limit/checkpoint,
retain value/unit, source (user/platform/agent-default), evidence and enforcement. Investigate
unknown provenance from original instructions/state; do not silently discard a real limit. Append terse attempt records
with evidence pointers; keep full tool logs outside the repeatedly loaded summary.

An attempt is one meaningful plan/action/evidence/decision cycle, not each command.
Reserve the attempt ID and increment cumulative consumption **before** its first action, including
a baseline check or bootstrap. Mark it running, then settle its outcome. An interrupted attempt
stays consumed. On resume, reconcile actual work and any uncertain effects before taking another
slot; do not repeat the action merely because its completion record is absent. At an applicable
user/platform limit, stop
new project work while still reconciling existing results, reporting and stopping the exact native
run. Agent-default review counts instead trigger internal replanning with history intact; do not
request another batch merely to extend that horizon. This is not unlimited-spend permission.
Persist each state update atomically when possible. Prose budgets are not hard host limits.

Define distinct decisions: continue (evidence supports the next action), change approach (stalled),
wait (known external condition), complete (all original requirements proved), and incomplete stop
(budget, cancellation or blocker). Record the concrete reason and resume condition. Only completion
emits FINAL. A native goal condition must also permit the declared incomplete terminal checkpoints;
stopping that execution must never be reported as achieving the project goal.

## Watchers: preserve event identity and effect outcomes

Bind the observable source, valid-reading conditions, occurrence identity, trigger, permitted
reaction, acknowledgement lookup and cancellation. Distinguish an entity ID from an occurrence ID:
two crashes of one worker are two events. Use a real source event ID or a persisted transition
generation (recovery followed by another failure); never invent a field the source does not expose.

Keep `last_seen` as the read frontier and `last_fired_digest` as confirmed dedup state. Preserve
unsettled events separately. Before a notification or action, save the occurrence key and intended
effect as pending. Afterward, record confirmed, definite failure, or unknown with receipt/evidence.
Advance the read frontier only once every observed event is durably represented or intentionally
ignored; advancing it must not discard pending work. Stop-on-event requires confirmed reaction.

On restart or timeout, reconcile pending/unknown effects through a receipt or authoritative state.
Do not blindly resend or mark them handled. A definite failure remains pending for bounded retry
within the same authority, selected independently of the read frontier. An unknown result without
a lookup stays blocked with a local handoff. Independent observations may continue. A key prevents duplicate effects only
if the destination enforces it; never promise exactly-once delivery from a cursor file alone.

Failed/partial observation is not an empty healthy tick: retain the previous frontier and report
the observation gap. Apply the cold-start/backlog policy only on the first valid observation, not
on every process restart. Bound retained receipts to the source's documented replay/retry horizon;
do not prune unresolved events or turn an old replay into a new occurrence.

## Check the design before saving

Walk a short concrete trace appropriate to the task: already satisfied; a real repair; repeated
failure; interruption before result recording. For a watcher, include the same event twice, a new
event on the same entity, and an acknowledgement lost after the reaction. State the resulting next
action and state transition. Repair any contradiction in the generated contract before delivering.
Do not execute the project or its launch commands for this assembly check.

Measure efficiency only when data exists: elapsed time and actual spend per accepted outcome,
including failed attempts and review. Gate duration estimates describe the gate portion, not total
wall time. Keep unmeasured values unknown; no universal acceptance-rate threshold decides value.

## Maintain the smallest effective contract

Each optional scaffold should address a concrete project need or observed failure. When the model,
host or tools change, reconsider inherited decomposition, reviewer cadence and context-management
workarounds. A historical workaround is a hypothesis about a limitation, not a permanent requirement.
Preserve explicitly required review, acceptance, authority and state; do not remove those controls
under the name of simplification. Narrow refinements still preserve unrelated contract choices.

For a generator change, compare one optional component at a time on representative cases, keeping
acceptance and authority fixed. Read the actual trace to distinguish a generator defect, a bad
grader and a host/tool failure. Record the checked model/host, capabilities, input/state and source
revision when available. Assembly examples and decision simulations establish only the behavior
they exercise; standalone scores do not prove behavior in the deployed Claude Code or Codex host.
Repeat model runs only to resolve observed variability or a declared reliability requirement,
never to select a lucky pass. Preserve failures as evidence and compare cost per accepted outcome.
