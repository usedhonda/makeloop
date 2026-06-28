# makeloop

A Claude Code and Codex plugin that **builds loop prompts for you**.

`/makeloop` or `$makeloop` reads your current project **and the session conversation**, pins down the work
goal, asks a couple of focused questions, and emits a complete, paste-ready loop prompt —
goal, strict success criteria, a real verify gate, a state file, and a stop condition,
**written in your working language**. It generates the prompt; it does not run the loop.

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

Then use the `makeloop` skill from the slash menu when available, or call it explicitly:

```
$makeloop
$makeloop finish the auth refactor   # optional goal hint
```

Optional local slash shim:

```
node plugins/makeloop/scripts/install-codex-prompt-shim.mjs
```

That installs a thin `~/.codex/prompts/makeloop.md` shim so `/prompts:makeloop ...` delegates to
`$makeloop`. The skill is the canonical Codex surface; the shim exists only for slash-like muscle
memory because custom prompts are deprecated in favor of skills.

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

The output is printed in chat and saved to `.loop/loop-prompt.md`. Claude Code output leads with a
file-backed `/loop` launch line. Codex output leads with a ready-to-send instruction for exactly
one iteration or watcher tick, referencing the saved `.loop/<slug>.md` file and state/cursor file.
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
  skills/makeloop/SKILL.md         # the $makeloop Codex skill
  templates/loop-prompt.tmpl.md    # the generated loop-prompt template (canonical)
  eval/scenarios.md                # golden eval — objective quality gate for makeloop itself
  eval/codex-scenarios.md          # Codex-surface eval — skill/plugin launch contract
  scripts/install-codex-prompt-shim.mjs # optional local Codex slash-like prompt shim installer
  scripts/check-codex-surface.sh   # self-improvement guard for the Codex plugin/skill surface
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
