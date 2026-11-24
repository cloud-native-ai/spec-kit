# Quickstart run — 103-team-view (T037)

Captured: 2026-11-24, package 4, after the error-path implementation (T034) and the mirror
re-sync (T036). Every command below was executed through the program surface
`python3 scripts/python/team-view.py` on the live repository (S-0…S-3, S-5) or on a disposable
fixture tree under `.specify/.tmp/quickstart-103/` (S-3 empty leg, S-4). No scenario writes
`.specify/teams/`; `git status --short .specify/teams/` was empty after the whole run.

## S-0 — Executed engine reads (the facts a single view composes)

Premises: `scripts/python/goal-utils.py` is `0.0.22`; `.specify/teams/086-efficient-test-execution/team.md`
exists with `anchor_slug: 086-efficient-test-execution`. Re-measured, not inherited.

### binding

Command:

```bash
python3 scripts/python/goal-utils.py binding team 086-efficient-test-execution --json
```

Output:

```text
{
  "kind": "teams",
  "slug": "086-efficient-test-execution",
  "owner": "human",
  "owner_id": "human",
  "origin": "086-efficient-test-execution",
  "path": ".specify/teams/086-efficient-test-execution/team.md",
  "archive_layer": "teams",
  "lifecycle": "active"
}
--- rc=0 ---
```

### list (projected to the one team)

Command:

```bash
python3 scripts/python/goal-utils.py list --json | python3 -c "import json,sys; print([g for g in json.load(sys.stdin)['goals'] if g['slug']=='086-efficient-test-execution'])"
```

Output:

```text
[{'slug': '086-efficient-test-execution', 'status': 'active', 'criteria_count': 5, 'updated': '2026-11-06'}]
--- rc=0 ---
```

### targets --list

Command:

```bash
python3 scripts/python/goal-utils.py targets 086-efficient-test-execution --list --json
```

Output:

```text
{
  "targets": []
}
--- rc=0 ---
```

## S-1 — One team, six groups

Premise: `.specify/teams/cws-workspace-cluster/team.md` exists (measured 2026-11-24) and declares
`pattern: continuous`; the sibling `goal-utils.py` resolves. The shape (six headings in order,
member/report coverage) is pinned by
`tests/integration/test_team_view_program.py::test_single_team_renders_six_groups`.

Command:

```bash
python3 scripts/python/team-view.py cws-workspace-cluster
```

Output (complete):

