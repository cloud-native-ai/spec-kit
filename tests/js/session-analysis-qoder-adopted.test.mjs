import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { QoderSessionAnalyzer } from "../../scripts/js/better-harness/session-analysis/platforms/qoder.mjs";

const SID = "11111111-2222-3333-4444-555555555555";

async function writeJsonl(filePath, records) {
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, records.map((r) => JSON.stringify(r)).join("\n") + "\n");
}

async function makeQoderFixture() {
  const root = await mkdtemp(path.join(os.tmpdir(), "qoder-ide-"));
  const home = path.join(root, ".qoder");
  const workspace = path.join(root, "workspace");
  await mkdir(workspace, { recursive: true });

  // project dir with a WRONG slug name — only cwd-in-file probing can find it
  const projectDir = path.join(home, "projects", "random-dir-name-not-a-slug");
  await writeJsonl(path.join(projectDir, `${SID}.jsonl`), [
    { type: "user", uuid: "u1", sessionId: SID, cwd: workspace, timestamp: "2026-07-01T10:00:00Z",
      message: { role: "user", content: "start the task" } },
    { type: "assistant", uuid: "a1", sessionId: SID, cwd: workspace, timestamp: "2026-07-01T10:01:00Z",
      message: { id: "chatcmpl-abcdef0123456789abcd", role: "assistant", model: "kmodel_latest",
        content: "working on it" } },
  ]);
  // another project dir whose sessions belong elsewhere
  const farDir = path.join(home, "projects", "other-project");
  await writeJsonl(path.join(farDir, "22222222.jsonl"), [
    { type: "user", uuid: "u2", sessionId: "22222222", cwd: path.join(root, "elsewhere"),
      timestamp: "2026-07-01T10:00:00Z", message: { role: "user", content: "x" } },
  ]);

  // IDE state.vscdb with the real per-session model
  const ideRoot = path.join(root, "Qoder", "User", "workspaceStorage", "hash1");
  await mkdir(ideRoot, { recursive: true });
  await writeFile(path.join(ideRoot, "workspace.json"),
    JSON.stringify({ folder: `file://${workspace}` }));
  const { DatabaseSync } = await import("node:sqlite");
  const db = new DatabaseSync(path.join(ideRoot, "state.vscdb"));
  db.exec("CREATE TABLE ItemTable(key TEXT PRIMARY KEY, value TEXT)");
  db.prepare("INSERT INTO ItemTable VALUES (?,?)").run(
    `chat.modelConfig.session.${SID}`, "qwen3.7-max");
  db.close();
  return { root, home, workspace, ideRoot };
}

test("qoder cwd-in-file probing finds sessions despite wrong dir slug", async () => {
  const { root, home, workspace } = await makeQoderFixture();
  try {
    const analyzer = new QoderSessionAnalyzer();
    const scope = await analyzer.resolveScope({ workspace, home });
    const roots = await analyzer.discoverSourceRoots(scope);
    const sessions = await analyzer.discoverSessions(scope, roots);
    const ids = sessions.map((s) => s.sessionId);
    assert.ok(ids.includes(SID), `must find session in non-slug dir, got ${ids}`);
    assert.ok(!ids.includes("22222222"), "far-workspace session must be filtered");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("qoder requestId extracted from chatcmpl- message ids", async () => {
  const { root, home, workspace } = await makeQoderFixture();
  try {
    const analyzer = new QoderSessionAnalyzer();
    const scope = await analyzer.resolveScope({ workspace, home });
    const roots = await analyzer.discoverSourceRoots(scope);
    const sessions = await analyzer.discoverSessions(scope, roots);
    const target = sessions.find((s) => s.sessionId === SID);
    const events = await analyzer.readSession(target, scope, {});
    const withRid = events.filter((e) => e.requestId);
    assert.equal(withRid.length, 1);
    assert.equal(withRid[0].requestId, "abcdef0123456789abcd");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("qoder IDE state.vscdb overlays real model over tier alias", async () => {
  const { root, home, workspace } = await makeQoderFixture();
  const originalHome = process.env.HOME;
  process.env.HOME = root; // qoderIdeUserDir reads ~/.config/Qoder/User
  try {
    await mkdir(path.join(root, ".config"), { recursive: true });
    const { rename } = await import("node:fs/promises");
    await rename(path.join(root, "Qoder"), path.join(root, ".config", "Qoder"));
    const analyzer = new QoderSessionAnalyzer();
    const scope = await analyzer.resolveScope({ workspace, home });
    const roots = await analyzer.discoverSourceRoots(scope);
    const sessions = await analyzer.discoverSessions(scope, roots);
    const target = sessions.find((s) => s.sessionId === SID);
    const events = await analyzer.readSession(target, scope, {});
    const assistant = events.find((e) => e.type === "assistant");
    assert.equal(assistant.model, "qwen3.7-max");
    assert.equal(assistant.modelSource, "ide-state-vscdb");
  } finally {
    process.env.HOME = originalHome;
    await rm(root, { recursive: true, force: true });
  }
});
