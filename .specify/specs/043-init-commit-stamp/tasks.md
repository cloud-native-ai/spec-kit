# Tasks: init 落章机制——以 commit id 为唯一标识的框架来源回溯(Framework Source Stamp)

**Requirement ID**: 043
**Requirement Key**: 043-init-commit-stamp
**Related Feature**: 045 Framework Source Provenance(feature-ref.md:Planned,实现后由 /speckit.implement 追加 implemented 记录)
**Input**: Design documents from `.specify/specs/043-init-commit-stamp/`(plan.md、requirements.md、data-model.md、contracts ×3、quickstart.md、feature-ref.md)
**Prerequisites**: plan.md ✅、requirements.md ✅、data-model.md ✅、contracts/ ✅、quickstart.md ✅

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation"(unit/contract/integration MUST)。本需求为纯引擎/CLI 代码面(非 template-only):解析与写入函数走进程内单元/契约测试,init 集成走 CliRunner 集成测试,构建钩子走 importlib 加载 + hatchling 接口 stub 的契约测试。

**Organization**: 按 user story 分组;解析核心(`_probe_head_commit`/`resolve_source_commit`)被 US1(git 形态)与 US3(嵌入形态)共同消费,按规则置于 **Foundational**;story 内测试先行。串行面:`tests/contract/test_source_stamp.py` 与 `tests/integration/test_init_source_stamp.py` 两个共享测试文件跨 story 追加(多 story 共文件则 [P] 失效,story 间严格顺序)。

**Environment Prerequisites(生成时已探测)**: python3.11 + pytest ✅、git ✅;**构建工具链不可用**(hatch/build/hatchling 均缺失)→ 真实 wheel 构建核验(T016)预标 **[~]-eligible**:替代路径为契约测试钉钩子行为 + `[~]` 记因(hatch 可得后补跑);若 `pip install build` 在内网镜像可达亦可就地满足。**pyproject.toml 在仓写门禁 confirm 名单**——T014 编辑前需用户确认。

## Definition of Done (DoD)

- DoD-1: 实现覆盖 FR-001..008(探测/解析/写入/init 调用点/构建钩子/声明/.gitignore),逐 FR 可溯源到任务
- DoD-2: 新测试文件全绿(test_source_stamp.py、test_build_hook.py、test_init_source_stamp.py),且全量套件对冻结基线零新增失败(name 级 comm)
- DoD-3: 三态语义闭合:有效 40-hex / [[STR-002]]+reason / 缺失=来源未知;臆造 id 出现 0 次;落章永不阻塞 init
- DoD-4: quickstart.md §1–§4 手工走查通过(📌 面转 ✅:init 落章、git show 回溯、刷新零残留、嵌入文件在包内或按 [~] 记因)
- DoD-5: SC-001..005 在 verification.md 中逐条给出状态与证据(实现期由 /speckit.implement 落笔)
- DoD-6: 用户文档落位(docs/tutorials/installation.md「来源标识」小节);Feature 复核无新增/失效(045 维持,无邻接 Feature 改动)

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件零新增失败 — check: `bash scripts/bash/run-tests.sh --names-out /tmp/043-final.txt && comm -13 .specify/specs/043-init-commit-stamp/baseline-failed.txt /tmp/043-final.txt` 输出为空
- GATE-2: 共享串语义 — check: `grep -c '"framework": "spec-kit"' <实测落章文件>` =1 且 commit 字段匹配 `^[0-9a-f]{40}$` 或逐字 `unavailable`;pyproject version 不出现在落章文件
- GATE-3: 无遗留任务行 — check: `grep -cE '^- \[[ >]\]' tasks.md` 返回 0
- GATE-4: verification.md 列全 SC-001..005 且各有状态 — check: `grep -cE '^SC-00[1-5]_status=' verification.md` = 5
- GATE-5: 新确定性面全部被契约钉住 — check: `pytest tests/contract/test_source_stamp.py tests/contract/test_build_hook.py tests/integration/test_init_source_stamp.py` 全绿

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行(不同文件、无未完成依赖);**[Story]**: US1/US2/US3;**[blockedBy: Txxx]**: 显式依赖
- Task State Sigil:`[ ]` Open / `[>]` Claimed / `[X]` Closed / `[~]` Deferred(理由记 verification.md `deferred_tasks=` + 行内注释)

