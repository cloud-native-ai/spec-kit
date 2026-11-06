# Quickstart — 087 配套图义务（Verify & Walkthrough）

**Feature**: 087 架构图为核心的文档空间 | **Date**: 2026-11-06 | **Stage**: plan (Phase 1)

本文件只登记**计划期已实跑的读法**与**实施期要跑的场景**。判据、取值域与 schema 的 owner 是
`contracts/diagram-obligation.contract.md`（`C-NNN`）与 `contracts/flow-obligations.contract.md`；
本文件不复述它们，只给命令行与预期形状。

**执行前提**：所有命令以**工作树根**为 cwd（`--root .` 是项目根，不是 `docs/`，见 `C-001`）。
`pytest` / `typer` 不在裸 `python3` 里（research `R6`）：镜像与 `regen` 检查 MUST 用能 import `typer`
的解释器（一次性 scratch venv 即可），否则 `sync-mirrors.py --check` 会**假红**（六对镜本身全 ok）。

---

## S1 — 检查器在既有文档空间上跑通（规划期已实跑）

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root . --json
```

计划期读数（规划期实跑，`docs-utils.py` 当前的 `--action` 选择表**尚不含** `obligation`；实施期才新增）：

```text
$ python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root . --json
docs-utils.py: error: argument --action: invalid choice: 'obligation'
  (choose from 'scan', 'expire', 'clean', 'archive-check', 'stats', 'validate', 'fix-links', 'audit')
exit 2
```

⇒ 这是**预期中的红**：动作名是实施期的交付物，`argparse` 以退出码 2（输入错误）拒绝它，
不产生任何 payload。实施期新增该动作后，本命令 MUST 输出 `C-013` 形态的 payload，且**退出码 0**
（判定完成，与干净与否无关）。

同一工作树上，既有动作的实测基线（供对照，本特性 MUST NOT 改变它们）：

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .
```

```text
{"violations": [ {"kind":"root-entry-oversize","path":"CHANGELOG.md","detail":"73 lines > 60 (one-screen rule)"},
                 {"kind":"note-frontmatter","path":"docs/notes/081-acceptance-hardening-final.md", ...},
                 {"kind":"note-frontmatter","path":"docs/notes/type-follows-stage-misclassification.md", ...} ]}
exit 0
```

这 3 条是**先于本特性存在的违规**（`validate` 的判据不含图义务，`C-015`），所以本特性不修它们，
也不把「`validate` 零违规」写成验收判据。

## S2 — 载体集合的规划期人口普查（已实跑，只读）

计划期用一段一次性只读扫描（与 `C-003` 的载体表同口径：六类正式目录内 `*.md` + 根 `ARCHITECTURE.md`）读到：

```text
concepts/ 12 · tutorials/ 2 · tasks/ 1 · reference/ 1 · decisions/ 5 · contribute/ 1  → 22
+ ARCHITECTURE.md                                                                       → 23 carriers
```

其中**只有一份文档引用了图的两面并实际解析**：`docs/tutorials/quickstart.md` 第 262 行
→ `docs/assets/quickstart-workflow.png`，同图源 `docs/assets/quickstart-workflow.puml`、
另一渲染面 `docs/assets/quickstart-workflow.svg`（`delivery-contract.md` § D2 的 puml 行要求 `svg`+`png` 两面）。

两条**必须在实施期显式处理**的读数：

1. **零追溯记录**：`docs/.speckit/runs/` 在本仓尚不存在 ⇒ 这张唯一存在的图按 `C-007` 第 4 条
   MUST 判 `not-evaluated` / `no-trace-record`，**MUST NOT** 判 `satisfied`（`FR-013`：无记录 = 未接受）。
   这是正确而非误判，也正是 `FR-016` 禁止的假绿的反面。
2. **不补写本仓 `docs/`**：本线是框架改动（Two Hats），`docs/` 只接受生成/镜像（`requirements.md`
   § Out of Scope 第 4 条）。因此 S2 的人口普查**只用于**验证检查器的判定形状，不产生任何内容改动。

## S3 — 负向可观测（`FR-023` 的核心场景，实施期执行）

夹具四段全部纯文件、零渲染、零网络（research `R5`）。最小复现（以 `missing-face` 为例）：

