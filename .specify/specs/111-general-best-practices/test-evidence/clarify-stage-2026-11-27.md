# Clarify Stage Record — 111-general-best-practices

**Date**: 2026-11-27
**Run**: `r20261127T071500Z-111a` · line `general-best-practices` · stage `clarify`
**Worktree**: `.specify/.tmp/sdd-loop/worktrees/general-best-practices` (branch `111-general-best-practices`, base `0419adae5`, stage baseline `d53d3c228`)
**Mode**: A (Post-Requirements) — `plan.md` absent in the feature's requirements dir; target `requirements.md`
**Target file**: `.specify/specs/111-general-best-practices/requirements.md`

## Preconditions measured

- Prerequisite script: `scripts/bash/check-prerequisites.sh --json --paths-only` → `MODE: A`, `WRITABLE: true`, `FEATURE_SPEC` resolves to this feature's `requirements.md`.
- Writability: confirmed by the prerequisite JSON above; no read-only fallback needed.
- Working tree at start: clean (`git status --short` empty).
- Line containment at start: `git diff --name-only 0419adae5..HEAD` = 12 paths, all inside FR-009's declared set (spec artifacts + three accounting records).
- Run id parity: the state spine's `run_id` is `r20261127T071500Z-111a`, matching FR-009's record-body predicate.

## Grounding facts verified before adjudicating

Source (ai-harness 087):

1. Five documents read in full: manifest declares the closed four-category set as a single Markdown table (`模块 | 文件 | 内容`, four rows, one relative link each); three owner files carry the `*(尚无条目。…)*` placeholder; `programming-tools.md` seeds `## Git clone 的默认协议` with `**实践**` / `**反例 / 证据**` / `**延伸**` bullets.
2. Source guard (`tests/contract/test_general_best_practices.py`) pins by substring: manifest categories, category files, accumulation declaration, first-entry tokens, mirror parity, and absence of a second-mechanism engine file.
3. Source contract C-001…C-005 and verification: mirror parity + baseline preserved; no map row, no instructions pointer.

Target (spec-kit, base `0419adae5`):

4. `shared/best-practices/` and `.specify/shared/best-practices/` do not exist yet.
5. `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` contains `("shared", ".specify/shared", False, set())`; `tests/contract/test_mirror_parity_suite.py` exists and derives its table from the engine.
6. `shared/definitions/framework-map.md` is a single three-column layout table; the `.specify/shared/` rows use a `(framework source: …)` sibling pointer style.
7. `src/specify_cli/__init__.py` copies `shared/` wholesale into `.specify/shared/`; `tests/integration/test_init_new_layout.py` runs `init --here --ai qoder --script sh --no-git` end-to-end but does not name `shared/best-practices/`.
8. `.specify/scripts/python/feedback-utils.py --help` lists the `record` action; `.specify/shared/guidelines/knowledge-promotion.md` exists.
9. No Feature 111 registry row exists; `.specify/glossary.md` carries neither candidate term; `.specify/.gitignore` ignores `state/`, `trigger/telemetry.jsonl` and `.tmp/`.
10. Validator rules read: doc-order anchors on definition lines only; Shared Strings `Consumed by` reverse consistency requires every named row to cite the id.

## Taxonomy coverage scan (Mode A)

| Category | Status | Outcome |
|----------|--------|---------|
| Feature Linkage | Clear | Feature 111 + name present; registry row deferred by brief (A-3 amended to say "feature-registration stage"). |
| Functional Scope & Behavior | Clear | 9 FR + explicit "不做什么"; no change. |
| Domain & Data Model | Partial → Resolved | Entry/Observation/Manifest/Guard shapes pinned (C2/C3). |
| Interaction & UX Flow | Clear | Docs-only; no UI surface. |
| Non-Functional Quality Attributes | Clear | Zero runtime change; A-14 covers re-init semantics. |
| Integration & External Dependencies | Partial → Resolved | Distribution, mirror and init proof (C4); map row (C5). |
| Edge Cases & Failure Handling | Partial → Resolved | Placeholder/entry exclusivity, delivery-count tension, hand-edited mirror, glossary boundary added. |
| Constraints & Tradeoffs | Partial → Resolved | Containment residual procedure (C6). |
| Terminology & Consistency | Partial → Resolved | Vocabulary handoff (C7): proposal text frozen, registration externalized. |
| Completion Signals | Partial → Resolved | SC-002/003/004/006 measurement forms aligned to decidable oracles. |
| Misc / Placeholders | Clear | No TODO/TBD/NEEDS CLARIFICATION markers. |
| Deferred-by-assumption | Clear after A-3/A-10 amendments | A-3 and A-10 now name the deferral target explicitly; no other entry holds an open choice. |

Every candidate passed the materiality filter: each changes the guard's assertions, the verification procedure, or a downstream artifact's wording.

## Clarifications made (self-adjudicated, recorded in the spec)

