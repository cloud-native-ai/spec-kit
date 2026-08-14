# Tasks: 预置 Agent 定义的元信息中立化与按工具渲染分发

**Input**: Design docs from `.specify/specs/040-agent-metadata-portability/` (plan.md, requirements.md, data-model.md, contracts/×4, quickstart.md, feature-ref.md)

**Prerequisites**: plan.md ✅ | requirements.md ✅ | research.md ❌(findings inlined in plan) | data-model.md ✅ | contracts/ ✅ | quickstart.md ✅

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" — 每个用户故事先出契约/集成测试,后出实现;无 template-only gate,本需求含真实渲染代码)

**Environment Prerequisites**: 无外部环境依赖(无 docker/集群/特殊硬件);仅需 Python >= 3.8 与仓库既有 pytest/sync-mirrors 工具链。

## Definition of Done (DoD)

- DoD-1: 28 条 FR 全部有对应实现或成文裁定,无遗留 NEEDS CLARIFICATION
- DoD-2: 契约 + 集成测试全绿,且相对 baseline-failed.txt 零新增失败(SC-008)
- DoD-3: `sync-mirrors.py --check` exit 0,per-tool 命令副本经 regen 后无旧软链接叙述残留
- DoD-4: SC-001~SC-008 在 verification.md 中逐条记录 pass/deferred
- DoD-5: 文档与术语联动完成(Worker/Meta 限定表述全仓一致,术语表条目经用户确认后写入)

**DoD Status**: pending

## Completion Gate

- GATE-1: `pytest -q` 完成且与基线按名比对零新增失败 — `pytest -q` + `diff` 基线文件
- GATE-2: 渲染产物零符号链接 — 集成测试断言(SC-002)
- GATE-3: `python3 scripts/python/sync-mirrors.py --check` exit 0
- GATE-4: 禁用词表扫描三目录命中数为 0(SC-001)— `pytest tests/contract/test_neutral_vocabulary_scan.py`
- GATE-5: 映射"待核实"行数为 0(SC-003)— `pytest tests/contract/test_tool_mapping.py`
- GATE-6: AGENTS.md 与兼容性软链接未被破坏 — `find . -maxdepth 1 -type l` + `/speckit.instructions` 刷新成功

## Format: `[ID] [P?] [Story] Description`

Task State Sigil:`[ ]` 待做 / `[X]` 完成 / `[~]` 延迟(须在 Notes 说明)。`[blockedBy: Txxx]` 表示拓扑依赖。

## Path Conventions

- 中立源:`agents/`(仓库上游)→ `.specify/agents/templates/`(镜像)→ `.specify/agents/instances/`(项目自写)
- 渲染目标:`.qoder/agents/`、`.claude/agents/`、`.github/agents/`、`.opencode/agents/`
- 清单/备份:`.specify/agents/.render-manifest.json`、`.specify/agents/.backups/<tool>/`

---

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 冻结测试基线:运行 `pytest -q`,把失败用例名清单写入 `.specify/specs/040-agent-metadata-portability/baseline-failed.txt`(SC-008 的对照面;区分既有失败与新引入失败) <!-- 证据:run-tests.sh 完成,39 failed/1720 passed/1 skipped(27.19s),baseline-failed.txt 39 行 -->
- [X] T002 [P] 记录镜像基线:运行 `python3 scripts/python/sync-mirrors.py --check` 确认 exit 0,任何既有 drift 先归因记录再动手 <!-- 实查:exit 2,但 drift 仅来自无关的 skills/create-pages/(他会话未跟踪新增,未镜像);本需求触及的 agents/templates/scripts/shared 对全部 ok,不修无关 drift -->

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T003 [blockedBy: T001] 在 `src/specify_cli/__init__.py` 增加中立键集常量与 frontmatter 解析/校验函数(data-model.md §E2 全表:键名、取值域、缺省、是否渲染;集合外键 → 结构化错误含文件名与键名;支持 `supervisor`/`capacity-scope` 框架键标记) <!-- 证据:11 中立键/10 禁用键/smoke 8 断言通过(含 U-1 修订:lite 入域、none=不下发) -->

## Phase 3: User Story 1 - 元信息与正文有明确边界 (Priority: P1) 🎯 MVP

**Goal**: 边界程序可判定(FR-001~004)。**Independent Test**: 不解析正文即可提取全部元信息;正文不含分发参数。

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T004 [US1] [blockedBy: T003] 创建 `tests/contract/test_neutral_metadata_schema.py`:C-1 键集封闭性(构造含未知键的临时 agent → 校验失败并指名)、C-2 必填/缺省、C-5 正文无分发参数、C-7 占位符拒入、C-8 仅凭 frontmatter 枚举(计数用 `len(glob)` 派生,禁硬编码)

