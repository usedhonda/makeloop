# Human-window proposal: FINAL is a convergence token, not a harness stop

Status: proposal only. Do not auto-apply. Tier-2 (human GO).

Intent: clarify that makeloop's `FINAL` is its own **contractual convergence token**, not a
built-in `/loop` harness stop. In self-paced mode the model stops itself after FINAL; in forced
fixed-interval mode the loop **cannot self-stop** and runs until the user stops it or the 7-day
expiry. This is a factual-accuracy strengthening (no rule loosened), so `.githooks/gate.sh`
should still print `GATE PASS` with it applied. No trust-anchor path is touched.

Provenance: candidate L2 in `.local/makeloop-research/fable-era-delta-2026-08-07.md` (see its §5
Evidence appendix). This candidate also closes the delta report's open A-scan finding A16
(FINAL-token unverified). No URLs / authors / absolute paths carried in.

Mirror applicability: this touches the **emitted contract** (the completion-token semantics),
so the generator prose and the template comment move together in the **same commit**. Sites are
listed below; note that the closed-loop self-paced default (`makeloop.md:311-312`) is already
correct and does not change.

---

## Candidate L2 — fixed-interval `/loop` has no self-stop; prefer self-paced for closed loops

Tier: **Tier-2** (emitted contract accuracy; affects every closed loop).

Target files & current wording (lines approximate; match on the quoted text):

- `commands/makeloop.md` Step-4 completion-token line (~325-326):
  ```
  Completion token (closed only): `FINAL` for built-in `/loop`; `<promise>DONE</promise>` for
  ralph-loop.
  ```
- `templates/loop-prompt.tmpl.md` header comment (:9):
  ```
  completion token: FINAL for built-in /loop (self-paced/interval); <promise>DONE</promise> for ralph-loop.
  ```
- Already-correct (no change): `commands/makeloop.md:311-312` — "Built-in `/loop` self-paced —
  omit the interval; iterate until done. ... (Recommended default.)".

Proposed diff (generator prose):

```diff
 Completion token (closed only): `FINAL` for built-in `/loop`; `<promise>DONE</promise>` for
 ralph-loop.
+
+FINAL is makeloop's **contractual convergence token, not a harness stop** — the built-in /loop
+harness has no FINAL stop token. In **self-paced** mode (interval omitted) the model stops
+itself after printing FINAL (it does not reschedule / it signals stop), so FINAL genuinely ends
+the run — this is why self-paced is the recommended default for closed loops. In **forced
+fixed-interval** mode the loop CANNOT self-stop: it keeps firing on the interval until the user
+stops it or the 7-day expiry, and FINAL is only a marker in the transcript. Prefer self-paced
+for drive-to-done; use a fixed interval only when cadence itself is the requirement.
```

`templates/loop-prompt.tmpl.md` (mirror, same commit):

```diff
-completion token: FINAL for built-in /loop (self-paced/interval); <promise>DONE</promise> for ralph-loop.
+completion token: FINAL for built-in /loop — a CONVERGENCE token, not a harness stop. Self-paced (interval omitted): the model self-stops after FINAL. Fixed-interval: no self-stop; runs until the user stops it or the 7-day expiry, FINAL is only a transcript marker -> prefer self-paced for closed loops. <promise>DONE</promise> for ralph-loop.
```

Rationale: makeloop emits "print FINAL and stop" as the completion token, but no FINAL stop
token exists in the built-in `/loop` harness. Self-paced mode makes FINAL effective (the model
declines to reschedule); fixed-interval mode does not (only the user or the 7-day expiry stops
it). Making this explicit prevents a user from forcing a fixed interval on a drive-to-done loop
and expecting FINAL to end it.

## Not proposed

- No change to the self-paced-default recommendation (already correct at `makeloop.md:311-312`).
- No `/schedule` adoption; the 7-day-expiry reference is factual, shared with candidate L1.
- No change to ralph-loop's `<promise>DONE</promise>` token.

## Post-apply verification

- `bash .githooks/gate.sh` prints `GATE PASS`.
- `rg -n "convergence token|not a harness stop|self-stop" plugins/makeloop/commands/makeloop.md plugins/makeloop/templates/loop-prompt.tmpl.md` shows the clarification on both files.
- A generated closed loop still emits `FINAL` as its completion token and recommends self-paced.