1. **Closed-set machine form** (A-15) — exactly five top-level documents; the manifest's sole three-column four-row table with one relative link per row, link-target set equal to the four owner files, literal `封闭集`. Touches FR-001, FR-007(a), SC-001.
2. **Entry shape and empty-category invariant** (A-16) — entry = `## ` title + `**实践**` + `**反例 / 证据**` bullets (optional `**延伸**`; promoted entries add `**来源**`); placeholder ⇔ zero entries; the guard never freezes the delivery count 3 and never claims semantic-fabrication detection. Touches FR-001/FR-002/FR-007(b), A-11, SC-001, SC-003, Edge Cases, Key Entities.
3. **Promotion/replay traceability** (A-17) — observation notes carry `[best-practice]` + one owner-file stem (no new fields/actions/stores); promoted entries carry `**来源**` (feedback id / ≥7-hex commit / quoted session words) with the generality basis; seed exempt, no fabricated feedback ID. Touches FR-003, FR-004, FR-007(b), Key Entities.
4. **Distribution, mirror and init proof** (A-18) — mirrors regenerated by `sync-mirrors.py` write mode in the same change; byte parity solely by the existing parameterized suite; init proof = code-path citation + existing init integration test + recorded read-only init drill under `.specify/.tmp/`; no second test file; guard registered with `pytest.mark.contract`. Touches FR-006, FR-007, SC-004.
5. **Framework-map row shape** (A-19) — one row in the sole layout table, adjacent to the `.specify/shared/` rows; Where = `.specify/shared/best-practices/`; Notes carries Feature 111 + `README.md` pointer + `(framework source: shared/best-practices/)`; exactly one row in source and mirror. Touches FR-005, FR-007(e), SC-004.
6. **Containment residual procedure** (A-20) — path-set difference, then the record-body predicate over the three accounting stores; per-entry writes only; no aggregate/index or trigger/state writes. Touches FR-009, SC-006.
7. **Vocabulary handoff** (A-21) — proposal text frozen for "best practice / 最佳实践" and "progressive accumulation / 渐进积累"; no `.specify/glossary.md` write inside this line (FR-009's closed set excludes it; a write requires amending FR-009 first). Touches A-10.

Also amended: A-3 (registry deferral target made explicit), A-10 (points to A-21), A-11 (points to A-16). **No FR/SC id was added, removed or renumbered** — 9 FR / 7 SC / 16 definition rows / 7 shared strings unchanged; the quality checklist's derived counts stay valid.

## Files written

- `.specify/specs/111-general-best-practices/requirements.md` (clarifications + affected sections)
- `.specify/specs/111-general-best-practices/test-evidence/clarify-validator.txt`
- `.specify/specs/111-general-best-practices/test-evidence/clarify-stage-2026-11-27.md` (this file)

Sanctioned accounting writes (outside the spec dir, per FR-009):

- `.specify/session/20261127T073236Z-run-determination-speckit-clarify-r20261127t071500z-111a.md`
- `.specify/exec-quant/records/20261127T073241883504Z-2aeff455.json`
- `.specify/feedback/20261127T073252Z-speckit-clarify.md`

No engine, template, skill, agent, command, constitution/instructions, registry, glossary, mirror or spine edits.

## Gates

| Gate | Command | Verdict | Evidence |
|------|---------|---------|----------|
| Requirements validator (re-run) | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/111-general-best-practices/requirements.md` | `status: ok`, 0 error / 0 warning; 220 lines, 16 definition rows, 7 shared strings | `clarify-validator.txt` |
| Workspace guard | snapshot before writing; `--check` after all writes | see § Workspace guard below | `.specify/.tmp/sdd-loop/tmp/general-best-practices/workspace-snapshot-clarify.json` |

Validator repair iterations: **0** (the first post-edit run was already green). Two wording corrections were made outside the validator's semantic scope and disclosed below; the stamped run above is the final one.

## Test entry decision

`scripts/bash/run-tests.sh` was **not** run at this stage: no executable surface changed (requirements text only), and the content guard lands in the implement stage with red-first evidence (FR-007 / SC-007). Recorded as not warranted, not as a skipped obligation.

## Workspace guard

- Snapshot taken before the first write: `.specify/.tmp/sdd-loop/tmp/general-best-practices/workspace-snapshot-clarify.json`.
- Check run after all writes: **`clean`** (exit 0) — branch, refs and the `.specify/specs/` listing unchanged.
- Post-stage tree shows exactly the six expected paths: `requirements.md` (modified); the three accounting records (new); the two `test-evidence/` files (new). No registry, glossary, mirror, spine or engine writes.

## In-passing repairs (disclosed)

1. **Shared-Strings ellipsis in the new FR-007(a) text**: the first draft wrote `[[STR-002]]…[[STR-005]]`, which literally contains only STR-002 and STR-005; the validator's reverse-consistency rule requires every row named in a `Consumed by` cell to cite that id in its definition line. The four ids are now spelled out in FR-007(a) and the `Consumed by` cells name FR-007 truthfully. One reading, local, reversible.
2. **SC-004 Source label**: three evidence items were miscalled "两件套"; corrected to "三件证据". Cosmetic, local.
3. **A-3 deferral target**: "后续澄清/特性阶段" became stale once this clarify stage ran without registry writes (the brief forbids them); corrected to "后续特性登记阶段（clarify 阶段写面同样不含注册表，A-10、A-21）". One reading, local, reversible.

## Concurrency

`requested=1`, `effective=not_evaluated`, `effective_reason=single-unit` — one bounded clarification slice over one artifact; no independent units available to parallelize.

## Anomaly line

未发现异常 — no anomaly beyond the three disclosed in-passing repairs above.