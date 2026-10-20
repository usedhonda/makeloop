# Codex launch surface

Read for Step 4/6 on Codex only. Use native capabilities actually exposed in this session.
Official documentation or an installed CLI version alone does not establish session availability.
Unconfirmed/unavailable features belong in Conditional options without runnable copy fences.
The portable default is a normal Codex message for one iteration or watcher tick.

| Need | Candidate | Explanation |
| --- | --- | --- |
| Try one bounded iteration | Manual tick | First inspect the changes and evidence; returns control after one iteration |
| Pursue a closed goal across turns | `/goal` if available | Same contract/state and objective; no permission expansion |
| Revisit a watcher in the same chat | Chat scheduled task if available | Uses this chat's context; setup is distinct from one tick |
| Independent background observations | Project/standalone scheduled task if available | Explain local directory versus isolated worktree and state visibility |
| CI/external scheduler | `codex exec resume` | Bind the exact session and working directory; no runner is created |

Recommend one iteration for a safe first run. Preserve an explicit goal/cadence/CI choice rather
than forcing manual mode. A confirmed explicit CI/external-resume choice remains selected and
recommended in the contract, INDEX and final launch group; manual is only an optional alternative. Describe the purpose, behavior, effects, check, stop and resume for each
candidate using the shared output guide. No fake `/loop`, `/ralph-loop` or `codex-loop` commands.

## Launch forms

Render with actual paths and values in the user's language; these are illustrative scaffolds.

- Closed manual message: “Follow .loop/repair.md for exactly one iteration. Read and update
  .loop/repair-state.md. If all criteria are proved, report FINAL; otherwise ITERATING.”
- Open manual message: “Follow .loop/deploy-watch.md for one watcher tick. Preserve and update
  .loop/deploy-watch.cursor.json; react once per new event under the saved permissions.”
- Goal: `/goal Follow .loop/repair.md until every criterion is proved or its cumulative budget/
  terminal blocker requires an incomplete checkpoint. Preserve scope, evidence, consumed attempts
  and remaining work in .loop/repair-state.md; distinguish successful completion from stopping
  this execution incomplete.` Bind actual limits and stop conditions in the generated launch.
- Chat schedule setup message: “Create a scheduled task in this chat, every five minutes,
  running one tick of .loop/deploy-watch.md with .loop/deploy-watch.cursor.json; observe only
  new events and stop under the contract's conditions.” Label it **schedule setup**, not a tick.

For external orchestration, show a shell command only when the request mentions CI/cron/wrapper
and the exact existing session ID and working directory are known. Verify installed help before
selecting flags. Use `codex exec resume SESSION_ID PROMPT` with real resolved arguments, proper
shell quoting, and explicit working-directory binding. Do not use `--last` for an unattended loop:
the most recent conversation can belong to another purpose. If the ID is unknown, explain what
is missing; provide a manual message instead of a runnable guessed ID. JSONL/output-schema options
are optional integration aids, not a new runner or proof of task success.

## Continuation and scheduling boundaries

- Generated contract, configured goal/schedule, started run and finished run are different states.
  FINAL/ITERATING are contract reports, not proof of native achieved/cancelled/exited state.
- Keep one continuation owner. Do not combine native goal, a chat timer and an external cron for
  the same state. A goal launch can replace an existing objective; expose that conflict first.
- Before resuming, reconcile exact session, repo/worktree, original goal and contract version,
  state/cursor, cumulative counters, run handle/generation/owner, cancellation and surviving work.
  Do not reset state or resend an uncertain external effect. One writer; preserve unknown locks.
- A local/worktree scheduled task needs accessible saved files in that execution context. Desktop
  local tasks need the host/app available. Web scheduled tasks cannot read a local folder simply
  because its path appears in a prompt. CLI/IDE alone do not provide Scheduled management UI.
- Only offer a runnable schedule setup when the tool/surface and required files are reachable.
  Explain where results appear and what is not yet configured. Do not create it from a request
  merely to generate a loop. Explicit authorization in the same request is sufficient; do not
  invent a mandatory second request, but do not expand this generator into a runner.
- Budget exhaustion is an incomplete checkpoint, not success. Keep required native status
  transitions separate from observed blockers; do not manufacture turns to satisfy thresholds.
  Record a blocker immediately, continue independent authorized work, and report unsupported
  capabilities honestly. Native completion/evaluation never substitutes for criterion evidence.
