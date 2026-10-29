# Tasks-stage deterministic checks — slice 074a-authorized-routing

**Stage**: tasks（`/speckit.tasks`，`decomposition=single-package`，无子代理派发）
**Slice**: `.specify/specs/074a-authorized-routing/`
**Stage base**: `907d21fbe`（074a plan 完成提交）
**Recorded**: 2026-10-29T02:17Z
**Host**: python3（本机 PATH），pytest 8.4.2，git

本文件只贴各确定性检查的**真实输出**与偏离裁定；结论不复述到其他产物。

## 1. 入口前提（command `scripts:` 块）与就地撰写理由

```text
$ bash scripts/bash/check-prerequisites.sh --json
{"REQUIREMENTS_DIR":"/storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification","REQUIREMENT_ID":"074","FEATURE_ID":"074","FEATURE_NAME":"Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）","AVAILABLE_DOCS":["research.md","data-model.md","contracts/","quickstart.md","checklists/","feature-ref.md"],"MODE":"C","WRITABLE":true}
rc=0
```

- **实测**：前提脚本按分支前缀解析到**父** spec 目录（`.specify/specs/074-goal-team-sdd-unification`），不是切片目录——分支名为 `074-goal-team-sdd-unification`，前缀匹配命中父目录。故 `REQUIREMENTS_DIR` 由派发简报覆盖为 `.specify/specs/074a-authorized-routing/`；未切换分支、未触碰父 `tasks.md`。
- **派发简报的前提偏差（实测优先于简报）**：简报称可能失败的脚手架脚本是 `create-new-tasks.sh`。实测该脚本在仓库内**不存在**：`find . -name "create-new-tasks*" -not -path "./.git/*"` → 0 命中；`scripts/bash/` 与 `.specify/scripts/bash/` 内只有 `create-new-requirements.sh` / `create-new-plan.sh` / `create-new-skill.sh` / `create-new-tools.sh`。因此切片 `tasks.md` 按 `templates/commands/tasks.md` → `create-tasks` 技能 → `templates/tasks-template.md` **就地撰写**，失败原因类别是「该脚手架不存在」，不是「前缀碰撞」；前缀碰撞的实际受害者是上一条 Prerequisites 解析。

## 2. 生成时实测的分母（Measured Premises 的复算）

```text
$ grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/074a-authorized-routing/requirements.md   → 20
$ grep -cE '^\- \*\*SC-[0-9]+\*\*:' .specify/specs/074a-authorized-routing/requirements.md   → 6
$ grep -cE '^\| `STR-[0-9]+`' .specify/specs/074a-authorized-routing/requirements.md          → 10
$ for f in …/contracts/*.md; do grep -cE '^\*\*C-[0-9]+\*\*' "$f"; done
  bootstrap-and-maintenance.md 4 / hierarchy-and-authorization.md 16 / nested-invocation.md 13 / routing-decision.md 14
$ grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md | wc -l                                       → 47
$ grep -cE '^- \[[ xX>~]\] T[0-9]{3}' .specify/specs/074a-authorized-routing/tasks.md           → 32
```

9 个新文件逐个 `test -e` → 9/9 ABSENT（3 个框架文件 + 5 个测试文件 + 1 个夹具），红先前提成立。
`grep -c 'sdd-invocation' src/specify_cli/__init__.py` → `0`（**陷阱形**：全仓 `grep -rn` 会命中本切片设计文档的说明文字，那是引用不是定义，故计量单位取代码 owner 文件）。

## 3. 结构校验（`validate-tasks.py`）

首稿（32 行、47 claims）报两条 `parallel-safe` WARN：

