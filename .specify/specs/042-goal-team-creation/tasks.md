# Tasks: 基于已定义 Goal 的团队创建流程(Goal→Target 分解提议 + 每 Target 一队)

**Requirement ID**: 042
**Requirement Key**: 042-goal-team-creation
**Related Feature**: 027 Team Management(feature-ref.md:Implemented,本需求为 Extended-by 扩展,状态不回退)
**Input**: Design documents from `.specify/specs/042-goal-team-creation/`(plan.md、requirements.md、data-model.md、4 contracts、quickstart.md、feature-ref.md)
**Prerequisites**: plan.md ✅、requirements.md ✅、data-model.md ✅、contracts/ ✅、quickstart.md ✅

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation"(unit/contract/regression MUST);本需求为混合形态:引擎面(`goal-utils.py` 扩展、`verify-territory-disjoint.py`)走进程内 `main()` 契约测试,模板/文档面按 Workflow Gates 的 template-only 规则走**结构契约测试**(模板子串断言 + per-tool 副本一致性),不强行套 unit/integration 形态。

**Organization**: 按 user story 分组(US1 分支地基 → US2 分解闭环 → US3 成组建队);三个 story 共享两个串行面(`templates/commands/team.md`、`tests/contract/test_goal_team_creation.py`),故 story 间为严格顺序依赖(US1 → US2 → US3),story 内测试先行。

**Environment Prerequisites(生成时已探测)**: 无外部环境依赖——python3.11 + pytest 8.4.2 已验证;无 docker/网络/集群面。全部 per-tool 副本目录现存 4 个(`.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/`;`.hermes`/`.codex` 不存在,不生成)。

## Definition of Done (DoD)

