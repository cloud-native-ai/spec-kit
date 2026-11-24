# 路由裁定记录：用户面输出维护机制（直接修改覆盖）

**日期**: 2026-11-24
**单元**: superagent 用户面输出维护机制（回显命令边界包封 + 工具结果重发）
**载体说明**: 本记录是本次直接修改的执行证据；路由裁决记录按 `shared/definitions/sdd-routing-definitions.md` § User override 落在 Agent 执行证据里。

## 1. 引擎裁决（覆盖前）

命令（只读）：

```console
$ python3 scripts/python/sdd-route.py --action route --nature feature --traceability required \
    --blast-radius cross-cutting --reversibility reversible --complexity complex --format json
```

载荷（逐字）：

```json
{
  "action": "route",
  "owner_document": "/storage/project/cloud-native-ai/spec-kit/shared/definitions/sdd-routing-definitions.md",
  "verdict": "sdd",
  "reason_code": "sdd-capability-or-contract-change",
  "triggered_conditions": [
    "nature-feature",
    "traceability-required",
    "blast-cross-cutting",
    "complexity-high",
    "reversal-reversible",
    "bounded-correction-recorded"
  ],
  "inputs": {
    "change_nature": "feature",
    "traceability": "required",
    "blast_radius": "cross-cutting",
    "reversibility": "reversible",
    "complexity": "complex"
  },
  "effective_blast_radius": "cross-cutting",
  "bounded_correction_rationale": null,
  "absent_inputs": [],
  "ambiguous_inputs": [],
  "actor": null,
  "recorded_at": null,
  "override": null
}
```

## 2. 用户覆盖（逐字）

用户原始请求：

> 当前superagent+subagent结构会让 /speckit.status 等命令的输出出现问题, 需要针对这种直接在superagent中执行的回显命令进行特殊处理, 存在的问题主要是:1) 大量subagent的打印导致命令回显被冲掉; 2) 命令输出的格式需要进行整理以适配输出的格式, 最好在启动superagent+subagent中有个独立的维护面向用户的输出的机制.

用户补充的真实案例（摘要，完整案例见会话）：

> 一个真实的team view命令执行案例如下, 需要根据用户实际看到的输出进行修复: /speckit.team view log-metrics-collection-system ...
> （宿主把 team-view.py 的 157 行输出折叠为 “+157 lines (Ctrl+O to expand)”；助手以“team-view.py 输出已逐字呈现（上方）”代替正文，最终只发缺陷摘要；EXIT=5）

用户在流程选择中的覆盖回答（逐字）：

> 这次改动走哪条流程落地？ → **直接修改**

覆盖记录：

| 字段 | 值 |
|---|---|
| 被覆盖的裁决 | `sdd` |
| 理由码 | `sdd-capability-or-contract-change` |
| 覆盖值 | `direct`（用户显式指示「直接修改」） |
| 覆盖单元 | user: Qiming Liu (John) |
| 记录时间 | 2026-11-24T09:31Z（UTC） |
| 引擎输出保留 | 上方 JSON 原样保留，未抹除 |

## 3. 本次直接修改的边界

- 不建立 SDD 工件链、不经过驱动阶段与 handoff。
- 仍受全部适用质量门与确认门约束；证据见 §4 与收尾的测试读数。
- 变更集与验证项以已批准计划 `/home/agent/.qoder/plans/slim-plateau-frog.md` 为准。

## 4. 拟定变更集（执行前登记，执行后由 `git diff --stat` 对账）

新增：

- `shared/guidelines/user-facing-output.md`（owner：通道/回显类/边界/包封/re-emission/范围限制）
- `tests/contract/test_user_facing_output.py`
- 本记录

编辑（框架源）：

- `templates/instructions-template.md`（新 H2 `## User-Facing Output`）
- `templates/commands/status.md`、`measure.md`、`team.md`、`goal.md`、`anchor.md`、`tools.md`、`todo.md`（回显声明 + 包封/re-emission 指针）
- `skills/internal/run-agent/SKILL.md`、`run-team/SKILL.md`、`view-team/SKILL.md`（startup 声明 / no-arg 标记 / re-emission）
- `shared/definitions/superagent-definitions.md`（一句指针）
- `tests/contract/test_agents_run_scope_contract.py` + `.specify/specs/104-agents-run/notes/pre-change-measurements.md`（范围绑定）
- `tests/contract/test_expression_compatibility.py`（冻结文件漂移 allowlist 记录）
- 生成物：`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` 对应副本；`shared/`、`skills/`、`templates/` 的 `.specify/` 镜像；`.specify/instructions.md`

