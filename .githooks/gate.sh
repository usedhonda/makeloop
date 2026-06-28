#!/usr/bin/env bash
# makeloop deterministic SAFETY gate (red-team unlock for Tier-1 auto-apply).
# Mechanically enforces SAFETY, not taste: guarded phrases intact, no gate-bypass clause
# added, trust anchor untouched, JSON valid, structure intact. Lives behind the trust anchor
# (.githooks/ -> settings deny + pre-commit + chmod), so the loop cannot edit the gate it runs.
# Usage: .githooks/gate.sh   (checks working tree vs HEAD + repo integrity). exit 0 = PASS.
set -u
root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root" || exit 2
cmd="plugins/makeloop/commands/makeloop.md"
tpl="plugins/makeloop/templates/loop-prompt.tmpl.md"
con="plugins/makeloop/SELF-IMPROVEMENT.md"
fail=0
err(){ echo "GATE FAIL: $*"; fail=1; }

# A) JSON validity
for j in .claude-plugin/marketplace.json plugins/makeloop/.claude-plugin/plugin.json .claude/settings.json; do
  python3 -m json.tool "$j" >/dev/null 2>&1 || err "invalid JSON: $j"
done

# B) command structure: Steps 0-6 present
for s in 0 1 2 3 4 5 6; do
  grep -q "^## Step $s" "$cmd" || err "missing Step $s"
done

# C) template both cores + key blocks present
for b in "CLOSED CORE" "OPEN CORE" "Two-stage gate" "Dedup/cursor" "Bootstrap block"; do
  grep -qF "$b" "$tpl" || err "template missing block: $b"
done

# D) guarded safety phrases intact (M2 — prune/auto-edit may not delete safety)
while IFS= read -r p; do
  [ -z "$p" ] && continue
  grep -qF "$p" "$cmd" "$con" || err "guarded safety phrase removed: $p"
done <<'PHRASES'
No self-grading
never delete, skip,
Intent deny-list
Security tax
monotonicity invariant
Tier 3
READ-ONLY
gate will be gamed
the wrong tool
STRENGTHEN a gate
PHRASES

# E) no source citation leaked into public files (provenance rule)
if git grep -niE 'kopadze|0xcodez|claudecode_ut|jason zhou|osmani|huntley|ghuntley|anatoli|amplitude|sondera|ingramhaus|timjwilliams|yannick|ouroboros|evoskills|redlib' -- plugins README.md >/dev/null 2>&1; then
  err "source citation leaked into a public file"
fi

# F) DIFF SAFETY (working tree + index vs HEAD)
names="$(git diff --name-only HEAD; git diff --cached --name-only)"
if printf '%s\n' "$names" | grep -qE '^(plugins/makeloop/SELF-IMPROVEMENT\.md|plugins/makeloop/eval/|\.claude/settings\.json|\.githooks/)'; then
  err "change touches a trust-anchor path (human-only, out-of-loop)"
fi

# G) no gate-bypass clause ADDED (C2/S10): an added line carrying BOTH a gate token and a
# bypass verb, excluding prohibitions (never/must not/do not).
skill="plugins/makeloop/skills/makeloop/SKILL.md"
added="$(git diff HEAD -- "$cmd" "$tpl" "$skill" | grep -E '^\+' | grep -vE '^\+\+\+' | grep -ivE 'never|must not|do not')"
if printf '%s\n' "$added" | grep -iE '(FINAL|SUCCESS CRITERIA|the gate|PASS =|stop condition)' | grep -iqE 'unavailable|skip|assume|treat[- ]as|fallback|degrade|bypass|when not present|fast-path'; then
  err "added a gate-bypass clause (C2/S10): a gate can be satisfied without the real check"
fi

if [ "$fail" -eq 0 ]; then
  echo "GATE PASS"
  exit 0
fi
echo "GATE BLOCKED"
exit 1
