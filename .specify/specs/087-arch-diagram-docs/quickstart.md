# Quickstart — 087 配套图义务（Verify & Walkthrough）

**Feature**: 087 架构图为核心的文档空间 | **Date**: 2026-11-06 | **Stage**: plan (Phase 1，attempt 2)
**Revision note**: 本版按独立校验 attempt 1 的 `P1-1` / `P1-2` 重写 S3–S5 与 S9——**每个命令示例自带一条 premises 行**
（假设的 flag / ID 形态 / 计数 / 落点），未实现的命令逐例给出当前实测读数，不再用文件级免责代替逐例前提。

判据、取值域与 schema 的 owner 是 `contracts/diagram-obligation.contract.md`（`C-NNN`）与
`contracts/flow-obligations.contract.md`；本文件不复述它们，只给命令行、**前提**与预期形状。

**执行前提（全局，逐例仍各自声明自己的前提）**：所有命令以**工作树根**为 cwd（`--root .` 是项目根，
不是 `docs/`，见 `C-001`）。`pytest` / `typer` 不在裸 `python3` 里（research `R6`）：镜像与 `regen` 检查
MUST 用能 import `typer` 的解释器；本阶段的实测解释器是 `/tmp/087-toolenv/bin/python`
（CPython 3.11.13 / `pytest 9.2.0` / `typer 0.27.3`，一次性 scratch venv）。该路径**不由本计划创建**，
换机器时按同一口径新建一个即可；文件不存在时如实记录「前置条件未就绪」，不得把裸 `python3` 的假红当结论。

---

## S1 — 检查器在既有文档空间上跑通（规划期已实跑）

**premises**: `--action obligation` **尚未实现**（本阶段 `docs-utils.py` 的 `choices` 表不含它）；
`--json` 是引擎的既有输出形态。因此本条**预期**是「`argparse` 以退出码 2 拒绝」，这是**预期中的红**。

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root . --json
```

计划期实测（2026-11-06，单行；`argparse` 的 usage 块被省略，此处只记错误行本体）：

```text
$ python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root . --json
docs-utils.py: error: argument --action: invalid choice: 'obligation' (choose from 'scan', 'expire', 'clean', 'archive-check', 'stats', 'validate', 'fix-links', 'audit')
exit 2
```

⇒ 动作名是实施期的交付物，`argparse` 以退出码 2（输入错误）拒绝它，不产生任何 payload。
实施期新增该动作后，本命令 MUST 输出 `C-013` 形态的 payload，且**退出码 0**（判定完成，与干净与否无关）。

同一工作树上，既有动作的实测基线（供对照，本特性 MUST NOT 改变它们）：

**premises**: `--action validate` 是既有动作；本仓当前有 3 条**先于本特性存在**的违规。

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .
```

```text
{"violations": [ {"kind":"root-entry-oversize","path":"CHANGELOG.md","detail":"73 lines > 60 (one-screen rule)"},
                 {"kind":"note-frontmatter","path":"docs/notes/081-acceptance-hardening-final.md","detail":"missing: title,created,expires,status"},
                 {"kind":"note-frontmatter","path":"docs/notes/type-follows-stage-misclassification.md","detail":"missing: "} ]}
exit 0
```

这 3 条先于本特性存在（`validate` 的判据不含图义务，`C-015`），本特性不修它们，
也不把「`validate` 零违规」写成验收判据。

## S2 — 载体集合与图人口的规划期普查（已实跑，只读）

**premises**: 与 `C-003` 的载体表同口径（六类正式目录内 `*.md`，**递归**；根 `ARCHITECTURE.md` 只在
**该文件存在**时入集）；`docs/notes/`、`docs/archive/`、`docs/.speckit/` 与站点工具目录不计；`python3` 即可
（纯标准库），cwd = 工作树根。

```bash
python3 - <<'EOF'
import pathlib
docs = pathlib.Path('.') / 'docs'
dirs = ['concepts','tutorials','tasks','reference','decisions','contribute']
total = 0
for d in dirs:
    n = len(list((docs/d).rglob('*.md')))      # rglob：递归，不是一级目录
    total += n
    print(f'{d}/ {n}')
arch = (docs/'ARCHITECTURE.md').exists()
print('ARCHITECTURE.md', arch)
print('carriers', total + (1 if arch else 0))
EOF
```

