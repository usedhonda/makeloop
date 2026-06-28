#!/usr/bin/env bash
# Lightweight Codex-surface check for makeloop self-improvement.
# This complements .githooks/gate.sh; it does not replace the trust-anchor gate.
set -u

root="$(git rev-parse --show-toplevel)" || exit 2
cd "$root" || exit 2

fail=0
err(){ echo "CODEX SURFACE FAIL: $*"; fail=1; }

market=".agents/plugins/marketplace.json"
plugin="plugins/makeloop/.codex-plugin/plugin.json"
skill="plugins/makeloop/skills/makeloop/SKILL.md"
ui="plugins/makeloop/skills/makeloop/agents/openai.yaml"
eval_file="plugins/makeloop/eval/codex-scenarios.md"
shim="plugins/makeloop/scripts/install-codex-prompt-shim.mjs"

for f in "$market" "$plugin" "$skill" "$ui" "$eval_file" "$shim"; do
  [ -f "$f" ] || err "missing file: $f"
done

python3 -m json.tool "$market" >/dev/null 2>&1 || err "invalid JSON: $market"
python3 -m json.tool "$plugin" >/dev/null 2>&1 || err "invalid JSON: $plugin"
node --check "$shim" >/dev/null 2>&1 || err "invalid JS syntax: $shim"

grep -q '^name: makeloop$' "$skill" || err "skill frontmatter missing name: makeloop"
grep -q '^description: ' "$skill" || err "skill frontmatter missing description"
grep -qF '$makeloop' "$skill" || err "skill does not expose $makeloop usage"
grep -qF 'Do not generate a Claude Code `/loop` or `/ralph-loop` launch line' "$skill" \
  || err "skill missing Codex no-/loop adaptation"
grep -qF '1 watcher tick' "$skill" || err "skill missing open watcher tick launch form"
grep -qF '1 iteration' "$skill" || err "skill missing closed iteration launch form"

grep -qF 'Codex surface and shim' "$eval_file" || err "Codex eval missing surface scenario"
grep -qF 'Does not emit `/loop`, `/ralph-loop`, or `codex-loop`' "$eval_file" \
  || err "Codex eval missing Claude-only launch ban"

if [ -e /Users/usedhonda/.agents/skills/makeloop ]; then
  target="$(readlink /Users/usedhonda/.agents/skills/makeloop || true)"
  expected="$root/plugins/makeloop/skills/makeloop"
  [ "$target" = "$expected" ] || err "dev-machine symlink points to $target, expected $expected"
fi

if [ "$fail" -eq 0 ]; then
  echo "CODEX SURFACE PASS"
  exit 0
fi
echo "CODEX SURFACE BLOCKED"
exit 1
