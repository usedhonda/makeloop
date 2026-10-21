# Project Profile (fresh generation only)

**Session context first (if any).** You are running inside a live session — read the
conversation so far as a *primary* signal for what the user is actually working on: the goal
they've been pursuing, what they just asked for, decisions already made, errors they hit,
files they touched. This often reveals the in-flight goal better than git does. Reconcile it
with the project state below — the **conversation tells you the intent, git/files tell you the
reality**; when they disagree, surface it. If there's no relevant history (fresh session, or
it was compacted away), say so and fall back to the project state.

Then investigate the working directory thoroughly and fill in the **Project Profile** below.
Use read-only commands only. Read only what changes the goal, gate or boundary decision. Use an `Explore`/`Agent`
subagent only when delegation is explicitly authorized and the tool is exposed; otherwise
collect evidence directly. Tool names and allowed-tools do not authorize delegation.

**A. Orientation**
- Git: `git status -s`, `git log --oneline -20`, `git diff --stat`, `git diff --stat HEAD`
  (in-flight + recent work). Note if not a repo.
- Project type, entry points, build & run commands (README, `package.json`,
  `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Package.swift`, etc.).

**B. Verification depth — this shapes the gate**
- Tests (unit/integration), typecheck, lint, build.
- Deeper checks: grep for `baseline`, `golden`, `snapshot`, `regression`, `parity`,
  `--audit`, `invariant`, `--drive-all`, e2e suites.
- Decide: is verification **single-stage** (one test command) or **multi-stage**
  (e.g. build -> drive -> audit/regression)? Record the exact commands and pass conditions.
- Map each requested outcome to evidence, including required delivery/review. Record what makes
  the observation valid (intended target, collected suite, readable source) and what invalidates
  prior proof. A green existing suite does not establish a requirement it never tests.
- Identify a concrete progress signal and the smallest experiment that would distinguish likely
  causes of a failure. Capture existing failed approaches instead of rediscovering them each run.
- **If the loop is open (a watcher)**, reframe B: instead of "what gate exists", find **what
  SIGNAL can be observed and what predicate fires on it** (a log pattern, a status field, a
  queue/inbox, a PR/CI event) — and whether that signal covers **every terminal/failure state
  incl crash/hang/OOM** (the silent-harness check in C generalizes to dead-watcher coverage).
  Find the real occurrence ID or recovery/failure transition, reaction acknowledgement/lookup,
  and destination idempotency support. Entity identity alone does not identify recurring events.

**C. Self-driving harness — this decides harness-failure handling**
- Look for drivers: Playwright, Cypress, Selenium, XCUITest, simulators (`xcrun simctl`),
  `scripts/*drive*`, `screencapture`, headless runners, `--drive`-style flags.
- Does the project emit observable artifacts (screenshots, state snapshots, logs) the loop
  must validate?
- Can the harness fail *silently* (blank capture, empty snapshot, frozen sim)? If so the
  loop needs an **observation-validity check** before trusting any result.

**D. Invariants, oracles & boundaries — feeds SUCCESS CRITERIA + RULES**
- Grep README/docs/test names for: `invariant`, `must not`, `read-only`, `parity`,
  `contract`, `do not modify`, `layout`, `idempotent`.
- Which properties must **never** break? What is off-limits to edit (vendored code, a
  read-only integration, UI layout, generated files)?

**E. Existing loop infrastructure — reuse, don't reinvent**
- Look for `.loop/`, `.loop-state.json`, `*state*.json`, `*FINDINGS*.md`, `*runbook*.md`,
  `scenarios/`, regression case dirs.
- If present, read them and **extend** the existing loop (reuse its state files, runbook,
  scenario format) rather than starting fresh.
- **List existing loops**: glob `.loop/*.md` (and read `.loop/INDEX.md` if present). If any loop
  files exist, show a one-line summary per loop (slug / goal / kind / launch line) so the user
  can choose **refresh/extend an existing loop** (→ the refine path in Step 0) vs **start a new
  one** before you spend turns profiling. If the new goal substantially matches an existing loop
  (same target + kind), default to **refining that loop** even when `$ARGUMENTS` never named it —
  don't spawn a near-duplicate (e.g. `qa-green-2`) or silently clobber the existing file.

**F. Operational facts**
- Commit convention (conventional commits in the log? commitlint/husky? signing policy?
  files that must never be staged, e.g. `outputs/`, `dist/`, build artifacts).
- Run cost/time (heavy build? long CI?) -> informs the budget. For each existing limit or
  checkpoint, inspect value/unit, source (user/platform/agent-default), evidence and enforcement.
  Internal counters inform replanning; they are not user-selected stopping limits.
- Crash/flake surfaces.

Then **summarize the profile** for the user and state explicitly:
- **What the session shows you're working on** (if any) — the in-flight goal from the
  conversation, and whether it matches the git diff.
- **Loop kind** — **closed** (drive-to-done) or **open** (watch/react). Classify from two
  signals: (1) the goal's verb/tense — terminus verbs → closed ("finish/complete/get green/
  fix all/完成/緑に"), continuous/recurring → open ("watch/monitor/notify me when/poll/alert
  on/triage incoming/監視/通知/見張る"); (2) the **decisive test** (also your confirm line to
  the user): *"Can you write a SUCCESS CRITERION that becomes permanently true and ENDS the
  loop? Yes → closed. If the only 'criterion' is a condition you REACT to that RECURS →
  open."* On silence/conflict, **default to closed** (ends on verified completion or actual stop boundaries) and state the assumption
  — misclassifying closed→open runs forever, the costlier error.
- **Maturity** (judge from the files, not a flag): where does it sit on the spectrum —
  *greenfield* (empty / only bootstrap files / no manifest / little-to-no git history) →
  *scaffolded but no gate* (code exists, but no tests/lint/build) → *mature* (a real gate
  already exists)?
- Is there a real automated gate? Single- or multi-stage?
- Is there a self-driving harness that can fail silently?
- Any existing loop infra to extend?
- Any hard invariants / off-limits boundaries?

Read the **"no automated check"** finding *through kind first, then maturity*:
- **kind=open (a watcher)** → "no completion gate" is **correct, not a defect**. Do NOT run
  the four-conditions "done is objective" test or the Ralph-Wiggum warning — they are
  closed-loop axioms. An open loop's failure modes are *missed events (coverage gap), alert
  fatigue (no dedup), non-idempotent double-acting, silent death* — never "fails to
  terminate". The two branches below apply only when **kind=closed**.
- **Mature repo, still no gate** → a loop is likely the wrong tool; say so plainly (a single
  good prompt usually wins).
- **Greenfield / early** → "no gate" is expected, nothing's built yet. Do NOT call the loop a
  bad fit. The loop's *first job is to create its gate* (scaffold + a first failing acceptance
  test); see Step 3's bootstrap guidance and the Bootstrap block in Step 5.