计划期实测（2026-11-06，逐行即输出）：

```text
concepts/ 12
tutorials/ 2
tasks/ 1
reference/ 64
decisions/ 5
contribute/ 1
ARCHITECTURE.md False
carriers 85
exit 0
```

> **纠正留痕（非裁定，共两次）**：attempt 1 的同一普查把 `reference/` 记成 1（实际 64：`agents/ 5`
> `cli/ 7` `commands/ 27` `history/ 8` `skills/ 13` `teams/ 3` `glossary.md`），因此写的是 **23**；
> 本版第一次复测用 `rglob` 得到 85，却把 `ARCHITECTURE.md` 当成「已存在」而写成 **86**——实测该文件在
> 本仓**不存在**（`grep` 全仓仅命中 `create-docs/SKILL.md` 的基线登记行）。因此本版最终记录是 **85**。
> 两次订正都只是**纠正**（`C-003` 的载体表未变：它登记的是「若项目根有 `ARCHITECTURE.md` 则它是载体」的
> 语义，不是「本仓已有一份」），不是新裁决。**这条留痕存在的原因**：一个数被改了两次就说明它是量出来的，
> 不是推出来的；把中间那次错误留在纸面上，实施期才不会再把它「复原」成 86。

其中**只有一份文档引用了解析到图的路径**：`docs/tutorials/quickstart.md` 第 262 行
→ `../assets/quickstart-workflow.png`，同目录同图源 `docs/assets/quickstart-workflow.puml` 与另一渲染面
`docs/assets/quickstart-workflow.svg`（`delivery-contract.md` § D2 的 `plantuml` 行要求 `.svg` + `.png` 两面）。
另一处命中是**历史决策** `docs/reference/history/04-draw-plantuml-optimization.md`：它把 `.puml` 等扩展名
当**正文内容**讨论，不产生指向渲染产物的引用 ⇒ 该文档在 `C-016` 序 3 落 `missing` / `no-diagram-reference`，
**不是** `satisfied`。这一条写在这里是因为「文本里出现 `.png` 字样」与「引用了渲染产物」是两件事，
普查脚本按扩展名计数时会把它们混为一谈。

三条**必须在实施期显式处理**的读数：

1. **零追溯记录**：`docs/.speckit/runs/` 在本仓尚不存在 ⇒ 这张唯一存在的图按 `C-016` 序 7
   MUST 判 `not-evaluated` / `no-trace-record`，**MUST NOT** 判 `satisfied`（`FR-013`：无记录 = 未接受）。
2. **同一张图也缺 D1 的 HTML 面**：`docs/assets/` 下没有 `quickstart-workflow.html`。检查器**不判**这一面
   （`C-012` 的四项不含它，`draw-diagram` 的 D6 才是它的 owner）；登记在此是为了让「本仓唯一的图**不**满足
   今日交付契约」这一事实可见，而不是让检查器替它报错。
3. **不补写本仓 `docs/`**：本线是框架改动（Two Hats），`docs/` 只接受生成/镜像（`requirements.md`
   § Out of Scope 第 4 条）。因此 S2 的普查**只用于**校准检查器的判定形状与被检规模，不产生任何内容改动。

## S3 — 负向可观测（`FR-023` / `SC-002` 的核心场景，实施期执行）

**premises（逐夹具，实施期由 `tests/unit/test_docs_utils_obligation.py` 与
`tests/integration/test_docs_obligation_scenarios.py` 执行，命令形态一致）**：

