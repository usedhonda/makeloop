# Human-window proposal: OPEN-loop caveats (7-day expiry + event-push hint)

Status: proposal only. Do not auto-apply. Tier-2 (human GO).

Intent: two additive, factual accuracy fixes to the OPEN CORE run-mode / runtime surface. Both
are strengthening-only (no rule loosened, no capability removed), so `.githooks/gate.sh` should
still print `GATE PASS` with them applied — unlike the anchor-touching `codex-*` proposals in
this directory, these edit only the canonical generator and its template, no trust-anchor path.

Provenance: candidates L1 and L4 in `.local/makeloop-research/fable-era-delta-2026-08-07.md`
(see its §5 Evidence appendix). No URLs / authors / absolute paths are carried into this tracked
file per the provenance rule in `plugins/makeloop/SELF-IMPROVEMENT.md`.

Both candidates touch the **emitted contract**, so each must be mirrored across the canonical
generator (`plugins/makeloop/commands/makeloop.md`) AND the template
(`plugins/makeloop/templates/loop-prompt.tmpl.md`) in the **same commit**. Note the drift trap
that motivated commit 8ba1944: the canonical file embeds its OWN copy of the OPEN CORE inside a
fenced block, so an OPEN-core edit has a canonical-prose site, a canonical-embedded-template
site, AND a `tmpl.md` site. All matching sites must move together.

---

## Candidate L1 — `/loop` watchers self-expire after 7 days; annotate "run-indefinitely"

Tier: **Tier-2** (OPEN CORE RUN MODE / STOP semantics — affects every generated open loop).

Target files & current wording (lines approximate; match on the quoted text):

- `commands/makeloop.md` OPEN CORE RUN MODE (embedded template, ~481-483):
  ```
  RUN MODE: <run-indefinitely>   # steady-state watcher; never prints a completion token
    # OR <stop-on-event>: the first time the trigger fires, NOTIFY then print "TRIGGERED" and exit.
  There is NO FINAL and NO "all criteria met -> stop" — those are closed-loop notions.
  ```
- `commands/makeloop.md` OPEN CORE STOP WHEN (embedded template, ~494):
  ```
  - never              : run-indefinitely; stops only when user / scheduler stops it.
  ```
- `templates/loop-prompt.tmpl.md` RUN MODE (:89) and STOP WHEN (:95):
  ```
  RUN MODE: <run-indefinitely>  # never prints a token   OR  <stop-on-event>  # first fire -> NOTIFY, print "TRIGGERED", exit
  STOP WHEN: never (run-indefinitely) / event-fired [stop-on-event] / watch-target-gone / budget (cap -> notify+exit).
  ```

Proposed diff (additive caveat; do NOT adopt `/schedule` — this only redirects to the existing
EXTERNAL-scheduler guidance in the Scheduled-loop safety block):

```diff
 RUN MODE: <run-indefinitely>   # steady-state watcher; never prints a completion token
   # OR <stop-on-event>: the first time the trigger fires, NOTIFY then print "TRIGGERED" and exit.
 There is NO FINAL and NO "all criteria met -> stop" — those are closed-loop notions.
+  # CAVEAT: a bare built-in /loop watcher SELF-EXPIRES 7 days after creation (fires one last
+  # time, then deletes itself). "run-indefinitely" therefore means "until stopped OR that
+  # 7-day expiry". For a truly unbounded watcher, drive it from an EXTERNAL scheduler
+  # (OS cron / CI / Actions) per the Scheduled-loop safety block — not a bare /loop.
```

```diff
-- never              : run-indefinitely; stops only when user / scheduler stops it.
+- never              : run-indefinitely; stops only when user / scheduler stops it — but a bare
+                       built-in /loop also self-expires 7 days after creation, so use an EXTERNAL
+                       scheduler (Scheduled-loop safety block) for a genuinely unbounded watcher.
```

`templates/loop-prompt.tmpl.md` (mirror, same commit):

```diff
-RUN MODE: <run-indefinitely>  # never prints a token   OR  <stop-on-event>  # first fire -> NOTIFY, print "TRIGGERED", exit
+RUN MODE: <run-indefinitely>  # never prints a token (but a bare /loop self-expires 7d after creation -> external scheduler for unbounded)   OR  <stop-on-event>  # first fire -> NOTIFY, print "TRIGGERED", exit
```

