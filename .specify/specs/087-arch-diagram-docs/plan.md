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
**Scale/Scope**: 6 处文本落点 / 4 个文件（`data-model.md` E7）+ 1 个引擎动作 + 2 份记录 schema + 11 段夹具；85 份载体文档的实测人口（`quickstart.md` S2）。

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
| 本仓 `docs/` 零改动 | requirements § Out of Scope / A6 | `git diff --name-only 24cb4edc...HEAD -- docs/` 为空 |

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

**Structure Decision**: 本特性落在**既有文档技能引擎 + 既有命令模板**之内，是一个「加动作 + 加文本 + 加夹具」的改动，**不新建任何顶层目录、不新建技能、不新建命令**。形态因此不是上面任何一个通用模板（single/web/mobile/library/monorepo），而是本仓惯用的「框架源 + 镜像运行时」双层：4 个源文件（`create-docs/SKILL.md`、`docs-utils.py`、`improve-docs/SKILL.md`、`templates/commands/docs.md`）+ 1 个既有文档（`docs/concepts/documentation-model.md`）承载全部行为改动，其余全是生成副本或测试。`skills/external/draw-diagram/**` 在交付树里**故意缺席**：它只被引用、一行不改（T-004），缺席就是「不交付」的登记。

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
- **`checklists/requirements.md` 的派生计数漂移**——**不构成 blocker，登记为未决项 `OI-087-01`**。owner 是 `/speckit.checklist`，处置归 requirements 阶段收尾；本特性 MUST NOT 改写它（宪法 XIV：发现陈旧的计数副本时删掉副本，而不是改正数字）。它是可见的未决项，不是前置条件：绕开它本特性仍可完整交付。

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
| `docs/` 树自 base `24cb4edc` 起零改动 | 实测 | 2026-11-06 | `git diff --name-only 24cb4edc...HEAD -- docs/` 空输出、exit 0 |
| `improve-docs/SKILL.md` 在 069a 的 74 条冻结清单内且当前未漂移，因此改它需要 allowlist 条目 | 实测 | 2026-11-06 | `research.md` R7（`grep "  skills/external/improve-docs/SKILL.md$" notes/pre-change-file-hashes.txt` 与当前文件同哈希） |
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
否则「负向可观测」只是文字承诺。表 A / B 覆盖两份契约的**全部条目**（`diagram-obligation` `C-001`…`C-016`、
`flow-obligations` `C-001`…`C-023`），表 C 是守卫文件的基线，表 D 是测试预算与红线。*

命名约定：`U::` = `tests/unit/test_docs_utils_obligation.py`；`I::` = `tests/integration/test_docs_obligation_scenarios.py`；
`F::` = `tests/integration/test_docs_command_scenarios.py`（既有文件，只加用例）。
`red-when` 列写的是**这条断言在什么情况下必须变红**——没有 `red-when` 的行等于没有断言。

### A — `diagram-obligation.contract.md`（`C-001`…`C-016`）