```text
Team View: cws_work Workspace 参考项目洞察收割（cws-workspace-cluster）
mode: single · as-of: 2026-11-20T10:27:20Z（文件时间；非实时探测）

## 1. 身份与绑定（Identity & Binding）
- slug: cws-workspace-cluster
- name: cws_work Workspace 参考项目洞察收割
- description: 以 /cws_work/work.code-workspace 为集群定义源，持续分析 10 个参考开源项目，为 /cws_work/spec-kit 提炼可采纳的改进点
- lifecycle: 未声明 → active
- 绑定（binding）: owner=human · owner_id=human · origin=未记录
- 锚点身份（anchor_identity）: inferred — cws-workspace-cluster
- handoff_ref: 未记录
- 其它声明键: goal（不可读）

## 2. 静态结构（Static Structure）
- type 来源（type_source）: 正文矩阵（body-matrix）
- 正文矩阵: 3 行
  | role | stage | type | lifecycle | responsibility |
  |---|---|---|---|---|
  | team-supervisor | optimizer | Meta | persistent | 花名册解析（folders − spec-kit）、并行派发只读分析 subAgent、证据抽查、汇总洞察报告 |
  | repo-analyst × 10 | executor | Worker | temporary | 每参考仓一个实例：定位/架构/独到机制/可迁移点，结构化档案+证据路径 |
  | insight-synthesizer | evaluator | Worker | temporary | 对照 spec-kit 现状蒸馏可采纳改进点，按价值/成本分级，剔除已具备或不适配项 |
- 成员（frontmatter）: 12 名
  - agent=agent-team-supervisor-template · role=team-supervisor · stage=optimizer · type=Meta · lifecycle=persistent · responsibility=解析 workspace folders（减去 home_project）生成分析花名册并 diff 上轮；派发 per-repo 只读分析 subAgent（注入统一输出 schema）；对"独到机制"类结论按证据路径抽查复核；汇总为洞察报告；一切对 spec-kit 的采纳动作只提建议、不执行
  - agent=agent-stage-evaluator-template · role=insight-synthesizer · stage=evaluator · type=Worker · lifecycle=temporary · responsibility=通读各仓分析档案，对照 spec-kit 现状（constitution/features/skills/commands）做能力差距判定，蒸馏可采纳改进点并按价值/成本分级；剔除 spec-kit 已具备或不适配的点
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/OpenSpec · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/superpowers · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/claw-code-agent · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/intellegix-code-agent-toolkit · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/claude-code-ts · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/claude-code-py · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/learn-claude-code · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/loop-engineering · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/ai-website-cloner-template · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent=agent-stage-executor-template · role=repo-analyst · stage=executor · type=Worker · lifecycle=temporary · territory=/cws_work/better-harness · responsibility=只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
- seats: 未声明（默认值见 create-mode.md § Schema notes）
- stage_seats: 未声明（默认值见 create-mode.md § Schema notes）
- 名册差异（roster_delta）: 未记录（正文矩阵无 agent 列，两侧名册不可比对）

## 3. 动态结构（Dynamic Structure）
- pattern: continuous
- config:
  - config.maturity: L1
  - config.cadence: 7d
  - config.verifier: independent
  - config.workspace_file: /cws_work/work.code-workspace
  - config.roster_source: workspace_folders
  - config.home_project: /cws_work/spec-kit
  - config.roster_rule: folders - home_project
  - config.roster_diff_on_start: true
  - config.write_policy: read-only
  - config.quality_dimensions: [{name: coverage, weight: 0.2}, {name: insight-specificity, weight: 0.3}, {name: evidence-quality, weight: 0.25}, {name: adoption-actionability, weight: 0.25}]
  - config.threshold: 0.8
  - config.budget.max_cycles_per_day: 2
  - config.budget.max_subagents_per_cycle: 11
  - config.budget.on_80pct: report-only
  - config.budget.on_100pct: halt
  - config.kill_switch: loop-pause-all
  - config.constraints_file: .specify/teams/cws-workspace-cluster/constraints.md
  - config.state_spine: .specify/teams/cws-workspace-cluster/STATE.md
  - config.run_log: .specify/teams/cws-workspace-cluster/run-log.jsonl
- 可选键声明（optional keys）:
  - lifecycle_state: 未声明（默认值见 create-mode.md § Schema notes）
  - anchor_slug: 未声明（默认值见 create-mode.md § Schema notes）
  - focus_target: 未声明（默认值见 create-mode.md § Schema notes）
  - territory: 未声明（默认值见 create-mode.md § Schema notes）
  - preset: 已声明 (project-cluster)
  - seats: 未声明（默认值见 create-mode.md § Schema notes）
  - stage_seats: 未声明（默认值见 create-mode.md § Schema notes）
  - config.summary: 未声明（默认值见 create-mode.md § Schema notes）
  - config.reporting-reason: 未声明（默认值见 create-mode.md § Schema notes）
- focus_target: 未声明

## 4. 持久化清单（Persistence Inventory）
- 团队目录（team_dir）: /storage/project/cloud-native-ai/spec-kit/.specify/teams/cws-workspace-cluster
- 运行报告: 已列出（共 2 份，显示最新 2 份，省略 0）
  - 20260730T094500Z-report.md
  - 20260730T082021Z-report.md
- 台账: 缺失（/storage/project/cloud-native-ai/spec-kit/.specify/teams/cws-workspace-cluster/items.jsonl）
- 脊柱文件（存在）: constraints.md, STATE.md, run-log.jsonl
- summary 送达目录: 未声明（默认值见 create-mode.md § Schema notes）

## 5. 最近运行状态（Recent Run State）
- 最近报告（latest_report）: 20260730T094500Z-report.md
- Outcome: 未记录
- Target 指派: 未记录
- Result Summary: 未记录
- Verification: 未记录
- Nested SDD Runs: 未记录
- 台账信号: 缺失

## 6. 其他归档层引用（Archive References）
- handoff_ref: 未声明
- 锚点（anchor）: cws-workspace-cluster（inferred）
  - 生命周期: 悬空（dangling）
  - 原因: engine list 未返回该 anchor slug
  - Targets: 未记录
- 内容入口: /speckit.anchor view
--- rc=0 ---
```

