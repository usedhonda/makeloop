---
name: makeloop
description: Generate a Codex-ready loop prompt contract for the current project. Use for makeloop, loop prompt, Codex loop, project loop, getting tests green with a reusable stateful loop, open watcher loops, or requests that ask to build a loop rather than do the project work directly.
argument-hint: "[goal hint (optional)]"
---

# makeloop for Codex

You are building a loop prompt contract for Codex, not running the project work.
Your deliverable is a saved `.loop/<slug>.md` prompt plus a seeded state or cursor file and a
ready-to-send Codex launch instruction plus Codex-native run options.

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
- Do not create a runner unless the user explicitly asks for a script/automation in a separate
  request. Codex v1 is prompt-contract first.
- The default launch instruction is a normal Codex message that references the saved file.
- Codex loop behavior maps to Codex-native surfaces, not to a fake `/loop` command:
  - manual tick: send one copyable message for one closed iteration or one open watcher tick;
  - `/goal`: for closed loops where the user wants Codex to keep pursuing the objective across
    turns, provide a copyable goal text that points at the saved loop file and state file;
  - thread automation: for open watchers or cadence follow-up, provide a copyable prompt that asks
    Codex to create a thread automation using the saved loop file and cursor file;
  - `codex exec resume`: for CI/cron/shell orchestration, provide a copyable resume prompt, but no
    shell runner unless explicitly requested.

## Proposal discipline

Mirror the canonical `/makeloop` interaction style instead of silently choosing a thin path.

- After DISCOVER, present one consolidated proposal before writing files unless the request says
  `just generate`, `don't ask`, `auto`, or equivalent.
- The proposal must include: kind, goal or watch target, SUCCESS CRITERIA or TRIGGER CONDITION,
  gate or signal predicate, state/cursor file, stop/run mode, and the recommended Codex run mode.
- Offer 2-3 concrete scope/run choices when the user has not already fixed them. Keep the options
  Codex-native:
  - closed: manual tick (default), `/goal` assisted continuation, or `codex exec resume` pipeline;
  - open: manual watcher tick, thread automation heartbeat, or standalone/project automation.
- Ask a follow-up only for choices that are ambiguous and high-impact. Otherwise make the same
  conservative assumptions the canonical generator would make and list them.
- Codex may not expose Claude Code's `AskUserQuestion` UI. If confirmation is needed, ask a concise
  normal chat question with the consolidated proposal and wait for the user's answer before writing
  files. If the user chooses a run mode, preserve that choice exactly in the saved `.loop/INDEX.md`
  and final `Codex run options`.
- If an existing `.loop/<slug>.md` substantially matches the goal, default to refining it rather
  than creating a duplicate.

Use this proposal shape when confirmation is needed:

```markdown
Proposed loop shape
- Kind: <closed/open> — <one-line reason>
- Target: <goal or watch target>
- Check: <SUCCESS CRITERIA summary or TRIGGER CONDITION>
- Verify/signal: <gate commands or observed signal>
- State: <state/cursor path>
- Run mode: <recommended Codex run mode> — <why>

Options
1. <recommended option>
2. <alternate option>
3. <alternate option, only if useful>

Reply with the option number or edits.
```

## Codex run-mode recommendation

Choose the recommendation from the user's intent and the profile, then show the alternates without
overloading the user.

| Situation | Recommend | Why |
| --- | --- | --- |
| Closed loop, user wants a safe first run or the gate is expensive/risky | Manual tick | Matches CC's controlled first iteration; easiest to inspect and stop. |
| Closed loop, user wants Codex to keep pursuing the same objective in this thread | `/goal` | Codex keeps the objective attached across turns while the saved state file remains the loop ledger. |
| Closed loop, user mentions CI, cron, wrapper, script, or non-interactive use | `codex exec resume` | An external scheduler can own cadence while Codex resumes the same contract. |
| Open watcher, user wants recurring checks in this same thread | Thread automation | Preserves thread context and works like a heartbeat. |
| Open watcher, each run should be independent or isolated from local edits | Standalone/project automation | Lets Codex use a background worktree when appropriate. |
| Open watcher, user only wants to test the watcher once | Manual watcher tick | Proves trigger/cursor/dedup before scheduling. |

If the user's requested run mode conflicts with safety (for example, unattended writes before one
manual tick), recommend the safer first step and list the requested mode as the next upgrade path.

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

## Codex run options

After the launch block and Loop brief, include a compact `Codex run options` section. Mark exactly
one option as recommended and keep the rest as alternates.

Closed loop options:

- **Manual tick (default, safest)** — the launch block above. User sends it again or asks Codex to
  continue when `ITERATING` appears.
- **Goal-backed continuation** — include this only when useful for a longer closed task:

```text
/goal .loop/<slug>.md の手順に従って <short goal> を完了まで進める。state は .loop/<slug>-state.md を毎回読んで更新する。VERIFY が全 SUCCESS CRITERIA を満たしたら FINAL、未達なら次の最小ステップへ進む。
```

- **Scripted resume** — include this only when the user wants CI/cron/wrapper control:

```text
codex exec resume --last ".loop/<slug>.md の手順に従って1 iterationだけ進めて。state は .loop/<slug>-state.md を読んで更新して。完了なら FINAL、続行なら ITERATING で終えて。"
```

Open watcher options:

- **Manual watcher tick (default, safest)** — the watcher launch block above.
- **Thread automation heartbeat** — recommend for recurring polling that should preserve thread
  context. Provide a setup prompt, not a created automation, unless explicitly asked:

```text
このthreadで <interval> ごとに .loop/<slug>.md の watcher tick を実行する automation を作って。cursor は .loop/<slug>.cursor.json を読んで更新し、新しい trigger だけ notify/act して。
```

- **Standalone/project automation** — recommend only when each run should be independent or should
  run in a background worktree. Mention that sandbox/worktree choice changes write risk.

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

- ready-to-send Codex launch instruction first, as a copyable fenced `text` block;
- `Loop brief` immediately after the launch block, with 3-5 short bullets:
  - what the loop is trying to change or watch;
  - closed/open kind and why;
  - the success gate or trigger condition;
  - the state or cursor file and what it preserves;
  - the stop condition or next expected outcome;
- saved prompt path;
- state or cursor path;
- `Codex run options` with the recommended mode and alternates;
- key assumptions or wrong-tool warning, if any;
- any validation gap found by the pre-save self-check.

Keep the brief concrete to the generated loop. Do not say only "follow the prompt" or repeat the
file path as the explanation.