```text
WARN  194: parallel-safe: [P] tasks T026 (line 194) and T027 (line 195) both WRITE ['shared/definitions/sdd-routing-definitions.md'] in phase `## Phase 6: Polish & Cross-Cutting Concerns`
WARN  195: parallel-safe: [P] tasks T027 (line 195) and T028 (line 196) both WRITE ['notes/quickstart-run.md'] in phase `## Phase 6: Polish & Cross-Cutting Concerns`
PASS (with warnings): …tasks.md — 0 error(s), 2 warning(s)
```

按行内实际写目标逐条裁定：

| WARN | 实际写目标 | 裁定 |
|------|-----------|------|
| T026 × T027 争 `shared/definitions/sdd-routing-definitions.md` | T026 只 `cmp` 只读该源文件（写的是 `.specify/` 投影）；T027 只读它做反向计数（写的是 `notes/quickstart-run.md`） | 误报：两者都不写该源文件。但 `[P]` 保留会让机器判据持续报警，故与下一条同一处置：Polish 段整体去掉 `[P]`，按行序串行 |
| T027 × T028 争 `notes/quickstart-run.md` | 两行都向同一追加落点写入 | **真冲突**：去掉 T028 的 `[P]`（正是该 WARN 给出的补救），未删任何被点名的路径 |

定稿：

```text
$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/074a-authorized-routing/tasks.md
PASS: .specify/specs/074a-authorized-routing/tasks.md — 0 error(s), 0 warning(s)
rc=0
$ grep -cE '^- \[[ xX>~]\] T[0-9]{3}' …/tasks.md   → 32
```

## 4. 分解规模（`decomposition-check.py --mode tasks`）

```text
$ python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks \
    --requirements .specify/specs/074a-authorized-routing/requirements.md \
    --tasks .specify/specs/074a-authorized-routing/tasks.md
{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 20, "task_count": 32, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": [], "checked_at": "2026-10-29T02:17:21Z"}
rc=0
```

32 ≤ 40、20 ≤ 30：本切片自身**不**触发再拆。父规格 57 行的 `split-required` 是拆分来源，切片化后已消解。

## 5. 条款覆盖（`account-clause-coverage.py`）

冻结前（首次全树核算，baseline 尚不存在——按设计为红，不冒充为绿）：

```text
claimed clauses (this feature): 47
baseline: .specify/specs/074a-authorized-routing/coverage-baseline.txt (0 names, MISSING)
ERROR frozen baseline not found … freeze it with --freeze
  [clause-uncovered] fail (495) — 495 uncovered, 495 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms
496 error(s), 0 warning(s)
status: baseline-missing
```

claims 已存在，故按冻结时机冻结（`--freeze`，脚本只打印、不写文件）：

```text
$ python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/074a-authorized-routing --freeze > …/coverage-baseline.txt
rc=0；497 行；头部：
# frozen-from: .specify/specs/*/contracts/* excluding 074a-authorized-routing | … | base-sha: 907d21fbe065 | files: 208 (parsed 114 + named 94)
```

冻结后复算：

```text
companion (must be non-empty on a green run): claimed clauses 47, scanned files 212, clause universe 1285, FR universe 20
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms; 0 of them declare a positive form
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
0 error(s), 0 warning(s)
status: ok
```

基线正文不含本切片 47 条 `C-N` 名（`--freeze` 排除被核算 spec 本身）：本切片条款只能被任务行认领，不能被自己的基线豁免。

## 6. 跨产物一致（`pre-analyze-check.py --stage tasks`）

```text
pre-analyze-check: stage=tasks decision=pass errors=0 advisories=65 waived=0
summary: {"errors": 0, "advisories": 65, "waived": 0, "fr": 20, "sc": 6, "tasks": 32, "clauses": 0, "files": 12}
```

65 条 advisory **全部**是 `missing-path`，逐类裁定（无一为 blocking，不加 `--strict`）：

| 类 | 条数（约） | 命名对象 | 裁定 |
|----|-----------|----------|------|
| 本切片**将创建**的框架文件与测试文件 | 55 | `shared/definitions/sdd-routing-definitions.md`、`scripts/python/sdd-route.py`、`skills/external/sdd-loop-driver/references/nested-invocation.md`、5 个 `tests/contract/test_sdd_*.py`、`tests/fixtures/nested_sdd.py` | 任务阶段尚未创建，属预期；T004/T005/T011/T013/T014/T017/T019/T020 各行的交付面 |
| 兄弟切片目录 | 1 | `.specify/specs/074b-nested-governance` | 尚未开始，本切片 MUST NOT 创建 |
| 本切片确认为 074b 承接的测试 | 1 | `tests/contract/test_nested_run_report.py` | `feature-ref.md` § 2 明示归 074b |
| 继承的 requirements 检查清单引用 | 1 | `feedback/20261028T160637Z-speckit-requirements.md` | 既有的未跟踪运行记录（脏文件），不提交不还原 |
| `.specify/` 投影 | 1 | `.specify/scripts/python/sdd-route.py` | 由 T026 的镜像机构生成，非手写 |

## 7. 镜像与命令副本基线（改前，未做任何源编辑）

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
rc=0
$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
```

零漂移，故本切片每条镜像义务的判据是「相对该基线零**新增**差异」。

## 8. 任务分布与条款分区

```text
Setup 3（T001–T003；一对 [P]）· Foundational 2（T004–T005）· US1 11（T006–T016）
US2 5（T017–T021）· US3 4（T022–T025）· Polish 7（T026–T032）  合计 32
```

47 条款分区（每条恰一行认领一次；每文件内序号随行序单调）：

| 契约文件 | 分区 |
|----------|------|
| `hierarchy-and-authorization.md`（16） | C-1…C-2→T004、C-3→T008、C-4→T009、C-5→T010、C-6…C-8→T011、C-9…C-10→T023、C-11…C-14→T024、C-15…C-16→T025 |
| `routing-decision.md`（14） | C-17→T004、C-18…C-27→T017、C-28→T019、C-29→T020、C-30→T027 |
| `nested-invocation.md`（13） | C-31…C-33→T013、C-34…C-37→T014、C-38…C-40→T015、C-41…C-42→T016、C-43→T028 |
| `bootstrap-and-maintenance.md`（4） | C-44…C-46→T004、C-47→T028 |

## 9. Feature 表复审（tasks 阶段的强制项）

`pre-analyze` 与本阶段的分解结果均未暴露新增 / 合并 / 失效 Feature：切片继续复用 Feature 074 的注册行（`.specify/memory/features.md` 074 行），MUST NOT 新增注册行。已同步更新 `.specify/memory/features/074.md`（§ Latest Review 加 tasks 段、§ Implementation Notes 加「074a 切片 tasks 期裁定」、`Last Updated`）与 `.specify/memory/features.md` 074 行的 Last Updated 单元格；状态列保持 `Planned`（`Implemented` 属 `/speckit.implement`）。

## 10. 红线复核

- 父 spec 与父设计（`.specify/specs/074-goal-team-sdd-unification/**`，含父 `tasks.md`）零改动。
- 本阶段零 plan-owned 面改动 → 无 `PLAN-EDIT:`。
- 未派发子代理（`decomposition=single-package`）；未切换分支；未 push。
- 只提交本阶段产物（`tasks.md`、`coverage-baseline.txt`、本文件、特性登记两处）；运行记录与状态脊不入提交。
