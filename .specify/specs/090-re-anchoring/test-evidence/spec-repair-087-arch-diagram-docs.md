# Spec Repair — 087-arch-diagram-docs

**Date**: 2026-11-10
**Spec**: `.specify/specs/087-arch-diagram-docs/` (live; settled scan kind = `live`)
**Sources**:
- Audit: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-1.md` § `087-arch-diagram-docs` (19 dead entries; its own refs 344 / dead 19).
- Deterministic scan: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` → `.specify/specs/087-arch-diagram-docs` (dead 41; `dead_list` = 20 entries).
- Baseline state: HEAD `9ac56bf10`, working tree edited only under the spec directory.
**Scope discipline**: no commit, no push, no subagents; no file outside the spec directory was modified (registry row 087 was checked and needed no edit — see § 5).

## 0. Summary counts

| Bucket | Occurrences | Entries |
|--------|------------:|--------:|
| **Dead total** (union of audit 19 + settled `dead_list` 20; 4 shared) | **200** | **35** |
| **live-fixed** | **12** | 5 (4 anchor paths + 1 archived-elsewhere path) |
| **dated-kept** | **117** | 17 |
| **non-reference** | **71** | 13 |

**Counting basis**: one *occurrence* = one literal dead-path occurrence in a `.md` file under the spec directory (grep-counted on the current tree); one *entry* = one dead path as listed by the audit or the settled scan. The two sources use different ref accounting (audit: occurrence-aware, dead 19; settled: path-token list, dead 41), so this report dispositioned the union at occurrence level: 75 audit-side occurrences (19 audit entries + the 1 archived-elsewhere ref listed in the audit prose) + 125 settled-only occurrences (16 entries not already in the audit list). 12 + 117 + 71 = 200.

## 1. Live-fixed (12 occurrences)

Every fix below is a pointer a current reader is expected to follow; all targets were verified to exist on disk. Dated status/reading parentheticals in the same lines were left untouched (`(Draft → Planned at this stage)`, `(status Planned)`).

| # | Site | Before | After | Basis |
|---|------|--------|-------|-------|
| 1–3 | `plan.md:54`, `plan.md:67`, `plan.md:99` | `.specify/memory/constitution.md` | `.specify/constitution.md` | `[anchor-move]`; the live plan template already carries the new path (`templates/plan-template.md:39,52,68`), so these were stale template copies in a live plan |
| 4 | `feature-ref.md:11` | `.specify/memory/features/087.md` | `.specify/features/087-arch-diagram-docs.md` | `[anchor-move]`; live binding map |
| 5 | `feature-ref.md:12` | `.specify/memory/features.md` | `.specify/features.md` | `[anchor-move]`; live binding map |
| 6 | `checklists/requirements-quality.md:8` | `.specify/memory/features/087.md` | `.specify/features/087-arch-diagram-docs.md` | `[anchor-move]`; live checklist scope pointer |
| 7–8 | `requirements.md:17` (two refs) | `.specify/memory/features.md` and `.specify/memory/features/087.md` | `.specify/features.md` and `.specify/features/087-arch-diagram-docs.md` | `[anchor-move]`; live requirements binding citation (the binding itself is still in force) |
| 9 | `requirements.md:33` | `.specify/memory/features.md` | `.specify/features.md` | `[anchor-move]`; live numbering-check citation |
| 10 | `contracts/flow-obligations.contract.md:29` | `.specify/memory/register.md` | `.specify/register.md` | `[anchor-move]`; live contract namespace disambiguation (`D-001` / `D-001-a` rows exist in the new register) |
| 11 | `contracts/diagram-obligation.contract.md:30` | `.specify/memory/register.md` | `.specify/register.md` | `[anchor-move]`; same disambiguation, reciprocal paragraph |
| 12 | `research.md:152` | `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` | `.specify/archive/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` | archived-elsewhere (audit § "Archived-elsewhere"); reading `→ 74` unchanged; `plan.md:384` already cites the archive form |

