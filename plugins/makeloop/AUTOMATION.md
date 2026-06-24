# makeloop automation — the every-2-days self-improvement loop

makeloop can improve itself on a schedule: harvest community loop-engineering knowledge,
gate it, and auto-apply what's safe. This doc is the operator's runbook. Governance/safety
lives in [`SELF-IMPROVEMENT.md`](SELF-IMPROVEMENT.md); the quality gate in
[`eval/scenarios.md`](eval/scenarios.md).

## What runs

Local cron fires a wrapper every 2 days; the wrapper runs ONE self-improvement cycle as a
fresh headless `claude` session, then exits. Each fresh run resumes from a cursor file (no
"paused process" — the cursor IS the resume mechanism).

```
cron (every 2 days, 09:00)
  -> $REPO/.loop/self-improve-run.sh          (wrapper: pause-check, env, logging)
       -> if .loop/PAUSED exists: skip
       -> claude -p "<one self-improve cycle>" --permission-mode acceptEdits
            -> follows .loop/self-improve.md  (harvest -> dedup -> fit-critic ->
               propose -> .githooks/gate.sh -> Tier-1 auto-apply / Tier-2 escalate)
            -> commits Tier-1 edits as author "makeloop-selfimprove"
       -> if the cycle made commits AND .githooks/gate.sh re-PASSES on HEAD:
            git pull --rebase --autostash origin main && git push origin main
            (the LLM never pushes; the wrapper does. NEVER force-push;
             on rebase/push failure the commits stay local for human review)
       -> appends to .loop/cron.log
```

Cron line (install on the dev machine — see "Install" below):
```
0 9 */2 * * <REPO>/.loop/self-improve-run.sh
```

## Files (all under `.loop/`, local/gitignored)

- `self-improve-run.sh` — the cron wrapper (pause switch, bot git identity, logging).
- `self-improve.md` — the loop prompt the cycle follows.
- `self-improve.cursor.json` — resume state (last round, seen-source digest, prune counter).
- `cron.log` — per-run log (`tail .loop/cron.log`).
- `PAUSED` — kill-switch flag (present = the wrapper skips, enforced before `claude` starts).
- `proposals/` — Tier-2 escalations (diffs needing a human GO) land here.

## Controls

| Want to… | Do |
| --- | --- |
| **Pause** (cron stays installed) | `touch .loop/PAUSED` |
| **Resume** | `rm .loop/PAUSED` |
| **See what it did** | `tail -n 40 .loop/cron.log` ; `git log --author=makeloop-selfimprove --oneline` |
| **Change frequency** | `crontab -e` (edit the `*/2` line) |
| **Remove entirely** | `crontab -e` and delete the `self-improve-run.sh` line |
| **Undo a bad auto-edit** | `git revert <commit>` (stopping cron does NOT revert past edits) |

The pause check runs in the wrapper (plain bash) *before* `claude` starts, so the LLM cannot
ignore or remove its own pause — it's a deterministic human kill-switch.

## First run (required before trusting the cron)

It ships **PAUSED on purpose**. Prove one watched run first (build order: prove → loop →
schedule):
1. Run `.loop/self-improve-run.sh` **interactively** (or run the loop in a normal session) and
   approve the tool prompts once — this also records the allowed tools so later headless runs
   don't stall. (Bash/WebFetch aren't auto-accepted by `acceptEdits` alone.)
2. Confirm it harvested → gated → behaved (check `cron.log`, `git log`).
3. Then enable autonomy: `rm .loop/PAUSED`.

## Safety model (why unattended is OK)

- The loop runs as a separate process; **its activity does NOT appear in any interactive
  Claude session** — monitor via `cron.log` + `git log`.
- **Anchors are read-only to the loop**, enforced out-of-band: `.claude/settings.json` denies
  Edit/Write on `SELF-IMPROVEMENT.md` / `eval/` / `settings.json` / `.githooks/`; the
  `.githooks/pre-commit` hook blocks commits to them; they are `chmod 444`; and the auto-mode
  classifier refuses to let an agent un-protect them without an explicit human `chmod`.
- **`.githooks/gate.sh`** mechanically checks each change (guarded phrases intact, no
  gate-bypass clause, anchor untouched, JSON/structure/leak/eval). Tier-1 auto-apply only on
  `GATE PASS`.
- Outbound exfil channels are denied (Gmail/Drive/Calendar MCP, secret-read globs); WebFetch
  is GET-only.
- The human owns the anchor (the "constitution"), not each edit. Changing the constitution
  requires a human `chmod u+w` first (deliberate friction).
- **Auto-push is gate-guarded**: the wrapper pushes bot commits to `origin/main` only after
  `gate.sh` re-PASSES on HEAD; it **never force-pushes**, and a rebase/push failure leaves the
  commits local for human review (fail-safe). The LLM cycle only *commits* — the deterministic
  wrapper decides the *push*. `.local/` (secrets, sources) is gitignored, so a push never carries
  them (H1 preserved). The anchor-touching commit can't exist (pre-commit blocks it), so it can't
  be pushed either.

## Install (needs the human — macOS asks permission to modify cron)

Modifying the user crontab triggers a macOS permission prompt that headless tooling can't
answer. Install it yourself, preserving existing cron jobs:
```
( crontab -l 2>/dev/null; echo "0 9 */2 * * <REPO>/.loop/self-improve-run.sh" ) | crontab -
crontab -l   # verify
```
(Replace `<REPO>` with the absolute repo path. macOS may prompt for Terminal cron access —
approve it.)
