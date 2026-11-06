# Implementation Plan: 087 架构图为核心的文档空间

**Branch**: `line/087-arch-diagram-docs` | **Date**: 2026-11-06 | **Spec**: [`.specify/specs/087-arch-diagram-docs/requirements.md`](./requirements.md)
**Requirement → Feature**: `087-arch-diagram-docs` → Feature 087 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space）
**Input**: Specification from `.specify/specs/087-arch-diagram-docs/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command, which **replaces** every `[PLACEHOLDER]` token in place — it MUST NOT append a second copy of this template below the filled content. See the `/speckit.plan` command for the execution workflow.

## Summary

规格的核心要求是一句话：**一份正式文档合规的必要条件里，加上「它配套的架构图」**，并且这件事由**既有的两条文档流程**保证、由**一个确定性只读检查**判决，而不是新增一个命令或一套绘图能力（FR-001…FR-004、FR-017、FR-011）。

技术路线（全部由 Phase 0 实测确定，见 [`research.md`](./research.md) R1–R7）：

1. **义务的定义点只有一个**：`skills/external/create-docs/SKILL.md` § Desired-State Baseline 追加一条基线条目。载体集合是「六类正式目录内的文档 + 根 `ARCHITECTURE.md`」（A11），其余保留根文件只承指针义务。
2. **检查器形态按调用方选**（T-002）：给 `skills/external/create-docs/scripts/docs-utils.py` 加一个 `--action obligation`，因为它与 `skill:create-docs` 的两处 R6 验证同形、同引擎；不另起顶层脚本，也不给 `doc-consistency-check.py` 加第六面。
3. **判据冻结在契约**：[`contracts/diagram-obligation.contract.md`](./contracts/diagram-obligation.contract.md) 拥有命令面、封闭 verdict/reason 集、**逐文档判定的有序优先级（`C-016`）**、`stale` 逐面判据、追溯记录与豁免记录 schema；所有其他面按路径引用它，不复述取值。
4. **能力零新建**（T-004）：`draw-diagram` 只被引用、一行不改；文档侧不出现第二个引擎、第二份路由表或第二份交付契约。
5. **诚实的能力边界**（T-003 / D-001）：`stale` 的第二半「图与文档就同一事实不一致」只判到「引用仍在且解析」，语义一致性**显式登记为未覆盖**，不发明一条没有判据的 verdict——这是 A12 自己给的第二条路。
6. **收敛责任在 reconcile 之内**（P1-5）：`flow-obligations.contract.md` 的 `C-008a` 把 Reconcile 的 R3/R4/R5/R6 各追加一步，使 `missing` / `stale` / `not-evaluated` 成为**可被这一轮 reconcile 收敛掉的差异项**——产图与重渲染由既有 `draw-diagram` 前门在 R5 内完成（safe local writes，不加确认档），`not-evaluated` 不跳过，`D-001` 的语义面在报告里显式点名且**不**属收敛目标。没有这条路径，`SC-003` 的「收敛后二次运行零图 finding」在文本上不可达。**收敛判据是一个独立的 `converged` 谓词**（`diagram-obligation.contract.md` `C-013`：`judged_scope_has_carrier && 三档全零`，豁免不参与），与严格的 `clean`（`exempted>0 ⇒ clean=false`）分开：具名豁免是 `FR-004` 的合法终态，用 `clean` 当收敛判据会让这类文档永远不收敛，收敛因此没有唯一读法。
7. **图的落点只有一个**（T-005）：`docs/assets/<slug>.<ext>`，源与渲染产物同处，文档用相对引用指向它；与 `flow-obligations` `C-009`、`diagram-obligation` `C-010` 的示例、`data-model.md` E6、`quickstart.md` S3 同源。

## Technical Context

**Language/Version**: Python 3（`pyproject.toml` 已声明 `requires-python >= "3.8"`，本次不新增 pin）；新增代码 stdlib-only（`argparse` / `json` / `os` / `hashlib` / `re`），不引入第三方依赖（RS-001）。
**Primary Dependencies**: 无新增运行时依赖。门禁侧沿用既有 `tests/contract/` 的 pytest 套件；镜像侧沿用 `scripts/python/sync-mirrors.py` 与 `scripts/python/regen-command-copies.py`（后者 `import specify_cli` → `import typer`，需能 import typer 的解释器，裸 `python3` 会假红）。
**Storage**: 文件系统即存储。三类在盘事实：载体文档（`docs/**` + 根 `ARCHITECTURE.md`）、图的两面（源 + 渲染产物）、两份记录（追溯记录 `docs/.speckit/runs/`、豁免记录 `docs/.speckit/exemptions/`，均为既有 `docs/.speckit/` C 区机器目录下的新子目录）。
**Testing**: `tests/unit/test_docs_utils_obligation.py`（新增，封闭集 / 优先级 / 只读 / 确定性断言）+ `tests/integration/test_docs_obligation_scenarios.py`（新增，夹具空间的端到端场景与 `tmp_path` 删除动作）+ `tests/fixtures/docs-obligation/**`（十一段纯文件夹具，零渲染、零网络）+ 既有六条契约守卫保持通过。映射见 § Test Plan；基线口径见 § Technical Constraints 与 § Baseline & Known-Red。
**Target Platform**: 任意 POSIX 文件系统（`os.stat` 的 mtime 与 `hashlib.sha256` 是唯一机器信号，无图形解析、无网络）。
**Project Type**: 文档 / 提示框架仓（Two Hats：改 `skills/` `templates/` 的框架源，`.specify/` 与四家 per-tool 副本由生成器同步；`docs/` 的内容工作不属本特性）。
**Performance Goals**: 不设指标。检查器只做一次目录遍历 + 每个图的两次 `stat` / 一次 sha256，载体规模是本仓 **85** 份量级（`quickstart.md` S2 的实测；根 `ARCHITECTURE.md` 是本仓尚不存在的载体，基线第 1 项登记其**语义**，不是盘上事实）。
**Constraints**: 检查器 MUST 只读（允许的副作用集合是空集）、确定性（两次运行字节可比）、幂等；MUST NOT 新增 `/speckit.*` 命令；MUST NOT 改动 069a 的四字面量与 W1/W3 接线小节；MUST NOT 改本仓 `docs/` 内容。
**Scale/Scope**: 5 处文本落点 / 4 个文件（`data-model.md` E7 的五行；`create-docs/SKILL.md` 的两个小节族同属一个文件）+ 1 个引擎动作 + 2 份记录 schema + 11 段夹具；85 份载体文档的实测人口（`quickstart.md` S2）。

### Technical Constraints（实施期 MUST 保持）

| 约束 | 来源 | 判据形态 |
|------|------|----------|
| 只读 | FR-015 / 契约 `C-002` | 允许副作用集合为空集；`git status --porcelain` 在检查后为空 |
| 确定性 + 幂等 | FR-015 / 契约 `C-006` | 两次运行输出 `cmp` 相同 |
| 封闭 verdict / reason 集 | FR-016 / 契约 `C-004`、`C-005` | 第六个值即契约违规，由 `tests/unit/test_docs_utils_obligation.py` 逐值断言 |
| 逐文档档位唯一 | 契约 `C-016` | 每个夹具文档的 `verdict`/`reason` 与九行优先级表一致（`orphan-*` 两值不得互换） |
| 无新命令 | FR-017 | `git diff --name-only 24cb4edc...HEAD -- templates/commands/` 只出现 `docs.md` |
| 守卫保持通过 | A7 / 契约 `C-014` | 五条具名守卫**相对基线无新失败**（基线见 § Baseline & Known-Red） |
| 镜像无新漂移 | 模板 § Mirror Obligations | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对基线 exit 0，需能 import `typer` 的解释器 |
| 本仓 `docs/` 仅一处改动 | requirements § Out of Scope / A6 + FR-001 | `git diff --name-only 24cb4edc...HEAD -- docs/` 的结果**恰为一行** `docs/concepts/documentation-model.md`（FR-001 要求的读者投影，T064 交付）；该目录下任何第二行即违约 |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

<!--
  ACTION REQUIRED for /speckit.plan:
  Do NOT hard-code principle names here. Instead, read `.specify/memory/constitution.md`,
  enumerate every heading matching `### <roman-or-arabic-numeral>. <name>` (e.g.
  `### I. Template-First Architecture`, `### IV. Test-First Development`), and render
  ONE row in the table below per principle in the exact order they appear in the
  constitution. Include the principle's NON-NEGOTIABLE / MANDATORY annotation verbatim
  when present. This avoids the drift documented in the constitution's Sync Impact Report.

  Each row must contain:
  - Principle (verbatim heading without the leading `### N.`)
  - Compliance ("✅ Pass" / "❌ Fail" / "⚠ Partial — see Complexity Tracking")
  - Evidence (one-line citation pointing at the design artefact that demonstrates compliance)
-->

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计裁决回溯到 FR：`contracts/diagram-obligation.contract.md` 头部 `FR served` 列了它所服务的 10 条 FR；`contracts/flow-obligations.contract.md` 的 A–F 组逐条映射 FR-001…FR-023；§ Test Plan 的 clause→test 表把每条契约条款落到一条断言 |
| II | Feature-Centric Development | ✅ Pass | 绑定既有 Feature 087（reuse-first 五候选复核见 `requirements.md` § Related Feature）；本阶段把 087 从 `Draft` 推进到 `Planned` 并同步 `features.md` 与 `features/087.md` |
| III | Intent-Driven Development | ✅ Pass | § Decision Tensions 的 5 条记录把每个「怎么落到工件」的取舍写成可独立采纳的反题 + 判别证据 + 重开条件；`research.md` 的 R1–R7 只给测量与裁决，不直接生成代码 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 契约先行（`contracts/` 两份已落盘）→ 再实现；§ Test Plan 的 clause→test 表给每条 `C-NNN` 一条具名断言或具名守卫，`tests/fixtures/docs-obligation/**` 与 `tests/unit/test_docs_utils_obligation.py` 在 `quickstart.md` S3–S5 定义了先行的负向断言（FR-023 的「主体坏了必须红」） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent、不改 `agents/`；义务落在既有技能与既有命令模板的文本上，窗口在 `data-model.md` E7 逐行列明 |
| VI | Continuous Quality & Observability | ✅ Pass | FR-022 的四项证据（源路径、渲染面路径、文档引用、追溯记录）落在运行报告；`test-evidence/` 记录本阶段的实测读数与机器可读的 `plan-stage-status.jsonl` |
| VII | Specification-Plan-Task-Implementation Workflow [NON-NEGOTIABLE] | ✅ Pass | 本阶段产物即 Phase 0（`research.md`）+ Phase 1（`data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`）；Feature 状态只走 `Draft → Planned`，**不退化为 Implemented**（无 open task、无 `verification.log`，Pre-Status-Flip Gate 未满足且本阶段不试图满足） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 检查器的行为以 `docs-utils.py` 的实现在盘为准；`data-model.md` 与契约只登记接口与取值域，不复述实现细节；`quickstart.md` S1 记录**当前**动作表用 `argparse` 拒绝未知动作的实测输出（单行原文），而不是凭记忆写 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 不新建引擎 / 渲染器 / 命令 / 确认分级 / 目录族（FR-011、FR-017、FR-018、T-004、T-005）；新增面无第三方依赖；`C-012` 把「引擎不可用」排除在检查器判据之外——引擎可用性不归检查器判 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 不新增保留根文件名、不改其注册位置（FR-002）；图的落点沿用 `docs/assets/`（T-005，先例 `docs/assets/quickstart-workflow.*`），两份记录的落点是既有 `docs/.speckit/` 机器目录下的 `runs/` 与 `exemptions/` 两个 lowercase 子目录，`data-model.md` E4/E5 与 `C-010`/`C-011` 同源 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已显式点名：本特性改框架源（`skills/` `templates/`），`.specify/` 与四家 per-tool 副本由 `sync-mirrors.py` / `regen-command-copies.py` 生成（§ Mirror Obligations 逐行登记）；本仓 `docs/` 内容工作被 § Out of Scope 排除，`quickstart.md` S8 以空 diff 为判据 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 图的产生一律走既有 `draw-diagram`（FR-011、T-004），MUST NOT 另写绘图/渲染代码；检查器复用既有文档引擎 `docs-utils.py` 而非另起脚本（T-002） |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 本特性强化 **Change Validation** 维度：图从「作者记得画」变成「既有验证步骤判得出」，且负面可观测（FR-023）。目标模型引 `shared/guidelines/better-harness.md`，不另立维度或评分 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 义务定义点唯一（Baseline 一条）；检查器取值域唯一（`contracts/diagram-obligation.contract.md`，含 `C-016` 的逐文档优先级）；图的落点唯一（`flow-obligations` `C-009`，实施期落脚到本特性**新建**的 Baseline `#### Assets` 小节——该小节当前不在盘，见 `flow-obligations.contract.md` 头部的读法说明）；`docs/concepts/documentation-model.md` 只做读者投影；`data-model.md` 与 `quickstart.md` 头部均写明「不复述取值域」。`checklists/requirements.md` 的派生计数副本**不改写、只登记**（`OI-087-01`），处置归 `/speckit.checklist` |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 新增 finding 的输出面向未参与运行的人：每份文档带路径与闭集理由（FR-016），`C-005` 给每个 reason 一句自然语言含义；`C-013` 的 `clean` 是显式结论而不是空输出。基准读者取自 `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议，不另定义 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 「主体坏了检查仍绿」被明确定义为**未验证而非通过**（FR-023 / `C-013` 的 `carriers == 0 ⇒ clean=false`）；`exemption_superseded` 把「豁免理由已失效」作为可见事实报出（FR-004）；本阶段的两处纠正（`reference/ 64` 的载体普查订正、`orphan-*` 两值的面序订正）已在 § Decision Tensions 与 `quickstart.md` 就地披露 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | 不新建顶层目录；两个新子目录（`docs/.speckit/runs/`、`docs/.speckit/exemptions/`）的含义在本特性契约 `C-010`/`C-011` 处登记，且**不是**新的顶层或新的目录族——`docs/.speckit/` 已是基线登记的机器目录；`docs/assets/` 已存在（本阶段 `find` 实测）。`test_directory_governance.py` 保持通过（`C-014`，基线 21 passed） |
| XVIII | Grounded Naming | ✅ Pass | 动作名 `obligation` 取自规格自身的验收判据措辞（`requirements.md` § User Story 2 独立测试：「the diagram obligation」）——它是本规格自己的措辞，不是外部术语，因此本计划**不**宣称它来自某个仓内既有词表；记录名 `diagram-trace` 取自 FR-013 的 traceability；`exempt-*` 三值取自 FR-004 的 exemption。三个名字都在规格正文有出处，无自创同义词 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | 用户看到的红是「哪份文档、缺哪个面、属于闭集里的哪个理由」（`C-005` 的 `path` + `line` + `reason`，其中面由 `orphan-rendered` / `orphan-source` 两值区分）；不需要打开检查器源码。提升的信息维度是「文档空间的图完整性」，落地机制是既有 reconcile 机制（`shared/patterns/reconcile-pattern.md`，`flow-obligations` `C-008a`），不新增第四种机制 |

**Gates Status**: ✅ All gates pass — 19/19 `Pass`，无 `Fail`、无 `Partial`，因此 `## Complexity Tracking` 为 `N/A`。

**Re-check after Phase 1**: 2026-11-06 — Phase 1 产物（`data-model.md` / `contracts/` 两份 / `quickstart.md` / `feature-ref.md`）落盘后逐行复读本表：XIV 的「单一定义点」由契约 `C-004`/`C-005` 的封闭表证明；XVII 的目录登记由 `data-model.md` E4/E5 的落点行证明；XVI 的负面可观测由 `quickstart.md` S3 的两条实测预期证明；XI 的两顶帽子由 § Mirror Obligations 的 4 个源文件 → 镜像/副本矩阵证明。逐条结论不变，无新 `Partial`。

## Decision Tensions

*Owner of the record shape, the admissibility criteria, the rejection forms and the load-bearing
threshold: `.specify/shared/guidelines/decision-tension.md` — one pointer, read from the repository
root (the same form this template uses for `.specify/memory/constitution.md`); a plan artifact lives
under `.specify/specs/<key>/`, so a plan-directory-relative link would resolve to a path that does
not exist. This section lists the field names and points at that file — it MUST NOT restate the
criteria table, the rejection list or the threshold table.*

Fields: `decision`, `antithesis`, `binding_constraints` (with `pole_a` and `pole_b`),
`discriminating_evidence`, `expected_sacrifice`, `revision_trigger`; record identifier `tension_id`
(`T-NNN`).

Every record is carried by a level-3 sub-section whose heading begins with `T-NNN`
(e.g. `### T-001 — <one-line title>`), and its six fields are written in the owner's shape.

本计划含 5 条承重决策（T-001…T-005）。`requirements.md` 显式移交 plan 的三条（A7 冻结基线处置、A4 检查器形态、`stale` 逐面判据）各占一条；另两条是义务落地的形态选择（图的落点、能力复用的边界）。

### T-001 — A7 冻结基线的处置：追加一条 allowlist 条目，不另立本特性自己的基线记录

- **decision**: 改 `skills/external/improve-docs/SKILL.md` 时，在同一提交里向 `tests/contract/test_expression_compatibility.py` 的 `ALLOWED_POST_BASELINE_CHANGES` 追加一条 `reason` + `markers` 条目，与 071/072/081d/084/085 的先例同形；MUST NOT 另建本特性自己的冻结基线文件。
- **antithesis**: 另立本特性自己的基线记录（例如在 `.specify/specs/087-arch-diagram-docs/notes/` 下新建一份 `post-baseline-changes.txt`，登记本次改动的哈希与理由）；当 069a 的冻结基线被多处并行特性同时触碰、且每次追加都要在共享文件里制造冲突时它更优——各特性互不争用同一个文件。
- **binding_constraints**:
  - pole_a: 基线只有一份，任何「这条改动被允许」的裁决 MUST 落在既有守卫能读到的那一处，否则守卫仍是红的而理由躺在别处。
  - pole_b: 并行特性 MUST NOT 因为共用一份登记文件而互相阻塞或互相覆盖。
- **discriminating_evidence**: 在改动 `improve-docs/SKILL.md` 后跑 `python3 -m pytest tests/contract/test_expression_compatibility.py -q`，看 `test_c5_non_wiring_files_keep_their_frozen_hashes` 是否由红转绿且 `test_c5_...` 的「每个 allowlist key 必须是 manifest 条目」断言同时通过；结果二值：绿 / 不绿。
- **expected_sacrifice**: SC-009 Source ↓ 本特性的改动理由是「被登记后放行」，不是「基线本身被修订」——069a 冻结清单的条目数不变，但该文件的内容按本特性的标记增长；若后续特性也改同一文件的同一段，会产生一次合并冲突（可机械解决）。
- **revision_trigger**: 若同一迭代内出现 ≥2 个特性都需要在同一 `ALLOWED_POST_BASELINE_CHANGES` 里追加 `skills/external/improve-docs/SKILL.md` 条目（即该文件的改动开始成为常态）→ 重开，改为把该文件提升进 `WIRING_SKILLS`（那是 069a 的 owner 的修订，不是本特性的）。

### T-002 — 检查器形态：扩展 `docs-utils.py` 的新动作，不新增顶层脚本

- **decision**: 配套图检查落成 `skills/external/create-docs/scripts/docs-utils.py --action obligation`；不新增顶层脚本，不给 `doc-consistency-check.py` 加第六面。
- **antithesis**: 另起一个独立脚本（例如 `scripts/python/diagram-obligation-check.py`）；当检查器需要第二个调用方族（例如 `/speckit.docs` 命令面也要独立调用它），或它的判据会与技能的私有引擎演化为两条独立的演进线时它更优——独立脚本不会被某个技能的内部重构带走。
- **binding_constraints**:
  - pole_a: 一个技能自己的验证步骤 SHOULD 用该技能自己的引擎，否则每次引擎重构都要跨技能改路径。
  - pole_b: 一个被多个调用方族消费的检查 MUST 独立成脚本，否则其他调用方要依赖某个技能的私有脚本。
- **discriminating_evidence**: 读 `shared/workflow/expression-gates.md` § 调用点表里 `skill:create-docs` 一行，看本检查器的调用点数量；结果二值：只有该技能的两个 R6（选扩展动作）／存在第二个调用方族（选独立脚本）。
- **expected_sacrifice**: SC-006 Source ↓ 检查器与 `validate` 同一进程、同一 `--root` 口径，因此单次运行的入口只有一个；代价是该动作的演进绑在 `create-docs` 技能的发布节奏上，无法独立发版。
- **revision_trigger**: 当出现第二个调用方族（例如 `/speckit.docs` 的 W1 直接调用它，或 humanize 流程需要它）→ 重开，按 069a 的形态抽成顶层脚本并把两处调用点改为引用它。

### T-003 — `stale` 第二半（图与文档就同一事实不一致）：冻结可判的最小面，把语义面登记为未覆盖

- **decision**: `stale` 按 A12 取并，但**第二半只判「文档对渲染产物的引用仍在且解析」**；「图内标签 / 关系与文档正文所述事实一致」本特性不判定，逐面登记为残差 `D-001`，由评审面承接。
- **antithesis**: 引入语义判据（例如要求产生方运行的 LDM 摘要入库、再与文档正文做标签对齐）；当图库已普遍有 LDM 落盘、且团队愿意把「图与文对齐」当作可自动判定的维度时它更优——那会把 `stale` 从「半个判据」变成完整判据。
- **binding_constraints**:
  - pole_a: verdict MUST 有判据；一条无法判定的 verdict 比没有该 verdict 更坏，因为它会被读成「已检查」。
  - pole_b: 规格明确要求 `stale` 覆盖「图与文档不一致」，缩到一半必须可见，不能被读成完整覆盖。
- **discriminating_evidence**: 取一张本特性之前产生的手工图（无 LDM 摘要落盘），用两种实现各跑一次：依赖语义的实现必然把它判 `not-evaluated` 或 `stale`（假红），只判引用解析的实现判 `satisfied`；结果二值：语义实现是否产生假红。
- **expected_sacrifice**: SC-004 Source ↓ 改名类内容改进只判到「引用解析 + 两面在盘」，语义级失步（图里仍写着旧组件名、文档已改名）不会被机械报出，必须由评审面发现。
- **revision_trigger**: 当 `docs/.speckit/runs/` 的 LDM 摘要已覆盖 ≥ 大多数图（可由 `--action obligation` 的 `no-trace-record` 计数下降观察），或评审面连续两次报出「机械检查绿但图文语义不一致」的实例 → 重开，把语义判据补进 `C-009`。

### T-004 — 能力复用：`draw-diagram` 只被引用、零改动

- **decision**: 图的产生、渲染、引擎路由、交付验收一律走既有 `draw-diagram`，文档侧只引用它的路径与章节；MUST NOT 在 `create-docs` / `improve-docs` / `docs.md` 里重述引擎名、路由顺序或交付契约条目。
- **antithesis**: 在文档流程里内联一份「画什么图用哪个引擎」的简表；当文档流程的作者需要不经打开另一个技能就能决定引擎，且该决定与 `draw-diagram` 的实际路由长期一致时它更优——一次读取即可动手。
- **binding_constraints**:
  - pole_a: 引擎路由与交付契约 MUST 只有一个 owner，否则两处会各自漂移（宪法 XIV 的第 2 类合法重复之外没有余地）。
  - pole_b: 文档流程 MUST 可执行——作者要知道「这一步去调哪个能力」，指针必须落在他正在读的位置。
- **discriminating_evidence**: 在 `skills/` `templates/` `shared/` `scripts/` 里搜 `draw-diagram` 的路由矩阵行文（例如引擎层名与 tie-break 词的组合），看本特性是否引入第二份；结果二值：命中数 0 / >0。
- **expected_sacrifice**: SC-005 Source ↓ 文档侧读者要跨一次文件才能知道引擎怎么选；本特性的接线只能写「按 `draw-diagram` 的路由」，不能写具体引擎。
- **revision_trigger**: 当 `draw-diagram` 的路由表在两次发布内改变且文档侧的指针文字因此失效 ≥1 次 → 重开，改为在 `create-docs` 侧放一个**机器生成的**引擎清单（机械副本 + drift 检查），MUST NOT 手写。

### T-005 — 图的落点：全局 `assets/` 约定，不按类型目录分叉

- **decision**: 图的源与渲染产物一律落 `<root>/docs/assets/<slug>.<ext>`（本仓先例 `docs/assets/quickstart-workflow.{puml,svg,png}`），文档以内联或相对引用指向它（`../assets/x.png`）——**一个全局落点，一处约定**，落点本身由 `flow-obligations.contract.md` `C-009` 登记，实施期由本特性在 `skills/external/create-docs/SKILL.md` § Desired-State Baseline 内**新建**的 `#### Assets` 小节承接（该小节当前不在盘；建成后它才是 `assets/` 区域约定的 owner，MUST NOT 在写它之前被当成既有章节）。
- **antithesis**: 按类型目录分叉——每类正式目录下各建一棵 `diagrams/` 子树（`docs/concepts/diagrams/`、`docs/reference/diagrams/`…）；当图像散文一样需要「就近导出、就近浏览」、且某类目录的图与另一类的图从不同时被读到、需要各自独立的生命周期时它更优——读者不必跳出一个类型目录就能看到该类型的全部图，站点侧也能按 section 分别 mount。
- **binding_constraints**:
  - pole_a: 图的落点 MUST 只有一个约定，否则同一张图的两个候选家会让「引用解析到哪一份」依赖作者习惯，检查器无法给出稳定 verdict。
  - pole_b: 图 MUST 落在既有 taxonomy 内、不新建顶层文档类型目录（FR-002），因此「按类型分叉」也只能是既有目录的子树，不能是第七类。
- **discriminating_evidence**: `find docs -type d -name assets -o -type d -name diagrams`（工作树根）——结果二值：若仓内**已存在** `docs/assets/` 且**不存在**任何 `diagrams/` 子树（实测 2026-11-06：`docs/assets/` 在盘、`diagrams/` 计数 0）⇒ 沿用既有约定；反之则需登记新目录并走 Baseline 修订。
- **expected_sacrifice**: SC-009 Source ↓ 图没有按类型分区的导航入口；读者靠文档正文的相对引用找到图，「某一类目录的全部图」这种浏览方式不存在。
- **revision_trigger**: 当同一类型目录下的图数量增长到「一个 `assets/` 无法在一屏内列出」（可观测：`ls docs/assets | wc -l` 超过一屏阈值且按类型聚集明显）→ 重开，评估按类型分叉为 `docs/<type>/assets/`（**子目录仍是既有 taxonomy 内**）；若届时需要独立索引与生命周期，则升级为 Baseline 修订（那是 owner 的修订，不是本特性的）。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/[REQUIREMENTS_KEY]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command) — see note below
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md     # Implementation output (/speckit.implement command)
```

<!--
  research.md conditional guidance:
  Produce `research.md` as a standalone file when Phase 0 research exceeds ~50 lines
  or involves external source evaluation (API docs, vendor comparisons, benchmark data).
  When Phase 0 findings are brief (< 50 lines) and fully resolvable from internal
  investigation (project docs, constitution, existing code), inline them into plan.md
  under the `## Phase 0: Research Review` heading and note in this tree:
  "No standalone research.md — findings inlined below."
-->

### Source Code (repository root)
<!--
  ACTION REQUIRED:
  Document ONLY the directories actually changed or created by THIS spec, with a
  one-line purpose per directory. Do NOT invent a generic layout, and do NOT paste
  a "Single project / Web / Mobile" stub if it does not reflect this project.

  Examples of valid shapes (see `.specify/templates/examples/structure-*.md` if
  shipped, otherwise infer from the repo):
    - Single application:           src/, tests/
    - Web app:                      backend/, frontend/
    - Mobile + API:                 api/, ios/ or android/
    - Library / SDK:                src/<package>/, examples/, tests/
    - Monorepo:                     packages/<name>/, apps/<name>/
    - Container-image factory:      images/, script/snippets/, script/build/
    - Code generator / framework:   templates/, scripts/, src/<package>/

  If your project does not match any of these, document what is true. The goal is
  evidence-faithful structure, not adherence to a fixed taxonomy.

  MIRROR OBLIGATIONS: if any changed file has mirrors or generated runtime copies
  (dual-written template dirs, per-tool command copies, script mirrors), list EVERY
  copy explicitly in this tree — missed mirrors are the highest-frequency rework
  source during implementation.
-->

```text
.specify/specs/087-arch-diagram-docs/
├── plan.md                    # 本文件（/speckit.plan 输出）
├── research.md                # Phase 0：R1–R7 的实测与裁决
├── data-model.md              # Phase 1：8 个实体 + 2 个状态机
├── quickstart.md              # Phase 1：S1–S9 的命令与预期形状（每例自带 premises）
├── contracts/                 # Phase 1：两份契约（检查器面 / 流程义务面）
├── feature-ref.md             # Phase 1：Feature 087 绑定与 FR/SC 映射
├── test-evidence/             # 本阶段实测读数（既有目录）
└── tasks.md                   # Phase 2（/speckit.tasks 产出，本阶段不创建）
```

### Source Code (repository root)

```text
skills/external/create-docs/
├── SKILL.md                             # + § Desired-State Baseline 一条义务条目（并在该节内**新建** `#### Assets` 小节登记图落点，当前不在盘）；+ Reconcile R3/R4/R5/R6 与 Authoring R2,R5,R6 的接线
└── scripts/docs-utils.py                # + --action obligation（只读判定，见 contracts/diagram-obligation.contract.md C-001…C-016）

skills/external/improve-docs/
└── SKILL.md                             # + § Workflow 2–5 的 Diagram-sync 分类行与最小编辑/验证规则

templates/commands/docs.md               # + § Outline 的 `### 分派` 义务指针（W1 接线小节原样保留）

docs/concepts/documentation-model.md     # + 读者面投影一段（既有文档的追加，不新建文件）

tests/
├── unit/test_docs_utils_obligation.py           # 封闭 verdict/reason 集、C-016 优先级、只读、确定性、空载体判脏
├── integration/test_docs_obligation_scenarios.py # 夹具空间端到端：删除动作只发生在 tmp_path 副本上
└── fixtures/docs-obligation/            # clean / no-diagram / deleted-rendered / orphan-rendered / orphan-source /
                                         # stale-source / no-trace / trace-incomplete / exempt-ok / exempt-bad / exempt-superseded

tests/contract/test_expression_compatibility.py   # + ALLOWED_POST_BASELINE_CHANGES 一条（仅 improve-docs）
```

**Structure Decision**: 本特性落在**既有文档技能引擎 + 既有命令模板**之内，是一个「加动作 + 加文本 + 加夹具」的改动，**不新建任何顶层目录、不新建技能、不新建命令**。形态因此不是上面任何一个通用模板（single/web/mobile/library/monorepo），而是本仓惯用的「框架源 + 镜像运行时」双层：4 个源文件（`create-docs/SKILL.md`、`docs-utils.py`、`improve-docs/SKILL.md`、`templates/commands/docs.md`）+ 1 个既有文档（`docs/concepts/documentation-model.md`）承载全部行为改动，其余全是生成副本或测试。`skills/external/draw-diagram/**` 在交付树里**故意缺席**：它只被引用、一行不改（T-004），缺席就是「不交付」的登记。上面那段结构清单**只登记改动落点，不登记镜像副本**——每个被改文件的镜像与生成副本、以及各自的验证命令，逐行登记在紧接的下表 § Mirror Obligations，此处按单一定义点不复述。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

**基线（编辑前实测，2026-11-06）**：`regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.`（exit 0）；`sync-mirrors.py --check` → 六对镜全 `ok`（exit 0）。两条都必须用**能 import `typer` 的解释器**跑：`sync-mirrors.py` 内嵌调用 `regen`，裸 `python3` 会因 `ModuleNotFoundError: typer` 以 exit 2 假红，即使六对镜本身全 ok（research R6 推论 1）。**该解释器不由本计划创建**：本阶段的实测用的是执行者一次性建的 scratch venv `/tmp/087-toolenv/bin/python`（CPython 3.11.13 / `pytest 9.2.0` / `typer 0.27.3`）；换环境时按同一口径新建一个，文件不存在就如实记「前置条件未就绪」，MUST NOT 用裸 `python3` 的假红当漂移。因此本表每一行 `Verify` 的判据形态是**相对上述基线无新漂移**，不是「退出码 0」这一条绝对断言。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/create-docs/SKILL.md` | `.specify/skills/create-docs/SKILL.md`（`MIRROR_PAIRS` 第 2 对 `skills/external` → `.specify/skills`，扁平运行时层） | `$PY scripts/python/sync-mirrors.py --check` —— 相对基线无新漂移（本行 pair 不得新增 `drift`） |
| `skills/external/create-docs/scripts/docs-utils.py` | `.specify/skills/create-docs/scripts/docs-utils.py`（同一对的子路径） | 同上；另加 `diff -q skills/external/create-docs/scripts/docs-utils.py .specify/skills/create-docs/scripts/docs-utils.py` 无输出 |
| `skills/external/improve-docs/SKILL.md` | `.specify/skills/improve-docs/SKILL.md`（同一对） | 同上；**另有一条独立守卫**：`pytest tests/contract/test_expression_compatibility.py -q` 相对基线无新失败（基线 16 passed；本行是唯一需要 `ALLOWED_POST_BASELINE_CHANGES` 条目的文件，见 T-001） |
| `templates/commands/docs.md` | 四家 per-tool 副本（`regen-command-copies.py` 逐工具生成，**无** `.specify/templates/commands/` 镜像——该子树两侧都已退役，`test -f` 实测不存在）：`.claude/commands/speckit.docs.md`；`.github/prompts/speckit.docs.prompt.md`；`.opencode/command/speckit.docs.md`；`.qoder/commands/speckit.docs.md` | `$PY scripts/python/regen-command-copies.py --check` —— 相对基线无新漂移，且新内容在四家副本里逐字出现 |
| `docs/concepts/documentation-model.md` | **无镜像、无生成副本**（`docs/` 树不在任何 `MIRROR_PAIRS` 内） | 无镜像判据；唯一约束是 `pytest tests/contract/test_directory_governance.py -q` 相对基线无新失败（基线 21 passed；该文件须留在 area-map 清单内，`C-014`） |
| `tests/**`（新增夹具与两个测试文件） | **无镜像**（`tests/` 不在任何 pair 内） | 无镜像判据 |
| `tests/contract/test_expression_compatibility.py`（追加 allowlist 条目） | **无镜像** | 该文件自身的哈希不在冻结清单内；修改由 T-001 的判别证据覆盖 |

（`$PY` = 上段那个能 import `typer` 的解释器；本阶段实测值 `/tmp/087-toolenv/bin/python`。）

**裸解释器的 `exit 2` 不是漂移（读法说明）**：本次复跑的裸 `python3 scripts/python/sync-mirrors.py --check` 输出是

```text
Traceback (most recent call last):
  File "scripts/python/regen-command-copies.py", line 35, in <module>
    import specify_cli
  File "src/specify_cli/__init__.py", line 40, in <module>
    import typer
ModuleNotFoundError: No module named 'typer'
ok    templates/ == .specify/templates/ (22 files)
… 六对镜全 ok …
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write      （exit 2）
```

同一份输出里六对镜**全 `ok`**，末尾的 `DRIFT detected` 只反映内嵌 `regen` 子进程非零退出。
⇒ 处置是**换解释器重跑**，MUST NOT 看到提示就去 `--write`——那会把一次环境缺口变成一次真实写入。

**不落镜像的显式登记**：`skills/external/draw-diagram/**`、`.specify/specs/087-arch-diagram-docs/**`、`.specify/memory/**` 都不在 `MIRROR_PAIRS` 内，因此本特性对它们的「零改动 / 仅新增 spec 工件」不需要镜像动作。**禁止手改**：`.specify/skills/**`、`.specify/templates/**`、四家 per-tool 副本都是生成物，实施期 MUST 先改源再跑 `sync-mirrors.py --write`（或 `regen-command-copies.py`），MUST NOT 直接编辑副本。

## Execution Premises

Owner of this table's shape, its `Status` and `Decision` value domains and its invalid-row rule: `shared/workflow/acceptance-hardening.md` § Execution Premises — this skeleton carries the column set and nothing else, so a value domain written here would be a second definition.

`requirements.md` § Runtime Stack & Dependency Ownership 的 RS-001…RS-007 **每一行**的 `Premises` 列都写着 `EP-001`，因此本表只有一行。若 EP-001 被证伪，七行 RS 同时失去前提，全部按 `Decision` 列处置。

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | 本特性所需的三个能力在**已安装的本仓工作树**里现成可用，不需要联网安装、不需要新的运行时、也不需要渲染后端：(a) 一个 ≥ 3.8 的 CPython 解释器能直接运行 `docs-utils.py` 与 `tests/`；(b) `draw-diagram` 技能前门（LDM 语义模型 / 路由 / 交付契约 / 拒绝语义）作为**只读引用目标**在盘；(c) 图的两面与两份记录都是普通文件，判定只需要 `os.stat` 与 `hashlib.sha256`。 | `python3 -c "import sys;print(sys.version)"` → `3.11.13`；`skills/external/draw-diagram/{SKILL.md,references/semantic-model.md,references/routing-matrix.md,references/delivery-contract.md}` 在盘（`ls` 实读）；`skills/external/create-docs/scripts/docs-utils.py --action validate --root .` → 合法 JSON、exit 0（同一解释器，无第三方 import）；`pyproject.toml` 声明 `requires-python >= "3.8"`。**环境特定部分的实证**：`xuanji-render` 渲染后端可用性**不属** EP-001——检查器不调用任何引擎（`contracts/diagram-obligation.contract.md` `C-012`），负向夹具零渲染（`quickstart.md` S3）。 | verified | resolve-in-scope |

## Inherited Blockers

Owner of this table's shape, its `Disposition` domain, the `Source row` / `Carrier` / `Carrier slice` grammar and the carrier's eligibility rule: `shared/workflow/acceptance-hardening.md` § Inherited Blockers — this skeleton carries the column set and nothing else. The dependency set these rows are extracted from MUST be declared in this section, either as the literal `**Dependency artifacts (declared, never implied)**` block or as the exact sentence `Dependency set: none`.

Dependency set: none

**为什么是 `none`（登记依据，MUST NOT 被读成「没查」）**：本特性的**全部**输入都在同一工作树内——`requirements.md`、`draw-diagram` 的只读引用目标、`docs-utils.py` 的既有动作、`tests/contract/` 的既有守卫。它不消费另一个特性的产出，也不消费另一个 feature 的未合并分支。逐项核对（此表是**登记依据**，不是 § Inherited Blockers 的表体；表体的每一行 MUST 落在 owner 的四列文法里，因此以下结论以散文登记）：

- **069a 的冻结基线**（`notes/pre-change-file-hashes.txt` + `ALLOWED_POST_BASELINE_CHANGES`）——**不构成**继承阻塞。它是**已落地的现状**（在 base `24cb4edc` 上已在盘、守卫在跑），本特性只需在其上追加一条登记（T-001）。判据：即使 069a 的 owner 立刻停止工作，本特性仍可完成。
- **077 的 W1/W3 接线**（`flow-class-check.py` / `doc-consistency-check.py`）——**不构成**。同上：已落地、只被引用；本特性 MUST NOT 改动那两个接线小节（`C-014`），因此无版本协商需求。
- **`draw-diagram` 技能**——**不构成**。本特性对它是只读引用（T-004），且该技能已在同一树内。
- **渲染后端 `xuanji-render`**——**不构成**。检查器不调用引擎、夹具零渲染（EP-001 的 evidence 列）。
- **`checklists/requirements.md` 的派生计数漂移**——**已消解（`OI-087-01` resolved 2026-11-06）**。该清单的 N6 记录副本已按宪法 XIV **删除而非改正**，FR/SC 的唯一 owner 归 `requirements.md`；`register.md` 的 `OI-087-01` 行已相应关闭。本特性仍未改写它，且此后无需改写。

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|
| 087-1 | (none) | not-applicable | — | — | 依赖集为空，本行是「无可处置」的哨兵行，不是一条被处置的依赖记录；owner 的 `Source row` 文法为 `(none)` 形态。 |

## Document Structure

<!--
  ACTION REQUIRED (expression-class lines only): replace every [<placeholder>] below, or delete
  this whole section. Delete it also when this line declares no class.

  OWNERSHIP: this template is the **producer** of the skeleton, so the literals are written here
  verbatim — the chapter heading `## Document Structure` and its four subsections `### Chapter Tree`,
  `### Reader Baseline`, `### Evidence List`, `### Fact Owners`. Read them from this file, not from
  another project's spec artifacts: `[[STR-NNN]]` ids are a per-spec namespace, so a downstream
  project that went looking for `[[STR-002]]`…`[[STR-006]]` in its own § Shared Strings would find
  unrelated literals or nothing at all.
  The semantics, and the code-first owner of the grammar, are
  `scripts/python/doc-consistency-check.py` (`STRUCTURE_HEADING`, `STRUCTURE_SUBSECTIONS`,
  `CHAPTER_TREE_COLUMNS`, `EVIDENCE_LIST_COLUMNS`, `FACT_OWNERS_COLUMNS`,
  `READER_BASELINE_MARKERS`); a checker consumes those constants, never a copied heading.
  A feature spec that keeps its own Shared Strings table MAY cite this section by its STR ids —
  that is a per-spec convenience and never the owner.

  CLASS CONDITION: 表达类 MUST 产出该章节、执行类 MUST NOT 被要求产出 — this section is a required
  plan output for an expression-class line, and it MUST NOT become a new mandatory section for an
  execution-class line (that would contradict the zero-change guarantee for execution-class lines).

  JUDGEMENT: `doc-consistency-check.py --action structure --spec-dir <spec dir>` reads this section;
  a missing chapter is `document-structure-missing` and a missing subsection is `subsection-missing`.
  Add `--path <delivered document>` to compare the delivered document's top-level chapters against
  the Chapter Tree; without it the run says `two-way: not-run` and MUST NOT be read as two-way pass.
-->

**本行线的类别读数与本节的关系**：`flow-class-check.py --action lookup --unit-id "spec:087-arch-diagram-docs"` 的读数是 `execution`，`doc-consistency-check.py --action structure --spec-dir .specify/specs/087-arch-diagram-docs` 因此给出 `status: not-applicable`（`class=execution source=declaration`，`files_scanned: 1`）——按模板的 CLASS CONDITION，**执行类 MUST NOT 被要求**产出本章节。本节存在是**交付方自己的选择**：本特性交付的正是文档空间的结构判据，作者因此按同一纪律写下它的四个子节（下面每一行都是本特性的设计事实，不是为了过门禁而填）。检查器对该 spec 仍会报 `not-applicable`；把它读成「结构已通过」是误读。

### Chapter Tree

*本特性的「交付文档」是**检查器的 payload 与两条流程的接线文字**，但读者真正读到的是**逐文档的 finding 列表**。下表登记这份读者可见产物的结构；`父节` 列按 owner 的取值（`—` 或另一行的节名）。*

| 节名 | 父节 | 目的 | 边界 |
|------|------|------|------|
| `summary`（结论区） | — | 让读者在打开清单之前就知道「这个空间是否干净、有没有豁免」 | 只给计数与 `clean` 布尔值；单个文档的处置不在本行展开 |
| `documents[]`（逐文档清单） | `summary`（结论区） | 让读者按路径定位每一份不合规文档，并知道它落在闭集的哪一档 | 不给修复建议、不给改动计划（那属流程的收敛步骤） |
| 豁免可见性段 | `documents[]`（逐文档清单） | 让读者看见「哪些文档是靠具名豁免通过的」，以及哪条豁免已被事实推翻 | 不评价豁免理由的语义是否成立（只判它是否自相矛盾） |
| 未评估段 | `documents[]`（逐文档清单） | 让读者看见「哪些文档判不了、为什么判不了」 | 不把判不了写成通过，也不写成缺失 |

### Reader Baseline

**Readers**: 未在本会话打开过本仓库、但具备该项目领域知识的人（读 `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者；本特性不申请覆盖值）
**Reading scenario**: 一个文档作者在文档流程的收尾验证步骤里，第一次看到配套图检查的输出；他要立刻判断「我要去补哪份文档的哪一面」，而不是去读检查器的源码或问执行这次检查的 agent。

### Evidence List

*一条事实性断言一行；三件套（等级 / `as-of` / source）由 `shared/workflow/expression-gates.md` § 证据分级与 as-of 拥有，本表只填列。*

| 断言 | 证据等级 | as-of | source |
|------|----------|-------|--------|
| 本仓当前的载体集合人口（六类正式目录内 `*.md` 递归计数 + 根 `ARCHITECTURE.md` 是否在盘） | 实测 | 2026-11-06 | `quickstart.md` S2 的普查命令与其逐行输出；**人口数字只在那处存在一份**（宪法 XIV：本行不复制该数字） |
| 本仓当前只有 1 份文档引用图的两面，且该图**没有**追溯记录（无 `docs/.speckit/runs/`） | 实测 | 2026-11-06 | `quickstart.md` S2 第 1 条 + `ls -d docs/.speckit` 返回「不存在」 |
| `docs-utils.py` 当前的 `--action` 选择表不含 `obligation`，未知动作以退出码 2 被 `argparse` 拒绝 | 实测 | 2026-11-06 | `quickstart.md` S1 的实际输出（`invalid choice: 'obligation' … exit 2`） |
| 既有动作 `--action validate` 在本仓报出 3 条违规（`root-entry-oversize` 1 + `note-frontmatter` 2），且先于本特性存在 | 实测 | 2026-11-06 | `quickstart.md` S1 的第二段输出（exit 0 + 3 条 violations） |
| `tests/contract` 的基线为 6038 passed / 17 failed / 2 skipped，其中 `test_residual_total_within_sc002_target` 先于本特性存在 | 实测 | 2026-11-06 | `research.md` R6（`python3 -m pytest tests/contract -q`） |
| 两命令的镜像基线均为 exit 0，且必须用能 import `typer` 的解释器才不假红 | 实测 | 2026-11-06 | `research.md` R6 推论 1 + 本阶段 scratch venv 的 `regen` / `sync-mirrors --check` 读数 |
| `draw-diagram` 的四份 owner 文件在盘，本特性只引用不改动 | 实测 | 2026-11-06 | `ls skills/external/draw-diagram/references/` → `delivery-contract.md` / `routing-matrix.md` / `semantic-model.md` / `self-deploy-render-service.md` |
| `docs/` 树自 base `24cb4edc` 起**只**改动 `docs/concepts/documentation-model.md` | 实测 + FR-001 | 2026-11-06（计划期实测为空；交付后预期恰为一行，即 T064 的读者投影） | `git diff --name-only 24cb4edc...HEAD -- docs/` → 计划期空输出、exit 0；交付后 MUST 恰为 `docs/concepts/documentation-model.md` |
| `improve-docs/SKILL.md` 在 069a 的 74 条冻结清单内且当前未漂移，因此改它需要 allowlist 条目 | 实测 | 2026-11-06 | `research.md` R7（`grep "  skills/external/improve-docs/SKILL.md$" notes/pre-change-file-hashes.txt` 与当前文件同哈希） |
| 74 条 = **25 条非接线模板 + 49 条非接线技能**，两个分母不是同一件事 | 引用 | 2026-11-06 | `tests/contract/test_expression_compatibility.py` 模块 docstring 的 C-5 段（"the 25 non-wiring templates and 49 non-wiring skills … the 74 non-wiring sources"）+ `assert len(manifest) == 74`；`FROZEN_SKILLS` 是 49 条那一半的名字表 |
| `create-docs/SKILL.md` 与 `templates/commands/docs.md` 不在冻结清单内（是 W1/W3 接线面），因此改它们无需 allowlist 条目 | 实测 | 2026-11-06 | `research.md` R7 的三条 `grep` 读数 |
| 069a 把「接线面」与「冻结技能」分开登记，所以同一改动可能既要 allowlist 条目又不必 | 引用 | 2026-11-06 | `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` + `tests/contract/test_expression_compatibility.py` 的 `WIRING_SKILLS` / `ALLOWED_POST_BASELINE_CHANGES` 定义 |

### Fact Owners

*每个事实恰好一个 owner；下表是为了让实施期改文字前知道「该改谁、不能改谁」。*

| 事实 | owner 路径 | 章节锚 |
|------|------------|--------|
| 什么算正式文档、六类目录是哪些、保留根文件的固定语义 | `skills/external/create-docs/SKILL.md` | § Desired-State Baseline |
| 配套图义务的检查接口、封闭 verdict/reason 集、`stale` 逐面判据、逐文档判定优先级、两份记录 schema | `.specify/specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md` | 整文件（`C-001`…`C-016`） |
| 义务在两条流程与命令模板上的落地条款 | `.specify/specs/087-arch-diagram-docs/contracts/flow-obligations.contract.md` | 整文件（A–F 组） |
| 引擎层、路由矩阵、语义模型、交付契约、拒绝语义 | `skills/external/draw-diagram/SKILL.md` + `skills/external/draw-diagram/references/routing-matrix.md` | § 路由 / 交付（整文件即 owner，按技能正文的章节引用） |
| 流程类别（execution / expression）的判据与台账 | `.specify/shared/definitions/flow-class-definitions.md` | 整文件 |
| 六个门禁面与阶段算子表、证据分级与 as-of | `.specify/shared/workflow/expression-gates.md` | § 六面 / § 阶段算子表 / § 证据分级与 as-of |
| 容忍带、反 churn、干跑计划的引擎语义 | `.specify/shared/patterns/reconcile-pattern.md` | 整文件 |
| 面向用户的措辞与基准读者 | `.specify/shared/guidelines/user-facing-comprehension.md` | § 基准读者与覆盖协议 |
| 069a 的冻结基线与放行登记 | `tests/contract/test_expression_compatibility.py` | `ALLOWED_POST_BASELINE_CHANGES` / `WIRING_SKILLS`（代码即 owner） |
| 文档型含义给读者的投影（不定义规则） | `docs/concepts/documentation-model.md` | 整文件（读者投影） |

## Test Plan — clause → test 映射（P1-4）

*本节是**条款到可执行断言**的唯一登记处：每一条契约条款都必须在实施期落到一个具名测试或一个具名夹具，
否则「负向可观测」只是文字承诺。表 A 覆盖 `diagram-obligation` 的 `C-001`…`C-016`（16 行），表 B 覆盖
`flow-obligations` 的 `C-001`…`C-023` 加 `C-008a`（24 行），两表合计 **40 行、40 条条款、每条恰一行**；
表 C 是守卫文件的基线，表 D 是测试预算与红线。每行按该条款的**实际主体**绑定断言，不按编号对齐——
`diagram` 的 `C-006`（确定性）绑确定性断言、`C-009`（`stale` 第二半）绑 `stale` 断言、`C-015`（与 `validate` 的关系）
绑「不复用不合并」断言，三处都是 v1 表里按同号错绑的位置。*

`C-008a` 在本表中有行、有名具名夹具断言，但它**不是**机器可判定的条款 id：条款语法
（`shared/definitions/contract-clause-definitions.md` § 1–§ 2）的 id 形态是 `C-<数字>` 加至多一个**小数**后缀，
不带字母后缀，故 `clause_extract.py` 对那份契约抽出 23 个 id，`tasks.md` 无法对它声明 `[green:]`（会被判
`green-dangling`，且判得正确——没有机器能核这条声明）。**覆盖判定按 39 个可判定 id 计**；`C-008a` 的交付由本表
这一行 + `quickstart.md` S9 + `I::test_c008a_*` 三条具名断言承担。这是本轮如实登记的边界，不是遗漏。

命名约定：`U::` = `tests/unit/test_docs_utils_obligation.py`；`I::` = `tests/integration/test_docs_obligation_scenarios.py`；
`F::` = `tests/integration/test_docs_command_scenarios.py`（既有文件，只加用例）。
`red-when` 列写的是**这条断言在什么情况下必须变红**——没有 `red-when` 的行等于没有断言。

### A — `diagram-obligation.contract.md`（`C-001`…`C-016`）

| 条款 | 断言 / 夹具 | red-when |
|------|-------------|----------|
| `C-001` Command surface（命令面与封闭选项集） | `U::test_c001_action_registered`（`--action obligation` 出现在 `choices`）；`U::test_c001_option_set_closed`（`--record` / `--only` / `--json` 均被接受，未知选项 exit 2）；`U::test_c001_before_implementation_exit2`（S1 的 argparse 单行，作为**门禁 4 的前态读数**保留）；`U::test_c015_exit_codes`（`0` = 已判定（含不干净）、`2` = 输入错误：`--root` 不存在 / `--record` 不可读 / 未知选项——退出码定义在命令面这一条款内） | `--record` 未注册、选项集出现契约外的第六个开关，或「不干净」被映射成非 0 |
| `C-002` Read-only by construction | `I::test_c002_no_writes_on_dirty_fixture`（脏夹具上运行后 `git status --porcelain` 仍为空）；`U::test_c002_open_for_write_never_seen`（源码里该动作路径不出现写模式的文件打开） | 动作在夹具上创建、修改或删除任何文件（只读构造被破坏） |
| `C-003` Carrier set | `U::test_c003_carrier_table`（六类目录 + `ARCHITECTURE.md` 入集；notes / 归档 / 站点工具目录不入集）；`U::test_c003_non_carrier_not_judged`（非载体文档不出现在 `documents[]`） | 非载体文档进入 `documents[]`，或某类正式目录被整类漏判 |
| `C-004` 封闭 verdict 集（五值） | `U::test_c004_verdict_domain_closed`（五值之外取值即失败）；`U::test_c004_not_evaluated_breaks_clean`（判 `not-evaluated` 的文档使 `converged` **与** `clean` 同时为 `false`） | `not-evaluated` 被算作合格态，或出现第六个 verdict 值 |
| `C-005` 封闭 `reason` 集 | `U::test_c005_reason_pairs_closed`（对每个 verdict，reason 只能取该 verdict 行内的值）；`U::test_c005_faces_not_swapped`（`orphan-rendered` / `orphan-source` 两值不得互换——`SC-002` 的核心）；`U::test_c005_every_entry_named`（每条 `documents[]` 都有 `path` 与 `line`） | 两个失面值被互换或合并为单值，或某条判定缺 `path`，或 reason 取到该 verdict 行之外的值 |
| `C-006` 确定性、幂等、零写 | `I::test_c002_two_runs_identical_json`（同输入两跑字节比对，且两跑皆零写）；`U::test_c002_two_runs_identical_payload`（进程内两次调用载荷逐字节相等）；`U::test_c006_field_order_stable`（同一输入的键序稳定） | 两次输出字节不等，或第二跑引入任何盘上改动（幂等面被破坏） |
| `C-007` `satisfied` 的合取条件 | `U::test_c007_satisfied_requires_all_five`（五条拆成五个独立断言：缺任一条 ⇒ 不是 `satisfied`，而由 `C-016` 落档）；`U::test_c007_no_record_not_satisfied`（两面齐 + 引用解析 + 无记录 ⇒ `not-evaluated` / `no-trace-record`，**不是** `satisfied`） | 五个合取条件任一被弱化成「或」，或「文件都在」被当成「义务已履行」 |
| `C-008` `stale` 第一半（两个面彼此不一致） | `U::test_c008_source_newer`（夹具 `stale-source/` ⇒ `stale` / `source-newer-than-render`）；`U::test_c008_render_digest_mismatch`（`tmp_path` 副本里改渲染面字节 ⇒ `stale` / `render-digest-mismatch`）；`U::test_c008_requires_both_faces`（只一面时**不得**落到 `stale`） | 单面文档被判 `stale`；`os.utime` 失效后夹具自发变色而断言仍绿 |
| `C-009` `stale` 第二半（图与文档就同一事实不一致，部分覆盖） | `U::test_c009_reference_unresolved_not_stale`（重命名/移走渲染件 ⇒ `missing` / `reference-unresolved`，**不落** `stale`）；`U::test_c009_unrecorded_target_not_evaluated`（解析到但记录未登记的目标 ⇒ `not-evaluated` / `trace-incomplete`）；`U::test_c009_semantic_half_has_no_verdict`（语义面 MUST 不产出任何 verdict，由运行报告以 `D-001` 未收敛报出） | 语义面被实现成一个 verdict（越出冻结的部分覆盖），或重命名被判成 `stale`，或未登记目标被判成 `satisfied` |
| `C-010` 追溯记录 schema | `U::test_c010_record_schema`（逐字段校验，含 `engine` / `engine_reason` / `ldm_summary` / `delivery.accepted` / `source` / `rendered[].path`）；`U::test_c010_relative_to_root`（记录内路径一律相对 `<root>`，绝对路径即红）；`U::test_c010_no_glob_no_guess`（只读 `--record` 指定的文件，不 glob `runs/`、不猜最新） | 记录里出现绝对路径、缺任一必填字段仍被判合格，或实现去 glob/猜最新记录 |
| `C-011` 豁免记录 schema | `I::test_c011_exempt_ok`（`exempt-ok/` ⇒ `recorded-exemption` / `exempt-chronological`，`exempted=1`、`clean=false`、**`converged=true`**）；`I::test_c011_exempt_bad`（缺 `justification` ⇒ `not-evaluated` / `exemption-invalid`）；`I::test_c011_superseded`（`exemption-invalid` + `summary.exemption_superseded=1`） | 无效豁免被当成有效豁免放行（假绿）；或 `exempted>0` 仍 `clean=true`；或 `exempted>0` 把 `converged` 压成 `false` |
| `C-012` `not-evaluated` 的封闭四项 | `I::test_c012_no_record_not_evaluated`（`no-trace/` 不传 `--record` ⇒ `not-evaluated` / `no-trace-record`）；`I::test_c012_two_faces_resolving_but_unrecorded`（两面齐 + 引用解析 + 无记录仍不是 `satisfied`）；`U::test_c012_four_conditions_closed`（四个条件各由自己的夹具驱动：`no-trace-record` / `trace-incomplete` / `exemption-invalid` / `render-unreadable`，第五个即失败） | 「文件都在」被当成「义务已履行」；或出现第五个 `not-evaluated` 条件；或引擎不可用被错列为其中之一（检查器不调引擎） |
| `C-013` Payload 形态（含 `converged` / `clean`） | `U::test_c006_payload_schema`（顶层键与 `documents[]` 四字段）；`U::test_c013_clean_is_strict`（`missing`/`stale`/`not_evaluated` 任一非零 ⇒ 两谓词皆 false；`exempted>0` ⇒ `clean=false`；`carriers==0` ⇒ 两者皆 false）；`U::test_c013_empty_scope_not_converged`（默认作用域 `carriers==0` ⇒ `converged=false`）；`U::test_c013_converged_ignores_exemptions`（`exempted>0`、其余全零 ⇒ `converged=true` 且 `clean=false`）；`U::test_c013_only_empty_scope`；`U::test_c013_documents_field_set` | 四个假绿面任一漏判（`exempted>0`、`carriers==0`、`--only` 空作用域、`not-evaluated` 计作通过）；或 `converged` 被实现成 `clean` 的同义词 |
| `C-014` 与既有守卫的关系 | `A1` / `A3` / `A5`（`test_expression_gate_wiring.py`）、`C3` / `C4a`（`test_docs_command_template.py`）、`KEEP_LIST`（`test_confirmation_gates_sweep.py`）、`test_directory_governance.py`、`C5`（`test_expression_compatibility.py`）——均为**既有测试**，本特性不改断言，只加义务指针；`tests/unit/test_docs_obligation_reuse.py` 以只读引用逐条钉住它们 | 任一守卫文件的冻结清单出现未登记变更（`C5` 的哈希比对），或本特性改写了某守卫的断言集 |
| `C-015` 与既有 `validate` 动作的关系（不复用、不合并） | `U::test_c015_validate_not_merged`（`--action validate` 仍在 `choices` 且判据不变；`obligation` 是**并列**动作，两者不共享判据函数）；`U::test_c015_validate_zero_new_violations`（W1 调用点「零新增违规」基准不因新动作改变）；`U::test_c015_judged_together_in_r6`（R6 里两动作并列执行、各出各的 verdict） | 两个动作被合并进一个 `--action`（「今日合规、明日因新义务全红」的过渡态无法表达），或 `validate` 判据被本特性改动 |
| `C-016` 逐文档判定的有序优先级 | `U::test_c016_precedence_order`（多档位同时成立的夹具，断言命中**最靠前**那档：`deleted-rendered/` 必须落 `reference-unresolved` 而非 `orphan-*`）；`U::test_c016_no_backtracking`（单趟、命中后 MUST NOT 被后续档位二次覆盖）；`U::test_c016_no_second_precedence_owner`（源码里不存在第二处 `verdict =` 的分支树） | 档位顺序被实现成集合判定（顺序无关）——attempt 1 的 `F-01` 本体；或出现第二处独立判定实现；或出现第二处优先级顺序声明（`C-004` 已不再声明顺序，见 `F-03`） |

### B — `flow-obligations.contract.md`（`C-001`…`C-023` + `C-008a`，共 24 条）

| 条款 | 主体 | 断言 / 夹具 | red-when |
|------|------|-------------|----------|
| `C-001` | 四件在盘产物 | `I::test_c001_four_artifacts_one_run`（一次产出恰得四件：载体文档、可再编辑源、交付契约要求的全部渲染面、文档内解析得到的相对引用；缺任一件则该运行 MUST NOT 报完成） | 运行在缺一面或引用不可解析时仍报「完成」；或把追溯记录算成第五件（记录属 `C-003`） |
| `C-002` | 按引用产生，不复制、不建第二渲染路径 | `F::test_c002_by_reference_only`（文档流程引用 `skills/external/draw-diagram` 路径，不复制其语义模型/路由判据/交付契约条文）；`F::test_c002_no_second_render_path`（反例闭集为空：无新增绘图脚本、无引擎选择表、无交付契约副本、无绕过前门的直调） | 任一处出现复制的语义模型或第二条渲染路径 |
| `C-003` | 追溯记录同轮落盘 | `F::test_c003_record_same_run`（记录在与产图同一次运行内落盘）；`I::test_c003_missing_record_not_satisfied`（缺记录的图在检查器眼里是 `not-evaluated` / `no-trace-record`，不是 `satisfied`） | 记录缺失或延后到另一次运行仍被判 `satisfied` |
| `C-004` | 引擎拒绝原样上抛 | `F::test_c004_refusal_carried_through`（前门 Step 2 preflight 失败 / Step 2.5 后端不可达 / Step 4 覆盖不通过三种拒绝各由自己的用例驱动：流程 MUST NOT 改写为「文档已写完，图跳过」、MUST NOT 本地即兴渲染、MUST NOT 标完成，措辞归 `draw-diagram`） | 任一种拒绝被吸收成「跳过」并仍报完成；或流程自行渲染 |
| `C-005` | 共享图去重 | `I::test_c005_shared_diagram_single_source`（两份文档引用同一渲染件 ⇒ 源恰一个、记录 `diagrams[]` 恰一条同路径条目；更新写回该条而非 fork 成逐文档副本） | 共享图被 fork 成逐文档副本，或记录出现两条同路径条目 |
| `C-006` | 既有图保持引擎层 | `I::test_c006_engine_sticky_on_update`（更新后记录的 `engine` 与更新前一致；只有新图走前门路由） | 更新现有图时引擎被重新路由 |
| `C-007` | 义务唯一落点 = § Desired-State Baseline | `F::test_c007_baseline_single_owner`（义务正文只在该节出现，以「载体集合 + 义务 + 豁免」三项写出，引 `[D-003]` 载体表而非重列；该节不复述 verdict 词表） | 义务在 Baseline 之外出现第二处定义，或该节复述了检查器 verdict 词表 |
| `C-008` | § Authoring Flow 三处接线（R2/R5/R6） | `F::test_c008_authoring_r2_plans_and_r6_checks`（R2 规划每份新文档的图类意图/预计引擎层/落点；R5 产两面 + 引用 + 记录；R6 跑 `--action obligation --record <本轮记录>` 并把 verdict 并入残差，任一非零 ⇒ MUST NOT 报收敛完成） | 三处接线任一缺失，或 R6 未把 verdict 并入残差 |
| **`C-008a`** | **Reconcile 的收敛路径（R3/R4/R5/R6）** | **`I::test_c008a_second_reconcile_zero_findings`**（S9 四步：首次 R6 有 finding → R5 产图 → 第二次 R6 **`converged=true`**（按 `C-013` 谓词：`judged_scope_has_carrier && 三档全零`）→ `git status` 空）；**`I::test_c008a_exemption_does_not_block_convergence`**（`exempted=1` ⇒ 同一轮 `converged=true` 且 `clean=false`，即「靠豁免收敛」是合法终态）；`I::test_c008a_r3_r4_r5_wiring`（R3 三档都进差异集、R4 每条差异恰一条产图/重渲染条目且不进移动/归档 opt-out、R5 在 reconcile 内产图不委派 Authoring Flow） | 断言写成 `clean=true`（带豁免的空间永远变不了绿 ⇒ 收敛判据不可判定）；或第二次运行仍有三档非零；或 R5 把产图委派给 Authoring Flow |
| `C-009` | 单一落点 `<root>/docs/assets/` | `F::test_c009_single_landing_named`（落点是 `docs/assets/<slug>.<ext>`，文档以相对引用指向它；无 `diagrams/` 子树；不新建顶层文档类型目录） | 出现第二落点（`docs/<类型>/diagrams/`），或新建顶层文档类型目录 |
| `C-010` | 分级确认一格不加 | `F::test_c010_tiers_unchanged`（写图仍是 safe local writes 自动执行；移动/归档/重构仍是 stop-and-confirm；MUST NOT 引入第三档） | 出现第三档，或写图被提升为需确认 |
| `C-011` | improve-docs `### 2. Gather evidence` | `F::test_c011_improve_pointer`（该节读文档的追溯记录，作为「哪张图/哪个引擎/哪两面」的机器证据；锚在真实标题上） | 指针指向不存在的章节，或该节不读记录 |
| `C-012` | improve-docs `### 3. Classify` 的 **Diagram-sync** 行 | `F::test_c012_improve_minimal_edit`（分类表恰新增一行 **Diagram-sync**：改进改到了图所描绘的事实（组件名/关系/步骤顺序），验证后果为「同轮更新图或报具名 staleness finding，二者必居其一」） | Diagram-sync 行缺失，或其验证后果被写成「或」以外的含糊表述 |
| `C-013` | improve-docs `### 4. Apply the minimal section-level edit` | `F::test_c013_improve_verify_includes_obligation`（命中 Diagram-sync 时按 `C-001`…`C-004` 更新；不命中时在原处打一行「本次无需图工作」并在报告里重复一次） | 不命中时不作声明地重渲染（为表演活动而渲染），或命中时不更新 |
| `C-014` | improve-docs `### 5. Verify` | `F::test_c014_improve_report`（`--action obligation --only <该文档>` 的 verdict 必须是 `satisfied` 或有效 `recorded-exemption`；`stale`/`missing`/`not-evaluated` ⇒ MUST NOT 报改进完成） | Verify 步骤漏掉图维度，或非合格 verdict 仍报改进完成 |
| `C-015` | 无法重渲染 ⇒ 具名 staleness finding + 源不动 | `F::test_c015_named_staleness_keeps_source`（引擎层不可用 ⇒ 报具名 staleness finding，且源文件保持不动；MUST NOT 回滚成「看起来一致」的形态） | 重渲染失败被静默吞掉，或源被回滚/降级 |
| `C-016` | `docs.md` `### 分派` 的义务指针 | `F::test_c016_dispatch_names_both_paths`（该节增加一句：authoring 与 content 两条路径都受义务约束，义务正文只引两个技能，命令内不复述条文） | 命令里复述义务条文，或只声明了一条路径 |
| `C-017` | 残差报告按技能归口分组 | `F::test_c017_residual_five_counts`（产出行把图维度并进分组：`satisfied`/`missing`/`stale`/`exempted`/`not-evaluated` 五计数按技能归口；MUST NOT 新增第六个分组名） | 出现第六个分组名，或计数缺项 |
| `C-018` | `docs.md` 硬约束（守卫钉住） | `C3`（既有 `test_docs_command_template.py`：顶层章节序列不变）；`KEEP_LIST`（既有 `test_confirmation_gates_sweep.py`：`stop-and-confirm` 字面量保留在分派段）；`F::test_c018_improve_docs_literal_kept`（`improve-docs/SKILL.md` 字面量保留）；`F::test_c018_w1_section_byte_unchanged`（W1 类别读取小节逐字不动，新内容落在其后） | 任一条硬约束被本特性的改动破坏 |
| `C-019` | 不新增命令 / 确认档 / 不改四技能分工 | `F::test_c019_no_new_command_no_new_tier`（义务只从既有流程的验证步骤可达；命令面不新增 `/speckit.*`、不新增确认档、四技能职责划分不变） | 新增 `/speckit.*` 命令、新增确认档，或改动四技能分工 |
| `C-020` | 读者面新增一节（≤ 12 行） | `F::test_c020_reader_projection_bounded`（`docs/concepts/documentation-model.md` 新增一节 ≤ 12 行，只含「图随文档交付 / 无用可绘时有可见豁免 / 失步会被报出」三点；不复述 verdict 词表、不复述载体表、不成第二本规则书） | 超出 12 行、复述词表或载体表，或写成第二本规则书 |
| `C-021` | 该文件留在 `docs/concepts/` 且路径不变 | `test_directory_governance.py`（既有：area-map 清单仍引用该路径）；`F::test_c021_path_unchanged`（该文件不在 `git diff --name-status` 里以 `R`/`D` 出现） | 该文件被移动、重命名或删除；area-map 不再引用它 |
| `C-022` | 运行报告含 FR-022 四件 | `F::test_c022_report_carries_four_evidences`（运行报告含源路径、渲染产物路径（可多条）、文档引用、追溯记录路径；缺任一件的「已完成」MUST NOT 被写成证据） | 报告缺任一件却仍得出「已完成」结论 |
| `C-023` | 负向可观测逐面点名 | `I::test_sc002_removing_either_face_turns_red`（三种各一次：删渲染面 ⇒ `missing`/`orphan-rendered`；删源 ⇒ `missing`/`orphan-source`；推进源 mtime ⇒ `stale`/`source-newer-than-render`）；`F::test_c023_per_face_reasons_named`（三值在流程文本里各自具名，并指向 `quickstart.md` S3 作为唯一步骤登记） | 三种任一不转红（「一直绿」= 未验证而非满足），或三面被合并成一句「图有问题」 |

### C — 守卫基线与「无新失败」红线

本特性的实施 MUST NOT 让下列文件出现**新失败**（读数见 § Mirror Obligations 与 § Phase 1 的实跑块）。
一行一个文件，守卫 id 按它**实际所在的文件**归行——v1 把 A1/A3/A5、C3/C4a、C5 三组钉在同一个 `test_expression_compatibility.py`
名下，那是把三个文件的守卫算成了一份（本轮的 `F-07`）：

| 守卫文件 | 钉住的守卫 id | 基线 | 判据 |
|----------|---------------|------|------|
| `tests/contract/test_expression_compatibility.py` | `C5`（74 条非接线源的 sha256 比对） | 无新失败 | 用 `$PY`（能 import `typer` 的解释器）跑；裸 `python3` 的 import 错是**环境缺口**，不是结论。本特性新增一条 `ALLOWED_POST_BASELINE_CHANGES` 条目（T071），`C5` 由红转绿 |
| `tests/contract/test_expression_gate_wiring.py` | `A1` / `A3` / `A5` | 无新失败 | 新增文字 MUST NOT 引入引擎词或类别词；本特性不改断言，只加义务指针 |
| `tests/contract/test_docs_command_template.py` | `C3` / `C4a` | 无新失败 | 顶层章节序列不变、W1 接线小节逐字不动 |
| `tests/contract/test_confirmation_gates_sweep.py` | `KEEP_LIST`（含 `stop-and-confirm`） | 无新失败 | 确认门不被新增小节绕开；不引入第三档 |
| `tests/contract/test_directory_governance.py` | area-map 清单 | 无新失败 | 义务 MUST NOT 触发新增顶层文档类型目录；`docs/concepts/documentation-model.md` 路径不变 |
| 仓库既有失败集（全部 `tests/`） | — | 17 项已知红（见 § Residual Risk 的基线登记） | 允许集合不变；新增红即失败 |
| 镜像检查 `sync-mirrors.py` / `regen-command-copies.py` | — | `exit 0`，六对镜全 ok | 同 `$PY` 前提 |

### D — 测试预算与红线

| 项 | 预算 | 说明 |
|----|------|------|
| 新增测试文件 | **2**（`tests/unit/test_docs_utils_obligation.py`、`tests/integration/test_docs_obligation_scenarios.py`） | 不开第三个；`test_docs_command_scenarios.py` 只加用例 |
| 新增夹具 | **11**（`tests/fixtures/docs-obligation/` 下的 E6 表），加 1 个 `conftest` 建造步骤 | 夹具是**仓库内删除前的绿灯态**，写入型用例先 `copytree` 到 `tmp_path` |
| 第三方依赖 | **0** | 检查器只用标准库（research R3/R4） |
| 测试时长 | 上述两文件的**全量运行 ≤ 10s**（本机、无网络） | 85 个载体在检查器里只读元数据，不读文档全文以外的内容 |
| 红线 | 任何断言 MUST NOT 依赖 `git checkout` 的写入顺序或机器时钟 | `stale-source/` 用 `os.utime` 显式造 mtime（`data-model.md` E6） |

## Complexity Tracking
N/A — § Constitution Check 的 19 行全部 `✅ Pass`，无 `❌ Fail`、无 `⚠ Partial`，因此没有需要在复杂度跟踪里辩护的违规。三处最容易变成 `Partial` 的面已由设计消化：VII（Feature 只走到 `Planned`，不越 Pre-Status-Flip Gate）、IX（零新建引擎/命令/目录/依赖）、XIV（义务与取值域各只有一个定义点，其余全按路径引用）。

## Residual Risk

本特性**显式登记**一项未覆盖的能力面（不是缺陷，是判据尚不存在）：

| ID | 未覆盖的面 | 为什么本特性不判 | 承接方 | 重开条件 |
|----|-----------|------------------|--------|----------|
| D-001 | 图内标签 / 关系与文档正文所述事实的**语义**一致（`stale` 的第二半，见 T-003） | 检查器只读、无第三方依赖、无图形解析器（research R3/R4）；依赖 LDM 摘要的实现会把「本特性之前产生的手工图」判成假红 | `/speckit.review` 的评审面 + 后续特性（补语义判据时按 T-003 的 `revision_trigger` 重开） | `--action obligation` 的 `no-trace-record` 计数显著下降（LDM 摘要已普遍落盘），或评审面连续两次报出「机械绿但图文语义不一致」。**读法**：`quickstart.md` S9 的「零 finding」只指 `converged` 的三档全零（`missing`/`stale`/`not_evaluated`），MUST NOT 被读成「图文语义也一致」，也 MUST NOT 被读成 `clean=true`——带豁免的空间 `clean` 恒为假，而 `converged` 仍可为真 |

已关闭的登记项：`OI-087-01` —— `checklists/requirements.md` 的派生计数副本已由该清单 **N6** 按宪法 XIV 删除而非改正（owner：`/speckit.checklist`，resolved 2026-11-06；`register.md` 同一行已更新）。`requirements.md` 是 FR/SC 集合的唯一 owner，其计数由 `validate-requirements.py` 每次派生，故不存在需要同步的第二个数字。

### 已知红基线（实施期的「无新失败」判据以此为准）

本特性的验收句是「具名守卫相对基线**无新失败**」，因此基线必须是**写下来的读数**，不可是「大概都绿」。以下两条基线在实施期第一跑（T001 的 `$PY -m pytest`）时重新量一次并把新读数贴回本节；若新读数与下表不一致，先解释差异，不得把差异当成「无新失败」。

| 基线项 | 规划期读数 | 对实施期的含义 |
|--------|-----------|----------------|
| 仓库既有失败集 | **17 项已知红**（与本特性无关，实施期不修、不计入本特性的红） | 判据是「17 项之外无新增」；新跑若变成 18 项，需逐条具名说明 |
| 载体总数 | **85**（`docs/` 下六类正式目录内 `*.md` 的实测人口：`concepts/ 12 · tutorials/ 2 · tasks/ 1 · reference/ 64 · decisions/ 5 · contribute/ 1`；见 `quickstart.md` S2 的可复跑普查命令） | `summary.carriers` 的期望值。**不是** attempt 1 写的 23（一级目录计数造成的低估），**也不是**修订中途写过又撤掉的 86：`docs/ARCHITECTURE.md` 在本仓**不存在**，`C-003` 登记的是基线对该**保留根文件名**的语义（若出现在项目根则是载体），不是「本仓已有一份」。计数 MUST NOT 把不存在的文件算进人口 |
| 已带图的载体 | **1**（`docs/tutorials/quickstart.md`），且**无** `docs/.speckit/runs/*-diagram-trace.json` 记录 | 检查器落地后该文档**第一次运行必然**是 `not-evaluated` / `no-trace-record`（`C-012`）——这是**已知红**，不是实现缺陷；`clean=false` 是正确结论 |
| 该图的交付面 | 只有渲染面、**缺 HTML 面**（`D1` 交付要求三面） | 同上，属 `D-001` 的内容债；本特性只负责把它**如实报出来**，不负责补图 |

⇒ 由此得出一条硬约束：**本特性的验收 MUST NOT 是「`--action obligation --root .` 返回 `clean=true`」**，也 **MUST NOT** 是「返回 `converged=true`」——规划期已经知道本仓不干净（85 个载体里 84 个无图、唯一有图的那份无记录），两条都是本仓**必然**达不到的判据。验收面只能是**夹具空间**（S3 / S9）与**守卫无新失败**两条，本仓的真实读数只作为「已如实登记」的证据。把本仓读成验收门会把内容工作伪装成实现工作。

## Phase 1: Design Artifacts Summary

<!--
  ACTION REQUIRED (backfill ONLY — delete this comment when filling):
  Fill this section AFTER the Phase 1 artifacts (data-model.md, contracts/,
  quickstart.md, feature-ref.md) have landed on disk — never pre-write counts
  here. Record the actual artifact inventory: entity count, contract count and
  names, quickstart scenario count, and any drift from the Phase 0 expectation.
  Summarize after, not before: pre-written counts routinely drift from the
  actual output and force a correction pass.
  Every derived command printed here MUST have been actually run with its real
  output pasted, and every count taken from that output — never from memory;
  where a count comes from a pattern match, state whether that pattern can also
  match non-target lines. (The run-and-paste duty for EVERY emitted command
  example, declared expected results included, is owned by the execution-verify
  rule in `/speckit.plan`'s Post-Generation Quality Gate
  (`templates/commands/plan.md`) — this note is only its count-taking
  specialization.)
-->

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Phase 0 research | [`research.md`](./research.md) | 7 条（R1–R7），每条含实测命令/读数 + 裁决 |
| Data model | [`data-model.md`](./data-model.md) | 8 个实体（E1–E8）+ 2 个状态机（E3 verdict 判定、E4/E5 记录生命周期） |
| Contracts | [`contracts/`](./contracts/) | 2 份：`diagram-obligation.contract.md`（`C-001`…`C-016`，含新增的有序优先级 `C-016`）、`flow-obligations.contract.md`（A–F 组，`C-001`…`C-023`，含新增的 Reconcile 收敛 `C-008a`） |
| Quickstart | [`quickstart.md`](./quickstart.md) | **9 个场景（S1–S9）**，每个命令示例自带 premises 行；S1/S2/S6/S7 含规划期实测读数，S9 是 `SC-003` 的收敛回路 |
| Feature ref | [`feature-ref.md`](./feature-ref.md) | 绑定表 + 10 行交付面 + 6 组 FR→契约映射 + 10 行 SC→计量 + 5 条已披露裁定 |
| Decision Tensions | 本文件 § Decision Tensions | 5 条（T-001…T-005），`validate-decision-tensions.py` 实测 `ok` / 5 record(s) / 0 error |
| Test Plan（条款→断言映射） | 本文件 § Test Plan | `diagram-obligation` 16 条 + `flow-obligations` 23 条全覆盖 + 守卫基线 + 测试预算；新增 2 个测试文件、11 个夹具 |
| Test evidence | `test-evidence/plan-stage-status.md` + `plan-stage-status.jsonl` | 本阶段各校验命令的**实跑读数**（见下）；`.jsonl` 是机器可读行（`stage=plan` / `row_type=stage-status`） |

**与 Phase 0 预期的漂移**：Phase 0 预期「两份契约覆盖 RS-006 的两半 + 流程接线」；实际落地时多发现一处需要机械纠正的口径——`C-001` 初稿把 `--root` 写成「文档空间根」，而 `docs-utils.py` 的既有动作一律以**项目根**为根（`--action validate --root .` 的实读输出证明）。该纠正已就地落进 `C-001`/`C-010`/`C-011`（`<root>`），并在本阶段回传中披露：它是**纠正**（恰有一种与既有引擎一致的读法），不是裁定。契约条款数因此从 15+23 不变，但三处路径口径改为统一引用 `C-001`。

**本阶段实跑的校验与读数**（命令与输出逐条对应，完整记录见 `test-evidence/plan-stage-status.md`）：

```text
python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs
  -> status: ok ; scanned: 562 lines, 5 record(s) ; 6 checks 全 pass (0) ; 0 error(s), 0 warning(s)   exit 0
python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/087-arch-diagram-docs --stage plan --repo .
  -> decision=pass errors=0 advisories=38 waived=0（fr=23 sc=10 files=9）                            exit 0
     38 条 advisory 全部同型：`missing-path`——指向的都是**实施期才存在**的路径
     （`tests/unit/test_docs_utils_obligation.py`、`tests/integration/test_docs_obligation_scenarios.py`、
     `tests/fixtures/docs-obligation/`、`docs/.speckit/runs|exemptions/`、`.specify/templates/commands/`、
     以及 T-005 **反题**里那两个 `diagrams/` 目录——引它们正是为了说明它们**不**该存在）
python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/087-arch-diagram-docs --stage requirements --repo .
  -> decision=pass errors=0 advisories=38 waived=0（同一批，规格面无回归）                          exit 0
/tmp/087-toolenv/bin/python scripts/python/sync-mirrors.py --check            -> exit 0，六对镜全 ok
/tmp/087-toolenv/bin/python scripts/python/regen-command-copies.py --check     -> exit 0，"OK: all per-tool command copies match the source templates."
python3 scripts/python/sync-mirrors.py --check（裸解释器，仅作反例）          -> exit 2，见 § Mirror Obligations 的读法说明
```

⇒ 两条读法：(1) 镜像判据 MUST 用能 import `typer` 的解释器，否则量到的是环境缺口而不是漂移；
(2) `advisories=38` 是**已知的、同型的**，`errors=0` 才是门禁；把 advisory 清零需要删掉「实施期才存在的路径」
这类正当前瞻引用，属倒退而非改进。
