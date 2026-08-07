# Human-window proposal: add `/goal` as an optional Step-4 launch surface

Status: proposal only. Do not auto-apply. Tier-2 (human GO).

Intent: offer `/goal` (native drive-to-done with a fresh small-model evaluator) as an OPTIONAL
Step-4 launch option for closed loops, WITHOUT letting its native evaluator be mistaken for the
independent sub-agent checker makeloop already prescribes. The native check is a **supplement,
not a replacement** — that caveat is mandatory in the diff.

Provenance: candidate L3 in `.local/makeloop-research/fable-era-delta-2026-08-07.md` (see its §5
Evidence appendix). No URLs / authors / absolute paths carried in.

Mirror applicability: **generator-only — NO template mirror.** Step 4 is /makeloop's own
decision dialog, not emitted loop text, so this edit lives solely in
`plugins/makeloop/commands/makeloop.md`. The applier should not hunt for a `tmpl.md` counterpart.

Availability gate: `/goal` availability must be verified on the target Claude Code before this
lands (it is version-gated and was not in this session's skill roster). Human GO is required —
this changes Step-4 decision logic.

---

## Candidate L3 — `/goal` as an optional closed-loop launch option

Tier: **Tier-2** (Step-4 decision logic).

Target file & current wording (lines approximate; match on the quoted text):

- `commands/makeloop.md` Step-4 runtime menu (~311-315):
  ```
  - **Built-in `/loop` self-paced** — omit the interval; iterate until done. Best for
    goal-completion. (Recommended default.)
  - **Built-in `/loop <interval>`** — e.g. `/loop 30m ...`; cadence-based. Ask for interval.
  - **ralph-loop plugin `/ralph-loop`** — built-in stop machinery (`--max-iterations N`,
    `--completion-promise '<TAG>'`).
  ```
- `commands/makeloop.md` Independent completion check (~319-323):
  ```
  **Independent completion check** (the `/goal` pattern, **closed loops only**): "the gate
  passes" is objective and self-grading is fine for it. But "the *goal* is met" should not be
  decided by the maker when it can't be fully reduced to the gate — have a separate checker (a
  sub-agent, ideally a different model, seeing the spec + diff but not the maker's reasoning)
  confirm completion before the loop prints its completion token.
  ```

Proposed diff (add `/goal` to the menu; extend the completion-check note with the
supplement-not-replacement caveat):

```diff
 - **Built-in `/loop` self-paced** — omit the interval; iterate until done. Best for
   goal-completion. (Recommended default.)
 - **Built-in `/loop <interval>`** — e.g. `/loop 30m ...`; cadence-based. Ask for interval.
+- **Built-in `/goal` (closed loops only; verify availability first)** — drives across turns to
+  a completion condition, with a fresh small-model evaluator judging "done". Offer it when the
+  goal is expressible as a single completion condition. Its native evaluator SUPPLEMENTS, does
+  NOT REPLACE, the independent sub-agent checker below (see the caveat there).
 - **ralph-loop plugin `/ralph-loop`** — built-in stop machinery (`--max-iterations N`,
   `--completion-promise '<TAG>'`).
```

```diff
 **Independent completion check** (the `/goal` pattern, **closed loops only**): "the gate
 passes" is objective and self-grading is fine for it. But "the *goal* is met" should not be
 decided by the maker when it can't be fully reduced to the gate — have a separate checker (a
 sub-agent, ideally a different model, seeing the spec + diff but not the maker's reasoning)
 confirm completion before the loop prints its completion token.
+  - If the loop launches via `/goal`, its native evaluator (a small fast model, likely the same
+    family) is a CONVENIENCE that SUPPLEMENTS this checker — it does not satisfy the
+    maker != checker requirement on its own. For risky or spec-heavy goals still run the
+    independent sub-agent checker (ideally a different model family) against the spec + diff.
```

Rationale: `/goal` is documented Claude Code behavior that matches makeloop's closed
"drive-to-done" semantics, and the Codex adapter already treats `/goal` as a launch surface. CC
currently borrows `/goal` only as a *concept name* for the independent check, never as an actual
launch line. Offering it as an option closes that gap. The mandatory caveat prevents the native
(small, likely same-family) evaluator from being read as a replacement for the stronger
different-family sub-agent checker makeloop requires.

## Not proposed

- No removal or weakening of the existing independent completion check — `/goal` is added
  beside it, and the caveat strengthens (not relaxes) maker != checker.
- No template mirror (Step 4 is generator dialog, not emitted loop text).
- No auto-selection of `/goal`; it stays an option the user picks, availability verified first.

## Post-apply verification

- `bash .githooks/gate.sh` prints `GATE PASS`.
- `rg -n "SUPPLEMENTS, does\n?|verify availability first|does not satisfy the" plugins/makeloop/commands/makeloop.md` (or a plain `rg -n "/goal" plugins/makeloop/commands/makeloop.md`) shows the new menu option and the supplement-not-replacement caveat.
- No new match appears in `plugins/makeloop/templates/loop-prompt.tmpl.md` (generator-only edit).
- A generated closed loop still prescribes the independent sub-agent checker before the token.