```bash
# 1) 干净夹具：两面齐 + 引用解析 + 追溯记录
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation \
  --root tests/fixtures/docs-obligation/clean --record <ts>-diagram-trace.json --json
# 预期：documents[0].verdict = satisfied / reason = reference-resolves ; summary.clean = true ; exit 0

# 2) 删掉渲染面再跑：必须由绿转红，且 finding 点名该文档与该面
rm tests/fixtures/docs-obligation/missing-face/docs/concepts/diagrams/foo.svg
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation \
  --root tests/fixtures/docs-obligation/missing-face --record <ts>-diagram-trace.json --json
# 预期：verdict = missing / reason = orphan-source（源在、渲染面缺）; summary.clean = false ; exit 0
```

- **退出码不变（0）**是设计要求（`C-001`）：红绿在 payload 里，不在退出码里；
  `FR-023` 的「验证必须变红」判在 `summary.clean` 与 `documents[].verdict` 上，MUST NOT 判在退出码上。
- 删**源**而非渲染面：`verdict = missing`，`reason` 仍为 `orphan-source` 的补集（两面剩一面即失面报告，
  `FR-008`）；两值都在 `C-005` 的闭集内，不得新增第三种写法。

## S4 — 确定性 / 幂等（`FR-015`、`SC-006`）

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/clean --record R.json --json > a.json
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/clean --record R.json --json > b.json
cmp a.json b.json && echo IDENTICAL
git status --porcelain tests/fixtures/docs-obligation/clean   # 预期：空（检查器零写）
```

预期：`IDENTICAL`（`documents[]` 按 `path` 字典序，`C-006`）+ **零写**。第二次运行前删掉第一条输出的比较对象
之外不得有任何文件变化——这正是 `C-002` 的「允许的副作用集合是空集」。

## S5 — 豁免的可见性与失效（`FR-004`、`SC-008`）

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/exempt-ok --json
# 预期：verdict = recorded-exemption / reason = exempt-chronological ; summary.exempted = 1 ; summary.clean = false

python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/exempt-superseded --json
# 预期：verdict = not-evaluated / reason = exemption-invalid ; summary.exemption_superseded = 1
```

`summary.exempted > 0 ⇒ clean=false` 是 `C-013` 的硬约束：**豁免可见，不等于通过**。

## S6 — 流程侧的接线验证（`FR-005`~`FR-010`、`FR-017`）

不是命令，而是**读文本**的验收：改动落点见 `data-model.md` E7 与 `contracts/flow-obligations.contract.md` A–E 组。

| 场景 | 判据 | 验证命令 |
|------|------|----------|
| `create-docs` 新建文档 | Authoring Flow R5 产出图两面、R6 报两面具名 | `pytest tests/contract/test_expression_gate_wiring.py -q` |
| `improve-docs` 改名改图 | 图的引擎与源不变（`FR-010`）；无须动图时明说「no diagram work」 | `pytest tests/contract/test_docs_command_template.py -q` |
| `docs.md` 分派 | W1 接线小节未动、`stop-and-confirm` 仍字面存在、`improve-docs` 指针仍在 | `pytest tests/contract/test_confirmation_gates_sweep.py -q -k test_protected_gate_preserved` |
| 读者面 | `documentation-model.md` 仍在目录治理清单内 | `pytest tests/contract/test_directory_governance.py -q` |

这些命令的计划期实测基线（research `R6`）：`tests/contract` **6038 passed / 17 failed / 2 skipped**，
其中 `test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target` 是**先于本特性存在**的失败。
⇒ 判据是**相对基线无新失败**；写成「全绿」在本仓当前状态下不可达，写下来就是一条没人量过的判据。

## S7 — 镜像与生成副本（`plan.md` § Mirror Obligations）

```bash
# 需能 import typer 的解释器；裸 python3 会因内嵌 regen 调用而假红（research R6 推论 1）
<venv>/bin/python scripts/python/regen-command-copies.py --check
<venv>/bin/python scripts/python/sync-mirrors.py --check
```

计划期读数：两条均 **exit 0**（`regen` → `OK: all per-tool command copies match`；`sync-mirrors` 六对镜全 `ok`）。
⇒ 实施期的判据同为**无新漂移**，不是「退出码 0」这一条绝对断言。

## S8 — 本仓的零改动核对（Two Hats）

```bash
git diff --name-only 24cb4edc...HEAD -- docs/
```

计划期读数：**空输出、退出码 0**（`docs/` 自 base 起零改动）。

预期：**空**。本特性只改框架源与其镜像（`skills/` → `.specify/skills/`、`templates/commands/` → 四家 per-tool 副本），
`.specify/` 的运行时副本由 `sync-mirrors.py` 生成；`docs/` 树的内容工作不属本特性（A6 / `requirements.md` § Out of Scope）。
