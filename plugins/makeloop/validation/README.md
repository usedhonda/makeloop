# Generated-output validation

The protected `../eval/scenarios.md` and `../eval/codex-scenarios.md` remain the golden gates.
This directory supplements them with the purpose-choice, copy, capability and resume cases for
the native launch update. It does not change their expected properties or authorize execution.

`scenarios.json` contains synthetic requests/profiles and checker metadata. Generate each request
using the current command, selected profile/host references, output guide, canonical template and
Codex skill when appropriate. Give the maker only `id`, `request` and `profile`, not expected results.
Use text-only generation, no project work or live schedules; retain outputs locally, not in Git.
Do not create new agents or delegate repo work without authorization. Existing host model access
can produce text-only test artifacts; never silently fall back to a paid API credential.

Expected output is a JSON array with one object per scenario:

```json
[
  {
    "id": "scenario-id",
    "files": {
      ".loop/example.md": "complete rendered contract",
      ".loop/example-state.md": "complete state (cursor JSON string for open loops)",
      ".loop/INDEX.md": "index entry"
    },
    "chat": "complete response, including the actual Markdown copy blocks and explanations"
  }
]
```

Unresolved purpose comparisons return `files: {}`. Refine cases include unchanged state in the
output map so its bytes can be compared; this does not instruct the generator to overwrite it.

Run the independent deterministic checker against the generated artifacts:

```sh
python3 plugins/makeloop/validation/check_outputs.py cases.json outputs.json
```

The checker inspects saved-file/kind/copy/state contracts; it never executes launch content.
It does **not** prove good explanations, correct real-world commands, or absence of semantic
gate bypasses. A checker who did not generate the examples must also grade all applicable
protected golden properties and the following acceptance criteria:

- alternatives differ meaningfully in purpose or execution mode and preserve the accepted scope;
- each explains suitability, effects, boundaries, checks, stopping and resume;
- explanation and the complete chosen Loop body appear only in the final package; resolved launch
  blocks are its last section, with nothing following the last fence;
- recommendation and every copy block agree on purpose, host, paste destination and exact state;
- unselected purposes do not create files or start work; existing progress/cancellation survives;
- unknown features are not runnable fences; exact-session shell examples quote spaced paths;
- expected repair RED proceeds, regression RED stops, missing/invalid proof is still acquired;
- valid unaffected green is reused; fresh signals remain fresh; native completion is not proof;
- no check weakening, invented success, source citations or operational secrets in output.

Record per-case results and evidence locally. Run the golden batch once after stabilization;
rerun only affected failed cases after a concrete correction. Synthetic generation is not a
live scheduled run, desktop paste test, or proof of production host availability.

The user explicitly replaced launch-first presentation with final-only, launch-last ordering.
The protected eval's old launch-first assertions are superseded **only** for presentation order;
all file/kind/safety/t=0/launch-content requirements remain enforced. Do not edit the protected
eval to hide that difference. Existing valid contract artifacts can be reused while separately
re-rendering changed presentation; do not repeat unchanged contract generation merely for layout.