### Implementation for User Story 1

- [X] T005 [US1] [blockedBy: T003, T004] 在 `src/specify_cli/__init__.py` 把校验函数接入 agent 读取路径(渲染与发现共用的唯一入口),未知键即失败并报告
- [X] T006 [US1] [blockedBy: T005] 运行 T004 套件至绿;用一次性脚本对 `agents/` 全部文件执行"仅 frontmatter 提取"演练并核对完整性(US1 Independent Test)

## Phase 4: User Story 2 - 元信息中立化 (Priority: P1)

**Goal**: 全仓消除工具方言(FR-005~008,SC-001)。**Independent Test**: 三目录禁用词表扫描命中 0;新增假想工具时定义文件零改动。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T007 [US2] [blockedBy: T003] 创建 `tests/contract/test_neutral_vocabulary_scan.py`:对 `agents/`、`skills/create-agent/templates/`、`skills/create-team/templates/agents/` 扫描禁用词表(C-4)并断言命中 0;断言全部键 kebab-case(C-3)

### Implementation for User Story 2

- [X] T008 [P] [US2] [blockedBy: T003] 重写 `agents/` 全部 7 个 `*.agent.md` 的 frontmatter 为中立键集(`maxTurns`→`run-turn-budget`、`tools`→`capability-tools`、`color`→`display-color`、`model`→`model-tier`;取值按 §E2 映射)
- [X] T009 [P] [US2] [blockedBy: T003] 重写 `skills/create-agent/templates/` 全部 10 个文件的 frontmatter 为中立键集(保持占位符白名单不动)
- [X] T010 [P] [US2] [blockedBy: T003] 重写 `skills/create-team/templates/agents/` 全部 8 个文件的 frontmatter 为中立键集(`role-scope` 作为框架键保留,T-5 裁定在 US5 成文)
- [X] T011 [US2] [blockedBy: T008] 改写 `tests/contract/test_shipped_agent_presets.py` 的 `test_preset_has_qoder_frontmatter` → 中立断言(更名去 qoder,[[STR-001]])
- [X] T012 [US2] [blockedBy: T009] 改写 `tests/contract/test_role_templates.py` 的 `test_template_has_qoder_frontmatter` → 中立断言(更名去 qoder,[[STR-002]];保留 `test_only_approved_placeholders` 与必备章节断言)
- [X] T013 [US2] [blockedBy: T007, T010, T011, T012] 运行契约套件至绿(`pytest tests/contract -q`)
- [X] T014 [US2] [blockedBy: T013] 文档去工具基准:重写 `docs/reference/agents/templates-and-agents.md` 中 [[STR-003]] 表述、删除 `## Qoder expert crosswalk`、以中立格式 + 出处表取代
- [X] T015 [P] [US2] [blockedBy: T013] 更新 `shared/definitions/agent-definitions.md` 的 frontmatter 键描述为中立键集

## Phase 5: User Story 3 - init 按目标工具渲染真实文件 (Priority: P1)

**Goal**: 中立源 → 每工具真实文件(FR-009~018,SC-002/003/005)。**Independent Test**: init 后目标目录全为常规文件、字段形态符合该工具、意图等价。

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T016 [US3] [blockedBy: T003] 创建 `tests/contract/test_tool_mapping.py`:M-1 完备性(以 `AGENT_CONFIG` 键域动态对照,禁硬编码 6)、M-2 每行 provenance 非空且无"待核实"、M-3 目录矩阵、M-4 字段转换无遗漏、M-5 策略文本在常量头部、M-6 越界回退、M-7 单点真源(渲染代码不得出现并行目录/字段知识)
- [X] T017 [US3] [blockedBy: T003] 创建 `tests/contract/test_agent_render.py`:R-1 真实文件非链接、R-2 仅 `*.agent.md` 且 execution 层不分发、R-3 instance 同名优先、R-4 连续两次渲染逐字节一致(SC-005)、R-9 反馈含工具/计数/备份/未承载汇总、R-10 占位符拒入、C-6 框架键不出现在任何产物
- [X] T018 [US3] [blockedBy: T017] 改写 `tests/integration/test_init_agents.py` 为渲染语义:四工具参数化(目录按 M-3)、符号链接计数为 0(SC-002)、渲染文件数 = `len(中立源 glob)`(禁硬编码)、user agent 保全、instances 层存活

### Implementation for User Story 3

