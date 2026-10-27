# Contracts: Command Orchestration — the two segments (C-1…C-16)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the composition shape of `/speckit.review` — segment order, delegation duty, failure propagation, applicability triage, output placement, and the process report's code section. Literal values pinned by the requirements are referenced as `[[STR-NNN]]`; the two severity vocabularies are owned by their skills and are cited here, never redefined.
**Pinned by**: `tests/contract/test_review_code_composition.py`
**Measures**: SC-001, SC-005

**C-1**: `/speckit.review` runs exactly two segments in a fixed order — the process segment (delegated to `review-sdd-process`) first, the code segment (delegated to `code-review`) second. There is no parallel mode, no single merged report, and no parameter that selects one segment over the other. The fixed order is a property of the command template, not of the skills, so neither skill may reverse or skip the other (FR-001).

**C-2**: The two segments' conclusions MUST NOT be merged into a single severity system, a single score, a mapping matrix, or a conversion table. A reviewer who has to compare a process `P1` with a code `important` reads them as two values in two vocabularies, and no artifact of this feature stores a combined value (FR-001, FR-007).

**C-3**: The process segment runs on every invocation. It MUST NOT be exempted by the feature's execution/expression class, by `$ARGUMENTS`, by an absent code delta, or by any earlier segment's outcome. This mirrors the 100%-call-rate property the flow-classification ledger already records for the `review` face (FR-002).

**C-4**: Each segment MUST be delegated to its existing skill by named runtime path, and the command template MUST NOT inline either skill's methodology. Concretely: no process-review dimension list, no code-review `P0`–`P6` dimension list, no severity definitions, and no receipt field list appear in `templates/commands/review.md`; the template orchestrates and points (FR-002).

**C-5**: A process-segment abort or error MUST NOT suppress the code segment — the two judgment objects are independent and the code segment's preconditions do not include the process segment's success. In that state the process segment MUST be recorded as [[STR-002]] with its reason, both segment conclusions are presented independently, and the command MUST NOT present the run as a completed review. If the abort happened before `review.md` was written, the command itself MUST author a minimal process report from `templates/review-template.md` carrying only the code-segment subsection and the abort reason, so the verifiable carrier stays the single `review.md` and its author is the command rather than the process skill (FR-002).

**C-6**: Before the code segment starts, the command MUST resolve and record the code segment's applicability to exactly one of three values: [[STR-005]] (this feature has a committed code delta containing at least one code path), [[STR-001]] with a recorded basis, or [[STR-002]] with a recorded reason. Any fourth state — an unspecified value, an empty value, or a silently skipped segment — is a violation of this clause (FR-003, SC-005).

**C-7**: [[STR-001]] requires a basis that names one of two facts: the feature produces no code deliverable, or the feature has no committed code delta. The bare literal without a basis does not satisfy this clause. What counts as a code path is decided by a named owner and not by this clause: the `code-review` skill's deterministic script (`skills/internal/code-review/scripts/git-delta-review.sh`) holds one closed default code-path set and accepts an explicit override (`--code-paths`); the command and this contract cite that owner's verdict and MUST NOT carry a second path list, because two lists drift and a drift changes the triage value for one repository state. An empty changed set (base and head at the same commit, zero changed files) MUST be triaged to [[STR-001]] with the basis "no committed code delta" **before** the coverage receipt runs — it MUST NOT reach the receipt and be reported as a clean review of nothing (FR-003).

**C-8**: The code segment's object is this feature slice's committed code delta. Uncommitted working-tree changes MUST NOT be counted into the default review object; when they exist, the record discloses the unreviewed scope and MUST NOT issue any conclusion over it (FR-004, FR-005).

**C-9**: `review.md` MUST carry a code-segment subsection whose content is limited to: the base and head commit identifiers with the base source, the renderer mode, the coverage receipt counts (changed / judged / skipped / gap) **copied from the receipt block**, the segment verdict, the gate verdict, the [[STR-001]] or [[STR-002]] reason when one applies, the uncommitted-scope disclosure when the working tree is dirty, the path to [[STR-004]], and this run's archive path ([[STR-009]] on a first run, the actual archive path afterwards). The block is the only source of the four counts: the subsection MUST NOT recompute, re-aggregate, or derive them from the record's prose, and the same four numbers copied into the feature detail entry are copied from the same block (C-74 of `coverage-receipt.md`). A reader who opens only `review.md` can therefore state both segments' outcomes (FR-005, FR-011, SC-001).

**C-10**: That subsection MUST NOT copy the code segment's opinion bodies and MUST NOT re-list its per-item counts. Duplicating the opinions would give the code findings a second, silently stale home (FR-011).

