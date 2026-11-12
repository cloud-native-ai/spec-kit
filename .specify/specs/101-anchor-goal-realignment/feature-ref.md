# Feature Reference — 101 Anchor / Goal Realignment

A navigation sheet for the plan set: **where each requirement is decided, where each criterion is
measured, and which rulings were taken to close a gap**. It owns no rule; every row points at an owner.

## 1. Binding and neighbours

| Fact | Value |
|------|-------|
| Feature | **101** — a new feature, not an increment of 041 |
| Spec | `.specify/specs/101-anchor-goal-realignment/` |
| Requirement count | 71 FR / 10 SC / 8 STR (unchanged by this stage) |
| Predecessors | **041** (Goal Registry — concept and command surface inverted here); **094** (directory rename `.specify/goal/` → `.specify/anchoring/`, command surface not renamed); **090** (Re-Anchoring — runtime discipline kept, terminology only disambiguated) |
| Protected baseline | commit `d7c9da7a3` (all dated records) |
| Plan baseline reading | HEAD `d3f85f059`, engine `0.0.22` — see `test-evidence/plan-baseline-2026-11-12.txt` |

041 keeps its `Implemented` status and its dated records; the only 041-side change is a successor note
pointing here. 094's directory rename is completed here, not reversed.

## 2. Delivery surface (what implement must produce)

| Surface | Canonical source | Generated copies |
|---------|------------------|------------------|
| Anchor command | `templates/commands/anchor.md` | `.specify/templates/` mirror is **retired** for commands; four per-tool copies via `regen-command-copies.py` |
| Goal command (rewritten) | `templates/commands/goal.md` | same four copies |
| Anchor skill | `skills/internal/manage-anchor/` | `.specify/skills/` mirror |
| Goal skill (rewritten) | `skills/internal/manage-goal/` | `.specify/skills/` mirror |
| Definitions | `shared/definitions/anchor-definitions.md` (new), `shared/definitions/goal-definitions.md` (rewritten) | `.specify/shared/definitions/` mirror |
| Engine | `scripts/python/goal-utils.py` | `.specify/scripts/python/goal-utils.py` mirror |
| Reference pages | `docs/reference/commands/anchor.md` (new), `docs/reference/commands/goal.md` (rewritten) | — (docs are not mirrored) |
| Ledger + probe | `shared/definitions/flow-class-definitions.md`, `shared/definitions/probe-definitions.md` | mirrors + compiled wrap-up faces |

The four per-tool copy directories are the only ones (`research.md` R-10): a fifth directory would be a
new surface and needs a plan revision.

## 3. Requirement → contract map

| FR range | Subject | Decided in |
|----------|---------|-----------|
| FR-001…FR-009 | Concept ownership, naming, identity, shared binding/lifecycle, term disambiguation | `plan.md` § Phase 1 Design; `data-model.md` E-1…E-6 |
| FR-010…FR-018 | `/speckit.anchor`: seven modes, sole authoring entry, skill delegation, mirror delivery, probe, live-surface pointers | `contracts/anchor-command.contract.md` C-1…C-12 |
| FR-019…FR-027 | `/speckit.goal`: four modes, named rejection, write boundary, no Anchor resolution, GD-2 exemption, docs page, command family | `contracts/goal-command.contract.md` C-13…C-22 |
| FR-028…FR-034 | Engine: single writer, layer-resolved filenames, four-member `--scope`, `auto`, action groups, existing actions, `-h`/`--version` | `contracts/goal-engine.contract.md` C-23…C-35 |
| FR-035…FR-049 | Classification, migration, archival, receipts, digest, resumability, conflict, team dispositions, binding rename, orphan summary | `contracts/migration-cleanup.contract.md` C-36…C-49; `classification.json`; `data-model.md` E-7…E-11 |
| FR-050…FR-060 | Live-surface convergence (framework-map, glossary, routing, re-anchoring, flow-class, probe, setup/house-keeping, docs, team domain, patterns, non-disposable) | `plan.md` § Decomposition WP-03/WP-04; `research.md` R-09 |
| FR-061…FR-071 | Guards: dated-record protection, contract tests per surface, convergence tests, evidence | `plan.md` § Testing Strategy; `quickstart.md` S-7/S-8 |

## 4. Success criterion → measurement

