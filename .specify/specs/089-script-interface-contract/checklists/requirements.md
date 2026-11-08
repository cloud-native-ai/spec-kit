# Specification Quality Checklist: 脚本接口契约（Script Interface Contract）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-06
**Feature**: [`../requirements.md`](../requirements.md)
**Deterministic checker**: `validate-requirements.py` → `status: ok`, 0 error / 0 warning
(380 lines, 43 definition rows, 0 shared strings). All counts below derive from that run;
none is hand-typed.

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — the contract is stated as
      externally observable behaviour (`-h`/`--help`, `--version`, exit codes, zero side
      effects, unknown-option rejection). The two runtime-stack rows name bash and Python
      only because they are the *runtime the feature stands on*, which the
      acceptance-hardening schema requires to be named.
- [x] Focused on user value and business needs — the driver is the concrete incident: a
      read-only intent (`--help`) executed a write action. Every P1 story traces to it.
- [x] Written for non-technical stakeholders — § Overview states the incident and the three
      failure layers in prose before any requirement id appears.
- [x] All mandatory sections completed — Related Feature, User Scenarios & Testing,
      Requirements (FR + Key Entities + Runtime Stack), Success Criteria (+ Measurement
      Sources), Assumptions; `**Flow Class**: execution` / `**Flow Type**: -` declared.

## Requirement Completeness

- [x] No `[NEEDS CLARIFICATION]` markers remain — checker `marker-count` = 0. The two
      genuinely undetermined points (version-identifier granularity, gate wiring) are
      resolved as labelled Assumptions (A4, A7) rather than as markers, because a reasonable
      default exists and the choice does not change scope.
- [x] Requirements are testable and unambiguous — every FR names an observable (a flag, an
      exit code, a byte-level diff, a counted violation), never an internal structure.
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta
      set — FR-018 / SC-007 (existing option semantics, JSON output and exit codes unchanged)
      are containment claims: the baseline referent is the pre-change behaviour of each
      named existing invocation, and the allowed delta is the set of *new* flag paths. The
      measurement is a before/after output diff with an empty difference list, so the
      allowed-delta set is re-derivable rather than hand-listed. Owner consulted:
      `.specify/shared/guidelines/closed-set-claims.md`.
- [x] Success criteria are measurable — each SC names a count, a byte comparison, an exit
      code, or a percentage; SC-003's threshold is "violations = 0" with the candidate set
      produced by the checker, not a hand-typed list.
- [x] Success criteria are technology-agnostic — no framework, library or API choice appears
      in any SC; "`argparse` is acceptable but not required" is stated in FR-017 / US5 as an
      acceptance note, and the judgement is external behaviour.
- [x] All acceptance scenarios are defined — 7 stories, 22 given/when/then scenarios,
      covering help, version, unknown options, distribution, backfill, exemption and gate
      wiring.
- [x] Edge cases are identified — 10 edge cases, including the incident-relevant
      "help requested together with a write flag", the `-h` collision case (measured: zero
      occurrences in this repo, kept as a rule-text boundary only), thin wrapper scripts,
      third-party scripts that must not be rewritten upstream, and an unclassifiable
      upstream source.
- [x] Scope is clearly bounded — § Out of Scope names seven exclusions, including the Typer
      CLI, pure-library files, per-script version files and retroactive record rewrites.
- [x] Dependencies and assumptions identified — 10 assumptions (A1–A10) including the
      flow-class rationale required by the command template, plus 5 runtime-stack rows with
      premises.

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria — FR-001…FR-031 map onto
      stories: FR-001/011–016 → US4 + SC-004/005/006; FR-002/009/024–026 → US6 + SC-003 /
      SC-009 / SC-010; FR-003–008/029 → US1–US3 + SC-001/002; FR-010/021/031 → US7 + SC-008;
      FR-017/018/019/027/030 → US5 + SC-001/007; FR-020 → US5 edge case + FR-010 visibility;
      FR-022 → SC-006; FR-023 → § Out of Scope; FR-028 is a tombstone (merged into FR-027)
      and maps to nothing.
- [x] User scenarios cover primary flows — the incident flow (US1), its real root cause
      (US3), the identity question (US2), the distribution requirement the user added
      explicitly (US4), and the "rule must not stay text-only" flow (US5).
- [x] Feature meets measurable outcomes defined in Success Criteria — 12 SC, of which 10 are
      `final` and 2 `supporting`; an `execution` line satisfies the `final` floor.
- [x] No `[NEEDS CLARIFICATION]` marker survives, and no decision the four clarify rounds
      fixed is still deferred: the owner-document path (A3), the version form (A4), the
      checker's 落点 and naming (A7 → FR-031) and the third-party judgement (A6 → FR-027) are
      now decided in the spec body, not left to plan.

## Notes

- **This checklist was refreshed by the clarify stage (2026-11-06).** Every derived count
  above was re-measured from the spec after the FR/SC additions, never carried forward:
  23 → 31 FR (one of them, FR-028, a tombstone), 8 → 12 SC, 9 → 10 edge cases, 9 → 10
  assumptions, 21 → 22 acceptance scenarios. Superseded literals to grep for (MUST return
  nothing): `FR 23`, `SC 8`, `9 edge cases`, `A1–A9` — those four strings are now cited
  only inside this note, by design.

- The incident claim was re-measured rather than inherited. Two task-brief premises did not
  survive measurement and are corrected in § Assumptions A2 with the commands and readings:
  (a) `refresh-tools.sh` *does* have a `--help` branch (6 of 14 bash scripts lack help, not
  the brief's list of 7); (b) no git commit exists that adds 11 sections / +70 lines to
  `.specify/instructions.md`, so SC-002 is written as a self-contained reproducible
  experiment instead of a comparison against the incident diff. Both are disclosed, not
  silently repaired.
- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`.
- The checklist validates requirement quality, not implementation behaviour; the deterministic
  checker's verdicts outrank any hand reading recorded here.
- **Companion record**: the specification-quality items that the requirement text cannot answer —
  the contract's decision logic, the design-side clause graph and the stale-count premises — are
  audited in [`contract-integrity-2026-11-06.md`](./contract-integrity-2026-11-06.md). A finding
  there that names a requirement is repaired in `requirements.md` first and this checklist's
  derived counts are then re-taken from the checker run, never carried forward.
- **Derived counts re-taken 2026-11-06** (after the analyze round-1 repair of `requirements.md`,
  commit `5c2bb98f`): the checker now scans **380** lines (it read 376 before that repair added the
  FR-030 two-class reading, the A4 exit-0 wording and the Q3/Q6 corrections), and
  `skills/external/*/` together carry **73** `.sh` / `.py` files (previous reading 72).
