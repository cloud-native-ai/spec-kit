# Analyze Round-1 Report — 111-general-best-practices

**Stage**: analyze (round 1) · **Baseline**: `5af1c1290` · **Run**: `r20261127T071500Z-111a` · **Worker**: SDD Analysis Worker (read-only analysis seat) · **Date**: 2026-11-27
**Spec**: `.specify/specs/111-general-best-practices/` · **Quartet**: `flow_class=execution; source=declaration; marker=; error=-`
**Findings file**: [`test-evidence/analyze-round1-findings.jsonl`](./analyze-round1-findings.jsonl) (12 records, schema-validated)
**Concurrency**: requested=1 · effective=1 · reason=single-unit

## 0. Verdict summary

- **12 findings**: **CRITICAL 1 · HIGH 2 · MEDIUM 3 · LOW 6**.
- No format-level defect: `validate-requirements.py` → 0 error / 0 warning (220 lines, 16 definition rows, 7 shared strings); `validate-tasks.py` → 0 error / 0 warning; every FR (9/9) is cited by ≥1 contract; 24/24 contract clauses are claimed exactly once; 24 real `[green:]` tags resolve to defined clauses.
- The artifact set is coherent on its primary spine (closed five-document set, FR↔SC↔tasks↔contracts coverage, containment, registry deferral, mirror/packaging premises). The substantive weaknesses cluster in three places: **(a) the accumulation mechanism's executable form and rule ownership** (AR1-01, AR1-02), **(b) guard-vs-task ordering around the mirror path** (AR1-03), and **(c) registration/containment verifiability edges** (AR1-04…AR1-06).
- **One CRITICAL** under the constitution-conflict rule: the plan's Constitution Check row XIV (One Source of Truth) claims a pass that the accumulation artifacts do not support.

## 1. Method and read domain

- Full read of the assigned domain: `requirements.md`, `checklists/requirements.md`, `checklists/general-best-practices-2026-11-27.md`, `plan.md`, `data-model.md`, `quickstart.md`, `feature-ref.md`, `tasks.md`, `contracts/` ×4 (24 clauses).
- Authority outside the domain read for precedence only: `.specify/constitution.md` (v1.20.0, 23 principles), `.specify/instructions.md`, `.specify/features.md` + `.specify/features/`, and the source delivery (`ai-harness/shared/best-practices/` five documents, `ai-harness/.ah/specs/087-general-best-practices/` inventory, source `knowledge-promotion.md`, source `.ah/instructions.md`, source `.ah/shared/definitions/framework-map.md`).
- `research.md` was **not read** (outside the assigned read domain); it was verified to exist and is referenced by plan/tasks only.
- All engine probes were read-only (`--help`, `args-manifest`, `--check`, `grep`, `git diff`, validators). No product write, no spine/registry edit, no push.
- **Anomaly line for this analysis run**: `未发现异常` (no in-passing repair was needed; no state contradicted a recorded expectation of the analysis assignment itself).

## 2. Mechanical readings (all re-measured today)

