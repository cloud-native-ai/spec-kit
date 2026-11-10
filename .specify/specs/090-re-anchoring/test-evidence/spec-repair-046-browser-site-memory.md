# Spec repair — 046-browser-site-memory

**Date**: 2026-11-10
**Tree**: `/storage/project/cloud-native-ai/spec-kit` (branch `master`), MAIN tree, no worktree
**Mode**: reference repair only. Writes: the two spec artifacts listed under § Live-fixed, plus this file.
No commit, no push, no subagents.
**Spec location**: archived — `.specify/archive/specs/046-browser-site-memory/` (14 artifacts; the
audit wrote "13" but its own enumeration and `find -type f` both yield 14 — 8 root `.md`, 3 contracts,
1 checklist, 2 failed-test lists).
No live copy exists at `.specify/specs/046-browser-site-memory/`.

## Inputs read

1. `.specify/specs/090-re-anchoring/test-evidence/spec-audit-046-browser-site-memory.md` — the
   per-spec audit (20 dead entries, 9 alive, 7 archived-elsewhere).
2. `.specify/specs/090-re-anchoring/test-evidence/spec-audit-settled.json` — entry
   `.specify/archive/specs/046-browser-site-memory`, `kind=archived`, `refs=34`, `dead=20`, and its
   `dead_list` of 20 strings.
3. All spec artifacts (whole-file reads): `requirements.md`, `plan.md`, `tasks.md`, `research.md`,
   `data-model.md`, `quickstart.md`, `verification.md`, `feature-ref.md`, `contracts/*` ×3,
   `checklists/requirements.md`, `baseline-failed.txt` + `current-failed.txt` (failed-test lists, no
   path references).

## Counting rule

Distinct repository path strings as written, deduplicated at the string level, with two folds:
a bare skill-relative filename folds into the same object as its `skills/browser-utils/…`-qualified
form, and `$SKILL_HOME/scripts/site-memory.py` folds to `scripts/site-memory.py`.
Runtime data files and templated placeholders are reported separately as **non-reference** and are
**not** part of the dead total (they are caller-project data this spec never ships).

Stack **re-measured** against the current tree, not inherited from the audit: the audit was taken
before the anchor-layout merge `6fb8093c2` landed, and the settled scan classified the three
`.specify/memory/…` anchors as `moved`. All three are dead **now**.

## Counts

| Bucket | From settled `dead_list` | Re-measured additions | Total |
|---|---|---|---|
| **live-fixed** | 0 | **5** | **5** |
| **dated-kept** | **20** | 5 | **25** |
| **Dead total** | 20 | 10 | **30** |
| non-reference (outside the dead total) | — | — | 10 |

Validator / resolver reading after the repair: **0** of the 25 dated-kept strings has a live target
anywhere in the tree; **0** dead anchor-layout or spec self-location strings remain.

## Live-fixed (5 strings, 6 line edits, 2 files)

Every one of these named an object that still exists under a different path. Each new target was
verified to exist before writing; no target was invented.

| # | Dead string | Locations | Before → After | Target evidence |
|---|---|---|---|---|
| 1 | `.specify/memory/constitution.md` | `plan.md:27` | `.specify/memory/constitution.md` → `.specify/constitution.md` | File exists; it is the project constitution (Sync Impact Report, v1.19.0). Anchor layout moved memory-root anchors to `.specify/` root in `6fb8093c2`. Cited by the plan as the source its Constitution Check was "rendered from" — a normative owner doc, not a past reading. |
| 2 | `.specify/memory/features/048.md` | `tasks.md:109` | `.specify/memory/features/048.md` → `.specify/features/048-derive-command.md` | File exists; its header is `# Feature Detail: Browser Utils Skill` / `**Feature ID**: 048`, and registry row 57 (`features.md`) declares that same path in its **Feature Details** column. The filename is a renumbering collision — the *content* is the Feature 048 object the task names. |
| 3 | `.specify/specs/046-browser-site-memory/requirements.md` | `plan.md:5` | `.specify/specs/046-browser-site-memory/requirements.md` → `.specify/archive/specs/046-browser-site-memory/requirements.md` | File exists at the archive path; spec archived in `c5b17a9fc`. Self-location pointer, not a dated reading. |
| 4 | `.specify/specs/046-browser-site-memory/` | `plan.md:66` | `.specify/specs/046-browser-site-memory/` → `.specify/archive/specs/046-browser-site-memory/` | Directory exists at the archive path. Heading of the spec's own `### Documentation (this spec)` tree. |
| 5 | `.specify/specs/046-browser-site-memory/baseline-failed.txt` | `tasks.md:23`, `tasks.md:31` | `.specify/specs/046-browser-site-memory/baseline-failed.txt` → `.specify/archive/specs/046-browser-site-memory/baseline-failed.txt` | File exists at the archive path (4441 B, in-tree). Named by Completion Gate **GATE-1** and task **T001** as the baseline set-difference input. |

