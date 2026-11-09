import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

const installer = fileURLToPath(new URL("../scripts/install-codex-prompt-shim.mjs", import.meta.url));

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "makeloop-shim-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const preload = path.join(root, "home.mjs");
  // Invoke the actual CLI with a synthetic home; never change the process HOME.
  fs.writeFileSync(preload, `import os from "node:os"; os.homedir = () => ${JSON.stringify(root)};\n`);
  const prompt = path.join(root, ".codex", "prompts", "makeloop.md");
  fs.mkdirSync(path.dirname(prompt), { recursive: true });
  const run = () => spawnSync(process.execPath, ["--import", preload, installer], { encoding: "utf8" });
  return { root, prompt, run };
}

test("creates the shim and leaves an identical existing file untouched", (t) => {
  const { prompt, run } = fixture(t);
  assert.equal(run().status, 0);
  const bytes = fs.readFileSync(prompt);
  assert.match(bytes.toString(), /Use the \$makeloop:makeloop skill/);
  assert.match(bytes.toString(), /\$ARGUMENTS/);
  const before = fs.statSync(prompt);
  assert.equal(run().status, 0);
  assert.deepEqual(fs.readFileSync(prompt), bytes);
  assert.equal(fs.statSync(prompt).mtimeMs, before.mtimeMs);
});

test("refuses an existing customized prompt without changing its bytes", (t) => {
  const { prompt, run } = fixture(t);
  const custom = "My existing prompt with local instructions.\n";
  fs.writeFileSync(prompt, custom);
  const result = run();
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /existing/i);
  assert.equal(fs.readFileSync(prompt, "utf8"), custom);
});

test("refuses a prompt symlink without modifying its target", (t) => {
  const { root, prompt, run } = fixture(t);
  const target = path.join(root, "owned.md");
  fs.writeFileSync(target, "Keep this unrelated file.\n");
  fs.symlinkSync(target, prompt);
  assert.notEqual(run().status, 0);
  assert.equal(fs.readFileSync(target, "utf8"), "Keep this unrelated file.\n");
  assert.equal(fs.lstatSync(prompt).isSymbolicLink(), true);
});
