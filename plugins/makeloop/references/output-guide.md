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
When a requested runtime is confirmed available, it is the selected/recommended mode, not merely
an alternative. In particular, a CI/external-resume request must not silently become manual-first;
manual can be an optional inspection card, not a replacement recommendation. If the requested mode
is unavailable, keep it recorded as requested/unconfigured and explain the usable alternative.

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

## Final-only output: explanation, contract, launches last

Do not show launch commands or the full Loop body in commentary, progress messages, proposals,
question rounds or before saving/checking is complete. Explain purpose choices when needed, but
hold executable text until the final deliverable. The user must not have to hunt through the
conversation to find the latest launch. Earlier copy-first guidance is superseded by this rule.

After resolving material questions, saving files and completing assembly checks, send ONE final
package in this order:

1. Explanations and a concrete **Loop brief**: purpose, closed/open reason, actual actions,
   scope/effects, check/trigger, stop/cap/expiry, state and next/resume behavior. Add a short
   **How it stops / 今回の止め方** sentence: verified completion (or the watcher's exit), the
   requested pause if any, the actual limits, and what is saved/how to resume. No new pause menu;
   do not imply a pause is completion or promise native stopping without confirmed support.
2. Explained candidate cards. For Codex, use **Codex run options**. Mark exactly one choice as
   recommended; distinguish different purposes from ways to run the same accepted contract.
3. Saved paths, assumptions/gaps, and truthful status: **contract generated; continuation/schedule
   not configured; not started**. Put caveats, cost notes and all closing prose HERE, not after commands.
4. **Loop contract / Loop本文**: show the complete chosen saved contract once in a `markdown` fence,
   so the user can inspect or copy the body. Use the saved content checked before the final response,
   not a newly reconstructed variant. Do not print unchosen-purpose executable contracts.
5. **Launch commands / 起動コマンド**, at the very end: one fully resolved independent block per
   confirmed runnable choice, with host/paste destination and the candidate name immediately above.
   Keep unconfirmed options in the earlier explanation; they have no launch fence.

After the last launch fence, output nothing: no summary, warning, file links, cost note, question,
metrics or repeated assumptions. Do not repeat a launch under its earlier candidate explanation.
Long criteria/source inventories remain in the saved contract; showing that contract once in the
final package does not authorize executing it or creating schedules.

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
