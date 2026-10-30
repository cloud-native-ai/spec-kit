# Pre-change measurements — 078 Coaching Skills

**Collected**: 2026-10-30T08:02Z（UTC） | **HEAD**: `500ff7178a81` | **Branch**: `078-coaching-skills`
**Scope**: T001（六条命令 + 闭集逐文件 `git grep -c`）与 T002（条款覆盖基线重采 + 两车道读数）。
**Role**: 本文件是全特性「改动前侧」的唯一落点；后续任何行引用「改动前」时只指向本文件与 `../coverage-baseline.txt`。

## T001 — 改动前读数

### M1 — 旧名受版本管理文件数

```text
$ git grep -l "think-skills" | wc -l
88
$ echo $?
0
```

说明：单位是**文件**。`tasks.md` § Measured Premises 在 HEAD `bc0ea7fb` 的读数为 85；当前 88 的 +3 逐项为 `.specify/specs/078-coaching-skills/checklists/coaching-loop-2026-10-30.md`、`.specify/specs/078-coaching-skills/tasks.md`、`.specify/state/078-coaching-skills.md`——本特性自身在 tasks 成文后新增的制品。差异来自计量时点，不是设计分歧；SC-006 只以 A10 的封闭集为判据，不使用全仓计数。

### M2 — 闭集逐文件 `git grep -c`

```text
$ git grep -c "think-skills" -- skills/external skills/internal templates/commands agents shared/definitions src/specify_cli/__init__.py docs/reference/agents/command-and-skills.md docs/tutorials/quickstart.md tests/contract .specify/skills
.specify/skills/internal/create-agent/templates/agent-capacity-module-designer-template.md:2
.specify/skills/internal/create-agent/templates/agent-capacity-requirements-analyst-template.md:2
.specify/skills/internal/create-agent/templates/agent-capacity-system-designer-template.md:2
.specify/skills/internal/create-agent/templates/agent-capacity-test-engineer-template.md:2
.specify/skills/internal/run-skills/SKILL.md:1
.specify/skills/think-skills/SKILL.md:8
.specify/skills/think-skills/references/prompt-templates.md:1
agents/skill-verifier.agent.md:1
agents/structure-adjuster.agent.md:1
docs/reference/agents/command-and-skills.md:1
docs/tutorials/quickstart.md:1
shared/definitions/flow-class-definitions.md:1
shared/definitions/probe-definitions.md:1
skills/external/think-skills/SKILL.md:8
skills/external/think-skills/references/prompt-templates.md:1
skills/internal/create-agent/templates/agent-capacity-module-designer-template.md:2
skills/internal/create-agent/templates/agent-capacity-requirements-analyst-template.md:2
skills/internal/create-agent/templates/agent-capacity-system-designer-template.md:2
skills/internal/create-agent/templates/agent-capacity-test-engineer-template.md:2
skills/internal/run-skills/SKILL.md:1
src/specify_cli/__init__.py:1
templates/commands/skills.md:1
tests/contract/test_expression_compatibility.py:1
tests/contract/test_migration_distribution.py:1
tests/contract/test_run_skills_wiring.py:2
tests/contract/test_skill_layer_visibility_guards.py:1
$ echo $?
0
```

说明：26 个文件 = 19 个手改源 + 7 个派生镜像（`.specify/skills/…`）；命中次数最高的两处是技能本体与它的镜像（各 8 次）。单位是「某个文件内几次」；`src/specify_cli/__init__.py:1` 即 `_OBSOLETE_SKILLS` 之外的唯一历史注释命中（plan § Phase 0 第 2 条），改名时必须重述为不带旧名字面量。

### M3 — flow-class 台账与库存对账

```text
$ python3 scripts/python/flow-class-check.py --action check
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
$ echo $?
0
```

### M4 — probe 编译面

```text
$ python3 scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 75 units, zero drift
$ echo $?
0
```

### M5 — 阻断式确认门基线

```text
$ python3 scripts/python/scan-confirmation-gates.py --summary
blocking confirmation gates: 27
  destructive: 20
  governance_kept: 7
violations (reversible gates still blocking): 0
$ echo $?
0
```

### M6 — 旧技能形态基线

```text
$ python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/think-skills/SKILL.md
SKILL.md 形态检查 — skills/external/think-skills/SKILL.md
  判定        pass
  正文估算     ≈1981 tokens 可控 / 预算 5000（110 行）
  代码围栏     0 段 / 0 行 = 0%，其中非图示超 5 行 0 段
  最大章节     Workflow
  发现：
    ! [oversized-section] Workflow=51行（单章节建议上限 40 行；工作流骨架可适当超出，但应检查是否夹带手册内容）
    ! [flags-outside-contract] 23 个具体 CLI flag 出现在非约束章节：Wrap-up(23)
$ echo $?
0
```

说明：本读数只作新旧对照，不替代 T030 的 `--budget-tokens 5000` 判定。

## T002 — 条款覆盖基线重采与两车道读数

### 冻结命令

```text
$ python3 scripts/python/account-clause-coverage.py .specify/specs/078-coaching-skills --freeze > .specify/specs/078-coaching-skills/coverage-baseline.txt
$ echo $?
0
```

### 头部核对（`../coverage-baseline.txt`）

```text
# coverage-baseline: frozen UNCOVERED clause names, codepoint-sorted, one per line; compare with `LC_ALL=C comm -13 <this file> <live uncovered>` — the LC_ALL=C is load-bearing: glibc collation ignores # / and . at the first level, so under a UTF-8 locale these header lines sort AFTER the names, comm reports 'file 1 is not in sorted order' and then echoes all of file 2 as the delta
# frozen-from: .specify/specs/*/contracts/* excluding 078-coaching-skills | owner-forms: md-bold-closed,md-bold-paren,md-heading,yaml-openapi,yaml-assertions,md-none (md-none named, never silently covered) | clause-rules: shared/definitions/contract-clause-definitions.md | per-form counts: notes/clause-form-census.md | base-sha: 500ff7178a81 | files: 229 (parsed 135 + named 94)
```

- 头部含 `excluding 078-coaching-skills`：成立（仅第 2 行出现该串，是冻结口径声明）。
- 正文不含本特性任何一条条款名：`tail -n +3 coverage-baseline.txt | grep -c "078-coaching-skills"` → `0`（rc=1，无命中）。
- 规模：497 行 = 2 行头部 + 495 个冻结名。

### 两车道读数

```text
$ python3 scripts/python/account-clause-coverage.py .specify/specs/078-coaching-skills
...
claimed clauses (this feature): 38
baseline: .specify/specs/078-coaching-skills/coverage-baseline.txt (495 names)
FR universe: 29
FR claimed: 0
FR uncovered: 29
...
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered] fail (29) — 0 of 29 FRs cited from citation groups
...
29 error(s), 0 warning(s)
status: uncovered
$ echo $?
1
```

- **Clause 车道**：`claimed clauses (this feature): 38`；`UNCOVERED` 名单中属于 `078-coaching-skills/contracts/` 的条数为 **0**（`grep -c` rc=1）。495 名全部是基线内既有未覆盖项，`0 beyond the frozen baseline`。
- **FR 车道**：`FR claimed: 0` / `FR uncovered: 29`，退出码 1。成因按 `tasks.md` § Measured Premises 与 `plan.md` § FR-Lane Exemption（M-07 显式豁免）：五份契约正文不带 citation group，FR→条款映射的 owner 是 `plan.md` § Phase 1，本阶段不改写 plan 属主制品。该车道按构造报零覆盖，不是映射缺失；本读数如实记录，交 `/speckit.analyze` / GATE-4 作制品缺口处理。
