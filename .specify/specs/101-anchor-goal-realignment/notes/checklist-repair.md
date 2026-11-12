# Checklist gate — round-1 repair record

- **Run**: `r20261112T064607Z-b101`, stage `plan` (checklist gate repair), 2026-11-12.
- **Authority**: `checklists/2026-11-12-requirements-quality.md` § 七 F-1…F-11 (11 fails) plus the
  downstream drift CHK025.
- **Rule of engagement**: every finding is closed in its **owner**, and the requirements are aligned to
  the contract when the contract already stated the behaviour (or the reverse) so exactly one answer
  survives. No user question was needed; no dated record was rewritten.

## 1. Finding → owner → change → evidence

| Finding | Owner(s) touched | Change landed | Evidence / gate |
|---------|------------------|---------------|-----------------|
| **F-1 / CHK003** — anchor body still speaks the retired terminology while FR-038/C-38 say "rename only" | `requirements.md` FR-005, FR-038; `contracts/migration-cleanup.contract.md` C-38, C-39, C-44 P1; `contracts/goal-engine.contract.md` C-35; `research.md` §5 (class C5); `tasks.md` T050, T067, T075 | **Normalization chosen** (the user ruling wants a live archive that speaks the new terminology). Rename stays byte-asserted; a **separate declared** normalization step applies A-N-1…A-N-4 (`^# Goal:` → `# Anchor:`, `.specify/goal\|teams` → `.specify/anchoring\|teams`, per-line `/speckit.goal` hints), each rewritten line recorded in `anchor-body-receipt.json`, unmatched lines byte-identical, digest computed through the same mapping. Measured surface: 9 headings + 4 retired refs (2 lines), all in `094-goal-team-parallel` | C5 baseline 16 lines (11 in the 9 retained anchors) → target 0: `test-evidence/checklist-repair-residue-baseline-2026-11-12.txt`; C-38 rules are the only writer |
| **F-2 / CHK004** — `.specify/features.md` and `.specify/features/` live but excluded from the scan | `research.md` §5 (roots + closed exclusion + class C7); `tasks.md` T042, T078, T080; `plan.md` WP-03; `feature-ref.md` R-18 | `.specify/features.md` becomes a **live file root**; `.specify/features/**/*.md` becomes a **recorded exclusion** (append-only delivery records, corrected by a dated successor note, never rewritten); class **C7** counts old-model index rows; the three rows that state the old model (027 / 041 / 094) are a WP-03 deliverable, and 094 gains the successor note 041 already had | C7 baseline 3 rows → target 0; T080 re-runs after the registry write |
| **F-3 / CHK024** — idempotency is 2 conditions in FR-043/D-4, 3 in C-41 | `requirements.md` FR-043, SC-007, D-4 | Both now read the **same three conditions** (target exists + receipt exists + digest equal); target-without-receipt → exit 4 `half-state`; digest mismatch → exit 4 `conflict` naming both paths, never a rewrite | Aligned to C-41/C-42; `validate-requirements.py` 0/0 |
| **F-4 / CHK026** — R3 "archive the team" was not operationalized | `requirements.md` FR-046; `contracts/migration-cleanup.contract.md` C-47; `classification.json` (`091`); `plan.md` § Phase 0 item 3; `feature-ref.md` R-20; `tasks.md` T057 | R3 terminal state stated: directory stays, `lifecycle_state: archived`, binding line removed, `disposition-receipt.json` inside the team directory (`bound_slug` / `reason` / `acted`); archived `team.md` remains a live definition under FR-047. `091-auto-git-closeout` was recorded `already-satisfied` although it still carries its `goal_slug` and has no receipt → corrected to `apply` | `run-checks 091` today = `ok/false` (still bound) — measured; contract C-47 carries the reasoning |
| **F-5 / CHK033** — SC-005 demanded "five checks pass" for R3 teams, which is unsatisfiable after the binding is removed | `requirements.md` SC-005 + Source; `tasks.md` T059, T067 (trace); `plan.md` G-5/G-6; `feature-ref.md` R-21 | SC-005 now reads `run-checks --json` per team: bound teams (incl. R2 `viz-skill-arena`) → `verdict: ok`, `blocked: false`, exit 0 with ②–④ honestly `not-evaluated`; R3 teams → `verdict: no-goal-definition`, `blocked: false`, exit 0, explicitly **not** a pass. The five-check enumeration is cited by owner (`skills/internal/run-team/SKILL.md` § 2 Preview), not restated | Measured: `089` (bound) = `ok/false`; `091` = `ok/false`; `demo-seat-dispatch` = `no-goal-definition/false`; `viz-skill-arena` = `no-goal-definition/false` (anchor missing today) |
| **F-6 / CHK031** — FR-061/SC-009 protect all dated spec dirs and test-evidence, contradicting FR-071's new 101 evidence | `requirements.md` FR-061, SC-009 | Both scope dated spec directories **and** dated test-evidence to **files baseline-existing at `d7c9da7a3`**; the 101 spec directory's own new artifacts and readings are additions outside the equality set | Same shape as the already-declared `.specify/archive/anchoring/**` addition rule |
| **F-7 / CHK034** — SC-008 unconditionally required the docs build, which EP-006 falsifies | `requirements.md` SC-008 + Source; `quickstart.md` unchanged; `tasks.md` T073 unchanged; `plan.md` EP-006 unchanged | SC-008 now states the docs-build limb reports **`not-evaluated`** with the EP-006 measurement (Hugo v0.141.0, `.Site.Language.Locale`, exit 1) and must not be recorded as a pass; the other limbs stay measurable, and no limb is silently waived | EP-006 (recorded at plan); `test-evidence/plan-baseline-2026-11-12.txt` |
| **F-8 / CHK017** — FR-065's single-writer claim was too broad | `requirements.md` FR-065; `contracts/migration-cleanup.contract.md` C-49; `contracts/goal-engine.contract.md` C-31 (already allowlisted); `tasks.md` T065 | FR-065 scoped to **definition files** (`anchor.md` / `goal.md`); `summary/**` is a legitimate derived writer (`build-summary-input.py`), named as the allowlist, with an injection case that still targets a definition write | C-31 allowlist + C-49 guard wording |
| **F-9 / CHK002** — the Goal↔Anchor relation was only negative | `requirements.md` FR-004, FR-023; `contracts/goal-command.contract.md` C-20; `data-model.md` E-2; `tasks.md` T008 | A Goal **carries no Anchor pointer**: no `anchor_ref` (or any Anchor-named key) in the schema, undeclared keys rejected exit 2; the only cross-reference is binding `origin`; Goal is not team-bound, sits outside the control hierarchy, and does not replace spec/plan/tasks | C-20 + E-2 forbidden row |
| **F-10 / CHK009** — engine strings still point to retired modes, `run-checks` still emits `goal_slug` | `requirements.md` FR-016; `contracts/goal-engine.contract.md` C-26, C-33; `research.md` §5 (class C6); `plan.md` WP-01/G-6; `feature-ref.md` R-22; `tasks.md` T017, T023, T042, T075 | FR-016 extended to engine **user-facing output**: the 8 hint sites (`goal-utils.py:1274,1294,1304,1310,1360,1363,1377,1393`) repoint to `/speckit.anchor`, and `run-checks` emits `anchor_slug`. Residue class **C6** guards it | C6 baseline 40 line-hits (8 engine × 2 mirrors, 16 team-domain refs, docs/glossary/src/team/index) → target 0 |
| **F-11 / CHK013** — `--scope auto` parsing defined but not write behaviour | `requirements.md` FR-031; `tasks.md` T011 | Writes under `auto` are **rejected**: exit 2 `scope-read-only`, zero writes, on all three layers (structured reading of the existing semantics in C-25, not an invention) | C-25 already stated it; T011 now names the literal |
| **CHK025** — T052 used `archive-receipt.json` while FR-042/C-40 use `migration-receipt.json` | `tasks.md` T052 | Task corrected to `migration-receipt.json` | C-40 |

