# Analyze Findings — W3（095-superagent-role · tasks.md）

- **Worker**: W3（analyze 并发波；唯一 spec 读域 `.specify/specs/095-superagent-role/tasks.md`）
- **Run ID**: r20261110T073257Z-b095
- **Date**: 2026-11-10
- **Contract**: `.specify/skills/internal/analyze-artifacts/SKILL.md` + `references/detection-and-severity.md` / `references/validation-and-report.md`
- **Mode**: 只读（不改制品、不修复、不提交、不 push）；本文件是本 Worker 唯一制品写面（另有 Wrap-up 三引擎记账）
- **Detection**: 本 Worker 为 fresh-context 检测者（tasks.md 非本会话产出）
- **Validation status**: W3-01 / W3-02 / W3-03 为 HIGH，**尚待编排侧的独立验证波**（validator 必须与本检测者不相交）；本文件按检测结果先落盘

## Findings（10 条：3 HIGH / 4 MEDIUM / 3 LOW）

| ID | Severity | Category | propagation_surface | Anchor（文件:行） | 一句话事实 | 建议归属（指针） |
|---|---|---|---|---|---|---|
| W3-01 | HIGH | inconsistency（计数/包含性声明） | DoD-3 / T050 的镜像义务验证门 | `.specify/specs/095-superagent-role/tasks.md:237`（并见 :19） | T050/DoD-3 声称镜像义务共 **11 行**，但 T050 括号内枚举 `definitions ×4 + template ×1 + engine ×1 + digest ×1 + skills ×5` 合计 **12** 项，且未声明“行数 vs 文件数”的单位，故“11 行每行都有 write+verify”无法从本文件机械判定。 | `/speckit.tasks`：对齐 `plan.md` § Mirror Obligations（行数 owner）并给出逐行映射；若 plan 本身为 12 行，先改 plan 再回写本文件。 |
| W3-02 | HIGH | coverage-gap | 任务 → 实现（六个 FR 无任何任务落点） | `.specify/specs/095-superagent-role/tasks.md:147`（全文件普查；可追溯规则见 :55） | 全文件普查显示 **FR-011…FR-016** 六个连续 FR 在任何任务行中都未被引用（引用从 FR-009 直接跳到 FR-017），这六个需求在任务图中没有落点。 | `/speckit.tasks`：对照 `requirements.md` 补齐任务或记录显式处置；FR-011 / FR-016 在覆盖率会计的契约引用组 lane 中同样未覆盖。 |
| W3-03 | HIGH | underspecification（证据生产者缺失） | GATE-4 / DoD-6 的完成门证据 | `.specify/specs/095-superagent-role/tasks.md:240`（DoD-6 :22；GATE-4 :34） | T053 只“记录” `smoke_command` / `smoke_exit_code=0` / `smoke_evidence_path=test-evidence/smoke-six-modules.txt`，但没有任何任务运行该 smoke 命令或生成该证据文件，GATE-4 要求的“存在且非空”文件没有生产者。 | `/speckit.tasks`：新增 smoke 运行行，或把显式运行并入 T053 并记录真实退出码。 |
| W3-04 | MEDIUM | inconsistency（验收口径） | US1 独立测试 / 验收 | `.specify/specs/095-superagent-role/tasks.md:116`（并见 :114, :124, :129） | US1 独立测试写“**三类**违例夹具各自非零”，而同故事目标、T013 夹具清单与 T015 的闭合违例集都是**四类**（self-dispatch / dangling-parent / unbacked-role-claim / depth-inconsistent）。 | `/speckit.tasks`：改为四类，与 T011/T013/T015 对齐。 |
| W3-05 | MEDIUM | inconsistency（依赖叙述漂移） | 任务派发顺序 | `.specify/specs/095-superagent-role/tasks.md:263`（并见 :254, :158） | “User Story Dependencies”称 US2 与 US1 的唯一交叉点是“T028 引用 T005 / T041 的产物”，但 T028 的阻塞集是 T005,T027，T041 是更晚的 US5 行，且 :254 已声明 US2 与 US1 无硬依赖——依赖叙述与 `blockedBy` 图不一致（该小节与 Phase Dependencies 近乎重复，漂移埋在其中）。 | `/speckit.tasks`：按 `blockedBy` 图重写该句，或删除重复小节只留一处 owner。 |
| W3-06 | MEDIUM | inconsistency / coverage-gap（声明 vs 确定性 lane） | analyze 覆盖率汇总 / 实现 | `.specify/specs/095-superagent-role/tasks.md:52`（并见 :90 T003） | 格式节声明“未声明的契约子句是可接受的留白”（严格子集），但 `account-clause-coverage.py --spec-dir .specify/specs/095-superagent-role` 返回 `status: uncovered`、exit 1、**29 条本特性契约子句超出冻结基线**（已声明仅 9/38），且本文件没有任何 DoD/GATE 行覆盖该 lane，两种口径互斥。 | `/speckit.tasks` + 覆盖率契约 owner：裁定该 lane 是否为门——是则补 green 声明与门项，否则在任务文件记录为何 `uncovered` 可接受。 |
| W3-07 | MEDIUM | underspecification（证据落点缺失） | SC 验证证据（US4 / US5） | `.specify/specs/095-superagent-role/tasks.md:200, :222` | T038 与 T044 只说 “record readings” 而未命名落盘文件，与同文件其它转绿行（均给出 `test-evidence/...` 路径）不一致，而 DoD-6 要求每条 SC 有来源指针。 | `/speckit.tasks`：为两行分别指定 `test-evidence/` 证据文件。 |
| W3-08 | LOW | inconsistency（机器标记 vs 散文） | 并行派发 | `.specify/specs/095-superagent-role/tasks.md:151, :284`（并见 :280, :292） | T021 未标 `[P]` 而 Parallel Opportunities 与 Parallel Example 都说 T021–T025 可同批并行；Polish 的 T046/T049/T050 也未标 `[P]` 而 :284 说 T049/T050 可与 T046 并行——`[P]` 标记与并行说明漂移。 | `/speckit.tasks`：对齐 `[P]` 标记与并行说明，保持其一为 owner。 |
| W3-09 | LOW | ambiguity | 任务输入构造 | `.specify/specs/095-superagent-role/tasks.md:123` | T012 说取 `data-model.md § 2.1` 的 “three carrier forms”，括号内却列出四个载体组（teams/、state/、logs/、registry/），且未说明 registry/ 是 cross-check 而非 carrier。 | `/speckit.tasks`：按 `data-model.md § 2.1` 对齐“三载体 + cross-check”的表述。 |
| W3-10 | LOW | underspecification（未命名载体） | 任务 → 实现 | `.specify/specs/095-superagent-role/tasks.md:146, :234` | T019 的“six downlink role fields block”与 T047 的“a deterministic check”都没有给出自身载体路径 / 实现归属（只给了产物或变异副本路径），与本文件 :54“每行含精确文件路径”的自定规则不一致。 | `/speckit.tasks`：为两处命名载体（夹具文件 / 检查脚本或其复用的 Tool）。 |

