---
description: Local management interface for the feedback mechanism — five execution modes. Mode 1 (no arguments) prints every probe placed in the current project as a vertical tree; Mode 2 processes collected feedback (view/filter/dispose/package/post-package cleanup); Mode 3 injects an external probe for client-project custom skills/agents/commands (feedback stays client-local, never submitted upstream); Mode 5 introspects accumulated feedback in the client project (scenario-grounded verification, root-cause clustering, routing decisions, report-enriched packaging); Mode 4 consumes incoming feedback bundles from the framework's feedback/ intake directory (framework project ONLY).
short-description: 反馈机制本地管理：探测总览、处置、外部探针、自省、消费反馈包
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. The input selects the execution mode and may carry a slice/kind/probe filter (Mode 2), a target custom unit (Mode 3), or `consume`/`--consume` (Mode 4).

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`) and apply the protocol in `shared/workflow/glossary.md`: correct recorded homophone/confusable variants before acting; propose new terms at wrap-up with user confirmation.

## Outline

This command is the local management interface for the Feedback Probe system. It works in **five execution modes**:

| Input | Mode | Who runs it |
|-------|------|-------------|
| *(empty)* | 1 — Probe Overview | Any project |
| filter/dispose/package keywords | 2 — Process Collected Feedback | Any project |
| unit / inject keywords | 3 — Inject External Probe | Any client project (its own custom units) |
| `introspect` | 5 — Introspect Feedback(自省) | Any client project |
| `consume` / `--consume` | 4 — Consume Framework Feedback | **Framework project ONLY** |

With no arguments it defaults to Mode 1. `introspect` 与 `consume` 同时出现时按 Mode 4 处理并在报告中说明。

### Mode 1 — Probe Overview (default; no arguments)

Print **every probe placed in the current project** as a graphical list / vertical (tree) structure.

```bash
python3 .specify/scripts/python/feedback-utils.py --action probes
python3 .specify/scripts/python/feedback-utils.py --action probes --validate     # schema check
python3 .specify/scripts/python/feedback-utils.py --action probes --reconcile   # embed audit
python3 .specify/scripts/python/feedback-utils.py --action map                  # OPTIONAL (writes): rebuild probe-map.md
```

Render the merged truth source (framework Classes/Objects + project external probes) as a tree: kind → class (with target slice, collection, processing) → objects (unit @ lifecycle point). Mark internal vs external. The overview MUST be rendered from the truth source — never a hand-maintained list. Empty external section: show the `external-custom` class with its zero-object marker, no error.

### Mode 2 — Process Collected Feedback

Guide the user through the local processing loop:

1. **Status view**: `--action status` (count / threshold / should_prompt)。若因阈值提示进入本命令:可先运行 Mode 5(`/speckit.feedback introspect`)自省再打包——建议而非强制,跳过不影响任何后续步骤。
2. **Summary view**: `--action list --limit 0` with filters as requested — `--slice <commands|skills|host-custom|...>`, `--kind <internal|external>`, `--disposition <processed|ignored|open>`, plus the pre-existing `--unit-id/--since/--contains`.
3. **Disposition**: `--action dispose --id <entry-id> --to processed|ignored` (local metadata only; optional `--reason`/`--ref` record provenance, e.g. from an introspection report).
4. **Package** (on user confirmation, internal entries only): `--action package` → print zip path + manual-send guidance. The agent NEVER sends the zip. 若待打包条目带有 `introspection_ref`(已被自省覆盖),默认提议改用 `--action package --include-introspection` 把覆盖它们的自省报告一并入包;用户可拒绝,拒绝不阻断打包。
5. **Post-package cleanup (default closing step of the package run)**: once the zip exists, the packaged batch no longer needs to live in the active store — the zip is the record. Preview with `--action cleanup --package <zip|latest> --dry-run`, then run without `--dry-run` in the same session as packaging. Cleanup removes only entries actually inside that zip; `cleanup-log.md` records every removal. The zip itself STAYS under `.specify/memory/feedback/packages/` as the delivery artifact.
6. **After delivery (`mark-submitted`)**: once the batch is dealt with (sent, or deliberately ignored) and `mark-submitted` has reset the counter, the zip has served its purpose — remove it from the outbox: `rm .specify/memory/feedback/packages/feedback-<ts>.zip`. The store, the outbox, and the counter all return to zero; `cleanup-log.md` plus the (already-delivered) zip's MANIFEST remain the audit trail.

### Mode 3 — Inject an External Probe

For **client-project** custom Skills/Agents/Commands (assets the framework's own probes never cover). Terminology — **客户项目 (Client Project)** / **框架项目 (Framework Project)** — is defined canonically in [`.specify/shared/definitions/dogfooding-definitions.md`](../../.specify/shared/definitions/dogfooding-definitions.md) §2 (one repo, two hats; the flow chain framework sources → publish → install → each client project's `.specify/`); this command says "client project" wherever older drafts said "host project":

1. Elicit the target unit (`custom:<owner>/<name>`), lifecycle point (default `wrap-up`), and a short collection-intent note (`--notes-file`).
2. Run `--action probe-inject --unit custom:<owner>/<name> --notes-file <file>` — writes `.specify/memory/feedback/probes/ext-<slug>.md`.
3. Verify the injection: the object appears in `--action probes` and after `--action map`.

External-probe feedback is **client-project-local** (Loop B — the client project's own use→feedback→iterate loop): it feeds the client project's own optimization, is separately filterable via `--kind external`, and is **never** included in upstream packages.

### Mode 5 — Introspect Feedback(自省)

在记录与上行之间做**场景化深加工**:回到真实场景核验条目事实、聚类同根因问题、产出自省报告并分流(本地下沉 Loop B / 随包上行 Loop A)。动机:消费方拿到的裸事实脱离了条目诞生的真实场景,容易产出错位方案;自省把深度思考移回客户项目现场。**触发**:`$ARGUMENTS` 含 `introspect`。任意客户项目可运行,无 Mode 4 的框架项目门。

1. **范围快照**:`python3 .specify/scripts/python/feedback-utils.py --action list --disposition open --format json`(可按 `--slice/--kind/--since` 收窄)取条目摘要投影;零条目 → 报告"无可自省条目"并正常结束,不落空报告文件。
2. **场景化分析**(agent 推理;适用 Token 效率纪律:程序优先、摘要优先、升级阶梯,禁止整库原文注入):逐条目调出被评单元的当前定义/源码与条目引用的上下文,给出带证据的核验结论(成立/部分成立/已过时/不成立);把同根因的条目聚类为**问题**;每个问题含齐五要素——问题陈述、根因、证据锚点(指向具体单元/文件/位置)、分流决定(`local-sink(<channel>)` 或 `upstream-bound(package-attachment)`)、具体优化方案。
3. **报告产出**:按报告 schema 落盘 draft 报告到 `.specify/memory/feedback/introspection/<report-id>.md`(`report-id` 形如 `introspection-<YYYYmmddTHHMMSSZ>`;frontmatter 七字段 + `## Findings` + `## Excluded`),然后运行 `--action introspect-register --report-file <path>` 完成结构校验与条目关联;校验失败(exit 2)会逐条列出违规,修正后重跑。
4. **用户确认**:呈现报告摘要(问题清单 + 每个问题的分流决定与建议处置);用户可逐问题覆盖分流方向——覆盖写回报告该问题的 `**用户覆盖**`(原决定 → 覆盖后决定)并同步 `**分流决定**`/`**建议处置**` 行后再确认。确认后运行 `--action introspect-register --report-file <path> --confirm`:报告置 `confirmed`,`**建议处置**` 行逐条生效(等价于逐条 `--action dispose --id <entry-id> --to <state> --reason "introspection:<report-id>#F-nn" --ref <report-id>#F-nn`);报告无 `建议处置` 行时仅翻转报告状态,不动条目。
5. **路由建议**:列出分流结果的建议去向——本地下沉项给出建议通道(直接修复 / improve-skills / improve-docs / 新需求),随包上行项提示下次打包可附报告(见 Mode 2 第 4 步);**仅建议,不自动执行任何动作**。