| 夹具 | 前置状态（仓库内的形态） | `--record` | 期望 `verdict` / `reason` |
|------|--------------------------|-----------|---------------------------|
| `clean/` | 两面齐 + 引用解析到 `foo.png` + 本夹具记录齐备（**无豁免记录**） | `tests/fixtures/docs-obligation/clean/docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json` | `satisfied` / `reference-resolves`；`summary.converged=true`、`summary.clean=true`（`exempted=0`，故两谓词同时成立）；exit 0 |
| `orphan-rendered/` | **删除前绿灯**的前态记录在案（`clean/` 同构）；渲染产物已删、源在、**引用指向源** | 本夹具记录 | `missing` / `orphan-rendered`；`converged=false`、`clean=false`；exit 0 |
| `orphan-source/` | 源已删、渲染产物在 | 本夹具记录 | `missing` / `orphan-source`；`converged=false`、`clean=false`；exit 0 |
| `stale-source/` | **两面都在**，源 mtime 严格晚于最早的渲染面 | 本夹具记录 | `stale` / `source-newer-than-render`；`converged=false`、`clean=false`；exit 0 |

**夹具 ID 形态**：追溯记录文件名 `<UTC ISO basic>-<8 hex>-diagram-trace.json`（例
`20261106T000000Z-aaaaaaaa-diagram-trace.json`）；计数形态：每个夹具恰 **1** 份载体文档、**1** 张图（两面以上）。
夹具落点与「`tmp_path` 副本」纪律见 `data-model.md` E6。

**`missing-face` 的原步序已被删除（P1-2 的修复本体）**：attempt 1 的 S3 在同一个 `missing-face` 夹具上
「先跑绿、再删渲染面、期望 `orphan-source`」。两处错：① 判据 `C-016` 序 4 规定「引用目标整个不在盘 ⇒
`reference-unresolved`」，序 5 才是失面，而原文把两个面混成一条用例，期望值随「删哪个面」而漂移；
② 原文的 `rm` 直接作用在**仓库内**夹具上，第二次运行就再也测不到「删除前的绿灯」。修复后**每个面各一个夹具**，
删除动作只发生在 `tmp_path` 的副本上：

```bash
# 1) 绿态基线：两面齐 + 引用解析 + 记录齐备
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation \
  --root tests/fixtures/docs-obligation/clean \
  --record tests/fixtures/docs-obligation/clean/docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json --json
# 预期：verdict = satisfied / reference-resolves ; summary.converged = true ; summary.clean = true ; exit 0

# 2) 失面（未删除前为绿灯，删除后必须转红）：渲染产物缺、源在、引用指向源
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation \
  --root tests/fixtures/docs-obligation/orphan-rendered \
  --record tests/fixtures/docs-obligation/orphan-rendered/docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json --json
# 预期：verdict = missing / reason = orphan-rendered（源在、渲染面缺）; summary.converged = false ; summary.clean = false ; exit 0

# 3) 面序对照：两面都在、只是源更新 ⇒ stale（不是 missing）
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation \
  --root tests/fixtures/docs-obligation/stale-source \
  --record tests/fixtures/docs-obligation/stale-source/docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json --json
# 预期：verdict = stale / reason = source-newer-than-render ; summary.converged = false ; summary.clean = false ; exit 0
```

- **退出码恒为 0**（`C-001`）：红绿在 payload 里，不在退出码里；`FR-023` 的「验证必须变红」判在
  `summary.converged` / `summary.clean` 与 `documents[].verdict` 上，MUST NOT 判在退出码上。
- **`orphan-rendered` 与 `orphan-source` 是两个值**（`C-005`）：`SC-002` 要求「点名缺失的那一面」，
  一个值同时表示两面就使该判据不可判。
- **判据的绿灯前态**：仓库里的夹具本身**永远是删除前的绿灯态**；「删一个面」发生在 `tmp_path` 的副本上
  （`data-model.md` E6 的纪律），因此「删除前绿灯」不是一句声明，而是同一条命令在 `clean/` 上的实测读数。

## S4 — 确定性 / 幂等 / 零写（`FR-015`、`SC-006`）

