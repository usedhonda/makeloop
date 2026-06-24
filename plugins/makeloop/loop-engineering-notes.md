# Loop-engineering notes

Design record for `/makeloop`'s generated prompts: the technique catalog, which were adopted
into the command, and what is deliberately deferred. It exists so the knowledge survives
across sessions and so contributors know *why* each block is shaped the way it is.

## Adopted (baseline — every generated loop)

- Five phases; three hearts (verify gate / state / stop); four-conditions test; maker≠checker;
  build order (prove manual → loop → schedule); cost per accepted change; Ralph Wiggum loop.
- **Re-anchor every iteration** — re-read GOAL + CRITERIA + RULES, not just state (drift fix).
- **Backpressure ladder** — order checks fastest→slowest, stop at first red.
- **Search before assuming**; **no fake done** (no stubs/TODOs as done, never weaken a check).
- **Feedback compression** — PASS = 1 line, FAIL = {expected/actual/fix}, no repeated failures.
- **Gate-will-be-gamed** (Goodhart) — holdouts, properties over self-written tests, spot-checks.

## Adopted (profile/directive-triggered optional blocks)

- Two-stage gate (pre/post, FREEZE on regression); observation-validity check; regression
  guard; budget (now incl. token+cost cap); extended stop taxonomy.
- **No-progress circuit breaker** — tool-call/plan hashing to detect a spin mechanically.
- **Cross-run learnings** — `.loop/learnings.md`, category-level prevention.
- **Escalation handoff** — context-rich handoff to a human inbox; escalate-as-success.
- **Scheduled-loop safety** — idempotency keys, external scheduler, tiered auto-approve,
  intent deny-list.
- **JSON done-ledger** — harder to casually fake than a markdown checklist.
- **LLM-as-judge hardening** — judge family ≠ maker family, coarse rubric, escalate
  low-confidence; property/metamorphic gates when example tests are the only oracle.
- **Maturity-adaptive** — DISCOVER judges greenfield → scaffolded → mature from the files;
  greenfield gets a **Bootstrap block** (iteration 0 scaffolds + writes failing acceptance
  tests, then drives red → green) instead of being told a loop is the wrong tool.
- **Session-context aware** — DISCOVER reads the live conversation (intent) as a primary goal
  signal and reconciles it with the git/files (reality); leads the in-flight-work goal with it.
- **Output in the user's language** — the generated prompt + summaries render in the
  conversation's language, not English by default; only machine-significant literals stay as-is.

## Deferred (fleet / multi-loop orchestration — out of scope for the single-loop generator)

makeloop today generates **one** loop. The biggest unexplored area is fleet-level: multiple
cooperating loops that compound. Candidate future "fleet mode":

- Shared **signals** + global append-only work log as the cross-loop bus.
- Four trigger types (heartbeat / cron / hook / goal) instead of just self-paced/interval.
- Worktree-per-loop isolation + single-writer file ownership; sub-agent depth cap.
- Standing read-only **reviewer loop** that pre-filters the human queue; risk-sorted PR triage.
- Structured spans / deterministic replay (run_id) / independent pre-action audit receipt.
- Shadow mode → competence-based autonomy promotion (HITL → HOTL → autonomous) with
  numeric promotion thresholds and demotion triggers.
- WIP limit tied to human review capacity (3–5 concurrent).
