# Tier-2 proposal: Fable-era Codex launch surface

Status: proposal only. Do not auto-apply.

Tier: **Tier 2**. This proposal changes the Codex invocation and run-mode surface, so it requires
human GO and paired adapter review under the Codex adapter invariant.

Intent: update the Codex adapter and public usage docs for two post-baseline product deltas without
changing the canonical generator or weakening any emitted loop contract:

1. Replace the old Codex-app slash-list claim with the current Skills / `@` / `/skills` / `$` entry
   points.
2. Replace old Automation terminology with host-gated Scheduled task terminology.

Evidence and source URLs are intentionally not duplicated here. See
`docs/log/codex/011-fable-era-codex-surface-delta.md` section **Sources checked**.

## Tier-2 changes requested

Apply the three files below as one paired adapter/docs change. Do not mix canonical generator,
template, eval, governance, or unrelated prompt-pruning work into the same change.

### 1. `plugins/makeloop/skills/makeloop/SKILL.md`

#### Current invocation wording

```md
- The user invokes this skill as `$makeloop:makeloop` in Codex CLI, or from the slash menu when the plugin is enabled in the Codex app.
```

#### Proposed invocation wording

```diff
-- The user invokes this skill as `$makeloop:makeloop` in Codex CLI, or from the slash menu when the plugin is enabled in the Codex app.
+- In Codex CLI or the IDE extension, the user invokes this skill with `$makeloop:makeloop` or
+  selects it through `/skills`. In the ChatGPT desktop app's Codex view, the user opens Skills or
+  types `@` and selects `makeloop`. Do not promise a top-level `/makeloop` or a skill entry in the
+  slash-command list.
```

#### Current run-surface wording

```md
  - thread automation: for open watchers or cadence follow-up, provide a copyable prompt that asks
    Codex to create a thread automation using the saved loop file and cursor file;
```

```md
  - open: manual watcher tick, thread automation heartbeat, or standalone/project automation.
```

```md
| Open watcher, user wants recurring checks in this same thread | Thread automation | Preserves thread context and works like a heartbeat. |
| Open watcher, each run should be independent or isolated from local edits | Standalone/project automation | Lets Codex use a background worktree when appropriate. |
```

```md
If the user asks for unattended scheduling, explain after the launch instruction that Codex
Automations can run the same tick prompt on a schedule, but do not create an automation unless the
user explicitly asks in a separate step.
```

````md
- **Thread automation heartbeat** — recommend for recurring polling that should preserve thread
  context. Provide a setup prompt, not a created automation, unless explicitly asked:

```text
このthreadで <interval> ごとに .loop/<slug>.md の watcher tick を実行する automation を作って。cursor は .loop/<slug>.cursor.json を読んで更新し、新しい trigger だけ notify/act して。
```

- **Standalone/project automation** — recommend only when each run should be independent or should
  run in a background worktree. Mention that sandbox/worktree choice changes write risk.
````

#### Proposed run-surface diff

```diff
 - Codex loop behavior maps to Codex-native surfaces, not to a fake `/loop` command:
   - manual tick: send one copyable message for one closed iteration or one open watcher tick;
   - `/goal`: for closed loops where the user wants Codex to keep pursuing the objective across
     turns, provide a copyable goal text that points at the saved loop file and state file;
-  - thread automation: for open watchers or cadence follow-up, provide a copyable prompt that asks
-    Codex to create a thread automation using the saved loop file and cursor file;
+  - scheduled task inside a chat: offer only in the ChatGPT desktop app's Codex view when the
+    current chat has access to the local project; it preserves that chat's context;
+  - standalone scheduled task: offer only in the ChatGPT desktop app when independent runs are
+    appropriate; say whether it uses the local project or an isolated worktree;
   - `codex exec resume`: for CI/cron/shell orchestration, provide a copyable resume prompt, but no
     shell runner unless explicitly requested.
+- Codex CLI and the IDE extension do not manage Scheduled tasks. On those hosts, recurring open
+  watchers use manual ticks or an external scheduler with `codex exec` / `codex exec resume`.
+- A web Scheduled task cannot read a local `.loop/<slug>.md`; do not recommend it for a file-backed
+  loop unless the durable contract is available in uploaded, project, or connected context.
```

```diff
 - Offer 2-3 concrete scope/run choices only when there is a real fork. Keep the options terse and
   Codex-native:
   - closed: manual tick (default), `/goal` assisted continuation, or `codex exec resume` pipeline;
-  - open: manual watcher tick, thread automation heartbeat, or standalone/project automation.
+  - open: manual watcher tick; in the ChatGPT desktop app, a scheduled task inside this chat or a
+    standalone scheduled task; in CLI/IDE, an external `codex exec` scheduler when requested.
```

