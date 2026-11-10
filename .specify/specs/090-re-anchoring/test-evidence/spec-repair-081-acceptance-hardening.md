# Spec repair — 081-acceptance-hardening (dead-reference repair)

**Date**: 2026-11-10 · **Tree**: main worktree `/storage/project/cloud-native-ai/spec-kit` (master) · **Mode**: read-first, bounded (no commit, no push, no subagents) · **Spec**: `.specify/specs/081-acceptance-hardening/` (live; not archived)

## Inputs

- Prior audit: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-live-batch-7.md` § 081-acceptance-hardening (`BROKEN`; 13 dead + 6 moved).
- Deterministic settled scan: `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` → key `.specify/specs/081-acceptance-hardening` → `dead_list` = **20 distinct tokens** (the authoritative work list; occurrence scan over the spec's `.md`/`.txt` files finds **165 token-occurrences**).

## Counts

| Measure | Count |
|---|---|
| Distinct dead tokens (settled `dead_list`) | **20** |
| Dead token-occurrences scanned | **165** |
| live-fixed occurrences | **9** (9 lines; 10 edited lines total, 5 files) |
| — path tokens rewritten | 15 (9 dead-form + 6 co-located moved-form index paths) |
| dated-kept occurrences | **77** |
| non-reference occurrences | **79** |

Post-repair residual: **38** occurrences of `.specify/memory/features/` remain in 22 files — every one classified `dated-kept`; **0 live normative pointers** remain on a dead path.

### Disposition criterion applied

- **live normative pointer** — a present-tense routing/ownership statement in the feature's *operative* artifacts: requirements binding basis, plan `Dependency artifacts` block ("the checker reads only the paths in this block"), data-model carrier declaration ("the live value lives in …"), the feature-ref routing card, and the final `tasks.md` gate/status-landing rows (the artifact the validators and closure checker consume).
- **dated-kept** — prose/captures recording a past run or measured reading: `notes/**`, `test-evidence/**`, dated `checklists/*-2026-11-03.md`, `review*.md` / `code-review*.md` review records, verification narrative, plan/research measured readings, clarification records, and the archived slice task files `tasks-081a/081b/081c.md` (the plan itself calls the 081b reading "the dated record of that slice's closure").
- **non-reference** — template placeholder, scanner prefix artifact of a live longer path, quoted diff, or prose shorthand that is not a filesystem path.

## Per-entry disposition (all 20 dead tokens)

| # | Dead token | Occ. | Disposition | Evidence (file:line) |
|---|---|---:|---|---|
| 1 | `.specify/memory/features/` | 47 | **9 live-fixed / 38 dated-kept** | fixed rows below; kept rows in the dated list below |
| 2 | `.specify/.tmp/081a-head-failed-clean.txt` | 2 | dated-kept | `test-evidence/closure-clean-run.txt:1671`; `notes/red-first-evidence.md:183` |
| 3 | `.specify/.tmp/081d-t001-probe` | 2 | dated-kept | `notes/red-first-evidence-081d.md:20,29` |
| 4 | `.specify/.tmp/probe-specB` | 1 | dated-kept | `notes/red-first-evidence-081b.md:135` |
| 5 | `.specify/.tmp/081a-head-failed.txt` | 9 | dated-kept | `tasks-081a.md:127`; `test-evidence/closure-repair-run{,2}.txt`; `notes/red-first-evidence.md:88,90,95,102,108,157` |
| 6 | `src/services/` | 1 | non-reference | `notes/red-first-evidence-081d.md:139` — inside quoted grep output of `templates/tasks-template.md:212` (`Implement [Service] in src/services/[service].py`), a template placeholder |
| 7 | `.specify/.tmp/081c-closure-verdict.json` | 5 | dated-kept | `review-081c.md:405`; `tasks-081c.md:140,141`; `test-evidence/tasks-081c-pre-analyze.txt:5`; `notes/red-first-evidence-081c.md:708` |
| 8 | `.specify/memory/features/NNN.md` | 1 | dated-kept | `review-081c.md:557` — quoted before/after diff of the owner-doc example (review record) |
| 9 | `.specify/specs/081-acceptance-hardening/notes/analyze-081c` | 2 | non-reference | `review-081c.md:10` (`notes/analyze-081c*.md` glob; `notes/analyze-081c.md` + `analyze-081c-r2.md` exist); `:237` (`notes/analyze-081c-r2.md:80`, exists) — scanner prefix artifacts |
| 10 | `.specify/.tmp/probe-specA` | 1 | dated-kept | `notes/red-first-evidence-081b.md:134` |
| 11 | `.specify/.tmp/081b-closure-verdict.json` | 3 | dated-kept | `tasks-081b.md:126`; `notes/red-first-evidence-081b.md:220,242` |
| 12 | `skills/internal/review-sdd-process/references/` | 7 | **1 non-reference / 6 dated-kept** | `tasks-081c.md:124` cites it as the **rejected antithesis** ("would give the process skill a second judgment object"; the skill ships only `SKILL.md`) → non-reference; 5 pre-analyze captures + `notes/red-first-evidence-081c.md:523` → dated-kept |
| 13 | `.specify/specs/071` | 15 | non-reference | every hit is the prefix of live `.specify/specs/071-review-code-integration/…` paths (or shorthand inside dated records) |
| 14 | `.specify/specs/077` | 9 | non-reference | every hit is the prefix of live `.specify/specs/077-doc-sdd-integration/…` paths |
| 15 | `docs/CHANGELOG` | 6 | non-reference | quoted plan § D10 scope phrase "mirrors/regen, docs/CHANGELOG" (`plan.md:344`; `tasks.md:11,211`; `tasks-081b.md:215`; `tasks-081c.md:256`; `test-evidence/checklist-081d-probes.txt:411`) — prose shorthand; the real changelog is root `CHANGELOG.md` (exists), and `docs/` + `CHANGELOG.md` are listed separately at `plan.md:204` |
| 16 | `.specify/.tmp/review-081c-verdict.json` | 2 | dated-kept | `review-081c.md:190,198` |
| 17 | `tests/contract/test_review_` | 45 | non-reference | prefix of the three live modules `test_review_code_composition.py`, `test_review_docs_isomorphism.py`, `test_review_feedback_boundary.py` (all verified on disk) or the `tests/contract/test_review_*` glob (static prefix dir exists) |
| 18 | `.specify/.tmp/review-081b-verdict.json` | 4 | dated-kept | `review-081b.md:32,33,47,58` |
| 19 | `.specify/.tmp/081a-head-failed-final.txt` | 2 | dated-kept | `test-evidence/closure-final-run.txt:1671`; `notes/red-first-evidence.md:199` |
| 20 | `scripts/external` | 1 | dated-kept | `checklists/081b-2026-11-03.md:69` — dated checklist prose ("`scripts/external` 侧的现状（P9：pre-analyze 无对应读取面）") |

Occurrence totals: 9 + 77 + 79 = **165**.

## Live-fixed entries (before → after)

All targets verified on disk after the edit: `.specify/features.md`, `.specify/features/081-acceptance-hardening.md`, `.specify/features/071-review-code-integration.md`, `.specify/features/077-doc-sdd-integration.md`, and the `<ID>-<slug>.md` convention (e.g. `.specify/features/061-subagent-cli-config.md`). The live checker reads the new anchor: `scripts/python/closure-acceptance-check.py:574` `repo_registry = Path(resolved["repo"]) / ".specify" / "features.md"`.

| File:line | Before | After | Why live |
|---|---|---|---|
| `requirements.md:15` | `.specify/memory/features/081.md`, `.specify/memory/features.md` | `.specify/features/081-acceptance-hardening.md`, `.specify/features.md` | Binding-basis statement of where the detail and index row live (co-located moved-form index path fixed with the same pointer) |
| `plan.md:242` | `.specify/memory/features/071.md` | `.specify/features/071-review-code-integration.md` | `Dependency artifacts` block: "the checker reads only the paths in this block" |
| `plan.md:243` | `.specify/memory/features/077.md` | `.specify/features/077-doc-sdd-integration.md` | same block |
| `data-model.md:148` | `.specify/memory/features/<ID>.md` | `.specify/features/<ID>-<slug>.md` | "the live value lives in … `**Status**`" — carrier declaration |
| `feature-ref.md:6` (+ co-located `:5`) | `.specify/memory/features/081.md`, `.specify/memory/features.md` | `.specify/features/081-acceptance-hardening.md`, `.specify/features.md` | Feature-routing card (`Feature index row` / `Feature detail`) |
| `tasks.md:49` | `.specify/memory/features.md` + `.specify/memory/features/*.md` | `.specify/features.md` + `.specify/features/*.md` | GATE-6 zero-write check definition (live subject paths) |
| `tasks.md:52` | `.specify/memory/features.md`, `.specify/memory/features/081.md` | `.specify/features.md`, `.specify/features/081-acceptance-hardening.md` | GATE-9 "record and claim agree" check |
| `tasks.md:154` | `.specify/memory/features.md`, `.specify/memory/features/081.md` | `.specify/features.md`, `.specify/features/081-acceptance-hardening.md` | T018 status-landing carrier statement |
| `tasks.md:205` | `.specify/memory/features.md`, `.specify/memory/features/081.md` | `.specify/features.md`, `.specify/features/081-acceptance-hardening.md` | T018 traceability row (same carriers) |

Edited lines containing a settled dead token: 9; plus 1 co-located line (`feature-ref.md:5`) whose moved-form index path was corrected so the routing pair stays coherent → **10 edited lines in 5 files**. Path tokens rewritten: 15 (9 dead-form + 6 co-located moved-form `.specify/memory/features.md` → `.specify/features.md`). `git diff --stat`: 5 files, 10 insertions / 10 deletions.

## Dated-kept occurrences of `.specify/memory/features/` (38; text unchanged)

`code-review.md:17,91`; `plan.md:231` (measured extraction reading); `requirements.md:275` (clarification record, "已落 …"); `research.md:123` (research measurement); `review-081b.md:37`; `review-081c.md:189,556,557`; `review.md:149,173,187,267,321`; `tasks-081a.md:19,126` (archived slice 081a); `tasks-081b.md:48` (slice 081b gate); `tasks-081c.md:46` (slice 081c gate); `verification.md:81` (verification narrative); `checklists/081b-2026-11-03.md:6,99,260,268`, `checklists/081c-2026-11-03.md:6,293`, `checklists/081d-2026-11-03.md:6`, `checklists/acceptance-2026-11-03.md:6,90,227` (dated checklists); `test-evidence/checklist-081b-probes.txt:52,144`, `checklist-081c-probes.txt:299`, `checklist-081d-probes.txt:346`, `checklist-fix-report.md:26`, `closure-verdict.txt:1` (captured command line); `notes/analyze-081d.md:4`; `notes/red-first-evidence-081c.md:515,517`.

## Validator readings

Working tree was clean for the edited paths before the repair (`git status --porcelain` empty for the spec dir and the registry/detail files).

**Before edits**

```
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/081-acceptance-hardening/requirements.md
status: ok — id-contiguous 0, doc-order 0, ref-resolvable 0, marker-count 0, dup-id 0, path-marker 0
scanned: 281 lines, 34 definition rows, 17 shared strings; 0 error(s), 0 warning(s); exit 0

$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/081-acceptance-hardening/tasks.md
PASS: 0 error(s), 0 warning(s); exit 0
```

**After edits** — identical readings:

```
$ python3 .specify/scripts/python/validate-requirements.py .specify/specs/081-acceptance-hardening/requirements.md
status: ok — all six checks pass (0); scanned: 281 lines, 34 definition rows, 17 shared strings; 0 error(s), 0 warning(s); exit 0

$ python3 .specify/scripts/python/validate-tasks.py .specify/specs/081-acceptance-hardening/tasks.md
PASS: 0 error(s), 0 warning(s); exit 0
```

`plan.md`, `data-model.md` and `feature-ref.md` have no dedicated validator; no other validator was re-run.

## Scope notes

- **Registry row**: `.specify/features.md` row `| 081 |` already resolves — Status `Completed`, Details `.specify/features/081-acceptance-hardening.md`, Spec Path `.specify/specs/081-acceptance-hardening/requirements.md`; the detail file's `**Status**: Completed` agrees. **No registry edit** (row is neither stale nor missing).
- No file outside `.specify/specs/081-acceptance-hardening/` was modified; the only other write is this evidence file.
- No commit, no push, no subagents.
