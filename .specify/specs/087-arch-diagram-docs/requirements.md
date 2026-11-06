# Requirements Specification: 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space）

**Requirement Branch**: `087-arch-diagram-docs`
**Created**: 2026-11-06
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "以087-* 为前缀开发一个需求,在原本speckit.docs命令的基础上,让docs文档整体结构改造成以架构图为核心, 重复发挥 spec-kit/skills/external/draw-diagram 技能的能力,在生成文档的时候都需要进行架构图的配套."

> **本行的由来（自用声明）**：本规格由本线作者按 `.specify/shared/definitions/flow-class-definitions.md` § 判据自行判定，判据与理由见 § Assumptions A1。`Flow Type` 写 `-`（`execution` 线只允许 `-`）。本阶段读到的类别记录见 A1 末尾的复读行。

## Related Feature *(mandatory)*

**Feature ID**: 087
**Feature Name**: 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space）

**绑定结论**：绑定**新建 Feature 087**（`Draft`，2026-11-06 由本阶段按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 绑定并登记）；登记行与详情文件随本阶段落盘（`.specify/memory/features.md` 索引行 + `.specify/memory/features/087.md`）。**不**把本规格挂到任何既有 Feature 名下。绑定证据见 `## Clarifications` `### Session 2026-11-06` 的 Q1 行与下面的 reuse-first 复核表。

**与直接前序的关系（只引用、不回写）**：Feature 037（Docs Command，`Implemented`）持有 `/speckit.docs` 命令本体、`create-docs` / `improve-docs` / `create-pages` 三个技能的归属划分与单一 reconcile 引擎；Feature 069（`Implemented`）持有「执行/表达」分类与文档型门禁；Feature 069a 与 Feature 077 持有文档型门禁的落地点与阶段命令接线。本特性**不重写**这些契约，只在其中做「配套图义务」类的**追加**（FR-001 的落点即 069a 的 W3 接线面）。这三个 Feature 的正文与状态 MUST NOT 因本特性改写或回退。

**reuse-first 复核（宪法 VII；判据是「该 Feature 是否已拥有本特性要建立的能力」，不是「是否持有交付载体」）**：

| 候选 Feature | 与本特性的关系 | 裁决 |
|---|---|---|
| 037 Docs Command | 拥有 `/speckit.docs` 命令、文档空间基线与两个写入技能的职责划分；**不拥有**「文档必须配套架构图」这一义务，也不拥有绘图能力（其 `docs/` 文档至今零 diagram 命中） | 交付载体，不是归属 |
| 069 执行/表达二元分类与文档型 SDD 同构 | 拥有分类判据与六面文档型门禁；不拥有图与文档的配套关系 | 无关 |
| 069a 分类与文档型门禁落地 / 077 文档的 SDD 接入 | 拥有门禁算子与阶段命令接线（本特性 A7 要动的 W1/W3 面）；不拥有图的义务 | 需追加的接线面，不是归属 |
| 084 Harness 三重结构 | 拥有「以核心实体为中心的交付物形态」这一表述方式；对象是 harness 载体，不是文档空间 | 表述先例，不是归属 |
| 085 SDD 临时 Goal/Team 与多 Agent 并发 | 编排层；对象是团队与目标协同 | 无关 |

**结论与理由**：037 打开的是文档空间的**结构**能力（分类法、期望态基线、调谐引擎），本特性打开的是文档空间的**内容形态**能力（每份正式文档是否配了能解释其所描述结构的架构图，以及如何机器判定）。二者分属不同能力域，且 037 已关闭：把本规格挂到它会重新解释一份已交付的契约。叠加第二条证据：本仓既有 `skills/external/draw-diagram/` 前门存在，但 `create-docs` / `improve-docs` / `templates/commands/docs.md` / `docs/concepts/documentation-model.md` 对 "diagram" 零命中——能力已存在而没有任何写入流程消费它，是一个**新**义务，不是既有义务的加固。故新建 087，并在 037 与 069a/077 的 owner 文件中只做**类条件追加**。

**编号占用核对**：086 未被占用（`.specify/memory/features.md` 索引行与 `.specify/specs/` 目录均无 086）；本特性占用 087。

## Overview

The user's request, read as one coherent change: **the `docs/` documentation space stops being organised around prose document types and starts being organised around the architecture diagram.** Every document the framework produces for a project gains a diagram that goes with it, and the diagram is what the reader actually looks at.

Two inputs constrain the shape of the change and MUST NOT be re-invented here:

- **Existing surface.** `/speckit.docs` (`templates/commands/docs.md`) is already a thin orchestration layer over three owning skills — `create-docs` (structure and authoring), `improve-docs` (content of an existing document), `create-pages` (optional presentation). The documentation taxonomy, the reserved root filenames, and the reconcile engine all live in `skills/external/create-docs/SKILL.md` § Desired-State Baseline; the reader-facing explanation lives in `docs/concepts/documentation-model.md`.
- **Existing drawing capability.** `skills/external/draw-diagram` already is the single front door of every diagram capability: it builds a semantic logical-diagram model (LDM), routes to one of six engine layers, delegates rendering, and accepts the result against the LDM plus a delivery contract. It is **not** to be duplicated, wrapped in a second engine, or reached around.

This feature therefore changes **what the documentation space is required to contain and how its two writing flows produce it**, and adds the *check* that makes "a diagram accompanies this document" a decidable fact rather than an aspiration. It does not author a new drawing engine, a new document type directory, or a second docs command.

**Two Hats (framework source vs client runtime).** This is a framework-level change. Source edits land in `templates/`, `skills/`, `shared/`, `scripts/`, `src/` and `tests/`; the `.specify/` tree of a consuming project receives them only as regenerated mirrors and rendered command copies. A direct edit to a project's `.specify/` would never reach another project and is out of scope.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A newly authored document arrives with its architecture diagram (Priority: P1)

An author asks `/speckit.docs` for a new document ("写一份部署教程", "新增 xxx 的概念文档"). Today the framework writes the Markdown, indexes it, and validates it. With this feature, the same commission produces the document **and** the diagram that explains the structure it describes: the diagram's editable source and its rendered image live alongside the document, the document embeds or links them, and the run does not report itself complete if the diagram is missing.

**Why this priority**: This is the user's literal ask — "在生成文档的时候都需要进行架构图的配套" — and it is the only story that changes what an author actually receives. Without it the rest of the feature is a rulebook with nothing to govern.

**Independent Test**: In a fixture documentation space, issue a writing commission for a single new concept document. Observe that the run produces (a) the document, (b) a diagram source file, (c) the rendered image the diagram's delivery contract requires, and (d) an embed or link from the document to the rendered image — and that removing (b) or (c) before the run's verification step turns the run's own verdict red.

**Acceptance Scenarios**:

