# Pre-Change Measurements — 056-probe-handler-system

> T002 冻结（2026-10-13，implement 启动时全部重跑，非引用 tasks.md 旧值）。后续所有"零新增失败 / 无 NEW drift / 预算不变"对比以本文件为唯一改前锚。

## PM-1 编译单元面与 SC-007 行基线

```text
$ grep -l '^## Feedback' templates/commands/*.md | wc -l
23
$ grep -l '^## Feedback' skills/internal/*/SKILL.md | wc -l
35
$ grep -l '^## Feedback' skills/external/*/SKILL.md | wc -l
11
$ awk 'FNR==1{u++} /^## /{sec=($0~/^## (Feedback|Documentation)( |$)/)} sec&&NF{n++} END{printf "units=%d non-blank_lines=%d\n",u,n}' templates/commands/*.md
units=26 non-blank_lines=90
$ awk '…同规则…' skills/internal/*/SKILL.md
units=35 non-blank_lines=575
$ awk '…同规则…' skills/external/*/SKILL.md
units=11 non-blank_lines=188
```

- 编译单元集 = **69**（23 + 35 + 11）；SC-007 非空行基线 = **853**（90 + 575 + 188）。
- 陷阱注记：命令面 awk 扫 26 个文件（3 个无 `## Feedback` 贡献 0 行）；单元计数以 69 口径为准。

## PM-2 feedback-utils.py 动作封闭集（迁移前 14）

```text
$ grep -n 'choices=' scripts/python/feedback-utils.py | head -1
1936:        choices=["record", "status", "list", "dispose", "mark-submitted", "reindex",
```

（续行含 `"package", "cleanup", "upstream", "probes", "map", "migrate-legacy", "probe-inject", "introspect-register"`，共 14。迁移后：probe-utils.py 承载 probes/map/probe-inject + handlers/compile-embeds；feedback 收缩为 11。）

## PM-3 门控预算

```text
$ python3 scripts/python/scan-confirmation-gates.py
blocking confirmation gates: 23
  destructive: 16
  governance_kept: 7
violations (reversible gates still blocking): 0
```

## PM-4 probe 注册表

```text
$ python3 scripts/python/feedback-utils.py --action probes --validate
Probe registry valid: 6 classes, 72 internal + 0 external objects
```

## PM-5 镜像对

```text
$ python3 scripts/python/sync-mirrors.py --check
ok    skills/internal/ == .specify/skills/internal/ (133 files)
ok    agents/ == .specify/agents/templates/ (2 files)
ok    scripts/ == .specify/scripts/ (106 files)
ok    shared/ == .specify/shared/ (46 files)
（templates 与 skills/external 对同为 ok，EXIT=0）
```

## 改前 failing-test 基线（templates/commands/implement.md § Test runs 口径）

- 命令：`scripts/bash/run-tests.sh --names-out .specify/specs/056-probe-handler-system/baseline-failed.txt`
- 实测（2026-10-13 UTC，108.07s）：**3598 passed, 0 failed**（3 warnings：PytestUnknownMarkWarning ×3，既有状况非本特性引入）
- 基线文件：`.specify/specs/056-probe-handler-system/baseline-failed.txt`（**0 条**）
- 判据形态：基线为空集 ⇒ 后续任何失败均为新增失败（绝对判据）；相界回归对比 `comm -13 baseline current` 必须为空。

## per-unit 差异矩阵（T019 前占位）

> T019 从 69 单元实测推导后追加于本节之后。
