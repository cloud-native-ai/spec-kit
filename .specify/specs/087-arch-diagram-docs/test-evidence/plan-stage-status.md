# Plan Stage — Test Evidence (087-arch-diagram-docs)

**Recorded**: 2026-11-06 | **Stage**: plan | **Base**: `24cb4edc` | **Worktree**: `line/087-arch-diagram-docs`
**Interpreter**: `/tmp/087-toolenv/bin/python` → CPython 3.11.13, `pytest 9.2.0`（一次性 scratch venv，`--system-site-packages` + `typer rich httpx platformdirs readchar truststore pytest pyyaml`）。

**判据形态（本特性统一口径）**：本仓基线**不是全绿**，因此这里的每一条都是**相对基线无新失败 / 无新漂移**，而不是绝对退出码 0。基线值与实测值并列在每一条下面。

## 1. 本阶段产物的静态校验

| 检查 | 命令 | 读数 |
|------|------|------|
| 决策张力六字段与行文法 | `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs` | `status: ok`；`scanned: 370 lines, 5 record(s)`；6 个标签全 `pass (0)`；`0 error(s), 0 warning(s)` |
| 结构面（执行类） | `python3 .specify/scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/087-arch-diagram-docs` | `class=execution source=declaration`；`status: not-applicable`；`two-way: not-run`；`files_scanned: 1` |
| 运行时行 / 前提 / 继承阻塞 / 悬空 ID / 计数 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/087-arch-diagram-docs --stage plan` | `decision=pass errors=0 advisories=0 waived=0`（`fr=23 sc=10 files=9`） |
| 同上（规格面无回归） | `... --stage requirements` | `decision=pass errors=0 advisories=0`（同上 counts） |

**过程中出现的 3 次纠正（已在回传中披露，非裁定）**：
1. `§ Inherited Blockers` 的登记依据表被 pre-analyze 的行文法读成表体（`row-1…row-5` 的 `Disposition` 为空）⇒ 改为散文登记，表体只留一行。
2. 哨兵行的 `Source row` 写成 `（无行）` ⇒ 不是 `<feature>:<row>` 定位符，也不在 `ABSENT_LOCATORS` 内 ⇒ 改用 owner 承认的哨兵形态 `(none)`。
3. 第一版把 `Source row` 写成 `087-arch-diagram-docs:requirements.md` ⇒ 仍不合 `<feature>:<row>` 文法，方向错在把「依赖集为空」当成一条可处置记录。

## 2. 镜像与生成副本（相对基线无新漂移）

```text
/tmp/087-toolenv/bin/python scripts/python/regen-command-copies.py --check   -> exit 0  "OK: all per-tool command copies match the source templates."
/tmp/087-toolenv/bin/python scripts/python/sync-mirrors.py --check            -> exit 0  六对镜全 ok（templates 22 / skills/external 415 / skills/internal 138 / agents 16 / scripts 121 / shared 94）
python3 scripts/python/sync-mirrors.py --check（裸解释器）                    -> exit 2  ModuleNotFoundError: No module named 'typer'（内嵌 regen 调用），六对镜本身仍全 ok
```

⇒ 实施期的验收 MUST 用能 import `typer` 的解释器；**本阶段零漂移、零写入**（检查类命令均只读）。

## 3. 既有守卫与基线（供实施期比对）

```text
python3 -m pytest tests/contract -q   -> 6038 passed, 17 failed, 2 skipped (289.58s)    （research R6，2026-11-06）
```

本特性直接相关的四条守卫在**未改动前**全部通过（`research.md` R2 的实测）：

```text
pytest tests/contract/test_expression_gate_wiring.py tests/contract/test_docs_command_template.py \
       tests/contract/test_directory_governance.py -q      -> 75 passed
pytest tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target -q
                                                           -> FAILED（先于本特性存在：residual 27 > 25% of baseline 93）
pytest tests/contract/test_confirmation_gates_sweep.py -q -k test_protected_gate_preserved
                                                           -> 16 passed, 30 deselected
```

## 4. 与本阶段的判据声明不一致的地方（如实记录）

- **`not-run-docs-only` 的反面**：本阶段**跑了**静态校验与镜像检查，因此不适用 `not-run-docs-only`；但 `targeted-set-v1` 的完整表单（每条守卫逐条记录）留待 tasks 阶段按 `tasks.md` 的行号重跑，本文件只登记「本阶段实际跑过的」。
- **`clean` 判据不在本阶段**：检查器本身属实施期交付物，本阶段只能用 `quickstart.md` S1 证明**它现在还不存在**（`argparse` 以 exit 2 拒绝 `obligation`）——这条红是预期内的，MUST NOT 被读成失败。