1. **Given** a documentation space with no document on topic X, **When** an author commissions a new document on topic X, **Then** the run creates the document and, in the same run, a diagram whose semantic model covers the components and relations the document describes, and the document references the rendered diagram by a relative path that resolves on disk.
2. **Given** the same commission, **When** the run reaches its verification step, **Then** the verification reports the diagram's source file, its rendered artifact(s), and the document's reference to them as present — and reports a named, blocking finding if any of the three is absent.
3. **Given** a commission whose subject genuinely has no structure to draw (e.g. a changelog-shaped chronological list), **When** the run classifies it, **Then** the run records an explicit, named exemption for that document rather than silently omitting the diagram, and the absence of a diagram is visible in the run's report.
4. **Given** a document produced by this flow, **When** a reader opens it, **Then** the diagram appears in the document body or is reachable by one relative link from it, and the document's prose does not merely restate what the diagram already shows.

---

### User Story 2 - The documentation structure baseline itself is diagram-centric (Priority: P1)

The desired-state baseline that `create-docs` reconciles toward is amended so that "has an accompanying diagram" is part of a compliant document, not an optional extra. A reader who lands anywhere in `docs/` — or at the root `ARCHITECTURE.md` signpost — meets the architecture first and the prose second. The root one-screen entry preserves its existing role and gains an explicit pointer to where the architecture picture lives.

**Why this priority**: The user asked for the *overall structure* to become diagram-centric ("让docs文档整体结构改造成以架构图为核心"). Story 1 changes one authoring run; this story changes the target every run converges toward, which is what makes the change durable across runs.

**Independent Test**: Run a full `/speckit.docs` reconcile over a fixture space whose documents are all compliant with today's baseline. Observe that the reconcile's dry-run plan and residual report now classify the missing diagrams as findings against the new baseline, and that a second run after convergence reports zero diagram findings.

**Acceptance Scenarios**:

1. **Given** a documentation space compliant with the pre-change baseline, **When** a full reconcile runs, **Then** every formal document lacking an accompanying diagram is reported as a finding against the amended baseline, grouped in the residual report by owning skill.
2. **Given** the same space after that finding is converged, **When** the reconcile runs again, **Then** the diagram dimension reports no new findings and the run performs no cosmetic churn (the existing tolerance-band / anti-churn rule already governs).
3. **Given** a project whose documentation root carries `ARCHITECTURE.md`, **When** the amended baseline is applied, **Then** the entry's existing fixed semantics and one-screen ceiling are preserved and it carries a pointer to the diagram material rather than duplicating it.
4. **Given** the taxonomy of formal document directories, **When** the amended baseline is read, **Then** the diagram accompanies documents **within** the existing taxonomy; no new top-level document-type directory is invented to hold diagrams.

---

### User Story 3 - Content improvements keep the diagram in step with the prose (Priority: P1)

An existing document is improved for staleness: a component was renamed, a relation changed, a step was reordered. Today `improve-docs` edits the prose and stops. With this feature, an improvement that changes a fact the document's diagram depicts also updates that diagram in the same run, or reports that the diagram is now stale and why, so a document and its picture cannot silently diverge.

**Why this priority**: The user asked for diagram accompaniment at the level of the whole space; an accompaniment that rots on the first content edit is worse than none, because it teaches readers to distrust the picture. This is also the only story that closes the loop between the two writing flows the command already dispatches.

**Independent Test**: Take a document with a converged diagram; edit prose so a depicted component's name changes; run the content-improvement flow. Observe that the run either updates the diagram source and re-renders it, or reports a named staleness finding — and never reports completion with the document and diagram disagreeing and no finding raised.

**Acceptance Scenarios**:

1. **Given** a document whose diagram depicts a component, **When** an improvement changes that component's name in the prose, **Then** the same run updates the diagram's semantic model accordingly and re-renders, leaving the document reference resolving to the new artifact.
2. **Given** an improvement whose scope reaches a depicted fact, **When** the run cannot re-render (for example the diagram engine layer is unavailable in this environment), **Then** the run reports a named, visible finding that the diagram is stale and MUST NOT report the improvement as complete.
3. **Given** an improvement that touches only prose the diagram does not depict, **When** the run completes, **Then** it performs no diagram work and says so, rather than re-rendering to manufacture activity.
4. **Given** a document whose diagram was produced by a different engine layer than the run would choose today, **When** the diagram must be updated, **Then** the run updates that diagram in its existing engine rather than silently re-routing it to a different one and replacing the author's source.

---

### User Story 4 - Every produced diagram is traceable to the drawing capability the framework already owns (Priority: P2)

An auditor or maintainer asks: was this diagram produced by the framework's declared drawing capability, or was it improvised? With this feature, any diagram the documentation flows produce is traceable to `draw-diagram`'s semantic model plus its delivery-contract acceptance — so the diagram can be re-checked and re-rendered later, and the framework has exactly one drawing capability rather than one per writing flow.

**Why this priority**: The user named the reuse requirement directly ("重复发挥 spec-kit/skills/external/draw-diagram 技能的能力"). It is P2 rather than P1 because it constrains *how* Stories 1–3 are satisfied; it delivers no reader-visible outcome of its own, but without it the earlier stories would be satisfied by a second improvised drawing path.

**Independent Test**: Inspect the run record of a document produced by Story 1 and confirm it names the selected drawing engine layer, carries the semantic-model summary the capability requires, and records the delivery-contract acceptance result — while a search of the framework sources finds no drawing engine, renderer, or engine-routing table introduced by this feature.

**Acceptance Scenarios**:

1. **Given** a run that produced a diagram, **When** its record is read, **Then** it names the selected engine layer and why that layer was selected, and carries the semantic-model summary and the delivery-contract acceptance outcome.
2. **Given** the framework source tree after this feature lands, **When** it is searched for a second drawing engine, engine routing table, or renderer introduced by this feature, **Then** none exists — the documentation flows reach the existing capability by reference and delegate to it.
3. **Given** the drawing capability is unavailable in the executing environment, **When** a documentation flow needs a diagram, **Then** the failure is surfaced in the existing loud-and-explicit way that capability already defines, and is not converted by the documentation flow into a silent skip or a locally improvised render.

---

### User Story 5 - A reviewer can tell, without reading every document, which ones are out of step (Priority: P2)

A maintainer wants a mechanical answer to "which documents still lack a diagram, which diagrams no longer match their document, and which documents were exempted". With this feature, the check is deterministic and re-runnable, so the answer is a verdict rather than an impression, and a second run on an unchanged space says "nothing to do" instead of manufacturing work.

**Why this priority**: The accompaniment obligation is only real if a machine can refuse it. It is P2 because it strengthens Stories 1–3 rather than adding a new reader-facing outcome.

**Independent Test**: On a fixture space with a known set of missing and stale diagrams, run the check twice. Observe identical verdicts both times, a stable finding set keyed by document, and a clean space reporting zero findings rather than a vacuous pass.

**Acceptance Scenarios**:

