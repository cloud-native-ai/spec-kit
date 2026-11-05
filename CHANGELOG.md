# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- **Feature 083 (meta-skill governance: mechanism/policy separation + skill-reference
  normalization)**: two framework owners — `shared/definitions/mechanism-policy-definitions.md`
  (boundary test, misplacement symptoms, archival rules, consumption contract, meta-layer
  membership) and `shared/definitions/skill-reference-definitions.md` (accepted forms,
  normalization order, disambiguation rules, failure semantics) — plus one mechanism/policy
  judgement line and one skill-reference line in each of the five meta-skill consumers
  (`create-skills`, `improve-skills`, `merge-skills`, `coaching-skills`, `run-skills`). Pinned by
  eleven contract modules under `tests/contract/`
  (`test_mechanism_policy_{owner_doc,skill_wiring,guard,ownership,decidability,missing_policy}.py`
  and `test_skill_reference_{grammar,matrix,consumers,command_surface,failures}.py`) and the
  normalization matrix fixture `tests/fixtures/skill-reference/normalization-matrix.json`.
- **Feature 081 (acceptance hardening)**: deterministic acceptance gates for feature-status
  transitions. New `closure-acceptance-check` engine (`scripts/python/closure-acceptance-check.py`)
  — four completion conditions judged by one program, `accept`/`block` only, a seven-literal
  closed reason set, and a read-only `--audit-existing` mode (zero writes under the audited root,
  one report line per affected feature). Declarative fixture sets under
  `tests/fixtures/acceptance-hardening/` and the contract suites that pin them: the three gate
  call sites (implement / review / driver closure-merge), the review composition (four fixed
  segments plus the Acceptance Reality Check), the line-state machine (the `blocked` value and its
  eight dispositions), the acceptance schema owner (`shared/workflow/acceptance-hardening.md`) and
  its schema-ownership guard.
- `create-pages`: **Hugo Book theme** (`alex-shpak/hugo-book`, pinned `v0.14.0`) as the
  preferred renderer, vendored offline under `docs/themes/book` via
  `scaffold-hugo.py --action theme --fetch`; the built-in layouts remain the fallback.
- `create-pages`: **navigation completion** for the docs directory — sidebar reading order,
  section labels, collapse for crowded sections, and a section landing page for every
  directory without an `index.md`, all derived from the live tree via a Hugo cascade and
  mounts (no documentation is written).
- `create-pages`: **local builds run in the CI image** — `--action build` uses docker with the
  image the pipeline uses (`--runner auto|docker|local`, `--hugo-image`, `SPECKIT_HUGO_IMAGE`),
  resolved from the rendered pipeline or the shared `ci-templates/hugo-image.txt` that stage 3
  renders from; the workstation Hugo is a reported fallback. New `--action image` prints the
  resolved image and its source.
- `/speckit.docs` command: documentation-space reconcile engine (six-type taxonomy, uppercase special-name registry, notes lifecycle, docs-utils engine). See ADR-0001.
- Docs-sync evaluation step (`## Documentation`) on all 14 complex commands.

### Changed

- **Feature 081 (acceptance hardening)**: the three status-transition call sites now run the
  closure checker — `/speckit.implement` before `Planned → Implemented` (a `block` lands
  `Blocked`, never `Implemented`), `/speckit.review` before `Implemented → Ready for Review`
  (four segments in one fixed order plus the Acceptance Reality Check; a `block` refuses the
  transition with a named condition), and the `sdd-loop-driver`'s closure/merge step, where
  `integrate-lines.py` defaults its quality gate to the checker through the existing
  `--gate-cmd` hook (`block` records `closure-blocked` then lands the line `blocked`; input
  errors record `closure-input-error` and leave the state unchanged). `line-registry.py` admits
  `blocked` as a first-class line state. The vocabulary owners (`templates/feature-details-template.md`,
  `templates/feature-index-template.md`, `skills/internal/manage-features/SKILL.md`) and the
  schema owner align on `Blocked`, with the narrow `Implemented → Blocked` audit-correction
  exception; the four `blocked` literals are reconciled once in
  `shared/workflow/acceptance-hardening.md` § Verification Vocabulary.
- `create-pages`: built-in layouts no longer use `.Site.Language.Locale` (Hugo ≥ 0.158 only),
  which broke every page on older Hugo; `.Site.Language.Lang` is used instead.
- `docs/` reorganized to the six-type taxonomy (tutorials / concepts / reference / decisions / contribute / tasks + notes, archive).