## Path Conventions

改动画 = 仓根 `src/specify_cli/__init__.py`、`hatch_build.py`(新)、`pyproject.toml`(confirm 门)、`.gitignore`、`docs/tutorials/installation.md`、`tests/{contract,integration}/`;**零镜像面**(plan.md Mirror Obligations 显式声明)——无扇出/核验任务,构建产物 `src/specify_cli/_source_commit.json` 由 .gitignore 排除。

---

## Phase 1: Setup(共享基线)

**Purpose**: 冻结测试基线,区分存量失败与回归

- [X] T001 运行全量测试套件并冻结基线:`bash scripts/bash/run-tests.sh --names-out .specify/specs/043-init-commit-stamp/baseline-failed.txt`;存量失败清单与数量记入完成说明——后续一切回归判定以该文件为准

**Checkpoint**: 基线冻结,后续测试任务可做 name 级二分

---

## Phase 2: Foundational(解析核心——US1/US3 共同消费)

**Purpose**: 落地唯一 git 探测文法与三态解析函数(source-stamp-resolution.contract.md),全 story 的地基

- [X] T002 [blockedBy: T001] 创建 `tests/contract/test_source_stamp.py` 解析组:钉 source-stamp-resolution.contract.md C-1..C-3——临时真 git 仓夹具(`git init`+commit)monkeypatch `specify_cli.MODULE_DIR`:命中 → `origin=git` 且 commit 与 `git rev-parse HEAD` 逐字符一致;指向含 `{"commit": <40hex>, ...}` 嵌入文件的普通目录(探测失败)→ `origin=embedded`;两者皆无 → `origin=unavailable` 且 reason 非空;嵌入 JSON 畸形/字段非法 → unavailable 不抛;`_probe_head_commit` 对无 git 目录返回 `(None, reason)` 永不抛。先运行确认新断言 FAIL
- [X] T003 [blockedBy: T002] 在 `src/specify_cli/__init__.py` 实现解析核心:`_probe_head_commit(start_dir)`(subprocess `git -C <dir> rev-parse HEAD`,timeout 5s,`^[0-9a-f]{40}$` 校验,永不抛)、`_read_embedded_source_commit()`(读 `MODULE_DIR/_source_commit.json`,OSError/JSONError/字段非法=无嵌入)、`resolve_source_commit()`(恒定顺序 checkout git > embedded > unavailable,返回 `{commit, origin, reason}`,只读零写入)
- [X] T004 [blockedBy: T003] 运行 `pytest tests/contract/test_source_stamp.py -q` 全绿;`pytest tests/contract/ -q -k "specify_cli or cli"` 相邻面零回归

**Checkpoint**: 解析核心独立可测——三种形态的 commit 判定全部经引擎函数,零臆造

---

## Phase 3: User Story 1 - init 落章:可回溯的框架 commit 标识 (Priority: P1) 🎯 MVP

**Goal**: init 完成后目标项目存在 `.specify/source.json`,commit 为框架仓 HEAD;凭它 `git show` 命中精确切片。

**Independent Test**: 临时目录 init(经最小资源夹具)→ 落章文件存在、载荷逐字段正确、无 reason 键;对本仓 HEAD 与 HEAD~1 两个 commit 值分别落章后 `git show --quiet <id>` 均 exit 0。

### Tests for User Story 1(先写、先看它失败)