1. **Given** a documentation space with a known set of documents missing diagrams and a known set with stale diagrams, **When** the check runs, **Then** it reports each affected document by path with a named reason, and the count matches the known set.
2. **Given** the same unchanged space, **When** the check runs a second time, **Then** it produces the same verdict and performs no writes.
3. **Given** a document carrying a recorded exemption, **When** the check runs, **Then** the exemption is reported as an exemption — visible, named, and distinct from a pass — and an exemption that no longer applies is reported rather than left silently in force.
4. **Given** the check cannot evaluate a document (unreadable path, unavailable engine), **When** it runs, **Then** that document is reported as not evaluated and the check does not report the space as clean.

---

### Edge Cases

- **A document with genuinely nothing to draw** — a changelog, a pure reference table of flags, a licence page. The obligation needs a named, recorded exemption path; an unrecorded absence is a finding, a recorded one is not.
- **A reserved root file that is a formal document but not a diagram carrier.** `README.md`, `CONTRIBUTING.md` and `CHANGELOG.md` have fixed one-screen semantics owned by the baseline; they carry FR-001's pointer obligation, not the accompanying-diagram obligation. A check MUST NOT report them as `missing`, and MUST NOT treat "no diagram" as an exemption either — they are simply outside the carrier set (FR-003). Treating them as missing would make every conforming project start non-compliant on day one.
- **A diagram whose engine layer cannot render in this environment.** The drawing capability already refuses to silently degrade; the documentation flows must not convert that refusal into "document done, diagram skipped".
- **A document that embeds a diagram belonging to a different document.** One picture cited by several documents is legitimate; the obligation is that each formal document has an accompanying diagram, which such a citation may satisfy — but then that shared diagram needs an identifiable home, and updating it must not fork into per-document copies.
- **A rendered image edited or deleted while the source survives** (or the reverse). Source and rendered artifact are two faces of one deliverable; losing either leaves the document unverifiable.
- **A diagram whose two faces disagree with each other while both still exist** — the source was edited and never re-rendered, or the image was hand-edited. This is `stale` under FR-014's first half and MUST be reported; it is not `satisfied` merely because both files resolve on disk.
- **A space that already contains hand-made diagrams** produced before this feature. Convergence must not silently replace an author's diagram with a re-routed one; the existing never-clobber and target-declaration rules govern.
- **A diagram that passes structure checks while being factually wrong** — the diagram renders, the link resolves, and the picture contradicts the prose. Structure passing is a necessary condition and never sufficient; the reader-facing judgement belongs to review.
- **A document produced by a project that has not refreshed its `.specify/` runtime.** The obligation must degrade visibly (existing wiring rules) rather than pretend the diagram exists.
- **Two documents authored concurrently that both want the same diagram.** The existing "add a writing agent's isolation and integration" discipline governs; this feature must not create a shared mutable diagram store.

## Requirements *(mandatory)*

### Functional Requirements

**A. The diagram-centric structure baseline**

- **FR-001**: The documentation space's desired-state baseline MUST be amended so that an accompanying architecture diagram is part of a compliant formal document. The amendment MUST land in the baseline's owning location — `skills/external/create-docs/SKILL.md` § Desired-State Baseline — and every other surface MUST cite it by path plus section anchor rather than restate its contents. The user-facing explanation in `docs/concepts/documentation-model.md` MUST be brought into agreement with the owner in the same change and MUST remain a reader-facing explanation, not a second rulebook.
- **FR-002**: The diagram obligation MUST apply **within** the existing formal document taxonomy. This feature MUST NOT introduce a new top-level document-type directory for diagrams, and MUST NOT change the fixed semantics or the registered location of any reserved root filename.
- **FR-003**: The obligation MUST apply to formal documents (the typed `docs/` directories and any diagram-bearing root entry) and MUST NOT be applied to the temporary `notes/` zone, whose lifecycle rules are already owned elsewhere and whose documents carry no stability guarantee. The obligation's **carrier set** is: every document inside the six formal type directories, plus the reserved root file whose fixed semantics already summarize the architecture (`ARCHITECTURE.md`). The other reserved root files — `README.md` (root index), `CONTRIBUTING.md` (contribution entry), `CHANGELOG.md` (self-contained timeline) — are compliant formal documents but are **not** carriers: a one-screen index or timeline has no architecture structure to depict, so they carry the pointer obligation of FR-001 (point at the diagram material, never duplicate it) instead. Their fixed semantics and registered location are governed by the baseline owner and MUST NOT be changed by this feature.
- **FR-004**: The diagram obligation MUST be expressible as a **named exemption**: a document that genuinely has no structure to depict MUST be able to carry a recorded, visible exemption, and an exemption whose justification no longer holds MUST be reportable. An unrecorded absence MUST NOT be treated as compliant, and a recorded exemption MUST NOT be reported as a pass.

**B. The accompanying-diagram obligation in each writing flow**

- **FR-005**: When the framework creates a document for a project, the same run MUST produce the document's accompanying architecture diagram: its editable source, and the rendered artifact(s) that the drawing capability's delivery contract requires for the selected engine layer. The document MUST reference the rendered artifact by a relative path that resolves on disk.
- **FR-006**: When the framework improves the content of an existing document, and the improvement changes a fact the document's diagram depicts, the same run MUST bring the diagram back into step — either by updating it or by reporting a named staleness finding. A run MUST NOT report the improvement as complete while the document and its diagram disagree and no finding has been raised.
- **FR-007**: An improvement that touches only content the diagram does not depict MUST NOT trigger diagram work. The run MUST say that no diagram work was needed rather than performing it to demonstrate activity.
- **FR-008**: Both flows MUST treat the diagram as one deliverable with two faces — an editable source and its rendered artifact(s) — and MUST report the two faces separately. The loss of either face while the other survives MUST be reported.
- **FR-009**: A document MUST be able to satisfy the obligation by citing a diagram that has a single identifiable home rather than a per-document copy. Where several documents cite one diagram, that diagram MUST have exactly one editable source, and an update to it MUST NOT fork into copies.
- **FR-010**: Where an existing document already carries a diagram, an update MUST preserve that diagram's engine choice and editable source. The flows MUST NOT silently re-route an existing diagram to a different engine and replace the author's source. Introducing a brand-new diagram is the only case where engine selection happens afresh.

**C. Reuse of the framework's one drawing capability (no second engine)**

- **FR-011**: Every diagram produced by the documentation flows MUST be produced through the framework's existing drawing capability — `skills/external/draw-diagram` — reached by reference. This feature MUST NOT introduce a second drawing engine, a second renderer, a second engine-selection table, or a second diagram delivery contract. Where a documentation surface needs to state how a diagram is built, it MUST cite that capability's own owner sections rather than paraphrase them.
- **FR-012**: The documentation flows MUST carry through the drawing capability's own refusal semantics: when the capability declines to produce or render a diagram, the documentation flow MUST surface that refusal and MUST NOT convert it into a silent skip, a locally improvised render, or a "document complete without diagram" verdict.
- **FR-013**: A run that produces a diagram MUST record its traceability: the selected engine layer and the reason for that selection, the semantic-model summary of what the diagram covers, and the delivery-contract acceptance outcome. A produced diagram without that record MUST be treated as an unaccepted diagram. The record is written by the **run that produces or changes the diagram** — through the documentation flow's existing run-artifact location and audit log, not through the FR-014 check — so a read-only check run neither writes it nor is required to. A check that reads a diagram whose producing run left no record MUST report it as unaccepted rather than as satisfied.