Surrounding validators were re-run for the two edited files — see § Validator readings.

## Dated-kept (25 strings)

These record the artifact set **as it existed at implementation time** (2026-08-24). The named
objects were deleted from `master` in two later commits, and **no live successor exists in this
repository** for any of them:

- `80a8c1fb0` "remove three skills" (2026-09-22) — deleted `browser-utils` (and `browser-extension`,
  `clone-website-ui`). Content survives only at revision `80a8c1fb0^`. The capability was relocated
  to a different project (`xuanji-extension`, per registry row 57 status `Relocated`).
- `15b5c683b` "remove browser-utils skill" (2026-10-08) — deleted both contract tests and the two
  `.gitignore` site lines.

Repointing any of these at the archive would be false (the skill content is not in the archive), and
repointing at a git revision is not a path. They are left byte-identical.

### 20 strings from the settled `dead_list`

| # | Dead string | Representative locations | Why no live target |
|---|---|---|---|
| 1 | `skills/browser-utils/scripts/js/run.js` | `research.md:31` | Playwright runner deleted with the skill (`80a8c1fb0`). |
| 2 | `skills/browser-utils/` | `plan.md:38`, `plan.md:81` | Skill source root deleted; relocated out of this repo. |
| 3 | `skills/browser-utils/references/request-level-patterns.md` | `tasks.md:72` (also `plan.md:9`, `tasks.md:66` as `references/…`, `feature-ref.md:14,22`) | Reference file deleted with the skill. |
| 4 | `skills/browser-utils/scripts/site-memory.py` | `contracts/site-memory-engine.md:8` (also `plan.md:9`, `tasks.md:55,56`, `feature-ref.md:21`, `research.md:26`) | 555-line engine deleted (`80a8c1fb0`). |
| 5 | `.specify/skills/browser-utils/site/probe.json` | `contracts/framework-exclusions.md:15` | X-2 verification probe path; skill mirror deleted. |
| 6 | `tests/contract/test_browser_site_exclusions.py` | `plan.md:89`, `tasks.md:37,41` | Contract test deleted (`15b5c683b`); grep over `tests/` finds no replacement. |
| 7 | `scripts/site-memory.py` | `contracts/site-memory-engine.md:8`, `quickstart.md:13,20,35,36,47` | `$SKILL_HOME/scripts/site-memory.py` form; same deleted engine. |
| 8 | `skills/browser-utils/site/probe.json` | `contracts/framework-exclusions.md:15` | X-4 probe path; same deleted skill tree. |
| 9 | `tests/contract/test_browser_site_memory.py` | 14 locations (`plan.md:16`, `tasks.md:51,56,66,83,98`, `quickstart.md:5`, all three contracts) | Contract test deleted (`15b5c683b`). |
| 10 | `.specify/skills/browser-utils` | `quickstart.md:5` (`$SKILL_HOME` value) | Mirror directory deleted. |
| 11 | `.specify/skills/browser-utils/` | `plan.md:82`, `plan.md:98` | Mirror directory deleted. |
| 12 | `.specify/skills/browser-utils/site/` | `requirements.md:157`, `plan.md:83`, `tasks.md:37,38`, `contracts/framework-exclusions.md:13` | Mirror-side site/data dir; skill gone, nothing creates it. |
| 13 | `skills/browser-utils/scripts/` | `research.md:17` | Skill scripts dir deleted. |
| 14 | `scripts/bridge/` | `research.md:9`, `research.md:32` | Bridge lived at `skills/browser-utils/scripts/bridge/`; no top-level `scripts/bridge` exists now or in history. |
| 15 | `skills/browser-utils/site/` | 11 locations incl. `requirements.md:102`, `plan.md:15,83`, `contracts/framework-exclusions.md:12,20,28`, `tasks.md:38` | Runtime memory dir of the deleted skill. |
| 16 | `scripts/bridge` | `plan.md:42` | Same as #14, slash-less form. |
| 17 | `.specify/skills/browser-utils/scripts/site-memory.py` | `contracts/site-memory-engine.md:8` | Mirror copy of the deleted engine. |
| 18 | `skills/browser-utils/site/secret.json` | `research.md:15` | R2 hatchling experiment fixture under the deleted tree. |
| 19 | `skills/browser-utils/references/site-memory.md` | `tasks.md:71` (also `plan.md:9`, `tasks.md:66`, `contracts/site-memory-formats.md:4`, `feature-ref.md:14,22`) | Reference file deleted with the skill. |
| 20 | `skills/browser-utils/SKILL.md` | `contracts/framework-exclusions.md:28`, `plan.md:98`, `tasks.md:70,73` | Skill definition deleted (`80a8c1fb0`); the wheel-path form `specify_cli/skills/browser-utils/SKILL.md` is the same object. |

