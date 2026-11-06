# Research — 087 架构图为核心的文档空间

**Feature**: 087 | **Date**: 2026-11-06 | **Stage**: plan (Phase 0)

本文件回答「设计之前必须先量清的六件事」。每条给出**实测命令 / 读数**与**裁决**；裁决若改变规格的读法，
在 `plan.md` § Decision Tensions 留承重记录。全部读数在 base `24cb4edc` 的工作树
`<worktree>/.specify/specs/087-arch-diagram-docs/` 上取得，命令可直接复核。

## R1 — 既有文档检查器的形态先例（A4 的输入）

**问题**：配套图检查器应扩展 `docs-utils.py`，还是另起一个脚本 / 一个既有检查器的新动作？

**实测**：

```text
wc -l skills/external/create-docs/scripts/docs-utils.py   -> 437
grep -n 'choices=\[' skills/external/create-docs/scripts/docs-utils.py
  -> choices=["scan","expire","clean","archive-check","stats","validate","fix-links","audit"]
wc -l .specify/scripts/python/doc-consistency-check.py     -> 1600+（069a 检查器）
grep -n 'STRUCTURE_ACTION\|FACES =' .specify/scripts/python/doc-consistency-check.py
  -> FACES = ("reader","evidence","duplicate","count")；STRUCTURE_ACTION = "structure"
```

两个先例的方向**相反**，但分界线清楚：

- 033 的 `docs-utils.py` 把「文档空间自查」的动作（validate / scan / audit …）收在文档技能自己的引擎里；
- 069a 的 `doc-consistency-check.py` 把「跨产物一致性」立成**独立脚本**——因为它有**第二组调用方**
  （`/speckit.docs` 命令面 W1、`create-docs` 技能面 W3、`/speckit.humanize` W4 与七个阶段命令），
  把它塞进任何一个技能引擎都会让另一个调用方去依赖该技能的私有脚本。

**裁决（供 T-002 采纳）**：按**调用方形态**选，不按「先例像谁」选。本特性的检查器只有一个调用方族——
`skill:create-docs` 的 R6 验证与 Authoring Flow R6（见 R2 的调用点表），调用方与 033 的
`docs-utils.py` 完全同形（文档技能自己的验证步骤）。因此**扩展 `docs-utils.py` 的一个新动作**，
不新增顶层脚本、不在 069a 检查器上加第六面。反题与代价见 T-002。

## R2 — 义务接线面的实测位置与既有守卫的约束力

**问题**：A7 的四条既有守卫具体钉住什么？改动落点在哪里才逐条保持绿？

**实测（2026-11-06，本工作树）**：

```text
python3 -m pytest tests/contract/test_expression_gate_wiring.py \
                 tests/contract/test_docs_command_template.py \
                 tests/contract/test_directory_governance.py -q
  -> 75 passed（含 test_confirmation_gates_sweep 除下条外的全部用例）
python3 -m pytest tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target -q
  -> FAILED：AssertionError: SC-002 target missed: residual 27 > 25% of baseline 93
     （**先于本特性存在的漂移**，见 R6 的基线读数；`stop-and-confirm` 那条 KEEP_LIST 断言在本轮为 pass）
```

| 守卫 | 钉住的字面量 / 结构 | 对本特性的约束 |
|------|--------------------|----------------|
| `test_expression_gate_wiring.py` A1 | `## Outline` 内**恰好入口小节**的接线块含 `flow-class-check.py`、`--action lookup`、`"/speckit.docs"`、两个 owner 路径、`doc-consistency-check.py`；且 `## Outline` 与 `## Wrap-up` 之间的位置固定 | 新内容 MUST 落在 `## Outline` 的既有分派小节或**之后新增的一节**，MUST NOT 改动 W1 小节 |
| 同上 A3 | `skills/external/create-docs/SKILL.md` 的 `doc-consistency-check.py` 提及 MUST 位于**含 `R6` 的章节** | R6 与 Authoring Flow R6 的接线文字 MUST 保留在各自章节内 |
| 同上 A5 | 接线块去掉路径后 MUST NOT 出现独立词 `expression` / `execution`，也不得出现「属表达类」类断言 | 新增接线文字 MUST NOT 复述类别词（只引 owner 路径） |
| `test_docs_command_template.py` C4a | `skills/external/improve-docs/SKILL.md` 字面量必须在 `templates/commands/docs.md` 内 | 重写 `## Outline` 时该指针 MUST 原样保留 |
| 同上 C3 | 顶层章节序列 MUST 恰为 `## User Input` / `## Glossary` / `## Outline` / `## Wrap-up` / `## Handoffs` | MUST NOT 新增顶层章节 |
| `test_confirmation_gates_sweep.py` KEEP_LIST:71 | `templates/commands/docs.md` 必须含 `stop-and-confirm` | 改写分派小节时 MUST 保留该词 |
| `test_directory_governance.py` | `docs/concepts/documentation-model.md` 必须出现在目录治理 owner 的 area-map 清单 | 该文件**保留在盘、保留路径**，本特性只追加读者面段落 |