```diff
-STOP WHEN: never (run-indefinitely) / event-fired [stop-on-event] / watch-target-gone / budget (cap -> notify+exit).
+STOP WHEN: never (run-indefinitely; bare /loop still self-expires 7d after creation -> external scheduler) / event-fired [stop-on-event] / watch-target-gone / budget (cap -> notify+exit).
```

Rationale: makeloop's OPEN CORE emits "STOP WHEN: never (run-indefinitely)", but a built-in
`/loop` recurring task automatically expires 7 days after creation (fires one final time, then
deletes itself). A watcher meant to run forever silently dies at day 7. This is a factual
accuracy fix that points at the generator's existing EXTERNAL-scheduler block; it is NOT a
`/schedule` adoption (which remains rejected per the delta report §4).

---

## Candidate L4 — add an event-push (Channels) hint beside Monitor / cron

Tier: **Tier-2** (OPEN CORE in-loop hint line; additive).

Target files & current wording — **THREE sites** (the report cites only two; the canonical's
embedded RUNTIME line is the third and is the 8ba1944 drift trap if missed):

- `commands/makeloop.md` Step-4 in-loop hint (generator prose, ~331-332):
  ```
  ... One hint for the loop body
  (not a launch line makeloop can emit): for live-stream watching use the **Monitor** tool; for
  wall-clock schedules use a **cron routine** — both are in-loop tool calls.
  ```
- `commands/makeloop.md` OPEN CORE RUNTIME (embedded template, ~485-486):
  ```
  RUNTIME: /loop <interval> for cadence polling. For live-stream watching use the Monitor tool;
  for wall-clock schedules use a cron routine — those are in-loop tool calls, not launch lines.
  ```
- `templates/loop-prompt.tmpl.md` RUNTIME (:90):
  ```
  RUNTIME: /loop <interval> for cadence; live-stream -> Monitor; wall-clock -> cron routine (in-loop tool calls).
  ```

Proposed diff (add a third hint — event-driven push as a low-latency alternative to interval
polling when a real event source exists):

```diff
 ... One hint for the loop body
 (not a launch line makeloop can emit): for live-stream watching use the **Monitor** tool; for
-wall-clock schedules use a **cron routine** — both are in-loop tool calls.
+wall-clock schedules use a **cron routine**; and when a real event source exists (CI, a
+webhook), have it **push into the session directly (Channels)** instead of interval polling —
+all three are in-loop tool calls / integrations, not launch lines.
```

```diff
 RUNTIME: /loop <interval> for cadence polling. For live-stream watching use the Monitor tool;
-for wall-clock schedules use a cron routine — those are in-loop tool calls, not launch lines.
+for wall-clock schedules use a cron routine; and if a real event source exists, have it push the
+event into the session directly (Channels) instead of interval polling — those are in-loop tool
+calls / integrations, not launch lines.
```

`templates/loop-prompt.tmpl.md` (mirror, same commit):

```diff
-RUNTIME: /loop <interval> for cadence; live-stream -> Monitor; wall-clock -> cron routine (in-loop tool calls).
+RUNTIME: /loop <interval> for cadence; live-stream -> Monitor; wall-clock -> cron routine; event-push -> Channels (in-loop tool calls).
```

Rationale: makeloop's OPEN runtime hints are poll-based (`/loop <interval>`) plus Monitor
(live-stream) and cron (wall-clock). When the watched system can push events, reacting to the
push is lower-latency than interval polling. This is a purely additive third hint in the same
line family.

---

## Not proposed

- No `/schedule` / Cloud Routines adoption (rejected in delta report §4). L1 only redirects to
  the generator's existing EXTERNAL-scheduler guidance; it does not add a new launch surface.
- No change to the completion-token semantics (that is candidate L2, a separate proposal).
- No new OPTIONAL block; both edits stay inside existing OPEN CORE lines.

## Post-apply verification

- `bash .githooks/gate.sh` prints `GATE PASS` (no anchor path touched; edits are additive).
- `rg -n "self-expire|7 days after creation|7d after creation" plugins/makeloop/commands/makeloop.md plugins/makeloop/templates/loop-prompt.tmpl.md` shows the L1 caveat on both files.
- `rg -n "Channels" plugins/makeloop/commands/makeloop.md plugins/makeloop/templates/loop-prompt.tmpl.md` shows the L4 hint at all three sites.
- The generated OPEN loop for a "watch app.log" scenario still emits the OPEN CORE (no FINAL, no closed-loop notions).
