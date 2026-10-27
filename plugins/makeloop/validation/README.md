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
It rejects malformed batches, duplicate IDs and unknown host/kind values before grading, so a
later duplicate cannot hide a failed artifact. Run its regression checks with:

```sh
python3 -m unittest discover -s plugins/makeloop/validation -p test_check_outputs.py -v
```

It does **not** prove good explanations, correct real-world commands, or absence of semantic
gate bypasses. A checker who did not generate the examples must also grade all applicable
protected golden properties and the following acceptance criteria:

- alternatives differ meaningfully in purpose or execution mode and preserve the accepted scope;
- each explains suitability, effects, boundaries, checks, stopping and resume;
- a concrete Loop brief covers the original purpose/actions, scope, criteria and actual stop/resume
  behavior. Grade its substance, not the presence of a literal English/Japanese title;
- explanations and the short saved-contract path appear in the final package; the full saved body
  appears only when explicitly requested (`show_body: true` in checker metadata). Resolved launch
  blocks are its last section, with nothing following the last fence;
- recommendation and every copy block agree on purpose, host, paste destination and exact state;
  compact launches may bind state in the saved contract rather than repeating its path. An explicit
  different state or a path-internal newline must still fail. Short text/fences do not prove GUI
  clipboard fidelity; that requires actual target-surface observation;
- unselected purposes do not create files or start work; existing progress/cancellation survives;
- unknown features are not runnable fences; exact-session shell examples quote spaced paths;
- expected repair RED proceeds, regression RED stops, missing/invalid proof is still acquired;
- valid unaffected green is reused; fresh signals remain fresh; native completion is not proof;
- no check weakening, invented success, source citations or operational secrets in output.

`goal_launch_required` marks a confirmed ready closed-completion scenario (including O1/O2 and
G1/G2). The structural check requires a `/goal` launch, or on a tool-capable Codex target an
affirmative setup beginning `Use create_goal for the objective in PATH` or `create_goal: PATH`.
It rejects mere mentions/negations and uses the existing exact contract/state checks for paths.
It does not prove arbitrary natural-language intent, runtime availability or actual Goal creation;
those still require the host evidence and semantic review above. G2 distinguishes a target CLI's
confirmed slash surface from the generator's tool list; it is a synthetic fixture, not a live run.

Recovery scenarios R1-Codex/R1-Claude require `completion_pair_required` and
`remediation_required`: a Goal-first pair, an ordinary non-tick alternative and a project-bound
REMEDIATION SCOPE section. The checker also rejects representative unqualified English/Japanese blocker exits
on CC. These are structural checks, not a general natural-language safety proof. Grade the
actual repair/stop decision, authorization sources and scoped alternatives independently.
F27-F34 cover repairable prerequisites, genuine authentication boundaries, changed hypotheses,
resume with cumulative state, uncertain external effects, required review waits and host enforcement. No fixture starts a native Goal.

The deterministic provenance check recognizes URLs in explicit source/reference/citation labels
or sections. Operational gate/target URLs and evidence links are valid contract content, not
automatically source citations. Unlabelled or differently formatted provenance still requires
the independent semantic check above; URL presence alone is not a rejection rule.

Record per-case results and evidence locally. Run the golden batch once after stabilization;
rerun only affected failed cases after a concrete correction. Synthetic generation is not a
live scheduled run, desktop paste test, or proof of production host availability.

The user explicitly replaced launch-first presentation with final-only, launch-last ordering.
The protected eval's old launch-first assertions are superseded **only** for presentation order;
file/kind/safety/t=0 requirements remain enforced. The later copy-improvement instruction also
supersedes mandatory full-body printing and mandatory state-path repetition in every launch;
state still must be bound to the saved contract and conflicting explicit paths remain invalid. Do not edit the protected
eval to hide that difference. Existing valid contract artifacts can be reused while separately
re-rendering changed presentation; do not repeat unchanged contract generation merely for layout.

## Feedback and recovery traces

`feedback-traces.json` supplements the golden generation cases with observed runtime situations.
It checks the decisions induced by a generated contract, not the presence of reassuring keywords.

1. Generate the named `contract_case` using only its request/profile and current skill sources.
   Keep `expect`, golden assertions and these traces hidden from that maker.
2. Give a fresh actor the generated contract/state plus each trace's `id` and `observation`.
   Ask for the next action, state changes and a short evidence-based reason. Do not provide
   `expect` or `rubric`, and do not execute external effects or the contract's launch commands.
3. Have an independent checker compare the response to every `expect` field and the behavioral
   rubric. Check the explanation as well as the declared decision; a correct boolean paired with
   a contradictory plan fails. Save actor outputs and per-case verdicts locally.

