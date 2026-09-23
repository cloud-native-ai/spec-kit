# Specification Quality Checklist: 快速失败纪律——异常分流而非静默兜底(Fast Fail)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-22
**Feature**: [requirements.md](../requirements.md) · Feature 052 · Status `Draft`
**Validation runs**: 3 — (1) initial draft, (2) after the 2026-09-22 scope addendum (subagent dispatch injection), (3) after `/speckit.clarify` Mode A integrated four user rulings and ~30 detector corrections. **Run 3 is operative.**

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification
- [x] Related Feature resolved — **Feature 052 / 快速失败纪律(Fast Fail) / `Draft`**; registry obligations discharged (index row added, `features/052.md` created, reverse cross-reference written into `features/051.md`, `Total Features` 51 → 52)

## Notes

- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
- **All items pass.** The `Related Feature` row that runs 1–2 carried as "PENDING by design" is resolved by run 3, so no unchecked row remains and the house rule at `.specify/shared/guidelines/requirements-guidelines.md:47` is not triggered.

### Validation evidence (run 3 — 2026-09-22, machine-re-derived, not transcribed)

| Check | Result |
|---|---|
| Functional requirements | 78 (`FR-001`–`FR-078`); **0 gaps, 0 duplicates, 0 letter-suffixed IDs, 0 dangling `FR-nnn` references** |
| Success criteria + sources | 15 + 15 (`SC-001`–`SC-015`, each with a Source row); **0 dangling `SC-nnn` references** |
| Shared Strings | 13 rows / 13 cited — **0 unresolved, 0 defined-but-uncited** |
| User stories (P1 / P2) | 6 (4 / 2); priority order monotonic `P1 P1 P1 P1 P2 P2` |
| Acceptance scenarios | 30 |
| Edge cases | 17 |
| Key-entity rows | 19 (2 rows each cover a pair, so the entity count exceeds the row count) |
| Out of Scope / Assumptions entries | 11 / 12 |
| `[NEEDS CLARIFICATION]` markers · template placeholders | **0 · 0** |
| Mandatory sections | 4 / 4 |
| `## Clarifications` entry rows | 8 across 2 sessions — **strictly greater than the pre-integration baseline of 5**, so the append-only invariant holds (no Edit replaced history) |

Run 2 counted 62 FR / 14 SC / 10 STR / 6 stories / 28 acceptance / 17 edge cases / 13 entities; run 1 counted 46 / 10 / 8 / 5 / 22 / 11 / 9. Every delta is itemised in the `## Clarifications` session entries.

### Two self-detected defects found by re-deriving rather than transcribing

Both were caught by counting the artifact after editing it, not by reading it — the exact discipline this feature specifies:

1. **Three Shared Strings were defined but never cited** (`STR-011`/`STR-012`/`STR-013`). A pinned literal with no consumer is dead weight and would have shipped as an unassertable contract row. Now wired into FR-016, FR-017, FR-054 and FR-067; the check now runs in **both** directions (unresolved *and* uncited).
2. **An entity count was asserted as 20 in two artifacts while the file held 19.** Corrected in both this spec's Clarifications log and `features/052.md`. A count written from memory rather than re-derived is the failure mode `SC-002` exists to make visible.

### Judgement notes on the two "implementation details" items

Both pass **with a recorded reason**, not silently:

1. This feature's deliverable **is** a set of governance artifacts — a truth-source document, an ambient instructions section, two closed lists, a constitution principle, a dispatch-time injection clause, a contract-test guard. Naming those by path is naming the *subject matter*, the way a data-migration spec names its tables. No language, framework or API is chosen anywhere; the "how" left to `/speckit.plan` includes the doc's internal section wording, the exact list phrasing, the injection clause's literal text and delimiters, the guard's assertion bodies, and the constitution principle's bullet text.
2. `SC-002`–`SC-007` and `SC-010`–`SC-012` are measured against repo structure because the outcome *is* structural. `SC-001`, `SC-008`, `SC-009`, `SC-013`(subagent side) and `SC-015` are reader/behaviour outcomes. House precedent for this split: features 040 and 051.

### Risks and open items carried into `/speckit.plan`

Resolved by user ruling this run: the fast-fail halt is **not** a confirmation gate (FR-028); injection is a **caller-side content obligation**, not wrapper behaviour (FR-058); the pre-dispatch missing-clause case splits **by discovery time** (FR-053); channel 2 binds the **authoring requirement**, not an enumerated file list (FR-050/FR-061); the lists grow **bidirectionally** with an over-triggering measure (FR-044/SC-015).

Still open, and deliberately not decided here:

1. **Injection clause size ceiling.** FR-048 requires the clause to be self-sufficient for the classification decision, which pulls against token efficiency on high-fan-out dispatches. The threshold is deliberately left to the truth-source doc as its single definition point — `/speckit.plan` must write actual clause text and therefore has to fix a figure.
2. **Channel 3's landing point.** Sixth field in the Per-Agent Payload table vs. folded into `task_brief`'s content rule. FR-050 leaves it to `/speckit.plan` but requires that the guard be able to discriminate it.
3. **SC-018-style cross-discipline edit.** FR-024 makes the fast-fail truth-source doc a *partial* rule source for surface class ⑪. Whether that requires a row edit in `user-facing-comprehension.md`'s class-mapping table must be settled in planning, and if it does, it must be listed as an explicit cross-discipline change rather than happening silently.
4. **Four upstream defects found but deliberately not fixed here** (each outside this feature's blast radius; fixing them mid-clarify would itself violate FR-073's radius rule): `feature-integration.md`'s status contradiction and its dead `memory/feature-index.md` pointer; the false "refresh instructions restores the mirror copy" wording pattern that other ambient sections also carry; the `反空转哨兵` / `反空真哨兵` canonical-vs-source word-form mismatch; and `agent-definitions.md:50`'s "seven shipped role agents" (measured: 2). All four are recorded in `features/052.md` › Future Evolution Suggestions.