- [X] T005 [P] [US1] [blockedBy: T004] 扩展 `tests/contract/test_source_stamp.py` 写入组:钉 source-stamp-write.contract.md C-1..C-3——monkeypatch `resolve_source_commit` 返回有效 commit → `write_source_stamp(tmp)` 落 `<tmp>/.specify/source.json`,载荷逐字段断言(`framework` 逐字 [[STR-003]]、commit 原样、**reason 键不存在**、`stamped_at` 匹配 `^\d{8}T\d{6}Z$`);JSON/UTF-8/indent 2;monkeypatch `Path.write_text` 抛 OSError → 返回 False 且不抛;[[STR-001]] 路径常量断言
- [X] T006 [US1] [blockedBy: T005] 创建 `tests/integration/test_init_source_stamp.py`:conftest 最小资源夹具(`qoder_minimal_resource_path`)+ `RUNNER.invoke(app, ["init", "<tmp 项目名>", "--ai", "qoder", "--no-git", "--skip-tls"])`(沿 `tests/script_api.py` 模式)→ 断言 `<项目>/.specify/source.json` 存在且 commit 等于本仓 `git rev-parse HEAD`(真实 git 探测路径);SC-002 回溯闭环:monkeypatch 解析分别返回 HEAD 与 `git rev-parse HEAD~1` 两个值、各落一次章 → 对两 id 执行 `git show --quiet <id>` 均 exit 0 且各自正确

### Implementation for User Story 1

- [X] T007 [US1] [blockedBy: T005] 在 `src/specify_cli/__init__.py` 实现 `write_source_stamp(project_path) -> bool`:消费 `resolve_source_result`,载荷 `{"framework": "spec-kit", "commit": <40hex|unavailable>, ["reason": <仅不可得>], "stamped_at": _utc_compact_stamp()}`;`.specify` 目录防御性兜底创建;整体覆写;捕获自身 OSError/序列化异常 → 模块级 console 黄色告警一行、返回 False,永不抛、永不改 init 退出语义;成功静默
- [X] T008 [US1] [blockedBy: T006,T007] 在 `src/specify_cli/__init__.py` `init()` 打印 `"Project ready."` 之前插入唯一调用点 `write_source_stamp(project_path)`(fresh 与再次 init 必经;不改任何既有输出步骤);运行 T005/T006 全部测试转绿,`pytest tests/integration/ -q -k init` 既有 init 面零回归

**Checkpoint**: US1 独立可测——一次 init、一份标识、一次成功回溯(MVP)

---

## Phase 4: User Story 2 - 升级刷新:零旧值残留 (Priority: P2)

**Goal**: 再次 init(升级)后落章刷新为新 commit;存量项目零迁移获得标识;正式版本号零参与。

**Independent Test**: 写 A → 写 B → 文件含 B 且 grep A 为 0;无落章项目 init → 直接获得;落章文件任何字段不含 pyproject version。

### Tests + Verification for User Story 2

- [X] T009 [US2] [blockedBy: T008] 扩展 `tests/contract/test_source_stamp.py` 刷新组:monkeypatch 解析先后返回 commit A(40-hex 造值)与 commit B → 连续两次 `write_source_stamp` → 文件最终载荷=B、`grep A` 于文件 0 命中(零残留,FR-006);断言载荷任何字段的值不等于 `pyproject` 的 version 串(FR-002;读 pyproject 提取对比)
- [X] T010 [US2] [blockedBy: T009] 扩展 `tests/integration/test_init_source_stamp.py` 升级组:同一临时项目连续两次 `RUNNER.invoke(init)`(第二次 monkeypatch 解析返回新造值)→ 落章为新值;模拟存量项目(预置 `.specify/` 而无 source.json)→ init 后获得
- [X] T011 [US2] [blockedBy: T010] 运行 US2 测试组;若红,修复 `write_source_stamp` 覆写路径(整体覆写、不合并)至全绿——测试即规格,不为绿改断言

**Checkpoint**: US2 独立可测——回溯恒指向最近一次 init 的真实来源

---

## Phase 5: User Story 3 - 构建期嵌入与诚实降级 (Priority: P3)

**Goal**: wheel/sdist 形态经构建钩子嵌入源 commit;commit 不可得时 [[STR-002]]+reason 落章且 init 照常成功。

**Independent Test**: 钩子契约测试(monkeypatch 探测→嵌入文件字段;探测 None→unavailable;同一函数对象钉);unavailable 注入的 init → 哨兵落章+exit 0。

### Tests for User Story 3(先写、先看它失败)

