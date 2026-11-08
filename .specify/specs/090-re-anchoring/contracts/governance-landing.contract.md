# Contract — Governance Landing

**Feature**: 090-re-anchoring | **Date**: 2026-11-09 | **Plan**: [plan.md](../plan.md)

How a principle reaches every surface that must carry it, and how the counting pins stay honest.
`FR-002`, `FR-009`, `FR-010`; `SC-003`.

**C-1** — Both constitution surfaces, one title, no forced numeral alignment

The template and the live constitution MUST carry the same principle title. Their numerals MAY differ and MUST NOT be
"repaired" to match: the live roster carries project-specific principles the template does not, so the same rule
naturally lands on different ordinals. A change that forces the numerals equal is a defect against this contract.

(FR-002)

**C-2** — The Sync Impact Report names the amendment

The live constitution's Sync Impact Report block MUST name the principle this amendment added, its version change and
`Last Amended` date. The report is the human-readable trace that the landing was deliberate.

**C-3** — The generator's mandate list grows with the principle

`skills/internal/manage-constitution/SKILL.md`'s `- **MUST include**` block MUST gain exactly one sub-entry per new
principle, and the sub-entry count pin (`COMMAND_COUNT`) MUST move in the same landing.

(FR-009)

**C-4** — The count pins move in the same batch

`tests/contract/test_constitution_double_landing.py` MUST carry `TEMPLATE_COUNT`, `LIVE_COUNT` and `COMMAND_COUNT`
consistent with the artifacts they describe, and `DOUBLE_LANDING_WATCHLIST` MUST gain the new title. The pin values are
**derived** by `test_fast_fail_discipline.py::test_x13` from the artifacts themselves, so "same batch" is recomputable
rather than asserted by a literal alone.

(FR-010)

**C-5** — The watchlist length is pinned by the fast-fail guard

`tests/contract/test_fast_fail_discipline.py::test_x15` MUST pin the watchlist length at its new value and MUST assert
that the newest entry is a template title — an append that does not reach the surface it guards is the failure this
pin exists for.

**C-6** — No historical record is rewritten

The incident that motivates the discipline is cited in the owner page and in the checkpoint protocol; neither may
rewrite a dated record, a commit message or a past checkpoint. History is a citation target, not an edit target.