Target-existence checks (all yes): `.specify/constitution.md`, `.specify/features.md`, `.specify/features/087-arch-diagram-docs.md`, `.specify/register.md`, `.specify/archive/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt`.

## 2. Dated-kept (117 occurrences) — text unchanged

Dated records are not rewritten. Every site below is a checkpoint, a note, a verification/evidence file, a review record, or a dated prose block that records a past run or a past measurement (including line-numbered readings that no longer match the moved files).

| Entry | Occ. | Sites |
|-------|-----:|-------|
| `.specify/memory/features.md` | 10 | `checkpoints/02-clarify.md:13`; `code-review.md:119,395`; `tasks.md:334` (dated 2026-11-06 T075 progress note with line-numbered readings); `review.md:67,192,408`; `test-evidence/analyze-report-round2.md:19`; `test-evidence/plan-stage-status.md:69,73` |
| `.specify/memory/features/087.md` | 13 | `checkpoints/02-clarify.md:14`; `code-review.md:120,398`; `tasks.md:334`; `review.md:67,161,192,374,408,642,823`; `test-evidence/analyze-report-round2.md:19`; `test-evidence/plan-stage-status.md:69` |
| `.specify/memory/register.md` | 4 | `code-review.md:121,401` (diff-stat / `file.NNN.path` evidence lists); `test-evidence/plan-stage-status.md:69,74` |
| `.specify/.tmp/087-review3` | 1 | `review.md:44` — round-3 record; the scratch dir was used and removed by that run |
| `.specify/skills/external` and `/external/**` | 2 | `test-evidence/analyze-report-round1.md:29`; `test-evidence/analyze-repair-round1.md:105` |
| `.specify/specs/087-arch-diagram-docs/goal/087-arch-diagram-docs/goal.md` | 5 | `checkpoints/01-requirements.md:21`, `02-clarify.md:24`, `03-plan.md:32`, `closure.md:14`; `code-review.md:458` (plus the wrap-truncated diff stat at `code-review.md:140`) |
| `.specify/specs/087-arch-diagram-docs/team/087-arch-diagram-docs/team.md` | 3 | `checkpoints/03-plan.md:49`, `closure.md:25`; `code-review.md:485` (plus the truncated diff stat at `code-review.md:149`) |
| `.specify/specs/087-arch-diagram-docs/test-evidence/baseline-full-suite.log` | 1 | `verification.md:33` (`baseline_record=`); the sibling relative form at `checkpoints/07-implement.md:12` is the same dated record |
| `.specify/templates/commands` (+ `/docs.md` form) | 11 | `plan.md:566` (recorded pre-analyze gate output, itself labelled as paths that must not exist); `checkpoints/06-analyze.md:18`; `review.md:38` (×2), `158`, `371`, `605`, `608`; `test-evidence/analyze-report-round1.md:29`, `analyze-report-round2.md:40`, `analyze-repair-round1.md:105` |
| `skills/external/create-docs/contracts` | 1 | `review.md:209` — known-dead link recorded as evidence (P2) |
| `skills/external/create-docs/quickstart.md` | 1 | `review.md:209` — same known-dead link |
| `skills/external/humanize/SKILL.md` | 1 | `research.md:151` — dated grep reading (R7); the skill was later renamed to `humanize-conclusion` |
| `tests/fixtures/docs-obligation/conftest.py` | 5 | `code-review.md:187,594`; `review.md:85,725,811` — review records; fixtures now use `helpers.py` |
| `docs/assets/widget.mmd` | 17 | `code-review.md` ×16 (fixture diff stats); `notes/quickstart-run.md` ×1 |
| `docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json` | 13 | `code-review.md` ×8 (fixture diff stats); `notes/quickstart-run.md` ×5 |
| `docs/concepts/widget-overview.md` | 24 | `code-review.md` ×22 (fixture diff stats); `notes/quickstart-run.md` ×1; `review.md` ×1 |
| `docs/.speckit/runs` (standalone) | 5 | `plan.md:374,519` (dated measurement / known-red premise); `notes/quickstart-run.md` ×1; `review.md` ×1; `test-evidence/plan-stage-status.md` ×1 |