```diff
-| Open watcher, user wants recurring checks in this same thread | Thread automation | Preserves thread context and works like a heartbeat. |
-| Open watcher, each run should be independent or isolated from local edits | Standalone/project automation | Lets Codex use a background worktree when appropriate. |
+| Open watcher in the ChatGPT desktop app, preserve this chat's context | Scheduled task inside this chat | Returns to the same chat and can use the local project. |
+| Open watcher in the ChatGPT desktop app, independent runs | Standalone scheduled task | Starts separate runs; choose local project or isolated worktree explicitly. |
+| Open watcher in Codex CLI/IDE, recurring checks | External scheduler with `codex exec` / `codex exec resume` | Those hosts do not manage Scheduled tasks. |
```

```diff
 If the user asks for unattended scheduling, explain after the launch instruction that Codex
-Automations can run the same tick prompt on a schedule, but do not create an automation unless the
-user explicitly asks in a separate step.
+Scheduled tasks can run the same tick prompt in the ChatGPT desktop app. Offer that setup only
+when the active host supports it and the local project is available. Otherwise describe an
+external `codex exec` scheduler. Do not create either unless the user explicitly asks in a
+separate step.
```

```diff
 Open watcher options:

 - **Manual watcher tick (default, safest)** — the watcher launch block above.
-- **Thread automation heartbeat** — recommend for recurring polling that should preserve thread
-  context. Provide a setup prompt, not a created automation, unless explicitly asked:
+- **Scheduled task inside this chat** — offer only in the ChatGPT desktop app's Codex view when
+  recurring polling should preserve this chat's context and the local project is available.
+  Provide a setup prompt, not a created scheduled task, unless explicitly asked:

 ```text
-このthreadで <interval> ごとに .loop/<slug>.md の watcher tick を実行する automation を作って。cursor は .loop/<slug>.cursor.json を読んで更新し、新しい trigger だけ notify/act して。
+この chat で <interval> ごとに .loop/<slug>.md の watcher tick を実行する scheduled task を作って。cursor は .loop/<slug>.cursor.json を読んで更新し、新しい trigger だけ notify/act して。
 ```

-- **Standalone/project automation** — recommend only when each run should be independent or should
-  run in a background worktree. Mention that sandbox/worktree choice changes write risk.
+- **Standalone scheduled task** — offer only in the ChatGPT desktop app when each run should be
+  independent. State whether it runs in the local project or an isolated worktree, and mention
+  that sandbox/worktree choice changes write risk.
+- **External scheduler** — in Codex CLI/IDE, offer `codex exec` / `codex exec resume` only when the
+  user requests recurring or non-interactive control. Do not present Scheduled setup there.
```

Keep unchanged:

- canonical-source reads;
- manual-tick launch blocks;
- `/goal` wording;
- `codex exec resume` wording;
- state/cursor paths and `.loop/INDEX.md` behavior;
- manual-first safety, explicit scheduling intent, and no silent scheduler creation.

### 2. `README.md`

#### Current wording

```md
In the Codex app, type `/` and choose **makeloop** from the slash menu when it appears. In Codex
CLI, use `/skills` to browse skills or call the same skill explicitly:
```

```md
It also shows Codex-native run options: manual
ticks by default, `/goal` for closed continuation, Automations for heartbeat/watch loops, and
`codex exec resume` for external schedulers or CI.
```

#### Proposed diff

```diff
-In the Codex app, type `/` and choose **makeloop** from the slash menu when it appears. In Codex
-CLI, use `/skills` to browse skills or call the same skill explicitly:
+In the ChatGPT desktop app's Codex view, open **Skills** or type `@`, then select **makeloop**.
+In Codex CLI or the IDE extension, use `/skills` to browse skills or call the same skill
+explicitly:
```

```diff
 It also shows Codex-native run options: manual
-ticks by default, `/goal` for closed continuation, Automations for heartbeat/watch loops, and
-`codex exec resume` for external schedulers or CI.
+ticks by default, `/goal` for closed continuation, host-supported Scheduled tasks for
+heartbeat/watch loops, and `codex exec resume` for external schedulers or CI. Scheduled tasks are
+managed in the ChatGPT desktop app, not Codex CLI or the IDE extension.
```

Keep the current plugin install commands and `$makeloop:makeloop` examples unchanged.

### 3. `plugins/makeloop/README.md`

#### Current wording

```md
In the Codex app, enabled skills may appear in the slash command list, so type `/` and choose
**makeloop** when it is shown. In Codex CLI, use `/skills` to browse skills or call
`$makeloop:makeloop` directly.
```

```md
Codex run-mode recommendations are conservative:

| Need | Codex mode |
| --- | --- |
| Inspect the first iteration safely | Manual tick |
| Keep a closed goal alive in the same thread | `/goal` |
| Run from CI, cron, or an external wrapper | `codex exec resume` |
| Keep an open watcher alive in this thread | Thread automation |
| Run independent/background watcher checks | Standalone/project automation |
```

#### Proposed diff

