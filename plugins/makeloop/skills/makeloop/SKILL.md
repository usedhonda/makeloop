---
name: makeloop
description: Generate a Codex-ready loop prompt contract for the current project. Use for makeloop, loop prompt, Codex loop, project loop, getting tests green with a reusable stateful loop, open watcher loops, or requests that ask to build a loop rather than do the project work directly.
argument-hint: "[goal hint (optional)]"
---

# makeloop for Codex

You are building a loop prompt contract for Codex, not running the project work.
Your deliverable is a saved `.loop/<slug>.md` prompt plus a seeded state or cursor file and a
ready-to-send Codex launch instruction.

## Canonical sources

Before generating, read these files from this plugin:

- `../../commands/makeloop.md` — canonical generator behavior and Steps 0-6.
- `../../templates/loop-prompt.tmpl.md` — canonical closed/open core and optional blocks.

Follow the canonical behavior unless this skill says to adapt it for Codex.

## Codex adaptations

- The user invokes this skill as `$makeloop:makeloop` in Codex CLI, or from the slash menu when the plugin is enabled in the Codex app.
- Preserve the loop-engineering contract: Project Profile, closed/open kind, real VERIFY gate or
  trigger, state/cursor, stop condition or run mode, t=0 policy, no fake done, maker != checker,
  no gate-bypass, and no unbound template placeholders.
- Do not generate a Claude Code `/loop` or `/ralph-loop` launch line. Codex does not have those
  commands.
- Do not create a runner. Codex v1 is prompt-contract only.
- The launch instruction is a normal Codex message that references the saved file.

## Launch instruction forms

Lead the final response with a short label, then a fenced `text` block that contains only the
ready-to-send Codex message in the user's working language. Do not wrap the message in quotes, and
do not put the message itself in a bullet.

Closed loop:

```text
.loop/<slug>.md の手順に従って1 iterationだけ進めて。state は .loop/<slug>-state.md を読んで更新して。完了なら FINAL、続行なら ITERATING で終えて。
```

Open watcher:

```text
.loop/<slug>.md の手順に従って1 watcher tickだけ実行して。cursor は .loop/<slug>.cursor.json を読んで更新して。新しい trigger があれば一度だけ notify/act し、なければ静かに終えて。
```

If the user asks for unattended scheduling, explain after the launch instruction that Codex
Automations can run the same tick prompt on a schedule, but do not create an automation unless the
user explicitly asks in a separate step.

## Output files

- Save the generated prompt to `.loop/<slug>.md`.
- Closed loops seed `.loop/<slug>-state.md`.
- Open loops seed `.loop/<slug>.cursor.json`.
- Append or update `.loop/INDEX.md` with the slug, goal, kind, gate or trigger, cap/run mode, and
  Codex launch instruction.

## Refine behavior

If the request names or clearly matches an existing `.loop/<slug>.md`, refine that loop instead of
creating a near-duplicate. Preserve the existing kind, state/cursor file, and blocks unless the user
explicitly asked to change them.

## Final response

Report compactly:

- ready-to-send Codex launch instruction first;
- saved prompt path;
- state or cursor path;
- key assumptions or wrong-tool warning, if any;
- any validation gap found by the pre-save self-check.
