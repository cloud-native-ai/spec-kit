# Requirements Specification: 架构图为核心的文档空间（Architecture-Diagram-Centric Documentation Space）

**Requirement Branch**: `087-arch-diagram-docs`
**Created**: 2026-11-06
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "以087-* 为前缀开发一个需求,在原本speckit.docs命令的基础上,让docs文档整体结构改造成以架构图为核心, 重复发挥 spec-kit/skills/external/draw-diagram 技能的能力,在生成文档的时候都需要进行架构图的配套."

> **本行的由来（自用声明）**：本规格由本线作者按 `.specify/shared/definitions/flow-class-definitions.md` § 判据自行判定，判据与理由见 § Assumptions A1。`Flow Type` 写 `-`（`execution` 线只允许 `-`）。本阶段读到的类别记录见 A1 末尾的复读行。

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

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
- **A diagram whose engine layer cannot render in this environment.** The drawing capability already refuses to silently degrade; the documentation flows must not convert that refusal into "document done, diagram skipped".
- **A document that embeds a diagram belonging to a different document.** One picture cited by several documents is legitimate; the obligation is that each formal document has an accompanying diagram, which such a citation may satisfy — but then that shared diagram needs an identifiable home, and updating it must not fork into per-document copies.
- **A rendered image edited or deleted while the source survives** (or the reverse). Source and rendered artifact are two faces of one deliverable; losing either leaves the document unverifiable.
- **A space that already contains hand-made diagrams** produced before this feature. Convergence must not silently replace an author's diagram with a re-routed one; the existing never-clobber and target-declaration rules govern.
- **A diagram that passes structure checks while being factually wrong** — the diagram renders, the link resolves, and the picture contradicts the prose. Structure passing is a necessary condition and never sufficient; the reader-facing judgement belongs to review.
- **A document produced by a project that has not refreshed its `.specify/` runtime.** The obligation must degrade visibly (existing wiring rules) rather than pretend the diagram exists.
- **Two documents authored concurrently that both want the same diagram.** The existing "add a writing agent's isolation and integration" discipline governs; this feature must not create a shared mutable diagram store.

## Requirements *(mandatory)*

### Functional Requirements

**A. The diagram-centric structure baseline**

- **FR-001**: The documentation space's desired-state baseline MUST be amended so that an accompanying architecture diagram is part of a compliant formal document. The amendment MUST land in the baseline's owning location — `skills/external/create-docs/SKILL.md` § Desired-State Baseline — and every other surface MUST cite it by path plus section anchor rather than restate its contents. The user-facing explanation in `docs/concepts/documentation-model.md` MUST be brought into agreement with the owner in the same change and MUST remain a reader-facing explanation, not a second rulebook.
- **FR-002**: The diagram obligation MUST apply **within** the existing formal document taxonomy. This feature MUST NOT introduce a new top-level document-type directory for diagrams, and MUST NOT change the fixed semantics or the registered location of any reserved root filename.
- **FR-003**: The obligation MUST apply to formal documents (the typed `docs/` directories and any diagram-bearing root entry) and MUST NOT be applied to the temporary `notes/` zone, whose lifecycle rules are already owned elsewhere and whose documents carry no stability guarantee.
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
- **FR-013**: A run that produces a diagram MUST record its traceability: the selected engine layer and the reason for that selection, the semantic-model summary of what the diagram covers, and the delivery-contract acceptance outcome. A produced diagram without that record MUST be treated as an unaccepted diagram.

**D. The decidable check**

- **FR-014**: The framework MUST provide a **deterministic, re-runnable check** that judges, per document, whether the diagram obligation is satisfied. It MUST report each affected document by path with a named reason, MUST distinguish "satisfied", "missing", "stale" (source and rendered artifact disagree with the document, or one face is absent), and "recorded exemption", and MUST report an un-evaluable document as not evaluated rather than as satisfied.
- **FR-015**: The check MUST be idempotent over an unchanged space: two consecutive runs MUST produce the same verdict, and the check MUST be read-only. It MUST NOT be used to write or to converge; convergence remains the documentation flows' job.
- **FR-016**: The check's finding vocabulary MUST be a closed, named set, and every finding MUST name the document path it concerns. A space with no affected documents MUST report zero findings as an explicit clean verdict; a check that cannot run MUST NOT be reportable as clean.
- **FR-017**: The check MUST be reachable from the existing documentation flows' verification steps rather than requiring a new user-facing command. This feature MUST NOT add a new `/speckit.*` command.

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