红线与边界:

- 本模式 MUST NOT 自动修改代码/配置、MUST NOT 触发任何网络行为或自动传输;所有落地动作(直接修复、improve-* 运行、打包与人工送达)均经既有通道由用户确认后执行。
- 外部 probe 条目参与自省时分流恒为 local-sink,永不进入上行候选。
- 自省执行期间新写入的条目不进入本次范围(以发起时刻快照为准);条目引用物已失时标注"已过时/无法复现"而非中断;对同一批条目重复自省时,新报告声明 `supersedes` 承继旧报告,不平行重复造问题。

### Mode 4 — Consume Framework Feedback (framework project ONLY)

Consumes incoming feedback bundles from the `feedback/` intake directory: reads, processes, routes findings, and cleans up processed bundles. This is the **receiving end** of Dogfooding Loop A — the counterpart to Mode 2's package-and-send.

**Framework-only gate**: Mode 4 runs ONLY in the framework project (the Spec Kit source repo). Client projects MUST NOT execute this mode. Gate on framework-source structure — the repo must have `templates/` + `skills/` + `src/specify_cli/` at root (the canonical source directories that only the framework repo owns). If absent → report "Mode 4 is framework-project-only; this is a client project" and stop. (Do NOT gate on `feedback/` directory existence — a client project could have one for unrelated purposes.) If the gate passes but `feedback/` is absent or empty, Step 1 handles it gracefully.