- DoD-1: 引擎与模板实现覆盖 FR-001..015(--check 干跑、resolve_effective_target、verify-territory-disjoint.py、team.md 命令分支、4 份技能参考、用户文档),逐 FR 可溯源到任务
- DoD-2: 3 个新契约测试文件全绿,且全量套件对冻结基线零新增失败(GATE-1)
- DoD-3: plan.md Mirror Obligations 全表逐行核验字节一致(引擎镜像 cmp、skills 镜像 sync --check、4 份 per-tool 副本 diff -q)
- DoD-4: quickstart.md §2–§6 手工走查通过(含两类拒绝、干跑 exit 码、聚焦运行披露)
- DoD-5: SC-001..006 在 verification.md 中逐条给出状态与证据(实现期由 /speckit.implement 落笔)
- DoD-6: 词汇表/Feature 索引复核完成(现记 Focus Target、Decomposition Proposal 两条 proposed 术语;任务分解未暴露新术语或 Feature 变更)

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件零新增失败 — check: `bash scripts/bash/run-tests.sh --names-out /tmp/042-final.txt && comm -13 .specify/specs/042-goal-team-creation/baseline-failed.txt /tmp/042-final.txt` 输出为空
- GATE-2: Mirror Obligations 全表一致 — check: `cmp scripts/python/goal-utils.py .specify/scripts/python/goal-utils.py` 且 `python3 scripts/python/sync-mirrors.py --check` exit 0 且 `python3 scripts/python/regen-command-copies.py --check` exit 0
- GATE-3: 无遗留 `[ ]`/`[>]` 任务行 — check: `grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- GATE-4: verification.md 列全 SC-001..006 且各有状态 — check: `grep -c '^.*SC-00[1-6]' .specify/specs/042-goal-team-creation/verification.md` ≥ 6
- GATE-5: 新增确定性面全部被契约钉住 — check: `pytest tests/contract/test_targets_check.py tests/contract/test_focus_target_resolution.py tests/contract/test_goal_team_creation.py` 全绿

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(不同文件、无未完成依赖)
- **[Story]**: US1 / US2 / US3(Setup 与 Polish 无 story 标签)
- **[blockedBy: Txxx,Tyyy]**: 显式依赖标签,所列任务全 `[X]` 前不得启动
- 描述含精确文件路径

### Task State Sigil (REQUIRED)

- `- [ ]` — Open;`- [>]` — Claimed(多 agent 专用);`- [X]` — Closed;`- [~]` — Deferred(理由记入 verification.md `deferred_tasks=` + 行内 `<!-- deferred: ... -->`)
- /speckit.implement 运行在零 `[ ]`/`[>]` 行时才算完成;`[~]` 允许残留并进 Deferred 汇总

## Path Conventions

改动画 = 仓根 `scripts/python/`、`skills/create-team/`、`templates/commands/`、`docs/reference/commands/`、`tests/contract/`;镜像落 `.specify/scripts|skills/` 与 4 个 per-tool 命令目录(见 plan.md Mirror Obligations)。框架源码帽子(framework sources)为默认;`.specify/` 运行时副本只经扇出脚本落地,零手工双写。

---

## Phase 1: Setup(共享基线)

**Purpose**: 冻结测试基线,区分存量失败与回归(AGENTS.md 反复教训:先跑全量、记基线)

- [X] T001 运行全量测试套件并冻结基线:`bash scripts/bash/run-tests.sh --names-out .specify/specs/042-goal-team-creation/baseline-failed.txt`;将存量失败清单(如有)与其数量记入本任务完成说明——后续一切"回归"判定以该文件为准,禁止把基线失败误报为本需求引入

**Checkpoint**: 基线冻结完成,后续每个 story 的测试任务都可做 name 级二分

---

## Phase 2: User Story 1 - 传入已定义 goal:识别、分析、产出单个匹配团队 (Priority: P1) 🎯 MVP

**Goal**: create 分支能识别 archive 精确命中的 goal,加载复述、四要素分析(建议非门禁),产出带 `goal_slug` 的单个团队;两类拒绝(悬空/终态)零产物。

**Independent Test**: 对叙事+判据明确、无 Targets 的 active goal 走 create → 四要素分析呈现并确认 → 单个 `team.md`(`goal_slug` 正确、派生理由可溯、preset 强匹配时推荐);全程 `goal.md` 零写入。传错 slug 得逐字 `goal 未定义:` 拒绝;终态 goal 拒绝。

### Tests for User Story 1(先写、先看它失败)

- [X] T002 [P] [US1] 创建 `tests/contract/test_goal_team_creation.py`:钉 contracts/goal-based-create.contract.md C-1..C-3 + C-5——① 分支识别文法(`goal-utils.py list --json` 枚举、slug 精确匹配、确认门禁、"近似不构成命中/零语义猜测"措辞);② 两类拒绝([[STR-003]] 逐字 `goal 未定义:` 前缀 + 指向 `/speckit.goal create`、终态显式拒绝、零产物零写入);③ 四要素分析披露(维度/判据覆盖含 `None provided.` 缺失声明/既有 Target/可达成性,各附理由;建议非门禁措辞);④ C-5 不变量(goal_slug 引用、内联 goal 仅渲染、不一致显式报出)。断言风格沿 `tests/contract/test_run_target_assignment.py`(模板子串断言;per-tool 副本一致性沿用其既有 fixture 风格,副本清单从目录树推导——现存 4 份,不二次硬编码清单)。先运行确认新断言全部 FAIL(模板尚无分支)

### Implementation for User Story 1

- [X] T003 [US1] 在 `templates/commands/team.md` create 路由撰写 goal-based 分支前半(C-1/C-2/C-3):识别步骤(先 `python3 scripts/python/goal-utils.py list --json` 取全集,token 精确匹配 slug 或指向其 `goal.md` 的路径 → 向用户确认进入;无命中走既有自由文本流程零回归)、`parse_goal` 加载并复述(objective/criteria 含缺失态/status/targets/history)、两类拒绝(停止不需确认)、四要素分析(每项附理由,链接概念锚 `shared/definitions/goal-definitions.md` 不复述)、路径裁决呈给用户(单团队 | 分解——分解细节步骤留 US2 占位锚点)
- [X] T004 [US1] [blockedBy: T003] 在 `templates/commands/team.md` 撰写单团队派生与落盘(C-4 单团队子集 + C-5):frontmatter 声明 `goal_slug`(引用非副本);roster/pattern 以 goal 叙事为输入走既有 `python3 skills/create-team/scripts/match-team-preset.py --goal "<文本>"` + pattern 决策树,派生理由入确认预览;preset 强匹配推荐复用;内联 `goal` 字段仅可读性,与定义不一致显式报出供裁决;落盘仅写 `team.md`,`goal.md` 零写入
- [X] T005 [P] [US1] 更新 `skills/create-team/SKILL.md`:create 流程骨架新增 goal-based 分支条目(指向 references/create-mode.md 过程规范)
- [X] T006 [P] [US1] 更新 `skills/create-team/references/create-mode.md`:新增 goal-based 创建过程规范章节——分支识别(引擎枚举驱动)、加载复述、四要素分析、路径裁决、单团队落盘(引用既有 frontmatter 字段序,不动既有六步结构)
- [X] T007 [US1] [blockedBy: T004,T005,T006] 扇出落地:运行 `python3 scripts/python/regen-command-copies.py` 再生 4 份 per-tool speckit.team 副本,再 `python3 scripts/python/sync-mirrors.py --write` 同步 skills 镜像(本 phase 覆盖 Mirror Obligations 行:team.md 模板、SKILL.md、create-mode.md;goal-utils.py 本 phase 未动)
- [X] T008 [US1] [blockedBy: T007] 镜像核验(逐行枚举):`diff -q` 4 份 per-tool 副本与再生输出一致(`.claude/commands/speckit.team.md`、`.github/prompts/speckit.team.prompt.md`、`.opencode/command/speckit.team.md`、`.qoder/commands/speckit.team.md`);`python3 scripts/python/sync-mirrors.py --check` exit 0(SKILL.md、create-mode.md 行);`cmp scripts/python/goal-utils.py .specify/scripts/python/goal-utils.py` 仍逐字节相同(证明本 phase 未误触引擎)
- [X] T009 [US1] [blockedBy: T002,T008] 运行 `pytest tests/contract/test_goal_team_creation.py tests/contract/test_run_target_assignment.py -q`(新面全绿 + 038 面零回归),再全量 `bash scripts/bash/run-tests.sh` 对照 baseline-failed.txt 无新增;手工 QA quickstart §2(窄 goal → 单团队;错误 slug → 逐字前缀拒绝;终态 goal → 拒绝)

**Checkpoint**: US1 独立可测——窄 goal 获得结构有据的单团队,两类拒绝 100% 拦截,自由文本路径逐项一致

---

## Phase 3: User Story 2 - 宽泛 goal 的分解决策与 Target 提议-批准闭环 (Priority: P1)

**Goal**: 分析判定宽泛并经用户裁决后,起草经 `--check` 干跑全通过的分解提议集(无序、成果形、不复述判据),一次合并确认 → 逐条 `targets --add` 落盘;既有 open Targets 为复用基线。

**Independent Test**: 对判据跨多维、无既有 Target 的宽泛 goal:带理由提议集 → 单次批准 → 逐条引擎落盘,`## Targets`/`## History` 由引擎渲染,`goal.md` 零手写。暂不建队时 goal 已获成组切片。