Reading: all six headings appear in order; every frontmatter member row and every
`runs/*-report.md` filename of the live team is covered; the `as-of:` line is present; exit 0.

## S-2 — No slug: overview

Premise: the live archive holds 20 team directories (measured 2026-11-24). The shape — one row
per team, slug ascending, seven columns — is pinned by
`tests/integration/test_team_view_program.py::test_overview_lists_every_team_sorted`; the
corrupt-row leg of that test runs on a fixture, since the live archive has no corrupt team.

Command:

```bash
python3 scripts/python/team-view.py
```

Output (complete):

```text
Team Overview: 20 teams · as-of: 2026-11-20T10:27:20Z（文件时间；非实时探测）

| slug | name | pattern | lifecycle | 绑定锚点（anchor） | updated | 最近运行（latest run） |
|---|---|---|---|---|---|---|
| 085-sdd-temporary-goal-team | SDD Team 085 (scope spec) | serial | archived | inferred — 085-sdd-temporary-goal-team | 2026-11-06 | 未记录 |
| 086-efficient-test-execution | SDD Temporary Team 086 | serial | active | declared — 086-efficient-test-execution | 2026-11-06 | 未记录 |
| 087-arch-diagram-docs | SDD Temporary Team 087 | serial | archived | declared — 087-arch-diagram-docs | 2026-11-06 | 未记录 |
| 088-reporting-dogfood | 088 Reporting Dogfood | parallel | archived | inferred — 088-reporting-dogfood | 2026-11-06 | 未记录 |
| 089-script-interface-contract | SDD Temporary Team 089 | serial | active | declared — script-interface-contract | 2026-11-06 | 未记录 |
| 090-re-anchoring | SDD Temporary Team 090 | serial | active | declared — 090-re-anchoring | 2026-11-09 | 未记录 |
| 091-auto-git-closeout | SDD Temporary Team 091 | serial | archived | inferred — 091-auto-git-closeout | 2026-11-09 | 未记录 |
| 094-goal-team-parallel | SDD Temporary Team 094 | parallel | active | declared — 094-goal-team-parallel | 2026-11-09 | 未记录 |
| command-logic-as-classified-skills | 命令逻辑技能化与分类标注团队 | serial | active（未声明） | declared — command-logic-as-classified-skills | 2026-10-09 | 20261012T115331Z |
| cws-workspace-cluster | cws_work Workspace 参考项目洞察收割 | continuous | active（未声明） | inferred — cws-workspace-cluster | 2026-08-20 | 20260730T094500Z |
| demo-seat-dispatch | 未记录 | serial | archived | inferred — demo-seat-dispatch | 2026-10-08 | 20261008T214100Z |
| draw-diagram-interactive | 绘图技能交互图表能力建设团队 | iteration | archived | inferred — draw-diagram-interactive | 2026-10-14 | 未记录 |
| draw-plantuml-optimizer | Draw-PlantUML 复杂大图优化团队 | iteration | active（未声明） | inferred — draw-plantuml-optimizer | 2026-08-20 | 20260716T104232Z |
| draw-two-layer-structure | 绘图双层结构重构团队 | serial | active（未声明） | declared — draw-two-layer-structure | 2026-09-16 | 未记录 |
| post-refactor-mechanism-integrity | 重构后机制完整性团队 | serial | archived | inferred — post-refactor-mechanism-integrity | 2026-10-11 | 20261011T144202Z |
| requirement-implement-monitor | 需求实现过程监控 | continuous | active（未声明） | inferred — requirement-implement-monitor | 2026-08-20 | 20260730T022200Z |
| session-driven-self-improvement | 自我提升流程建立团队 | serial | active（未声明） | declared — session-driven-self-improvement | 2026-10-08 | 20261008T090000Z |
| skill-layer-install-separation | 技能分层与安装分流团队 | serial | active（未声明） | declared — skill-layer-install-separation | 2026-10-09 | 20261011T021003Z |
| summarize-project-optimizer | Summarize-Project 技能迭代优化团队 | iteration | active（未声明） | inferred — summarize-project-optimizer | 2026-08-20 | 20260730T180020Z |
| viz-skill-arena | 可视化技能竞技场团队 | continuous | active（未声明） | declared — visualization-skill-selection | 2026-09-15 | 未记录 |
--- rc=0 ---
```