- **A2（「以架构图为核心」的落地层级 = 结构基线的强制项，而不是新分类法）— 裁决：adopted**。用户原话「让 docs 文档整体结构改造成以架构图为核心」有两种读法：(i) 新建一族以图为中心的文档类型目录；(ii) 在既有六类正式目录的基线上，把「配套架构图」写成合规的必要条件。取 (ii)，理由三条：① **reuse-first**（宪法 VII）——(i) 会与既有 taxonomy 并列造出第二套文档分类，直接违反 one-source-of-truth；② 用户同一句里说的是「在原本 speckit.docs 命令的基础上」，落点是在既有机制上加义务，不是换掉机制；③ (i) 会让每一份既有文档都需要一次搬迁，把一次能力增强变成一次全量重构。**「以架构图为核心」的可验收含义**因此落在三处：读者先看到图（FR-005 的嵌入/链接义务）、每份正式文档必有图或具名豁免（FR-004 / FR-014）、图与文档失步必须被报出（FR-006）。这条是**裁定**而非纠正，故明确留痕：若 clarify 认为用户要的是 (i)，本规格的 § Requirements A 与 SC-003 需整体重写。

- **A3（架构图的定义 = 既有绘图能力的语义模型产物，不另立定义）— 裁决：adopted**。本规格反复使用「架构图」，但**不在本文件定义它**：一份图是否算架构图，判据归 `.specify/shared/definitions/flow-class-definitions.md` § 同构映射 的「结构 = 实体 / 关系 / 边界」一格所描述的实体—关系—边界语义，以及绘图能力 `references/semantic-model.md` 的 LDM 覆盖检查。本规格只在**义务层**说：文档描述的结构必须在图里有对应覆盖。这样「架构图」不新增第二个定义点，也避免本规格把某个引擎的图种名固化成框架语义。

- **A4（检查器形态留给 plan，但「确定性 + 只读 + 幂等」本阶段钉死）— 裁决：deferred → plan（判定面除外）**。检查器是新增脚本、扩展既有 `docs-utils.py` 的动作，还是复用既有验收脚本的一个动作，属实现口径，本阶段不预设。本阶段只钉住三条**可验收的判定面**：确定性（同输入两次同 verdict）、只读（无写点）、幂等（不改动空间时零写、同结论）。依据是先例——Feature 033 的 `docs-utils.py` 与 069a 的 `doc-consistency-check.py` 都采用「既有检查器加动作」而不是另起一套；但本阶段不据此替 plan 做选择。**约束（不是选择）**：无论形态如何，检查 MUST 由既有文档流程的验证步骤触达（FR-017），MUST NOT 新增 `/speckit.*` 命令。

- **A5（配套图的产物形态由被调用的绘图能力决定，本规格只钉「两面」）— 裁决：adopted**。用户说「源文件 + 渲染产物 + 嵌入/链接」（见本线补充解析）。这条恰好等于既有交付契约的 D2（源文件与渲染图一并保留）与 D1（自足 HTML 入口）。因此本规格只说「两面」——可再编辑的源、渲染产物——并按 FR-013 要求记录交付契约的验收结论；**具体扩展名、文件数量与放置目录由所选引擎层的交付契约决定**，本规格 MUST NOT 复述那张表（复述即第二 owner，且会随引擎层修订而漂移）。

- **A6（既有文档的存量处理 = 渐进收敛，不回溯强制）— 裁决：adopted**。框架自己这份仓库的 `docs/` 树里今天有多份无图文档（本阶段实测：`create-docs` / `improve-docs` / `docs.md` / `documentation-model.md` 对 "diagram" 全部零命中）。本特性不承担「把本仓所有文档一次性补齐图」的义务——那会让本线变成一个内容项目而非框架改动，且与 FR-021 的「不破坏内容」直接冲突。落地方式：基线与检查器对**新产生/新改进**的文档即时生效；对存量的处置沿用 reconcile 的残余报告与容忍带机制，由项目按自己的 target 声明决定节奏。

