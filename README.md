# makeloop

A Claude Code plugin that **builds `/loop` prompts for you**.

`/makeloop` reads your current project, pins down the work goal, asks a couple of focused
questions, and emits a complete, paste-ready loop prompt — goal, strict success criteria, a
real verify gate, a state file, and a stop condition. It generates the prompt; it does not
run the loop.

## Install

```
/plugin marketplace add usedhonda/makeloop
/plugin install makeloop
```

Then, in any project:

```
/makeloop
/makeloop finish the auth refactor   # optional goal hint
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

The output is printed in chat and saved to `.loop/loop-prompt.md`. `/makeloop` will also
tell you when a loop is the wrong tool (no automated check -> a single good prompt wins).

See [`plugins/makeloop/README.md`](plugins/makeloop/README.md) for details.

## Repository layout

```
.claude-plugin/marketplace.json   # marketplace manifest (one plugin: makeloop)
plugins/makeloop/
  .claude-plugin/plugin.json       # plugin manifest
  commands/makeloop.md             # the /makeloop command (self-contained)
  templates/loop-prompt.tmpl.md    # the generated loop-prompt template (canonical)
  README.md                        # plugin docs
```

## License

MIT — see [LICENSE](LICENSE).