The expected fields describe observable decision facts. `new_project_work` excludes read-only
result reconciliation and checkpoint/native-stop handling. `reserve_new_attempt` means consuming
a new slot, not settling an interrupted one. `discard_pending` means forgetting an unsettled
effect; removing a confirmed receipt from pending is different. `force_approach_change` means
changing strategy solely because repetition hit a limit despite evidenced progress.

The traces cover useful repeated checks, cosmetic activity without progress, completed plans
with uncovered criteria, missing collection versus valid empty output, interruption at the last
budget slot, lost acknowledgements, retries behind the read frontier, separate failures of one
entity, failed observation and invalidated evidence. They are bounded decision simulations, not
proof that a host enforces prose budgets or that a destination supports exactly-once delivery.
Use a live host/destination test before claiming those guarantees.

Refine inputs must include the complete original contract when exact preservation is asserted.
M3 supplies that fixture and compares the entire cap-only replacement as well as unchanged state.
A summary of an unseen original file cannot establish byte-for-byte preservation.

## Calibration and maintenance

Check valid alternatives as well as plausible failures. A declared `LEARNINGS FILE` ledger is
auxiliary state, not a second contract; its declaration must not hide another closed/open core.
An independent grader must explain which criterion its evidence actually covers, including a
new/custom verifier's known-good and known-bad examples. Unknown coverage is not a passing score.

Record the source revision, available model/host/capabilities and input/state used in a check.
Compare optional scaffolding changes with acceptance and authority fixed; retain failed traces
and distinguish generator, checker and runtime defects. Synthetic results do not substitute for
target-host tests. Investigate observed run-to-run variability with focused repeats when needed;
never repeat until one passing sample can hide the failures.

## Continuation intent under unavailable runtimes

A known unavailable requested execution can set checker metadata `execution_unconfigured: true`.
That permits a saved contract plus an honest explanation without a runnable launch group; a
manual or invented goal launch is rejected for that unresolved request. This does not approve
changing the requested mode or prove the explanation is semantically complete. Preserve actual
contract/state bytes with `preserve` and independently inspect purpose, residual work, used and
remaining budget and its source/enforcement, authority, review and resume requirements.
M9/F16 and M10/F17 encode the 7/8 and 8/8 agent-default counter reports: missing native
resume is the technical constraint, not exhausted user authority. M11/F18 is the usable native
continuation positive contrast; M12/F19 differs by an explicit exhausted user limit. F20 contrasts
internal no-progress replanning with the user-selected no-progress stop in F2. Historical
fixtures never rewind live state. Checker metadata supplies expected readiness; its acceptance
does not independently derive feasibility or classify the semantic provenance of a limit.

These authored fixtures and checker regressions do not prove that a model completes the whole
generation workflow in one invocation. Read actual generated decisions against the original
request and state; a valid-looking compact command cannot replace readiness evidence.

Clear plain launch headings and A/B/C labels are valid as well as Markdown headings. The checker
still requires the final group to contain only its heading, ordered host/destination labels and
copy blocks, and rejects extra prose or trailing caveats. A known nonready request needs no
runnable-choice section. These structural allowances do not grade the brief's substance or
convert an unavailable requested mode into an executable one.

## Outcome-first task discovery

O1/O2 supply the same complete CSV use-path request on Codex/Claude Code: existing parser proof is
green, but app integration and saving are missing. O3 is the genuinely already-delivered contrast;
O4 explicitly chooses a single work unit without shrinking the overall result. F21-F26 check
missing-task discovery, original-purpose versus unrelated work, ordinary execution versus selected
single-pass boundaries, already-satisfied honesty and unresolved review waits. Existing M10-M12
retain runtime/limit contrasts. Grade whether generated work follows the actual original use or
delivery path, not just familiar headings. Keep outcome/acceptance/authority stable; derive necessary
checks within scope without inventing commands. These synthetic cases are not live host proof.

The outcome-first user instruction supersedes the protected eval's historical safe-first manual
recommendation for completion requests. Explicit one-pass requests remain bounded; watcher tick
semantics and all safety/state/acceptance properties remain unchanged. Do not edit protected eval
files to make this override disappear.

A single explained Codex choice needs no comparison-menu heading. Multiple choices still carry
Codex run options and must pass host/destination/order/final-only checks. First-VERIFY honesty
requires a real initial no-change success branch, not only a warning against partial green.
Independently check that Codex native success excludes incomplete checkpoints; reporting them
honestly does not authorize marking the native goal complete.