**D. The decidable check**

- **FR-014**: The framework MUST provide a **deterministic, re-runnable check** that judges, per document, whether the diagram obligation is satisfied. It MUST report each affected document by path with a named reason, MUST distinguish "satisfied", "missing", "stale", "recorded exemption", and "not evaluated", and MUST report an un-evaluable document as not evaluated rather than as satisfied. **`stale` is the union of two conditions** — the diagram's two faces are inconsistent with each other, **or** the diagram disagrees with the document on the same fact — and its per-face decision criteria MUST be frozen by plan at the owner of this closed reason vocabulary (RS-006). If plan cannot make `stale` decidable, it MUST report that face as not covered rather than leave a verdict with no criteria.
- **FR-015**: The check MUST be idempotent over an unchanged space: two consecutive runs MUST produce the same verdict, and the check MUST be read-only. It MUST NOT be used to write or to converge; convergence remains the documentation flows' job. "Read-only" is absolute: the check MUST NOT write anything into the documentation space, including a semantic-model summary or a delivery-contract acceptance summary. Findings are therefore re-derived from the live state of the source, the rendered artifact and the document on every run — never from a record that, once edited, would make out-of-step documents undetectable.
- **FR-016**: The check's finding vocabulary MUST be a closed, named set, and every finding MUST name the document path it concerns. A space with no affected documents MUST report zero findings as an explicit clean verdict; a check that cannot run MUST NOT be reportable as clean.
- **FR-017**: The check MUST be reachable from the existing documentation flows' verification steps rather than requiring a new user-facing command. This feature MUST NOT add a new `/speckit.*` command. This obligation is a **reachability claim on an existing flow** and adds no new confirmation tier: the check is a read-only verification step, and the diagrams it evaluates are safe-local writes that `create-docs` § Tiered Confirmation already auto-executes. Moving, archiving or restructuring a document while bringing a space into line stays under that flow's existing stop-and-confirm tier (FR-019 / FR-021), unchanged.

**E. Boundaries: what this feature does not become**

- **FR-018**: This feature MUST NOT change the existing division of ownership among `/speckit.docs`, `create-docs`, `improve-docs` and `create-pages`. Structure stays with `create-docs`, content of an existing document with `improve-docs`, optional presentation/publishing with `create-pages`. The diagram obligation is an addition to what each of those must produce, not a reallocation between them.
- **FR-019**: This feature MUST NOT change the existing confirmation tiers, the archive-not-delete rule of the formal zone, the reading order of the drawing capability's routing (the routing order is that capability's own decision and MUST NOT be amended here).
- **FR-020**: This feature MUST NOT weaken the read-only and anchor zones that the documentation flows already respect, and MUST NOT cause diagrams to be triaged as ordinary prose content or archived as documents.
- **FR-021**: This feature MUST NOT silently re-classify any existing project document as non-compliant in a way that destroys content. Bringing an existing space into line MUST happen under the flows' existing dry-run-plan, tolerance-band and stop-and-confirm rules for actions that move, restructure or archive.

**F. Evidence and verification obligations**

- **FR-022**: For each document the flows produce or update, the run's evidence MUST include: the diagram's editable source path, its rendered artifact path(s), the document's reference to the rendered artifact, and the record required by FR-013. These four MUST be present in the run report; a report that asserts a diagram without them MUST NOT be treated as evidence.
- **FR-023**: The feature MUST provide an observable negative case: on a fixture where the diagram is deliberately absent (or one of its faces is removed) after the document is written, the framework's own verification MUST go red and name the missing face. A check that stays green when the subject is broken MUST be treated as unverified, not as satisfied.

### Key Entities

- **Accompanying diagram**: the architecture picture that belongs to one document — its editable source, its rendered artifact(s), and the document's reference to them. Two faces of one deliverable; neither alone is the deliverable.
- **Diagram obligation record**: per-document judgement of the obligation — satisfied, missing, stale, recorded exemption, or not evaluated — with a named reason and, for exemptions, the recorded justification.
- **Diagram traceability record**: produced per diagram-generating run — selected engine layer plus selection reason, semantic-model summary, delivery-contract acceptance outcome.
- **Diagram-bearing root entry**: the existing one-screen root signpost whose fixed semantics already summarize the architecture; it points at diagram material rather than duplicating it.

### Runtime Stack & Dependency Ownership

