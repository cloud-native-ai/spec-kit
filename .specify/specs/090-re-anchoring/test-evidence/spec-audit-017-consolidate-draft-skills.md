# Spec audit — 017-consolidate-draft-skills (batch 4)

- **Date**: 2026-11-10
- **Tree audited**: `/storage/project/cloud-native-ai/spec-kit` on `master` (current working tree, read-only; no spec or source file was modified by this audit)
- **Spec under audit**: `.specify/archive/specs/017-consolidate-draft-skills/`
- **Method**: every repository-path reference in the archived artifacts was extracted, then resolved against the current tree with filesystem existence checks. Contract tests, guard files and implementation claims were checked statically (files read); the only execution was `query.py --help`/`--version` discovery output, which the script itself documents as writing nothing. Git history was consulted for objects that disappeared from disk.

## Scope

Artifacts read in full:

| Artifact | Status |
|---|---|
| `requirements.md` | present |
| `plan.md` | present |
| `tasks.md` | present |
| `data-model.md` | present |
| `contracts/skill-format.md` | present |
| `quickstart.md` | present |
| `verification.md` | present |
| `feature-ref.md` | present |
| `checklists/requirements.md` | present |
| `notes.md` / `research.md` | **absent** — plan.md:10 explicitly says "No standalone research.md"; the audit set names notes, none exists |

Classification rule applied:

- **alive** — the target path exists in the current tree.
- **archived-elsewhere** — the reference is a bare spec-local filename and its content now exists under `.specify/archive/specs/017-consolidate-draft-skills/`, or the named spec is archived under `.specify/archive/specs/`.
- **dead** — no target exists; per the audit instruction, any path literally written as `.specify/specs/017-consolidate-draft-skills/...` is dead even though the same-named file survives in the archive. Subpaths under a removed draft-skill root are collapsed into that root's row (one fate); deliverable files named by more than one artifact are counted individually.

## Reference census

**Refs total: 68 distinct path references** (repeated occurrences of the same path counted once). Split: **alive 34 / archived-elsewhere 9 / dead 25**. Occurrence-level, the dead references appear **≈130 times** across the artifacts — dominated by 63 `draft/skills` matches and 53 `browser-utils` matches.

### Alive (34)

Document-utils deliverable (`skills/external/document-utils/`):

- `skills/` — root exists (packages live under `skills/external/` and `skills/internal/`).
- `skills/external/document-utils/` — tasks:36,155; quickstart:15.
- `skills/external/document-utils/SKILL.md` — contract:22; tasks T012–T018.
- `skills/external/document-utils/LICENSE.txt` — tasks:57.
- `skills/external/document-utils/scripts/office/` — soffice.py, pack.py, unpack.py, validate.py present; `helpers/{__init__,merge_runs,simplify_redlines}.py` and `validators/{__init__,base,docx,pptx,redlining}.py` present (plus an extra `schemas/` tree).
- `skills/external/document-utils/scripts/docx/` — accept_changes.py, comment.py, `__init__.py`, `templates/` with all 5 XML files.
- `skills/external/document-utils/scripts/pdf/` — all 8 named scripts present (check_bounding_boxes, check_fillable_fields, convert_pdf_to_images, create_validation_image, extract_form_field_info, extract_form_structure, fill_fillable_fields, fill_pdf_form_with_annotations).
- `skills/external/document-utils/scripts/pptx/` — add_slide.py, clean.py, `__init__.py`, thumbnail.py.
- `skills/external/document-utils/scripts/xlsx/recalc.py`.
- `skills/external/document-utils/references/pdf-forms.md`, `…/pdf-reference.md`, `…/pptx-editing.md`, `…/pptx-creation.md` — all present (plus 9 later-added reference docs).
- `skills/external/document-utils/themes/` — 10 theme `.md` files + `theme-showcase.pdf`.

Database-utils deliverable (`skills/external/database-utils/`):

- `skills/external/database-utils/` — tasks:37,156; quickstart:32.
- `skills/external/database-utils/SKILL.md`.
- `skills/external/database-utils/LICENSE.txt`.
- `skills/external/database-utils/connections.example.json` — 4 entries with `protocol` field: mysql/3306, postgres/5432, ClickHouse postgres/9005, Doris mysql/9030.
- `skills/external/database-utils/requirements.txt` — mysql-connector-python + psycopg2-binary.
- `skills/external/database-utils/.gitignore` — present.
- `skills/external/database-utils/scripts/query.py`, `…/query_mysql.py`, `…/query_postgres.py`.

Mirrors and framework files:

