# Contracts: Evidence Binding & Baseline Consumption（F6/F7）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md`
**Convention**: canonical clause form (`**C-N**` md-bold-closed) per `shared/definitions/contract-clause-definitions.md` § 3. Each clause's citation group is the trailing `(FR-…, SC-…)` at the end of its block (§ 4 rule 2). Shared strings cited as [[STR-NNN]] per the requirements' table.

> Owner anchors (current code, verified 2026-10-19): `templates/verification-log-template.md` is a flat key-value log whose sections are `# -- Baseline --`, `# -- /speckit.implement results --`, `# -- Success Criteria evaluation --`, `# -- Deferred tasks --`, `# -- Free-form notes --` — no per-sample evidence slot exists. `shared/definitions/probe-definitions.md` registers command gates as `| <gate_id> | command-gate | <unit> | <lifecycle_point> |` rows (sibling precedent: `gate-implement-checklist-waiver`) with `h-gate-evidence` HandlerBinding rows at `@point:confirm-gate`.

## Claim-to-evidence binding（F6）

**C-26**: 逐样本证据段 `templates/verification-log-template.md` MUST gain a structured evidence-record section between `# -- /speckit.implement results --` and `# -- Success Criteria evaluation --`: one record per evaluation sample carrying `sample_id`, `evidence_path` (repo-relative archived artifact), `evidence_sha256`, `verdict`. The template MUST declare the deterministic hash algorithm — SHA-256 over the archived file's bytes (plan-level decision; requirements deliberately left the algorithm to plan) — and the rule that a `pass` verdict requires a complete evidence row. The template keeps its existing section set and key-value conventions; the new section is additive (FR-019, SC-010)。

**C-27**: gate 注册与消费点 `shared/definitions/probe-definitions.md` MUST register `gate-implement-evidence-binding` ([[STR-001]]) beside the existing command-gate rows: class `command-gate`, unit `/speckit.implement`, with its `h-gate-evidence` HandlerBinding row at `@point:confirm-gate` (same shape as `gate-implement-checklist-waiver`). `skills/internal/implement-feature/SKILL.md` MUST reference the gate at the verification-log step (Step 9), where `verification.md` is populated — the skill has no per-feature `GATE-8` numbering (gate ids are tasks.md-local constructs), so the skill-side anchor is the step that owns the evidence the gate checks. The gate MUST reuse the existing gate-probe mechanism (firing evidence recorded via the feedback engine with `--lifecycle-point`); MUST NOT add a subsystem (FR-020, SC-010)。

**C-28**: 判红语义 the gate's check: for every sample recorded `pass`, the archived artifact at `evidence_path` MUST exist, MUST be non-empty, and its computed SHA-256 MUST equal `evidence_sha256`; missing, empty, or mismatching each ⇒ the gate verdict is red, naming the sample id and the failure reason — the failure MUST NOT be downgraded to "self-disclosed and continue". A sample whose verdict is not `pass` (`fail`/`deferred`/`partial`/`unknown`) carries no binding duty. A `pass` without a complete evidence row is `unverified` and MUST NOT be cited as passing evidence anywhere downstream (FR-020, FR-021, SC-010)。

## Frozen-baseline consumption（F7）

**C-29**: implement 预检与差异归因 `skills/internal/implement-feature/SKILL.md` MUST gain a pre-flight step before Step 1: re-capture every frozen baseline of the feature — the set derived from the spec directory by glob (`<spec-dir>/baseline-*`, `<spec-dir>/notes/baseline-*`) plus the coverage baseline file ([[STR-002]]; the set is directory-derived, never a hand-written count, per FR-030; the globs cover both the root-level captures the skill's own Test-runs bullet writes and the `notes/` captures prior features used). Where a re-capture differs from the frozen value, the new value MUST be written into the row that cites it, and every difference MUST be classified — BEFORE any drift verdict is issued — as `upstream repair` / `inherited` / `attributable to this feature` / `undecidable` using `git log` provenance. `undecidable` MUST be explicitly reported; guessing between the three attributed classes MUST NOT happen. A missing baseline file is handled as a first capture with provenance recorded, never as zero drift (FR-022, FR-030, SC-011)。

**C-30**: 命令面同职责 `templates/commands/implement.md` MUST state the same pre-flight duty in the command face (its Skill Delegation inputs, before "follow its steps 1–9"), so the obligation reaches a reader of the command alone and does not live only inside the skill (FR-023, SC-011)。

## Traceability

| Clause | Finding | FR | SC | Primary artifact |
|--------|---------|----|----|------------------|
| C-26 | F6 | FR-019 | SC-010 | templates/verification-log-template.md |
| C-27 | F6 | FR-020 | SC-010 | shared/definitions/probe-definitions.md + skills/internal/implement-feature/SKILL.md |
| C-28 | F6 | FR-020/FR-021 | SC-010 | gate check semantics |
| C-29 | F7 | FR-022/FR-030 | SC-011 | skills/internal/implement-feature/SKILL.md |
| C-30 | F7 | FR-023 | SC-011 | templates/commands/implement.md |