## Coverage verdict（确定性 lane，供波次汇总）

- 运行：`python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/095-superagent-role` → **exit 1，status: uncovered**（未使用 `--freeze`，符合 analyze 侧禁令）。
- `[clause-uncovered]` fail：669 uncovered，其中 **29 beyond the frozen baseline**；本特性已声明（green）9 条，四个契约合计 38 条。29 条分布：`harness-landing` C-2/C-4/C-6（3）、`role-edge-engine` C-2…C-10（9）、`role-transition-payload` C-1/C-3…C-12（11）、`status-digest-role-view` C-2…C-6/C-8（6）。→ 与 tasks.md:52 的“严格子集可接受”政策冲突，已记为 **W3-06**。
- `[fr-uncovered]` fail：19/38 —— 该 lane 以**契约引用组**为准（“never task rows”），属 contracts / requirements owner，**不在 W3 读域**，移交波次覆盖率汇总。名单：FR-001/002/003/004/006/007/011/016/017/022/023/024/025/026/027/030/036/037/038（其中 FR-011、FR-016 同时命中 W3-02，即任务行也未引用）。
- `[clause-unparsable]` fail：107（语料级，其中 1 个 positive-form parse doubt；非 095 特有，基线内）。
- `coverage-baseline-delta` fail(29)：基线存在，会计计数 640 names；tasks.md:79 记 642 行，差值与文件头行一致，不单列 finding。
- **Method note（非 W3 finding）**：技能 §3 的示例命令写作 `--spec <spec-dir>`，而引擎声明的是 positional 或 `--spec-dir`（`--spec` 会被作为未声明选项拒绝，exit 2）；本次按引擎声明形式运行。归属：analyze-artifacts 技能源文件。

