# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- `create-pages`: **Hugo Book theme** (`alex-shpak/hugo-book`, pinned `v0.14.0`) as the
  preferred renderer, vendored offline under `docs/themes/book` via
  `scaffold-hugo.py --action theme --fetch`; the built-in layouts remain the fallback.
- `create-pages`: **navigation completion** for the docs directory — sidebar reading order,
  section labels, collapse for crowded sections, and a section landing page for every
  directory without an `index.md`, all derived from the live tree via a Hugo cascade and
  mounts (no documentation is written).
- `/speckit.docs` command: documentation-space reconcile engine (six-type taxonomy, uppercase special-name registry, notes lifecycle, docs-utils engine). See ADR-0001.
- Docs-sync evaluation step (`## Documentation`) on all 14 complex commands.

### Changed

- `create-pages`: built-in layouts no longer use `.Site.Language.Locale` (Hugo ≥ 0.158 only),
  which broke every page on older Hugo; `.Site.Language.Lang` is used instead.
- `docs/` reorganized to the six-type taxonomy (tutorials / concepts / reference / decisions / contribute / tasks + notes, archive).
