import assert from "node:assert/strict";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { createAnalyzer } from "../../scripts/js/better-harness/session-analysis.mjs";
import { OpencodeSessionAnalyzer } from "../../scripts/js/better-harness/session-analysis/platforms/opencode.mjs";

async function writeJson(filePath, value) {
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, JSON.stringify(value, null, 1));
}

async function makeFixture() {
  const root = await mkdtemp(path.join(os.tmpdir(), "opencode-provider-"));
  const home = path.join(root, "opencode-home");
  const workspace = path.join(root, "workspace");
  await mkdir(workspace, { recursive: true });
  const sessionRoot = path.join(home, "project", "proj1", "storage", "session");
  const created = Date.parse("2026-07-01T10:00:00Z");

  await writeJson(path.join(sessionRoot, "info", "ses_abc.json"), {
    id: "ses_abc",
    projectID: "proj1",
    directory: workspace,
    title: "fixture session",
    time: { created, updated: created + 60_000 },
  });
  // A session for another workspace must be filtered out.
  await writeJson(path.join(sessionRoot, "info", "ses_other.json"), {
    id: "ses_other",
    projectID: "proj1",
    directory: path.join(root, "elsewhere"),
    time: { created, updated: created },
  });
  await writeJson(path.join(sessionRoot, "message", "ses_abc", "msg_1.json"), {
    id: "msg_1", sessionID: "ses_abc", role: "user", time: { created },
  });
  await writeJson(path.join(sessionRoot, "message", "ses_abc", "msg_2.json"), {
    id: "msg_2", sessionID: "ses_abc", role: "assistant", modelID: "fixture-model",
    time: { created: created + 10_000 },
  });
  await writeJson(path.join(sessionRoot, "part", "ses_abc", "msg_1", "prt_1.json"), {
    id: "prt_1", messageID: "msg_1", sessionID: "ses_abc", type: "text",
    text: "please fix the bug in parser AKIA_NOT_A_KEY",
  });
  await writeJson(path.join(sessionRoot, "part", "ses_abc", "msg_2", "prt_2.json"), {
    id: "prt_2", messageID: "msg_2", sessionID: "ses_abc", type: "text",
    text: "done, patched the parser",
  });
  await writeJson(path.join(sessionRoot, "part", "ses_abc", "msg_2", "prt_3.json"), {
    id: "prt_3", messageID: "msg_2", sessionID: "ses_abc", type: "tool",
    callID: "call_1", tool: "bash",
    state: {
      status: "completed",
      input: { command: "npm test" },
      output: "2 passing",
      time: { start: created + 11_000, end: created + 15_000 },
    },
  });
  return { root, home, workspace };
}

test("opencode analyzer registers in the loadPlatform dispatch", async () => {
  assert.ok(await createAnalyzer("opencode") instanceof OpencodeSessionAnalyzer);
});

