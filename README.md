# makeloop

A Claude Code and Codex plugin that **builds loop prompts for you**.

Claude Code `/makeloop` or Codex `$makeloop:makeloop` reads your current project **and the session conversation**, pins down the work
goal, offers purpose-led choices and emits a complete, copyable loop contract —
goal, strict success criteria, a real verify gate, a state file, and a stop condition,
**written in your working language**. It generates the prompt; it does not run the loop.

## Choose by what you want to do

makeloop separates **purpose** from **execution mode**. If the goal is unclear, compare concrete
project-specific purposes before creating a contract. If it is clear, compare ways to run the
same contract. Usually you get one recommendation plus one or two useful alternatives:

| Want to… | Choice | What the explanation covers |
| --- | --- | --- |
| Finish the accepted repair or milestone | Native goal continuation, when available | Edits, acceptance evidence, budget, stop and resume |
| Inspect one bounded step first | One manual iteration | What may change, what is checked, remaining work and how to continue |
| Watch for new events | Open watcher tick or supported cadence | Signal, new-event dedup, notification/action scope, cursor, expiry and cancellation |
| Continue from CI or a wrapper | Exact-session resume, when requested | Working directory, state ownership and uncertain-effect reconciliation |

Each choice explains when it fits **and when it does not**, its actual effects and permissions,
its saved state and its stopping condition. A watcher is not an alternative implementation of a
repair. Choices are derived from the project, not fixed presets or a menu padded with irrelevant tools.

**Copy-first output:** a host/paste-destination label, one complete launch block, then a concrete
Loop brief and explained alternative cards. Long criteria live in the saved file. Each usable
alternative has its own block; explanations and shell prompts stay outside it, necessary shell
quotes stay inside. Unconfirmed features are described separately, not presented as runnable commands.

**Generated is not started.** Displaying goal/schedule alternatives does not create them, replace
an existing goal, reset a cursor or authorize concurrent writers. Existing `.loop/` files are not
bulk-migrated; refining preserves unrelated choices and progress.

## Install

Claude Code:

```
/plugin marketplace add usedhonda/makeloop
/plugin install makeloop
```

Then:

```
/makeloop
/makeloop finish the auth refactor   # optional goal hint
```

Codex:

```
codex plugin marketplace add usedhonda/makeloop
codex plugin add makeloop@makeloop
```

In the Codex app, type `/` and choose **makeloop** from the slash menu when it appears. In Codex
CLI, use `/skills` to browse skills or call the same skill explicitly:

```
$makeloop:makeloop
$makeloop:makeloop finish the auth refactor   # optional goal hint
```

Codex CLI does not currently support a typed top-level `/makeloop` command. The legacy custom
prompt form (`/prompts:makeloop`) is deprecated by Codex and may not appear in current CLI slash
completion even when `~/.codex/prompts/makeloop.md` exists. The helper below is retained only for
older Codex builds that still load custom prompts:

```
node plugins/makeloop/scripts/install-codex-prompt-shim.mjs
```

## What you get

A loop prompt grounded in loop-engineering practice — built around the three things that
make a loop work instead of just burn tokens:

- **Verify** — a real gate (test / build / lint), never the agent grading its own homework.
- **State** — `.loop/state.md` carries done / failed / next across iterations (resume, not
  restart).
- **Stop condition** — success OR a hard iteration cap, to avoid the "Ralph Wiggum loop".

`/makeloop` first builds a read-only **Project Profile** and **sizes the loop to it** — lean
for a single `npm test`, richer (two-stage gate, harness-failure detection, labeled stop
taxonomy, budget) when the project has a build + regression audit or a self-driving harness.

It judges the project's **maturity** too: for a greenfield/empty repo it generates a loop that
*bootstraps its own gate* (scaffold + failing acceptance tests, then drives red → green)
instead of calling a loop the wrong tool; for a mature repo it reuses the existing gate.

And it judges the **loop kind** — **closed** (drive-to-done: goal + verify gate + `FINAL`) vs
**open** (watch/react: a trigger condition + notify/act + dedup, runs indefinitely, no
`FINAL`). For an open watcher "no completion gate" is correct, so the wrong-tool warning is
suppressed; on ambiguity it defaults to closed.

The output is printed in chat and saved to `.loop/<slug>.md` (a descriptive name so multiple
loops coexist, listed in `.loop/INDEX.md`). Claude Code output leads with a
file-backed `/loop` launch line. Codex output leads with a copyable launch block for exactly one
iteration or watcher tick, then a short Loop brief explaining the loop's purpose, kind, gate or
trigger, state/cursor file, and stop condition. It also shows Codex-native run options: manual
ticks by default, `/goal` for closed continuation, Automations for heartbeat/watch loops, and
`codex exec resume` for external schedulers or CI.
`makeloop` will also tell you when a loop is the wrong tool (no automated check -> a single good
prompt wins).

See [`plugins/makeloop/README.md`](plugins/makeloop/README.md) for details.

## Repository layout

```
.agents/plugins/marketplace.json    # Codex marketplace manifest (one plugin: makeloop)
.claude-plugin/marketplace.json   # marketplace manifest (one plugin: makeloop)
plugins/makeloop/
  .codex-plugin/plugin.json        # Codex plugin manifest
  .claude-plugin/plugin.json       # plugin manifest
  commands/makeloop.md             # the /makeloop command (self-contained)
  skills/makeloop/SKILL.md         # the $makeloop:makeloop Codex skill
  templates/loop-prompt.tmpl.md    # the generated loop-prompt template (canonical)
  eval/scenarios.md                # golden eval — objective quality gate for makeloop itself
  eval/codex-scenarios.md          # Codex-surface eval — skill/plugin launch contract
  scripts/install-codex-prompt-shim.mjs # optional local Codex slash-like prompt shim installer
  SELF-IMPROVEMENT.md              # governance contract for makeloop's self-strengthening loop
  AUTOMATION.md                    # operator runbook for the every-2-days self-improvement cron
  loop-engineering-notes.md        # technique catalog + self-improvement run history + fleet-mode roadmap
  README.md                        # plugin docs
```

## Self-improvement (for maintainers)

makeloop can strengthen itself on a schedule. A local cron runs one harvest → gate → apply cycle
every 2 days: it adopts community loop-engineering techniques that pass a **deterministic safety
gate** (`.githooks/gate.sh`) plus an adversarial fit-critic, and prunes to stay lean (homeostasis,
not bloat). Gate-passed **Tier-1** edits auto-commit and push to `main`; anything that changes core
behavior or weakens a constraint **escalates to a human** instead. The trust anchor is read-only to
the loop (enforced out-of-band by settings deny + a pre-commit hook + `chmod`). Governance lives in
[`plugins/makeloop/SELF-IMPROVEMENT.md`](plugins/makeloop/SELF-IMPROVEMENT.md); the operator runbook
(install, pause/resume, undo) in [`plugins/makeloop/AUTOMATION.md`](plugins/makeloop/AUTOMATION.md).
The system is opt-in; fresh clones ship **PAUSED** (enable after a watched run — see AUTOMATION.md).
Each run that changes a public file is logged in `loop-engineering-notes.md` § Self-improvement run
history, alongside `git log --author=makeloop-selfimprove`.

## License

MIT — see [LICENSE](LICENSE).