### Tests for User Story 2(先写、先看它失败)

- [ ] T010 [P] [US2] [blockedBy: T009] 创建 `tests/contract/test_targets_check.py`:钉 contracts/decomposition-proposal.contract.md C-1——进程内 `main()` 断言(风格沿 `tests/contract/test_goal_targets_engine.py` 的 importlib 夹具):合法成果形语句 exit 0 且 goal.md 前后逐字节不变(mtime/内容双钉);步骤形语句 exit 2 附原因;复述判据 exit 2;`--check --add` 同给 exit 2;不存在 slug exit 3;终态 goal exit 4;`--json` 输出 verdict 形状;全程零 `## History` 记录、零身份发放
- [ ] T011 [P] [US2] [blockedBy: T009] 扩展 `tests/contract/test_goal_team_creation.py` 增分解提议组:钉 decomposition-proposal.contract.md C-2/C-3/C-4 模板面——[[STR-002]] 逐字 `分解提议` 小节名、每条语句+理由+`--check` verdict 的呈现规则、"呈现前每条已 exit 0"措辞、一次合并确认 → 逐条 `--add` 措辞、exit-2 verdict 原样上报/修订重提/显式放弃、无序集措辞(无依赖边/无编号顺序语义)、复用基线措辞(open 复用、done/dropped 不复用不重开)、独立成立候选引导另立 goal(GD-3)、提议阶段 `goal.md` 零写入断言

### Implementation for User Story 2