## 3. Non-reference (71 occurrences) — ignored

Examples, placeholders, design-defined future paths, tree-relative displays and prose tokens. None is a pointer to an existing artifact, so no target was invented.

| Entry | Occ. | Sites / class |
|-------|-----:|---------------|
| `.specify/templates/commands` (retirement assertions only) | 2 | `feature-ref.md:30`; `plan.md:266` — live docs asserting the subtree is retired and absent on both sides (a statement, not a pointer) |
| `.specify/templates/examples/structure-*.md` | 1 | `plan.md:201` — conditional template boilerplate; the live `templates/plan-template.md:117` carries identical text and no `examples/` ships |
| `scripts/docs-utils.py` | 1 | `plan.md:237` — tree-display path relative to the tree root `skills/external/create-docs/` (declared one line above at `plan.md:235`) |
| `scripts/python/diagram-obligation-check.py` | 1 | `plan.md:127` — hypothetical path inside a decision antithesis for a deliberately rejected alternative |
| `.specify/.tmp/space-stale-source.XXXXXX` | 1 | `quickstart.md:171` — `mktemp -d` template under the live `.specify/.tmp/` |
| `docs/.speckit/` (standalone) | 13 | design-defined machine directory owned by this spec's `C-010`/`C-011`; `plan.md:374` records that it does not exist in this repo by design |
| `docs/.speckit/exemptions/` | 12 | same class (design-defined record location / example records) |
| `docs/.speckit/runs` (standalone) | 15 | `plan.md` ×4 (design statements), `contracts/diagram-obligation.contract.md` ×3 (example/definition), `data-model.md` ×1, `quickstart.md` ×5 (fixture-relative), `tasks.md` ×2 (design) |
| `docs/.speckit/runs/20261106T090000Z-…-diagram-trace.json` | 8 | `quickstart.md` ×8 — `--record` values resolved relative to `--root tests/fixtures/docs-obligation/<space>` (fixture-relative) |
| `docs/assets/foo.png` / `.svg` / bare `foo` | 6 | `contracts/diagram-obligation.contract.md:225–228` (×5), `data-model.md:104` (brace display `foo.{mmd,svg,png}`) — example payload |
| `docs/assets/widget.mmd` | 1 | `quickstart.md:127` — fixture-relative |
| `docs/reference/diagrams/` | 1 | `plan.md:160` — antithesis example; `plan.md:566` states the `diagrams/` dirs are cited to show they must not exist |
| `docs/concepts/foo.md` | 2 | `contracts/diagram-obligation.contract.md:217,299` — example payload |
| `docs/concepts/changelog-shaped.md` | 1 | `contracts/diagram-obligation.contract.md:256` — example exemption record |
| `docs/concepts/widget-overview.md` | 3 | `quickstart.md` ×3 — fixture-relative `--only` examples |
| `tests/fixtures/docs-obligation/orphan-rendered/.../2026…-diagram-trace.json` | 1 | `code-review.md` — wrap-truncated path; resolves to the committed fixture file `tests/fixtures/docs-obligation/orphan-rendered/docs/.speckit/runs/20261106T090000Z-0870a1b2-diagram-trace.json` |
| `.specify/specs/087-` | 1 | `contracts/diagram-obligation.contract.md:14` — ellipsis prose token (`.specify/specs/087-…/contracts/`) |
| `scripts/tests` | 1 | `code-review.md:330` — prose meaning "scripts and tests" |

## 4. Settled-scan `dead_list` reconciliation (20 entries)

