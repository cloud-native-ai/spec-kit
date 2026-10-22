# Research & Decisions — 068 Exec-Quant Feedback Channel

**Phase 0 output** for Feature 068 (`/speckit.plan`, 2026-10-22, unattended Mode A).
Every decision cites the spec clause it serves and the measured repo fact it rests on.
Exploration evidence path: **degraded** — this run has no subagent dispatch tool, so the
codebase exploration pass was a bounded manual probe (grep for symbols + targeted
excerpt reads) per create-plan § Phase 0 subagent-unavailable fallback; marked
`(detected: direct read, subagent unavailable)`.

## D1 — 打包腿落点：扩展 feedback-utils.py 的 package 流程，不在 exec-quant.py 新增打包动作

- **Serves**: FR-001 / FR-002 / FR-004 / FR-005 / FR-019.
- **Decision**: payload 采集与写入落在框架源 `scripts/python/feedback-utils.py`（镜像
  `.specify/scripts/python/feedback-utils.py`）的 `write_package` / `action_package`
  扩展里；`exec-quant.py` 动作面（collect / list-records / score / collect-dispatch /
  args-manifest）零改动（FR-017）。
- **Evidence** (direct read): `write_package` 位于
  `.specify/scripts/python/feedback-utils.py:1098`，`action_package` 同文件 `:1201`；
  现行为 = feedback 条目 zip 根部 + 可选 `introspection/` + `MANIFEST.md` + 可选
  `SUBMISSION-NOTES.md`；`selected` 为空时提前返回
  `"No feedback entries to package."`（`:1114-1116`）——FR-019 要修订的正是这一提前返回。
- **Rejected**: 在 exec-quant.py 加 package 动作 → 打包写入路径分裂到两个引擎，
  Path B 技能要跨两个引擎编排，违反"打包侧改动落 feedback 引擎"的既有分工
  （spec Key Entities: 量化引擎只扩展回传/聚合动作面）。

## D2 — 包内布局：独立 `exec-quant/` 目录 + `payload-manifest.json` + 逐条 `records/`

- **Serves**: FR-001（一等载荷、显式声明）、Edge Cases（来源形态标注）。
- **Decision**:
  ```text
  <zip root>
  ├── <feedback entries>.md          # 不变
  ├── introspection/                 # 不变（可选）
  ├── SUBMISSION-NOTES.md            # 不变（可选）
  ├── MANIFEST.md                    # 新增 ## Exec-Quant Payload 声明段
  └── exec-quant/                    # 新增载荷目录
      ├── payload-manifest.json      # 载荷清单：源身份 + 计数 + 降级
      └── records/
          ├── <original-filename>.json          # 逐条文件原样字节拷贝
          └── legacy-records-L0007.json         # 遗留 jsonl 每行一个文件
  ```
- **Rationale**: feedback 条目为 `.md`、载荷为 `.json` 且收在独立目录，零文件名冲突；
  逐条文件使接收侧可逐条幂等去重；遗留流按行拆条并标注来源形态（`source_form:
  legacy-jsonl`），源文件永不重写（FR-002 / A4）。
- **Evidence** (direct read): 载荷内文件名沿用 exec-quant 存储的 `entry_filename()`
  形态（时间戳-uuid，`exec-quant.py:215-217`）；本仓存储实测含 `records/`(15 个
  schema v2) + `records.jsonl`(59 行 v1) + `scores/` + `scores.jsonl`
  （spine U1 + 本阶段复核）；样例客户项目 cws-lib-python 仅 `records/`(7 条 v2)。

## D3 — 包级源项目身份：`project_name`（必选）+ `source_commit`（可选），取自 instructions.md 的 Project Name 行与 git HEAD，缺一降级 unknown-project

