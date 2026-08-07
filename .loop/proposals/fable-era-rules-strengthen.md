# Human-window proposal: strengthen emitted RULES (liveness, grounded progress, safe-decline retry, checker cadence)

Status: proposal only. Do not auto-apply. Mixed tier — see each candidate.

Intent: four additive / strengthening edits to the emitted loop contract. Every one is
monotonic (adds capability or strengthens a gate; none loosens a rule), so `.githooks/gate.sh`
should still print `GATE PASS` with them applied. No trust-anchor path is touched. These are
general loop-robustness improvements, framed model-neutrally so the emitted template runs on any
user model (the emitted template is provider-neutral by design).

Provenance: candidates R1-R4 in `.local/makeloop-research/fable-era-delta-2026-08-07.md` (see its
§5 Evidence appendix). No URLs / authors / absolute paths carried in.

Mirror discipline (the 8ba1944 drift class): the canonical generator
`plugins/makeloop/commands/makeloop.md` **embeds its own copy** of the CLOSED CORE and OPEN CORE
RULES; `plugins/makeloop/templates/loop-prompt.tmpl.md` holds the second copy. Any emitted-RULES
edit must move ALL matching sites in the **same commit**. Each candidate lists its exact sites.

---

## Candidate R1 — loop liveness / no premature termination (2 clauses)

Tier: **Tier-1** (a new OPTIONAL block for autonomous loops; purely additive, monotonic).

Framed as a general loop failure class (liveness / no premature termination), NOT as a
model-specific crutch, so it traces to the stop taxonomy contract and stays C5-safe.

Target sites (a NEW optional block + one Step-5 trigger-row mention):

- `commands/makeloop.md` — insert a new block after the **No-progress circuit breaker** block
  (~555), current tail:
  ```
  - Hash {tool name + args} for each action this iteration and keep a short window. The same
    action repeated (3rd identical call, or >85% similar plan/action across iterations) means
    stuck -> stop_reason=no-progress. Don't keep paying for a spin.
  ```
- `templates/loop-prompt.tmpl.md` — insert the mirror after the tmpl No-progress block (~133).
- `commands/makeloop.md` Step-5 profile table, autonomous row (~357):
  ```
  | Any autonomous (self-paced) loop | **Budget block** + stop reasons `no-progress`, `oscillation`, `failure`; **No-progress circuit breaker** |
  ```

Proposed diff — new canonical block (after No-progress circuit breaker):