- **A7（与 069a 冻结基线的冲突面已知，处置留 plan）— 裁决：deferred → plan，并显式登记为需裁定的点**。本特性必然改动三处已被既有守卫钉住的源：`skills/external/create-docs/SKILL.md`（069a 的 W3 接线面，内容哈希在 `notes/pre-change-file-hashes.txt` 中）、`templates/commands/docs.md`（W1 接线面）、`docs/concepts/documentation-model.md`（003/037 的读者面）。`skills/external/improve-docs/SKILL.md` 虽在 069a 的 49 技能冻结清单内但不在其 W3 白名单，改动它需要在 `tests/contract/test_expression_compatibility.py` 的 `ALLOWED_POST_BASELINE_CHANGES` 登记理由与标记，与 071/072/081d/084/085 的先例同形。**本阶段只登记冲突面与既有先例，不就地裁定**：是「按先例追加 allowlist 条目」还是「另立本特性自己的基线记录」，属 plan 阶段的承重决策。本阶段同时确认：这几处的改动**不涉及** 069a 的四字面量与被守卫的类别接线，`create-docs` / `docs.md` 的 W3/W1 接线小节 MUST 保持原样。

- **A8（命名：沿用既有术语，不新造）— 裁决：adopted**。本规格只用三个名称：**架构图（architecture diagram）**、**配套图义务**、**豁免记录**。其中「架构图」已是绘图能力的触发词之一（其 description 明列 "架构图" / "architecture diagram" / "系统架构图"），故按 Grounded Naming 的第一优先来源（既有约定）沿用，不另造同义词；「配套」「义务」「豁免」取中文常用义，不引入新概念。本规格 MUST NOT 为这三者登记第二个定义点；若 plan 认为需要一个 owner 章节，它必须落在既有 owner 内（`create-docs` § Desired-State Baseline），而非新建一份定义文档。

- **A9（文档类型 `Flow Type` 的处置）— 裁决：confirmed**。本线交付的是「把义务变成可判定事实」的机制与检查器，不是一份给人读的说明书；按 owner § 文档类型 的类约束，`execution` 线只允许写 `-`，写具体类型会触 `flow-type-mismatch`（退出码 1）。故写 `-`。

- **A10（本阶段无 clarification marker）— 裁决：confirmed**。所有开放点都能在目标仓库内裁决并留证，或已显式移交 plan（A4 形态、A7 冲突处置）。**显式移交、并未伪装成已决的两条**：A2（若 clarify 判定用户要的是「新建文档类型目录」而非「基线上加义务」，本规格需重写）与 A7（冻结基线的处置方式）。`## Related Feature` 按技能 § 5.3 保持 `Need clarification`，绑定动作归 `/speckit.clarify`。

## Out of Scope

- **不新建绘图引擎、不新建渲染器、不新建引擎选择表**（FR-011）。`draw-diagram` 的路由顺序与交付契约归它自己，本特性一行不改。
- **不新增 `/speckit.*` 命令**（FR-017）。义务挂在既有 `create-docs` / `improve-docs` 的既有步骤上，检查由既有流程的验证步骤触达。
- **不改变既有四个技能的职责划分**（FR-018），也不改变确认分级、只归档不删除、容忍带与反churn 规则（FR-019）。
- **不改动本仓 `docs/` 树的内容**——本线是框架改动（Two Hats），`docs/` 与 `.specify/` 只接受生成/镜像；把本仓文档逐份补图属内容工作，A6 已排除。
- **不覆盖表达类门禁集与流程类别机制**（077 / 069a 的领域）；本特性只消费它们，不修订。
- **不提供图形化编辑器或站点层改动**；`create-pages` 的发布面不在本特性范围内。

## Clarifications

<!-- 本节由 /speckit.clarify 填充；A2 与 A7 是已显式移交的两条候选裁定。 -->
