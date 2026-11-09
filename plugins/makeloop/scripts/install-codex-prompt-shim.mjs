#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const promptsDir = path.join(os.homedir(), ".codex", "prompts");
const promptPath = path.join(promptsDir, "makeloop.md");

const prompt = `---
description: Generate a Codex-ready makeloop prompt contract
argument-hint: "[goal hint (optional)]"
---

Use the $makeloop:makeloop skill to generate a Codex-ready loop prompt contract.

Optional goal hint:
$ARGUMENTS
`;

fs.mkdirSync(promptsDir, { recursive: true });
try {
  // Exclusive creation also refuses symlinks and a file created by another installer.
  fs.writeFileSync(promptPath, prompt, { encoding: "utf8", flag: "wx" });
  console.log(`installed legacy Codex prompt shim: ${promptPath}`);
} catch (error) {
  if (error.code !== "EEXIST") throw error;
  if (fs.lstatSync(promptPath).isFile() && fs.readFileSync(promptPath, "utf8") === prompt) {
    console.log(`legacy Codex prompt shim already installed: ${promptPath}`);
  } else {
    console.error(`Refusing to replace existing prompt: ${promptPath}. Move it aside explicitly before installing.`);
    process.exitCode = 1;
  }
}
if (!process.exitCode) {
  console.log(
    "Note: custom prompts are deprecated and current Codex CLI builds may not show /prompts:makeloop. Use $makeloop:makeloop or /skills when it is not listed.",
  );
}
