# Plan Stage Evidence — 104-agents-run (2026-11-24)

Stage: plan, attempt 1 + bounded completion attempt 2. Base commit `6f027b0b6`. Artifacts: `plan.md`, `research.md`, `data-model.md`, `contracts/` (3 files), `quickstart.md`, `feature-ref.md`; requirements/checklist carry the FR-020 plan-stage amendment; Feature 019 registry/detail notes updated (status unchanged). Attempt 2 did not re-plan: it completed the same-author audit, repaired the discrepancies the two audits found, recorded the E3 row and closed the stage bookkeeping.

## Gates

| # | Command | rc | Reading |
|---|---------|----|---------|
| G-1 | `flow-class-check.py --action lookup --unit-id "spec:104-agents-run"` | 0 | `flow_class: execution`, `source: declaration` (one read, reused by every judgement) |
| G-2 | `validate-requirements.py .specify/specs/104-agents-run/requirements.md` | 0 | `status: ok`, 0 error / 0 warning, 281 lines, 31 rows (24 FR + 7 SC), 8 shared strings (re-run after the FR-020 amendment) |
| G-3 | `pre-analyze-check.py --spec-dir .specify/specs/104-agents-run --stage plan --repo .` (engine at `.specify/skills/sdd-loop-driver/scripts/`) | 0 | `decision: pass`, errors 0, advisories 28 (not-yet-created test paths; `INV-*` namespace notes; the intentional "NO `.specify/templates/commands/` mirror" line), fr 24 / sc 7 / clauses 35. **Re-run after the attempt-2 corrections** (`plan-gates/pre-analyze-plan-rerun.json`): `decision: pass`, errors 0, advisories 31 — the three added advisories are exactly the citations attempt 2 added (the INV-12 namespace note at `plan.md:115` and the two future test-module paths in quickstart S-4/S-5); fr 24 / sc 7 / clauses 35 unchanged |
| G-4 | `validate-decision-tensions.py --spec .specify/specs/104-agents-run` | 0 | `status: ok`, 0 records (N/A with four trigger lines), 0 error / 0 warning |
| G-5 | `clause_extract.py .specify/specs/104-agents-run/contracts/*.contract.md` | 0 | `md-bold-closed`: command 10 (C-01…C-10), dispatch 12 (C-11…C-22), docs 13 (C-23…C-35) = 35 |
| G-6 | plan integrity: heading count / stamp / residual placeholders | — | `1` / `1` / `0` |
| G-7 | `sync-mirrors.py --check` | 0 | all six pairs ok, six projected rows ok, per-tool copies OK (baseline unchanged — no source edit in this stage) |
| G-8 | `regen-command-copies.py --check` | 0 | `OK: all per-tool command copies match the source templates.` |
| G-9 | `doc-consistency-check.py --action structure` | n/a | execution-class plan carries no Document Structure section by design (owner: plan template class condition) |

Raw outputs: `test-evidence/plan-gates/`.

## Concurrency reading