### 5 re-measured dated-kept strings

Missed by the settled scan's token regex or by the audit's grouping; re-measured in this pass and
given the same disposition.

| # | Dead string | Locations | Note |
|---|---|---|---|
| 21 | `skills/browser-utils` (slash-less) | `requirements.md:6` | Prose mention in the **Input** quote: "全面优化skills/browser-utils技能". Same deleted skill. |
| 22 | `references/playwright-patterns.md` | `research.md:33` | Deleted with the skill. |
| 23 | `mcp-browser-tools.md` | `research.md:33` | Deleted with the skill. |
| 24 | `extension-bridge-patterns.md` | `research.md:33` | Deleted with the skill. |
| 25 | `scripts/js/package.json` | `research.md:31` | Runner manifest under the deleted skill tree. |

## Non-reference (10, outside the dead total)

Examples / placeholders / caller-project runtime data. Nothing to repair; named for completeness.

| # | Token | Location | Kind |
|---|---|---|---|
| 1 | `skills/browser-utils/site/<host:port>/` | `plan.md:15` | Templated runtime memory dir placeholder |
| 2 | `../site/g.aliyun-inc.com` | `contracts/site-memory-engine.md:18` | Ellipsis form inside a JSON **output sample** |
| 3 | `state.json` | `data-model.md:13`, `contracts/site-memory-engine.md:17,22` | Runtime data file (per-site) |
| 4 | `records/<task-slug>.jsonl` | `data-model.md:14`, `contracts/site-memory-engine.md:28` | Runtime data, templated |
| 5 | `records/query-baseline.jsonl` | `quickstart.md:25,31` | Runtime data from the walkthrough |
| 6 | `site/g.aliyun-inc.com/records/query-baseline.jsonl` | `quickstart.md:25` | Runtime data from the walkthrough |
| 7 | `recipe.json` | `data-model.md:15`, `contracts/site-memory-engine.md:37` | Runtime data (per-site) |
| 8 | `validation/<run-id>.json` | `data-model.md:16`, `contracts/site-memory-engine.md:42` | Runtime data, templated |
| 9 | `notes.md` | `data-model.md:17` | Optional free-text runtime file |
| 10 | `$SKILL_HOME` / `${SKILL_HOME}` | `quickstart.md:5,13,20,35,36,47`; `contracts/site-memory-engine.md:8` | Shell variable placeholder; the path it *expands to* is dated-kept #7/#10/#11 |

Alive tokens deliberately left untouched: `.gitignore`, `pyproject.toml`, `src/hatch_build.py`,
`scripts/python/sync-mirrors.py`, `.specify/scripts/python/sync-mirrors.py`,
`.specify/skills/improve-skills/scripts/skill-shape.py`, `./requirements.md`, `../requirements.md`,
and the bare directory tokens `.specify/scripts/`, `.specify/skills`, `scripts/js`, `scripts/python/`,
`tests/contract/`.

