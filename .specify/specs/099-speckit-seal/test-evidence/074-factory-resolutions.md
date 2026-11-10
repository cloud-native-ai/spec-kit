# 074 回合 — T039 输入处置记录（recheck-clean）

生成时间：2026-11-10T17:12:13Z（本记录由回合执行者逐条写入，不建第二份台账）

## A. 合并清单 36 条 `factory-doc-ref-ambiguous` 的逐条处置（18 个源引用 × 源/镜像双扫）

处置形式全部为 C-018 `recheck-clean`：修复输入（出厂文档引用措辞）后重跑不再复现。`kind` 按 C-017 封闭集记 `literal` 或 `repoint`。镜像副本由 `sync-mirrors.py --write` 从源投影，与源逐字节一致（`sync-mirrors.py --check` exit 0）。

| # | 源文档:行 | token（冲突对） | 语义登记处 | kind | before → after |
|---|-----------|-----------------|------------|------|----------------|
| 1 | `shared/definitions/flow-class-definitions.md:10` | `STR-004` | 069 § Shared Strings（`未声明·按默认`） | literal | 四个共享字面量（`[[STR-001]]` / `[[STR-002]]` / `[[STR-003]]` / `[[STR-004]]`）→（`execution` / `expression` / `flow_class` / `未声明·按默认`） |
| 2 | `shared/definitions/sdd-routing-definitions.md:8` | `STR-004` | 074a 本地 004=`sdd`（父级同号同义） | literal | 三值裁决表（`[[STR-004]]` …）→（`sdd` / `direct` / `adjudicate`） |
| 3 | `shared/definitions/sdd-routing-definitions.md:8` | `STR-005` | 074a 本地 005=`direct` | literal | 同上行，`[[STR-005]]` → `direct` |
| 4 | `shared/definitions/sdd-routing-definitions.md:8` | `STR-006` | 074a 本地 006=`adjudicate` | literal | 同上行，`[[STR-006]]` → `adjudicate` |
| 5 | `shared/definitions/subagent-definitions.md:175` | `STR-004` | 074a 本地 004=`sdd` | literal | the `sdd` verdict ([[STR-004]]) → (the literal `"sdd"`) |
| 6 | `shared/definitions/subagent-definitions.md:175` | `STR-005` | 074a 本地 005=`direct` | literal | `direct` ([[STR-005]]) → (`"direct"`) |
| 7 | `shared/definitions/subagent-definitions.md:175` | `STR-006` | 074a 本地 006=`adjudicate` | literal | `adjudicate` ([[STR-006]]) → (`"adjudicate"`) |
| 8 | `shared/workflow/expression-gates.md:172` | `STR-004` | 069 § Shared Strings（`未声明·按默认`） | literal | （[[STR-004]]，未声明·按默认）→（`未声明·按默认`） |
| 9 | `skills/internal/create-team/SKILL.md:99` | `STR-004` | 074b 本地 004=`completed` → 父 `STR-007` | literal | `[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]` → `completed` / `blocked` / `failed` |
| 10 | `skills/internal/create-team/SKILL.md:99` | `STR-005` | 074b 本地 005=`blocked` → 父 `STR-008` | literal | 同上行 |
| 11 | `skills/internal/create-team/SKILL.md:99` | `STR-006` | 074b 本地 006=`failed` → 父 `STR-009` | literal | 同上行 |
| 12 | `skills/internal/create-team/SKILL.md:101` | `STR-005` | 074b 本地 005=`blocked` | literal | `[[STR-005]]` / `[[STR-006]]` → `blocked` / `failed` |
| 13 | `skills/internal/create-team/SKILL.md:101` | `STR-006` | 074b 本地 006=`failed` | literal | 同上行 |
| 14 | `skills/internal/create-team/references/goal.md:39` | `STR-004` | 038 § Shared Strings（`goal-definitions.md → Target Decomposition(目标切片)`） | literal | Target Decomposition([[STR-004]]) → Target Decomposition(§ Target Decomposition 目标切片) |
| 15 | `skills/external/sdd-loop-driver/SKILL.md:163` | `STR-007` | 093 § Shared Strings（`decomposition-coverage`） | literal | （[[STR-007]]，内置缺省的唯一 owner）→（`decomposition-coverage`，…） |
| 16 | `skills/external/sdd-loop-driver/references/decomposition-model.md:327` | `STR-007` | 093 § Shared Strings（`decomposition-coverage`） | literal | (`[[STR-007]]`) → (`decomposition-coverage`) |
| 17 | `skills/external/sdd-loop-driver/references/nested-invocation.md:40` | `STR-007` | 074a 本地 007=`completed`（父级同号同义） | literal | [[STR-007]] / [[STR-008]] / [[STR-009]] → `completed` / `blocked` / `failed`（同一字面量也落到 :72、:78 两处 `已声明` 的 outcome 引用，见 B） |
| 18 | `templates/plan-template.md:200` | `STR-006` | 说明性示例（非引用） | literal | `[[STR-002]]`…`[[STR-006]]` → `STR-002`…`STR-006` |

