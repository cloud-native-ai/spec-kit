# Contracts: Coverage receipt and segment verdict (C-31…C-44, plus the appended C-74)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the receipt's carrier, its closed field set, its exit-code semantics, the gap-versus-skip distinction, and the mechanical derivation of the segment verdict. The record header that hosts the receipt is owned by `code-review-skill.md` C-21; the process report that mirrors the counts is owned by `command-orchestration.md` C-9.
**Pinned by**: `tests/contract/test_coverage_receipt.py`
**Measures**: SC-002, SC-003

**C-31**: The receipt is one delimited, machine-readable block inside [[STR-004]], opened by the literal line `<!-- coverage-receipt:begin -->` and closed by `<!-- coverage-receipt:end -->`. It MUST NOT be written to a second artifact file, and it MUST NOT be split across files (FR-014).

**C-32**: The block's name set is closed. It carries exactly: `receipt_version`, `base`, `head`, `base_source`, `renderer`, `changed_files`, `judged_files`, `skipped_files`, `gap_files`, `lines_added`, `lines_deleted`, plus one `file.<NN>.path` and one `file.<NN>.verdict` per changed file, and a `file.<NN>.reason` only where the verdict is `skipped`. Each line is one `name=value` pair; a name outside this set is a violation (FR-014).

**C-33**: The receipt's per-file entry set MUST equal the delta's changed-file set. Entries are emitted in sorted path order with zero-padded ordinals, so two runs over the same repository state produce a byte-identical block (FR-014, SC-002).

**C-34**: The receipt command exits `0` when the two sets are equal and every changed file carries a verdict — a reasoned skip from the closed reason set included — and exits `1` when any changed file has no entry, the two sets differ in either direction, or a skip carries a reason outside that closed set (C-36). Exit `1` therefore means one thing only: a coverage gap. It MUST NOT be used for a state the tool cannot evaluate (C-35), and it is not suppressible by a flag (FR-014, SC-002).

**C-35**: The receipt command exits `2` and writes no block when the base or head cannot be resolved, the target record file is missing, or the repository state is unusable. Exit `2` therefore means one thing only: cannot evaluate. The segment then records [[STR-002]] with the failure reason, and a partial block is never left behind. The exit alphabet is closed at `0` / `1` / `2` — no fourth code exists, and `1` and `2` MUST NOT be swapped (FR-006, FR-014).

**C-36**: A reasoned skip is a legal verdict only when its reason belongs to the closed reason set owned by `requirements.md` FR-014. This clause cites that owner instead of keeping a second list; a skip whose reason falls outside the set — free text included — is not a legal skip but a coverage gap, and it moves the exit code to `1` (C-34). A legal skip does not change the exit code and is excluded from `judged_files`. A skip is therefore disclosed rather than punished, and it is never counted as coverage the run did not earn (FR-014).

**C-37**: When `skipped_files` is greater than zero the segment verdict MUST NOT be [[STR-006]]. It is [[STR-007]] when the current [[STR-004]] record contains at least one `blocking` entry, and [[STR-002]] otherwise. Focus-driven review of an oversized diff keeps its path; it simply cannot be presented as a complete pass (FR-014, SC-002).

**C-38**: The segment verdict is derived from three signals together — `gap_files = 0`, `skipped_files = 0`, and no `blocking` entry in the current record. The third signal is a presence test over the record's headings as they stand: the feature defines no "clearing" action and no "cleared" state, so this clause never asks whether an entry was resolved. Only their conjunction yields [[STR-006]]; no single signal may stand in for the verdict, and no verdict may be assigned by hand before the three are counted. The conjunction is scoped to triage = [[STR-005]] with a non-empty changed set: an empty delta is triaged to [[STR-001]] before the receipt runs (C-7 of `command-orchestration.md`) and MUST NOT reach this clause, where an absolute conjunction would return a 0/0/0 pass over nothing (FR-014).

**C-39**: The segment verdict is exactly one of [[STR-006]], [[STR-007]], [[STR-001]], [[STR-002]]. There is no fifth value, no empty value, and no meaningful absence: a segment that produced nothing is [[STR-002]] with a reason (FR-003, FR-011).

