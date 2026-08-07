# Fable-era Codex surface delta

Date: 2026-08-07

## Task intent

Identify only the post-2026-07-01 Codex-side deltas that matter to makeloop's run-mode contract,
launch surface, and Codex documentation. This is a read-only implementation review; no generator,
skill, README, eval, hook, or governance file was changed.

## Sources checked

Primary sources:

- Current Codex manual, refreshed on 2026-08-07:
  <https://developers.openai.com/codex/codex-manual.md>
- Current skill activation and discovery contract:
  <https://learn.chatgpt.com/docs/build-skills>
- Current scheduled-task surfaces and permission model:
  <https://learn.chatgpt.com/docs/automations>
- Current Goal mode contract:
  <https://learn.chatgpt.com/docs/long-running-work>
- Current CLI command reference:
  <https://learn.chatgpt.com/docs/developer-commands?surface=cli>
- July 2026 product changes:
  <https://learn.chatgpt.com/docs/changelog#codex-2026-07-30-app>
- Codex CLI 0.146.0 release notes:
  <https://github.com/openai/codex/releases/tag/rust-v0.146.0>

Runtime corroboration on this machine used Codex CLI 0.147.0. `codex plugin marketplace --help`
and `codex exec resume --help` agree with the current command reference.

## Verdict

Two material post-baseline deltas exist. Both concern the Codex launch/run surface, so neither is a
Tier-1 additive edit. The implementation should be one paired Tier-2 proposal for the skill and
README surfaces, followed by a human-window Tier-3 update to `eval/codex-scenarios.md`.

The Fable-class-model assumption does not justify removing or weakening any emitted loop contract.
No model-strength-based deletion is recommended.

## Delta 1: desktop skill entrypoint moved away from the old slash-list story

### Current repo claim

- `plugins/makeloop/skills/makeloop/SKILL.md:28` says the skill is selected from the slash menu in
  the Codex app.
- `README.md:33` and `plugins/makeloop/README.md:27` make the same slash-list claim.

### Current official behavior

- On 2026-07-09 the Codex app merged into the ChatGPT desktop app; Codex remains a dedicated view.
- Current skill docs say explicit selection is `@` in ChatGPT, while Codex CLI and the IDE extension
  use `/skills` or `$` mentions.
- The current docs expose a Skills sidebar/deep link in the desktop app. They do not promise that an
  installed skill appears as a typed slash command.
- `$makeloop:makeloop` remains a valid plugin-namespaced Codex skill form; official plugin examples
  continue to use `$plugin-name:skill-name`.

### Candidate

Replace the app-side invocation statement with a surface-specific contract:

- ChatGPT desktop app, Codex view: open Skills or type `@`, then select `makeloop`.
- Codex CLI/IDE: use `/skills` or explicitly invoke `$makeloop:makeloop`.
- Do not promise a top-level `/makeloop` or a skill entry in the slash list.
- Rename prose references from "Codex app" to "ChatGPT desktop app, Codex view" where the product
  surface matters.

### Tier

- `SKILL.md` plus paired README corrections: **Tier-2 proposal**. This changes the documented Codex
  invocation surface covered by the Codex adapter invariant.
- C5 and cross-cutting eval wording: **Tier-3 anchor**, human-window only.

## Delta 2: Automations terminology and availability are now surface-specific

### Current repo claim

- `SKILL.md` recommends "thread automation" for same-thread watchers and
  "standalone/project automation" for independent runs.
- Its open-loop setup prompt can be emitted without first distinguishing desktop app from CLI/IDE.
- Both READMEs and C2 use the older Automation terminology.

### Current official behavior

- The current product name is **Scheduled tasks**.
- Same-context recurrence is a **scheduled task inside a chat**.
- Independent recurrence is a **standalone scheduled task**.
- Local scheduled tasks can run in the project directory or an isolated worktree in the ChatGPT
  desktop app.
- Codex CLI and the IDE extension do not provide the Scheduled management interface. They can only
  prepare or test the prompt/skill/script.