- [ ] T012 [US2] [blockedBy: T010] 在 `scripts/python/goal-utils.py` 实现 `targets <slug> --check "<语句>" [--json]`:校验器与 `--add` 同源(复用 `_bad_shape`/`_reject_bad_target_statement`/判据归一化比对,零第二文法);零写入(不发放身份、不改 goal.md、不记 History);退出码 0/2/3/4 沿全局语义;`--check` 与 `--add`/`--list`/`--set` 互斥(违者 exit 2)
- [ ] T013 [US2] [blockedBy: T011] 在 `templates/commands/team.md` 撰写分解路径(C-2/C-3/C-4):分解决策呈现(结论+依据,用户裁决,否决则回退单团队或中止、裁决留痕);起草纪律(每条成果形 GD-2、GD-3 litmus 引导另立 goal 退出提议集、MUST NOT 复述判据或 SC-xxx);以 `分解提议` 小节一次性呈现全量(语句+理由+每条 `--check` verdict,呈现前必须全过);一次合并确认 → 逐条 `python3 scripts/python/goal-utils.py targets <slug> --add "<语句>"`,每条 verdict 即时尊重;中途中止语义(已落盘保留、续起走复用基线零重复授权)
- [ ] T014 [P] [US2] 扩展 `skills/create-team/references/goal.md` §Target:团队侧提议纪律补强——复用基线处置(open 直接复用、终态条目不复用身份不顺带重开)、提议只补缺口、单一撰写入口红线(team 侧对 goal.md 零写入)
- [ ] T015 [P] [US2] 更新 `skills/create-team/references/create-mode.md`:分解提议与成组批准步骤并入 goal-based 过程规范(含"提议集为空 → 直接进入成组建队"分支)
- [ ] T016 [US2] [blockedBy: T012,T013,T014,T015] 扇出 + 核验:`python3 scripts/python/regen-command-copies.py` + `python3 scripts/python/sync-mirrors.py --write`;核验(Mirror Obligations 本 phase 行):`cmp scripts/python/goal-utils.py .specify/scripts/python/goal-utils.py` 逐字节相同(引擎镜像首次实际变更)、`sync-mirrors.py --check` exit 0(goal.md、create-mode.md 行)、4 份 per-tool 副本 `diff -q` 一致
- [ ] T017 [US2] [blockedBy: T016] 运行 `pytest tests/contract/test_targets_check.py tests/contract/test_goal_team_creation.py tests/contract/test_goal_targets_engine.py -q`(新面全绿 + 既有 targets 引擎面零回归),全量对照基线无新增;手工 QA quickstart §3(--check 合法/步骤形/复述判据的 exit 码与原因;批准后逐条 --add;模拟中途中止再续起的基线复用)

**Checkpoint**: US2 独立可测——宽泛 goal 获得成组切片,全部 Target 变更可溯源到引擎调用,零 `goal.md` 手写

---

## Phase 4: User Story 3 - 每 Target 一个团队:N teams : 1 Goal 的成组创建 (Priority: P1)

**Goal**: 每个 open Target 一个团队(同一 `goal_slug`、`focus_target` 默认聚焦、slug 确定性查重、territory 两两不相交经薄脚本校验);run 侧解析顺序 显式 > focus_target > 无,披露带 [[STR-001]] 标记;无字段团队逐字节等价。

**Independent Test**: 对含 3 条 open Target 的 goal 成组创建 → 3 个 `team.md`(同 goal_slug、各聚焦、territory 两两不相交);无显式 `--target` 的 run 归属默认 Target 且披露 `(团队默认)`;显式覆盖语义同 038。

### Tests for User Story 3(先写、先看它失败)

- [ ] T018 [P] [US3] [blockedBy: T017] 创建 `tests/contract/test_focus_target_resolution.py`:钉 contracts/focus-target-resolution.contract.md——引擎面:`resolve_effective_target(team_md_path, explicit_target=None)` 单元/契约断言(解析顺序恒 显式 > focus > 无;`source ∈ {explicit, team-default, none}`;`declared_focus` 透传;`focus_target` 格式非法 → `input-error` 停止;`effective` 喂既有 `preview_target_check` 五查(悬空/终态/跨 goal/goal 终态 verdict 沿 038);`source=none` 逐字节等价直通;显式值与 focus 相同 → `source=explicit` 无特例)。模板面子串:三式披露行(含 `本次 Target: T-003 — <statement>(open)(团队默认)` 即 [[STR-001]] 后缀)、`**Target 指派**` 行携带来源标记、解析顺序句;无字段 team.md 样本与 038 既有 run 契约夹具共用证明零回归
- [ ] T019 [P] [US3] [blockedBy: T017] 扩展 `tests/contract/test_goal_team_creation.py` 增成组+territory 组:① goal-based-create.contract.md C-4 成组纪律子串(每个 open Target 一队、同一 `goal_slug`、`focus_target = T-<nnn>`、roster/pattern 以 Target 语句走 match-team-preset.py、slug `<goal-slug>-t<nnn>` 三位零填充 + `.specify/teams/` 查重 + 门禁改名、既有团队检测 → 复用或移交 coordinate、确认门禁五件套披露);② creation-territory-disjoint.contract.md verify 组(构造提议 JSON + 既有团队夹具驱动 `skills/create-team/scripts/verify-territory-disjoint.py`):全不相交 exit 0;write 相交 exit 4 + contested 路径;既有团队未声明 territory exit 4 + undecidable;非法 JSON/schema exit 2;`--repo-root` 无 teams/goal_slug 失败 exit 3;`non_path` 只列不求交;文法一致性钉(相同输入下脚本 verdict 与直调 `detect_overlaps` 一致)

