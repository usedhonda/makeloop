# Claude Code launch surface

Read for Step 4/6 on Claude Code only. Contract generation is not execution or permission setup.
Use observed host capabilities, not a version number alone. Keep unavailable or unconfirmed
commands in Conditional options without runnable fences.
Confirm the intended target surface, not just tools visible to the generator: the target's
observed command menu/help, an explicit user report that `/goal` works there, or a supplied
host-bound capability profile can establish availability. Merely asking for Goal, a version
number, or generic documentation cannot. A slash command need not appear as a model tool.
Record the evidence in the contract; distinguish a fresh unstarted Goal from an unavailable one.
Confirm optional ralph-loop through the actual exposed Skill/command list, not just a package name.
Ordinary no-Goal execution can pursue successive necessary steps in the current execution; it is
not a one-iteration default or proof of cross-turn persistence. Honor the requested runtime when available.
If it is unavailable, preserve the requested continuation as unconfigured. A short single-pass
example is not equivalent to completing all residual work; do not choose it merely to shorten
the launch. Read saved contract/state; distinguish user/platform limits from internal review
thresholds and disclose actual remaining budget and required review.

| Need | Candidate | Behavior and limits |
| --- | --- | --- |
| Finish scoped work in the current execution | Normal message referencing saved contract | Pursues successive necessary steps; no native cross-turn setup |
| Explicitly inspect one iteration | Normal message referencing saved prompt + state | Returns after one iteration; no scheduler/goal created |
| Complete a measurable closed goal | `/goal` | Cross-turn pursuit, fresh evaluator; goal does not change permissions |
| Wait/poll during this session | `/loop` with dynamic or fixed cadence | Wakes between turns, not a zero-delay while-loop |
| Existing ralph-loop workflow | `/ralph-loop` when installed | Uses installed plugin's cap/promise syntax |

For closed completion work, include an available Goal-equipped launch in the initial proposal,
even if the user did not name a runtime; recommend it for requested looping/cross-turn pursuit.
Bind the existing Stop, evaluate, resume rules below during generation, including actual limits
and evidenced incomplete exits; unfinished assembly is not a reason to defer Goal as conditional.
Honor explicit no-Goal, bounded-pass or other supported runtime choices instead. A bounded single
pass is an explicit choice, not the default for completion or ordinary no-Goal execution. For a cadence watcher, prefer the available `/loop <interval>`.
Do not stack goal, loop, Stop-hook runner and external cron for the same contract. Check for an
active goal before offering a launch that would replace it. Explain replacement, never do it here.

## Final copy choices

Use the shared output guide: save/check first, then explanations, the saved contract path (full
body only on explicit request), and, for ready proposals only, one final launch group with A/B/C labels. Every chat block is `text`, pasted into **Claude Code input**,
not the operating-system terminal. For closed completion, include the confirmed Goal option from
the first proposal. When no other runtime is explicitly selected and both modes are ready,
pair recommended Goal completion with ordinary current-execution completion; both reference
the same contract/state and REMEDIATION SCOPE, never simultaneous writers. Ordinary execution
is not a replacement for requested cross-turn continuation. Explicit different runtime choices still win. If Goal really cannot
be confirmed, explain the specific missing evidence/control without a runnable Goal block;
do not silently omit a requested Goal. For an open watcher, offer one tick plus `/loop <interval>` when confirmed.
An installed Ralph option is an extra only when it is relevant, never an install recipe in the
launch group. Put the recommended choice first. `/loop` polling is not a zero-delay substitute
for closed goal continuation. Keep every alternative on the same accepted goal, state and limits;
its execution unit must be explicit. Emit slash launches as one physical line.

## Launch forms

Fill real values in the user's language; examples here are scaffolds, not executable output.

- Ordinary execution: “Follow .loop/repair.md through its required work and verification.” Bind
  provisional pending work, delivery/review and actual stop conditions in the saved contract.
- Explicit bounded pass: “Follow .loop/repair.md for exactly one iteration.” Keep the bound state, criteria,
  reporting and limits in that saved contract rather than duplicating them in the launch.
- Closed continuation: `/goal Follow .loop/repair.md, including necessary authorized prerequisite repair under its REMEDIATION SCOPE. End this run when (1) all acceptance
  criteria and the original outcome are proved with no unmet/unverified work, or (2) a saved
  incomplete checkpoint evidences an actual user/platform limit, or a surfaced remediation
  assessment proves no productive authorized repair/alternative or independent work remains,
  including only approval/other-owner waits such as required human review with the waiting party
  and condition surfaced after independent authorized work is exhausted. Preserve
  .loop/repair-state.md and report the evidence, cumulative counters and unmet criteria.
  Report FINAL only for acceptance success.`
- Watcher: `/loop 5m Follow .loop/deploy-watch.md for one tick; update
  .loop/deploy-watch.cursor.json; react only to new events under the saved permissions.`