| 条款 | 断言 / 夹具 | red-when |
|------|-------------|----------|
| `C-001` 接口面与封闭参数集 | `U::test_c001_action_registered`（`--action obligation` 出现在 `choices`）；`U::test_c001_option_set_closed`（`--record` / `--only` / `--json` 均被接受，未知选项 exit 2）；`U::test_c001_before_implementation_exit2`（S1 的 argparse 单行，作为**门禁 4 的前态读数**保留） | `--record` 未注册、或选项集出现契约外的第六个开关 |
| `C-002` 只读 / 确定性 / 幂等 | `I::test_c002_two_runs_identical_json`（S4 的两跑比对 + `git status --porcelain` 为空）；`I::test_c002_no_writes_on_dirty_fixture` | 任一跑写出盘上文件，或两次输出字节不等 |
| `C-003` 载体集合 | `U::test_c003_carrier_table`（六类目录 + `ARCHITECTURE.md` 入集；保留根文件 / notes / 归档 / 站点工具目录不入集）；`U::test_c003_non_carrier_not_judged`（`in_carrier_set=false` 的文档不出现在 `documents[]`） | 非载体文档进入 `documents[]`，或某类正式目录被整类漏判 |
| `C-004` 封闭 verdict 集 | `U::test_c004_verdict_domain_closed`（五值之外取值即失败）；`U::test_c004_not_evaluated_breaks_clean`（判 `not-evaluated` 的文档使 `converged` **与** `clean` 同时为 `false`） | `not-evaluated` 被算作合格态（`converged=true` 或 `clean=true`） |
| `C-005` verdict↔reason 封闭表 + 失面具名 | `U::test_c005_reason_pairs_closed`（对每个 verdict，reason 只能取表内值）；**`U::test_c005_faces_not_swapped`**（夹具 `orphan-rendered` ⇒ `orphan-rendered`、`orphan-source` ⇒ `orphan-source`，两值互换即红——`SC-002` 的核心）；`U::test_c005_every_entry_named`（每条 `documents[]` 都有 `path` 与 `line`） | 两个失面值被任一实现互换、合并为单值，或某条判定缺 `path` |
| `C-006` JSON 载荷与字段序 | `U::test_c006_payload_schema`（顶层四键 + `documents[]` 四字段）；`U::test_c006_field_order_stable` | 载荷形状漂移，或同一输入的键序不稳定 |
| `C-007` `satisfied` 的五条合取 | `U::test_c007_satisfied_requires_all_five`（五条拆成五个独立断言：缺任一条 ⇒ 不是 `satisfied`，而是由 `C-016` 落档）；`U::test_c007_no_record_not_satisfied`（两面齐 + 引用解析 + 无记录 ⇒ `not-evaluated` / `no-trace-record`，**不是** `satisfied`——本条与 `C-012` 同一事实，两条款各挂自己的断言） | 五个合取条件任一被弱化成「或」，或「文件都在」被当成「义务已履行」 |
| `C-008` `stale` 逐面判据 | **`U::test_c008_source_newer`**（夹具 `stale-source/` ⇒ `stale` / `source-newer-than-render`）；`U::test_c008_render_digest_mismatch`（夹具在 `tmp_path` 副本里改渲染面字节 ⇒ `stale` / `render-digest-mismatch`）；`U::test_c008_requires_both_faces`（只一面时**不得**落到 `stale`） | 单面文档被判 `stale`；`os.utime` 失效后夹具自发变色而断言仍绿 |
| `C-009` 单一落点 | `U::test_c009_landing_is_docs_assets`（`source` / `rendered[]` 的父目录必须是 `<root>/docs/assets/`）；`U::test_c009_no_second_landing`（不存在 `docs/*/diagrams/` 形式的第二落点——T-005 的反题已被排他） | 图落进 `docs/<类型>/diagrams/` 或项目根下第二个 `assets/` |
| `C-010` 记录 schema | `U::test_c010_record_schema`（`--record` 文件逐字段校验，含 `engine` / `engine_reason` / `ldm_summary` / `delivery`）；`U::test_c010_relative_to_root`（记录里的路径一律相对项目根，绝对路径即红） | 记录里出现绝对路径，或缺任一必填字段仍被判合格 |
| `C-011` 豁免记录 | `I::test_c011_exempt_ok`（`exempt-ok/` ⇒ `recorded-exemption` / `exempt-chronological`，`exempted=1`、`clean=false`、**`converged=true`**）；**`I::test_c011_exempt_bad`**（`exempt-bad/` 缺 `justification` ⇒ `not-evaluated` / `exemption-invalid`，**不是** `recorded-exemption`）；`I::test_c011_superseded`（`exempt-superseded/` ⇒ `exemption-invalid` + `summary.exemption_superseded=1`） | 无效豁免被当成有效豁免放行（假绿）；或 `exempted>0` 仍 `clean=true`；或 `exempted>0` 把 `converged` 压成 `false`（那会让豁免终态永远不收敛） |
| `C-012` 未记录不得合格 | `I::test_c012_no_record_not_evaluated`（`no-trace/` 不传 `--record` ⇒ `not-evaluated` / `no-trace-record`、`converged=false`、`clean=false`）；`I::test_c012_two_faces_resolving_but_unrecorded`（两面齐 + 引用解析 + 无记录仍然不是 `satisfied`） | 「文件都在」被当成「义务已履行」（`SC-002` 的假绿面） |
| `C-013` 计数、`converged` 与 `clean` | **`U::test_c013_clean_is_strict`**（`clean` 的严格面：`missing`/`stale`/`not_evaluated` 任一非零 ⇒ `converged=false` 且 `clean=false`；`exempted>0` ⇒ `clean=false`；`carriers==0` ⇒ `converged=false` 且 `clean=false`）；**`U::test_c013_empty_scope_not_converged`**（默认作用域 `carriers==0` ⇒ `judged_scope_has_carrier=false` ⇒ `converged=false` 且 `clean=false`；与 `--only` 空作用域的 vacuous true 对照）；**`U::test_c013_converged_ignores_exemptions`**（`exempted>0`、其余三档全零 ⇒ `converged=true` 且 `clean=false`——两个谓词的分歧点本体）；`U::test_c013_only_empty_scope`（`--only` 匹配 0 个对象时两个谓词都按公式算得 `true` 而输出带注记）；`U::test_c013_documents_field_set`（`documents[]` 恰四字段，`summary` 含 `converged`） | 四个假绿面任一漏判（`exempted>0`、`carriers==0`、`--only` 空作用域、`not-evaluated` 计作通过）；或 `converged` 被实现成 `clean` 的同义词（带豁免的空间于是永远不收敛） |
| `C-014` 接线守卫不动 | `A1` / `A3` / `A5`（`test_expression_gate_wiring.py`）、`C3` / `C4a`（`test_docs_command_template.py`）、`KEEP_LIST`（`test_confirmation_gates_sweep.py`）、`test_directory_governance.py`——均为**既有测试**，本特性不改断言只加义务指针 | 任一守卫文件的冻结清单出现未登记变更（`C5` 的哈希比对） |
| `C-015` 退出码 | `U::test_c015_exit_codes`（`0` = 已判定（含不干净）、`2` = 输入错误：`--root` 不存在 / `--record` 不可读 / 未知选项） | 「不干净」被映射成非 0（会让调用方把判定当故障） |
| `C-016` 有序优先级 | `U::test_c016_precedence_order`（构造**多档位同时成立**的夹具，断言命中的是最靠前的那一档：`deleted-rendered/` 必须先落 `reference-unresolved` 而非 `orphan-*`）；`U::test_c016_no_backtracking`（单趟、不重复覆盖——命中后 MUST NOT 被后面的档位二次覆盖）；`U::test_c016_no_second_precedence_owner`（源码里不存在第二处 `verdict =` 的分支树，落档只能走 `C-016` 的单趟函数） | 档位顺序被实现成集合判定（顺序无关）——这是 attempt 1 的 `F-01` 本体；或出现第二处独立判定实现（两处判据各自漂移） |

