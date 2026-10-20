# Purpose-led choices and copyable output

Use this guide in Steps 2 and 6. Generate contracts; do not start project work.

## Choose the purpose before the mechanism

When the purpose is unclear, offer 2-3 concrete, project-grounded goals: for example, repair
the current failing suite, finish the next milestone, or watch for new CI failures. Explain
what each includes and excludes. A watcher is not a substitute for repairing today's failure.
Do not create executable contracts or initialize state for unselected purposes. Wait for the
purpose choice when material; minimal-interaction requests may use the stated, capped closed
interpretation. If the request explicitly asks to compare, preserve the comparison.

When the purpose is clear, keep it fixed. Offer execution alternatives for that same contract:
one iteration, native goal continuation, or a supported scheduled watcher. Do not invent extra
goals or expand scope to fill a menu. Normally show one recommendation and 1-2 meaningful
alternatives (at most four total when useful); one appropriate choice is better than padding.
Explicit runtime, cap, gate and safety decisions override defaults without a second confirmation.

## Explain every candidate

Use purpose-led titles such as “Finish the repair”, “Try one iteration”, “Watch new failures”,
not just tool names. Each card must explain, concretely for this project:

- outcome and when to choose it;
- what happens per iteration/tick, whether it edits or only observes/notifies, and its scope;
- when another choice fits better;
- exact verification or trigger, stop/cap/expiry, and what an incomplete checkpoint means;
- saved contract and state/cursor, how to continue, and whether it shares state with another card;
- permission, host/session, local/worktree and unattended constraints that affect the choice;
- known cost/runtime only when measured; otherwise say unmeasured.

Give enough explanation to make the choice, usually a short paragraph plus concrete bullets.
Do not compress differences into generic “safe / advanced” labels or bury them in a tool menu.

## Output order after the purpose is settled

1. One short recommendation label naming the host and **paste destination**.
2. The recommended complete launch block, before lengthy explanations.
3. A concrete **Loop brief**: purpose, closed/open reason, check/trigger, state and stop/next outcome.
4. Candidate cards explaining the recommendation and meaningful alternatives. For Codex, group
   these under **Codex run options**. Mark exactly one recommendation across the response.
5. Saved paths, assumptions, and status: **contract generated; continuation/schedule not configured;
   not started**. Report an existing run only with its real observed handle/status.

Do not dump the full assembled prompt into chat unless requested; the saved file is the full
contract. Long criteria, source inventories and instructions belong there, not in the launch line.

## Copy contract

- One independently usable launch per fenced `text` block (conversation input) or `sh` block
  (terminal). Label the host, destination and execution unit immediately outside the fence.
- Inside: only what to paste. No bullets, shell `$` prompt, wrapping display quotes, explanatory
  comments, other candidates or mixed shell/chat commands. Preserve syntactically required quotes,
  including around shell paths with spaces. Use the user's language, not smart-quote shell syntax.
- Resolve actual slug, paths, interval and session ID. Do not emit runnable placeholders.
- A capability documented but unconfirmed/unavailable in this session belongs in a separate
  **Conditional options** explanation, not an executable copy fence. Offer a verified alternative.
- For schedule setup, label **creates a schedule**, not “starts one tick”. Generating its setup
  message does not create it. Do not create a runner or schedule without explicit authorization.
- Two launch alternatives can reference the same contract/state, but only one may write it at a
  time. Explain switching after the earlier run has stopped; never suggest concurrent launches.
- Do not overwrite existing state/cursor, choose a purpose, set an INDEX selection or replace an
  active native goal merely because alternatives were displayed.

## Example differences (not fixed presets)

“Finish the repair” keeps pursuing the accepted failing-case criteria using native continuation.
“Try one iteration” uses the same criteria/state but returns control after one bounded iteration;
it can include an edit and is not a read-only diagnosis. It reports remaining work, not fake success.
“Watch new CI failures” is a different open purpose, with new-event dedup and an explicit reaction
boundary; it does not fix current failures unless authorized. Derive actual cards from the request.