- [ ] T012 [P] [US3] [blockedBy: T011] 创建 `tests/contract/test_build_hook.py`:钉 build-embedding.contract.md C-1..C-2——importlib 加载仓根 `hatch_build.py`(**测试前置向 `sys.modules` 注入 stub 的 `hatchling.builders.hooks.plugin.interface.BuildHookInterface`**,构建 API 仅在构建环境存在):① monkeypatch 探测返回固定 40-hex → `initialize()` 后 `src/specify_cli/_source_commit.json` 逐字段断言(commit/reason 缺席/embedded_at 形如时间戳);② 探测返回 None → `unavailable` + reason,钩子不抛;③ 钩子内部引用的探测函数与 `specify_cli._probe_head_commit` 为同一对象(防第二文法);④ monkeypatch 写入抛 OSError → `initialize()` 抛错(构建失败语义);⑤ 断言 pyproject.toml 含 `[tool.hatch.build.hooks.custom]` 且 `.gitignore` 含产物路径(声明钉)
- [ ] T013 [P] [US3] [blockedBy: T011] 扩展 `tests/contract/test_source_stamp.py` 降级组:monkeypatch 解析返回 `{"commit": None, "origin": "unavailable", "reason": "..."}` → `write_source_stamp` 载荷 commit 逐字 [[STR-002]] 且 reason 透传;monkeypatch `resolve_source_commit` 为嵌入 `unavailable` → 同语义透传(两级降级链)

### Implementation for User Story 3

- [ ] T014 [US3] [blockedBy: T012] 创建仓根 `hatch_build.py`(custom hook:initialize 经 importlib 复用 `src/specify_cli/__init__.py` 的 `_probe_head_commit(<仓根>)`,写 `src/specify_cli/_source_commit.json` = `{commit, [reason], embedded_at}`,wheel/sdist 幂等;探测失败嵌入 unavailable 不抛、写入失败抛);**经用户确认后**(confirm 门)编辑 `pyproject.toml` 增 `[tool.hatch.build.hooks.custom] path = "hatch_build.py"`,`​.gitignore` 增 `src/specify_cli/_source_commit.json`
- [ ] T015 [US3] [blockedBy: T013,T014] 扩展 `tests/integration/test_init_source_stamp.py` 降级组:monkeypatch 解析为 unavailable → `RUNNER.invoke(init)` 退出码 0(init 不被阻塞)且落章为 [[STR-002]] + reason;运行 US3 全部测试组转绿
- [ ] T016 [US3] [blockedBy: T014] 真实构建核验(环境预标 [~]-eligible:hatch/build 本机缺失):若 `python3 -m pip install build` 可达则 `python3 -m build --wheel` 后 `unzip -p dist/*.whl specify_cli/_source_commit.json` 断言 commit == `git rev-parse HEAD`(build-embedding 契约集成收口);不可达则置 `[~]` 并行内注释记因(hatchling 可得后补跑),契约测试 T012 已钉钩子行为为替代证据 <!-- deferred-eligible: build toolchain absent; T012 contract tests substitute -->

**Checkpoint**: US3 独立可测——分发形态可得、不可得显式、init 可用性不受 git 可达性绑架

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T017 [blockedBy: T015] 用户文档:在 `docs/tutorials/installation.md` 增「来源标识(source stamp)」小节——`cat .specify/source.json` → 框架仓 `git show <commit>` 回溯指引、三态语义表(沿 spec quickstart §5)、checkout 运行 CLI 的可执行形态(直跑 `src/specify_cli/__init__.py`,plan 勘测 `-m` 形态不可用);链接 `.specify/shared/definitions/goal-definitions.md` 式概念不复述原则不适用(无新概念面)
- [ ] T018 [blockedBy: T016,T017] 全量回归收口:`bash scripts/bash/run-tests.sh --names-out /tmp/043-final.txt && comm -13 .specify/specs/043-init-commit-stamp/baseline-failed.txt /tmp/043-final.txt` 输出必须为空;quickstart.md 📌 项按实现态复核(可执行者实跑转 ✅,T016 若 [~] 则对应项保持 📌 并注因)
- [ ] T019 [blockedBy: T018] 端到端演练:临时目录走 quickstart §1–§3——真 init(checkout 形态)→ 读落章 → 本仓 `git show <commit> --stat` 命中 → 再次 init 刷新零残留(grep 旧 id 0 命中);结果记 verification.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖;T001 基线贯穿全程
- **Foundational (Phase 2)**: blockedBy T001——解析核心是 US1(git 腿)与 US3(嵌入腿)的共同消费面
- **US1 (Phase 3)**: blockedBy Phase 2
- **US2 (Phase 4)**: blockedBy US1(覆写语义建立在写入函数与集成夹具之上;共享两个测试文件的追加面)
- **US3 (Phase 5)**: blockedBy US2(同上串行;钩子与降级为最后叠加面)
- **Polish (Phase 6)**: blockedBy 全部 story

