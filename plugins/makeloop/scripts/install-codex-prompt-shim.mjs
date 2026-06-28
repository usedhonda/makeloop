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

Use the $makeloop skill to generate a Codex-ready loop prompt contract.

Optional goal hint:
$ARGUMENTS
`;

fs.mkdirSync(promptsDir, { recursive: true });
fs.writeFileSync(promptPath, prompt, "utf8");
console.log(`installed Codex prompt shim: ${promptPath}`);
