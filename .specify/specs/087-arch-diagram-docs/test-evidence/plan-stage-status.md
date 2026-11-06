# Plan Stage — Test Evidence (087-arch-diagram-docs)

**Recorded**: 2026-11-06（attempt 2 复跑；attempt 1 读数保留在 § 5 的差异表里） | **Stage**: plan | **Base**: `24cb4edc` | **Worktree**: `line/087-arch-diagram-docs`
**Interpreter**: `/tmp/087-toolenv/bin/python` → CPython 3.11.13, `pytest 9.2.0`（一次性 scratch venv，`--system-site-packages` + `typer rich httpx platformdirs readchar truststore pytest pyyaml`）。

**判据形态（本特性统一口径）**：本仓基线**不是全绿**，因此这里的每一条都是**相对基线无新失败 / 无新漂移**，而不是绝对退出码 0。基线值与实测值并列在每一条下面。

## 1. 本阶段产物的静态校验

| 检查 | 命令 | 读数 |
|------|------|------|
| 决策张力六字段与行文法 | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs` | `status: ok`；`scanned: 562 lines, 5 record(s)`；6 个标签全 `pass (0)`；`0 error(s), 0 warning(s)`；**exit 0** |
| 运行时行 / 前提 / 继承阻塞 / 悬空 ID / 计数 | `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/087-arch-diagram-docs --stage plan --repo .` | `decision=pass errors=0 advisories=38 waived=0`（`fr=23 sc=10 files=9`）；**exit 0**；38 条全为 `missing-path`，指向实施期才存在的路径（含 T-005 反题里的两个 `diagrams/` 目录） |
| 结构面（执行类） | `python3 .specify/scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/087-arch-diagram-docs` | `class=execution source=declaration`；`status: not-applicable`；`two-way: not-run`；`files_scanned: 1`；**exit 0** |
| 同上（规格面无回归） | `... --stage requirements --repo .` | `decision=pass errors=0 advisories=38 waived=0`（同一批）；**exit 0** |

**过程中出现的 3 次纠正（已在回传中披露，非裁定）**：
1. `§ Inherited Blockers` 的登记依据表被 pre-analyze 的行文法读成表体（`row-1…row-5` 的 `Disposition` 为空）⇒ 改为散文登记，表体只留一行。
2. 哨兵行的 `Source row` 写成 `（无行）` ⇒ 不是 `<feature>:<row>` 定位符，也不在 `ABSENT_LOCATORS` 内 ⇒ 改用 owner 承认的哨兵形态 `(none)`。
3. 第一版把 `Source row` 写成 `087-arch-diagram-docs:requirements.md` ⇒ 仍不合 `<feature>:<row>` 文法，方向错在把「依赖集为空」当成一条可处置记录。

## 2. 镜像与生成副本（相对基线无新漂移）

```text
/tmp/087-toolenv/bin/python -c "import typer,sys; print(sys.version.split()[0], typer.__version__)"
  -> 3.11.13 0.27.3            （前置条件实测：该 scratch venv 存在且可 import typer；本计划不创建它）
/tmp/087-toolenv/bin/python scripts/python/regen-command-copies.py --check
  -> OK: all per-tool command copies match the source templates.                          exit 0
/tmp/087-toolenv/bin/python scripts/python/sync-mirrors.py --check
  -> ok ×6（templates 22 / skills/external 415 / skills/internal 138 / agents 16 / scripts 121 / shared 94）  exit 0
python3 scripts/python/sync-mirrors.py --check（裸解释器，反例）
  -> Traceback … ModuleNotFoundError: No module named 'typer' + ok ×6 + "DRIFT detected"  exit 2