Two **content-level** (not path-level) claims inside this spec are also dated and left as written —
they are true readings of the tree at implementation time, false today, and re-adding them would be
wrong because their subject no longer exists:
`.gitignore` X-1/X-2 (the two `…/browser-utils/site/` ignore lines, removed in `15b5c683b`) and the
`MIRROR_PAIRS` tuple `("skills", ".specify/skills", …)` (relabelled to two `skills/external` /
`skills/internal` pairs in `scripts/python/sync-mirrors.py:95-96`; the `site` exclusion semantics
survive on the successors). Recorded here rather than edited.

## Validator readings

| Validator | Target | Result |
|---|---|---|
| `validate-tasks.py` | `tasks.md` (edited) | **PASS — 0 error(s), 0 warning(s)**, exit 0 |
| `validate-requirements.py` | `requirements.md` (not edited) | **status: error — 5 error(s), 5 warning(s)**, exit 1 |

`validate-requirements.py` detail: all 10 lines are `[ref-resolvable]` on the **Shared Strings**
block — `STR-001…STR-005` are defined but never cited as `[[STR-NNN]]`, and each `Consumed by` cell
names an FR row (`FR-005` ×4, `FR-003` ×1) that re-types the literal instead of citing the id. The
other five checks pass (`id-contiguous`, `doc-order`, `marker-count`, `dup-id`, `path-marker`).
Per-check header: `[ref-resolvable] fail (10)`, everything else `pass`.

This is a **pre-existing** content defect in a Draft-era archived artifact, not a reference failure
and not introduced by this repair: `requirements.md` is unmodified in the working tree
(`git status` shows only `plan.md` and `tasks.md` modified). Fixing it would rewrite dated normative
content — out of this repair's scope. Reported, not repaired.

## Out-of-scope findings (reported, not touched)

Files outside this spec's directory, or registry edits barred because the spec is **archived** (the
registry-row exception applies to live specs only):

1. **Registry row 57** (`.specify/features.md`): the **Spec Path** cell still reads
   `.specify/specs/046-browser-site-memory/requirements.md` — dead since the archive move. The
   **Feature Details** cell (`.specify/features/048-derive-command.md`) is correct and was used as
   the evidence for live-fixed #2.
2. **`src/hatch_build.py:15,21`** — docstring contracts still point at
   `specs/046-browser-site-memory/research.md` and
   `.specify/specs/046-browser-site-memory/contracts/framework-exclusions.md` (audit entry F/20).
   Both now resolve only under `.specify/archive/specs/…`.
3. **Feature 048 detail file name collision** — the detail file for Feature 048 (Browser Utils) is
   named `.specify/features/048-derive-command.md`; that name belongs to Feature 049's subject
   ("Derivation Command"), while the file's content is Browser Utils. Separately, its line 42 contains
   a corrupted self-reference `.specify/.specify/features/048-derive-command.md` (doubled prefix).
4. **`048.md` status divergence** — the detail file still says `**Status**: Implemented` while
   registry row 57 says `Relocated` (audit ledger-check).
5. **Ledger** — `.specify/archive/specs/CONSOLIDATION-LEDGER.md:15` carries `review-G4`, a string with
   no in-tree record; and the ledger-wide structural defect (the `054` row sits outside its Markdown
   table) is unchanged.
6. **Missing guards** (audit § Missing guards 1–6) — both contract tests, the `.gitignore` closure, and
   `site`-drop coverage for `_stage_skills` / `sync-mirrors` remain absent. This repair restores no
   guard; it only makes surviving pointers resolve.

## Anomaly

**No anomaly.** No repair anomaly: every repaired target was verified to exist, no target was
invented, no dated reading or dated content was rewritten, and no file outside the spec directory was
modified. One in-passing correction, disclosed rather than repaired silently: the audit's artifact
count reads "13" while its own enumeration and `find -type f` both yield 14; the measured value (14)
is used here.

Out-of-scope finding 3 is worth a separate flag: Feature 048's detail file carries another feature's
filename *and* a corrupted double-prefixed self-reference, so the anchor that live-fixed #2 points at
is itself defective — repairing it further is a different task.

SPEC-REPAIR-12-DONE