| Reading | Command | Result |
|---|---|---|
| FR / SC / STR / A / US / Edge / RS | greps on `requirements.md` | **9 / 7 / 7 / 21 / 3 / 11 / 3** — matches checklist footer and plan input |
| Contract clauses | `grep -cE '^\*\*C-[0-9]{3}\*\*'` per file | **6 + 5 + 6 + 7 = 24** — matches plan/checklist |
| Tasks rows / EP / scenarios / CHK | greps | **19 / 5 / 9 / 40** — matches all footers |
| Requirements validator | `validate-requirements.py` | `status ok`, **0 error / 0 warning**, 220 lines, 16 definition rows, 7 shared strings |
| Tasks validator | `validate-tasks.py` | **PASS**, 0 error / 0 warning |
| Clause coverage | `account-clause-coverage.py` | claimed clauses (this feature) **24**; baseline file absent (created at T002, expected) |
| FR→contract citations | per-FR grep | **9/9** FRs cited by ≥1 contract; SC-007 is the only SC with no contract citation (process criterion, expected) |
| Green partition | `[green:]` tags | 24 real tags, 24 unique, each clause defined once; 25th regex hit is the format placeholder `[green: <contract>#<clause>]` |
| Shared Strings refs | `[[STR-00N]]` counts | STR-001…STR-007 all resolve; 15–23 references each |
| Mirror baseline | `sync-mirrors.py --check` | `ok shared/ == .specify/shared/ (117 files, byte-identical)`, rc 0 |
| Map mirror | `cmp` | `.specify/shared/definitions/framework-map.md` byte-identical to source |
| Containment | `git diff --name-only 0419adae5..HEAD` | **72 paths**, all inside FR-009's declared set (residual set empty) |
| Target absence | `ls` | `shared/best-practices/`, `.specify/shared/best-practices/`, `tests/contract/test_general_best_practices.py` all absent → red-first premise valid |
| Test stack | `/usr/local/bin/python3 -c 'import pytest…'`; `python3 -c 'import pytest'` | 8.4.2 / 3.11.11; PATH `python3` has no pytest (SPECKIT_PYTHON override needed, as stated) |
| Packaging | `pyproject.toml:51` | `"shared" = "specify_cli/shared"` in wheel `force-include` → a new `shared/` subdirectory ships with **zero** packaging change |
| Engine premises | `feedback-utils.py`, `sync-mirrors.py`, `src/specify_cli/__init__.py` | `record` action exists; pair `("shared", ".specify/shared", False, set())` at L99; shared wholesale copy at ~L2743-2757 |
| Mirror adjudicator | `tests/contract/test_mirror_parity_suite.py` | derives parameters from `MIRROR_PAIRS` (L51-66) — sole byte-identity adjudicator claim holds |
| Source module inventory | `wc -l` + residue grep | 5 docs / 61 lines; README:3 `ai-harness`, README:33 `.ah/`, README:5 `Feature 040`; `/ah.` = 0 |
| Source wiring absence | grep `best-practices` in source `.ah/instructions.md` + `.ah/shared/definitions/framework-map.md` | **0 hits each** — A-6's source premise verified |
| Registry deferral | `features.md` rows, `features/` listing | no 109/110/111 row, no `.specify/features/111-*`; max registered id 108 |
| Glossary | grep | no `best-practice` / `最佳实践` hit; FR-009 set excludes glossary (A-21) |
| Instructions pointer | `.specify/instructions.md:300-304` | Framework Map section is a pointer to `framework-map.md`; zero `best-practices` hits — A-6 holds |
| Drill root / runner | `.specify/.gitignore:30`; `scripts/bash/run-tests.sh` | `.tmp/` ignored; `--names-out` / `--full` supported |
| Contract marker | `pyproject.toml:57-58` | `contract` marker registered |

## 3. Coverage results

- **FR ↔ tasks**: Requirement Coverage Map covers 9/9 FRs and 7/7 SCs with concrete task rows (spot-verified against task bodies).
- **FR ↔ contracts**: 9/9 FRs cited; contract clause partition (manifest 6 / entry-shape 5 / accumulation 6 / distribution-guard 7) is claimed exactly once by green tags on T008/T010/T013/T015/T019.
- **SC ↔ evidence**: SC-001…SC-006 each name a machine reading (guard legs, `--check`, `git diff`); SC-007 is process-shaped (runner exit code, red-first capture, name-set comparison) and is owned by T017/T018 plus the `/speckit.implement` Test-runs owner — no contract citation is expected for it.
- **User stories**: US1→SC-001/SC-002, US2→SC-003, US3→SC-004/SC-005; SC-006/SC-007 are cross-cutting (Polish). Each story keeps an independently testable checkpoint.
- **Five-document closed set**: consistent across FR-001, A-15, C-101, E1, DoD-2, GATE-5 (5 docs; mirror count 117+5=122 stated in tasks/quickstart, still 117 today as expected pre-implementation).
- **Checklist coverage**: the dated checklist reports FR 9/9, SC 7/7, clauses 24/24, 40/40 trace anchors; the twelve open observation points it names are adjudicated below (two become non-findings, ten become findings).