- **Serves**: FR-003、A3。
- **Decision**: 打包时 `project_name` 读取
  `<workspace>/.specify/instructions.md` 的 `**Project Name**:` 行（本仓实测为
  `spec-kit (distributed as specify-cli)`，`instructions.md:193`）；读取失败回退到
  workspace 目录基名（目录名非绝对路径）；两者皆不可得时 `project_name` 置空并在
  payload-manifest 置 `identity_status: "unknown-project"`。`source_commit` 取
  `git rev-parse HEAD`（失败置 null，不重试、不阻塞）。
- **Rationale**: instructions.md 由 `/speckit.instructions` 生成于每个客户项目，
  是既有的项目名唯一落点（零新增配置面）；目录基名跨机稳定且不泄露路径结构；
  绝对路径与凭据面零引入（FR-003 MUST NOT）。
- **Rejected**: git remote URL 作身份 → 可能携带 token（凭据面），且 fork 后漂移。

## D4 — 接收腿承接面：新增 feedback-utils.py 动作 `--action ingest-exec-quant --package <zip>`，由 Path A A2 调用

- **Serves**: FR-006 / FR-007 / FR-008 / FR-009 / FR-010（"引擎动作名留 plan"的兑现）。
- **Decision**: 现状 Path A 入站包处理是 **agent 技能驱动**（A2 用 `unzip -p` 手工读条目，
  无引擎 intake 动作——`path-a-digest.md` A2 实测）。068 新增引擎动作
  `ingest-exec-quant`：只处理包内 `exec-quant/` 载荷段（解出、归因、幂等写入聚合层），
  feedback 条目仍走既有 A2/A4 agent 流程（语义零变化，FR-009）。调用点 = Path A A2
  对每个 bundle 执行一次该动作；无载荷包返回计数 0、exit 0（零差异）。
- **Evidence** (direct read): `_ACTIONS` 注册表
  `.specify/scripts/python/feedback-utils.py:1645-1658` 共 12 动作，无 intake 类动作；
  `path-a-digest.md` § A2 的读取形态为 `unzip -p`。
- **Rejected**: 扩展既有 `cleanup`/`reindex` 兼职 → 语义混杂；新命令 → 违反"零新增命令"裁定。

## D5 — 聚合层布局：`aggregated/<source-slug>/records/` 按条信封文件 + `aggregated/summaries/` 按次汇总

- **Serves**: FR-012（A2 裁决：`aggregated/` 平行子目录、按条落盘、可重建、禁可变聚合单文件）。
- **Decision**:
  ```text
  .specify/memory/exec-quant/aggregated/
  ├── <source-slug>/                # 源项目组；缺身份 = 字面 unknown-project
  │   └── records/
  │       └── <entry-filename>.json # 信封：attribution + verbatim record
  └── summaries/
      └── <summary-id>.json         # 每次显式汇总一个不可变产物
  ```
  `source-slug` = 项目名 slug 化（小写、`[a-z0-9-]`）+ 身份串短哈希 8 位
  （`cws-lib-python-3f2a1b9c` 形态）；unknown-project 组 = 字面 `unknown-project`
  （空身份串哈希，确定性）。信封文件形如
  `{"aggregation_envelope": {schema_version, kind: "speckit.exec-quant-aggregated",
  source_project, source_commit, identity_status, identity_key, content_hash,
  package_file, ingested_at}, "record": {<verbatim>}}`。
- **Rationale**: 按条文件 + 原子写（tmp+rename，沿用 `write_entry` 形态
  `exec-quant.py:220-235`）天然满足并发开发安全纪律；信封把 verbatim 记录整个封入
  `record` 键，未知字段零丢弃（FR-007），归因不污染记录字段命名空间；
  summaries 按次落盘、可重建（重跑产生新文件不覆盖旧文件）。
- **Rejected**: 单一聚合 JSON → 违反 FR-012 禁令；归因字段并进记录顶层 → 命名空间冲突风险。

## D6 — 幂等身份键：`source_project + unit_id + unit_type + run_id + collected_at` + 记录内容 canonical sha256