本特性交付的运行时能力是下表的 `in-scope` 三行：义务如何被判定与如何被改（`reason` 枚举 + 复核流程）、检查器动作、以及承载本文义务的文档空间。其余四项由外部供给、本仓只消费，按 `signed-contract` 记——其中 `draw-diagram` 的两行是本特性最实质的依赖：读法正确性与交付契约（源 + 渲染产物两面）是 FR-005 / FR-008 / FR-013 的前提。该表是 SC-001、SC-002、SC-004、SC-005、SC-006 的运行时前提；本阶段无 `user-waived` 行。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行检查器、引擎动作与守卫测试） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不新增 pin；新增脚本 stdlib-only） | `pyproject.toml` | 新增与改动的测试在 `>=3.8` 解释器上通过；新增脚本无第三方 import | FR-019 | EP-001 |
| RS-002 | pytest（守卫测试运行器） | signed-contract | pytest 上游（本仓只消费） | 无声明 pin；执行时以 `pytest --version` 原文记录进 test-evidence | `scripts/bash/run-tests.sh` | 基线差集为空，且 FR-023 的负向夹具在同一 pin 上全绿 | FR-023 | EP-001 |
| RS-003 | `draw-diagram` 技能前门（LDM 语义模型、路由、交付契约、验收与拒绝语义）——本特性只消费，不新建引擎 | signed-contract | `skills/external/draw-diagram/SKILL.md` | 同一提交（框架源与 `.specify/` 镜像同一次生成；本特性 MUST NOT 改动该技能） | `skills/external/draw-diagram/SKILL.md` | 每个产出图都带 FR-013 的记录（引擎层 + 选择理由 + LDM 摘要 + 交付契约验收结论），且仓内搜索找不到本特性引入的第二引擎或第二交付契约 | FR-011, FR-012, FR-013 | EP-001 |
| RS-004 | 共享渲染后端可用性 preflight 与自部署回退（六引擎共用的 `xuanji-render` 服务，环境特定） | signed-contract | `skills/external/draw-diagram/SKILL.md` § Step 2.5（前门统一持有） | 无声明 pin；执行时把 `healthz` preflight 的原文读数记录进 test-evidence | `skills/external/draw-diagram/references/self-deploy-render-service.md` | 后端不可达的夹具上，文档流程报出该技能既有的响亮失败，MUST NOT 出现静默跳过或本地即兴渲染（FR-012 / SC-002）；后端可达的夹具上图正常产出（SC-001） | FR-012, FR-005 | EP-001 |
| RS-005 | `create-docs` 与 `improve-docs` 两个写入技能及其验证步骤（本特性在其上追加配套图义务） | in-scope | 本仓 `skills/external/create-docs/SKILL.md` § Desired-State Baseline 与其 Authoring Flow、`skills/external/improve-docs/SKILL.md` § Workflow | 同一提交 | `skills/external/create-docs/SKILL.md` | SC-001（新建文档四件产物齐备且验证报 present）与 SC-004（改名后文档与图一致或留下具名 staleness finding） | FR-001, FR-006, FR-007, FR-008, FR-017 | EP-001 |
| RS-006 | 检查器的理由词表：FR-016 的封闭 finding 集合，以及 FR-004 具名豁免的 `reason` 枚举 | in-scope | 本特性 plan 阶段确定的检查器接口（取值域 owner 在 plan 冻结；FR-016 拥有「封闭」这一性质） | 同一提交 | `skills/external/create-docs/SKILL.md` | SC-006（两次运行同 verdict、每份受影响文档按路径给出集合内的理由、干净空间零 finding、不可评估文档报 not evaluated）与 SC-008（豁免可见且失效可报） | FR-014, FR-015, FR-016, FR-004 | EP-001 |
| RS-007 | 文档检查引擎的既有动作与验证步骤（被 FR-017 的既有验证步骤触达；形态归 plan，A4） | in-scope | 本仓 `skills/external/create-docs/scripts/docs-utils.py` | 同一提交 | `skills/external/create-docs/scripts/docs-utils.py` | SC-003（reconcile 报出告缺文档、收敛后二次运行零图 finding 且无 cosmetic churn）与 SC-009（只读区、锚区、归档不删除与确认分级可观测地未变） | FR-017, FR-019, FR-020 | EP-001 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fixture documentation space in which a single document is authored through the documentation flow yields all four required artifacts — document, diagram source, rendered artifact, and a resolving relative reference — and the flow's own verification reports the diagram dimension as present. **Path**: final
- **SC-002**: On the same fixture, removing the diagram's rendered artifact after a green run makes the flow's next verification go red with a finding that names both the document and the missing face; removing the source instead produces the correspondingly named finding. **Path**: final
- **SC-003**: A reconcile over a fixture space compliant with the pre-change baseline reports every formal document lacking a diagram as a named finding, and after convergence a second reconcile reports zero diagram findings and performs no cosmetic change. **Path**: final
- **SC-004**: A content improvement that renames a depicted component leaves the document and its diagram in agreement, or leaves a named staleness finding — never a green run with the two disagreeing. **Path**: final
- **SC-005**: A search of the framework source tree finds no drawing engine, renderer, engine-selection table, or diagram delivery contract introduced by this feature; every diagram-producing surface reaches the existing drawing capability by reference. **Path**: final
- **SC-006**: The deterministic check produces identical verdicts on two consecutive runs over an unchanged fixture space, reports each affected document by path with a reason from the closed vocabulary, reports zero findings on a clean space, and reports un-evaluable documents as not evaluated. **Path**: final
- **SC-007**: Every diagram the flows produce carries a traceability record naming its engine layer, selection reason, semantic-model summary, and delivery-contract acceptance outcome; a produced diagram missing any of these is reported as unaccepted. **Path**: supporting
- **SC-008**: A document that genuinely has nothing to depict converges with a recorded, visible exemption, and an exemption whose justification no longer holds is reported rather than silently retained. **Path**: supporting
- **SC-009**: The documentation flows' read-only zone, anchor zone, archive-not-delete rule and existing confirmation tiers are observably unchanged: a fixture run that would move or archive still stops for confirmation, and no diagram artifact is triaged as ordinary prose content. **Path**: supporting
- **SC-010**: A project that has not refreshed its `.specify/` runtime, when it runs a documentation flow, degrades visibly — the diagram obligation is reported as not evaluated rather than as satisfied — and the flow produces no false green. **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: Fixture run under `tests/fixtures/`, with the run report and the on-disk artifact listing (document, source, rendered artifact, reference target) captured into the feature's `test-evidence/`.
- **SC-002 Source**: The same fixture with a deletion step between the two verification runs; both runs' command lines, exit codes and full output captured to `test-evidence/` per the single-run evidence discipline.
- **SC-003 Source**: Reconcile's dry-run plan, residual report and audit-log records from the fixture space, before and after convergence.
- **SC-004 Source**: The content-improvement run record for the rename fixture, plus a byte-level comparison of the document and its diagram source before and after.
- **SC-005 Source**: Repository-wide search over `templates/`, `skills/`, `shared/` and `scripts/` for engine names and routing tables introduced by the change, recorded as the search command and its output.
- **SC-006 Source**: Two consecutive check invocations over the same fixture tree, with both outputs and exit codes captured; the clean-space case and the un-evaluable case captured from their own fixtures.
- **SC-007 Source**: The traceability record as emitted by the fixture runs, reviewed against the required four fields.
- **SC-008 Source**: The exemption fixture space and the check's verdict on it before and after the justification is invalidated.
- **SC-009 Source**: A fixture run containing a move/archive action, showing the confirmation stop; plus the flows' zone definitions read against the change.
- **SC-010 Source**: A fixture project with an unrefreshed `.specify/` runtime, its flow output, and the degraded-state label it emits.

## Boundary and Ownership (non-duplication)

This feature adds obligations to surfaces that already have owners. It creates no second owner and MUST NOT restate what an owner already defines.

| Fact this feature touches | Owner (cited, never restated) |
|---|---|
| Documentation taxonomy, reserved root filenames, one-screen ceiling, reconcile loop, confirmation tiers, zones | `skills/external/create-docs/SKILL.md` § Desired-State Baseline · § Reconcile Loop · § Tiered Confirmation |
| Content-improvement method for an existing document | `skills/external/improve-docs/SKILL.md` § Ownership boundary · § Workflow |
| Diagram capability itself: semantic model, engine routing, delivery contract, acceptance, refusal semantics | `skills/external/draw-diagram/SKILL.md` · `references/semantic-model.md` · `references/routing-matrix.md` · `references/delivery-contract.md` |
| Reconcile engine semantics (tolerance band, anti-churn, dry-run plan) | `.specify/shared/patterns/reconcile-pattern.md` |
| Flow classification and document-type gates | `.specify/shared/definitions/flow-class-definitions.md` · `.specify/shared/workflow/expression-gates.md` |
| Reader baseline and user-facing wording rules | `.specify/shared/guidelines/user-facing-comprehension.md` |
| Containment / stability claims | `.specify/shared/guidelines/closed-set-claims.md` |
| Document-type meaning for the reader | `docs/concepts/documentation-model.md` (reader-facing projection, not a rule owner) |

## Assumptions（本阶段的缺省裁决；clarify 阶段可推翻，翻转须给出证据）

裁决语法沿用本仓惯例：**adopted** = 本阶段作出选择并给出理由，clarify 可改判；**deferred** = 明确留给后续阶段裁定，本阶段不预设结论；**confirmed** = 依据仓内可复核证据成立。