test("opencode discovers workspace-scoped sessions from project storage", async () => {
  const { root, home, workspace } = await makeFixture();
  try {
    const analyzer = new OpencodeSessionAnalyzer();
    const scope = await analyzer.resolveScope({ workspace, home });
    const roots = await analyzer.discoverSourceRoots(scope);
    assert.equal(roots.find((r) => r.id === "opencode-project-storage").exists, true);
    const sessions = await analyzer.discoverSessions(scope, roots);
    assert.equal(sessions.length, 1, "other-workspace session must be filtered out");
    assert.equal(sessions[0].sessionId, "ses_abc");
    assert.ok(sessions[0].firstSeen && sessions[0].lastSeen);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("opencode reads message/part events with tool lifecycle and inherited timestamps", async () => {
  const { root, home, workspace } = await makeFixture();
  try {
    const analyzer = new OpencodeSessionAnalyzer();
    const scope = await analyzer.resolveScope({ workspace, home });
    const roots = await analyzer.discoverSourceRoots(scope);
    const [session] = await analyzer.discoverSessions(scope, roots);
    const events = await analyzer.readSession(session, scope, { includeCommandText: true });

    const userEvents = events.filter((e) => e.type === "user");
    const assistantEvents = events.filter((e) => e.type === "assistant");
    const toolCalls = events.filter((e) => e.type === "tool.call");
    const toolResults = events.filter((e) => e.type === "tool.result");
    assert.equal(userEvents.length, 1);
    assert.equal(userEvents[0].userPrompt, true);
    assert.equal(assistantEvents.length, 1);
    assert.equal(assistantEvents[0].model, "fixture-model");
    assert.equal(toolCalls.length, 1);
    assert.equal(toolCalls[0].toolName, "bash");
    assert.equal(toolCalls[0].commandText, "npm test");
    assert.equal(toolResults.length, 1);
    assert.equal(toolResults[0].success, true);
    for (const event of events) {
      assert.ok(event.timestamp, `event ${event.type} must carry a timestamp (inherited when absent)`);
      assert.equal(event.sessionId, "ses_abc");
    }
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("opencode analyze runs the provider pipeline and declares capability gaps", async () => {
  const { root, home, workspace } = await makeFixture();
  try {
    const analyzer = new OpencodeSessionAnalyzer();
    const analysis = await analyzer.analyze({ workspace, home });
    assert.equal(analysis.scope.platform, "opencode");
    assert.equal(analysis.sessions.length, 1);
    const codes = (analysis.warnings ?? []).map((w) => w.code);
    assert.ok(codes.includes("opencode-partial-event-timestamps"),
      "capability gap must be declared explicitly");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("opencode facts flow redacts user text by default (no raw prompt in facts)", async () => {
  const { root, home, workspace } = await makeFixture();
  try {
    const analyzer = new OpencodeSessionAnalyzer();
    const facts = await analyzer.runCommand
      ? null
      : await analyzer.analyze({ workspace, home });
    const serialized = JSON.stringify(facts ?? {});
    assert.ok(!serialized.includes("please fix the bug in parser"),
      "raw user prompt must not appear in default analysis output");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

async function makeSqliteFixture() {
  const { root, home, workspace } = await makeFixture();
  const { DatabaseSync } = await import("node:sqlite");
  const db = new DatabaseSync(path.join(home, "opencode.db"));
  db.exec(`CREATE TABLE session(id TEXT PRIMARY KEY, parent_id TEXT, directory TEXT, title TEXT,
           time_created INTEGER, time_updated INTEGER, data TEXT)`);
  db.exec(`CREATE TABLE message(id TEXT PRIMARY KEY, session_id TEXT, role TEXT, time_created INTEGER, data TEXT)`);
  db.exec(`CREATE TABLE part(id TEXT PRIMARY KEY, message_id TEXT, session_id TEXT, type TEXT, data TEXT)`);
  const created = Date.parse("2026-07-01T12:00:00Z");
  const ins = (sql, args) => db.prepare(sql).run(...args);
  ins("INSERT INTO session VALUES (?,?,?,?,?,?,?)",
    ["ses_parent", null, workspace, "parent session", created, created + 90_000, null]);
  ins("INSERT INTO session VALUES (?,?,?,?,?,?,?)",
    ["ses_child", "ses_parent", workspace, "child subsession", created + 30_000, created + 60_000, null]);
  ins("INSERT INTO session VALUES (?,?,?,?,?,?,?)",
    ["ses_far", null, path.join(root, "far"), "other workspace", created, created, null]);
  ins("INSERT INTO message VALUES (?,?,?,?,?)",
    ["msg_p1", "ses_parent", "user", created, JSON.stringify({ role: "user" })]);
  ins("INSERT INTO message VALUES (?,?,?,?,?)",
    ["msg_p2", "ses_parent", "assistant", created + 5_000,
     JSON.stringify({ role: "assistant", model: { modelID: "db-model" } })]);
  ins("INSERT INTO part VALUES (?,?,?,?,?)",
    ["prt_p1", "msg_p1", "ses_parent", "text",
     JSON.stringify({ type: "text", text: "run the db fixture" })]);
  ins("INSERT INTO part VALUES (?,?,?,?,?)",
    ["prt_p2", "msg_p2", "ses_parent", "tool",
     JSON.stringify({ type: "tool", callID: "call_db1", tool: "bash",
       state: { status: "completed", input: { command: "make test" }, output: "ok",
         time: { start: created + 6_000, end: created + 8_000 } } })]);
  ins("INSERT INTO message VALUES (?,?,?,?,?)",
    ["msg_c1", "ses_child", "assistant", created + 40_000,
     JSON.stringify({ role: "assistant", modelID: "db-model" })]);
  db.close();
  return { root, home, workspace };
}

test("opencode sqlite source: workspace filtering, parent_id, message/part events", async () => {
  const { root, home, workspace } = await makeSqliteFixture();
  try {
    const analyzer = new OpencodeSessionAnalyzer();
    const scope = await analyzer.resolveScope({ workspace, home });
    const roots = await analyzer.discoverSourceRoots(scope);
    assert.equal(roots.find((r) => r.id === "opencode-sqlite").exists, true);
    const sessions = await analyzer.discoverSessions(scope, roots);
    const ids = sessions.map((s) => s.sessionId).sort();
    assert.deepEqual(ids, ["ses_abc", "ses_child", "ses_parent"],
      "JSON-layout ses_abc plus sqlite parent/child; far-workspace filtered");
    const parent = sessions.find((s) => s.sessionId === "ses_parent");
    const child = sessions.find((s) => s.sessionId === "ses_child");
    assert.equal(child.parentId, "ses_parent");
    const events = await analyzer.readSession(parent, scope, { includeCommandText: true });
    const types = events.map((e) => e.type);
    assert.ok(types.includes("user") && types.includes("assistant"));
    const call = events.find((e) => e.type === "tool.call");
    assert.equal(call.toolName, "bash");
    assert.equal(call.commandText, "make test");
    const result = events.find((e) => e.type === "tool.result");
    assert.equal(result.success, true);
    assert.ok(events.find((e) => e.type === "assistant").model === "db-model");
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