- **Serves**: FR-008、US2 场景 2/4。
- **Decision**: `identity_key = sha256(join([source_project, unit_id, unit_type,
  run_id, collected_at], "\x1f") + "\x1e" + sha256(canonical_json(record)))`。
  canonical_json = `json.dumps(sort_keys=True, ensure_ascii=False, separators=(",",":"))`。
  同 identity_key 且同 content_hash → 重复，跳过计数；同 identity_key 不同
  content_hash（引擎法则下不应发生）→ keep-first + `identity_conflict` 显式计数，
  不覆盖不并行写入。
- **Rationale**: 五元组覆盖 spec 指定身份（FR-008）；内容哈希兜底同身份异内容；
  059 采集侧已按 (unit_id, run_id) 去重（`append_record_locked` →
  `existing_record`，`exec-quant.py:895-917`），故全量包含产生的重复必然是
  同内容重复，keep-first 语义零信息损失。

## D7 — 载荷封顶：MAX_PAYLOAD_RECORDS = 1000、MAX_PAYLOAD_BYTES = 16 MiB，按 (collected_at, 文件名) 升序纳入，截断显式计数

- **Serves**: FR-005（显式封顶、截断数入 MANIFEST）、Edge Cases（不静默丢弃不无界膨胀）。
- **Decision**: 两个模块常量钉在 feedback-utils.py；排序键 `(collected_at, 源文件名)`
  升序（确定性、跨机可复现）；触顶截断时 payload-manifest 记
  `included / truncated` 计数，MANIFEST.md 同步声明。
- **Rationale**: 与单条 64 KiB 记录上限（`RECORD_SIZE_CAP_BYTES`，`exec-quant.py:89`）
  化算：1000 条 × ≤64 KiB 理论上界 64 MiB，16 MiB 总包体上限约束实际最坏情况；
  1000 条远超现网量级（两仓实测 15 + 7 + 59 条），截断是防御性边界非常态路径。

## D8 — 汇总腿：exec-quant.py 新增 `--action aggregate`，只读 `aggregated/`，产物落 `aggregated/summaries/`

- **Serves**: FR-011 / FR-013 / FR-014、US3。
- **Decision**: 动作名 `aggregate`（加入 ACTIONS 元组 + ARG_MANIFEST，argparse parser
  保持唯一事实源——既有 `args-manifest` 契约自动校验新旗标）。消费面 =
  `aggregated/` 信封记录（**不含**本地 `records/`——US3 语境是聚合层，本地记录无源
  归因）。输出双面：stdout 机器可读 JSON + `aggregated/summaries/<summary-id>.json`
  不可变产物。视图字段：按源项目 × 单元维度的 record_count、quality 各字段
  evaluated/not_evaluated 分布（[[STR-002]] 计数）、coverage 汇总；每组附
  `record_files` 名单（每个数字可对账到具体文件——FR-011）。
- **Evidence** (direct read): `ACTIONS` 元组 `exec-quant.py:45`；`read_entry_files`
  通用按条读取器 `:238-249` 可直接复用于 `aggregated/` 读取；
  `normalize_record_view`（`:929-940`）是输出侧形态升级先例，aggregate 的
  v1/v2 归一遵循同模式（只影响视图，不写源）。
- **Rejected**: 放在 feedback-utils.py → 汇总是量化域派生能力，owner 是量化引擎；
  spec Key Entities 明确"本特性只扩展其回传/聚合相关动作面"。

## D9 — FR-019 修订点：`write_package` 的空条目提前返回改为「条目与载荷双空才不产出」

- **Serves**: FR-019、US1 场景 4。
- **Decision**: `action_package` 先算 payload，再与 selected 一并传入
  `write_package`；`write_package` 仅当 `not selected and not payload.records` 时
  保持早退（措辞更新为覆盖两类数据），否则照常产包——`Entries: 0` 显式入
  MANIFEST，载荷段照常写入。external 排除、时间过滤、`--all` 语义零变化。
- **Evidence** (direct read): 提前返回点 `.specify/scripts/python/feedback-utils.py:1114-1116`。

## D10 — 退出码与降级语义：degradation ≠ 失败；exit 0 + 计数，整体不可执行才 exit 2