**premises**: 同一 `--root` + 同一 `--record`；输出重定向到**工作树之外**的两个临时文件（`${TMPDIR}`），
否则重定向本身会让 `git status` 非空，把「零写」量成假红。

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/clean --json > "${TMPDIR}/087-a.json"
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/clean --json > "${TMPDIR}/087-b.json"
cmp "${TMPDIR}/087-a.json" "${TMPDIR}/087-b.json" && echo IDENTICAL
git status --porcelain tests/fixtures/docs-obligation/clean    # 预期：空（检查器零写）
```

预期：`IDENTICAL`（`documents[]` 按 `path` 字典序、字段集固定，`C-006`）+ **零写**（`C-002` 的「允许的副作用集合是空集」）。
注意 `--record` 缺省时两份输出**同样**可比——缺省值以 `null` 出现，不省略字段。

## S5 — 豁免的可见性与失效（`FR-004`、`SC-008`）

**premises**: 三个夹具各带一份 `C-011` 形态的豁免记录（`exempt-ok` 三字段齐备；`exempt-bad` 缺
`justification`；`exempt-superseded` 记录齐备但文档已带解析到渲染产物的引用）。豁免记录**不产生**
`documents[]` 之外的计数，只走 `summary` 的两个字段。

```bash
python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/exempt-ok --json
# 预期：verdict = recorded-exemption / reason = exempt-chronological ; summary.exempted = 1
#       summary.converged = true（豁免是合法终态，不参与收敛算式）; summary.clean = false（exempted>0）

python3 skills/external/create-docs/scripts/docs-utils.py --action obligation --root tests/fixtures/docs-obligation/exempt-bad --json
# 预期：verdict = not-evaluated / reason = exemption-invalid ; summary.not_evaluated = 1 ; summary.converged = false

python3 skills/external/create-docs/scripts/docs-utils.py --action obligation \
  --root tests/fixtures/docs-obligation/exempt-superseded \
  --record tests/fixtures/docs-obligation/exempt-superseded/docs/.speckit/runs/20261106T000000Z-aaaaaaaa-diagram-trace.json --json
# 预期：verdict = not-evaluated / reason = exemption-invalid ; summary.exemption_superseded = 1 ; summary.converged = false
```

`summary.exempted > 0 ⇒ clean=false` 是 `C-013` 的硬约束：**豁免可见，不等于通过**。
同一条款同时规定 `exempted` **不参与** `converged`——因此 `exempt-ok/` 的读数是
**`converged=true` + `clean=false`**，这不是矛盾，而是「已收敛但仍不干净」这个真实状态的唯一写法
（`SC-008`；收敛判据的用法见 `C-008a` R6）。

## S6 — 流程侧的接线验证（`FR-005`~`FR-010`、`FR-017`）

不是命令，而是**读文本**的验收：改动落点见 `data-model.md` E7 与 `contracts/flow-obligations.contract.md` A–E 组。

**premises**: 这些守卫文件在盘且当前全绿（除 `test_residual_total_within_sc002_target`，它先于本特性存在）；
判据是**相对基线无新失败**。

| 场景 | 判据 | 验证命令 |
|------|------|----------|
| `create-docs` 新建文档 | Authoring Flow R5 产出图两面、R6 报两面具名 | `pytest tests/contract/test_expression_gate_wiring.py -q` |
| `create-docs` 全量 reconcile 收敛 | Reconcile R3/R4/R5 产图条目 + R6 图维度残差（`flow-obligations` C-008a） | `pytest tests/unit/test_docs_utils_obligation.py -q -k reconcile` |
| `improve-docs` 改名改图 | 图的引擎与源不变（`FR-010`）；无须动图时明说「no diagram work」 | `pytest tests/contract/test_docs_command_template.py -q` |
| `docs.md` 分派 | W1 接线小节未动、`stop-and-confirm` 仍字面存在、`improve-docs` 指针仍在 | `pytest "tests/contract/test_confirmation_gates_sweep.py::test_protected_gate_preserved[templates/commands/docs.md-stop-and-confirm]" -q`（**逐实例 node id**，不是 `-k test_protected_gate_preserved`） |
| 读者面 | `documentation-model.md` 仍在目录治理清单内 | `pytest tests/contract/test_directory_governance.py -q` |

计划期实测基线（2026-11-06，`/tmp/087-toolenv/bin/python -m pytest …`，逐条即第 5 步 gate 4 的读数）：

```text
pytest tests/contract/test_expression_gate_wiring.py tests/contract/test_docs_command_template.py \
       tests/contract/test_confirmation_gates_sweep.py -q
  -> 1 failed, 83 passed, 1 warning in 1.84s
     FAILED tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
