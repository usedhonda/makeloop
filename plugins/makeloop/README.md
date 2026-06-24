# makeloop

A Claude Code slash command that **builds `/loop` prompts for you**.

`/makeloop` reads your current project **and the session conversation**, figures out the work
goal, asks you a couple of focused questions, and emits a complete, paste-ready loop prompt —
goal, strict success criteria, a real verify gate, a state file, and a stop condition,
**written in your working language**. It does **not** run the loop; it produces the prompt you
then feed to `/loop` (or `/ralph-loop`).

## Usage

```
/makeloop                  # analyze the project and build a loop prompt
/makeloop finish the auth refactor   # optional: pass a goal hint
```

### Inline directives

The text after `/makeloop` is parsed for both a **goal** and **operational directives** —
anything you decide up front is honored and its question is skipped. Natural phrasing, not
strict flags:

```
/makeloop QA all green, ralph-loop, cap 20, with harness detection, ask minimally
/makeloop 全テストを緑に、30分ごと、上限15、質問は最小で
```

Recognized: goal/scope, runtime (`self-paced` / `interval 30m` / `ralph-loop`), iteration
cap & budget (`cap 20`, `wall-clock 30min`, `no-progress 3`), success streak (`K=3`), an
explicit verify gate (`gate: npm test && tsc`), forcing optional blocks on/off
(`two-stage gate`, `no budget block`, `harness off`), and interaction level
(`don't ask` / `just generate`). Anything you omit falls back to its normal question.
`/makeloop` echoes a one-line summary of what it parsed so you can correct it.

You'll be asked (for anything not already specified inline):

1. **Scope** — finish in-flight work / reach the next milestone / complete the project.
2. **Success criteria** — confirmed, strict, objectively checkable.
3. **Verify gate + stop condition** — the test/build/lint that rejects bad work, and a hard
   iteration cap (default 8).
4. **Runtime** — built-in `/loop` (self-paced or interval) or the `ralph-loop` plugin.

The result is printed in chat and saved to `.loop/loop-prompt.md`, with a seeded
`.loop/state.md`. The generated prompt is written in **your working language** (the language
of the conversation) — only machine-significant literals (commands, paths, `FINAL` /
`<promise>DONE</promise>`, JSON keys) stay as-is.

## Depth that matches the project

`/makeloop` reads **two things**: the **live session conversation** (what you've been working
on, what you just asked for, decisions made, errors hit — the *intent*) and the **project
state** (git diff, code, tests — the *reality*), and reconciles them. From the project it
builds a read-only **Project Profile**: **maturity** (greenfield → scaffolded-but-no-gate →
mature), verification depth (single- vs multi-stage), whether there's a self-driving test
harness that can fail silently, hard invariants and off-limits boundaries, existing loop
infrastructure to extend, and commit conventions. It judges maturity from the files — no
flag — and adapts:

- **Greenfield / empty** — instead of declaring "no gate → loop is the wrong tool", the loop
  *bootstraps its own gate*: iteration 0 scaffolds the project and writes the acceptance
  criteria as failing tests, then drives red → green.
- **Mature** — reuses the gate the project already has.

The generated loop is also **sized to the profile** — it stays lean for a project with one
`npm test`, and grows the advanced blocks when the project supports them:

- **Two-stage gate** (pre-gate / post-gate) with FREEZE-no-commit on regression, for
  projects with a build + baseline/regression audit.
- **Observation-validity check** + `unrecoverable-harness` / `pinata` stops, for self-driving
  harnesses that emit screenshots/snapshots.
- **Regression-guard step** (one minimal case per fix) when `scenarios/`/golden files exist.
- **Budget** + a **labeled stop taxonomy** (`no-progress`, `oscillation`, `failure`,
  `scope-boundary`, …) for autonomous loops.

For large or unfamiliar codebases it can dispatch `Explore` subagents to build the profile
faster, then confirm the key findings before generating.

### Hardening built into every generated loop

Beyond the three hearts, each loop is shaped by lessons from loop-engineering practice:

- **Re-anchor every iteration** — re-read goal + criteria + rules, not just state, so a long
  run doesn't drift past its "do not touch" boundaries.
- **Backpressure ladder** — run checks fastest→slowest, stop at the first red.
- **Search before assuming**, **no fake done** (no stubs/TODOs as done, never weaken a check),
  and **compact feedback** (pass = 1 line, fail = expected/actual/fix).
- **Gate-will-be-gamed defense** — holdouts, properties over self-written tests, spot-checks.

Profile/directive-triggered blocks add a **no-progress circuit breaker**, **cross-run
learnings** (`.loop/learnings.md`), **escalation handoff** for unattended runs,
**scheduled-loop safety** (idempotency, external scheduler, tiered auto-approve, intent
deny-list), a **JSON done-ledger**, and **LLM-as-judge hardening**.

The technique catalog and the deferred fleet-mode roadmap live in
[`loop-engineering-notes.md`](loop-engineering-notes.md).

## Why it's shaped this way (loop engineering)

Every generated prompt carries the parts that make a loop actually work rather than just
spend tokens:

- **Verify** is a real gate (test/build/lint), not the agent grading its own homework.
- **State** (`.loop/state.md`) carries done / failed / next across iterations, so the loop
  resumes instead of restarting.
- **Stop condition** is success OR a hard cap, to avoid the "Ralph Wiggum loop" (exits too
  early, or spins forever spending money).
- **maker != checker**: risky changes get re-verified with fresh eyes.

It will also tell you when a loop is the *wrong* tool — if there's no automated way to
reject bad output, a single good prompt usually beats a loop.
