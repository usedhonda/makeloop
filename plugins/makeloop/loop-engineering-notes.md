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
- **Goal-fit guidance** — bias candidates toward loop-appropriate work (CI triage, dep bumps,
  lint-fix, flaky repro, suite-green); steer off loop-hostile goals (architecture, auth/
  payments, prod deploy, vague) → recommend a single guided prompt instead.
- **Independent completion check** (`/goal` pattern) — a separate model confirms the goal is
  met (not just the gate) when "done" can't be fully reduced to the gate.
- **Security tax** for unattended loops — security checks in the gate (secret scan / dep audit
  / SAST), human approval before irreversible actions, log hygiene, skill/connector source
  audit, periodic permission re-audit.
- **Ready-to-paste launch line** — Step 6 leads with the exact command the user runs, in
  file-reference form (`/loop <saved file> の手順に従って…`) so the loop re-reads its contract
  each iteration instead of pasting the whole prompt; saved files use a descriptive slug
  (`.loop/<slug>.md`) so multiple loops don't clobber each other.
- **Loop kind: closed vs open** — DISCOVER classifies closed (drive-to-done: goal + verify
  gate + FINAL) vs open (watch/react: WATCH TARGET + TRIGGER CONDITION + observe→evaluate→
  notify/act + dedup/cursor, no FINAL). Decided by goal verb + the decisive test ("can a
  SUCCESS CRITERION become permanently true and END the loop?"); default closed on ambiguity
  (open→runs-forever is the costlier misclassification). The wrong-tool warning is suppressed
  for open watchers. Deliberately NOT added: a trigger sub-taxonomy (heartbeat/cron/hook) and
  a second full skeleton — one skeleton, kind-conditional middle; shared blocks stay DRY.

## Adopted — Round 1 community harvest (2026-06-24)

Surfaced by the sources-harvest loop and wired in after review:
- **Iteration economics / wide-not-deep** — size the cap from diminishing returns (gain ≈50%
  round 1, ≈25% round 2; ~5-6 cap); past the ceiling, re-touching validated code regresses;
  when quality plateaus add more verifier *types*, not more iterations.
- **Re-verify the diff, not the world** — iter 1 checks all; later iters re-check only the
  changed surface.
- **Dual-verifier AND-gate** — pair an LLM-judge with a deterministic assertion; done only if
  both pass; route the failing check into the retry.
- **Failure-class retry** — rate-limit→backoff; validation→rewrite-from-feedback; 5xx→retry
  then move on; tool-unavailable→pause+notify.
- **UI drive-and-capture** — for UI/web, verify by exercising the feature + capturing a
  screenshot/GIF as proof-of-use (and PR evidence).
Held in the local catalog (not wired — too niche/fleet for the generic generator): formal-spec
(TLA+) as driver, self-instrumentation feedback, opportunity-object ranker, behavioral
circuit breaker [D], toxic-flow simulation [D].

Round 2 (confirmation, decay 11→5, harvest loop closed at near-saturation) — wired 2:
- **Shrink-the-unit on repeat failure** — retry → decompose to the smallest failing fragment →
  escalate (a middle gear between blind retry and abort).
- **Repo-grounded rubric + anti-cheat/blast-radius axes** — the LLM-judge reads the repo before
  scoring and carries an explicit anti-cheating axis (test-weakening / mass-rename / dep-churn)
  and a blast-radius axis.
Held in catalog: pre-code ambiguity gate (restates existing goal/criteria confirmation),
weighted-drift→auto-retrospective [thin], oracle-gap adaptive test hardening [thin/eval-rig].

## Adopted — convenience hardening (2026-06-25)

A maintainer-driven pass (multi-angle community harvest + cross-source ideation, deduped vs the
catalog at near-saturation) that HARDENS machinery the generator already ships rather than adding
scope. All seven are additive / generation-time-only; the golden eval stayed 10/10 green
(maker≠checker) and the deterministic gate passed on each.

Generated-loop content (CORE/OPTIONAL blocks):
- **Typed verify status (empty-but-valid)** — a check that runs cleanly and returns nothing
  (empty grep / zero diff / no-op build) is a real PASS, not a retry trigger; only a true error
  re-enters the retry ladder. Plugs a silent token-burn where empty success read as "try harder".
- **Learnings poisoning guard** — `.loop/learnings.md` splits into DURABLE (corroborated, obeyed)
  and UNVERIFIED (candidate, read-not-obeyed); a lesson promotes only on a 2nd occurrence or an
  independent pass, and may never rewrite a criterion/gate/stop condition. Stops one atypical run
  from minting a rule the loop then obeys forever.

Generator behavior (Steps):
- **Pre-save self-check** — Step 6 opens with an assembly lint (no leftover `<...>`, exactly one
  CORE, no cross-kind block leak, kind-consistent structure, launch line + state/cursor filenames
  correct) and a confirm-gated, advisory gate smoke-test (closed + deterministic gate only: does
  the command resolve? is the baseline green or a poisoned RED?). Catches per-run output defects
  the golden eval's fixed scenarios can't.
- **One-confirm default** — after DISCOVER, propose the whole loop (kind + goal + criteria/trigger
  + gate + cap + runtime) and confirm in ONE question; branch to the granular per-step questions
  only on genuine high-impact ambiguity (closed-vs-open, destructive gate, judgment-call success).
  ~4 round-trips → 1, with the fail-safe fallback preserved.
- **Refine mode** — a request naming an existing `.loop/<slug>.md` (or "tweak/adjust the X loop")
  applies just the requested delta and re-saves under the same slug, skipping DISCOVER + the
  question rounds; falls through to a normal build if the loop doesn't exist.
- **Repo loop registry** — list existing `.loop/*.md` at invocation (refresh/extend vs new), and
  append one row per generated loop to `.loop/INDEX.md` so a repo's loops stay listable.

Held (not wired): falsifiable-prediction-per-edit (no automated cron edits yet to falsify),
context-hygiene handoff (enforcement is runtime — a prompt can only advise), preset archetypes
(would short-circuit the deep-discovery that is makeloop's value — only ever a DISCOVER bias).

## Self-improvement system (auto-strengthening — LIVE via the every-2-days cron)

makeloop can strengthen itself by harvesting community knowledge and wiring what earns its
weight. The machinery (built and running unattended every 2 days):
- **Golden eval** (`eval/scenarios.md`) — the objective quality gate ("still good", beyond the
  lint's "not broken"): regenerate loops for fixed scenarios, check the output's properties.
- **Governance contract** (`SELF-IMPROVEMENT.md`, the fixed trust anchor) — autonomy tiers
  (0 data / 1 additive-auto / 2 behavior-human-GO / 3 contract-human-only), the **monotonicity
  invariant** (auto-edits may only add/strengthen, never weaken a gate), the **fit-critic
  rubric** (earns-weight, default-reject), the **prune mandate** (strengthen+prune homeostasis),
  and what stays read-only/out-of-loop.
- **Self-improve open loop** (`.loop/self-improve.md`, local) — harvest → dedup → fit-critic →
  propose diff → eval-gate → Tier1 auto-apply / Tier2 escalate / Tier3 never → prune every 3
  cycles. Run-indefinitely. The contract + eval are read-only anchors it cannot edit.
- **Deterministic gate** (`.githooks/gate.sh`) — the code (not prose) that makes Tier 1 real
  automation: mechanically checks guarded phrases intact, no gate-bypass clause added, anchor
  untouched, JSON/structure/leak/eval. Behind the anchor (deny + pre-commit + chmod). Red-team
  hardened (C1 firewall, C2 behavioral monotonicity, C3 out-of-band enforcement, H1 exfil
  allow-list, H2 critic independence, M1 fresh-context apply, M2 guarded-phrase integrity).
- **H1/H2 now code-enforced (toward zero-human Tier 1):** H1 — `.claude/settings.json` denies
  the outbound MCP tools (Gmail/Drive/Calendar) + secret-read globs (`.env`/`*credential*`/
  `id_rsa*`); WebFetch is GET-only and gate.sh blocks committing secrets to public files. H2 —
  the fit-critic runs as a 3-different-model panel (one a dedicated injection-hunter), with
  corroboration counted by independent operator-trusted domains, not text agreement. Editing the
  anchor to add the H1 deny required an explicit human chmod (the auto-mode classifier blocked
  the agent from un-protecting it on a generic "GO" — the design working as intended).

## Automation (the every-2-days self-improvement cron)

The self-improvement loop runs unattended via local cron every 2 days → wrapper
(`.loop/self-improve-run.sh`) → one headless `claude` cycle → Tier-1 auto-apply on
`gate.sh` PASS. Operator runbook (pause/resume/monitor/install, first-watched-run, undo) is in
[`AUTOMATION.md`](AUTOMATION.md). Pause = `touch .loop/PAUSED`; log = `.loop/cron.log`; bot
commits authored `makeloop-selfimprove`. Fresh clones ship PAUSED; enable with `rm .loop/PAUSED`
after one watched run.

## Self-improvement run history

A public trail of what the self-improvement loop changed, when, and in which commit — the companion
to `git log --author=makeloop-selfimprove` (richer per-commit detail) and `.loop/cron.log` (local
raw log, gitignored). The loop appends ONE line here after any run that changed a public file.
**Allowed fields only (H1): date, commit SHA, Tier, changed public files, change class, gate result,
round/prune — NEVER source URLs, authors, fetched text, secrets, or `.local/` contents.**

Format: `- <date> <SHA> [Tier-N] <changed public files> — <change class> · gate:PASS · <round|prune|manual>`

Setup history (manual — built by hand before going LIVE; see `git log` for full diffs):
- 2026-06-24 c1ef3d5 [manual] self-improvement system + red-team hardening (scaffold)
- 2026-06-24 d67283e [manual] deterministic safety gate (`.githooks/gate.sh`)
- 2026-06-24 54889a6 [manual] H1 code-enforced (`settings.json` deny: outbound MCP + secret globs)
- 2026-06-24 5bcf686 [manual] AUTOMATION.md operator runbook
- 2026-06-24 0095e2e [manual] auto-push to origin/main wired (decision A)
- 2026-06-24 6781153 [manual] reconcile auto-push with H1 / undo / deny-list
- 2026-06-25 e7e5ed2 [manual] enforcer bootstrap + README self-improvement section
- 2026-06-25 9f26017 [manual] cross-cutting RULES restored (golden-eval green)

Automated runs (`makeloop-selfimprove`): none yet — near-saturation, silent archives so far.

## Dogfood runs (does the generator earn its weight?)

Real runs of makeloop-*generated* loops, measured for accept + cost — the public, sanitized
"examples-as-benchmark" trail (raw ledger is local). Closed-loop metric = cost proxy per accepted
change; cost proxy falls back tokens → iterations → wall-clock when tokens aren't available.

| run | request | kind | profile | gate | iters | outcome |
|-----|---------|------|---------|------|-------|---------|
| df-001 | CSV→JSON CLI, tests green | closed | greenfield/empty (py) | `pytest -q` | 2 | accepted |
| df-002 | watch app.log, notify on ERROR | open | greenfield, notify-only | TRIGGER `/ERROR\|FATAL/` | 8 ticks | accepted |
| df-003 | mature lib, fix planted bug | closed | mature (py, existing pytest) | `pytest -q` | 1 | accepted |
| df-004 | watch crashed proc, auto-restart | open+acts | scaffolded, run-indefinitely | TRIGGER crash_id | 11 ticks | accepted |
| df-005 | disk-cleanup watcher (re-dogfood after fix) | open+acts | scaffolded | TRIGGER disk% | gen-check | accepted |
| df-006 | get the test suite green | closed | real-public, mature, gate already green | `pytest` | gen-check | accepted |
| df-007 | improve the docs | wrong-tool | real-public, mature, docs gate already green | n/a | n/a | accepted (wrong-tool) |

**df-004/005 residual eval-retired (2026-06-25, `a8dff5a`)** — the Scheduled-loop-safety
unbound-`<...>` weakness is now closed end-to-end: generator fix (bind-placeholders) →
generation-time pre-save assembly lint (the maker==checker floor) → golden-eval **S11** + a
cross-cutting no-unbound-placeholder check (the independent maker≠checker ceiling). The
recurring-candidate is mechanically retired, not just patched. (Anchor edit applied in a
human-authorized window; S11 verified gradeable + generator-passing before it landed.)

**Phase 2 Measure — first real-repo / non-author runs (2026-06-25, `wqo111shs`)** — df-006/007
used makeloop as a *non-author first-timer* on two real public repos (maker≠checker; graders
independently RAN the gates). Both: kind/maturity/block-selection + the wrong-tool call were
**correct** — generation is sound on real code, not just toys. The signal toy runs can't surface:
the **"already-green-at-generation / degenerate-loop" gap** — on a mature repo whose gate is
*already passing*, makeloop offers no off-ramp between "good closed loop" and "wrong tool"; a
closed loop on a green gate prints FINAL at iteration 0 (does nothing) or tempts fabricated work,
and the pre-save gate smoke-test *detects* already-green but is advisory-only with no decision
branch. Second signal (→ Phase 3 Prune): cold-start spec weight — the command is read-heavy
relative to its small product for a routine ask. **Per the framework these are RECORDED, not
patched**: an already-green off-ramp would add a new decision branch (fails the
immediate-exception gate), so it is a Phase 4 Decide candidate, not a reflexive fix.

- df-001: **Bootstrap fired correctly** — iter0 scaffolded + confirmed RED, iter1 drove green; `csv.DictReader` met all 4 criteria in one pass. cost/accepted = 2.
- df-002: **OPEN CORE correct** — no closed-only block leaked (grep 0); precision / dedup (edge-trigger) / coverage (truncation + file-gone) all PASS; wrong-tool warning suppressed per spec.
- df-003: **mature/closed correct** — NO Bootstrap, existing gate reused verbatim; surgical 1-line fix, tests untouched (no Goodhart). cost/accepted = 1. Minor: `scope-boundary` STOP label omitted though the boundary was encoded in SUCCESS CRITERIA + RULES.
- df-004: **open+acts correct** — Scheduled-loop safety + idempotency key + deny-list + escalation all wired; 21/21 sim checks. **Finding (recurring-candidate):** the Scheduled-loop-safety block ships as boilerplate with `<...>` placeholders — the safety *value* (idempotency key, allowed-action set) must be bound by the operator; pasted as-is it lists generic deny verbs without a project-bound authority check.

5/5 accepted across closed (greenfield + mature) and open (notify + acts) paths — the generator
classifies kind/maturity and selects blocks faithfully, with no cross-kind block leakage.

**Loop closed (first dogfood → improve → re-verify round):** the df-004 recurring-candidate
(Scheduled-loop safety shipped as raw `<...>` boilerplate with no project-bound authority check) was
fixed — a **Bind the placeholders** bullet added to `makeloop.md` Step 5 + the template (additive
+7 lines, 0 deletions). Re-dogfood **df-005** (open+acts, disk-cleanup watcher) confirms it: the
directive is present AND acted on — idempotency key, allowed-action set, and a concrete `./logs`-only
authority check are all project-bound (the exact thing df-004 lacked). Golden eval stayed **10/10
green**, no regression. Independently verified (maker≠checker + a judge agent: `loop_closed=true`).
Residual: to *mechanically* retire the candidate (vs. relying on operator diligence), graduate it to a
golden-eval scenario asserting "no unbound `<...>` in a Scheduled-loop-safety output" — that edits the
`eval/` anchor, so it needs a human `chmod` (out-of-loop). Volume still early (5 runs, target ~5-10).

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
