# Tasks: 浏览器站点记忆与分级自动化(需求 046 / Feature 048)

**Requirement → Feature**: `046-browser-site-memory` → Feature 048 Browser Utils Skill
**Tests Mode**: ON(Constitution Principle IV "Test-First & Contract-Driven Implementation";契约测试先行,每个故事先红后绿)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Environment prerequisites**(已在生成时探测):Python 3.11 ✓;hatchling 可导入 ✓(wheel 构建测试需要);无 docker/集群/外部站点依赖;引擎为 stdlib-only,契约测试全部本地文件级。

## Definition of Done (DoD)

- DoD-1: site-memory.py 引擎 7 个 action 全部实现且契约测试通过(contracts/site-memory-engine.md)
- DoD-2: 状态机迁移/脱敏强制/文件格式按 contracts/site-memory-formats.md 全覆盖测试
- DoD-3: 分发排除三收口(gitignore / sync-mirrors site 分量 / hatch_build 舞台拷贝)各有确定性验证
- DoD-4: SKILL.md 路由段 + 两个新 references 落地,技能镜像字节一致,sync-mirrors --check 退出 0
- DoD-5: 全套件零新增失败(对 T001 基线)
- DoD-6: quickstart.md 三个走查的 CLI 示例对真实引擎执行验证通过

**DoD Status**: pending

## Completion Gate