pytest tests/contract/test_directory_governance.py tests/contract/test_docs_utils_cli.py \
       tests/integration/test_docs_command_scenarios.py -q
  -> 35 passed, 1 warning in 0.62s
pytest tests/contract/test_directory_governance.py -q        -> 21 passed
pytest tests/contract/test_docs_utils_cli.py -q              -> 11 passed
pytest tests/integration/test_docs_command_scenarios.py -q   -> 3 passed
tests/contract（全量，research R6）                          -> 6038 passed / 17 failed / 2 skipped
```

> **两处必须读懂再用的细节**：(1) `test_residual_total_within_sc002_target` 的失败**先于本特性存在**
> （它是 085 遗留的残差总数断言），本特性的实施 MUST NOT 让它变绿也不得让它变红更多——判据是「失败集不变」；
> (2) 两条 `pytest` 命令挑选的是**不同文件集合**（第一条 84 例，第二条 35 例），不是同一批用例跑了两次；
> 下文的三条单文件读数加起来是 21 + 11 + 3 = 35，正是第二条命令的例数。

⇒ 判据是**相对基线无新失败**；写成「全绿」在本仓当前状态下不可达，写下来就是一条没人量过的判据。

**`test_protected_gate_preserved` 是 16 个参数化实例，不是一条断言**：`KEEP_LIST`（该测试文件）里只有
`("templates/commands/docs.md", "stop-and-confirm")` 这一对属于 `docs.md` 的 `stop-and-confirm` 守卫，
其余 15 对分别钉别的受保护门。因此**宽选择器 `-k test_protected_gate_preserved` 是错的判据形态**：
它会在那 15 个无关守卫上变绿，而 `docs.md` 的那一条早已被删除——一条会因无关对象变绿的门等于没有门。
收窄到具体实例可以做到（`-k` 表达式做不到「按参数取值」这一粒度，node id 可以）：

```text
/tmp/087-toolenv/bin/python -m pytest "tests/contract/test_confirmation_gates_sweep.py::test_protected_gate_preserved[templates/commands/docs.md-stop-and-confirm]" -q
  -> 1 passed, 1 warning in 0.06s                     （2026-11-06 实测，本阶段复跑）
/tmp/087-toolenv/bin/python -m pytest tests/contract/test_confirmation_gates_sweep.py -q -k test_protected_gate_preserved
  -> 16 passed, 30 deselected                          （同一文件；这 16 例是**更宽的守卫**，不构成 docs.md 的判据）
```

⇒ 读法：`docs.md` 的 `stop-and-confirm` 判据只认第一条（`1 passed`，且 `1` 就是全部被选中的实例数）。
第二条的 `16 passed` 登记在此是为了**说明它不是本行的判据**，不是为了给它算读数。

## S7 — 镜像与生成副本（`plan.md` § Mirror Obligations）

**premises**: 需能 import `typer` 的解释器（`sync-mirrors.py` 内嵌调用 `regen-command-copies.py`，后者
`import specify_cli` → `import typer`）。本阶段实测解释器 `/tmp/087-toolenv/bin/python`；该 venv 由执行者
一次性创建，**不在仓内、不由本计划提供**。

```bash
/tmp/087-toolenv/bin/python scripts/python/regen-command-copies.py --check
/tmp/087-toolenv/bin/python scripts/python/sync-mirrors.py --check
```

计划期实测（2026-11-06，本次 attempt 2 复跑）：

```text
/tmp/087-toolenv/bin/python scripts/python/regen-command-copies.py --check
  -> OK: all per-tool command copies match the source templates.        exit 0
/tmp/087-toolenv/bin/python scripts/python/sync-mirrors.py --check
  -> ok  templates/ == .specify/templates/ (22 files)
     ok  skills/external/ == .specify/skills/ (415 files)
     ok  skills/internal/ == .specify/skills/internal/ (138 files)
     ok  agents/ == .specify/agents/templates/ (16 files)
     ok  scripts/ == .specify/scripts/ (121 files)
     ok  shared/ == .specify/shared/ (94 files)                          exit 0