### Implementation for User Story 3

- [ ] T020 [US3] [blockedBy: T018] 在 `scripts/python/goal-utils.py` 实现 `resolve_effective_target(team_md_path, explicit_target=None)`(data-model §2):读 team.md frontmatter `focus_target`(值域校验 `^T-\d{3}$`,非法即 `input-error` 停止,不静默忽略);返回 `{effective, source, declared_focus}`;只解析不判定——`effective` 非 None 时由调用面喂既有 `preview_target_check`,五查零旁路;无字段且无显式 → `source=none` 下游逐字节等价
- [ ] T021 [P] [US3] [blockedBy: T019] 创建 `skills/create-team/scripts/verify-territory-disjoint.py` 薄脚本:CLI `--input <proposals.json> [--repo-root <root>] [--json]`;输入 schema = data-model §5(`{goal_slug, teams[]}`,teams 含 write/read/forbidden/non_path);校验对象 = 提议团队 ∪ 磁盘同 `goal_slug` 既有团队(读 `.specify/teams/*/team.md` frontmatter,未声明 territory 记 `undecidable` 不猜测);判定函数 import 复用 `skills/create-team/scripts/build-summary-input.py` 的 `expand_scopes`/`scopes_overlap`/`overlap_verdict`/`detect_overlaps`(importlib 加载,零第二文法);退出码 0(全 no-overlap)/2(输入非法逐字段报错)/3(无 teams 目录或 goal_slug 解析失败)/4(overlap 列争用区 或 undecidable 列未声明方);`--json` 输出 `{verdicts: [{a, b, verdict, contested?}], summary}`,人读模式逐对打印;脚本零写入
- [ ] T022 [US3] [blockedBy: T019] 在 `templates/commands/team.md` 撰写成组建队面(goal-based-create C-4 全量):每个 open Target 一队(全部同 `goal_slug`;`focus_target: T-<nnn>` 插在 `goal_slug` 之后——字段序 `slug, name, description, goal, goal_slug, focus_target, territory, pattern, members, config, created, updated`);roster/pattern 以各 Target 语句为输入走 `python3 skills/create-team/scripts/match-team-preset.py --goal "<语句>"` + pattern 决策树,理由入预览;slug 缺省 `<goal-slug>-t<nnn>` 对 `.specify/teams/` 查重、冲突改写回显、门禁可改名;创建期校验(focus_target 存在于绑定 goal 的 `## Targets` 且 open,否则拒绝);territory 提议基于切片 + `verify-territory-disjoint.py` verdict 随门禁呈现(exit 4 → 披露争用/未声明方,改划重跑或移交 `/speckit.goal coordinate`,MUST NOT 静默落盘已知重叠;同 goal 下已有团队时单团队路径同样必跑 verify);确认门禁一次性披露五件套(分支判定/分析结论/路径决策/提议集或复用声明/territory 划分);既有同 goal 团队检测 → 提议复用或移交 coordinate
- [ ] T023 [US3] [blockedBy: T018,T022] 在 `templates/commands/team.md` Run Mode 第 2 步插入解析层(focus-target-resolution C-2):先经 `resolve_effective_target` 得有效 Target 再走既有五项 preview 校验(校验本身零修改);披露三式——`(open)`(显式)/`(open)(团队默认)`(team-default,[[STR-001]] 逐字)/`无(对 goal 整体运行)`(none);run 报告 `**Target 指派**:` 行携带来源标记;新台账条目 `target_ref = effective` 仍仅由 Team Supervisor 写入;显式 `--target` 恒覆盖;未声明字段的团队全流程与引入前逐字节等价(不读取不解析)
- [ ] T024 [P] [US3] 更新 `skills/create-team/references/create-mode.md`:frontmatter schema 增可选字段 `focus_target`(位置 goal_slug 之后、值域 `^T-\d{3}$`、创建期 open 校验、可选缺省合法);成组建队步骤与 slug 派生模式入 goal-based 过程规范
- [ ] T025 [P] [US3] 更新 `skills/create-team/references/execution-guide.md`:run 解析顺序(显式 > focus_target > 无)、三式披露与 [[STR-001]] 标记格式、报告行来源标记、台账 `target_ref` 归属;默认聚焦转终态后的拦截-重聚焦-重开路径(improve-team / `/speckit.goal targets --set open`)
- [ ] T026 [P] [US3] 扩展 `skills/create-team/references/goal.md`:focus_target 语义钉——run 级 `--target` 的预填,非写域声明、非 Goal–Team 绑定变更、不参与 goal 身份解析、不改 summary 交付目录
- [ ] T027 [P] [US3] 更新 `docs/reference/commands/team.md`(用户文档,无镜像):goal-based 创建流程、分解提议与成组批准、focus_target 语义与聚焦运行披露、territory 校验与 coordinate 移交;概念按 `shared/definitions/goal-definitions.md` 链接不复述
- [ ] T028 [US3] [blockedBy: T020,T021,T022,T023,T024,T025,T026,T027] 扇出落地:`python3 scripts/python/regen-command-copies.py` + `python3 scripts/python/sync-mirrors.py --write`(含新文件 `verify-territory-disjoint.py` 随 skills 对同步)
- [ ] T029 [US3] [blockedBy: T028] 镜像核验全表(Mirror Obligations 逐行):`cmp scripts/python/goal-utils.py .specify/scripts/python/goal-utils.py`;`cmp skills/create-team/scripts/verify-territory-disjoint.py .specify/skills/create-team/scripts/verify-territory-disjoint.py`(新镜像存在且一致);`python3 scripts/python/sync-mirrors.py --check` exit 0(SKILL.md、create-mode.md、goal.md、execution-guide.md、新脚本五行);`python3 scripts/python/regen-command-copies.py --check` exit 0(team.md 行,4 副本)
- [ ] T030 [US3] [blockedBy: T029] 运行三个新契约套件 + `tests/contract/test_run_target_assignment.py` + `tests/contract/test_overlap_verdicts.py` + `tests/contract/test_team_territory.py`(新面全绿 + 038 run 面/036 territory 面零回归),全量对照基线无新增;手工 QA quickstart §4–§6(3 Target goal → 3 队两两不相交;聚焦 run 披露与台账;verify 脚本四类 exit 码;重叠 → 披露移交 coordinate)