## S-3 — Unknown slug

Premise: the live archive is non-empty; `no-such-team` has no directory and no near-miss sibling.
The shape is pinned by `::test_unknown_slug_reports_not_found`.

Command:

```bash
python3 scripts/python/team-view.py no-such-team
```

Output:

```text
team not found: no-such-team
可用 slug（available slugs；共 20，显示 20）:
  - 085-sdd-temporary-goal-team
  - 086-efficient-test-execution
  - 087-arch-diagram-docs
  - 088-reporting-dogfood
  - 089-script-interface-contract
  - 090-re-anchoring
  - 091-auto-git-closeout
  - 094-goal-team-parallel
  - command-logic-as-classified-skills
  - cws-workspace-cluster
  - demo-seat-dispatch
  - draw-diagram-interactive
  - draw-plantuml-optimizer
  - draw-two-layer-structure
  - post-refactor-mechanism-integrity
  - requirement-implement-monitor
  - session-driven-self-improvement
  - skill-layer-install-separation
  - summarize-project-optimizer
  - viz-skill-arena
建议（next step）: /speckit.team create no-such-team
--- rc=3 ---
```

Second leg — empty archive (disposable fixture root `.specify/.tmp/quickstart-103/empty`, no
`.specify/teams/` inside):

```bash
python3 scripts/python/team-view.py no-such-team --repo-root .specify/.tmp/quickstart-103/empty
```

Output:

```text
team not found: no-such-team
No teams found
建议（next step）: /speckit.team create no-such-team
--- rc=3 ---
```

## S-4 — Corrupt definition

Premise: fixture root `.specify/.tmp/quickstart-103/corrupt` holds two teams —
`broken-team/` without `team.md`, and `unparsable-team/team.md` with frontmatter outside the
closed subset. The shape is pinned by `::test_corrupt_definition_is_not_not_found`.

Variant A (directory present, `team.md` missing):

```bash
python3 scripts/python/team-view.py broken-team --repo-root .specify/.tmp/quickstart-103/corrupt
```

Output:

```text
定义损坏: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/quickstart-103/corrupt/.specify/teams/broken-team/team.md
--- rc=4 ---
```

Variant B (frontmatter unparseable):

```bash
python3 scripts/python/team-view.py unparsable-team --repo-root .specify/.tmp/quickstart-103/corrupt
```

Output:

```text
定义损坏: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/quickstart-103/corrupt/.specify/teams/unparsable-team/team.md
--- rc=4 ---
```

Both name the exact `team.md` path, never `team not found`, and never render a six-group body.

## S-5 — `--target` is a mode conflict (program surface)

Premise: `--target` is not declared by `team-view.py`. The command-level conflict statement is
pinned by `tests/contract/test_team_view_command.py::test_view_target_conflict_declared`; the
program-level rejection by `tests/contract/test_team_view_program_contract.py::test_undeclared_target_option_rejected`.

Command:

```bash
python3 scripts/python/team-view.py some-team --target T-001
```

Output:

```text

--- stderr ---
error: unrecognized option: --target
--- rc=2 ---
```

## S-6 — Read-only proof

No separate command is run here: the executable surface is
`tests/integration/test_team_view_program.py::test_view_leaves_tree_byte_identical`, executed
through the unique entry `scripts/bash/run-tests.sh` in the targeted suite (T038) and quoted in
`test-evidence/polish-targeted-suite.txt`. Re-running it here would duplicate that reading, so
it is referenced, not re-captured.

## Cleanup

The disposable fixture root `.specify/.tmp/quickstart-103/` (fixtures plus this document's
capture files) was removed after the transcript above was assembled; nothing under
`.specify/teams/` was created or modified.