```diff
+
+**Liveness — no premature termination** (autonomous / unattended; complements the stop
+taxonomy):
+```
+- Before ending a turn, check the last paragraph: if it is a plan, a question, a next-steps
+  list, or an unexecuted "I'll now ..." promise, execute it as a tool call in THIS turn before
+  yielding. A turn that only describes the next action has not taken it.
+- Context remaining is not a stop_reason. The loop halts ONLY through its own stop taxonomy or
+  the escalation handoff — never because context feels low, and never by proposing a new
+  session / summarize / self-trim. Do NOT emit an unverifiable capacity claim (e.g. "ample
+  context remaining"); state only what a tool result shows.
+```
```

Proposed diff — tmpl mirror (after tmpl No-progress block):

```diff
+
+## [autonomous loop] Liveness — no premature termination
+- Before ending a turn, inspect the last paragraph: plan / question / next-steps / unexecuted
+  promise -> run it as a tool call this turn before yielding.
+- Context remaining is not a stop_reason; halt only via the stop taxonomy or escalation handoff,
+  not by proposing a new session / summarize. Don't emit an unverifiable "ample context" claim.
```

Proposed diff — Step-5 profile table row (wire the new block):

```diff
-| Any autonomous (self-paced) loop | **Budget block** + stop reasons `no-progress`, `oscillation`, `failure`; **No-progress circuit breaker** |
+| Any autonomous (self-paced) loop | **Budget block** + stop reasons `no-progress`, `oscillation`, `failure`; **No-progress circuit breaker**; **Liveness — no premature termination** |
```

Optional note (verified mechanism, not required by the diff): when a loop is packaged/launched as
a skill, `disallowed-tools: AskUserQuestion` mechanically enforces the existing "no questions
mid-loop" rule.

Rationale: autonomous runs occasionally end a turn on an unexecuted promise, or halt out of
context-budget anxiety. Clause (a) makes the loop finish the action it announced; clause (b)
keeps context pressure from short-circuiting the stop taxonomy while explicitly forbidding a
fabricated capacity claim (fabrication-adjacent, and it must not contradict the existing
Escalation-handoff block).

---

## Candidate R2 — ground progress/observation claims in this session's tool results

Tier: **Tier-2** (core RULES; affects every loop). Strengthens the existing No-fake-done gate.

Target sites — **FOUR** (No-fake-done in both cores, both files):

- `commands/makeloop.md` CLOSED No-fake-done (~422-423):
  ```
  - No fake done: no placeholders, stubs, or TODOs reported as complete; never delete, skip,
    or weaken a check to make the gate go green.
  ```
- `commands/makeloop.md` OPEN No-fake-done (~508-509):
  ```
  - No fake done: never fabricate or suppress an observation to stay quiet, and never weaken the
    trigger to silence it — a fire must reflect a real event.
  ```
- `templates/loop-prompt.tmpl.md` CLOSED No-fake-done (:56) and OPEN No-fake-done (:102) (same
  text, single-line form).

Proposed diff — CLOSED (canonical; mirror the added line into tmpl:56):

```diff
 - No fake done: no placeholders, stubs, or TODOs reported as complete; never delete, skip,
   or weaken a check to make the gate go green.
+- Ground every claim: before reporting progress or printing the completion token, audit each
+  claim against a tool result from THIS session. Report only work you can point to; mark
+  anything unverified as unverified. No status you cannot tie to a tool result.
```

Proposed diff — OPEN (canonical; mirror into tmpl:102):

```diff
 - No fake done: never fabricate or suppress an observation to stay quiet, and never weaken the
   trigger to silence it — a fire must reflect a real event.
+- Ground every claim: before firing or reporting "all quiet", audit the observation against a
+  tool result from THIS tick. A fire cites concrete evidence; silence means you actually read
+  the signal and found nothing new — never an assumed state.
```

Rationale: additive strengthening of No-fake-done / First-VERIFY honesty — anchoring reported
status to an actual tool result from the current session sharply reduces fabricated progress
reports. C5-safe: it strengthens the existing no-fake-done characteristic, removes nothing.

---

## Candidate R3 — retry ladder: safety/policy decline branch (provider-neutral)

Tier: **Tier-2** (emitted retry ladder; affects every closed loop).

Target sites — **TWO** (closed-only; the open core has no retry-by-failure-class line):

- `commands/makeloop.md` CLOSED retry ladder (~428-430):
  ```
  - Retry by failure class: rate-limit -> back off; validation fail -> rewrite from the
    feedback (no blind retry); transient 5xx -> retry once or twice then move on; tool
    unavailable -> pause and surface it (don't burn retries).
  ```
- `templates/loop-prompt.tmpl.md` CLOSED retry ladder (:59):
  ```
  - Retry by failure class: rate-limit->backoff; validation->rewrite-from-feedback; 5xx->retry then move on; tool-unavailable->pause+notify.
  ```

Proposed diff — canonical:

```diff
 - Retry by failure class: rate-limit -> back off; validation fail -> rewrite from the
   feedback (no blind retry); transient 5xx -> retry once or twice then move on; tool
-  unavailable -> pause and surface it (don't burn retries).
+  unavailable -> pause and surface it (don't burn retries); safety/policy decline -> do NOT
+  retry the identical request (verbatim retry just spins) — escalate / hand off, since even a
+  benign security or similar task can trip a safeguard.
```

Proposed diff — tmpl:59 (mirror):

```diff
-- Retry by failure class: rate-limit->backoff; validation->rewrite-from-feedback; 5xx->retry then move on; tool-unavailable->pause+notify.
+- Retry by failure class: rate-limit->backoff; validation->rewrite-from-feedback; 5xx->retry then move on; tool-unavailable->pause+notify; safety/policy decline->don't retry verbatim, escalate/handoff.
```

Rationale: the current ladder has no branch for a safety/policy decline, so an unattended loop
whose gate runs security work (secret scan / SAST) can spin forever on a verbatim retry when a
benign task is declined. Written provider-neutrally ("safety/policy decline", not an
provider-specific `stop_reason:"refusal"` wiring) because the emitted template runs on any user
model. Additive robustness = handling a runtime signal, not compensating for a model defect.

---

## Candidate R4 — concretize maker != checker (cadence + fresh/separate context + spec)

Tier: **Tier-2** (checker prescription).

Primary site — **generator-only** (Step-4 Independent completion check, no template mirror):

- `commands/makeloop.md` (~319-323). NOTE: this same block is also touched by
  `fable-era-goal-launch.md` (candidate L3); if both proposals are applied, merge the two
  additions to the block.
  ```
  **Independent completion check** (the `/goal` pattern, **closed loops only**): "the gate
  passes" is objective and self-grading is fine for it. But "the *goal* is met" should not be
  decided by the maker when it can't be fully reduced to the gate — have a separate checker (a
  sub-agent, ideally a different model, seeing the spec + diff but not the maker's reasoning)
  confirm completion before the loop prints its completion token.
  ```

Proposed diff — canonical Step-4:

```diff
 **Independent completion check** (the `/goal` pattern, **closed loops only**): "the gate
 passes" is objective and self-grading is fine for it. But "the *goal* is met" should not be
 decided by the maker when it can't be fully reduced to the gate — have a separate checker (a
 sub-agent, ideally a different model, seeing the spec + diff but not the maker's reasoning)
 confirm completion before the loop prints its completion token.
+Make the check concrete, not aspirational: run it at a set cadence (e.g. every N iterations and
+before the completion token), in a fresh / separate context (a subagent, ideally a different
+model family), verifying the work against the written spec — a fresh-context verifier tends to
+outperform the maker's self-critique.
```

Optional secondary (emitted RULES; **only if** the concretized cadence should ship inside the
generated loop, not just guide /makeloop). If taken, mirror BOTH sites in the same commit:

- CLOSED emitted maker != checker — `commands/makeloop.md:418` + `templates/loop-prompt.tmpl.md:53`:
  ```
  - maker != checker: on risky changes, re-verify with fresh eyes / a sub-agent.
  ```
  → append: `... at a set cadence, in a fresh/separate context, against the spec.`
- OPEN emitted maker != checker — `commands/makeloop.md:501-503` +
  `templates/loop-prompt.tmpl.md:99`: the "re-verify with fresh eyes / a sub-agent ... verify the
  action before its side effect" line — leave as-is unless the same cadence phrasing is wanted;
  the open watcher's checker is per-fire, not per-cadence, so the secondary edit is CLOSED-focused.

Rationale: makeloop's maker != checker is implemented; this only sharpens the vague
"re-verify with a sub-agent" into an explicit cadence + fresh/separate context + spec check,
which is the stronger, documented practice. No new capability, no rule removed.

---

## Not proposed

- No weakening of any existing RULES line; every edit is additive.
- No model-name hardcoding and no "the model is smart, so drop this" removal (C5 monotonicity).
- R3 stays provider-neutral — no provider-specific `stop_reason` / API wiring in the emitted
  template.
- R4's emitted-RULES change is left OPTIONAL; the default is the generator-only Step-4 sharpen.

## Post-apply verification

- `bash .githooks/gate.sh` prints `GATE PASS`.
- `rg -n "Liveness — no premature termination|Context remaining is not a stop_reason" plugins/makeloop/commands/makeloop.md plugins/makeloop/templates/loop-prompt.tmpl.md` shows R1 on both files plus the Step-5 trigger row.
- `rg -n "Ground every claim" plugins/makeloop/commands/makeloop.md plugins/makeloop/templates/loop-prompt.tmpl.md` shows R2 at all four No-fake-done sites (two per file).
- `rg -n "safety/policy decline" plugins/makeloop/commands/makeloop.md plugins/makeloop/templates/loop-prompt.tmpl.md` shows R3 on both retry-ladder sites.
- `rg -n "at a set cadence|fresh-context verifier|against the written spec" plugins/makeloop/commands/makeloop.md` shows R4's Step-4 sharpen.
- The golden eval (`plugins/makeloop/eval/scenarios.md`) still grades green (three hearts, right blocks, no bloat) after the edits.