- **Serves**: FR-005 / FR-010（非阻塞）、Edge Cases。
- **Decision**: `ingest-exec-quant` / `package` 载荷腿 / `aggregate` 在
  "有降级但完成"时 exit 0，JSON/text 输出携带显式计数（skipped_unreadable、
  truncated、identity_conflict 等）；exit 2 仅留给动作整体不可执行
  （--package 文件缺失、zip 无法打开为 zip、聚合层存储不可写）——与既有
  `FeedbackError` exit 2 形态一致（`feedback-utils.py:1698-1706`）。zip 成员级、
  单条记录级损坏一律计为 skipped，非阻塞。

## D11 — 测试策略：全量 Test-First（本特性含可执行运行时代码，不适用 template-only Partial），red-first 取证 + 名字级基线比对

- **Serves**: FR-018、SC-006、宪法 IV。
- **Decision**:
  - **契约**（`tests/contract/`）：`test_feedback_exec_quant_payload.py`（打包腿布局/
    MANIFEST 声明/只读/FR-019/封顶/身份）、`test_feedback_intake_exec_quant.py`
    （接收幂等/归因/零混入/无载荷零差异/损坏计数）、`test_exec_quant_aggregate.py`
    （汇总视图/未测计数/可对账/仅本地）。
  - **单元**（`tests/unit/`）：identity key 与 canonical hash、slug 生成、
    payload 采集（双布局混合字段形态）、封顶排序。
  - **集成**（`tests/integration/`）：package → ingest → aggregate 端到端、
    同包双收幂等、既有套件基线比对。
  - **Red-first 取证**：每支新测试先以未实现断言跑出失败（红）并留痕
    `test-evidence/`，再实现转绿；实现完成后重跑既有
    `test_feedback_*.py` + `test_exec_quant_*.py` 契约/集成套件，排序后失败
    nodeid 名单与实现前冻结基线逐名比对（名字级，非计数级）。
  - 不新增确认门（Explicit Exclusions）。

## D12 — 文档与镜像义务（Mirror Obligations 摘要，plan.md 表为权威）

- **Serves**: 派发要求 6。
- **Decision**: 源侧改动面 = `scripts/python/feedback-utils.py`、
  `scripts/python/exec-quant.py`、`skills/internal/manage-feedback/SKILL.md`、
  `skills/internal/manage-feedback/references/path-a-digest.md`、
  `skills/internal/manage-feedback/references/path-b-and-probe.md`、
  `templates/commands/feedback.md`、`shared/workflow/feedback-step.md`（载荷随包后
  该 step 的观察面更新）、docs `docs/reference/commands/feedback.md`、
  `docs/reference/skills/feedback.md`。镜像对以
  `scripts/python/sync-mirrors.py MIRROR_PAIRS` 为准（direct read）：scripts、
  skills/internal、shared、templates(excl. commands) 四对；
  `templates/commands/feedback.md` 走 regen-command-copies.py 逐工具副本。
  同步顺序 = 先源后 `sync-mirrors.py --write`，禁止手改镜像（两顶帽子，宪法 XI）。

## D13 — 同作者评分委派的降级执行

- **Serves**: create-plan § Same-author detection delegation、objective-analysis-gate。
- **Decision**: 本运行是 `requirements → plan` 无断点链，评分对象确系同代理所写，
  门条件成立；但本运行无子代理派发工具，按 objective-analysis-gate §7
  subagent-unavailable fallback 降级为直接有界复核，且所有疑似 Partial 判行
  标注 `(detected: direct read, subagent unavailable)`，弱证据路径对读者可见，
  不以委派名义静默放行。复核方式 = 独立一趟逐原则对照产物证据的重读
  （非填表时记忆）。

## D14 — 无 research.md 前置文件；本文件即 Phase 0 载体

- SPECS_DIR 下无既有 research.md（`ls` 实测仅 checklists/ requirements.md
  test-evidence/）；Phase 0 结论以本文件承载，plan.md § Phase 0 引用之。
