# Claude Code launch surface

Read for Step 4/6 on Claude Code only. Contract generation is not execution or permission setup.
Use observed host capabilities, not a version number alone. Keep unavailable or unconfirmed
commands in Conditional options without runnable fences.
Confirm optional ralph-loop through the actual exposed Skill/command list, not just a package name. A normal one-iteration message is the
portable first-run alternative. Honor the requested runtime when available.

| Need | Candidate | Behavior and limits |
| --- | --- | --- |
| Inspect one iteration | Normal message referencing saved prompt + state | Returns after one iteration; no scheduler/goal created |
| Complete a measurable closed goal | `/goal` | Cross-turn pursuit, fresh evaluator; goal does not change permissions |
| Wait/poll during this session | `/loop` with dynamic or fixed cadence | Wakes between turns, not a zero-delay while-loop |
| Existing ralph-loop workflow | `/ralph-loop` when installed | Uses installed plugin's cap/promise syntax |

For a safe first run, recommend one iteration. When the user explicitly wants closed completion,
prefer the available `/goal` option. For a cadence watcher, prefer the available `/loop <interval>`.
Do not stack goal, loop, Stop-hook runner and external cron for the same contract. Check for an
active goal before offering a launch that would replace it. Explain replacement, never do it here.

## Launch forms

Fill real values in the user's language; examples here are scaffolds, not executable output.

- Manual: “Follow .loop/repair.md for exactly one iteration; update .loop/repair-state.md;
  report FINAL only when every criterion is proved, otherwise ITERATING.”
- Closed continuation: `/goal Follow .loop/repair.md to complete its acceptance criteria;
  preserve .loop/repair-state.md and its cumulative budget; report evidence and unmet criteria.`
- Watcher: `/loop 5m Follow .loop/deploy-watch.md for one tick; update
  .loop/deploy-watch.cursor.json; react only to new events under the saved permissions.`
- Ralph: use the installed plugin's verified invocation, with `--max-iterations N` and
  `--completion-promise '<promise>DONE</promise>'` when that syntax is supported.

The saved contract carries the host-specific stop instructions below, not merely the launch line.

## Stop, evaluate, resume

- FINAL is a report marker, not a native scheduler stop token. Separate contract success,
  native goal achieved, cancelled job, and exited process in state and reports.
- `/goal`'s evaluator reads surfaced conversation; it does not independently inspect files or
  run checks. Native evaluation supplements objective evidence and any required independent
  review, not replaces them. It can clear a goal as impossible or after an unrecoverable error;
  neither is success. A new agent/checker still needs explicit delegation authorization.
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
turns. The final package must be a tool-free final text turn: explanations, chosen Loop body,
then launch blocks last. Do not mix a launch with a tool call or run a saving/checking tool
after it. Text between tools is visible to the user and is not the final deliverable.
Allowed-tools entries expose capabilities; they do not authorize spawning agents. Honor the
user's chosen interaction style rather than imposing a question UI.