**Checkpoint**: US3 独立可测——切片集直接转化为可运行多团队编队,创建期解决写域纪律,聚焦运行闭环且无字段团队零感知

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: FR-014/FR-015 收口与全量回归

- [ ] T031 [P] FR-015 文档集完整性核查:检查 `skills/create-team/references/summary-mapping.md`——按 feature-ref.md 裁定 036 summary 语义零改动,预期结论"无需变更";仅当该文件存在 team.md frontmatter 字段清单时,补一行 focus_target 不参与 summary 的交叉引用(不引入语义)
- [ ] T032 全量回归收口:`bash scripts/bash/run-tests.sh --names-out /tmp/042-final.txt && comm -13 .specify/specs/042-goal-team-creation/baseline-failed.txt /tmp/042-final.txt` 输出必须为空(GATE-1);任何新增失败先二分归属再修复,禁止改基线文件消音
- [ ] T033 端到端演练:在隔离临时 repo root(`--repo-root /tmp/<dir>`)依 quickstart.md §1–§6 走黄金路径——定义 goal → goal-based create → 分析裁决分解 → `--check` 全过 → 合并批准逐条落盘 → 成组 3 队(territory exit 0)→ 聚焦 run(披露 `(团队默认)`、台账 target_ref)→ coordinate 冲突面;结果记入 verification.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖,立即开始;T001 冻结的基线贯穿全程
- **US1 (Phase 2)**: blockedBy T001;本需求无独立 Foundational phase——US1 即分支地基(requirements 明示),引擎面按 story 归属(US2 得 `--check`、US3 得 `resolve_effective_target` + verify 脚本),无跨 story 共享引擎前置
- **US2 (Phase 3)**: blockedBy US1 完成(同一模板文件的分支区域 + 同一测试文件的追加面,串行)
- **US3 (Phase 4)**: blockedBy US2 完成(成组建队消费分解产出的 open Target 集;共享模板与测试文件)
- **Polish (Phase 5)**: blockedBy 全部 story

