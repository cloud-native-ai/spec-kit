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
3. **判据冻结在契约**：[`contracts/diagram-obligation.contract.md`](./contracts/diagram-obligation.contract.md) 拥有命令面、封闭 verdict/reason 集、`stale` 逐面判据、追溯记录与豁免记录 schema；所有其他面按路径引用它，不复述取值。
4. **能力零新建**（T-004）：`draw-diagram` 只被引用、一行不改；文档侧不出现第二个引擎、第二份路由表或第二份交付契约。
5. **诚实的能力边界**（T-003 / D-001）：`stale` 的第二半「图与文档就同一事实不一致」只判到「引用仍在且解析」，语义一致性**显式登记为未覆盖**，不发明一条没有判据的 verdict——这是 A12 自己给的第二条路。

## Technical Context

**Language/Version**: Python 3（`pyproject.toml` 已声明 `requires-python >= "3.8"`，本次不新增 pin）；新增代码 stdlib-only（`argparse` / `json` / `os` / `hashlib` / `re`），不引入第三方依赖（RS-001）。
**Primary Dependencies**: 无新增运行时依赖。门禁侧沿用既有 `tests/contract/` 的 pytest 套件；镜像侧沿用 `scripts/python/sync-mirrors.py` 与 `scripts/python/regen-command-copies.py`（后者 `import specify_cli` → `import typer`，需能 import typer 的解释器，裸 `python3` 会假红）。
**Storage**: 文件系统即存储。三类在盘事实：载体文档（`docs/**` + 根 `ARCHITECTURE.md`）、图的两面（源 + 渲染产物）、两份记录（追溯记录 `docs/.speckit/runs/`、豁免记录 `docs/.speckit/exemptions/`，均为既有 `docs/.speckit/` C 区机器目录下的新子目录）。
**Testing**: `tests/unit/test_docs_utils_obligation.py`（新增，封闭集与只读断言）+ `tests/fixtures/docs-obligation/**`（四段负向夹具 + 三段豁免夹具，纯文件、零渲染、零网络）+ 既有四条契约守卫保持通过。基线口径见 § Technical Constraints。
**Target Platform**: 任意 POSIX 文件系统（`os.stat` 的 mtime 与 `hashlib.sha256` 是唯一机器信号，无图形解析、无网络）。
**Project Type**: 文档 / 提示框架仓（Two Hats：改 `skills/` `templates/` 的框架源，`.specify/` 与四家 per-tool 副本由生成器同步；`docs/` 的内容工作不属本特性）。
**Performance Goals**: 不设指标。检查器只做一次目录遍历 + 每个图的两次 `stat` / 一次 sha256，载体规模是本仓 23 份量级。
**Constraints**: 检查器 MUST 只读（允许的副作用集合是空集）、确定性（两次运行字节可比）、幂等；MUST NOT 新增 `/speckit.*` 命令；MUST NOT 改动 069a 的四字面量与 W1/W3 接线小节；MUST NOT 改本仓 `docs/` 内容。
**Scale/Scope**: 5 处文本落点 / 4 个文件（`data-model.md` E7）+ 1 个引擎动作 + 2 份记录 schema + 7 段夹具；23 份载体文档的实测人口（`quickstart.md` S2）。

### Technical Constraints（实施期 MUST 保持）