| # | `dead_list` entry | Occ. | Disposition |
|---|-------------------|-----:|-------------|
| 1 | `.specify/.tmp/space-stale-source.XXXXXX` | 1 | non-reference (mktemp template) |
| 2 | `docs/.speckit/` | 13 | non-reference (design-defined machine dir) |
| 3 | `docs/assets/foo.png` | 1 | non-reference (example payload) |
| 4 | `docs/reference/diagrams/` | 1 | non-reference (antithesis example) |
| 5 | `docs/assets/foo.svg` | 1 | non-reference (example payload) |
| 6 | `scripts/docs-utils.py` | 1 | non-reference (tree-relative display) |
| 7 | `skills/external/create-docs/quickstart.md` | 1 | dated-kept (`review.md:209`) |
| 8 | `docs/.speckit/exemptions/` | 12 | non-reference (design-defined) |
| 9 | `tests/fixtures/docs-obligation/orphan-rendered/.../2026…-diagram-trace.json` | 1 | non-reference (wrap truncation; committed fixture resolves) |
| 10 | `docs/concepts/foo.md` | 2 | non-reference (example payload) |
| 11 | `.specify/specs/087-` | 1 | non-reference (ellipsis prose) |
| 12 | `docs/assets/widget.mmd` | 18 | 17 dated-kept / 1 non-reference (fixture-relative) |
| 13 | `skills/external/create-docs/contracts` | 1 | dated-kept (`review.md:209`) |
| 14 | `docs/concepts/changelog-shaped.md` | 1 | non-reference (example record) |
| 15 | `docs/.speckit/runs/2026…-diagram-trace.json` | 21 | 13 dated-kept / 8 non-reference (fixture-relative) |
| 16 | `docs/assets/foo` | 4 | non-reference (brace display / example payload) |
| 17 | `docs/concepts/widget-overview.md` | 27 | 24 dated-kept / 3 non-reference (fixture-relative) |
| 18 | `docs/.speckit/runs` | 20 | 5 dated-kept / 15 non-reference |
| 19 | `scripts/tests` | 1 | non-reference (prose) |
| 20 | `.specify/specs/087-arch-diagram-docs/goal/087-arch-diagram-docs/goal.md` | 5 | dated-kept (checkpoints / review records) |

Entries 6, 7, 13 and 20 are shared with the audit list and are counted once. The audit's own reclassifications are preserved: the `mktemp` template, the fixture path, and `templates/commands/docs.md` as a live pytest node id remain non-dead.

## 5. Registry row

`087` row in `.specify/features.md` was read, not edited: status `Completed`, Feature Details `.specify/features/087-arch-diagram-docs.md` (exists, matches the anchor layout), Spec Path `.specify/specs/087-arch-diagram-docs/requirements.md` (exists). The row resolves; the "stale or missing row" clause does not apply.

## 6. Validator readings

No validator exists for `feature-ref.md`, `checklists/requirements-quality.md`, `contracts/*.md` or `research.md` (the installed set is the four `validate-*` scripts). The surrounding validator for the edited `plan.md` is `validate-decision-tensions.py`; `requirements.md` and `tasks.md` have their own validators.

| Validator | Before edits | After edits |
|-----------|--------------|-------------|
| `python3 .specify/scripts/python/validate-requirements.py .specify/specs/087-arch-diagram-docs/requirements.md` | `status: ok`; 6/6 checks pass; 318 lines, 33 definition rows; 0 error / 0 warning; exit 0 | identical: `status: ok`; 6/6 pass; 318 lines, 33 definition rows; 0 error / 0 warning; exit 0 |
| `python3 .specify/scripts/python/validate-tasks.py .specify/specs/087-arch-diagram-docs/tasks.md` | `PASS`; 0 error / 0 warning; exit 0 | identical: `PASS`; 0 error / 0 warning; exit 0 |
| `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs` | `status: ok`; 6/6 checks pass; 577 lines, 5 record(s); 0 error / 0 warning; exit 0 | identical: `status: ok`; 6/6 pass; 577 lines, 5 record(s); 0 error / 0 warning; exit 0 |

Post-edit residual grep: `.specify/memory/{constitution,features,register}.md` and `.specify/memory/features/087.md` occur only in `checkpoints/`, `code-review.md`, `review.md`, `tasks.md` (dated note) and `test-evidence/` — i.e. exactly the dated-kept set above; the old 069a spec path occurs zero times.

**Anomaly**: none.

SPEC-REPAIR-5-DONE