python3 scripts/python/sync-mirrors.py --check   （裸解释器，仅作反例）
  -> Traceback … ModuleNotFoundError: No module named 'typer'
     ok  ×6（六对镜本身全 ok，与上同）
     DRIFT detected — run: … --write                                    exit 2
```

⇒ 两条结论分开读：**六对镜零漂移**是实测事实；裸解释器的 `exit 2` 与 `DRIFT detected` 是
**内嵌 `regen-command-copies.py` 的 import 失败冒充的漂移信号**（同一份输出里六对镜全是 `ok`）。
把这一行当漂移去 `--write` 会制造真实改动——**MUST NOT** 那样处置；正确处置是换解释器重跑。
⇒ 实施期的判据同为**无新漂移**，不是「退出码 0」这一条绝对断言。

## S8 — 本仓的零改动核对（Two Hats）

**premises**: base 是 `24cb4edc`；本特性只改框架源与其镜像。

```bash
git diff --name-only 24cb4edc...HEAD -- docs/
```

计划期实测（2026-11-06 复跑）：`git diff --name-only 24cb4edc...HEAD -- docs/` → **空输出、`exit 0`**；
`git status --porcelain docs/` → **空输出、`exit 0`**（`docs/` 自 base 起零改动，含未提交改动面）。

预期：**空**。本特性只改框架源与其镜像（`skills/` → `.specify/skills/`、`templates/commands/` → 四家 per-tool 副本），
`.specify/` 的运行时副本由 `sync-mirrors.py` 生成；`docs/` 树的内容工作不属本特性（A6 / `requirements.md` § Out of Scope）。

## S9 — Reconcile 的收敛回路（`SC-003`；实施期执行）

**premises**: reconcile 的收敛路径由 `contracts/flow-obligations.contract.md` `C-008a` 登记（R3 差异 → R4 计划 →
R5 产图 → R6 图维度残差）；本条的断言落在**夹具空间**（不是本仓 `docs/`），因为把本仓 85 份载体文档补图属内容工作（A6）。
「reconcile」在可执行层面就是它的四条命令序列——`plan` 不新增命令，也不假装存在一个 `--action reconcile`。
**收敛判据是 `converged`，不是 `clean`**（两个谓词的定义点：`diagram-obligation.contract.md` `C-013`；
收敛判据的用法：`C-008a` R6）。`converged` 的算式**不在本文件复述**——它的唯一定义点是 `C-013`
（合取项含 `judged_scope_has_carrier`）；`clean` 更严格（`exempted>0 ⇒ clean=false`，同条 `C-013`）。

| 步 | 命令（`--root` 指向夹具空间的 `tmp_path` 副本） | 期望 |
|----|--------------------------------------------------|------|
| 首次 R6 | `docs-utils.py --action obligation --root <fixture>` | 每份无图文档一条 `missing` / `no-diagram-reference`；`converged=false`、`clean=false` |
| R5 产图 | 按 `C-008a` 调 `draw-diagram` 前门产出两面 + 引用 + 同轮记录（夹具里由测试替身写出与 `clean/` 同构的记录与文件） | 该文档 verdict 变 `satisfied` |
| 二次 R6（全产图） | 同第一条命令 | `missing` / `stale` / `not_evaluated` 三档全零 ⇒ **`converged=true`**；`exempted=0` ⇒ `clean=true` |
| 二次 R6（含豁免夹具 `exempt-ok/`） | 同第一条命令，`--root` 指向带一份有效豁免记录的夹具 | `missing` / `stale` / `not_evaluated` 三档全零 ⇒ **`converged=true`**，而 `exempted=1` ⇒ **`clean=false`**——**这是合法终态**（`FR-004` / `SC-008`：无结构可绘的具名豁免即「已收敛」），MUST NOT 被判成未收敛 |
| 反 churn | `git status --porcelain <fixture>` | 空（第二次运行零写，`C-002`） |

**判据的可达性说明**：`D-001`（图文语义面）**不在这条回路的收敛目标内**——它由评审面承接，
因此 S9 的「零 finding」只指 `converged` 的三档全零，MUST NOT 被读成「图文语义也一致」，也 MUST NOT 被读成
`clean=true`（带豁免的空间 `clean` 恒为假）。这两句同样写在 `D-001` 的登记行里。