**Observations touched for coherence (same pass, no new source of truth):**

- FR-010 / FR-019: `modify` emptying a required narrative or the completion-condition set now requires
  explicit user approval — the contract already required it (C-6 via anchor-command, C-16).
- FR-020: "非零退出" → **exit 2**, matching C-15 and `[[STR-007]]`.
- FR-033: the existing-action list is declared **illustrative, not closed**; unlisted actions keep
  their layer's semantics.
- SC-001 Source pointed at a nonexistent "§ Live-surface roots" inside the spec; it now owns nothing
  and points only at `research.md` §5.
- `classification.json` `091-auto-git-closeout.state` → `apply` (see F-4).
- `research.md` §3 row 7 evidence wording updated to the new terminology.

## 2. Rebaseline events (requirements changes, old → new)

| Clause | Old | New | Reason | Affected downstream |
|--------|-----|-----|--------|---------------------|
| FR-004 | ends at "任何控制层级位置" | + no `anchor_ref` / Anchor-named key; undeclared key exit 2; relation to SDD/Team | F-9 | C-20, data-model E-2, T008 |
| FR-005 | contrary-definition ban only | + retained-anchor bodies are live surfaces; normalization via FR-038 | F-1 | C-38, T050 |
| FR-010 | seven modes | + `modify` emptying needs explicit approval | coherence with C-6 | — |
| FR-016 | live pages point to `/speckit.anchor` | + engine hints and `run-checks` JSON key `anchor_slug` | F-10 | C-26, C-33, T017, C6 |
| FR-019 | modify edits guidance + conditions | + emptying the condition set needs approval | coherence with C-16 | — |
| FR-020 | "非零退出" | exit 2 | coherence with C-15 | — |
| FR-023 | negative resolution only | + Goal↔SDD/Team relation stated | F-9 | C-20 |
| FR-031 | `auto` resolution only | + writes rejected `scope-read-only` | F-11 | C-25, T011 |
| FR-033 | fixed action list | list declared illustrative; no behaviour change | coherence | — |
| FR-038 | rename-only; summary regenerated | + declared body normalization A-N rules with per-line receipt | F-1 | C-38/39/44, T050, C5 |
| FR-043 | two-condition idempotency | three conditions; `half-state` / `conflict` exits | F-3 | C-41/42, T015, SC-007, D-4 |
| FR-046 | R3 "archive the team" | R3 terminal state + receipt location + `team.md` stays live | F-4 | C-47, T057, classification |
| FR-061 | dated records byte-identical | + "baseline-existing at `d7c9da7a3`" for dated spec dirs and test-evidence; own new artifacts excluded | F-6 | SC-009, T002, T070 |
| FR-065 | any code path writing the stores | definition files only; `summary/**` allowlisted | F-8 | C-31, C-49, T065 |
| SC-001 | two classes; Source cited a nonexistent section | all declared classes; Source → `research.md` §5 | F-2 / F-10 | T067, T075 |
| SC-005 | "five checks pass" for viz + demo | per-team `run-checks` readings with archived-team exemption | F-5 | T059, T066 |
| SC-007 | rerun produces zero diff | + `already-*` only when target + receipt + digest hold | F-3 | T060, T068 |
| SC-008 | docs build passes | docs-build limb `not-evaluated` with EP-006 measurement | F-7 | T073 |
| SC-009 | all dated spec dirs/test-evidence | + baseline-existing qualifier; 101's own additions excluded | F-6 | T070 |
| D-4 | "目标存在且回执存在" | three conditions; `half-state` / `conflict` | F-3 | — |

Counts are unchanged: **71 FR / 10 SC / 8 STR**. `validate-requirements.py` re-run: 0 error / 0 warning.

## 3. Gate readings (this repair round)

| Gate | Command | Reading |
|------|---------|---------|
| Requirements | `python3 scripts/python/validate-requirements.py .specify/specs/101-anchor-goal-realignment/requirements.md` | see § 4 |
| Tasks | `python3 scripts/python/validate-tasks.py .specify/specs/101-anchor-goal-realignment/tasks.md` | see § 4 |
| Pre-analyze (requirements / plan / tasks) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir … --stage <stage> --repo .` | see § 4 |
| Plan-change audit | `python3 .specify/skills/sdd-loop-driver/scripts/audit-plan-changes.py …` | see § 4 |

## 4. Recorded readings

Filled by the round-1 repair run after the edits; see the final block of the stage report and
`test-evidence/checklist-repair-residue-baseline-2026-11-12.txt` for the measured residue baselines.
