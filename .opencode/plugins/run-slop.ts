import { spawn } from "node:child_process";
import { resolve as resolvePath } from "node:path";

import { Plugin } from "@opencode/plugin";

type RunSlopResult = {
  stdout: string;
  stderr: string;
  exitCode: number;
};

function runSlop(filePath: string): Promise<RunSlopResult> {
  return new Promise((resolve) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", filePath], {
      cwd: resolvePath(import.meta.dir, "../.."),
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (chunk: Buffer) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk: Buffer) => {
      stderr += chunk.toString();
    });
    child.on("error", (error) => {
      resolve({ stdout, stderr: `${stderr}${error.message}`, exitCode: 1 });
    });
    child.on("close", (exitCode) => {
      resolve({ stdout, stderr, exitCode: exitCode ?? 1 });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description: "Run a SlopLang file with Sloperator",
        input: {
          type: "object",
          properties: {
            filePath: { type: "string" },
          },
          required: ["filePath"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { filePath } = input as { filePath: string };
          const result = await runSlop(filePath);
          return { content: JSON.stringify(result) };
        },
      });
    });
  },
});