## Feature / registry linkage（pass G 的 W3 边界）

- tasks.md:5 绑定 Feature 095，状态 `Planned`；T054 记录 Feature-list review 且明确 “no `.specify/features.md` edit”。这与 `.specify/shared/workflow/feature-integration.md` 的 Status State Machine 一致（`/speckit.tasks` → Maintain `Planned`；`/speckit.implement` → `Planned → Implemented`），T054 发生在翻转前，“stays Planned”在时序上成立。
- 索引行实际内容、Last Updated 日期与 `.specify/features/095-*.md` 细节文件**不在 W3 读域**，未核；无 W3 finding。

## Constitution alignment（pass D）

- **未发现 CRITICAL 宪法冲突**（本法域内）。
- 已核对：IV（测试先行 / 契约测试：测试行先于实现行，结构契约测试与运行时测试分层）、VII（Planned 维持、Completion Gate、deferred 纪律）、IX（无新运行时机制；T041 的零第二机制断言）、XII（Tool Reuse：W3-10 只记为载体未声明，LOW）、XIV（指针纪律：owner 引用；重复出现的测量值属 dated record / test pin）、XVII（新目录仅 `tests/fixtures/superagent-role/`，按每特性夹具惯例）、XX（唯一测试入口 `run-tests.sh`）、XXI（引擎接口契约 + GATE-5 命令形式已核对）、XXII（内容层不涉及）。
- 说明：`[~]` 图例只写 `verification.md` 的理由登记，而任务模板把 inline comment 标为 “ideally”、宪法 VII 提及该注释——属框架模板层面的既有缩写，不是 095 特有缺陷，未立 finding。

## Premise / reality checks（支撑“无 finding”的取样证据）

- `python3 .specify/scripts/python/validate-tasks.py .specify/specs/095-superagent-role/tasks.md` → **PASS 0 error / 0 warning**（exit 0）。
- 任务引用且应存在的文件全部存在（含 6 个既有契约测试模块、3 个并发测试、`sync-mirrors.py`、`generate-instructions.sh`、四个定义页、三个技能面、模板与 live 指令文件、`notes/pre-change-measurements.md`、`coverage-baseline.txt`）。
- 任务声明应不存在的 9 个新产物全部不存在（`role-edge-check.py`、`tests/fixtures/superagent-role/`、新定义页、6 个新测试模块）。
- 前提读数核对通过：`python3 --version` → 3.11.11；`requires-python = ">=3.8"`（pyproject.toml:5）；`INSTRUCTIONS_BUDGET_BYTES=38400`（generate-instructions.sh:107）；模板锚点 266/272、live 283/289；`status-digest.py --action {digest,guard,report}` / `--format {table,json}`；`test_i13_channel_three_payload_sixth_field_row` 存在于 tests/contract/test_fast_fail_discipline.py:1629。
- FR / SC 引用普查：SC-001…SC-010 全部 10 个被引用；FR 引用 32/38（缺 FR-011…FR-016，见 W3-02）。

## Metrics

- Task rows: 54（T001–T054，无编号缺口）；新契约测试模块 6；Work Package 计数自洽（7 / 13 / 10 / 6 / 6 / 9）。
- Findings: 10（HIGH 3 / MEDIUM 4 / LOW 3）；constitution CRITICAL: 0。
- Coverage: tasks FR citation 32/38；SC 10/10；green-claimed clauses 9/38（确定性 lane 29 beyond baseline）。
- Deterministic engines: validate-tasks PASS；account-clause-coverage exit 1 / uncovered。

## Limits & anomalies（Fast Fail 交代）

- **Pass H（checklist 问责）未运行**：`checklists/*.md` 不在 W3 读域，由波次编排侧负责。
- **Pass I（Decision Tensions）未运行**：判定对象是 `plan.md`，不在 W3 读域。
- requirements / plan / contracts / feature index 的实际内容未读；相关结论仅以确定性引擎输出或 tasks.md 内文为证据。
- 无本读域内需 halt 的异常；未做任何就地修复（read-only worker）；未触碰仓库既有脏文件。
- Method observation（供编排侧）：任务文件引用的预算字面量、锚点行号与检验器 CLI 形式均与仓库现实一致；唯一契约级漂移是技能 §3 的 `--spec` 形式（见上）。
