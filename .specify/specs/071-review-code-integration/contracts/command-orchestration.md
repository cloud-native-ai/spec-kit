# Contracts: Command Orchestration — the two segments (C-1…C-16)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the composition shape of `/speckit.review` — segment order, delegation duty, failure propagation, applicability triage, output placement, and the process report's code section. Literal values pinned by the requirements are referenced as `[[STR-NNN]]`; the two severity vocabularies are owned by their skills and are cited here, never redefined.
**Pinned by**: `tests/contract/test_review_code_composition.py`
**Measures**: SC-001, SC-005

**C-1**: `/speckit.review` runs exactly two segments in a fixed order — the process segment (delegated to `review-sdd-process`) first, the code segment (delegated to `code-review`) second. There is no parallel mode, no single merged report, and no parameter that selects one segment over the other. The fixed order is a property of the command template, not of the skills, so neither skill may reverse or skip the other (FR-001).

**C-2**: The two segments' conclusions MUST NOT be merged into a single severity system, a single score, a mapping matrix, or a conversion table. A reviewer who has to compare a process `P1` with a code `important` reads them as two values in two vocabularies, and no artifact of this feature stores a combined value (FR-001, FR-007).

**C-3**: The process segment runs on every invocation. It MUST NOT be exempted by the feature's execution/expression class, by `$ARGUMENTS`, by an absent code delta, or by any earlier segment's outcome. This mirrors the 100%-call-rate property the flow-classification ledger already records for the `review` face (FR-002).

**C-4**: Each segment MUST be delegated to its existing skill by named runtime path, and the command template MUST NOT inline either skill's methodology. Concretely: no process-review dimension list, no code-review `P0`–`P6` dimension list, no severity definitions, and no receipt field list appear in `templates/commands/review.md`; the template orchestrates and points (FR-002).

**C-5**: A process-segment abort or error MUST NOT suppress the code segment — the two judgment objects are independent and the code segment's preconditions do not include the process segment's success. In that state the process segment MUST be recorded as [[STR-002]] with its reason, both segment conclusions are presented independently, and the command MUST NOT present the run as a completed review (FR-002).

**C-6**: Before the code segment starts, the command MUST resolve and record the code segment's applicability to exactly one of three values: `run` (this feature has a committed code delta), [[STR-001]] with a recorded basis, or [[STR-002]] with a recorded reason. Any fourth state — an unspecified value, an empty value, or a silently skipped segment — is a violation of this clause (FR-003, SC-005).

**C-7**: [[STR-001]] requires a basis that names one of two facts: the feature produces no code deliverable, or the feature has no committed code delta. The bare literal without a basis does not satisfy this clause (FR-003).

**C-8**: The code segment's object is this feature slice's committed code delta. Uncommitted working-tree changes MUST NOT be counted into the default review object; when they exist, the record discloses the unreviewed scope and MUST NOT issue any conclusion over it (FR-004, FR-005).

**C-9**: `review.md` MUST carry a code-segment subsection whose content is limited to: the base and head commit identifiers with the base source, the renderer mode, the coverage receipt counts (changed / judged / skipped / gap), the segment verdict, the gate verdict, the [[STR-001]] or [[STR-002]] reason when one applies, the path to [[STR-004]], and this run's archive path. A reader who opens only `review.md` can therefore state both segments' outcomes (FR-011, SC-001).

**C-10**: That subsection MUST NOT copy the code segment's opinion bodies and MUST NOT re-list its per-item counts. Duplicating the opinions would give the code findings a second, silently stale home (FR-011).

**C-11**: The process report stays at `<spec>/review.md` with the structure owned by `templates/review-template.md`; the code segment record is a separate file [[STR-004]] in the same directory. Neither file overwrites the other, and the two MUST NOT share one severity summary table (FR-010).

**C-12**: When a run finds an existing [[STR-004]], it MUST first archive that file inside the same directory as `code-review-<run timestamp>.md` and then write the new [[STR-004]]. `review.md` records the path written this run and, when present, this run's archive path. After the rotation [[STR-004]] denotes the latest run and every earlier run survives as its own archive file (FR-010).

**C-13**: [[STR-004]] MUST NOT enter any downstream available-documents list and MUST NOT be read as plan or tasks input. It MUST be referenced from the bound feature's review-record row so a reader arriving from the feature side can reach it (FR-012).

**C-14**: The closing summary and the feature detail MUST both present the two segment conclusions — the process segment's counts by severity and the code segment's verdict with its receipt counts — so the code-segment outcome is knowable without opening a second file (FR-019, SC-001).

**C-15**: A code-segment finding keeps its existing locating form (severity plus file and optional line) and MUST NOT be coined as a `REC-…` identifier. Only framework-targeted recommendations use that family and carry its same-commit registration duty (FR-020).

**C-16**: The command's non-segment surfaces are unchanged by this feature: the frontmatter `scripts:` prerequisite block stays as published, the `## Wrap-up` compiled face keeps its existing steps, and `## Handoffs` keeps the recommendation-registration obligation in its current form (FR-016, FR-020).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-1 | FR-001 | — | command template |
| C-2 | FR-001, FR-007 | — | command template |
| C-3 | FR-002 | — | command template |
| C-4 | FR-002 | — | command template |
| C-5 | FR-002 | — | command template |
| C-6 | FR-003 | SC-005 | command template + report |
| C-7 | FR-003 | — | command template |
| C-8 | FR-004, FR-005 | — | command template + record |
| C-9 | FR-011 | SC-001 | report template |
| C-10 | FR-011 | — | report template |
| C-11 | FR-010 | — | command template + record |
| C-12 | FR-010 | — | script + report template |
| C-13 | FR-012 | — | command template + feature detail |
| C-14 | FR-019 | SC-001 | command template + feature detail |
| C-15 | FR-020 | — | command template |
| C-16 | FR-016, FR-020 | — | command template |