**Trigger**: `$ARGUMENTS` contains `consume` or `--consume`.

#### Step 1 — Enumerate pending bundles

```bash
ls feedback/feedback-*.zip 2>/dev/null
```

- Zero bundles → report "No pending feedback bundles in `feedback/`" and stop.
- N bundles → list them (filename + size) and proceed. **Batch discipline**: process ALL bundles as ONE consolidated batch, never one zip at a time — reconciling claims across bundles surfaces factual conflicts between reporters and yields one mechanism fitting every environment.

#### Step 2 — Extract and read entries

For small batches (≤3 bundles, ≤20 entries total), read inline:

```bash
unzip -p <zip> MANIFEST.md       # manifest first
unzip -p <zip> <entry-filename>.md  # then each entry
```

For larger batches, extract to a temp directory first (faster, avoids repeated unzip overhead):

```bash
tmpdir=$(mktemp -d)
for z in feedback/feedback-*.zip; do unzip -o -d "$tmpdir/$(basename $z .zip)" "$z"; done
# then read files with standard file-reading tools
```

Collect from every entry: `unit_id`, `probe`, `slice`, `run_id`, `## Review`, `## Optimization Points`. Build a **cross-bundle findings table**: unit × finding × source-bundle. Clean up the temp dir after reading. 包内可能附 `introspection/<report-id>.md` 自省报告(条目经源头场景化核验):此类发现可直接采信其核验结论与证据锚点,把精力集中在跨包对账与冲突裁决上,无需重复事实核验。

#### Step 3 — Reconcile and route findings

Cross-bundle reconciliation (the reason for batch discipline):

- **Conflicting claims**: two reporters assert different facts about the same unit → surface the conflict explicitly, pick the one verified against source code, note the rejection.
- **Recurring findings**: the same optimization point appears in ≥2 bundles → elevate priority (systemic friction, not one-off).

Route each finding to its destination:

| Finding type | Route to | Example |
|-------------|----------|---------|
| Small, obvious fix | Direct fix (in this run) | Typo, stale count, broken link |
| New feature / capability | `/speckit.requirements` | New command, new engine action |
| Skill/agent improvement | `improve-skills` / `improve-agent` / `improve-team` | Workflow refinement, template fix |
| Tool record correction | `improve-tools` | Wrong contract, missing alias |
| Documentation gap | `improve-docs` or direct edit | Stale doc, broken link |
| Acknowledge only | Record in consume report | Already fixed, duplicate, WONTFIX |