### User Story Dependencies

- **US1 (P1)**: 无 story 间依赖;**MVP = US1 单独成 MVP**(一次 init、一份标识、一次回溯)
- **US2 (P2)**: blockedBy US1(覆写即写入函数行为的刷新面)
- **US3 (P3)**: blockedBy US2(嵌入/降级叠加在已可用的落章链路上;三态语义的最后一态)

### Within Each User Story

- 契约测试先行且先行失败(T002/T005+T006/T009/T012+T013)
- 引擎函数先于 init 集成点(T007→T008)
- 共享测试文件(`test_source_stamp.py`、`test_init_source_stamp.py`)跨 story 串行追加——[P] 仅出现在不同文件对(T005∥T006、T012∥T013)

### Parallel Opportunities

- Phase 3:T005 ∥ T006(契约写入组 vs 集成新建,不同文件)
- Phase 5:T012 ∥ T013(钩子契约新建 vs 写入降级组扩展,不同文件)
- 其余共享文件面全串行

---

## Parallel Example: User Story 3

```bash
# 测试面并行(两个不同文件):
Task: T012 "创建 tests/contract/test_build_hook.py(hatchling stub 前置)"
Task: T013 "扩展 tests/contract/test_source_stamp.py 降级组"

# 随后串行:
Task: T014 "hatch_build.py + pyproject(confirm)+ .gitignore"
Task: T015 "集成降级组 + 全绿"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1**——最小独立可交付切片(checkout 形态完整闭环);US2/US3 为递进增量。

1. Complete Phase 1: 基线冻结
2. Complete Phase 2: 解析核心可测
3. Complete Phase 3 (US1) → **STOP and VALIDATE**: init → 落章 → git show 命中
4. Complete Phase 4 (US2) → 独立验证: 刷新零残留
5. Complete Phase 5 (US3) → 独立验证: 嵌入 + 哨兵降级
6. Complete Phase 6: 文档 + 回归 + 端到端

### Incremental Delivery

1. Setup → Foundational:地基可测
2. +US1 → MVP!
3. +US2 → 升级安全
4. +US3 → 分发形态全覆盖
5. Polish → 文档收口与全量回归

---

## Notes

- [P] = 不同文件且无未完成依赖;两个共享测试文件是全程串行面
- Pin hygiene:commit 断言用 `^[0-9a-f]{40}$` 正则(不硬编码具体 id——HEAD 会前进);探测超时/失败是数据不是错误,断言返回形不抛;时间戳断言形 `^\d{8}T\d{6}Z$`(不断言具体时刻)
- 测试不臆造:所有 unavailable 断言都配 reason 非空;`_probe_head_commit` 的同一对象钉(T012 ③)防第二套 git 文法
- T014 触 confirm 门:pyproject.toml 编辑前征得用户确认(仓 gate.yaml confirm 名单)
- 提交粒度:每 story 收尾提交一次;T001 基线文件随首个提交入库
- 禁止事项:落章写入 pyproject version、落章失败阻塞 init、第二套 git 探测实现、绕过 hatchling stub 直接 import hatch_build 测试、改基线文件消音
- Deferral discipline:T016 为预标 [~]-eligible 唯一候选;其余任务不留 [ ]