- **A1（类别 = `execution`，basis = `behavior-oracle`）— 裁决：adopted**。指认主交付物：本特性最终必须交出去、并被消费者用于最终判定的那一件产物，是**一组把「文档必须配套架构图」变成可判定事实的机器面**——写入 `create-docs` / `improve-docs` 的强制性步骤与其收尾判定、一个确定性检查器、以及钉住这些行为的守护测试；读者看到的文档与图是这个机器面跑出来的结果。指认判定面：缺陷最先在**机器面**暴露——文档写完了图没生成、图生成了源文件丢了、图更新了文档没跟上、检查器对缺失图保持绿色。这些都表现为退出码、产物缺失或下游消费失败，不需要读者先读懂才发现。按 `.specify/shared/definitions/flow-class-definitions.md` § 判据，属 `execution`；`Flow Type` 只对 `expression` 有效，写 `-`。**反向读法不采纳**：本特性产出的 Markdown 占比很高（规格、模板、技能正文），但 owner § 不参与判定的因素 明写介质不参与判定；若因「交付物主要是 Markdown」判 `expression`，正是该条要禁的判据缺陷。**复读行**：类别声明写入后执行 `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:087-arch-diagram-docs"`；写入前的基线读数为 `flow_class: null` / `source: default` / `marker: null` / `exit 2`（`spec input not found`，属 owner 未就绪的降级形态，据实记录，不读作判定）。

- **A2（「以架构图为核心」的落地层级 = 结构基线的强制项，而不是新分类法）— 裁决：ratified（clarify 2026-11-06 复核后维持 adopted）**。用户原话「让 docs 文档整体结构改造成以架构图为核心」有两种读法：(i) 新建一族以图为中心的文档类型目录；(ii) 在既有六类正式目录的基线上，把「配套架构图」写成合规的必要条件。取 (ii)，理由三条：① **reuse-first**——(i) 会与既有 taxonomy 并列造出第二套文档分类，直接违反 one-source-of-truth（`create-docs` § Desired-State Baseline 自称覆盖 «all of its enumerations»；`one-source-of-truth.md` § Legitimate duplicates 只承认机械副本 / 守卫副本 / dated record 三类重复）；② 用户同一句里说的是「在原本 speckit.docs 命令的基础上」，落点是在既有机制上加义务，不是换掉机制；③ (i) 会让每一份既有文档都需要一次搬迁，把一次能力增强变成一次全量重构（宪法 IX）。**「以架构图为核心」的可验收含义**因此落在三处：读者先看到图（FR-005 的嵌入/链接义务）、每份正式文档必有图或具名豁免（FR-004 / FR-014）、图与文档失步必须被报出（FR-006）。**clarify 复核结论**：维持 (ii)；只剩一种反向读法未被排除——「只做图、不再写散文」——它与本规格 US4 / US5 与 FR-018 冲突，已被 § Out of Scope 显式排除。复核证据与逐条裁决见 `## Clarifications` Session 2026-11-06 第 2–3 行。

- **A3（架构图的定义 = 既有绘图能力的语义模型产物，不另立定义）— 裁决：adopted**。本规格反复使用「架构图」，但**不在本文件定义它**：一份图是否算架构图，判据归 `.specify/shared/definitions/flow-class-definitions.md` § 同构映射 的「结构 = 实体 / 关系 / 边界」一格所描述的实体—关系—边界语义，以及绘图能力 `references/semantic-model.md` 的 LDM 覆盖检查。本规格只在**义务层**说：文档描述的结构必须在图里有对应覆盖。这样「架构图」不新增第二个定义点，也避免本规格把某个引擎的图种名固化成框架语义。

- **A4（检查器形态留给 plan，但「确定性 + 只读 + 幂等」本阶段钉死）— 裁决：deferred → plan（判定面除外）**。检查器是新增脚本、扩展既有 `docs-utils.py` 的动作，还是复用既有验收脚本的一个动作，属实现口径，本阶段不预设。本阶段只钉住三条**可验收的判定面**：确定性（同输入两次同 verdict）、只读（无写点）、幂等（不改动空间时零写、同结论）。依据是先例——Feature 033 的 `docs-utils.py` 与 069a 的 `doc-consistency-check.py` 都采用「既有检查器加动作」而不是另起一套；但本阶段不据此替 plan 做选择。**约束（不是选择）**：无论形态如何，检查 MUST 由既有文档流程的验证步骤触达（FR-017），MUST NOT 新增 `/speckit.*` 命令。

- **A5（配套图的产物形态由被调用的绘图能力决定，本规格只钉「两面」）— 裁决：adopted**。用户说「源文件 + 渲染产物 + 嵌入/链接」（见本线补充解析）。这条恰好等于既有交付契约的 D2（源文件与渲染图一并保留）与 D1（自足 HTML 入口）。因此本规格只说「两面」——可再编辑的源、渲染产物——并按 FR-013 要求记录交付契约的验收结论；**具体扩展名、文件数量与放置目录由所选引擎层的交付契约决定**，本规格 MUST NOT 复述那张表（复述即第二 owner，且会随引擎层修订而漂移）。

- **A6（既有文档的存量处理 = 渐进收敛，不回溯强制）— 裁决：adopted**。框架自己这份仓库的 `docs/` 树里今天有多份无图文档（本阶段实测：`create-docs` / `improve-docs` / `docs.md` / `documentation-model.md` 对 "diagram" 全部零命中）。本特性不承担「把本仓所有文档一次性补齐图」的义务——那会让本线变成一个内容项目而非框架改动，且与 FR-021 的「不破坏内容」直接冲突。落地方式：基线与检查器对**新产生/新改进**的文档即时生效；对存量的处置沿用 reconcile 的残余报告与容忍带机制，由项目按自己的 target 声明决定节奏。