- GATE-1: 全套件零新增失败 vs 基线 — check: `pytest` 失败集与 `.specify/specs/046-browser-site-memory/baseline-failed.txt` 做集合差
- GATE-2: 技能镜像字节一致 — check: `python3 .specify/scripts/python/sync-mirrors.py --check`(skills 对)
- GATE-3: wheel 不含 site/ — check: 植探针后 `python3 -m hatchling build -t wheel`,namelist 无 `specify_cli/skills/browser-utils/site/`
- GATE-4: 无 `[ ]` / `[>]` 任务行残留 — check: `grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- GATE-5: verification.md 列出全部 SC-001..005 及状态 — check: grep SC id 对 requirements.md

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 运行全套件记录失败基线到 `.specify/specs/046-browser-site-memory/baseline-failed.txt`(pytest 全量,失败名单一行一个,用于 GATE-1 集合差)

## Phase 2: Foundational (Blocking Prerequisites)

框架分发排除(FR-003 / contracts/framework-exclusions.md)——阻断后续一切(site/ 数据一旦产生即依赖三收口)。

- [X] T002 编写 `tests/contract/test_browser_site_exclusions.py`(先红):断言 (a) `.gitignore` 含 `skills/browser-utils/site/` 与 `.specify/skills/browser-utils/site/` 两行且 `git check-ignore` 命中探针路径;(b) sync-mirrors.py `MIRROR_PAIRS` skills 对 exclude_parts 含 `"site"`;(c) pyproject.toml wheel force-include 无静态 `"skills"` 行;(d) X-7 闭环——植探针文件、构建 wheel、断言无 site/ 条目且 SKILL.md 在场
- [X] T003 [P] 根 `.gitignore` 追加 `skills/browser-utils/site/` 与 `.specify/skills/browser-utils/site/` 两行,`git check-ignore -v` 双向验证 [blockedBy: T002]
- [X] T004 [P] `scripts/python/sync-mirrors.py` 与镜像 `.specify/scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS` skills 对 exclude_parts 增加 `"site"` 分量(两副本同步编辑,diff -q 验证一致;放探针文件后 `--check` 退出 0) [blockedBy: T002]
- [X] T005 `src/hatch_build.py` initialize 增加 skills 舞台拷贝(剔除任何路径分量为 `site` 的目录,经 `tempfile`+`shutil.copytree(ignore=...)` 实现,注册 `build_data["force_include"]`;拷贝失败使构建失败)+ `pyproject.toml` 移除 `[tool.hatch.build.targets.wheel.force-include]` 中 `"skills" = "specify_cli/skills"` 静态行 [blockedBy: T002]
- [X] T006 运行 `pytest tests/contract/test_browser_site_exclusions.py` 转绿 [blockedBy: T002,T003,T004,T005]

## Phase 3: User Story 1 - 探索期:完成任务的同时完整留痕 (Priority: P1) 🎯 MVP

**Goal**: 陌生站点首次任务完整完成,DOM 操作与网络请求全量脱敏留痕,引擎骨架可用。

**Independent Test**: 对测试站点执行一次任务,site/<host>/ 下产出完整 records,脱敏违规即拒绝写入,validate-records 给出完整性判定。

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T007 [US1] 编写 `tests/contract/test_browser_site_memory.py`(先红):覆盖 contracts/site-memory-engine.md 的 init(URL→目录名导出、幂等)、get-state(正常/缺失/损坏三态)、append-record(schema 校验、seq 连续、S-1/S-2/S-3 脱敏拒绝——含 `Bearer ` 前缀与高熵串用例)、validate-records(完整性判定、ok=false 需 error 字段、≥1 network 记录);用 tmp_path 构造 skill-home 夹具

### Implementation for User Story 1

- [X] T008 [US1] 实现 `skills/browser-utils/scripts/site-memory.py`(stdlib-only,≥3.8):CLI 骨架(--action/--format/--skill-home,退出码 0/1/2,JSON 信封)+ init / get-state / append-record / validate-records 四个 action;脱敏侦测规则按 contracts/site-memory-formats.md §4 S-1..S-3;单文件原子写(临时文件+rename) [blockedBy: T007]
- [X] T009 [US1] 运行 `pytest tests/contract/test_browser_site_memory.py` 中 US1 用例转绿;同步技能镜像(`python3 .specify/scripts/python/sync-mirrors.py --write` 后 diff 验证 `skills/browser-utils/scripts/site-memory.py` 两副本一致) [blockedBy: T008]

## Phase 4: User Story 2 - 能力分层与双方向路由 (Priority: P1)

**Goal**: SKILL.md 入口路由贯通"Tier 判定 → 站点状态路由 → 方向选择",机制细节落 references/。

**Independent Test**: grep 结构断言 + skill-shape 门 + 人工走读决策树三种能力环境 × 两种记忆状态的路由正确性。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T010 [US2] 在 `tests/contract/test_browser_site_memory.py` 追加结构契约用例(先红):SKILL.md 含"Site Memory"(或等价命名)路由节且引用四个状态字面量(exploration/optimization/validation/sealed);`references/site-memory.md` 与 `references/request-level-patterns.md` 存在且被 SKILL.md 指针引用 [blockedBy: T009]

### Implementation for User Story 2

- [X] T011 [US2] `skills/browser-utils/SKILL.md` 新增"站点记忆与双方向路由"节(契约级,遵守 skill-shape 门):策略选择决策树扩展——Tier 判定后对 Tier 2/3 站点任务先 `get-state` 路由(exploration=页面级+全量留痕;optimization=混合;validation=执行 recipe;sealed=直接 recipe 零探测,失败回退);页面级 vs 请求级方向选择指引(FR-002) [blockedBy: T010]
- [X] T012 [P] [US2] 编写 `skills/browser-utils/references/site-memory.md`:状态机语义、记录/配方/证据格式指针(指 contracts 真源不复制)、engine CLI 用法、探索/优化/验证/sealed 各态执行要点 [blockedBy: T010]
- [X] T013 [P] [US2] 编写 `skills/browser-utils/references/request-level-patterns.md`:请求级方向模式——Playwright `page.on('request')` 捕获 + `page.evaluate(fetch(...))` 重放(继承会话)、Tier 3 经 bridge evaluate/execInPage 的同等通道、动态字段解析来源标注惯例(吸收 2026-08-22 PoC 结论) [blockedBy: T010]
- [X] T014 [US2] 结构验证:技能镜像同步 + `diff -q` 三文件两副本一致;`python3 .specify/skills/improve-skills/scripts/skill-shape.py skills/browser-utils/SKILL.md` 退出 0;T010 结构用例转绿 [blockedBy: T011,T012,T013]

## Phase 5: User Story 3 - 优化期:从操作记录蒸馏请求级步骤 (Priority: P2)

**Goal**: write-recipe 与状态迁移门(exploration→optimization→validation)确定性判定。

**Independent Test**: 以探索期 records 为输入,合法 recipe 落盘并通过迁移;非法迁移(跳态/缺前置)被拒绝并输出原因。

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T015 [US3] 扩展 `tests/contract/test_browser_site_memory.py`(先红):write-recipe schema 用例(request 步缺 expect 拒绝、page 步缺 reason 拒绝、distilled_from 指向不存在文件拒绝);transition 迁移表用例(exploration→optimization 需 records 完整、optimization→validation 需合法 recipe、跳态拒绝并输出合法目标) [blockedBy: T009]

### Implementation for User Story 3

- [X] T016 [US3] 在 `skills/browser-utils/scripts/site-memory.py` 实现 write-recipe 与 transition(迁移前置判定全部确定性,按 data-model.md §2 迁移表;回退类迁移 --evidence 必填;history 追加带证据) [blockedBy: T008,T015]
- [X] T017 [US3] US3 用例转绿 + 镜像同步验证 [blockedBy: T016]

## Phase 6: User Story 4 - 验证期与 sealed:状态机驱动的固化与回退 (Priority: P3)

**Goal**: record-validation 落盘证据并自动迁移(pass→sealed / fail→optimization),sealed 漂移失败人工回退。

**Independent Test**: 构造 pass/fail 两种证据分别验证自动迁移与回退;sealed 后 transition --to optimization 带漂移证据成功;回退后 records/recipe/validation 零丢失。

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T018 [US4] 扩展 `tests/contract/test_browser_site_memory.py`(先红):record-validation(pass→sealed、fail→optimization 自动回退、fail 时 failures 非空校验、状态不符时证据落盘但迁移拒绝);sealed→optimization 回退需 --evidence;回退后既有文件存在性断言(SC-004) [blockedBy: T017]

### Implementation for User Story 4

- [X] T019 [US4] 在 `skills/browser-utils/scripts/site-memory.py` 实现 record-validation 与 sealed 回退路径(verdict 驱动自动迁移;迁移拒绝不阻碍证据落盘) [blockedBy: T016,T018]
- [X] T020 [US4] US4 用例转绿 + 镜像同步验证 [blockedBy: T019]

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T021 quickstart.md 三个走查 + 异常走查的全部 CLI 示例对真实引擎逐一执行验证(tmp skill-home),输出与契约信封一致(DoD-6) [blockedBy: T020]
- [X] T022 运行全套件,失败集与 baseline-failed.txt 集合差为空(GATE-1);`sync-mirrors.py --check` 退出 0(GATE-2);wheel 探针构建复核(GATE-3) [blockedBy: T021] <!-- waiver: 范围化验收(用户批准 2026-08-24)——新增失败 14 个全部归因于并行 root 会话 create-pages 工作进行态(root-owned assets / 镜像未同步 / .migration-backups);本次改动的 2 个真实回归已修复转绿;046 自有镜像逐文件 diff -q 通过 -->
- [X] T023 复核 plan.md Mirror Obligations 表逐行打勾;更新 `.specify/memory/features/048.md` Implementation Notes 补引擎/契约测试落点

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1(基线)→ Phase 2(分发排除,阻断 site/ 数据落地)→ Phase 3-6(用户故事,P1→P1→P2→P3)→ Phase 7
- US2(Phase 4)仅文档面,与 US1 引擎面弱耦合;但结构用例断言的引用文件须真实存在,故排在引擎骨架之后

### User Story Dependencies

- US1(引擎骨架+留痕)是 US3/US4 的共同前置(engine 文件单一,序列化演进)
- US2(路由文档)独立可交付,仅需 SKILL.md 与 references
- US3 → US4:record-validation 依赖 transition 实现

### Parallel Opportunities

- T003 / T004 可并行(不同文件)
- T012 / T013 可并行(不同 references 文件)
- 引擎实现任务(T008/T016/T019)因同一文件不可并行

## Parallel Example: User Story 2

```bash
# T010 结构用例(红)先行,随后并行起草两份 references:
#   T012 references/site-memory.md
#   T013 references/request-level-patterns.md
# 汇合后 T011 SKILL.md 路由段,最后 T014 统一验证
```

## Implementation Strategy

1. **MVP = Phase 1+2+3**:分发排除 + 引擎骨架 + 探索期留痕,即可支撑首个真实站点的探索期运行。
2. US2 文档面紧随其后(每次技能调用都经过路由段,优先级同为 P1)。
3. US3/US4 按序演进同一引擎文件,每步先红后绿。
4. Phase 7 以真实执行走查与全套件基线差收口。