- `.specify/skills/` — root exists; 18 skill directories.
- `.specify/skills/document-utils/` — present; byte-identical to `skills/external/document-utils/` (`diff -r` clean).
- `.specify/skills/database-utils/` — present; byte-identical to `skills/external/database-utils/` (`diff -r` clean). Mirrors are real copies, not symlinks.
- `.specify/skills/<name>/` + `skill_id: "<SKILL:.specify/skills/<name>/SKILL.md>"` pattern — contract C-001/C-006; demonstrated alive by both surviving skills.
- `templates/skills-template.md` — plan:10; owns the frontmatter shape the contract describes.
- `templates/commands/skills.md` — plan:95; contract:34.
- `.specify/memory/features.md` — tasks:5 (alive today; see rename section).
- `.specify/memory/features/013.md` — tasks:159; feature-ref:25 (alive today; see rename section).
- `.specify/memory/constitution.md` — plan:28 (alive today; see rename section).
- `.specify/specs/012-skill-home-workdir` — feature-ref related spec; present.
- `.specify/specs/013-portable-skill-creation` — feature-ref related spec; present.

### Archived-elsewhere (9)

Bare spec-local filenames; each resolves to the archived copy:

| Reference | Anchor | Resolves to |
|---|---|---|
| `requirements.md` | plan:3,4 | `.specify/archive/specs/017-consolidate-draft-skills/requirements.md` |
| `plan.md` | tasks:7 | `…/archive/…/plan.md` |
| `data-model.md` | plan:52, tasks:7 | `…/archive/…/data-model.md` |
| `quickstart.md` | plan:115, tasks:7 | `…/archive/…/quickstart.md` |
| `tasks.md` | plan:57 | `…/archive/…/tasks.md` |
| `contracts/skill-format.md` | plan:54, tasks:7, quickstart:78 | `…/archive/…/contracts/skill-format.md` |
| `checklists/requirements.md` | plan:56 | `…/archive/…/checklists/requirements.md` |
| `007-skill-install-layout` (related spec) | feature-ref:16 | `.specify/archive/specs/007-skill-install-layout/` |
| `008-create-skills-skill` (related spec) | feature-ref:17 | `.specify/archive/specs/008-create-skills-skill/` |

### Dead (25) — broken list

Pre-archive spec paths (content preserved in the archive, links never repointed):