**C-11**: The process report stays at `<spec>/review.md` with the structure owned by `templates/review-template.md`; the code segment record is a separate file [[STR-004]] in the same directory. Neither file overwrites the other, and the two MUST NOT share one severity summary table. Record existence follows the triage value: only [[STR-005]] writes [[STR-004]]; [[STR-001]] and [[STR-002]] write no record file — not even an empty one — and their conclusion and reason live in the report's code subsection (FR-010).

**C-12**: When a run finds an existing [[STR-004]], it MUST first archive that file inside the same directory as `code-review-<run timestamp>.md` and then write the new [[STR-004]]. The run timestamp is `YYYYMMDDTHHMMSSZ` (UTC, second resolution). Two runs inside one second MUST NOT overwrite an existing archive: the later run either waits for the next second before writing or exits `2` with the reason. `review.md` records the path written this run and this run's archive path — [[STR-009]] on a first run, the archive's actual path afterwards. After the rotation [[STR-004]] denotes the latest run and every earlier run survives as its own archive file (FR-010).

**C-13**: [[STR-004]] MUST NOT enter any downstream available-documents list and MUST NOT be read as plan or tasks input. It MUST be referenced from the bound feature detail's existing `## Latest Review` entry — the review-record line inside that entry — so a reader arriving from the feature side can reach it. That existing entry is the carrier: no new structured field and no second count copy are added to the feature detail, whose counts are copied per C-9 (FR-012).

**C-14**: The two segment conclusions MUST appear on both verifiable carriers — the process report's code subsection (C-9) and the feature detail's `## Latest Review` review-record entry (C-13) — so the code-segment outcome is knowable from the report alone. The closing summary (console and handoff output) MAY restate both; it is a presentation, not an artifact: this feature assigns it no independent content obligation and treats no third carrier as verifiable, and where it disagrees with the two carriers the carriers govern (FR-019, SC-001).

**C-15**: A code-segment finding keeps its existing locating form (severity plus file and optional line) and MUST NOT be coined as a `REC-…` identifier. Only framework-targeted recommendations use that family and carry its same-commit registration duty (FR-020).

**C-16**: The command's non-segment surfaces are unchanged by this feature: the frontmatter `scripts:` prerequisite block stays as published, the `## Wrap-up` compiled face keeps its existing steps, and `## Handoffs` keeps the recommendation-registration obligation in its current form (FR-016, FR-020).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-1 | FR-001 | — | command template |
| C-2 | FR-001, FR-007 | — | command template |
| C-3 | FR-002 | — | command template |
| C-4 | FR-002 | — | command template |
| C-5 | FR-002 | — | command template + report template |
| C-6 | FR-003 | SC-005 | command template + report |
| C-7 | FR-003 | SC-005 | command template + skill script |
| C-8 | FR-004, FR-005 | — | command template + record |
| C-9 | FR-005, FR-011 | SC-001 | report template |
| C-10 | FR-011 | — | report template |
| C-11 | FR-010 | — | command template + record |
| C-12 | FR-010 | — | script + report template |
| C-13 | FR-012 | — | command template + feature detail |
| C-14 | FR-019 | SC-001 | report template + feature detail |
| C-15 | FR-020 | — | command template |
| C-16 | FR-016, FR-020 | — | command template |

## Amendment log — remediation round 1 (2026-10-27)

Trigger: `test-evidence/analyze-report.md` (`GATE: CRITICAL=0 HIGH=6`) and the worklist in `notes/remediation-round-1.md`. No clause id was renumbered and no obligation was dropped; every row below is a wording amendment to an existing clause, made because the requirement it cites was adjudicated further in `requirements.md`.

| Clause | Change | Why (finding) |
|--------|--------|---------------|
| C-5 | the abort case names its author: the command writes a minimal process report when `review.md` does not exist yet | A-07 |
| C-6 | the bare `run` literal becomes `[[STR-005]]`; the value is defined by "at least one code path in the committed delta" | A-09 |
| C-7 | code-path predicate delegated to the skill script (closed default set + `--code-paths`); empty delta triaged before the receipt runs | A-02, A-11 |
| C-9 | the uncommitted-scope disclosure joins the closed list; the counts are copied from the receipt block, never recomputed | A-04, A-29, A-33 |
| C-11 | record existence follows the triage value: only [[STR-005]] writes a record | A-08 |
| C-12 | archive timestamp fixed to `YYYYMMDDTHHMMSSZ`, same-second disposition added, first-run value [[STR-009]] | A-22 |
| C-13 | the carrier is the existing `## Latest Review` entry, with no new structured field | A-21 |
| C-14 | two verifiable carriers; the closing summary is demoted to presentation | A-01, A-29 |