- `requested`: 24 (line deployment's agent concurrency request; owner: `shared/declarations/facts/concurrency-slot-and-reserve.yaml`)
- `effective`: 1
- `effective_reason`: `host-no-parallel` — the stage body executes as one `stage-runner.sh` fork subprocess; no external-process dispatch carrier is exposed to it, and the host-internal in-process path is not a concurrency mechanism. The two audit subagents are read-only in-process auditors, not production units.

## Same-author audit

**Condition and split**: the artifacts were authored in attempt 1 of this line, minutes before this completion; detection was delegated to two fresh-context read-only subagents with disjoint scopes — Audit A (`plan.md` + `research.md`) and Audit B (`data-model.md` + the three contracts + `quickstart.md` + `feature-ref.md`) — so the attempt-2 executor that validated and repaired them never audited its own text. Each row below carries its propagation surface first; severity is derived from that surface (blocking only where an implement-stage artifact inherits an unsatisfiable clause; mid-tier where sibling artifacts inherit; minor where the surface is the same file).

| Propagation surface | Finding | Detected by | Severity → disposition |
|---|---|---|---|
| `agents-run-command.contract.md` C-09 → implement task rows / SC-005 allowed set | C-09 required `[[STR-001]]` in the four per-tool copies, but `regen-command-copies.py` projects the template body only (frontmatter stripped; measured 0 `argument-hint` in all four copies) — a clause no implement step could satisfy without a `src/` change | B | blocking → C-09 rewritten (copy face = the body's `run <agent-name> [task]`; `[[STR-001]]` stays a source-template face) and the `plan.md` mirror row aligned |
| `research.md` B-02 → `plan.md` Summary item 1 → task framing | B-02 stated "no team-intent redirect sentence"; the template already redirects teams generally at lines 25 / 35 — the real gap is the never-serve statement | A | important → B-02 re-baselined; Summary item 1 narrowed |
| `plan.md` constraints + `data-model.md` INV-11 + docs contract C-34 + the docs test's file set | "eight named files" contradicted research B-03's enumerated seven; C-34 double-counted the command reference | A, B | important → all four aligned to the seven enumerated files |
| this evidence file — Corrections bullet | Claimed contract citations that do not exist: FR-013 / FR-021 / FR-024 live in `data-model.md`; SC-003 / SC-007 appeared nowhere in the plan artifacts | A, B | important → bullet replaced with the measured carrier map; SC-003 / SC-007 now carry a real `plan.md` carrier |
| `plan.md` §§ contract cross-references | C-25 of the docs contract cited "C-28 of the command contract"; that file holds C-01…C-10 and the grammar is C-01 | A (minor), B (blocking) | re-tiered minor → repointed to C-01 |
| docs contract C-34 baseline table | The `generate seven` and `no arguments`+`generate` rows listed the command reference; measured matches are installation + quickstart only | A | minor → baseline rows corrected (after-state 0 unchanged) |
| `plan.md` artifact tree | Comments said B-01…B-12 and S-0…S-6; research has B-13 and quickstart S-0…S-7 | A | minor → comments aligned (`plan.jsonl` is created by this completion) |
| `plan.md` Constitution row VI | Cited B-05/B-06 for the mirror/copy baseline; B-05 is the capability-count measurement, B-06 the mirror baseline | A | minor → citation corrected to B-06 |
| `data-model.md` Entity→FR map → tasks coverage mapping | FR-004 mapped to E2 while its rule sits in E1; FR-013 was attributed to E7 with no body rule | B | minor → FR-004 → E1, FR-013 → E2 with a read-only-resolution rule, E7 → FR-011 |
| `quickstart.md` S-2 pinning | Pin named C-16/C-17 for the "parent row / child row / truncation" claim, which only E8 states | B | minor → `data-model.md` E8 added |
| `quickstart.md` S-4 / S-5 pinning | No test module named; S-5's `--target` conflict claim is stated by E1, not C-03/C-08 | B | minor → module names and E1 added |
| `plan.md` structure → tasks | `test_agents_run_scope_contract.py` had no criterion anchor; SC-003 / SC-007 were cited nowhere | B | minor → module anchored to SC-005 / INV-12; both SCs cited in the Testing line |
| `feature-ref.md` delta list | "(zero modification, RS-004…RS-007)" was attached to five engines; `status-digest.py` has no RS row | B | minor → citation scoped to the four RS-backed engines; status-digest named separately |
| this evidence file — Same-author audit | Section read `TBD` | A | minor → replaced by this record |

**Reading**: Audit A produced 8 findings, Audit B 9; 3 overlapped, so 14 unique findings. Validation dismissed none and repaired all 14; 1 of 14 was re-tiered downward (the C-25 cross-reference: Audit B ranked it blocking, Audit A minor — adjudicated minor, local text fix with no downstream surface). Downgrade rate 1/14 ≈ 7%. The two blocking rows were both authoring defects a self-review would have reproduced: the C-09 copy face and the C-25 dangling id. The repaired set was re-gated once (`pre-analyze-plan-rerun.json`: pass, errors 0) rather than assumed clean.

## Corrections applied in stage

- FR-020 plan-stage amendment: the fifth enumeration face (`tests/scenarios/agents-command/single-entry-routing-scenario.md`) was added to the closed list upstream **before** editing; SC-005 parenthetical synced; requirements re-validated once (G-2).
- Clause-id namespace: the first gate run reported 22 duplicate-id errors across the three contracts (each file restarted at C-01). All three were renumbered into one namespace (command C-01…C-10, dispatch C-11…C-22, docs C-23…C-35) and every cross-reference in `plan.md` / `quickstart.md` was updated; G-3 then passed.
- `watch-model.md` references point at the real owner path `.specify/skills/sdd-loop-driver/references/watch-model.md` § 11 (the owner's bare file name does not resolve repo-relative).
- quickstart S-1's instance-path premise was rephrased so it does not cite a path that never exists in this repository.
- FR citation coverage (measured, not assumed): all 24 FRs carry a design carrier across the three contracts plus `data-model.md` — FR-013 / FR-021 / FR-024 in `data-model.md` rows, FR-022 in the command contract and data-model. SC-002 / SC-005 are carried by `data-model.md` / `research.md`; SC-003 / SC-007 are implement-stage test-execution criteria and now carry a real `plan.md` § Technical Context (Testing) citation (added in attempt 2). No clause id changed; the count stays 35.

### Attempt-2 completion corrections (from the two audits)

- C-09 rewritten: the four per-tool copies are body-only projections, so the copy face is `run <agent-name> [task]` and `[[STR-001]]` remains a source-template face (C-01). The `plan.md` mirror-obligation row was aligned.
- docs contract C-25 cross-reference repointed C-28 → C-01; C-34 rewritten to name the seven files once (no double count) and its `generate seven` / `no arguments`+`generate` baseline rows corrected to installation + quickstart.
- research B-02 re-baselined (a general team redirect exists; the missing piece is the never-serve statement); plan Summary item 1 and Constitution row VI citation (B-05/B-06 → B-06) corrected.
- "eight named files" → "seven named files" in `plan.md` (×2) and `data-model.md` INV-11; plan artifact-tree comments aligned to B-01…B-13 and S-0…S-7, and the scope test module anchored to SC-005 / INV-12.
- `data-model.md` Entity→FR map aligned to the body: FR-004 → E1; FR-013 → E2 with a read-only-resolution rule; E7 → FR-011 only.
- `quickstart.md` S-2 pin gains `data-model.md` E8; S-4 / S-5 pins gain the test-module name (S-5 also `data-model.md` E1); `feature-ref.md` scopes "(zero modification, RS-004…RS-007)" to the four RS-backed engines and names `status-digest.py` separately.
- `plan.md` § Technical Context (Testing) now cites SC-003 / SC-007, the criteria the same entry carries at implement.

## Environment anomaly

- **Fact**: `.git/config` became root-owned mode `600` at 14:03 mid-stage (all other `.git` entries remain agent-owned); every plain `git` command fails with `unable to access '.git/config': Permission denied`.
- **Policy**: `chmod` / `chown` remediation is blocked; the file was not modified.
- **Remediation**: the 103-documented read-only overlay — a temporary git-dir at `.specify/.tmp/git-overlay-104` with a copied index, a copied config (core + hooksPath + remotes), `HEAD` pointing at `refs/heads/104-agents-run`, and symlinks to the real `objects/refs/logs/info/packed-refs`; the resulting index is copied back to `.git/index`. The real `.git/config` is untouched.
- **Class**: environment anomaly, not a stage anomaly; reported to the driver.
- **Resolution (attempt 2)**: the driver restored `.git/config` ownership before this attempt; plain `git` commands work again and no overlay is used. The attempt-1 overlay directory `.specify/.tmp/git-overlay-104` is abandoned, not committed.

## Tests

Docs-only stage: no executable or test path changed in the stage diff; the targeted set (`targeted-set-v1`) is empty and no test run is applicable. The unique entry remains `scripts/bash/run-tests.sh`. The single E3 row (`test-evidence/plan.jsonl`, `row_type=stage-status`) records `status=not-run-docs-only` with the six reduced fields.