| SC | Sensor | Reading (plan-time) | Artifact |
|----|--------|--------------------|----------|
| SC-001 | `tests/contract/test_live_semantic_residue.py` over the roots declared in `research.md` §5 | C1 4 · C2 0 · C3 7 · C4 15 · total 26 | `test-evidence/live-semantic-scan-baseline-2026-11-12.txt` |
| SC-002 | Template `argument-hint` parse + subprocess refusal probes | both templates today carry the old surface (expected) | contract tests C-1/C-14 |
| SC-003 | `classification.json` + `cleanup --check` enumeration | 9 anchor / 3 action-goal / 2 obsolete across 14 entries | `classification.json`; `research.md` §3 |
| SC-004 | Receipts + digest equality + protected-path hashes | no receipts exist yet (nothing migrated) | `test-evidence/plan-baseline-*` (pre) |
| SC-005 | `team.md` frontmatter scan + `run-checks` per team | 16 bound / 4 unbound; 2 dangling (`viz-skill-arena`, `demo-seat-dispatch`) | `classification.json` `teams`; `research.md` §4 |
| SC-006 | Static write-surface audit + two-writer fixture | engine is sole writer today | `contracts/goal-engine.contract.md` C-31 |
| SC-007 | Two applies + one interruption injection on a fixture | n/a before implement | `contracts/migration-cleanup.contract.md` C-41/C-42 |
| SC-008 | File existence, `flow-class-check.py`, probe compile, docs build | flow-class clean (89 units); **docs build fails** (Hugo exit 1, EP-006) | `test-evidence/plan-baseline-*`; EP-006 |
| SC-009 | `git hash-object` set vs `d7c9da7a3` | protected roots equal at plan entry | `test-evidence/plan-baseline-*` |
| SC-010 | Reader restatement record | not evaluated at plan time | `research.md` §7 |

SC-008's docs-build limb is measured **false at plan time** for a pre-existing reason unrelated to this
feature (`.Site.Language.Locale`); it reports `not-evaluated` rather than a fabricated pass — see EP-006.

## 5. Rulings taken at this stage (disclosed, not silent)

| ID | Ruling | Where |
|----|--------|-------|
| R-01 | Classification is **decided at plan**; `classification.json` is a plan artifact read verbatim by implement | `research.md` §6 |
| R-02 | One layer-parameterized engine, never a second binary | T-001 |
| R-03 | `.specify/goals/` is plural; no singular alias | `data-model.md` E-11 |
| R-04 | No alias for the retired `--scope goal` member or for retired modes | T-004 / C-24 |
| R-05 | Team `forbidden` lists gain no new `.specify/goals/**` entry; the sole-writer invariant is the control | C-46 |
| R-06 | `summary/**` is a derived tree written by the summary flow, outside the definition-writer invariant | PLAN-EDIT 1–3 |
| R-07 | Migrated Targets are preserved under one fixed heading `## Migrated Targets` **and** in the receipt | C-38 |
| R-08 | Owner rewrite happens in two commits (history-preserving move, then rewrite) | FR-006 |
| R-09 | Ledger and probe are **regenerated**, never hand-edited | FR-054 / FR-055 |
| R-10 | Only four per-tool command-copy directories are in scope | §2 |
| R-11 | The Hugo premise is falsified at plan time → docs-build limb measures `not-evaluated` | EP-006 |
| R-12 | Protected-path equality is per-file `git hash-object` against `d7c9da7a3` | C-49 / S-7 |
| R-13 | Six inherited-blocker rows are declared, five `not-applicable` | `plan.md` § Inherited Blockers |
| R-14 | Archived teams lose the binding line; provenance moves to `disposition-receipt.json` | C-47 |
| R-15 | `list` is not given a team-reading surface: `--scope teams list` exits 2 `scope-not-applicable`, and today's `list` ignoring `--scope` is recorded as measured rather than "fixed" | `contracts/goal-engine.contract.md` C-27 |
| R-16 | The `.specify/archive/**` equality assertion covers **baseline-existing entries**; the new `.specify/archive/anchoring/**` subtree is an addition evidenced by receipts | PLAN-EDIT 4; C-49; G-8 |

**Plan-stage corrections to requirements (declared, four):** (1–3) FR-011 / FR-028 / SC-006 scope the
single-writer invariant to **definition files** and name `summary/**` as a derived exception — forced by a
pre-existing writer (`build-summary-input.py`) that no requirement had accounted for; (4) FR-061 / SC-009
scope the `.specify/archive/**` byte-equality to **baseline-existing entries**, because FR-041 mandates
creating the new `.specify/archive/anchoring/**` subtree in the same change. Requirements were re-validated
after each (`0 error / 0 warning`).

**Not evaluated at plan time** (reported, never assumed): SC-010 reader restatement; SC-007 idempotency
(the mechanism does not exist yet); SC-004 receipts.

## 6. Decomposition pointer

Work packages, write territories, the fence and the ceiling readings are owned by `plan.md`
§ Decomposition & Ceiling. Package order is WP-01 (definitions/engine) → WP-02 (command surface) →
WP-03 (live surfaces) → WP-04 (cleanup/migration) → WP-05 (guards/evidence) → WP-06 (registry/docs).