调用点侧：`shared/workflow/expression-gates.md` § 调用点表把 `skill:create-docs` 的时点写作
「Reconcile Loop 的 R6 verify 与 Authoring Flow 的 R6 验证（两处）」——本特性的检查器**恰好挂在同一两处**，
不需要扩面（FR-017 的「由既有验证步骤触达」因此不新增调用点，属最小接线）。

## R3 — 反射面（渲染产物 ↔ 源）判据的机器信号

**问题**：FR-014 的 `stale` 第一半「图的两个面彼此不一致」能否用**无第三方依赖**的信号判定？

**实测**：`skills/external/draw-diagram/references/delivery-contract.md` § D2 的源 / 渲染产物扩展名表
（`plantuml .puml→.svg+.png`；`mermaid .mmd→.svg+.png`；`excalidraw .excalidraw→.svg+.png`；
`drawio .drawio→.svg|.png|.pdf`；`d3js` / `echarts` 源即 `.html`）。仓内无 PNG/SVG 内容的解析器，
且 `pyproject.toml` 的 `requires-python >= "3.8"` 与「新增脚本 stdlib-only」（RS-001）排除了引入图形库。

**裁决**：`stale` 第一半取**两种信号，任一成立即 stale**（具体取值域与判定规则冻结在
`contracts/diagram-obligation.contract.md` C-008）：
① 渲染产物 mtime **早于** 源文件 mtime（源改过而没再渲染）；
② 产生方运行的追溯记录里 `rendered[].sha256` 与盘上实际文件的 sha256 **不等**（图被手改过）。
两者都只是在盘事实，不需要解析二进制；「渲染器重跑后字节不同但语义相同」不属本判据，MUST NOT 被报成 stale
（每次真实重渲染都会刷新 ②，因为记录由产生方运行重写）。

## R4 — 文档侧判据的机器信号

**问题**：FR-014 `stale` 第二半「图与文档就同一事实不一致」在只读 + 无语义模型的情况下能判到什么程度？
A12 明确要求 plan 给不出可判据时**如实登记为该面未覆盖**，不得留一条无判据的 verdict。

**实测**：

- 文档正文是 Markdown，图的源是可编辑文本（`.puml` / `.mmd` / `.drawio` XML / `.excalidraw` JSON / `.html`）。
  仓内没有任何机制把图内标签抽出来与文档正文对齐；`draw-diagram` 的 LDM **只存在于产生方运行的 SDS 文件**里，
  而 FR-015 禁止检查器写这类摘要，读一份产生方留下的 SDS 又会在它缺失时把干净空间判脏（见 R4 反例）。
- 反例构造：一个项目的手工图 `.drawio` 从没有 SDS 落盘（本特性之前产生的图即如此）。若判据依赖 SDS，
  该图会被判 `not evaluated` 或 `stale`——两种都是假红。

**裁决**：`stale` 第二半**只冻结可判的最小面**：文档对渲染产物的**引用仍在**且**解析**（否则不是 stale，
是 `missing`／`reference-unresolved`）；「图内容与文档语义一致」**本特性不判定**，逐面登记为
`criterion: doc-face 未覆盖（residual-risk D-001）`，并由评审面承接（`draw-diagram` 的能力边界本来就是
「结构通过 ≠ 事实正确」，规格 § Edge Cases 同句）。理由是判据必须先可判、再可加严；登记覆盖缺口比
发明一条不可判的 verdict 诚实，正是 A12 允许的第二条路。

## R5 — 最小夹具的代价（FR-023 负向可观测的前置）

**问题**：`tests/fixtures/` 里造一个「文档 + 图两面 + 追溯记录」的空间要花多少，能否在无渲染后端的环境里跑？

**实测**：夹具不需要真渲染。`docs-utils.py` 的新动作只读在盘文件（存在性、mtime、sha256、引用解析），
所以夹具可以是**三行文本文件 + 一个 1×1 PNG**。R2 的实测显示本机**没有** `pytest` / `typer`（`ModuleNotFoundError`），
渲染后端 `xuanji-render.aliyun-inc.com:9697/healthz` 的可用性也没有声明 pin（RS-004 已把它记为环境特定）；
负向夹具因此 MUST NOT 依赖渲染，MUST NOT 依赖网络。