| 约束 | 来源 | 判据形态 |
|------|------|----------|
| 只读 | FR-015 / 契约 `C-002` | 允许副作用集合为空集；`git status --porcelain` 在检查后为空 |
| 确定性 + 幂等 | FR-015 / 契约 `C-006` | 两次运行输出 `cmp` 相同 |
| 封闭 verdict / reason 集 | FR-016 / 契约 `C-004`、`C-005` | 第六个值即契约违规，由 `tests/unit/` 逐值断言 |
| 无新命令 | FR-017 | `git diff` 里不出现 `templates/commands/*` 的新文件 |
| 守卫保持通过 | A7 / 契约 `C-014` | 四条守卫**相对基线无新失败**（基线：`tests/contract` 6038 passed / 17 failed / 2 skipped） |
| 镜像无新漂移 | 模板 § Mirror Obligations | `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对基线不新增漂移（基线两命令均 exit 0，需 typer 可 import 的解释器） |
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
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每个设计裁决回溯到 FR：`contracts/diagram-obligation.contract.md` 头部 `FR served` 列了它所服务的 10 条 FR；`contracts/flow-obligations.contract.md` 的 A–F 组逐条映射 FR-001…FR-023 |
| II | Feature-Centric Development | ✅ Pass | 绑定既有 Feature 087（reuse-first 五候选复核见 `requirements.md` § Related Feature）；本阶段把 087 从 `Draft` 推进到 `Planned` 并同步 `features.md` 与 `features/087.md` |
| III | Intent-Driven Development | ✅ Pass | § Decision Tensions 的 5 条记录把每个「怎么落到工件」的取舍写成可独立采纳的反题 + 判别证据 + 重开条件；`research.md` 的 R1–R7 只给测量与裁决，不直接生成代码 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 契约先行（`contracts/` 两份已落盘）→ 再实现；`tests/fixtures/docs-obligation/**` 与 `tests/unit/test_docs_utils_obligation.py` 在 `quickstart.md` S3–S5 定义了先行的负向断言（FR-023 的「主体坏了必须红」） |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent、不改 `agents/`；义务落在既有技能与既有命令模板的文本上，窗口在 `data-model.md` E7 逐行列明 |
| VI | Continuous Quality & Observability | ✅ Pass | FR-022 的四项证据（源路径、渲染面路径、文档引用、追溯记录）落在运行报告；`test-evidence/` 记录本阶段的实测读数 |
| VII | Specification-Plan-Task-Implementation Workflow [NON-NEGOTIABLE] | ✅ Pass | 本阶段产物即 Phase 0（`research.md`）+ Phase 1（`data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`）；Feature 状态只走 `Draft → Planned`，**不退化为 Implemented**（无 open task、无 `verification.log`，Pre-Status-Flip Gate 未满足且本阶段不试图满足） |
| VIII | Code as the Single Source of Truth | ✅ Pass | 检查器的行为以 `docs-utils.py` 的实现在盘为准；`data-model.md` 与契约只登记接口与取值域，不复述实现细节；`quickstart.md` S1 记录**当前**动作表用 `argparse` 拒绝未知动作的实测输出，而不是凭记忆写 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 不新建引擎 / 渲染器 / 命令 / 确认分级 / 目录族（FR-011、FR-017、FR-018、T-004、T-005）；新增面无第三方依赖；《scope》一句「框架，非运行时」在 `contracts/diagram-obligation.contract.md` `C-012` 得到遵守——引擎可用性不归检查器判 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 不新增保留根文件名、不改其注册位置（FR-002）；两份记录的落点是既有 `docs/.speckit/` 机器目录下的 `runs/` 与 `exemptions/` 两个 lowercase 子目录，`data-model.md` E4/E5 与 `C-010`/`C-011` 同源 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 两顶帽子已显式点名：本特性改框架源（`skills/` `templates/`），`.specify/` 与四家 per-tool 副本由 `sync-mirrors.py` / `regen-command-copies.py` 生成（§ Mirror Obligations 逐行登记）；本仓 `docs/` 内容工作被 § Out of Scope 排除，`quickstart.md` S8 以空 diff 为判据 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 图的产生一律走既有 `draw-diagram`（FR-011、T-004），MUST NOT 另写绘图/渲染代码；检查器复用既有文档引擎 `docs-utils.py` 而非另起脚本（T-002） |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 本特性强化 **Change Validation** 维度：图从「作者记得画」变成「既有验证步骤判得出」，且负面可观测（FR-023）。目标模型引 `shared/guidelines/better-harness.md`，不另立维度或评分 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 义务定义点唯一（Baseline 一条）；检查器取值域唯一（`contracts/diagram-obligation.contract.md`）；`docs/concepts/documentation-model.md` 只做读者投影；`data-model.md` 与 `quickstart.md` 头部均写明「不复述取值域」。`checklists/requirements.md` 的派生计数副本**不改写、只登记**（`OI-087-01`），处置归 `/speckit.checklist` |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 新增 finding 的输出面向未参与运行的人：每份文档带路径与闭集理由（FR-016），`C-005` 给每个 reason 一句自然语言含义；`C-013` 的 `clean` 是显式结论而不是空输出。基准读者取自 `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议，不另定义 |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | 「主体坏了检查仍绿」被明确定义为**未验证而非通过**（FR-023 / `C-013` 的 `carriers == 0 ⇒ clean=false`）；`exemption_superseded` 把「豁免理由已失效」作为可见事实报出（FR-004）；本阶段实施的纠正（`quickstart.md` S1 命令面实测、契约 `C-001` 的 root 口径）已在回传中披露 |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | 不新建顶层目录；两个新子目录（`docs/.speckit/runs/`、`docs/.speckit/exemptions/`）的含义在本特性 plan 与其契约 `C-010`/`C-011` 处登记，且**不是**新的顶层或新的目录族——`docs/.speckit/` 已是基线登记的机器目录（Baseline A 区注释）。`test_directory_governance.py` 保持通过（`C-014`） |
| XVIII | Grounded Naming | ✅ Pass | 动作名 `obligation` 取自规格自身术语（diagram obligation）；记录名 `diagram-trace` 取自 FR-013 的 traceability；`exempt-*` 三值取自 FR-004 的 exemption。无自创名词，`C-011` 的三值都读作「本文件没有结构可绘」 |
| XIX | Self-Explanatory Structure (不言自明) | ✅ Pass | 用户看到的红是「哪份文档、缺哪个面、属于闭集里的哪个理由」（`C-005` 的 `path` + `line` + `reason`），不需要打开检查器源码；提升的信息维度是「文档空间的图完整性」，其落地机制就是 reconcile/verification 这一既有 reconcile 机制（`shared/patterns/reconcile-pattern.md`），不新增第四种机制 |

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

### T-005 — 图的落点：沿用现有分类学的 `assets/` 约定，不新增文档类型目录

- **decision**: 图的源与渲染产物放在被引用文档所在区域的 `assets/` 下（本仓先例 `docs/assets/quickstart-workflow.{puml,svg,png}`），由基线既有约定表达；MUST NOT 为图新建顶层目录、MUST NOT 把图判成文档。
- **antithesis**: 为图建一族与六类正式目录并列的第七类（`docs/diagrams/`）；当图本身是主要交付物、需要独立的索引与生命周期时它更优——图的发现与导航不再依附于散文。
- **binding_constraints**:
  - pole_a: 分类学 MUST 只有一套（Baseline 自称其 enumerations 的唯一 owner），新增一族即第二套 taxonomy。
  - pole_b: 图 MUST 有可导航的家，不能散落在未登记的位置。
- **discriminating_evidence**: 读 `skills/external/create-docs/SKILL.md` § Desired-State Baseline 的目录枚举与「`docs/.speckit/` 与站点工具目录不是文档」的既有判据，看 `assets/` 是否已在其中被承认为非文档区域；结果二值：是（沿用）/ 否（需登记新目录）。
- **expected_sacrifice**: SC-009 Source ↓ 图没有自己的顶层导航入口；读者通过文档正文的相对引用找到图，跨文档复用的图靠引用计数而非索引发现。
- **revision_trigger**: 当同一张图被 ≥3 份文档引用、且出现「要整体浏览所有架构图」的实际需求 → 重开，评估是否把图提升为有索引的一等区域（那会触及 Baseline 的 owner，须走其修订）。

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
├── quickstart.md              # Phase 1：S1–S8 的命令与预期形状
├── contracts/                 # Phase 1：两份契约（检查器面 / 流程义务面）
├── feature-ref.md             # Phase 1：Feature 087 绑定与 FR/SC 映射
├── test-evidence/             # 本阶段实测读数（既有目录）
└── tasks.md                   # Phase 2（/speckit.tasks 产出，本阶段不创建）
```

### Source Code (repository root)

```text
skills/external/create-docs/
├── SKILL.md                             # + § Desired-State Baseline 一条义务条目；+ Reconcile R6 / Authoring R2,R5,R6 的接线
└── scripts/docs-utils.py                # + --action obligation（只读判定，见 contracts/diagram-obligation.contract.md C-001…C-015）

skills/external/improve-docs/
└── SKILL.md                             # + § Workflow 的 Diagram-sync 分类行与最小编辑规则

templates/commands/docs.md               # + § Outline 内的义务指针小节（W1 接线小节原样保留）

docs/concepts/documentation-model.md     # + 读者面投影一段（既有文档的追加，不新建文件）

tests/
├── unit/test_docs_utils_obligation.py   # 封闭 verdict/reason 集、只读、确定性、空载体判脏
└── fixtures/docs-obligation/            # clean / missing-face / no-diagram / stale-source / exempt-ok / exempt-bad / exempt-superseded

tests/contract/test_expression_compatibility.py   # + ALLOWED_POST_BASELINE_CHANGES 一条（仅 improve-docs）
```

**Structure Decision**: 本特性落在**既有文档技能引擎 + 既有命令模板**之内，是一个「加动作 + 加文本 + 加夹具」的改动，**不新建任何顶层目录、不新建技能、不新建命令**。形态因此不是上面任何一个通用模板（single/web/mobile/library/monorepo），而是本仓惯用的「框架源 + 镜像运行时」双层：4 个源文件（`create-docs/SKILL.md`、`docs-utils.py`、`improve-docs/SKILL.md`、`templates/commands/docs.md`）+ 1 个既有文档（`docs/concepts/documentation-model.md`）承载全部行为改动，其余全是生成副本或测试。`skills/external/draw-diagram/**` 在交付树里**故意缺席**：它只被引用、一行不改（T-004），缺席就是「不交付」的登记。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

**基线（编辑前实测，2026-11-06）**：`regen-command-copies.py --check` → `OK: all per-tool command copies match`（exit 0）；`sync-mirrors.py --check` → 六对镜全 `ok`（exit 0）。两条都必须用**能 import `typer` 的解释器**跑：`sync-mirrors.py` 内嵌调用 `regen`，裸 `python3` 会因 `ModuleNotFoundError: typer` 以 exit 2 假红，即使六对镜本身全 ok（research R6 推论 1）。因此本表每一行 `Verify` 的判据形态是**相对上述基线无新漂移**，不是「退出码 0」这一条绝对断言。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/create-docs/SKILL.md` | `.specify/skills/create-docs/SKILL.md`（`MIRROR_PAIRS` 第 2 对 `skills/external` → `.specify/skills`，扁平运行时层） | `<venv>/bin/python scripts/python/sync-mirrors.py --check` —— 相对基线无新漂移（本行 pair 不得新增 `drift`） |
| `skills/external/create-docs/scripts/docs-utils.py` | `.specify/skills/create-docs/scripts/docs-utils.py`（同一对的子路径） | 同上；另加 `diff -q skills/external/create-docs/scripts/docs-utils.py .specify/skills/create-docs/scripts/docs-utils.py` 无输出 |
| `skills/external/improve-docs/SKILL.md` | `.specify/skills/improve-docs/SKILL.md`（同一对） | 同上；**另有一条独立守卫**：`pytest tests/contract/test_expression_compatibility.py -q` 相对基线无新失败（本行是唯一需要 `ALLOWED_POST_BASELINE_CHANGES` 条目的文件，见 T-001） |
| `templates/commands/docs.md` | 四家 per-tool 副本（`regen-command-copies.py` 逐工具生成，**无** `.specify/templates/commands/` 镜像——该子树两侧都已退役）：`.claude/commands/speckit.docs.md`；`.github/prompts/speckit.docs.prompt.md`；`.opencode/command/speckit.docs.md`；`.qoder/commands/speckit.docs.md` | `<venv>/bin/python scripts/python/regen-command-copies.py --check` —— 相对基线无新漂移，且新内容在四家副本里逐字出现 |
| `docs/concepts/documentation-model.md` | **无镜像、无生成副本**（`docs/` 树不在任何 `MIRROR_PAIRS` 内） | 无镜像判据；唯一约束是 `pytest tests/contract/test_directory_governance.py -q` 相对基线无新失败（该文件须留在 area-map 清单内，`C-014`） |
| `tests/**`（新增夹具与单测） | **无镜像**（`tests/` 不在任何 pair 内） | 无镜像判据 |
| `tests/contract/test_expression_compatibility.py`（追加 allowlist 条目） | **无镜像** | 该文件自身的哈希不在冻结清单内；修改由 T-001 的判别证据覆盖 |

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
| 本仓当前的载体集合是 23 份（六类正式目录 22 份 + 根 `ARCHITECTURE.md`） | 实测 | 2026-11-06 | `quickstart.md` S2 的一次性只读扫描（`concepts/ 12 · tutorials/ 2 · tasks/ 1 · reference/ 1 · decisions/ 5 · contribute/ 1` = 22，+1） |
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
| 配套图义务的检查接口、封闭 verdict/reason 集、`stale` 逐面判据、两份记录 schema | `.specify/specs/087-arch-diagram-docs/contracts/diagram-obligation.contract.md` | 整文件（`C-001`…`C-015`） |
| 义务在两条流程与命令模板上的落地条款 | `.specify/specs/087-arch-diagram-docs/contracts/flow-obligations.contract.md` | 整文件（A–F 组） |
| 引擎层、路由矩阵、语义模型、交付契约、拒绝语义 | `skills/external/draw-diagram/SKILL.md` + `skills/external/draw-diagram/references/routing-matrix.md` | § 路由 / 交付（整文件即 owner，按技能正文的章节引用） |
| 流程类别（execution / expression）的判据与台账 | `.specify/shared/definitions/flow-class-definitions.md` | 整文件 |
| 六个门禁面与阶段算子表、证据分级与 as-of | `.specify/shared/workflow/expression-gates.md` | § 六面 / § 阶段算子表 / § 证据分级与 as-of |
| 容忍带、反 churn、干跑计划的引擎语义 | `.specify/shared/patterns/reconcile-pattern.md` | 整文件 |
| 面向用户的措辞与基准读者 | `.specify/shared/guidelines/user-facing-comprehension.md` | § 基准读者与覆盖协议 |
| 069a 的冻结基线与放行登记 | `tests/contract/test_expression_compatibility.py` | `ALLOWED_POST_BASELINE_CHANGES` / `WIRING_SKILLS`（代码即 owner） |
| 文档型含义给读者的投影（不定义规则） | `docs/concepts/documentation-model.md` | 整文件（读者投影） |

## Complexity Tracking

N/A — § Constitution Check 的 19 行全部 `✅ Pass`，无 `❌ Fail`、无 `⚠ Partial`，因此没有需要在复杂度跟踪里辩护的违规。三处最容易变成 `Partial` 的面已由设计消化：VII（Feature 只走到 `Planned`，不越 Pre-Status-Flip Gate）、IX（零新建引擎/命令/目录/依赖）、XIV（义务与取值域各只有一个定义点，其余全按路径引用）。

## Residual Risk

本特性**显式登记**一项未覆盖的能力面（不是缺陷，是判据尚不存在）：

| ID | 未覆盖的面 | 为什么本特性不判 | 承接方 | 重开条件 |
|----|-----------|------------------|--------|----------|
| D-001 | 图内标签 / 关系与文档正文所述事实的**语义**一致（`stale` 的第二半，见 T-003） | 检查器只读、无第三方依赖、无图形解析器（research R3/R4）；依赖 LDM 摘要的实现会把「本特性之前产生的手工图」判成假红 | `/speckit.review` 的评审面 + 后续特性（补语义判据时按 T-003 的 `revision_trigger` 重开） | `--action obligation` 的 `no-trace-record` 计数显著下降（LDM 摘要已普遍落盘），或评审面连续两次报出「机械绿但图文语义不一致」 |

已登记、但**不是**本特性风险的未决项：`OI-087-01` —— `checklists/requirements.md` 的派生计数副本与「23 FR / 10 SC」的实际计数共存（owner：`/speckit.checklist`；处置归 requirements 收尾；本阶段不改写，见 § Inherited Blockers 的最后一行）。

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
| Contracts | [`contracts/`](./contracts/) | 2 份：`diagram-obligation.contract.md`（`C-001`…`C-015`）、`flow-obligations.contract.md`（A–F 组，`C-001`…`C-023`） |
| Quickstart | [`quickstart.md`](./quickstart.md) | 8 个场景（S1–S8），其中 S1/S2/S6/S7/S8 含规划期实测读数 |
| Feature ref | [`feature-ref.md`](./feature-ref.md) | 绑定表 + 10 行交付面 + 6 组 FR→契约映射 + 10 行 SC→计量 + 5 条已披露裁定 |
| Decision Tensions | 本文件 § Decision Tensions | 5 条（T-001…T-005），`validate-decision-tensions.py` 实测 `ok` / 5 record(s) / 0 error |
| Test evidence | `test-evidence/plan-stage-status.md` | 本阶段各校验命令的**实跑读数**（见下） |

**与 Phase 0 预期的漂移**：Phase 0 预期「两份契约覆盖 RS-006 的两半 + 流程接线」；实际落地时多发现一处需要机械纠正的口径——`C-001` 初稿把 `--root` 写成「文档空间根」，而 `docs-utils.py` 的既有动作一律以**项目根**为根（`--action validate --root .` 的实读输出证明）。该纠正已就地落进 `C-001`/`C-010`/`C-011`（`<root>`），并在本阶段回传中披露：它是**纠正**（恰有一种与既有引擎一致的读法），不是裁定。契约条款数因此从 15+23 不变，但三处路径口径改为统一引用 `C-001`。

**本阶段实跑的校验与读数**（命令与输出逐条对应，完整记录见 `test-evidence/plan-stage-status.md`）：

```text
python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs
  -> status: ok ; scanned: 370 lines, 5 record(s) ; 0 error(s), 0 warning(s)
python3 .specify/scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/087-arch-diagram-docs
  -> class=execution source=declaration ; status: not-applicable ; two-way: not-run ; files_scanned: 1
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/087-arch-diagram-docs --stage plan
  -> decision=pass errors=0 advisories=0 waived=0（fr=23 sc=10 files=9）
python3 scripts/python/sync-mirrors.py --check（裸解释器）
  -> exit 2: ModuleNotFoundError: No module named 'typer'（内嵌 regen 调用；六对镜本身全 ok）
/tmp/087-toolenv/bin/python scripts/python/sync-mirrors.py --check     -> exit 0，六对镜全 ok
/tmp/087-toolenv/bin/python scripts/python/regen-command-copies.py --check -> exit 0，"OK: all per-tool command copies match the source templates."
```

⇒ 实施期的镜像判据 MUST 用能 import `typer` 的解释器，否则量到的是环境缺口而不是漂移。