Produce a **consume report** for user confirmation: findings table, routing decisions, conflicts found, and proposed cleanup list.

#### Step 4 — Cleanup (mandatory closing step of the consume run)

The user confirms the **routing decisions** in the consume report — confirmation of the report, NOT completion of every downstream routed run (findings routed to later `improve-*` / `/speckit.requirements` runs carry their input from the consume report and the log row below). On that confirmation, cleanup runs before the command ends:

```bash
rm feedback/feedback-<ts>.zip   # each processed bundle in this batch
```

- Delete ONLY the bundles that were in this batch; cleanup is atomic and **part of the run** — a consume run does not end with its intake files still on disk. The durable record is the consume-log row (routings + conflicts), never the zips: lingering bundles would form a second, staler source of truth.
- Record the consume event by appending one row to `.specify/memory/feedback/consume-log.md`:

  ```markdown
  | 2026-08-15 | feedback-<ts1>.zip, feedback-<ts2>.zip | 23 | 5 direct fix, 3 improve-skills, 1 requirement | 1 (conflicting tool count) | 2 zips removed |
  ```

  Columns: `| Date | Bundles | Entries | Findings Routed | Conflicts | Cleanup |`

- The `feedback/` directory itself remains (it is the permanent intake point).

#### Mode 4 behavior rules

- **Read-only toward bundles until cleanup**: never modify zip contents; extraction is read-only (`unzip -p` to stdout).
- **One batch, one cleanup**: do not delete individual bundles mid-batch; cleanup is atomic, runs once at the end of the consume run (after the routing report is confirmed), and leaves the intake empty.
- **No network**: consume is entirely local file I/O + agent reasoning.
- **Framework source fixes only**: findings are acted on in the framework source (`templates/`, `skills/`, `scripts/`, `shared/`, `src/`), never in `.specify/` mirrors (two-hats rule: Constitution XI).

## Behavior Rules

- Zero network operations of any kind (red line); `mark-submitted` remains local bookkeeping.
- Modes 1–3 operate on the local store `.specify/memory/feedback/`; never edit store files by hand. Mode 4 operates on the `feedback/` intake directory (read-only until atomic cleanup).
- Exit code 2 from the engine is a verdict — report it, do not argue around it.
- Probe truth source: `.specify/shared/definitions/probe-definitions.md` (+ project `probes/`); derived views (`probe-map.md`) are rebuilt, never hand-edited.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this command reached its wrap-up stage. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against `/speckit.feedback`'s declared purpose and produce a short review plus ≥1 concrete, command-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this command's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a nested skill/command already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "/speckit.feedback" --unit-type command \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
   Probe attribution: the engine resolves the unit to its probe object automatically — the entry inherits kind/slice from the probe registry. External custom units record via `--unit-id custom:<owner>/<name> --unit-type custom-unit`; their entries stay client-project-local and never enter upstream packages.
6. **Consolidated submission prompt(非阻塞).** If the returned `should_prompt` is `true`, append ONE non-blocking line to the wrap-up report inviting submission (point the user to the `/speckit.feedback package` command — the user-facing path; never paste the raw `feedback-utils.py` engine call into the user-facing line); it MUST NOT block the wrap-up flow and MUST NOT trigger any 自动传输 (manual delivery only; `--action mark-submitted` runs only if the user initiates submission). Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.

## Handoffs

**Before**: none (any Spec Kit project; requires the probe registry installed by `/speckit.instructions`).

**After**: Mode 3 injection → the client project's own improvement loop (`improve-skills` / `improve-agent` consume `list --kind external` findings). Mode 2 cleanup → `mark-submitted` if not yet run for the batch. Mode 4 consume → routed `/speckit.requirements` calls for new-feature findings; `improve-*` invocations for skill/agent/tool findings; `consume-log.md` records the batch disposition.
