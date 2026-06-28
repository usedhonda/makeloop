# makeloop Codex eval — scenarios + expected properties

This file is the Codex-surface companion to `scenarios.md`. The Claude Code golden eval remains
the canonical behavioral gate for `/makeloop`; this eval checks that the Codex skill/plugin surface
preserves the same loop contract without depending on Claude-only slash commands.

## How to run

For each scenario, act as the Codex `$makeloop:makeloop` skill would act:

1. Read the current request and profile.
2. Generate the loop prompt that would be saved under `.loop/<slug>.md`, plus the state/cursor file
   and the chat summary.
3. Judge the generated artifacts mechanically against the expected properties below.

The checker must be independent from the maker. Do not self-grade. A PASS requires every listed
property for that scenario plus every cross-cutting property.

This file is part of the self-improvement eval suite. Any self-improvement candidate that
changes canonical generator behavior must grade this file along with `scenarios.md`. A FAIL here
blocks Tier-1 auto-apply and escalates the candidate for human review.

## C1 — closed mature loop

Request/profile:
- Request: `$makeloop:makeloop finish the auth refactor, gate: npm test && tsc`
- Profile: mature project, existing test/build commands, no watcher intent, no existing loop named.

Expected properties:
- Classified as closed.
- Uses exactly one CLOSED CORE and no OPEN CORE.
- Contains GOAL, SUCCESS CRITERIA, VERIFY, RULES, UPDATE STATE, and FINAL.
- VERIFY uses the explicit gate `npm test && tsc` unless repo evidence finds a stricter matching gate.
- Seeds a state file, not a cursor file.
- Chat output leads with a copyable fenced `text` launch block that contains only a Codex-ready
  message. It references `.loop/<slug>.md` and the state file, says to run exactly one iteration,
  and ends with `FINAL` or `ITERATING`.
- Chat output includes a concrete Loop brief explaining the loop purpose, closed kind, gate,
  state file, and stop or next outcome.
- Chat output includes Codex run options. Manual tick is the recommended default for a safe first
  run; `/goal` may be offered for same-thread continuation; `codex exec resume` is offered only
  when CI/cron/wrapper intent is present.
- Does not emit `/loop`, `/ralph-loop`, or `codex-loop` as the launch mechanism.

## C2 — open watcher loop

Request/profile:
- Request: `$makeloop:makeloop watch deploy status every 5 min and notify me when it fails`
- Profile: mature project with deploy/status files or commands; no permanent completion criterion.

Expected properties:
- Classified as open.
- Uses exactly one OPEN CORE and no CLOSED CORE.
- Contains WATCH TARGET, TRIGGER CONDITION, RUN MODE, DEDUP/CURSOR, RULES, and UPDATE CURSOR.
- Does not contain FINAL or SUCCESS CRITERIA as a completion gate.
- Seeds a cursor file, not a closed-loop state file.
- Suppresses the wrong-tool warning for missing final completion gate.
- Chat output leads with a copyable fenced `text` launch block that contains only a Codex-ready
  watcher message. It references `.loop/<slug>.md` and the cursor file, says to run exactly one
  watcher tick, and updates the cursor.
- Chat output includes a concrete Loop brief explaining the watch target, open kind, trigger,
  cursor file, and dedup or next outcome.
- Chat output includes Codex run options. Manual watcher tick is the recommended default for first
  proof; thread automation is offered for same-thread heartbeat; standalone/project automation is
  offered only when independent or background runs are appropriate.
- Does not emit `/loop`, `/ralph-loop`, or `codex-loop` as the launch mechanism.

## C3 — greenfield closed loop

Request/profile:
- Request: `$makeloop build a CLI that converts CSV to JSON, tests passing`
- Profile: empty or near-empty repo, no existing gate.

Expected properties:
- Classified as closed.
- Includes the Bootstrap block.
- Bootstrap creates or discovers a deterministic acceptance gate before claiming completion.
- Does not call the lack of an existing gate a wrong-tool condition.
- Chat output leads with a copyable fenced `text` launch block for one closed iteration and includes
  a concrete Loop brief plus Codex run options.

## C4 — pre-existing-state policy

Request/profile:
- Closed subcase: mature repo, all SUCCESS CRITERIA are already satisfied at first VERIFY.
- Open subcase: log watcher with pre-existing matching backlog and no explicit replay/backfill request.

Expected properties:
- Closed subcase: first VERIFY honesty is present. If the initial VERIFY satisfies every criterion,
  the loop may print an honest FINAL saying the work was already satisfied, and must not fabricate a
  diff or weaken the criteria.
- Open subcase: cursor seed policy defaults t=0 to EOF/latest marker; pre-existing backlog is seen
  and does not trigger a day-zero notification.
- Open replay/backfill is opt-in only and bounded when explicitly requested.

## C5 — Codex surface and shim

Request/profile:
- Request: use makeloop from Codex with a slash-like entrypoint if available.
- Profile: repository contains the makeloop Codex plugin and optional prompt shim installer.

Expected properties:
- Canonical surface is a Codex skill named `makeloop`.
- Plugin manifest exposes the skill as installable/discoverable.
- Explicit CLI invocation may be `$makeloop:makeloop` when plugin prefixing is visible.
- Optional prompt shim is thin: it delegates to `$makeloop:makeloop` and does not duplicate
  generator logic.
- Generated loop files remain file-backed under `.loop/`.
- No deterministic runner, scheduler, or background loop is created unless requested separately.
  Codex run options may be described without implying creation.

## Cross-cutting Codex properties

Every generated Codex loop prompt must satisfy:

- Preserves the three hearts: verify/trigger, state/cursor, stop/dedup.
- RULES contain maker != checker, Surgical changes only, Search before assuming, and No fake done.
- No source citations, raw harvest text, secret material, or `.local/` contents appear.
- Chat output begins with a file-reference launch block for Codex.
- Chat output includes a concrete Loop brief.
- Chat output includes Codex run options with exactly one recommended mode and safe alternates.
- Closed-only blocks do not appear in open prompts; open-only blocks do not appear in closed prompts.
- No gate-bypass wording in RULES or VERIFY (unavailable, skip, assume, treat-as, fallback, degrade,
  bypass, or equivalent).
- No unbound placeholders such as `<channel>` or `<...>` remain in generated output.
- Preset hints, if any future surface reintroduces them, are non-binding only; current output must not
  depend on `preset_hint` or skip DISCOVER because of it.