### B — `flow-obligations.contract.md`（`C-001`…`C-023`）

| 条款 | 断言 / 夹具 | red-when |
|------|-------------|----------|
| `C-001` 第五类工件登记 | `F::test_c001_obligation_artifact_listed`（Desired-State Baseline 的工件清单含配套图义务） | 义务被写成「可选建议」而非工件 |
| `C-002` Baseline `#### Assets` | `F::test_c002_assets_subsection_present`（`create-docs/SKILL.md` 出现 `#### Assets` 且含 `docs/assets/`——该小节由**实施期新建**，当前不在盘，因此这条断言在实施前**必然红**，这正是它作为「未交付即红」判据的用法） | 实现在盘上仍无 `#### Assets` 小节（落点区域无 owner 章节）；判据 MUST NOT 因其它小节含有 `docs/assets/` 字样而变绿 |
| `C-003` Reconcile R2 口径 | `F::test_c003_r2_scope_names_obligation` | R2 的文档范围口径漏掉图维度 |
| `C-004` Reconcile R3 差异含 verdict | `F::test_c004_r3_includes_verdicts`（R3 的 diff 描述含四计数） | R3 只报文本差异 |
| `C-005` R4 干跑计划含产图行 | `F::test_c005_r4_dry_run_has_produce_rows` | 干跑计划无法预告产图/重渲染 |
| `C-006` R6 残差报告四计数 | `F::test_c006_r6_residual_four_counts` | 残差只报总数不报分类 |
| `C-007` Baseline 唯一落点 | `F::test_c007_baseline_single_owner`（§ Desired-State Baseline 是义务的唯一落点，不重述检查器 verdict 词表） | 义务在 Baseline 之外出现第二处定义；`--record` 调用点义务归 `C-008a` R6 / `diagram-obligation` C-012，不在本行 |
| **`C-008a` Reconcile 收敛** | **`I::test_c008a_second_reconcile_zero_findings`**（S9 的四步：首次 R6 有 finding → R5 产图 → 第二次 R6 **`converged=true`**（按 `C-013` 的 `converged` 谓词：`judged_scope_has_carrier && missing` / `stale` / `not_evaluated` 三档全零）→ `git status` 空）；**`I::test_c008a_exemption_does_not_block_convergence`**（`exempt-ok/` 形态的夹具：`exempted=1` ⇒ 同一轮 `converged=true` 且 `clean=false`，即「靠豁免收敛」是合法终态） | 断言写成 `clean=true`（带豁免的空间永远变不了绿 ⇒ 收敛判据不可判定），或第二次运行仍有 `missing`/`stale`/`not_evaluated`，或第二次运行又写盘（churn） |
| `C-009` 单落点（流程侧） | `F::test_c009_single_landing_named`（`create-docs` 的落点文字与 `C-009` 一致，无 `diagrams/` 子树） | 流程文本与契约落点冲突 |
| `C-010` Authoring Flow 产图点 | `F::test_c010_authoring_flow_produces` | 新建文档时无产图步骤 |
| `C-011` improve-docs `### 2. Gather evidence` | `F::test_c011_improve_pointer`（锚在真实标题上） | 指针指向不存在的章节 |
| `C-012` improve-docs `### 4. Apply…` | `F::test_c012_improve_minimal_edit` | 最小编辑规则被改写成可大改 |
| `C-013` improve-docs `### 5. Verify` | `F::test_c013_improve_verify_includes_obligation` | 校验步骤漏掉图维度 |
| `C-014` improve-docs `### 6. Record and report` | `F::test_c014_improve_report` | 报告不含义务读数 |
| `C-015` Authoring R2 | `F::test_c015_authoring_r2` | — |
| `C-016` Authoring R5 | `F::test_c016_authoring_r5_render` | 重渲染步骤缺失 |
| `C-017` Authoring R6 | `F::test_c017_authoring_r6` | — |
| `C-018` `docs.md` 顶层章节序列 | `C3`（既有 `test_docs_command_template.py`） | 顶层序列被改动 |
| `C-019` `docs.md` `### 分派` 义务指针 | `F::test_c019_dispatch_pointer` | 新增小节改动了 W1 接线小节 |
| `C-020` `stop-and-confirm` 保留 | `KEEP_LIST`（既有 `test_confirmation_gates_sweep.py`） | 确认门被新增小节绕开 |
| `C-021` 禁类别词 | `A1` / `A3` / `A5`（既有 `test_expression_gate_wiring.py`） | 新增文字引入类别词 |
| `C-022` 冻结清单登记 | `C5`（既有 `test_expression_compatibility.py`）+ `manifest` key | 冻结清单哈希漂移且未登记 |
| `C-023` 逐面拒绝语义的流程侧 | `F::test_c023_per_face_reasons_named`（`orphan-rendered` / `orphan-source` / `source-newer-than-render` 三值在流程文本里各自具名，且指向 `quickstart.md` S3 作为唯一步骤登记） | 流程侧把三面合并成一句「图有问题」 |

