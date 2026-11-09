# RepoFix audit — makeloop — 2026-11-09

## Scope and delivery

Audited all 47 tracked files at `usedhonda/makeloop@559f887b1264a6e54a2a67aac196c178d0aa382e`. Each retrieved/reused file was verified against its Git blob SHA; the local frozen tree also matches `6c781a6f99b2b340b78b62fbf98f8d748b16e6cb`. Read AGENTS.md, both host surfaces, command/template/references, runtime helpers, manifests, governance, hooks, scenario fixtures and tests. Existing PRs #9 and #10 are merged into this baseline; there were no open issues.

The fixes are independently reviewable:

- [PR #11](https://github.com/usedhonda/makeloop/pull/11): preserve existing legacy prompt files.
- [PR #12](https://github.com/usedhonda/makeloop/pull/12): preserve personal-rule replacement lineage.
- The companion checker PR carrying this audit: exact saved-path validation, consistent recognized launch detection, and one proven low-value test removal.

No installed skill, real personal store/transcript, source project, Goal, scheduler, paid model endpoint, user configuration, deployment or default branch was modified. Protected governance, eval, settings and hooks remain byte-identical. The canonical generator/template and host lifecycle policy are unchanged.

## Reproduced findings

| Boundary | Failure on frozen main | Correction and evidence |
| --- | --- | --- |
| Optional legacy prompt installer | Unconditional write truncated a customized prompt, followed a final symlink to overwrite its target, and rewrote an identical shim | Exclusive `wx` creation; exact existing regular content is a no-op; other existing paths fail without replacement. Three actual-CLI temporary-home regressions failed before and pass after. |
| Personal-rule replacement | Reusing `rid` in the replacement loop made the adoption decision point to the old rule and the old rule link to itself | Separate replaced IDs from the new ID. One test covers both same-cause automatic replacement and explicit replacement, verifies the selected active rule and decision snapshot, and preserves prior decisions. Both modes failed before the fix. |
| Saved contract/state references | `.loop/example.md.backup`, `.mdx`, child/prefixed paths, and state suffix variants could satisfy substring checks | Require a complete lexical saved-path reference, with positive quote/punctuation controls. Keep the existing fence and shell parsing. This is structural validation, not arbitrary natural-language interpretation. |
| Recognized Goal setup outside final launches | The checker accepted affirmative `Use create_goal for the objective in PATH` / `create_goal: PATH` as a runnable final option but missed those same forms in progress, an unselected purpose, or unconfigured output | Use the same recognized forms in launch detection. Strengthen existing regressions for raw/fenced alternatives and retain ordinary feature-mention positive controls. |

The checker regressions produced 20 failing subcases across six definitions against the original checker, then passed. Subcases are not counted as separate top-level tests. No actual launch content was executed.

## Test-value audit

The per-definition ledger in `REPOFIX-TEST-LEDGER-2026-11-09.jsonl` covers every baseline definition and addition, including the removed record. It records assertion evidence, actual production or template/checker routes, keep/remove rationale and validation limitations. Static text sentinels are labeled as such; authored fixtures do not establish native host compliance.

| Metric | Baseline | Combined final |
| --- | ---: | ---: |
| Python definitions / executed unittest cases | 81 | 82 |
| Node installer definitions / executed cases | 0 | 3 |
| Total definitions | 81 | 85 |
| Test-bearing files | 5 | 6 |
| Physical test-file lines | 1,145 | 1,245 |
| Deleted definitions | — | 1 |
| Consolidated definitions | — | 0 |
| Added definitions | — | 5 |
| Unread definitions | 0 | 0 |

**85 = 81 − 1 deleted − 0 consolidated + 5 added.** This is not a net suite-size or speed reduction claim.

Removed `test_rendered_files_survive_save_and_readback`: the only filesystem writer was the test's own `Path.write_text`; it then read those bytes with Python and rechecked an already-covered authored fixture. No production writer or native host path was exercised. Retained bound-rendering, existing-state preservation and JSON-ledger cases cover the actual checker/template assertions.

Separately removed one tautological evidence-row uniqueness assertion: the tested table primary key and `put(id=value.id)` already enforce that property. Cold-tail/backfill and incremental evidence tests remain. Repaired the changed-source regression to select pending evidence instead of already-reviewed evidence, so it reaches the source-freshness check. A temporary in-memory freshness bypass made the repaired test fail. Five existing checker definitions were strengthened; no duplicate definitions were added for those failure modes.

## Executed validation

- Frozen baseline: `python3 -m unittest discover -s plugins/makeloop/validation -p 'test_*.py' -v` — **81/81 PASS**.
- Combined final, same command — **82/82 PASS**.
- `node --test plugins/makeloop/validation/test_prompt_shim.mjs` — **3/3 PASS**.
- All Python source parses; all tracked JSON parses; repository safety gate, staged pre-commit guard and diff whitespace checks pass.
- Independent source/test review covered the installer and checker changes. Remote published blob hashes are checked against the validated bytes.

The Node suite changes only the child process's home-directory lookup to a temporary fixture. The learning suite uses synthetic logs/projects/SQLite stores. No model generation, native Goal/pause/resume, clipboard, live schedule or end-to-end host evaluation was run. Existing protected semantic/golden evaluations were inventoried, not represented as newly executed. Passing the deterministic safety gate is not a semantic evaluation result.

## Compatibility and remaining limits

No model pin, package dependency, storage schema or version metadata change is required by these narrow helper/checker corrections. Existing corrupt historical learning records are not silently migrated. Installer first-write crash atomicity and adversarial filesystem races beyond exclusive final-path creation are not promised. The output checker remains a bounded structural checker, with independent semantic review required by its own documentation.

Current host invocation/documentation drift and broader lifecycle changes are already recorded in `.loop/proposals/fable-era-codex-surface.md` and related proposals. This audit does not silently adopt those outstanding proposal changes. The current official model/host inventory follows below.

## Model, API and host-contract inventory

Audit date: 2026-11-09. Frozen baseline: `usedhonda/makeloop@559f887b1264a6e54a2a67aac196c178d0aa382e` (both plugin manifests: `0.12.0`).

## Result

No inference model, provider endpoint, model SDK, or model version is selected by this repository. The product is a prompt-generating plugin for an existing Claude Code or Codex host. Its command, skill and template inherit the host's configured model and available tools. There is no justified provider/model migration in this change.

All **47 frozen files** were included in the model/API/dependency surface inventory, including the six tracked proposals and historical host research. [file inventory](REPOFIX-FILE-INVENTORY-2026-11-09.jsonl) records each path, baseline hash, role and executable imports. Generated Python caches are excluded. The aggregate per-definition audit above covers all tests.

The current official contracts support keeping the existing plugin formats and explicit legacy shim. The known desktop invocation guidance drift remains covered by the existing Codex-surface proposal; this audit does not promote that proposal or alter protected eval/governance files.

## Actual repository surfaces

| Surface | Actual contract or implementation | Assessment |
| --- | --- | --- |
| `commands/makeloop.md` | Canonical Steps 0–6 produce file-backed loop contracts; host-loaded Markdown and tool instructions, with no model pin or API call. | Keep model selection with the host. Literal prompt invariants are product source, not a reason to introduce an inference SDK. |
| `skills/makeloop/SKILL.md` | Thin host-aware adapter reads the shared command, references and template; `$makeloop:makeloop` is the explicit Codex skill form. | Keep shared-source architecture. Native discovery and actual per-session capability remain distinct from documentation. |
| `skills/makeloop/agents/openai.yaml` | Display name, short description, default prompt and `allow_implicit_invocation`; no model/API key/provider configuration. | OpenAI-named metadata is not an OpenAI API integration. Current skill documentation still supports this metadata file. [S1] |
| `templates/loop-prompt.tmpl.md` | Closed/open cores and optional verification, handoff, pause, recovery and learning instructions. | Host/model-independent prompt product. No model-strength-based deletion or automatic simplification is warranted without representative output evaluation. |
| `references/codex.md` | Conditional `/goal`, ordinary execution, scheduled-task setup, and exact-session `codex exec resume`; lifecycle tools are conditional on the exposed session contract. | The documented modes remain current. CLI help corroborates external-resume syntax; it does not establish native Goal/tool availability in a particular session. [S2, S3] |
| `references/claude-code.md` | Conditional `/goal`, `/loop`, optional installed Ralph invocation, host cancellation/resume and evaluator boundaries. | Current official docs corroborate goal evaluation from surfaced conversation, counter resets on resume, fixed/self-paced loop differences and seven-day recurring expiry. No Claude executable was available for native verification. [S4, S5] |
| Remaining four references | Project profile, output guide, feedback design and user-local learning guidance. | Generation/verification and local-data contracts, without an inference endpoint or pinned model. Do not confuse fixture validation with blind generation or semantic grading. |
| `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` | Skills directory plus UI metadata, relative local plugin source, `AVAILABLE` installation and `ON_INSTALL` authentication policy. | Current OpenAI docs retain the compatibility manifest and marketplace format. A portable root `plugin.json` is an available authoring format, not a required repair for this supported package. [S6] |
| `.claude-plugin/plugin.json` and root `.claude-plugin/marketplace.json` | Claude plugin identity/version and a relative marketplace source; default `commands/` and `skills/` directories. | Current Claude docs still support these paths. They prefer skills for new plugins, while existing commands remain supported. Host-discovered aliases must govern actual invocation. [S7] |
| `scripts/install-codex-prompt-shim.mjs` | Node built-ins write a Markdown prompt at the documented default `~/.codex/prompts/makeloop.md`; no Codex process or model is launched. | Custom prompts are explicitly deprecated by current official docs. Keep this optional legacy compatibility helper; do not claim current slash-menu discovery or promote it over skills. The exclusive-create fix prevents overwriting an existing custom file or following a final-path symlink. [S8] |
| `scripts/local-learning.py` | Python standard-library local file/JSON/SQLite handling and personal-rule state; no provider client. | Host history/storage compatibility is a local data-format boundary, not a model API. No actual user store was read or changed by this inventory. Native host data formats were not validated with real stores. |
| `validation/check_outputs.py` | Deterministic Python checker consumes supplied artifact strings and authored scenario data. It never executes launch blocks. | Standard-library only. A PASS is structural output validation; it is not native execution, model generation or independent semantic review. |
| Five baseline Python test files and four JSON fixture files | Mock/synthetic local-learning tests, checker tests, source-string sentinels, authored template rendering, and scenario/feedback trace data. | No inference request is made. All test definitions are covered in the aggregate ledger. |
| `eval/scenarios.md`, `eval/codex-scenarios.md` | Protected golden semantic rubrics. | No model runner or paid API implementation is shipped in these files. They were left unchanged, and no generation/eval result is inferred from the deterministic test suite. |
| `AUTOMATION.md`, `SELF-IMPROVEMENT.md`, repository hooks/settings | Operator runbook, protected governance and deterministic Git safety gates. The runbook describes `claude -p ... --permission-mode acceptEdits`. | Current Claude CLI docs retain that grammar. The local cron wrapper described under `.loop/` is not part of the 47-file tracked snapshot; neither an installed cron nor a real pause flag was inspected or created. Protected files were read only. [S9] |
| READMEs, engineering notes, `AGENTS.md`, metadata | Installation/run-surface instructions and historical decisions; no inference implementation. | `AGENTS.md` is supported by current Claude versions, subject to version and instruction-file selection. Host availability must still be checked in the target session. [S10] |
| Six `.loop/proposals/fable-era-*.md` files and `docs/log/codex/011-fable-era-codex-surface-delta.md` | Historical research and proposed prompt/host changes. “Fable-class” is a design assumption, not a live model identifier. | Existing proposals were inventoried, not executed, adopted or treated as current runtime proof. |

Paths under `commands/`, `skills/`, `templates/`, `references/`, `scripts/`, `validation/` and `eval/` in this table are relative to `plugins/makeloop/`.

## CLI and dependency evidence

Only read-only help/version commands were run:

| Command | Observed result |
| --- | --- |
| `/opt/codex/bin/codex --version` | `codex-cli 0.167.0-alpha.4` |
| `codex --help` | Exposes `plugin`, `exec`, `resume` and other host commands; no model run initiated. |
| `codex plugin marketplace add --help` | Accepts a local path, `owner/repo[@ref]`, HTTPS or SSH Git source; repository installation example has compatible grammar. |
| `codex plugin add --help` | Accepts `PLUGIN@MARKETPLACE`; `makeloop@makeloop` is syntactically consistent. |
| `codex exec resume --help` | Accepts `[SESSION_ID] [PROMPT]`; `--last` selects the newest session. The repository's exact-ID rule avoids ambiguous unattended selection. |

Help output proves parser grammar only. No plugin was installed, no marketplace configuration or authentication was read/changed, and no Goal, schedule, conversation or model invocation was started. The installed alpha version is an observation, not a recommended upgrade target. Claude was absent.

There is no `package.json`, Python requirement file, lockfile or vendored inference dependency in the frozen tree. The two shipped helper scripts and deterministic checker import only Node/Python standard-library modules. There is therefore no package/API/model version to bump as an obsolescence repair. Runtime support requirements and native host behavior are not established by this observation.

## Existing host-documentation follow-up

Both READMEs still describe choosing makeloop from the Codex app slash menu. Current official skill guidance describes **ChatGPT Skills / `@`** and **Codex CLI or IDE `/skills` / `$`**. The historical research note and `.loop/proposals/fable-era-codex-surface.md` already identify this drift and the paired host/eval review it requires. [S1]

The same existing proposal covers Scheduled task terminology and surface availability. Current documentation confirms the CLI/IDE lack the Scheduled management interface and web tasks cannot retain a local folder/worktree between runs. The active Codex host reference already carries those capability/file-access cautions. Do not create a duplicate proposal or silently adopt the older draft as a current implementation. [S3]

This remains a documentation follow-up, not a new native failure reproduced during this audit. No protected eval, governance, hook, setting, host prompt or model-selection source was changed by this audit.

## Current official sources

These sources were opened on 2026-11-09. Repository findings come from the frozen files; the sources below establish host contracts, not runtime verification of this plugin.

- **S1 — Skills and metadata:** https://learn.chatgpt.com/docs/build-skills — ChatGPT `@`, Codex `/skills`/`$`, progressive loading and optional `agents/openai.yaml`.
- **S2 — Goal surface:** https://learn.chatgpt.com/docs/long-running-work — `/goal` on desktop, CLI and IDE, scope/verification and unchanged access boundaries.
- **S3 — Scheduled tasks:** https://learn.chatgpt.com/docs/automations — surface-specific management and local-versus-web file availability.
- **S4 — Claude goals:** https://code.claude.com/docs/en/goal — transcript-based evaluator, cancellation and resume counter behavior.
- **S5 — Claude loops:** https://code.claude.com/docs/en/scheduled-tasks — fixed/self-paced loops, native cancellation, expiry and resume exceptions.
- **S6 — OpenAI plugin packaging:** https://developers.openai.com/plugins/build/plugins — current portable format and continued `.codex-plugin/plugin.json` compatibility, marketplace configuration and path rules.
- **S7 — Claude plugin reference:** https://code.claude.com/docs/en/plugins-reference — supported manifest/component directories and command namespacing.
- **S8 — Legacy custom prompts:** https://learn.chatgpt.com/docs/custom-prompts — deprecated status, default local prompts directory and skills as the supported reusable-instruction route.
- **S9 — Claude CLI grammar:** https://code.claude.com/docs/en/cli-reference — print mode and accepted permission modes.
- **S10 — Instruction-file discovery:** https://code.claude.com/docs/en/memory — current `AGENTS.md` support and its version/selection conditions.

## Limits

No paid/live model request, blind generation, golden semantic grading, native plugin discovery, Goal lifecycle, scheduling, actual user history/store, or permission/configuration mutation was performed. A passing source/fixture check is not a claim about those boundaries. The helper's filesystem-safety regression is synthetic process execution with a stubbed home directory; it does not establish current Codex legacy-prompt discovery.