- Ralph: use the installed plugin's verified invocation, with `--max-iterations N` and
  `--completion-promise 'DONE'` when that syntax is supported. The argument is the plain promise
  text; the completion output is `<promise>DONE</promise>`. Do not put the tags in the flag value.

The saved contract carries the host-specific stop instructions below, not merely the launch line.
For `/goal`, expand the contract's actual cumulative limits and terminal blocker conditions into
the emitted condition. An agent-default checkpoint is not a terminal limit. Do not invent a cap.
When a pause point is requested, include its evidenced checkpoint as another non-success exit in
that condition. Surface the remaining criteria, not a project-completion claim. On explicit resume,
release only that reached pause in the saved state and retain the original scope and limits.

## Stop, evaluate, resume

- FINAL is a report marker, not a native scheduler stop token. Separate contract success,
  native goal achieved, cancelled job, and exited process in state and reports.
- `/goal`'s evaluator reads surfaced conversation; it does not independently inspect files or
  run checks. Native evaluation supplements objective evidence and any required independent
  review, not replaces them. It can clear a goal as impossible or after an unrecoverable error;
  neither is success. A new agent/checker still needs explicit delegation authorization.
- Include both acceptance success and evidenced non-success terminal checkpoints in the native
  goal condition. A bare "only blockers remain" does not establish that exit: before stopping,
  surface the symptom, diagnosis, permitted repairs/alternatives tried or concrete reasons they
  cannot be attempted, remaining work, and the unblock condition in the conversation. The
  assessment must establish no productive authorized recovery or independent safe work remains.
  Necessary authorized repair is part of the original Goal; verify it, then return to the pending
  work without a fresh repair request. A prohibited repair need not be attempted. Approval or
  other-owner waits are terminal only after independent authorized work is exhausted.
  A budget/dead-end stop must not leave the evaluator instructed to continue
  until acceptance passes. Surface the check results, target, cumulative counters, stop reason,
  remaining work and checkpoint path in the conversation; a pointer to an unread file is not
  evidence for that evaluator. Native condition satisfaction can mean the run ended incompletely;
  keep project acceptance status separate and never print FINAL for that case.
  Explain `/goal clear` as the user's cancellation command for an active goal. If a terminal
  checkpoint leaves the goal active, report that status and the cancellation command rather than
  claiming it stopped. Showing the command does not execute it; do not invent a goal-control tool
  or change hook/permission settings to force an exit.
- Self-paced `/loop` chooses a delay (typically one minute to one hour). On completion or cap,
  explicitly stop its native wakeup (`ScheduleWakeup` with `stop: true` when exposed).
- Fixed intervals keep firing until cancelled or expired. Record the exact job ID; cancel that
  job with the native cancellation tool (such as `CronDelete`) at stop-on-event/cap/completion.
  Do not cancel unrelated schedules or claim FINAL cancelled anything.
  A fixed schedule is a cron cadence, not a guaranteed elapsed-time timer. Capture the host's
  confirmed cron/timezone/next fire; do not invent an immediate first tick or promise exact 24h
  spacing/number of runs. For “nightly”, resolve the intended wall-clock time before scheduling.
- Session loops have a seven-day expiry; “run-indefinitely” describes intent, not an uptime
  guarantee. Self-paced wakeups are not restored by session resume. Do not silently recreate an
  uncertain prior schedule. Record expiry and actual cancellation/restart status.
  This does NOT mean every schedule disappears: CronCreate tasks are restored on resume except
  expired recurring tasks and elapsed one-shots; background Bash/Monitor tasks are not restored.
  Never generalize the self-paced limitation to fixed scheduled tasks.
- Resumed native goals can reset native turn/time/spend counters. Keep the original goal version,
  accepted scope and cumulative budget in the file-backed ledger. Native and prompt limits are
  different mechanisms; do not promise a machine-enforced limit from prose alone.
- Before resuming, reconcile repo/worktree, goal version, state and real run/job handle,
  cancellation, generation/owner and surviving work. One writer per state. Unknown side effects
  require outcome reconciliation, not re-sending. Never delete an unknown lock or replace drafts.

Persistent cloud/Desktop scheduling is a separate deployment choice, not an automatic migration
of local `.loop/` files. Describe it only if requested; keep this generator free of new runners.

## Final text turn

Finish all Write/Bash operations, INDEX updates, saved-file checks and other tools in earlier
turns. The final package must be a tool-free final text turn: explanations, saved contract path
(full body only on explicit request), then launch blocks last. Do not mix a launch with a tool call or run a saving/checking tool
after it. Text between tools is visible to the user and is not the final deliverable.
`allowed-tools` pre-approves the listed tools for the invoking turn; it does not restrict the
available tool pool, and the grant clears on the next user message. A bare `Bash` entry grants
broad shell pre-approval rather than enforcing read-only discovery. Keep these grants separate
from the user's task scope and delegation authorization. Honor the user's chosen interaction
style rather than imposing a question UI.