- [X] T019 [US3] [blockedBy: T016] 在 `src/specify_cli/__init__.py` 实现 `_AGENT_METADATA_MAPPING` 全量(qoder/claude/copilot/opencode 渲染行 + codex/hermes 标注行;每行 provenance URL 见 contracts/tool-mapping.md §M-2;D3 策略写入常量头部注释;claude 行字段清单实现期对照官方文档二次核实后方可去"待核实")
- [X] T020 [US3] [blockedBy: T019, T017] 在 `src/specify_cli/__init__.py` 实现 `render_agents_for_tool()` + 清单写入(E4 schema);替换 init 调用点(`:1599-1617` 区域)为渲染调用;tracker 文案按 R-9
- [X] T021 [US3] [blockedBy: T020] 退役软链接机制(R-11):先把 `tests/contract/test_agents_symlink.py` 改写为 `tests/contract/test_agent_render_migration.py`(语义映射到 R-5/R-6/R-8),绿后删除 `ensure_per_file_agent_links()` 与 `_AGENT_LINK_DIRS`;按仓库 rename/retire 纪律评估是否登记 `_OBSOLETE_*`
- [X] T022 [US3] [blockedBy: T018, T021] 运行 US3 全量(契约 + 集成)至绿

## Phase 6: User Story 4 - 迁移平滑且不吞用户改动 (Priority: P2)

**Goal**: 升级路径与手改保护(FR-019~022,SC-006)。**Independent Test**: 三类内容项目(旧链接/自写/手改)跑升级路径后状态全部正确。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T023 [US4] [blockedBy: T020] 扩展 `tests/contract/test_agent_render_migration.py` 与 `tests/integration/test_init_agents.py`:旧逐文件链接项目 → init 后零链接(R-8);手改 → 备份 + 覆盖 + 反馈含备份路径(R-5);中立源删除 → 清理且手改先备份(R-6);清单外无源文件 → 不触碰;工具 A→B 切换隔离(R-7);SC-006 端到端场景

### Implementation for User Story 4

- [ ] T024 [US4] [blockedBy: T023] 在 `src/specify_cli/__init__.py` 补齐漂移/备份/清理实现(`.specify/agents/.backups/<tool>/<name>.<UTC-compact>.agent.md` 命名、init 反馈列备份)使 T023 全绿
- [ ] T025 [US4] [blockedBy: T024] 在临时目录按 quickstart.md §4 手工演练手改→再渲染→取回,核对 SC-006 两计数为 0

## Phase 7: User Story 5 - 三目录差别成文与迁移落位 (Priority: P2)

**Goal**: Worker/Meta 目录划分落地(FR-023~026,SC-007)。**Independent Test**: 任一文件一步查表定类;7 角色定义完成迁移;`agents/` 由 Meta Agent 填充。

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T026 [US5] [blockedBy: T013] 改写 `tests/contract/test_shipped_agent_presets.py` 的 `test_preset_shipped`:断言对象改为 Meta 预置集(`structure-adjuster`、`skill-verifier`);同步核对并调整 `test_agent_skill_enablement.py`、`test_handoff_chain.py`、`test_context_injection.py`、`test_persistent_agent_lifecycle.py` 中引用旧 7-slug 的夹具(pin hygiene:文件清单从目录派生)——此任务先红,随 T027/T028 转绿

### Implementation for User Story 5