- Web scheduled tasks cannot directly use a local folder or worktree. A file-backed
  `.loop/<slug>.md` therefore requires the desktop app's local-project surface, or an external
  CLI scheduler.
- Official guidance still says to test the prompt manually before scheduling it, matching
  makeloop's manual-first safety policy.

### Candidate

Make run-mode recommendation conditional on the active host:

| Host and intent | Recommended wording |
| --- | --- |
| Any host, first open tick | Manual watcher tick |
| ChatGPT desktop app, preserve current chat context | Scheduled task inside this chat |
| ChatGPT desktop app, independent runs | Standalone scheduled task; choose local project or isolated worktree explicitly |
| Codex CLI/IDE, recurring watcher | External scheduler plus `codex exec`/`codex exec resume`; do not emit a Scheduled setup prompt |
| Web scheduled task with local `.loop/` file | Wrong surface unless the durable contract is moved to accessible uploaded/project/connected context |

Update the setup prompt and `Codex run options` labels to use those exact terms. Preserve the
existing requirements for a manual first tick, cursor/dedup, explicit scheduling intent, and no
silent scheduler creation.

### Tier

- `SKILL.md` run-mode table, launch/setup forms, and paired README wording: **Tier-2 proposal**.
  This changes Codex run-surface decision logic and user-visible launch guidance.
- C2 plus cross-cutting host-capability expectations: **Tier-3 anchor**, human-window only.

## Contracts that remain current

These areas do not need a post-baseline change:

- `/goal` is a current, non-experimental surface in the ChatGPT desktop app, Codex CLI, and IDE.
  Keeping the saved state file as the loop ledger remains compatible.
- `codex exec resume [SESSION_ID]` and `--last` remain current. `--last` selects the newest recorded
  session from the current working directory, so an external scheduler must own that session
  unambiguously. This is an existing operational caveat, not a post-2026-07-01 delta.
- `codex plugin marketplace add usedhonda/makeloop` and
  `codex plugin add makeloop@makeloop` match the current stable CLI grammar.
- `$makeloop:makeloop` remains the correct explicit plugin-skill invocation in Codex CLI.
- The file-backed `.loop/<slug>.md` plus state/cursor contract remains the right single coupling
  point. No runner or fake `/loop` command should be added.

## Fable-class model judgment

- **Delete:** none. The three hearts, t=0 policy, no-fake-done, maker != checker, gate honesty,
  state/cursor, stop/dedup, and placeholder checks are properties of the emitted artifact, not
  compensation for a weaker model.
- **Add:** only surface-awareness before recommending a run mode: identify whether the request is
  running in desktop Codex, CLI, IDE, or web, and offer only modes that surface can actually
  create/manage. This addition is justified by product capability, not model intelligence.
- **Keep:** thin-reader architecture. Fable-class execution does not justify copying canonical
  generator logic into `SKILL.md`.

## Tier summary

| Candidate | Tier |
| --- | --- |
| Additive model-strength hint or contract deletion | Rejected; no earned weight |
| Correct desktop invocation and product name in SKILL/README | Tier-2 proposal |
| Make Scheduled recommendations host-aware and rename run modes | Tier-2 proposal |
| Update C5 for Skills/@ vs CLI `/skills`/`$` | Tier-3 anchor |
| Update C2/cross-cutting for scheduled-task host capability | Tier-3 anchor |

Tier-1 candidate count: **0**. The narrow Tier-1 class does not cover Codex run-surface changes,
and the governance contract explicitly assigns those changes to Tier 2 with paired adapter review.

## Proposed implementation boundary

One Tier-2 proposal should update only:

- `plugins/makeloop/skills/makeloop/SKILL.md`
- `README.md`
- `plugins/makeloop/README.md`

One separate human-window Tier-3 change should update only:

- `plugins/makeloop/eval/codex-scenarios.md`

Do not mix in `codex exec --last` redesign, model-based prompt pruning, plugin metadata, runner
creation, or canonical generator changes.