### User Story Dependencies

- **US1 (P1)**: 无 story 间依赖;MVP 就是它
- **US2 (P1)**: blockedBy US1(分支识别/加载/分析是分解决策的宿主)
- **US3 (P1)**: blockedBy US2(每 Target 一队以既有 open Target 集为对象);三个 story 同为 P1 但构成递进增量,建议顺序交付

### Within Each User Story

- 契约测试先行且先行失败(T002/T010/T011/T018/T019)
- 引擎面先于消费它的模板措辞(T012→T013、T020/T021→T022/T023)
- 模板主文件 `templates/commands/team.md` 内部串行(T003→T004;T022→T023)
- 扇出(写)先行,核验(读)随后,测试/QA 收尾

### Parallel Opportunities

- 每 story 的两个测试任务 [P] 并行(T002+无;T010+T011;T018+T019——不同文件)
- US1:T005 ∥ T006(不同 skills 文件);US2:T014 ∥ T015;US3:T021 ∥ T022、T024 ∥ T025 ∥ T026 ∥ T027(四个不同参考/文档文件)
- 跨 story 不可并行:`templates/commands/team.md` 与 `tests/contract/test_goal_team_creation.py` 是两个全程串行面(这正是 tasks 规则"多 story 追加同一测试文件则 [P] 失效"的实例)

---

## Parallel Example: User Story 3

```bash
# 测试面并行(两个不同文件):
Task: T018 "创建 tests/contract/test_focus_target_resolution.py"
Task: T019 "扩展 tests/contract/test_goal_team_creation.py 成组+territory 组"

# 实现面并行(T021/T022 起步后,四个不同文件):
Task: T024 "create-mode.md focus_target schema"
Task: T025 "execution-guide.md run 解析顺序"
Task: T026 "references/goal.md focus_target 语义"
Task: T027 "docs/reference/commands/team.md 用户文档"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 单独成 MVP**——它是三个 P1 story 中最小且独立可交付的切片(窄 goal → 结构有据的单团队);US2、US3 为同优先级递进增量,不与 US1 捆绑(US2 自身可独立交付"goal 获得成组切片")。

1. Complete Phase 1: 基线冻结
2. Complete Phase 2 (US1) → **STOP and VALIDATE**: 独立测试 = 窄 goal 单团队 + 两类拒绝零产物
3. Complete Phase 3 (US2) → 独立验证:提议-批准闭环、goal.md 零手写
4. Complete Phase 4 (US3) → 独立验证:3 队成组 + 聚焦运行 + 逐字节等价钉
5. Complete Phase 5: 全量回归 + 端到端演练

### Incremental Delivery

1. Setup → 基线就绪
2. +US1 → 分支地基可测(MVP!)
3. +US2 → 宽泛 goal 获得分解纪律
4. +US3 → 用户诉求终点形态(N teams : 1 Goal)
5. Polish → FR-014 零回归 + FR-015 文档收口

---

## Notes

- [P] = 不同文件且无未完成依赖;`templates/commands/team.md` 与 `test_goal_team_creation.py` 全程串行
- Pin hygiene:副本清单从目录树推导(现存 4 份,勿硬编码清单副本);退出码断言用精确值(0/2/3/4 是契约本身);goal.md 逐字节不变用 mtime+内容双钉
- 每个扇出任务后必跟核验任务(Mirror Obligations 行枚举,非隐式副作用);sync-mirrors 失败按 FAIL 清单 `sudo chown` 修复后重跑(仓内既有教训)
- 提交粒度:每 story 收尾(测试+扇出+核验+QA 全绿)提交一次;T001 基线文件随首个提交入库
- 禁止事项:绕过引擎直写 `goal.md`、手改 `## Targets`、手工双写镜像、把基线失败当回归修、`--no-verify`
- Deferral discipline:宁可 `[~]` + 记录理由,不留 `[ ]` 挂账