镜像对应：以上 18 处在 `.specify/shared/**`、`.specify/skills/**`、`.specify/templates/**` 的同名副本由 `sync-mirrors.py --write` 同批投影（36 条冲突中的另外 18 条随之清除）。

## B. 同批 `factory_doc_refs` 重指向（非冲突，引擎原会自动改写的 3 处）

| # | 源文档:行 | before | after | kind | 依据 |
|---|-----------|--------|-------|------|------|
| B1 | `shared/definitions/sdd-routing-definitions.md:16` | `[[STR-001]]` … `[[STR-010]]` 的取值与语义 owner 是本特性切片的 `requirements.md` | `[[STR-001]]` … `[[STR-011]]` 的取值与语义 owner 是合并后的父规格 `.specify/specs/074-goal-team-sdd-unification/requirements.md` § Shared Strings | repoint | 074a `## Parent Mapping` 声明本地 `STR-010`(`seats`) → 父 `STR-011`；合并后父级为唯一现行权威（C-019） |
| B2 | `shared/definitions/sdd-routing-definitions.md:28` | `[[STR-010]]` 块映射 | `[[STR-011]]` 块映射 | repoint | 同上 |
| B3 | `shared/definitions/sdd-routing-definitions.md:71` | 席位侧载体为 `[[STR-010]]` 块映射 | 席位侧载体为 `[[STR-011]]` 块映射 | repoint | 同上 |

## C. 分片 STR 同号不同义的声明映射核验（T039 的映射面）

| 组 | 分片本地 | 父级目标 | 值 | 核验 |
|----|----------|----------|----|------|
| 074a | `STR-010` | `STR-011` | `seats` | `merge-plan-after.json` 的 `id_maps.STR` 含该条（kind=localization/mapped） |
| 074b | `STR-004` | `STR-007` | `completed` | 同上 |
| 074b | `STR-005` | `STR-008` | `blocked` | 同上 |
| 074b | `STR-006` | `STR-009` | `failed` | 同上 |
| 074b | `STR-007` | `STR-010` | `## Nested SDD Runs` | 同上 |

## D. 父 requirements 的 `**Path**` 标记（T039(b)，严格默认 `final`，逐条记录）

| SC | 行（首行） | 决策 | 依据 |
|----|-------------|------|------|
| SC-001 | 392 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-002 | 396 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-003 | 401 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-004 | 404 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-005 | 407 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-006 | 410 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-007 | 412 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |
| SC-008 | 414 | `**Path**: final`（行尾，恰一个） | FR-027(a)：缺标记使闭包判定器 exit 2；严格默认取更严格一侧并逐条记录 |

补标记前实测：`grep -c "\*\*Path\*\*"` = 0（2026-11-10）；补标记后 = 8（每条 SC 恰一个、行尾）。

## E. 由该轮词汇对齐强制更新的消费者 pin（3 处，逐条记录）

| 文件 | before | after | 理由 |
|------|--------|-------|------|
| `tests/contract/test_nested_run_report.py` | `OUTCOME_STRINGS = ("STR-004","STR-005","STR-006")`，断言 `[[STR-xxx]]` | `OUTCOME_STRINGS = ("completed","blocked","failed")`，断言反引号字面量 | 报告契约按 A9–A13 改写字面量后，断言须指向当前词汇；否则新增失败（GATE-1） |
| `tests/contract/test_nested_sdd_invocation.py` | `OUTCOME_STRINGS = ("STR-007","STR-008","STR-009")`，断言 `[[STR-xxx]]` | `OUTCOME_STRINGS = ("completed","blocked","failed")`，断言反引号字面量 | 同上（A17 及 B 节） |
| `tests/contract/test_sdd_routing_definitions.py` | `REQUIREMENTS_PATH` = `074a-authorized-routing/requirements.md` | 指向 `074-goal-team-sdd-unification/requirements.md` | owner 文档的登记处已按 B1 重指向合并后父级；引用解析须读当前权威 |