- [ ] T027 [US5] [blockedBy: T008, T009, T026] 迁移落位(T-3):用 `agents/<slug>.agent.md` 的已中立化内容逐一**替换** `skills/create-agent/templates/agent-capacity-<slug>-template.md`(7 份),正文仅把项目身份行与 Project Context 段的 "Spec Kit (specify-cli)" 参数化为 `{{PROJECT_NAME}}`;完成后删除 `agents/` 下该 7 文件
- [ ] T028 [US5] [blockedBy: T027] 新作 `agents/structure-adjuster.agent.md` 与 `agents/skill-verifier.agent.md`(T-4:中立元信息、`user-invocable: true`、六大必备章节、职责限定操作技能/agent/结构)
- [ ] T029 [US5] [blockedBy: T028] 运行迁移后的契约 + 集成套件至绿(T026 转绿;`test_role_templates.py` 的 ROLE_SLUGS 断言对象随替换自然满足,若白名单需增补同一任务内完成)
- [ ] T030 [P] [US5] [blockedBy: T029] 成文差别定义(T-1/T-2/T-5):重写 `docs/reference/agents/templates-and-agents.md` 的目录分类节 —— Worker/Meta 三目录表、组队取件规则、[[STR-005]]/[[STR-006]] 与阶段模板缺参的裁定记录
- [ ] T031 [P] [US5] [blockedBy: T029] 机械联动(文档面):改写 `docs/reference/commands/agents.md`、`docs/tutorials/quickstart.md`、`docs/reference/agents/design.md` 的预置表与软链接叙述 → 渲染叙述
- [ ] T032 [P] [US5] [blockedBy: T029] 机械联动(模板面):改写 `templates/commands/agents.md` 与 `templates/commands/skills.md`(去软链接表述、7-slug 枚举改为维度表述),然后运行 `python3 scripts/python/regen-command-copies.py` 并 grep 验证 `.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`、`.codex/commands/`、`.hermes/commands/` 副本无旧叙述残留
- [ ] T033 [P] [US5] [blockedBy: T029] 机械联动(shared/skills 面):改写 `shared/workflow/agent-configuration.md`(软链接核验 → 渲染产物核验)、`shared/workflow/interview-walkthrough.md`、`skills/create-skills/SKILL.md`、`skills/create-team/references/patterns.md`、`skills/create-team/templates/agents/agent-workflow-schema.md` 中的旧枚举与软链接表述
- [ ] T034 [US5] [blockedBy: T030, T031, T032, T033] 镜像扇出:运行 `python3 scripts/python/sync-mirrors.py --write` 再 `--check`(覆盖 plan.md Mirror Obligations 全部行:`.specify/agents/templates`、`.specify/skills/...`、`.specify/shared/...`、`.specify/templates/...`),exit 0
- [ ] T035 [US5] [blockedBy: T034] 运行 `/speckit.instructions` 刷新 `AGENTS.md`(Agents 注册表与分发叙述;顺带修复缺 ux-analyst 的既有漂移),验证 GATE-6 软链接完好
- [ ] T036 [US5] [blockedBy: T034] 术语表提案:向用户提交 feature-ref.md 的 5 条候选(Meta Agent/Worker Agent/渲染产物/渲染清单/"原 Agent"更正);获确认后写入 `.specify/memory/glossary.md`,未确认则 `[~]` 延迟并注明
- [ ] T037 [US5] [blockedBy: T030] SC-007 演练:三目录各抽样 ≥3 文件,按 T-1 表一步判类,记录正确率 100%

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T038 [blockedBy: T022, T025, T029] 全量回归:`pytest -q` 与 `baseline-failed.txt` 按名比对,零新增失败(GATE-1/SC-008)
- [ ] T039 [blockedBy: T034] 运行 `python3 scripts/python/sync-mirrors.py --check`(GATE-3)与 docs-utils validate,零新增违规
- [ ] T040 [blockedBy: T019] SC-003 交付门:运行 `pytest tests/contract/test_tool_mapping.py` 确认"待核实"行数 0(GATE-5)
- [ ] T041 SC-004 演练:在映射中临时加入假想工具行,验证 agent 定义文件零改动,随后还原(记录改动文件清单入 verification.md)
- [ ] T042 [blockedBy: T038] 填写 `.specify/specs/040-agent-metadata-portability/verification.md`:SC-001~008 逐条 pass/partial/deferred + 证据
- [ ] T043 [blockedBy: T042] 收尾:更新 `.specify/memory/features/044.md` 实施备注;执行 Feedback 与 Documentation 收尾步骤

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 (US4) → Phase 7 (US5) → Phase 8 (Polish)
- US2 依赖 US1 的中立键集与校验;US3 依赖 US1/US2 的中立源;US4 依赖 US3 的渲染器与清单;US5 依赖 US2 的中立化 frontmatter(迁移携带)与 US3 的测试形态(计数派生,迁移不改测试)

### User Story Dependencies

- US1 → US2 → US3 为硬链(键集 → 中立化 → 渲染消费)
- US4 仅依赖 US3;US5 依赖 US2(frontmatter)+ US3(测试对迁移免疫的设计)
- US3/US4 的测试以 `len(glob)` 派生计数,US5 迁移不触发其返工(pin hygiene)

### Within Each User Story

Tests(红)→ 实现(绿)→ 套件回归 → 文档/联动;迁移类任务(T027/T028)与测试改写(T026)按 blockedBy 交错,先红后绿。

## Parallel Execution Examples

- Phase 4:`T008 | T009 | T010`(三目录 frontmatter 互不重叠);`T015` 与 `T014` 完成 T013 后可并行
- Phase 7:`T030 | T031 | T032 | T033`(四个文档/模板面互不重叠),汇合于 `T034` 镜像扇出
- Phase 1:`T001 | T002`

## Implementation Strategy

**MVP = US1(边界可判定)**:独立交付即满足"元信息可提取、正文无泄漏"。
**增量路线**:US1 → US2(中立化,全仓扫描为闸)→ US3(渲染上线,软链接退役)→ US4(迁移安全)→ US5(分类法落位与迁移)。
**独立部署点**:US2 完成后仓库已无方言;US3 完成后 init 即为真实文件分发;US5 完成后目录体系定型。
**风险控制**:claude 行字段清单在 T019 实现期对照官方文档二次核实(FR-010);任何"待核实"残留由 GATE-5 拦截。
