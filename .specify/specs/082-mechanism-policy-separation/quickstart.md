# Quickstart — 082 机制/策略分离（可执行场景）

每个场景标注三件事：**执行口径**（本次 plan 运行实际跑过 = `run`；依赖尚未落地的产物 = `deferred`，并列出它依赖的前提）、**命令逐字**、**判据**。所有命令在仓根执行。

> 本文件属于 `/speckit.plan` 的 Post-Generation Quality Gate 的 execution-verify 范围：`run` 的场景含**实际输出**；`deferred` 的场景逐条列出它假设的 flags、ID 形态、文件位置与工具行为（见各场景末尾的 **Premises**），供 `/speckit.tasks` 与 `/speckit.implement` 重新测量而不是继承。

## S1 — 运行器与测试入口（`run`）

```bash
.venv/bin/python --version && .venv/bin/python -m pytest --version
git --version
```

实测输出（本阶段）：

```
Python 3.14.6
pytest 9.2.0
git version 2.54.0 (Apple Git-157)
```

**判据**：三者与 `research.md` § R1 一致；不一致时本文件里的「基线 892 passed」不再可比（GM-08 的差集判据失效，须重测基线）。

**Premises**：`.venv/` 已就位；`PYTHONPATH` 未参与（下一条 S2 专门处理）。

## S2 — 定向集基线（`run`）

```bash
env -u PYTHONPATH bash scripts/bash/run-tests.sh -q -p no:cacheprovider \
  --names-out /tmp/mp-plan-probe/impact-names.txt \
  tests/contract/test_merge_provenance_gate.py tests/contract/test_expression_compatibility.py \
  tests/contract/test_one_source_of_truth.py tests/contract/test_bilingual_expression.py \
  tests/contract/test_token_efficiency_gates.py tests/contract/test_feedback_skill_conformance.py \
  tests/contract/test_mirror_parity_suite.py tests/contract/test_glossary_mechanism.py \
  tests/contract/test_instructions_section_propagation.py \
  tests/contract/test_skill_layer_visibility_guards.py tests/contract/test_directory_governance.py \
  tests/contract/test_portable_skill_creation.py
```

实测输出：`892 passed in 16.66s`；`--names-out` 文件写入 0 条失败名。

**判据**：实现期以同一命令 + 六个新模块重跑，`实现后失败集 − 本基线失败集（空）` 必须为空。

**Premises**：`run-tests.sh` 优先解析 `.venv/bin/python`（未改）；`env -u PYTHONPATH` 是必要的，否则 pytest 无法启动（`research.md` § R1 的逐字报错）。

## S3 — 镜像与命令副本基线（`run`）

```bash
python3 scripts/python/sync-mirrors.py --check; echo "rc=$?"
python3 scripts/python/regen-command-copies.py --check; echo "rc=$?"
```

实测输出（`sync-mirrors.py --check`，逐行）：

```
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (62 files)
rc=0
```

**判据**：实现关闭时两条 `--check` 仍 exit 0；`shared/` 的文件数在新增 owner 文档后从 62 变为 63 —— 这是同步后的新基线，MUST NOT 被写死进断言。

**Premises**：`scripts/python/` 下这两个引擎存在且未改；`.specify/` 镜像当前与源逐字节相等（上面逐行证明）。

## S4 — SC-003 封闭集预演（`run`）

在 `tmp_path` 写一个脚本（`/tmp/mp-plan-probe/conserv.py`，本阶段实跑的形态），逻辑是 `data-model.md` § GM-03 的补集断言：

```python
import re, subprocess
base = "3ffeb26e"
paths = subprocess.run(["git","ls-tree","-r","--name-only",base,"--","skills/","templates/commands/"],
                       capture_output=True, text=True).stdout.split()
allowed = {  # 六条「属比较单元」的允许差异路径（data-model.md § GM-03 第 1–6 行）
 "skills/external/create-skills/SKILL.md",
 "skills/external/create-skills/references/mechanism-policy-check.md",
 "skills/external/improve-skills/SKILL.md",
 "skills/external/improve-skills/references/loop-playbook.md",
 "skills/external/merge-skills/SKILL.md",
 "skills/external/merge-skills/references/provenance-record.md",
}
comp = [p for p in paths if p not in allowed]
bad = 0
for p in comp:
    blob = subprocess.run(["git","cat-file","blob","%s:%s" % (base, p)], capture_output=True).stdout
    try:
        cur = open(p, "rb").read()
    except OSError:
        bad += 1; continue
    if blob != cur:
        bad += 1
print("compared=%d complement=%d allowed_in_unit=%d frozen_mismatches=%d"
      % (len(paths), len(comp), len(allowed & set(paths)), bad))
```

实测输出（改动前）：

```
compared=575 complement=570 allowed_in_unit=5 frozen_mismatches=0
```