- **A7（与 069a 冻结基线的冲突面已知，处置留 plan）— 裁决：deferred → plan，并显式登记为需裁定的点**。本特性必然改动三处已被既有守卫钉住的源：`skills/external/create-docs/SKILL.md`（069a 的 W3 接线面，内容哈希在 `notes/pre-change-file-hashes.txt` 中）、`templates/commands/docs.md`（W1 接线面）、`docs/concepts/documentation-model.md`（003/037 的读者面）。`skills/external/improve-docs/SKILL.md` 虽在 069a 的 49 技能冻结清单内但不在其 W3 白名单，改动它需要在 `tests/contract/test_expression_compatibility.py` 的 `ALLOWED_POST_BASELINE_CHANGES` 登记理由与标记，与 071/072/081d/084/085 的先例同形。**clarify 阶段实测复核（2026-11-06）**：上句点名的守卫文件 `tests/contract/test_expression_compatibility.py` 在工作树中**存在且非空**（56282 bytes），`ALLOWED_POST_BASELINE_CHANGES` 在 `:445` 起逐条登记（reason + markers 二元组），最近的先例是 085 的 `templates/commands/goal.md` / `team.md` 两条；该断言成立，路径无需订正。**冲突面残留实测（供 plan 定 allowlist 条目形态）**：这四处一旦追加内容，仓内除该 allowlist 外还有四条既有守卫会同时被触发——`tests/contract/test_expression_gate_wiring.py`（A1：W1 的 `templates/commands/docs.md` 接线小节，本特性 MUST NOT 改动该小节）、`test_docs_command_template.py`（断言 `templates/commands/docs.md` 仍指向 `skills/external/improve-docs/SKILL.md`，本特性 MUST NOT 拆掉该指针）、`test_confirmation_gates_sweep.py:71`（`templates/commands/docs.md` 必须保留 `stop-and-confirm` 字面量）、`test_directory_governance.py:122`（`docs/concepts/documentation-model.md` 必须保留在目录治理的既有清单中）。这四条是**约束**而非裁定：plan 追加内容时必须逐条保持它们通过，不得改守卫来换取绿灯。**本阶段只登记冲突面与既有先例，不就地裁定**：是「按先例追加 allowlist 条目」还是「另立本特性自己的基线记录」，属 plan 阶段的承重决策。本阶段同时确认：这几处的改动**不涉及** 069a 的四字面量与被守卫的类别接线，`create-docs` / `docs.md` 的 W3/W1 接线小节 MUST 保持原样。

- **A8（命名：沿用既有术语，不新造）— 裁决：adopted**。本规格只用三个名称：**架构图（architecture diagram）**、**配套图义务**、**豁免记录**。其中「架构图」已是绘图能力的触发词之一（其 description 明列 "架构图" / "architecture diagram" / "系统架构图"），故按 Grounded Naming 的第一优先来源（既有约定）沿用，不另造同义词；「配套」「义务」「豁免」取中文常用义，不引入新概念。本规格 MUST NOT 为这三者登记第二个定义点；若 plan 认为需要一个 owner 章节，它必须落在既有 owner 内（`create-docs` § Desired-State Baseline），而非新建一份定义文档。

- **A9（文档类型 `Flow Type` 的处置）— 裁决：confirmed**。本线交付的是「把义务变成可判定事实」的机制与检查器，不是一份给人读的说明书；按 owner § 文档类型 的类约束，`execution` 线只允许写 `-`，写具体类型会触 `flow-type-mismatch`（退出码 1）。故写 `-`。

- **A10（本阶段无 clarification marker）— 裁决：confirmed（clarify 2026-11-06 复核后维持）**。所有开放点都能在目标仓库内裁决并留证，或已显式移交 plan（A4 检查器形态、A7 冲突处置）。**显式移交、并未伪装成已决的三条**：(1) A7 的冻结基线处置方式（两种读法间选择，plan 裁定）；(2) FR-014 的 `stale` 逐面判据（新检查器无既有 owner 可裁定，plan 在 RS-006 处冻结取值域）；(3) A4 的检查器实现形态。**clarify 阶段已裁定、原先未决的点**：A2 落地层级复核（维持）、义务的载体集合（A11）、`stale` 取并（FR-014 正文）。`## Related Feature` 已于本阶段绑定 Feature 087。

- **A11（配套图义务的载体集合 = 六类正式目录内文档 + `ARCHITECTURE.md`，其余保留根文件只承指针义务）— 裁决：adopted（clarify 2026-11-06）**。判据取自基线 owner 自身：`skills/external/create-docs/SKILL.md` § Desired-State Baseline 第 1 项把四个保留根文件各自的**固定语义**登记为「一屏摘要 / 贡献入口 / 时间线 / 根索引」；其中只有 `ARCHITECTURE.md` 的语义（concepts + decisions 的一页摘要）本身就是**结构**的载体，其余三个按语义不含可绘的结构。因此载体集合 = 六类正式目录内文档 + `ARCHITECTURE.md`；`README.md` / `CONTRIBUTING.md` / `CHANGELOG.md` 只承 FR-001 的指针义务。**不采纳的读法**：「全部正式文档一视同仁」会让每一个符合今日基线的项目在启用本特性当天就整体非合规，且把没有结构可绘的一屏索引判为缺图；「其余三个保留根文件走具名豁免」会把本可静态判定的边界变成逐项目申报的负担，违反宪法 IX。该裁决已同步落到 FR-003 与 § Edge Cases。

- **A12（`stale` 取两个条件的并集，逐面判据留 plan）— 裁决：adopted（clarify 2026-11-06）**。`stale` = 「图的两个面彼此不一致」或「图与文档就同一事实不一致」。取并的理由是 FR-014 正文与 US5 的独立测试都把两种情形并列为 stale，单取一方面会让另一半个案无判据。**移交项**：逐面判据（何谓「就同一事实不一致」、用哪些信号判定）由 plan 在 RS-006 的取值域 owner 处冻结；plan 若给不出可判据，MUST 把该面报为未覆盖并如实登记，MUST NOT 留一条无判据的 verdict（见 `## Clarifications` 第 4 行）。

## Out of Scope

- **不新建绘图引擎、不新建渲染器、不新建引擎选择表**（FR-011）。`draw-diagram` 的路由顺序与交付契约归它自己，本特性一行不改。
- **不新增 `/speckit.*` 命令**（FR-017）。义务挂在既有 `create-docs` / `improve-docs` 的既有步骤上，检查由既有流程的验证步骤触达。
- **不改变既有四个技能的职责划分**（FR-018），也不改变确认分级、只归档不删除、容忍带与反churn 规则（FR-019）。
- **不改动本仓 `docs/` 树的内容**——本线是框架改动（Two Hats），`docs/` 与 `.specify/` 只接受生成/镜像；把本仓文档逐份补图属内容工作，A6 已排除。
- **不覆盖表达类门禁集与流程类别机制**（077 / 069a 的领域）；本特性只消费它们，不修订。
- **不提供图形化编辑器或站点层改动**；`create-pages` 的发布面不在本特性范围内。

## Clarifications

### Session 2026-11-06

无人值守运行（无用户可回答问题）：按 `/speckit.clarify` 的自动裁决形态执行，每条裁定都以仓内可复核证据落定，证据不足裁决者显式标注为 plan/implement 移交，不伪装成已决。**未新增任何活跃的澄清标记**——`validate-requirements.py` 的 `marker-count` 检查在写回前后均为 `pass (0)`。

- Q: 本规格应绑定哪个既有 Feature，还是新建？ → A: 新建 Feature 087（`Draft`）。reuse-first 复核五候选（037 / 069 / 069a + 077 / 084 / 085）均不拥有「文档必须配套架构图」这一能力；最接近的 037 持有交付载体与结构能力但已关闭，且本仓实测 `create-docs` / `improve-docs` / `templates/commands/docs.md` / `docs/concepts/documentation-model.md` 对 "diagram" 零命中——绘图能力已存在而无任何写入流程消费它，属新义务而非既有义务加固。证据与逐候选裁决见 § Related Feature 的 reuse-first 表。