**C-40**: The block's `renderer` value MUST equal the mode carried by the record's renderer marker, and both are written by the same command invocation. A contract test asserts the equality so the two forms cannot drift into disagreement (FR-013, FR-014).

**C-41**: `lines_added` and `lines_deleted` are measured from `git diff --numstat` over the resolved range. A quantity that cannot be measured means the block is not written (exit `2`); it MUST NOT be written as zero and MUST NOT be estimated (FR-014).

**C-42**: The block's grammar is stable enough that a contract test parses it without heuristics: the test asserts the closed name set, the counting identity `judged_files + skipped_files + gap_files = changed_files`, and the exit codes — never prose (FR-014, FR-028).

**C-43**: A non-zero gap count or skip count MUST be surfaced outside the block as well — in the process report's code subsection (C-9 of `command-orchestration.md`) and in the feature detail's `## Latest Review` review-record entry (C-13 of the same file). A shortfall visible only to a reader who scrolls into the block is not a disclosure (FR-005, FR-014).

**C-44**: The record MUST disclose the existence of unreviewed uncommitted scope when the working tree is dirty, and MUST NOT issue any conclusion over that scope. The disclosure is by design carried twice — in the record and in the process report's code subsection — as one fact with two carriers, not two criteria, so a reader who opens only the report still learns the scope was excluded. The default review object remains the committed delta (FR-005).

**C-74**: The receipt block is the single source of the four counts (`changed_files`, `judged_files`, `skipped_files`, `gap_files`). Every other place that shows them — the process report's code subsection and the feature detail's `## Latest Review` review-record entry — copies the block field by field and MUST NOT recompute, re-aggregate, or derive them from the record's prose. A contract test asserts the three agree, mirroring the equality assertion C-40 already carries for the renderer literal, so a later edit cannot move a number in one place only. This clause is appended in remediation round 1 rather than inserted, so no existing clause id changes (FR-011, SC-001, SC-002).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-31 | FR-014 | — | record block |
| C-32 | FR-014 | — | script + test |
| C-33 | FR-014 | SC-002 | script + test |
| C-34 | FR-014 | SC-002 | script exit |
| C-35 | FR-006, FR-014 | — | script exit |
| C-36 | FR-014 | SC-002 | script + report |
| C-37 | FR-014 | SC-002 | derivation |
| C-38 | FR-014 | — | derivation |
| C-39 | FR-003, FR-011 | — | record + report |
| C-40 | FR-013, FR-014 | SC-003 | script + test |
| C-41 | FR-014 | — | script |
| C-42 | FR-014, FR-028 | SC-002 | test |
| C-43 | FR-005, FR-014 | — | report + feature detail |
| C-44 | FR-005 | — | record + report |
| C-74 | FR-011 | SC-001, SC-002 | receipt block + report + feature detail |

## Amendment log — remediation round 1 (2026-10-27)

Trigger: `test-evidence/analyze-report.md` (`GATE: CRITICAL=0 HIGH=6`) and `notes/remediation-round-1.md`. C-31…C-44 keep their ids and their meaning; **C-74 is appended** (no renumbering, no insertion), so the file's clause range is C-31…C-44 plus C-74.

| Clause | Change | Why (finding) |
|--------|--------|---------------|
| C-34 | exit `1` becomes the closed meaning "coverage gap", and an unrecognised skip reason joins its triggers | A-12, A-13 |
| C-35 | exit `2` becomes the closed meaning "cannot evaluate"; the alphabet is stated as closed at 0/1/2 | A-12 |
| C-36 | the skip-reason set is owned by FR-014 and cited; an unrecognised reason is a gap, not a legal skip | A-13 |
| C-37 | `blocked` reads the current record's `blocking` entries (presence), not "unresolved" ones | A-05 |
| C-38 | the three-signal conjunction is scoped to triage = [[STR-005]] with a non-empty changed set; presence semantics stated | A-05, A-11 |
| C-39 | the two verdict literals become [[STR-006]] / [[STR-007]] | A-14 |
| C-43 | the two carriers replace the closing summary | A-01 |
| C-44 | the uncommitted disclosure is stated as a dual carrier by design | A-04 |
| C-74 | new: the block is the single source of the four counts, with a three-way equality assertion | A-29 |
