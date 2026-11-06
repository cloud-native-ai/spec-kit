# Analyze Report — Round 2 (087-arch-diagram-docs)

- Object: `.specify/specs/087-arch-diagram-docs/` @ `7b6b6cc6` (the round-1 repair commit)
- Mode: strictly read-only cross-artifact re-check — no artifact was modified by this round
- Verdict: **pass for the release criterion** — **0 CRITICAL / 0 HIGH / 4 MEDIUM / 7 LOW**
- Release criterion (CRITICAL and HIGH zero, or each closed with evidence): **holds**

## Round-1 findings — closed

| id | severity | disposition | evidence |
|----|----------|-------------|----------|
| F-01 contract clause → test/`green` binding misaligned | HIGH | **closed** — table A/B rebuilt by the clause's own subject; 39/39 machine-decidable clause ids each claimed exactly once (`C-008a` carries no machine-decodable claim, see the escalation row below); the 7 previously-unclaimed ids (diagram `C-014`, flow `C-007`, `C-008`, `C-008a`, `C-009`, `C-021`, `C-022`, `C-023`) now have named assertions | `analyze-repair-round1.md` § HIGH — closed |
| F-02 "`docs/` zero change" vs FR-001's reader projection | HIGH | **closed** — the constraint narrowed to "except `docs/concepts/documentation-model.md`" in `tasks.md` GATE-6, `tasks.md` T073/S8 and `quickstart.md` S8; `plan.md` and `requirements.md` still carried the old wording at this commit — see M2 below | `analyze-repair-round1.md` § HIGH — closed |

## Round-2 regression readings (all pass)

- 19/19 constitution gates re-read against the repaired artifact set — no new violation
- `EP-001` (Execution Premises) and the Inherited Blockers table unchanged and still disposed
- Feature 087 still `Planned` in both `.specify/memory/features.md` and `.specify/memory/features/087.md`
- Mirror Obligations rows unchanged; the `.specify/skills/<name>` paths and the four per-tool copies are the ones on disk
- No out-of-territory write: every path the repair touched is inside the spec directory

## MEDIUM (4) — carried into the implement stage, each with a named owner

- **M1** — `plan.md` § Test Plan tables A/B and the `tasks.md` assertion pointers drifted: diagram `C-009`/`C-015`
  have no named assertion in `tasks.md`, flow `C-022`'s slot is occupied by `FR-021`'s subject. `plan.md` is the
  single registry; `tasks.md` must point at it rather than re-list it.
- **M2** — the F-02 narrowing never reached `requirements.md` § Out of Scope, `plan.md` (three sites) or
  `feature-ref.md`. The requirements change is a **re-baseline event**, not a plan edit; it is returned to the
  driver rather than taken by a repair round.
- **M3** — the `C-01` fixture invariant was rewritten only in `data-model.md` E6; `plan.md:493`, `tasks.md:22/77`
  and `quickstart.md` still read the old "pre-deletion green state", which makes DoD-4 literally unsatisfiable.
- **M4** — the plan's "2 new test files" budget contradicts the 4 files `tasks.md` creates; plan table A cites the
  reuse file for `C-014`.

## LOW (7) — all closed by the round-1 repair or registered here

| id | finding | state |
|----|---------|-------|
| L1 | `feature-ref.md` lists `.specify/templates/commands/docs.md` as a generated copy that no longer exists | **carried** — the retired path is still listed; the real copies are the four per-tool ones |
| L2 | `feature-ref.md` / `plan.md:84` still call `OI-087-01` open while the register records it resolved | **carried** — the two sites were not rewritten |
| L3 | `data-model.md:46` attributes the closed five-value set *and* the ordered precedence to `C-004` | **carried** — `C-016` is the only owner of the order |
| L4 | `quickstart.md` selects `C-008a`'s assertion with `-k reconcile` over the **unit** file | closed — the assertion lives in the integration file and the selector names it |
| L5 | `quickstart.md` and `diagram-obligation.contract.md:322` cite `plan.md` sections that do not exist | **carried** — two dangling `plan.md § …` pointers |
| L6 | the repair evidence recorded `pre-analyze` advisories as 84; round 2 measures 77 | closed — the round-2 reading below is the measured one |
| L7 | `C-012`'s "each of the four is driven by its own fixture" overstates the eleven-space composition | **carried** — the sentence reads wider than E6 supports |

## Gate readings (verbatim, this round)

1. `python3 .specify/scripts/python/validate-tasks.py .specify/specs/087-arch-diagram-docs/tasks.md`
   → `PASS: … 0 error(s), 0 warning(s)` / **exit 0**
2. `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks …`
   → `{"mode": "tasks", "decision": "proceed", "measured": {"fr_count": 23, "task_count": 76, "fr_ceiling": 60, "task_ceiling": 80}, "reasons": []}` / **exit 0**
3. `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir … --stage tasks --repo .`
   → `stage=tasks decision=pass errors=0 advisories=77 waived=0` / **exit 0**
4. `python3 .specify/scripts/python/validate-decision-tensions.py --spec .specify/specs/087-arch-diagram-docs`
   → `scanned: 577 lines, 5 record(s)` / `0 error(s), 0 warning(s)` / **exit 0**
5. `python3 .specify/scripts/python/validate-requirements.py .specify/specs/087-arch-diagram-docs/requirements.md`
   → `scanned: 314 lines, 33 definition rows` / `0 error(s), 0 warning(s)` / **exit 0**
6. `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/087-arch-diagram-docs`
   → `[clause-uncovered] pass (573) — 573 uncovered, 0 beyond the frozen baseline`
   → `[fr-uncovered] fail (7) — 16 of 23 FRs cited from citation groups` / **exit 1** — the pre-existing
   citation-group gap recorded in round 1, unchanged and deliberately not greened

## Evidence

- Round-1 findings and their closures: `test-evidence/analyze-report-round1.md`, `test-evidence/analyze-repair-round1.md`
- This file is the round-2 pointer the stage-status row names.