```

裸解释器那一行的 `DRIFT detected` 是内嵌 `regen` 子进程 import 失败冒充的信号（同一份输出里六对镜全 `ok`）：
处置是**换解释器重跑**，MUST NOT 据此跑 `--write`。

⇒ 实施期的验收 MUST 用能 import `typer` 的解释器；**本阶段零漂移、零写入**（检查类命令均只读）。

## 3. 既有守卫与基线（供实施期比对）

```text
python3 -m pytest tests/contract -q   -> 6038 passed, 17 failed, 2 skipped (289.58s)    （research R6，2026-11-06）
```

本特性直接相关的四条守卫在**未改动前**全部通过（`research.md` R2 的实测）：

```text
/tmp/087-toolenv/bin/python -m pytest tests/contract/test_expression_gate_wiring.py \
    tests/contract/test_docs_command_template.py tests/contract/test_confirmation_gates_sweep.py -q
  -> 1 failed, 83 passed, 1 warning in 1.84s
     FAILED tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
/tmp/087-toolenv/bin/python -m pytest tests/contract/test_directory_governance.py \
    tests/contract/test_docs_utils_cli.py tests/integration/test_docs_command_scenarios.py -q
  -> 35 passed, 1 warning in 0.62s
  （拆开：test_directory_governance.py -> 21 passed / test_docs_utils_cli.py -> 11 passed /
    test_docs_command_scenarios.py -> 3 passed，合计 35）
```

`test_residual_total_within_sc002_target` 的失败**先于本特性存在**（residual 27 > 25% of baseline 93，085 遗留）。

## 4. 与本阶段的判据声明不一致的地方（如实记录）

- **`status` 字段为什么是 `not-run-docs-only`**：本阶段**跑了**静态校验与镜像检查（§ 1/§ 2），
  但没有跑任何**被改动代码的** pytest 用例——`targeted-set-v1` 的选中依据是「改动路径全部是规格/记忆文档」，
  所以 `pytest` 侧的读数是**基线复量**（§ 3），不是「本阶段改动后的回归」。机器可读行见
  `plan-stage-status.jsonl`（六字段：`stage` / `row_type` / `status` / `selection_basis` / `changed_paths[]` / `evidence_ptr`）。
- **`clean` 判据不在本阶段**：检查器本身属实施期交付物，本阶段只能用 `quickstart.md` S1 证明**它现在还不存在**（`argparse` 以 exit 2 拒绝 `obligation`）——这条红是预期内的，MUST NOT 被读成失败。
- **本仓 `docs/` 的 `clean` 也不在验收面内**：85 个载体里 84 个无图、唯一有图的那份无追溯记录 ⇒
  检查器落地后本仓**必然** `clean=false`。该读数已登记在 `plan.md` § Residual Risk 的「已知红基线」里，
  验收面只能是夹具空间（S3 / S9）与守卫无新失败。

## 5. attempt 1 → attempt 2 的读数差异（为什么变了）

| 读数 | attempt 1 | attempt 2 | 差异来源 |
|------|-----------|-----------|----------|
| `validate-decision-tensions.py` 的 `scanned` | 370 lines | **562 lines** | 修复轮给 `plan.md` 加了 § Test Plan、给两份契约各加了一条条款（`C-016` / `C-008a`） |
| `pre-analyze-check.py` 的 advisories | 0 | **38** | 新增的条款与测试映射**点名了实施期才存在的路径**（两个测试文件、11 个夹具根、`docs/.speckit/**`、T-005 反题的两个 `diagrams/` 目录）。`errors` 仍为 0 |
| 结构面 `doc-consistency-check.py --action structure` | `not-applicable`（`files_scanned: 1`） | `not-applicable`（`files_scanned: 1`），exit 0 | 结论不变：执行类规格不做结构判定 |
| 载体总数 | 23 | **85** | 23 是一级目录计数造成的低估；复测用 `rglob`，且 `docs/ARCHITECTURE.md` 在本仓**不存在**（见 `plan.md` § Residual Risk 的注） |
| 守卫 pytest 读数 | 75 passed（三文件合并） | **1 failed / 83 passed**（三文件合并）+ **35 passed**（另三文件合并） | 更换了被测文件集合（见 § 3），不是同一批用例变了色 |