```diff
-In the Codex app, enabled skills may appear in the slash command list, so type `/` and choose
-**makeloop** when it is shown. In Codex CLI, use `/skills` to browse skills or call
-`$makeloop:makeloop` directly.
+In the ChatGPT desktop app's Codex view, open **Skills** or type `@`, then select **makeloop**.
+In Codex CLI or the IDE extension, use `/skills` to browse skills or call
+`$makeloop:makeloop` directly.
```

Apply the same terminology to the Runtime, output, and Codex packaging sections:

```diff
-continuation, Automations for heartbeat/watch loops, and `codex exec resume` for external
-schedulers or CI.
+continuation, host-supported Scheduled tasks for heartbeat/watch loops, and `codex exec resume`
+for external schedulers or CI.
```

```diff
-tick, a goal-backed continuation, an Automation heartbeat, or an external `codex exec resume`
-pipeline when the host supports that mode.
+tick, a goal-backed continuation, a host-supported Scheduled task, or an external
+`codex exec resume` pipeline. Scheduled setup is offered only on a host that can manage it.
```

```diff
 | Inspect the first iteration safely | Manual tick |
 | Keep a closed goal alive in the same thread | `/goal` |
 | Run from CI, cron, or an external wrapper | `codex exec resume` |
-| Keep an open watcher alive in this thread | Thread automation |
-| Run independent/background watcher checks | Standalone/project automation |
+| Keep an open watcher in the current desktop chat | Scheduled task inside this chat |
+| Run independent desktop watcher checks | Standalone scheduled task |
+| Run recurring watcher checks from CLI/IDE | External scheduler with `codex exec` / `codex exec resume` |
```

```diff
-run options: `/goal` for closed continuation, thread/standalone Automations for cadence and
-watchers, and `codex exec resume` for external orchestration. It describes these modes but does not
-create unattended schedulers unless the user explicitly asks.
+run options: `/goal` for closed continuation, scheduled tasks inside a chat or standalone
+scheduled tasks in the ChatGPT desktop app, and `codex exec resume` for external orchestration.
+CLI/IDE output does not offer Scheduled setup. The skill describes these modes but does not create
+unattended schedulers unless the user explicitly asks.
```

## Tier-3 anchor follow-up — excluded from this proposal diff

`plugins/makeloop/eval/codex-scenarios.md` is a trust anchor. Do not edit it while applying this
Tier-2 proposal. A separate human-authorized anchor window must update:

- C2: replace `thread automation` and `standalone/project automation` expectations with
  surface-gated Scheduled task terminology; CLI/IDE must not receive a Scheduled setup prompt.
- C5: replace the old slash-like app-entry assumption with ChatGPT desktop Skills/`@` and
  Codex CLI/IDE `/skills`/`$` behavior.
- Cross-cutting: require every offered run mode to be available on the active host while keeping
  exactly one recommended option and safe alternates.

Tier: **Tier 3 — human-window only**. This anchor follow-up is intentionally excluded from every
diff block above.

## Application order

1. Apply the `SKILL.md` Tier-2 adapter change.
2. Apply the two paired README corrections.
3. Run the gate and a maker != checker review of the three-file diff.
4. In a separate human-window, update C2/C5/cross-cutting and run the full Codex eval.

## Explicitly not proposed

- No edit to `commands/makeloop.md` or `templates/loop-prompt.tmpl.md`.
- No model-strength-based deletion or weakening of emitted rules.
- No top-level `/makeloop`, custom prompt revival, fake `/loop`, or runner creation.
- No `codex exec --last` redesign.
- No plugin metadata or marketplace layout change.
- No web Scheduled task for a local file-backed `.loop/` contract.
- No direct edit to `SELF-IMPROVEMENT.md`, `eval/`, `.githooks/`, or `.claude/settings.json`.

## Expected verification after Tier-2 apply

- `rg -n "slash menu|slash command list|thread automation|standalone/project automation|Codex Automations" plugins/makeloop/skills/makeloop/SKILL.md README.md plugins/makeloop/README.md`
  returns no stale positive claims.
- `rg -n "ChatGPT desktop app|Scheduled task|Codex CLI|IDE extension|codex exec resume" plugins/makeloop/skills/makeloop/SKILL.md README.md plugins/makeloop/README.md`
  shows the paired surface wording.
- `bash .githooks/gate.sh` prints `GATE PASS`.
- The canonical generator and template remain unchanged.
- The Tier-3 anchor window remains a separate diff and commit.

## Maker-checker review checklist

- The adapter still reads the canonical generator and template; no Steps 0-6 logic was copied.
- Desktop, CLI, IDE, and web capabilities are not conflated.
- Manual tick remains the safe first recommendation.
- Scheduled setup is offered only when the active host can manage it and the local loop contract is
  reachable.
- `/goal`, `$makeloop:makeloop`, plugin install commands, and `codex exec resume` remain unchanged.
- No emitted loop safety, gate, state/cursor, stop/dedup, or placeholder invariant was weakened.
