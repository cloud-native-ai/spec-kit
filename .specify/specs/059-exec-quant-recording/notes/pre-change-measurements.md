# Pre-Change Measurements(Feature 059 implement 期,T001)

采集日:2026-10-16(implement 开工时实测,never-cache 重探)。每条附真实命令输出;计数规则与 `tests/contract/test_wrap_up_line_budget.py` 一致(per-file H2 `Feedback`/`Documentation`/`Wrap-up` 非空行;naive whole-grep 是已文档化的陷阱形态,不采用)。

## PM-1 wrap-up 编译面非空行总数

命令:上文计数规则的内联 Python 复算(与测试同规则),输出:

```text
per-group files: {'templates/commands': 26, 'skills/internal': 37, 'skills/external': 12}
per-group non-empty face lines: {'templates/commands': 137, 'skills/internal': 222, 'skills/external': 72}
TOTAL non-empty face lines: 431 (budget 853)
```

**总计 431 = 137 + 222 + 72,预算 853,余量 422。**

## PM-2 编译面数量

命令:按 `AUTO-GENERATED` 标记统计含编译面的文件数,输出:

```text
face files (autogen) vs total files: {'templates/commands': (23, 26), 'skills/internal': (37, 37), 'skills/external': (12, 12)}
compiled-face total: 72
```

**72 面 = 23 命令模板 + 49 技能**(templates/commands 中 3 个文件无编译面)。

## PM-3 sync-mirrors --check

命令:`python3 scripts/python/sync-mirrors.py --check` → **exit 0**,输出尾部:

```text
ok    scripts/ == .specify/scripts/ (107 files)
ok    shared/ == .specify/shared/ (48 files)
```

## PM-4 regen-command-copies --check

命令:`python3 scripts/python/regen-command-copies.py --check` → **exit 0**,输出尾部:

```text
OK: all per-tool command copies match the source templates.
```

## PM-5 行预算测试基线

命令:`python3 -m pytest tests/contract/test_wrap_up_line_budget.py -q` → **1 passed**(431 ≤ 853)。

## T002 基线冻结(同日配套)

`bash scripts/bash/run-tests.sh --names-out .specify/specs/059-exec-quant-recording/baseline-failed.txt tests/contract tests/integration -q`(canonical runner,`--names-out` 形态由 implement-feature SKILL § Test runs 钉定);失败名单与退出码以 `baseline-failed.txt` 及当轮运行日志为准,本文件不转抄。