## 4. Constitution check (verification of the plan's gate)

- 23 principle rows in `plan.md` match constitution v1.20.0 (I–XXIII) in order; no missing or invented principle.
- **No direct MUST conflict** found in Principles I–XIII, XV–XXIII against the delivered design artifacts.
- **Principle XIV (One Source of Truth) — plan's pass is unsupported → CRITICAL (AR1-02)**: the accumulation rule is attributed to an owner that does not define it, and one contract clause (C-305) forbids what another contract clause and a task (C-302, T009) mandate the manifest to state. This is the sole CRITICAL.

## 5. Findings

| ID | Severity | Category | One-line claim |
|---|---|---|---|
| AR1-01 | HIGH | underspecification | Observation form requires a `notes` field the feedback engine does not have; ad-hoc unit/run-id convention missing. |
| AR1-02 | CRITICAL | constitution-conflict | Promotion rule ownership is inconsistent; plan Constitution Check XIV pass unsupported (C-305 vs C-302/T009; cited owner lacks the rule). |
| AR1-03 | HIGH | consistency | Guard prelude (C-404) requires the mirror path, but US1/US2 green runs (T008/T010) precede mirror regeneration (T012) — checkpoints impossible as ordered. |
| AR1-04 | MEDIUM | consistency | Manifest must point at a spec-local contract path that `specify init` never distributes → guaranteed downstream dangling pointer. |
| AR1-05 | MEDIUM | consistency | Second-mechanism detection is phrased five ways; C-304 (exact names) and C-404(d) (wildcard) disagree inside one contract face. |
| AR1-06 | MEDIUM | ambiguity | Containment residual predicate (A-20 sentence / GATE-7 / T019) omits the per-entry qualifier C-406 has; an aggregate append could pass as written. |
| AR1-07 | LOW | coverage | Map-row adjacency and two Notes elements (A-19/C-403) have no verification surface although the six guard legs are declared exhaustive. |
| AR1-08 | LOW | ambiguity | Seed `**来源**`: "exempt" (A-17/C-204) vs "must be absent" (T007/S-3) vs "no fabricated line" (T004 leg c) — three readings. |
| AR1-09 | LOW | consistency | A-15 says module-wide sole table; FR-001/C-103/INV-03/T004 check the manifest only. |
| AR1-10 | LOW | duplication | Six guard-pinned literals (`**实践**`, `**反例 / 证据**`, `**延伸**`, `**来源**`, `积累机制`, `封闭集`) are replicated but not in Shared Strings. |
| AR1-11 | LOW | ambiguity | "同一变更" has no referent (commit / landed change / branch) for the closed-set trio and related MUSTs. |
| AR1-12 | LOW | underspecification | Init-drill CLI form unspecified at requirement layer; resolved in tasks (source-run mandated) without conflict. |

### Detail

**AR1-01 (HIGH, underspecification) — the observation form is not executable against the engine.**
FR-004 / A-17 / C-301 / T009 say the observation's `notes` carry `[best-practice]` + the owner-file stem. The engine's contract says otherwise: `feedback-utils.py --action args-manifest` lists `record` required args as `--unit-id --run-id --review --points` with an empty source set; `action_record` never reads `args.notes`; `compose_entry` writes `frontmatter + ## Review + ## Optimization Points`; the glob verbatim `--notes` is parser-declared (L2945) and therefore **silently accepted and dropped** for `record`. Second leg: `record` demands a valid `--unit-id` (`/speckit.<command>` | `skill:<name>` | `custom:<owner>/<name>` with `--unit-type custom-unit`) and a `--run-id`, but the spec gives no convention for an observation that is not a command/skill run. The accumulation entry point must name the real carrier (review/points text) and the ad-hoc identity convention, or the module will ship a mechanism that cannot be followed.