**裁决**：新增三段夹具（`clean` / `missing-face` / `stale-source`）+ 一段豁免夹具，全部纯文件；
负向断言用**删除一个面**的方式构造，不使用渲染后端。

*（Phase 1 修订，attempt 2）* 「`missing-face` 一段夹具」在流程上不可复检：删除发生在同一个夹具上，
第二次运行就测不到「删除前的绿灯」，而且 `C-016` 的落档顺序决定了缺失的两面**各需一段独立夹具**
（否则量到的是「哪个真在前」而不是「这一面被判成什么」）。因此最终的夹具集是 `data-model.md` E6 的
**11 段**（8 段判定 + 3 段豁免），删除动作一律发生在 `tmp_path` 的副本上。R5 的**结论**未变
（纯文件、不依赖渲染、不依赖网络）；变化的只是**段数**，且是纠正（同一判据下唯一可复检的读法），不是新裁决。

## R6 — 基线读数（本特性必须「零新增」，而不是「全绿」）

**实测（2026-11-06，本工作树；解释器 3.11.13；`pytest 9.2.0` 取自一次性 scratch venv）**：

```text
python3 -m pytest tests/contract -q          -> 6038 passed, 17 failed, 2 skipped (289.58s)
python3 scripts/python/sync-mirrors.py --check   -> EXIT 0 仅在能 import typer 的解释器下成立
                                                      （裸 python3 → exit 2「DRIFT detected」，见 R6 推论 1）
python3 scripts/python/regen-command-copies.py --check -> OK: all per-tool command copies match
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
        --spec-dir .specify/specs/087-arch-diagram-docs --stage requirements
  -> decision=pass errors=0 advisories=0（fr=23 sc=10）   ← requirements 时点读数
     Phase 1 落盘后复跑：advisories=38（全部同型 missing-path，指向实施期才存在的路径），errors 仍 0
python3 .specify/scripts/python/doc-consistency-check.py --action structure \
        --spec-dir .specify/specs/087-arch-diagram-docs
  -> status: not-applicable（class=execution）
```

两条口径推论：

1. **`sync-mirrors.py --check` 用裸 `python3` 会假红**：它内嵌调用 `regen-command-copies.py`，后者
   `import specify_cli` → `import typer`。裸 `python3` 无 `typer` 时报 traceback，`--check` 因此退出 2，
   即使六对镜本身全部 `ok`。实施阶段 MUST 用能 import `typer` 的解释器（仓内无 `.venv`，一次性 scratch venv 即可）。
2. **基线里已有 17 条 failed**，其中 `test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`
   与本特性相关面（SC-002 分母 93 / 残余 27）而**先于本特性存在**。镜像与测试的判据因此 MUST 写成
   「相对基线无**新**漂移 / 无**新**失败」，而不是退出码 0。

## R7 — 名册与冻结面的实测（A7 裁定的依据）

```text
grep -n "WIRING_TEMPLATES\|WIRING_SKILLS" tests/contract/test_expression_compatibility.py
  -> WIRING_TEMPLATES = ("docs.md","humanize.md")；WIRING_SKILLS = ("skills/external/create-docs/SKILL.md",
     "skills/external/humanize/SKILL.md")
grep -c "" .specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt  -> 74
grep "  skills/external/improve-docs/SKILL.md$" ...pre-change-file-hashes.txt
  -> f77ec5f4…（与当前盘上文件同哈希 ⇒ 尚未漂移）
```

- `skills/external/create-docs/SKILL.md` 与 `templates/commands/docs.md` **不在** 74 条冻结清单内
  （它们是 069a 的 W1/W3 接线面），因此改它们**不**需要 `ALLOWED_POST_BASELINE_CHANGES` 条目；
- `skills/external/improve-docs/SKILL.md` **在**清单内且当前未漂移，改它就必须追加
  `ALLOWED_POST_BASELINE_CHANGES` 条目（reason + markers 二元组，同 071/072/081d/084/085 先例）；
- 契约侧另有一条硬约束：`ALLOWED_POST_BASELINE_CHANGES` 的每个 key MUST 是 manifest 条目，
  否则本条被断言判为 vacuous——因此 `docs/concepts/documentation-model.md`（不在 manifest，也不在
  `test_c5_untouchable_framework_paths_are_unchanged` 的 `src/`、`AGENTS.md`、`.specify/instructions.md` 三路径内）
  **不能也不需要**登记。