### C — 守卫基线与「无新失败」红线

本特性的实施 MUST NOT 让下列文件出现**新失败**（读数见 § Mirror Obligations 与 § Phase 1 的实跑块）：

| 守卫 | 基线 | 判据 |
|------|------|------|
| `test_expression_compatibility.py` 五条具名守卫（A1 / A3 / A5 / C3 / C4a / C5） | 无新失败 | 用 `$PY`（能 import `typer` 的解释器）跑；裸 `python3` 的 import 错是**环境缺口**，不是结论 |
| `test_directory_governance.py` | 无新失败 | 目录治理不被义务触发新增目录 |
| `test_confirmation_gates_sweep.py` | 无新失败 | `KEEP_LIST` 覆盖 `stop-and-confirm` |
| 仓库既有失败集 | 17 项已知红（见 § Residual Risk 的基线登记） | 允许集合不变；新增红即失败 |
| 镜像检查 `sync-mirrors.py` / `regen-command-copies.py` | `exit 0`，六对镜全 ok | 同 `$PY` 前提 |

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

已登记、但**不是**本特性风险的未决项：`OI-087-01` —— `checklists/requirements.md` 的派生计数副本与「23 FR / 10 SC」的实际计数共存（owner：`/speckit.checklist`；处置归 requirements 收尾；本阶段不改写，见 § Inherited Blockers 的最后一行）。

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