**AR1-02 (CRITICAL, constitution-conflict) — promotion rule ownership.**
`knowledge-promotion.md` declares ownership of the recording obligation and the 2+ user-emphasis escalation; it defines no feedback→category-owner-file promotion and its threshold (2+) is not the spec's criterion (recurrence or one explicit user correction). Yet C-302 says promotion "follows" that file, and C-305 forbids the manifest to restate "the promotion threshold" while C-104(c)/C-302/T009 require the manifest to declare exactly that criterion. Either the module restates a rule it does not own (contradicting FR-004's pointer-only sentence and C-305) or the pointer reaches an owner that does not define the rule (contradicting Principle XIV's declared-owner discipline). The source module carries the same pointer, so this is an inherited premise that A-4 verified only by path existence, not by content fit. **This is the finding the driver should treat as the gate.**

**AR1-03 (HIGH, consistency) — guard vs task order.**
C-404/T004: one shared module-read prelude asserts "the existence of every repository path the module cites — at minimum … `.specify/shared/best-practices/` …". The ported manifest cites that mirror path (source README:33, adapted per FR-008). T008 and T010 run legs sharing that prelude and are claimed green; the mirror directory is created only at T012 (blocked by T011, itself blocked by T010). Result: US1 and US2 green checkpoints are unattainable as ordered, and T008's recorded "cited-path readings" cannot be green. Resolution is a decision: reorder mirror regeneration ahead of T008/T010 (creates interim stale-mirror states), or scope the prelude's minimum set to source-side paths and let leg (e) at T015 own the mirror path.

**AR1-04 (MEDIUM, consistency) — downstream dangling pointer.**
C-104(b)/T005 mandate the manifest to point at `.specify/specs/111-general-best-practices/contracts/entry-shape.contract.md`. `specify init` distributes `shared/` wholesale (verified at `src/specify_cli/__init__.py:2743-2757`) and ships no specs, so every client project receives a README with a dead pointer. FR-008's existence check is a target-repo check and cannot see this. The source README declares the entry shape inline and cites no spec path; the pointer is target-added. Options: declare the shape inline (source form) and keep the spec contract as the build-time owner, or accept and disclose the coupling.

**AR1-05 (MEDIUM, consistency) — five detection surfaces for one check.**
FR-007(d) "named best-practices", SC-003 exact `best-practices.py`/`best_practices.py`, C-304 same exact names, C-404(d) `best-practices*.py` wildcard, T004/T010/feature-ref wildcard, quickstart S-4 exact names. `best-practices-utils.py` is red under C-404 and green under C-304. One expression should own the check (e.g. a glob covering both `best-practices`/`best_practices` spellings) and all other sites should cite it.

**AR1-06 (MEDIUM, ambiguity) — containment predicate vs aggregate ban.**
A-20's predicate sentence and its per-entry/aggregate prohibition are two clauses in one item; GATE-7 and T019 restate only the predicate. An append to `.specify/exec-quant/records.jsonl` (present, 176,571 B) carrying the feature key would pass the restated procedure while C-406/A-20 forbid it. SC-006 is a final-path criterion, so the wording must name the per-entry-only domain (or explicitly list aggregates/indexes as always violating).

**AR1-07…AR1-12 (LOW)** — as tabulated: unverified registration-row MUSTs; seed source-line reading; A-15's module-wide vs manifest-only table scope; six unregistered guard literals; "同一变更" referent; init-drill CLI form (already closed in tasks § Environment Prerequisites, no conflict).

## 6. Verified claims and non-findings

- **Registry/detail/reverse refs**: no Feature 111 row, no `.specify/features/111-*`; `feature-ref.md` discloses the deferral and FR-009 names the registration stage as the sole exception. Consistent, no edit needed.
- **Additive-docs invariant**: no `src/`, `templates/`, instructions, `.gitignore`, glossary, scripts, or decision-governance change is required; packaging ships `shared/` wholesale (`pyproject.toml:51`); distribution rides init + the existing mirror pair. Zero-code claim holds.
- **Five-document closed set**: consistent everywhere, including mirror arithmetic (117 → 122 at implementation).
- **Mirror chain**: pair at `sync-mirrors.py:99`; parity suite derives from `MIRROR_PAIRS`; write-mode regeneration + `--check` are the stated and correct mechanics.
- **Instructions pointer**: A-6 holds on both sides (target instructions/map zero hits; source `best-practices` zero hits in `.ah/instructions.md` and `.ah/shared/definitions/framework-map.md`).
- **Checklist observation CHK022** (per-module mirror reading): resolved downstream — GATE-5/DoD-6 define the pair-level 122-file reading, which implies an empty module-level diff; no verdict divergence.
- **Checklist observation CHK026** (cited-path "at minimum" set): all four minimum paths are cited by the ported module text (guard path README:16; feedback engine README:30; promotion owner README:31; mirror path README:33 post-adaptation) — the set is derivable; no finding.
- **Init integration test nuance**: `tests/integration/test_init_new_layout.py:33-57` runs init source-run and therefore executes the shared copy step, but asserts nothing about `shared/`. SC-004's wording ("runs the same copy step") is accurate; outcome evidence properly rests on C-407 evidence 3 (the recorded drill). Flagged for the review stage, not a defect.
- **SC-007 has no contract citation**: expected — process criterion owned by T017/T018 and the `/speckit.implement` Test-runs owner.
- **Environment**: interpreter/pytest, runner flags, `.tmp/` sanction, contract marker, baseline object `0419adae5` all verified present.

## 7. Containment reading (this stage's own effect)

`git diff --name-only 0419adae5..HEAD` = **72 paths**; set difference against FR-009's declared set = empty (prefix check). This stage produced exactly two evidence files under `.specify/specs/111-general-best-practices/test-evidence/**` plus its per-entry wrap-up accounting records in `.specify/{session,feedback,exec-quant}/` — all inside the declared set. No engine, template, skill, agent, command, constitution/instruction, store-layout or decision-governance path changed; no registry edit; no push.

## 8. Limits of this round

- No implementation exists (module, mirror, guard all absent), so every guard-leg finding is design-level: legs were not executed, and "red-first" remains a plan premise.
- `research.md` was outside the assigned read domain and was not read; claims that depend only on it (M1–M11, R-1–R-10 internals) were not independently re-derived beyond the measurements listed in §2.
- `pre-analyze-check.py` exposes stages `requirements|plan|tasks` only; there is no `--stage analyze`, so no pre-analyze gate exists for this stage (not an anomaly). Cross-artifact checks were performed directly and mechanically.
- Engine probes were interface-level (`--help`, `args-manifest`, `--check`); no product behavior was exercised.

## 9. Disposition routing (recommendation only — the driver owns the verdict)

1. **Before implement** (blocking-class): AR1-02 (rule ownership + XIV gate), AR1-01 (observation form), AR1-03 (prelude/order).
2. **Repair-in-stage candidates** (local, reversible, no new intent): AR1-05, AR1-06, AR1-09, AR1-10, AR1-11 — wording/ownership alignment.
3. **Decision-class** (needs a recorded choice): AR1-04 (inline shape vs spec pointer), AR1-07 (add checks vs downgrade to producer guidance), AR1-08 (seed source-line reading).
4. **No action required**: AR1-12 (closed in tasks), plus all §6 non-findings.

## 10. Wrap-up pointers

- Findings: `test-evidence/analyze-round1-findings.jsonl` (12 records; validated).
- This report: `test-evidence/analyze-round1-report.md`.
- Accounting (per-entry, existing engines): `run-determination --action determine` (session), `exec-quant --action collect`, `feedback-utils --action record` for `/speckit.analyze`, feature key `111-general-best-practices`.

**Anomaly line**: `未发现异常`.