**读法**：`allowed_in_unit=5` 表示允许集里已存在的路径数（`mechanism-policy-check.md` 尚未创建，故 6 条中 5 条在基线里存在）；实现后它应为 6，`frozen_mismatches` 仍为 0。**判据**：`compared` 必须为 575（分母非零），`frozen_mismatches` 为 0。

**Premises**：基线提交 `3ffeb26e` 在本仓可达；比较单元 = `skills/` + `templates/commands/`（不含 `.specify/` 镜像与 `__pycache__`）；`git cat-file blob` 可用（RS-003）。

## S5 — 元技能形状与红线的 before/after（`run` 的 before 已跑，`after` 属实现期）

```bash
python3 skills/external/improve-skills/scripts/skill-shape.py skills/external/<name>/SKILL.md; echo "rc=$?"
python3 skills/external/improve-skills/scripts/redline-check.py skills/external/<name>/SKILL.md; echo "rc=$?"
```

实测（改动前，`<name>` ∈ `create-skills` / `improve-skills` / `merge-skills`）：

| 文件 | `skill-shape.py` rc | `redline-check.py` rc / verdict |
|---|---|---|
| `create-skills` | 10（可控 ≈ 5354 / 5000） | 0 / `PASS — no red line triggered` |
| `improve-skills` | 10（可控 ≈ 5584 / 5000） | 0 / `PASS — no red line triggered` |
| `merge-skills` | 10（可控 ≈ 5096 / 5000） | 0 / `PASS — no red line triggered` |

**判据**：实现后被改文件 MUST 记录 exit code 与 `est_tokens_controllable` 的 before/after 两数与 delta；`redline-check.py` MUST 仍为 rc 0（若转红则按 red-lines 处置，MUST NOT 静默例外）。`skill-shape.py` 的 rc 10 在改动前就已存在，属 `improve-skills` Hard Constraint 3 情形 (a) 的基线。

**Premises**：脚本位于 `skills/external/improve-skills/scripts/`（不在 `.specify/scripts/python/`）；`skill-shape.py` 的预算为 5000 可控 tokens、`--help` 可查；`redline-check.py` 的位置参数是 `skill_md` 路径。

## S6 — 消费侧「策略缺失 → 零写入」（`deferred`，实现期）

```bash
env -u PYTHONPATH bash scripts/bash/run-tests.sh -q -p no:cacheprovider \
  tests/contract/test_mechanism_policy_missing_policy.py
```

**判据**：测试在 `tmp_path` 内造「假技能 + 假运行目录」，先取路径集 + sha256 快照，再走 owner § Consumption Contract 的检查（缺策略分支），断言快照逐文件相等（零写入），随后补齐策略重跑，断言产物哈希等于基线产物哈希。

**Premises**：本模块由实现期创建（`data-model.md` E-5、`contracts/guard-and-measurement.contract.md` GM-05）；`tmp_path` 由 pytest 提供（既有 `tests/conftest.py` 已存在）；被检对象是 **owner 契约文本 + 文件系统快照**，不是 AI 行为。

## S7 — SC-002 的宿主实录（`deferred`，实现期，证据而非测试）

**判据**：一个受支持宿主上，对「误置样本 ×2 + 正确分层样本 ×2」在改动前 / 改动后各跑一次 `create-skills`（或 `improve-skills`），改动后 2/2 被点名（文件 + 位置）、2/2 零误报。记录落 `test-evidence/sc-002-<date>.txt`，含宿主名 + 版本原文、输入草稿路径、输出原文、逐样本 verdict 表。

**Premises**：宿主取自 `docs/reference/cli/supported-agent-tools.md` 的 roster（`AGENT_CONFIG` 为准）；`create-skills` § 6 的判定行已在实现期落地（SW-01）；样本草稿放在受制裁的临时根（`.specify/.tmp/` 或 `tmp_path`），MUST NOT 落到仓内未登记目录。

## S8 — SC-001 / SC-005 的题集与作答（`deferred`，实现期）

**判据**：owner § Worked Examples 的题集 ≥ 12 条（`data-model.md` E-7 / V-21）；两位 fresh-context 只读判定者仅凭 owner 文档作答，一致率 100%（SC-001）；一位未参与本特性的读者作答，正确数 = 题集全集（SC-005）。记录落 `test-evidence/sc-001-<date>.txt` 与 `sc-005-<date>.txt`。

**Premises**：owner 文档与附录题集已创建；判定者不能读到 `requirements.md` / `plan.md`（只读 owner，否则分母被污染）；题集的 `basis` 列可被解析（`test_mechanism_policy_decidability.py`）。

## S9 — 阶段门（`run`）

```bash
python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/082-mechanism-policy-separation --stage plan --repo .
python3 scripts/python/validate-requirements.py \
  .specify/specs/082-mechanism-policy-separation/requirements.md
```

实测：见 `test-evidence/plan-gates.txt`（本阶段逐字输出，含 exit code）。

**Premises**：本仓 `.specify/skills/sdd-loop-driver/` 已安装（镜像自 `skills/external/sdd-loop-driver/`）；`validate-requirements.py` 的计数字面以那次运行为准。
