# Pre-Change Measurements — Feature 100（Setup · T001）

> 冻结**改前基线**：本文件只贴捕获时刻的真实输出、退出码与捕获日期，供后续「零新增」判据作对照物。
> 捕获日期：2026-11-11（11:53 +08:00 前后逐项执行）；工作树：`.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive`，分支 `100-seal-slice-archive`。
> 本行不写任何源文件；本文件自身是 T001 的唯一写面。

## 1 冻结读数总表

| 项 | 读数 | 退出码 |
|----|------|--------|
| `sync-mirrors.py --check` | 唯一 `DIFF` = `.specify/templates/gitignore-specify-template`（既有、非本特性写面） | 2（`DRIFT detected`） |
| `regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.` | 0 |
| `ls templates/commands/*.md \| wc -l` | 31 | 0 |
| `git rev-parse HEAD` | `f821daf8362a3050cb14909a820294f70f04d8a9` | 0 |
| `git status --short` | 空（干净，捕获时刻） | 0 |
| seal 测试文件清单 | 9 个文件（见 § 6） | 0 |
| seal 相关套件名字级基线 | `3 failed, 124 passed in 8.27s`；失败名单见 § 7 | 1（pytest 自身：有失败） |

## 2 `python3 scripts/python/sync-mirrors.py --check`

**退出码**：2。

**完整 stdout/stderr（verbatim）**：

```text
OK: all per-tool command copies match the source templates.
DIFF .specify/templates/gitignore-specify-template
ok    skills/external/ == .specify/skills/ (429 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (136 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (18 files, byte-identical)
ok    scripts/ == .specify/scripts/ (129 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (113 files, byte-identical)
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
```

**`DIFF` 集逐行（本特性 GATE-2 的对照基准）**：

```text
DIFF .specify/templates/gitignore-specify-template
```

## 3 `python3 scripts/python/regen-command-copies.py --check`

**退出码**：0。

**完整 stdout（verbatim）**：

```text
OK: all per-tool command copies match the source templates.
```

## 4 命令面基线

```bash
ls templates/commands/*.md | wc -l
```

实测输出：

```text
31
```

## 5 版本与工作树

```bash
git rev-parse HEAD
git status --short
```

实测输出：

```text
f821daf8362a3050cb14909a820294f70f04d8a9
```
（`git status --short` 无输出——空，干净；捕获时刻在本次 Setup 落盘之前。）

## 6 seal 测试文件清单（名字级套件面）

```bash
ls tests/contract/test_seal_*.py tests/integration/test_seal_*.py
```

实测输出：

```text
tests/contract/test_seal_archive_gate.py
tests/contract/test_seal_boundaries.py
tests/contract/test_seal_concurrency_and_readonly.py
tests/contract/test_seal_engine_contract.py
tests/contract/test_seal_merge_apply.py
tests/contract/test_seal_merge_plan.py
tests/contract/test_seal_seal.py
tests/integration/test_seal_074_round.py
tests/integration/test_seal_merge_determinism.py
```

## 7 seal 相关套件名字级基线（改前）

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_seal_*.py tests/integration/test_seal_*.py --names-out .specify/.tmp/100-seal-baseline-failed.txt -q
```

**退出码**：1。**汇总行**：`3 failed, 124 passed in 8.27s`。

完整转录：`.specify/.tmp/100-seal-baseline-run.txt`；失败名单：`.specify/.tmp/100-seal-baseline-failed.txt`（均在被 gitignore 覆盖的沉淀临时根下）。

**失败名单（verbatim，3 条）**：

```text
tests/contract/test_seal_boundaries.py::test_the_audit_report_is_complete_and_optionally_recorded
tests/contract/test_seal_boundaries.py::test_the_directory_registry_difference_is_fully_classified
tests/integration/test_seal_074_round.py::test_live_plan_identifies_both_slices_from_the_split_record
```

**逐条失败要点（摘自完整转录）**：

1. `test_the_directory_registry_difference_is_fully_classified` — `C-036`：live spec 目录 `['067', '075', '080', '097', '098', '100']` 对钉住名单 `['067', '075', '080']`，多出 `097`/`098`/`100`（本 spec 目录 100 亦在其中）。
2. `test_live_plan_identifies_both_slices_from_the_split_record` — `order_basis` 实测 `{'letter-order'}`，期望 `{'split-record'}`（`C-012`）。
3. `test_the_audit_report_is_complete_and_optionally_recorded` — `KeyError: '097'`。

> 本节的用途是 T001 的 Setup 对照物——「seal 相关套件」的名字级改前基线；GATE-1 的全量套件基线归 `/speckit.implement` step 6 的 `**Test runs**` 所有（tasks.md § Completion Gate GATE-1），本节不另立第二基线。