- `.specify/archive/specs/017-consolidate-draft-skills/plan.md:4` -> `.specify/specs/017-consolidate-draft-skills/requirements.md` — no such directory; the spec dir is `.specify/archive/specs/017-consolidate-draft-skills/`.
- `.specify/archive/specs/017-consolidate-draft-skills/feature-ref.md:25` -> `.specify/specs/017-consolidate-draft-skills/requirements.md` — same dead path, asserted as the live feature-index pointer.
- `.specify/archive/specs/017-consolidate-draft-skills/plan.md:49` -> `.specify/specs/017-consolidate-draft-skills/` — dead directory; archived copy exists.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:6` -> `.specify/specs/017-consolidate-draft-skills/` — dead directory; archived copy exists.

Source drafts (removed by this spec's own T043/T044; no archive copy anywhere on disk):

- `.specify/archive/specs/017-consolidate-draft-skills/requirements.md:6` (+ :70,74,78,106,113,124,133,139), `plan.md:8,66,69`, `tasks.md:20,140,142,144,145`, `quickstart.md:8,17,19–27,34,35,47–51,69,70,77`, `verification.md:35` -> `draft/skills/` — directory absent; `draft/` itself does not exist.
- `draft/skills/{docx-utils,pdf-utils,pptx-utils,theme-creator,xlsx-utils,mysql-utils,postgres-utils,playwright-utils,web-test}/` — all 9 named source drafts dead; every named subpath (e.g. `draft/skills/mysql-utils/scripts/query.py` at tasks:85, `draft/skills/web-test/examples/` at quickstart:50) dies with its root.

Deliverable path as written vs. current layout (skills were later reorganized under `skills/external/`):

- `.specify/archive/specs/017-consolidate-draft-skills/plan.md:63` + `data-model.md:10` -> `skills/document-utils/` — no such directory; successor `skills/external/document-utils/` is alive.
- `.specify/archive/specs/017-consolidate-draft-skills/plan.md:64` + `data-model.md:86` -> `skills/database-utils/` — no such directory; successor `skills/external/database-utils/` is alive.

Browser-utils deliverable (removed from the tree on 2026-10-08 by commit `15b5c683b "remove browser-utils skill"`; feature 048's registry row records relocation to `xuanji-extension`; no archive copy in this repo):

- `.specify/archive/specs/017-consolidate-draft-skills/plan.md:65`, `data-model.md:145`, `tasks.md:38,117–128`, `quickstart.md:45` -> `skills/browser-utils/` — missing (directory absent from `skills/`, `skills/external/`, `.specify/skills/` and every archive).
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:125–128` -> `skills/browser-utils/SKILL.md` — missing.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:117` -> `skills/browser-utils/scripts/js/{run.js,package.json}` — missing.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:118` -> `skills/browser-utils/scripts/python/with_server.py` — missing.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:119` -> `skills/browser-utils/references/playwright-api.md` — missing.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:120` -> `skills/browser-utils/examples/{console_logging.py,element_discovery.py,static_html_automation.py}` — missing.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:121` -> `skills/browser-utils/LICENSE.txt` — missing.
- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:157` -> `.specify/skills/browser-utils/` — missing (mirror removed with the source; contract C-006's mirror half now holds for 2 of 3 skills).

Renamed / never-created deliverable files:

- `.specify/archive/specs/017-consolidate-draft-skills/tasks.md:91` + `data-model.md:97` -> `skills/external/database-utils/references/README.md` — missing; the consolidated guide now lives at `skills/external/database-utils/references/setup-and-usage.md` (renamed by a later skill pass; `SKILL.md:213` points at the new name).
- `.specify/archive/specs/017-consolidate-draft-skills/contracts/skill-format.md:100` -> source root `skills/<name>/` in C-006 — stale as written; the current source root is `skills/external/<name>/` (the `.specify/skills/<name>/` mirror half is still accurate).

Related-spec reference that no longer resolves:

- `.specify/archive/specs/017-consolidate-draft-skills/feature-ref.md:15` -> `005-tool-skill-ids` — no `.specify/specs/005-tool-skill-ids/` and no archive copy; the spec name appears only in stale historical pointers inside `.specify/memory/features/013.md:117–122`.

## Ledger-target check

Ledger row audited: `.specify/archive/specs/CONSOLIDATION-LEDGER.md:13` — `017-consolidate-draft-skills | archive | Feature 013 child (historical; complete 50/50) | review-G2`.

- **Verdict column accurate**: the spec directory is in `.specify/archive/specs/017-consolidate-draft-skills/` (9 files) and `.specify/specs/017-consolidate-draft-skills/` does not exist — matching `archive`.
- **Target resolves**: Feature 013 resolves in the registry — `.specify/memory/features.md:22` (row `013 | Skills Command | … | Implemented`) points at `.specify/memory/features/013.md`, which exists and is titled "Skills Command". The detail records this iteration at lines 43–46 and the 2026-11-09 archiving at line 136.
- **"complete 50/50" accurate**: `tasks.md` has 50 `[X]` and 0 `[ ]`; `verification.md` records "All 50 tasks completed (T001-T050) … No tasks deferred."
- **Accuracy defects around the row**:
  1. `.specify/memory/features/013.md:77-78` still links `.specify/specs/017-consolidate-draft-skills/requirements.md` and `.../checklists/requirements.md` as "Historical" pointers — both dead (the registry's own links were not repointed when the spec was archived; the same defect the batch-2 audit found for its 007 links at lines 110–115).
  2. The Notes pointer `review-G2` has no retrievable artifact: no `review-G2.md` exists anywhere in the tree.
  3. `verification.md:15` still says `post_change_commit=pending` — the record was never closed out.
  4. The ledger row is silent on the fact that one of 017's three headline deliverables (browser-utils) was already removed before the ledger date; the surviving record of that removal is only in `features.md` row 048 (`Relocated`) and commit `15b5c683b`.
- Unrelated ledger formatting defect noticed while reading the table: the `054-agent-registration-wiring` row at `CONSOLIDATION-LEDGER.md:23` sits after the "Not executed" paragraph, outside the table (same defect the batch-2 audit reported).

## Missing guards

The 017 spec names **no** automated test or guard file anywhere — plan.md's Complexity Tracking explicitly waives automated tests (skills are prompt artifacts, validated manually), and every verification task (T019, T032, T042, T044, T048, T050) is a manual check. So there is no named guard that is missing.

De-facto guards that still name the surviving skills and exist today:

| Guard | Status |
|---|---|
| `tests/contract/test_migration_distribution.py` | present; lists `database-utils`, `document-utils` at :109-110 |
| `tests/contract/test_run_skills_wiring.py` | present; lists both at :38-39 |
| `tests/contract/test_expression_compatibility.py` | present; lists `skills/external/{database,document}-utils/SKILL.md` at :165-166, :869-870 |
| `tests/contract/test_skill_layer_visibility_guards.py` | present; lists both at :57 |

Missing guards for the removed deliverable: `tests/contract/test_browser_site_memory.py` and `tests/contract/test_browser_site_exclusions.py` were deleted together with the skill in commit `15b5c683b`; no current test references `browser-utils` at all. These files postdate 017 (they guard the 046 site-memory work) but are the only automated guards the browser-utils deliverable ever had, and their removal is what let the skill disappearance go unguarded.

## Three implementation claims — spot checks

1. **File claim** (`data-model.md:13-54`, tasks T004–T008): `document-utils` carries one deduplicated `scripts/office/` tree plus format-specific script directories. **Holds**: `scripts/office/{soffice,pack,unpack,validate}.py` + `helpers/` + `validators/` exist once; `scripts/{docx,pdf,pptx,xlsx}/` contain all named files; the PDF directory has exactly the 8 claimed scripts; `scripts/docx/templates/` has all 5 XML templates.
2. **Symbol/command claim** (FR-004/FR-006, contract C-004, tasks T022): the unified `query.py` exposes `--list/--tables/--schema/--query/--limit` (plus `--db`, `--config`) and routes by the connection's `protocol` field with port inference. **Holds**: `skills/external/database-utils/scripts/query.py:78-116` (`determine_protocol` → `load_handler` dynamic import of `query_mysql.py`/`query_postgres.py`), port map at :26-29 (`3306→mysql`, `9030→mysql`, `5432→postgres`, `9005→postgres`); `query.py --help` prints all six options and the script-interface footer (`--version`, exit codes).
3. **Behaviour surface claim** (SC-001/SC-006, contract C-002/C-003/C-006): each SKILL.md has format sections, `## Path Conventions` with `${SKILL_HOME}`/`${SKILL_WORKDIR}`, EN+CN triggers, a `skill_id`, and a byte-equivalent mirror. **Holds for the two survivors**: `document-utils/SKILL.md` has `## Quick Reference`, `## DOCX`, `## PDF`, `## PPTX`, `## XLSX`, `## Themes`, `## Path Conventions`, 26 `${SKILL_HOME}` mentions; `database-utils/SKILL.md` has its C-004 sections and 14 `${SKILL_HOME}` mentions; both frontmatters carry EN/CN triggers and `<SKILL:.specify/skills/<name>/SKILL.md>` IDs; both `diff -r` mirrors are clean. Two numeric drifts from the archived verification record: `verification.md:23` claims a 1,469-line document-utils SKILL.md and 89 files — current values are 208 lines and 98 files (later rewrite/expansion); database-utils is 9 files as claimed; browser-utils (claimed 8 files) has 0.

## Pending anchor-layout rename — references that will move

The `rename-anchors` worktree (`.specify/.tmp/sdd-loop/worktrees/rename-anchors`, commit `8b9030371 "refactor(layout): move the project anchors out of memory/"`) moves the project anchors out of `.specify/memory/`. The following references from this spec are alive today but will move:

| Current reference (anchors) | Post-rename target |
|---|---|
| `.specify/memory/constitution.md` (plan:28) | `.specify/constitution.md` |
| `.specify/memory/features.md` (tasks:5) | `.specify/features.md` |
| `.specify/memory/features/013.md` (tasks:159, feature-ref:25) | `.specify/features/013-portable-skill-creation.md` (filename gains the slug; verified in the worktree) |

The stale `.specify/specs/017-consolidate-draft-skills/...` links listed as dead remain dead after that rename (they are pre-archive paths, not `memory/` anchors), including the registry's own dead links at `.specify/memory/features/013.md:77-78`.

## Verdict

**BROKEN.**

The two surviving deliverables are intact and every live path they name resolves; all three spot-checked claims hold (with two historical number drifts and one file-count drift noted). What is broken is the spec's overall referenced surface: 25 distinct references (≈130 occurrences) are dead. They split into **intended** removals — the 9 draft source skills the spec itself deleted, and the stale pre-archive `.specify/specs/017-…` paths whose objects survive only in the archive — and **unintended** breaks: the entire browser-utils deliverable (source, mirror, scripts, references, examples, license) no longer exists anywhere on disk, having been removed on 2026-10-08 and recorded only as "relocated" in feature 048's registry row; `database-utils/references/README.md` was renamed to `setup-and-usage.md`; C-006's source root `skills/<name>/` no longer matches the `skills/external/<name>/` layout; and the `005-tool-skill-ids` related-spec reference no longer resolves anywhere. The consolidation ledger row is substantively accurate (Feature 013 resolves, 50/50 tasks verified), but the registry detail retains two dead pre-archive links and its `review-G2` pointer is unretrievable.

**Anomaly**: one of the spec's three headline deliverables (browser-utils) has no representation in the current tree — it was removed by commit `15b5c683b`, its only automated guards were deleted with it, and neither the consolidation ledger nor the Feature 013 detail records that removal, so the archived spec still reads as a 3-skill delivery; additionally the ledger's `054-agent-registration-wiring` row renders outside its table.

SPEC-AUDIT-4-DONE