- Q: A2「以架构图为核心」应落成 (i) 新建一族以图为中心的文档类型目录，还是 (ii) 在既有六类正式目录的基线上把「配套架构图」立为合规必要条件？ → A: **维持 (ii)，ratify**。仓内四条证据支持：(a) `skills/external/create-docs/SKILL.md` § Desired-State Baseline 自称「single source of truth for the static documentation baseline and **all of its enumerations**」——另立一族目录即造出第二套并行 taxonomy，正是该句禁止的形态；(b) 宪法 XIV 与 `.specify/shared/guidelines/one-source-of-truth.md` § Legitimate duplicates 只承认机械副本 / 守卫副本 / dated record 三类重复，「第二套分类」不属任何一类；(c) 用户原话「在原本 speckit.docs 命令的基础上」指向加义务，不是换机制；(d) 宪法 IX 禁止 speculative infrastructure，而 (i) 会让每份既有文档都需搬迁。**反向读法不采纳但并不隐藏**：把 (i) 读成「与六类并列的第七类文档类型」，其可验收面（每份正式文档必有图或具名豁免、失步必被报出）与 (ii) 无差别；只有读成「只做图、不再写散文」，本规格的 US4 / US5 与 FR-018 才与之冲突。该反向读法被 § Out of Scope 的「不新建绘图引擎 / 不新增命令 / 不改变四技能职责划分」与 FR-018 显式排除，冲突面如实登记于此。

- Q: A2 若 (ii) 成立，「义务适用于哪些文档」是否已在仓内被判据钉死，还是要另行裁定？ → A: **本阶段裁定补全**：正式文档 = 落在六类正式目录（`concepts/` `tutorials/` `tasks/` `reference/` `decisions/` `contribute/`）内的文档，加上基线第 1 项已登记为 semantic carrier 的保留根文件（`ARCHITECTURE.md`，固定语义即 concepts + decisions 的一页摘要）；`README.md` / `CONTRIBUTING.md` / `CHANGELOG.md` 虽是合规正式文档，其固定语义是一屏摘要 / 贡献入口 / 时间线，**不带**配套图义务，改由 FR-001 的指针义务覆盖（指向图材料而非复制它）。逐项处置写入 § Assumptions A11，并同步修订 FR-003 与 § Edge Cases。

- Q: FR-014 的封闭 verdict 集合（satisfied / missing / stale / recorded exemption / not evaluated）中，`stale` 的判据是「源与渲染产物不一致」还是「图与文档不一致」，或被两者取并？ → A: **取并**：`stale` = 图的两个面彼此不一致，**或**图与文档就同一事实不一致。理由是 FR-014 的正文与 US5 的独立测试都把两种情形并列为「stale」，单取一方面会让另一半落进无判据的空隙。**可判定性移交**：本阶段只冻结「取并」，`stale` 的逐面判据（怎么算图与文档就同一事实不一致、用哪些信号）MUST 由 plan 在 RS-006 的取值域 owner 处冻结，原因是本阶段新增该检查器，其判据无既有 owner 可裁定；plan 若无法给出可判据，MUST 把 `stale` 降级并如实登记为该项未覆盖，而不是留一条不可判定的 verdict。

- Q: FR-014 / FR-015 的「确定性 + 幂等 + 只读」是否让发现失步必须依赖记录（记录被改即发现失效）？ → A: **不**。FR-015 明确「the check MUST be read-only. It MUST NOT be used to write」——记录只是一个输入，不是发现机制；发现必须由 `stale` 判据（上一行）重新从源、渲染产物与文档三者的实态推出。补充裁定：**检查本身不得向文档空间写入任何内容（含 LDM 摘要与交付契约验收摘要）**；FR-013 的记录随改变图的**产生方运行**落盘（写入流程的既有运行产物位与审计日志），不改图的检查运行只报告、不落记录。

- Q: 与 069a 冻结基线的冲突面（A7）本阶段是否裁定？ → A: **裁定为 plan-owned，本阶段不改判 A7**。本阶段只确认四件事：(a) 冲突面范围——`skills/external/create-docs/SKILL.md`（069a 的 W3 接线面，内容哈希在 `notes/pre-change-file-hashes.txt`）、`templates/commands/docs.md`（W1 接线面）、`docs/concepts/documentation-model.md`（003/037 读者面）、`skills/external/improve-docs/SKILL.md`（在 069a 的 49 技能冻结清单内但不在 W3 白名单，改动需在 `tests/contract/test_expression_compatibility.py` 的 `ALLOWED_POST_BASELINE_CHANGES` 登记理由与标记）；(b) **守卫文件实测**：`tests/contract/test_expression_compatibility.py` 在工作树中存在且非空（56282 bytes），A7 正文的路径断言成立，plan 以其实际内容为准解析条目形态；(c) **四条既有守卫的残留约束**——`test_expression_gate_wiring.py`（A1 的 W1 接线小节保持原样）、`test_docs_command_template.py`（`templates/commands/docs.md` 仍须指向 `improve-docs`）、`test_confirmation_gates_sweep.py:71`（`stop-and-confirm` 字面量保留）、`test_directory_governance.py:122`（`documentation-model.md` 留在目录治理清单内）——plan 追加内容时必须逐条保持通过，MUST NOT 改守卫换绿灯；(d) 处置方式（追加 allowlist 条目 vs 另立本特性的基线记录）是在两种读法间选择，属裁定，归 plan，本阶段 MUST NOT 就地修平。**纠正留痕**：本行初稿曾据一次只列出部分目录项的目录读取误判该守卫文件「不存在」，随即以 `ls -la` 与 `grep -rl` 复核推翻，该误判是纠正而非裁定，已就地修正并在 A7 正文留下实测行。

- Q: 本阶段写回后，`checklists/requirements.md` 的派生计数是否需要刷新？ → A: **不需要刷新条目数，但需要新增一条过门记录**。本阶段对 FR/SC **零增删**：所有新裁定落在既有 FR-003 / FR-013 / FR-014 / FR-015 / FR-016 的语义收紧上（追加约束子句、不改编号、不改 `Path` 标记），故 23 FR / 10 SC 的派生计数不变。`validate-requirements.py` 的文件行数与 shared-string 数每次写回都会变，二者不是派生计数，不落登记面。手工统计（本阶段实测）与检查器读数一致：23 条 FR 定义行 + 10 条 SC 定义行 = 33 行，与检查器 `33 definition rows` 相符。

- Q: 本次写回中发现的 `checklists/requirements.md` 残留漂移（形如「definitions stay 23 FR / 10 SC」的派生计数副本，与宪法 XIV / OST「on finding a stale count, remove the copy; do not correct the number」相违）如何处理？ → A: **本阶段不改它，登记为未决项**。`checklists/requirements.md` 的 owner 是 `/speckit.checklist`，它在当前阶段的产品里不是本阶段的写属；本阶段直接改写会越过 owner 且留下第二处措辞。该漂移的处置归 requirements 阶段收尾或 plan 的 `## Clarifications` 追加轮，本行只作可见登记。
