# 改前实测 — Feature 099（implement 入口，T001 / T002）

> **采集点**：implement 阶段任何框架源写入之前（工作树起始状态，`HEAD` = `5840ac0f0`，branch `099-speckit-seal`）。
> **基线形态 owner**：`/speckit.implement` step 6 `**Test runs**`（`.specify/skills/internal/implement-feature/SKILL.md`）；本文件只引用该形态，不定义第二形态。
> 全部数值为 2026-11-10 本工作树实测（never-cache 重探），逐字附命令与输出；不是 tasks.md 旧值的转抄。

## 环境重探（implement 入口）

```text
python3 --version            -> Python 3.11.11
python3 -c "import pytest; print(pytest.__version__)" -> 8.4.2（pytest-xdist 可导入）
git --version                -> git version 2.43.5
LANG=en_US.UTF-8（runner 的 sort 排序 locale，见 PM-3）
```

外部服务 / 网络 / 容器运行时：本包两条实测均不依赖。

## PM-1 `sync-mirrors.py --check`（T001）

**命令（verbatim）**：

```bash
python3 scripts/python/sync-mirrors.py --check
```

**退出码**：0 —— **完整 stdout（verbatim）**：

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (23 files, byte-identical)
ok    skills/external/ == .specify/skills/ (428 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (135 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (17 files, byte-identical)
ok    scripts/ == .specify/scripts/ (126 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (111 files, byte-identical)
```

**读数**：`shared/` 对 111 files byte-identical，与 tasks.md T001 冻结值复测一致；与 plan 阶段基线一致（`test-evidence/plan-stage-checks.txt:52-54`，exit=0 / 111 files）。零预存漂移，作为 GATE-2 的比较锚。

## PM-2 `regen-command-copies.py --check`（T001）

**命令（verbatim）**：

```bash
python3 scripts/python/regen-command-copies.py --check
```

**退出码**：0 —— **完整 stdout（verbatim）**：

```text
OK: all per-tool command copies match the source templates.
```

**读数**：零预存漂移，作为 GATE-2 的比较锚。

## PM-3 全量失败名基线（T001，implement 入口捕获）

**命令（verbatim，经唯一 runner；`--names-out` 形态由 step 6 owner 钉定）**：

```bash
bash scripts/bash/run-tests.sh --names-out .specify/specs/099-speckit-seal/baseline-failed.txt
```

**运行区间**：`start_utc=2026-11-10T15:07:43Z` → `end_utc=2026-11-10T15:08:59Z`（76 s），`suite_exit_code=1`。

**runner 模式行（verbatim）**：

```text
# test runner exceptions: 1 declared serial test(s)
# test runner: python3 -m pytest -n auto --dist load 
# test runner: mode=parallel workers=auto dist=load passes=2
```

**两 pass 汇总（verbatim）**：

```text
========== 280 failed, 8260 passed, 2 skipped, 576 warnings in 43.16s ==========   （并行 pass）
=============== 1 passed, 8542 deselected, 3 warnings in 17.80s ================   （串行例外 pass）
# failed-name list written: .specify/specs/099-speckit-seal/baseline-failed.txt (280 entries) passes=2
```

**基线文件读数**：

- 路径：`.specify/specs/099-speckit-seal/baseline-failed.txt`（**280** 条 FAILED node id，去重排序）
- sha256：`f749b805e521d2641e77b9c2756d890951ff44c1ce1897336dc3438645352c42`
- 排序口径：runner 内 `sort -u` 按 `en_US.UTF-8` collation；已实测 `LC_ALL=en_US.UTF-8 sort -u` 复验与文件一致（`LC_ALL=C` 的排序顺序不同）——T045/GATE-1 的 `comm -13` 比较两侧必须取自同一 runner 形态（同 locale），或两侧同法以 `LC_ALL=C` 重排后比较
- 完整单次输出：`test-evidence/baseline-full-suite-20261110T150720Z.txt`（9568 行，含头尾 `start_utc` / `end_utc` / `suite_exit_code` 三行；仓库 `*.log` 全局忽略，按既有证据 `.txt` 惯例落盘）
- 失败分布头部：`test_trigger_engine.py` 27、`test_trigger_promotion.py` 18、`test_fast_fail_discipline.py` 14、`test_trigger_tuning.py` 13、`test_summary_legacy_backfill.py` / `test_summary_accumulation.py` / `test_goal_aggregation.py` 各 10

**读数**：280 条为本特性开工时的**既有**失败集合。GATE-1 的判据是相对本名单的**新增**失败集为空（`comm -13 baseline current`），不是对 280 这个绝对值的清零承诺。

**测试运行副作用（已处置）**：全量运行会按设计重写 Feature 081 的 smoke 证据（`tests/integration/test_acceptance_smoke.py` 的既有行为），本次运行改写了 `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt`；该文件非本包产物，已恢复为 `HEAD` 版本，不随本包提交。

## PM-4 条款覆盖基线冻结（T002）

**命令（verbatim，`--freeze` 只打印不写盘；重定向即落盘）**：

```bash
python3 scripts/python/account-clause-coverage.py .specify/specs/099-speckit-seal --freeze > .specify/specs/099-speckit-seal/coverage-baseline.txt
```

**退出码**：0 —— stderr 为空。

**基线文件读数**：

- 路径：`.specify/specs/099-speckit-seal/coverage-baseline.txt`
- 行数：**642** = 2 行 header + **640** 条已冻结 UNCOVERED 名称（codepoint 序）
- sha256：`26da52464b5558c568be9c0a203648f6cc7d2a8ee242d9627033eab8bdb840f0`
- header 关键字段（verbatim）：`frozen-from: .specify/specs/*/contracts/* excluding 099-speckit-seal`；`files: 286 (parsed 179 + named 107)`；`base-sha: 5840ac0f0f61`

**读数**：本 spec 的契约集 C-001…C-045 覆盖核算以该冻结文件为 delta 参照（FR-025、SC-008），是真实冻结名单而非空基线；T050 做终局对照（`comm -13`，`LC_ALL=C`，见该文件 header 的排序警示）。

## 证据落点汇总

| 落点 | 内容 |
|------|------|
| `notes/pre-change-measurements.md` | 本文件 —— T001/T002 改前读数汇总 |
| `baseline-failed.txt` | GATE-1 失败名基线（路径形态由 step 6 owner 拥有） |
| `coverage-baseline.txt` | T002 冻结的条款覆盖基线 |
| `test-evidence/baseline-full-suite-20261110T150720Z.txt` | 全量单次运行的完整 stdout/stderr 与退出码 |