不编辑：`templates/commands/agents.md`、`skills/external/sdd-loop-driver/SKILL.md`（069a 冻结且无/不新增放行）、三个确定性引擎（不新增格式）、可理解性纪律 11 类与 glossary。

## 5. 验证读数（2026-11-24）

**生成确定性**：

- `python3 scripts/python/probe-utils.py --action compile-embeds --check` → 86 units, zero drift。
- `python3 scripts/python/regen-command-copies.py --check` → all per-tool copies match。
- `python3 scripts/python/sync-mirrors.py --check` → shared/ 115 files byte-identical。
- `.specify/instructions.md` 38,872 B < `INSTRUCTIONS_BUDGET_BYTES=38912`（余量 40 B）。

**新契约测试**：`tests/contract/test_user_facing_output.py` 9 passed（owner 文档源+镜像、包封字面量唯一、回显标记集合、status/measure verbatim、dispatch 指针、re-emission、零新通道/存储/引擎）。

**定向组**（15 项 contract 文件）：1068 passed / 3 failed；3 个失败均在 HEAD worktree 上同样失败（既有红，非本次引入）：

- `test_user_facing_comprehension_doc.py::test_gn_c2_gate_scan_total_unchanged` —— 树实测总数 **31**，钉死值 27 已过时；HEAD 同为 31，本次新文档零新增命中。
- `test_user_facing_comprehension_section.py::test_c11_no_dangling_guideline_pointer_on_either_instruction_surface` —— `self-explanatory.md` 既有未挂指针。
- `test_qoder_command_frontmatter.py::test_every_template_has_short_description` —— `research.md` 既有 78 字符超长。

**全量相对绿**（`tests/contract tests/unit`，HEAD worktree vs 当前树）：两轮均 **160 failed / 9465+ passed**。逐名差分：

- 本轮修复的既有失败：`test_ask_record_repeat.py::test_canonical_engine_does_not_self_resolve_to_the_framework_repo`、`test_docs_command_template.py::test_c10_runtime_copies_exist_for_every_present_tool`（生成物补全）。
- 首次差分暴露的 2 项已修：`test_fast_fail_discipline.py::test_a7_section_counts...`（模板/活指令各 +1 章节，钉死值 38/39 同批更新）、`test_script_interface_contract.py::test_c20...`（未跟踪的新测试文件被界面检查器计为 `candidate-not-collected`；纳入索引后 exit 0）。
- 第二轮差分出现的 2 个名字（`test_isomorphism_map.py::test_no_second_map_or_boundary_table_exists`、`test_seal_boundaries.py::test_registries_and_ledgers_are_single_files`）**单独复跑均通过**，属并行全量的顺序/竞态噪声，与本次改动面无关；无持久新增失败。

**真实案例验收（本仓）**：

- `python3 scripts/python/team-view.py demo-seat-dispatch` → exit 0，六组完整（66 行）。
- `python3 scripts/python/team-view.py 103-team-view`（不存在）→ exit 3，`team not found` + 有界 slug 清单。
- 程序 stdout 现在由 view-team 技能强制作为**本会话消息**逐字重发（工具结果不计）；命令模板 `team.md` 携带回显声明与包封指针。宿主 UI 的最终人工验收需在带活跃子代理的会话中执行 `/speckit.team view <team>`；确定性部分已由上述测试钉住。
- 目标团队（`log-metrics-collection-system`）的报告命名为 `-<席id>-report.md`，不符合 create-team 的 `runs/<UTC-timestamp>-report.md` 契约，`unrecognized` 披露正确；修复在目标项目侧（改命名 / `/speckit.team modify`），本次不放宽识别器。

## 6. 真实案例的契约判断（不随覆盖改变）

- `team-view.py` 的 `REPORT_NAME_RE = ^(\d{8}T\d{6}Z)-report\.md$` 与 create-team 报告契约 `runs/<UTC-timestamp>-report.md` 一致；目标团队的 `-<席id>-report.md` 属非合规命名，`unrecognized` 披露是正确行为。修复在目标团队侧（改命名 / `/speckit.team modify`），不放宽识别器。
- 目标团队的 binding / 矩阵 / goal 缺口是目标数据问题；view 的披露正确，修复路径为目标项目 `/speckit.team modify`。
- 本次框架修复的是**呈现**：程序 stdout 必须作为执行体自己的消息在包封内逐字重发；工具结果（可能被宿主折叠）不算用户面输出。
