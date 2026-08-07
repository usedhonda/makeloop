# Human-window proposal: generator-side miscellany (tool rename, wrong-tool pointer, era-number)

Status: proposal only. Do not auto-apply. Mixed tier — see each candidate.

Intent: three small generator-only fixes. None touches the emitted template, none touches a
trust-anchor path, so `.githooks/gate.sh` should still print `GATE PASS` with them applied.

Provenance: candidates G1, L5, and the marginal era-number note in
`.local/makeloop-research/fable-era-delta-2026-08-07.md` (see its §5 Evidence appendix). No URLs
/ authors / absolute paths carried in.

Mirror applicability: **all three are generator-only — NO template mirror.** They live solely in
`plugins/makeloop/commands/makeloop.md`; the applier should not hunt for a `tmpl.md` counterpart.

---

## Candidate G1 — `allowed-tools` subagent-dispatch token: `"Task"` -> `"Agent"`

Tier: **Tier-2** (frontmatter). Non-behavioral future-proofing (see verified facts below).

Target file & current wording:

- `commands/makeloop.md` frontmatter (:4):
  ```
  allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "Write", "Task"]
  ```

Proposed diff:

```diff
-allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "Write", "Task"]
+allowed-tools: ["Read", "Glob", "Grep", "Bash", "AskUserQuestion", "Write", "Agent"]
```

Verified facts (established in the same investigation as the delta report; postdates the report
body, which had listed this as a verify item — originates there as A-scan finding 5 / G1):

- The subagent-dispatch tool was renamed `Task` -> `Agent` in v2.1.63.
- `Task` **survives as an alias**, so the current frontmatter is NOT broken today.
- A command's `allowed-tools` is a **pre-approval list only** — it does not gate tool
  availability. So neither the old token nor the rename changes what /makeloop can actually do.

Because of the above, this is a **non-behavioral, future-proofing** edit: it aligns the token
with the current tool name against the day the `Task` alias is eventually retired. No functional
break either way.

Note on Step-1 dispatch prose (~109-111): it already reads tool-neutrally — "dispatch an
`Explore` subagent (or 2-3 in parallel)" names the subagent TYPE, not the tool — so it needs no
change. `SendMessage` is not added: /makeloop's Explore usage is fire-and-collect (dispatch,
read findings), which does not require continuing a running agent.

---

## Candidate L5 — one-line wrong-tool pointer to `/batch` / Workflow for many independent units

Tier: **Tier-1** (additive pointer).

Target file & current wording:

- `commands/makeloop.md` Step-1 loop-fit classification (~188-192):
  ```
  - **Mature repo, still no gate** → a loop is likely the wrong tool; say so plainly (a single
    good prompt usually wins).
  - **Greenfield / early** → "no gate" is expected, nothing's built yet. Do NOT call the loop a
    bad fit. The loop's *first job is to create its gate* (scaffold + a first failing acceptance
    test); see Step 3's bootstrap guidance and the Bootstrap block in Step 5.
  ```

Proposed diff (add a sibling loop-fit note after the greenfield bullet):

```diff
   - **Greenfield / early** → "no gate" is expected, nothing's built yet. Do NOT call the loop a
     bad fit. The loop's *first job is to create its gate* (scaffold + a first failing acceptance
     test); see Step 3's bootstrap guidance and the Bootstrap block in Step 5.
+  - **Decomposes into many independent units** → a single loop may be the wrong shape; work that
+    splits into many parallel, independently-checkable pieces can fit `/batch` (worktree-isolated
+    subagents each opening a PR) or the Workflow tool better than one serial loop. A one-line
+    pointer only — full multi-agent orchestration stays out of scope (deferred per the roadmap).
```

Rationale: makeloop already flags when a loop is the wrong tool (mature repo, no gate). This adds
the "highly parallel / decomposable" case as a one-line pointer, consistent with the existing
wrong-tool guidance. Deliberately just a pointer — adopting multi-agent `/batch` / Workflow as an
actual run mode remains deferred (delta report §4).

---

## Candidate (marginal) — generalize the era-bound "~turn 47" number

Tier: **Tier-1**, optional. Model-independence hygiene — NOT a rule weakening.

Target file & current wording:

- `commands/makeloop.md` Re-anchor principle (:38-40):
  ```
  - **Re-anchor, don't drift**: a long run loses its "do not touch" boundaries as context
    grows (rules tend to evaporate by ~turn 47). Make the loop *re-read its contract* (goal +
    criteria + rules) every iteration, and prefer many short fresh-context iterations over one
    long one.
  ```

Proposed diff:

```diff
 - **Re-anchor, don't drift**: a long run loses its "do not touch" boundaries as context
-  grows (rules tend to evaporate by ~turn 47). Make the loop *re-read its contract* (goal +
+  grows (rules tend to evaporate deep into a long run). Make the loop *re-read its contract* (goal +
   criteria + rules) every iteration, and prefer many short fresh-context iterations over one
   long one.
```

Rationale: "~turn 47" is an era-bound empirical figure tied to a specific model/harness. Per C5
model-independence, replacing the hardcoded number with a model-agnostic phrasing keeps the
principle current across models. **This is NOT a C5-forbidden weakening**: the re-anchor RULE
(re-read the contract every iteration; prefer short fresh-context iterations) is fully preserved
— only the stale number is generalized. It is the one candidate in this set closest to a
removal, so it is explicitly marked optional: if the applier judges any text removal too
aggressive, skip it with no loss to the other candidates.

---

## Not proposed

- No template mirror for any candidate (all generator-only).
- No `SendMessage` addition (fire-and-collect Explore needs none).
- No multi-agent `/batch` / Workflow run-mode adoption (L5 is a pointer only).
- No removal of the re-anchor rule itself; the marginal edit only generalizes one number.

## Post-apply verification

- `bash .githooks/gate.sh` prints `GATE PASS`.
- `rg -n '"Agent"' plugins/makeloop/commands/makeloop.md` shows the renamed frontmatter token;
  `rg -n '"Task"' plugins/makeloop/commands/makeloop.md` returns nothing.
- `rg -n "Decomposes into many independent units|/batch" plugins/makeloop/commands/makeloop.md` shows the L5 pointer.
- `rg -n "turn 47" plugins/makeloop/commands/makeloop.md` returns nothing (if the marginal edit was taken); `rg -n "deep into a long run"` shows the generalized phrasing.
- No new match appears in `plugins/makeloop/templates/loop-prompt.tmpl.md` (all generator-only).
