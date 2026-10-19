# Quickstart Run — 063-review-p1-governance (2026-10-20, implement attempt 2 续跑)

Real runs of `quickstart.md` S1–S10, each with command, output tail, and exit code.
Fixtures under `/tmp` were removed after their sections were recorded (teardown noted
per section). S0's four runs are the frozen starting line recorded at plan time
(2026-10-19) and in `notes/pre-change-measurements.md` / `notes/baseline-*.txt`; they
are cited, not re-run (re-freeze semantics: the baseline files ARE the frozen record).

## S1 — Dual-width citation groups (SC-001)

```bash
mkdir -p /tmp/s63-s1/contracts && cat > /tmp/s63-s1/contracts/mixed.md <<'EOF'   # fixture per quickstart
python3 scripts/python/account-clause-coverage.py --spec /tmp/s63-s1             # rc=0, 144 files scanned
python3 - <<'EOF'  # direct dual-width extraction over the fixture corpus
```

- `clause_extract.parentheticals(corpus)` → `['FR-001', 'FR-002', 'FR-003(a)']` — the
  full-width group（FR-001）, ASCII group (FR-002), and same-width one-level nest
  (FR-003(a)) all extract as citations.
- `clause_extract.malformed_parentheticals(corpus)` → `['（FR-004)']` — the
  cross-width unpaired delimiter is reported as an independent malformed-group result,
  counted neither as citation nor as mention (C-2).
- Owner charset sentence present: `shared/definitions/contract-clause-definitions.md`
  line 51 (开组 `(` 或 `（`… 畸形组 … MUST 将其作为独立结果报告).
- Accountant run rc=0 (spec-dir `/tmp/s63-s1`; the repo-wide corpus scan counts 144
  files — the per-form census is owned by `notes/clause-form-census.md`).
- Teardown: `rm -rf /tmp/s63-s1` — done.

## S2 — Coverage lane wired into analyze (SC-002)

- Wired callers: `skills/internal/analyze-artifacts/SKILL.md:76` runs
  `python3 scripts/python/account-clause-coverage.py --spec <spec-dir>` read-only;
  `templates/commands/analyze.md` Inputs bullet declares the fixed coverage step
  (never `--freeze`); per-tool copies carry it (2/2 spot-checked).
  Path note: the quickstart's `.specify/templates/commands/analyze.md` path is the
  retired mirror location — post-056 the mirror pair excludes `templates/commands`
  (per `sync-mirrors.py` MIRROR_PAIRS note; per-tool copies come straight from
  `templates/commands/` via regen). The duty is verified on the live path.
- Freeze duty: `skills/internal/create-tasks/SKILL.md:380-382` (`--freeze` form +
  never-fabricate-empty-baseline).
- Baseline census: `find .specify/specs -name coverage-baseline.txt` → 053 + **063**
  (063's own baseline frozen at tasks time, per C-6/C-7).
- Compare mode with the baseline present: `account-clause-coverage.py --spec
  .specify/specs/063-review-p1-governance` → rc=0.
- baseline-missing lane (the F1 dark case) is exercised by the contract suite
  (`test_clause_coverage.py`, C-5/C-6/C-7 legs, green).

## S3 — Gap items consumed at first analyze (SC-003)

- Load table: `analyze-artifacts/SKILL.md:67` — `checklists/*.md` (item text, checked
  state, tags — `[Gap]` in particular); `:110` — unchecked `[Gap]` items MUST be raised
  or carry an explicit deterministic disposition; the "unchecked + unraised +
  undispositioned = 0" sentinel is asserted by the suite.
- Suite legs: `python3 -m pytest tests/contract/test_review_p1_checklist_governance.py
  tests/contract/test_review_p1_recheck_waiver.py -q` → **14 passed** (S3's Gap
  consumption + S4's recheck/waiver semantics, both pinned).

## S4 — Recheck answers replace the every-feature waiver (SC-004)

- Same suite run as S3 (14 passed): append-only recheck form, answered-items third
  branch, four-part waiver (`Scope`/`Basis`/`Disposition`/`Closed`), missing-any-part
  non-compliance, `waivers.md` at the feature spec dir.

## S5 — REC- ids persist and transitions resolve (SC-005, SC-006)

- Live surface: `grep -n "REC-" .specify/instructions.md` → line 176 (the ID-Register
  enumeration names `recommendation (`REC-…`)`; reached via `/speckit.instructions`
  content refresh per the D-T7 adjudication, commit a8c3c1f0).
- Named legal entry: `shared/workflow/feedback-step.md:83` — § A3 自省(Introspection).
- Transition row: `shared/workflow/feature-integration.md:38` —
  `| /speckit.review | Implemented → Ready for Review | review.md committed AND every
  deferred item resolved or waived |`.
- Fixture drill (compact re-run, `/tmp/s63-s5`, removed after): a seed review with
  `REC-s63-01..03` (two repo-relative targets + one external) landed register pointer
  rows **in the same commit** (`git show --stat` → `review.md` + `register.md` both in
  one commit); a clean clone resolved both repo-relative targets (`test -f` green);
  the external target stays external.
- Note (recorded fact, no live-register mutation): the live
  `.specify/memory/register.md` holds zero `REC-` rows — 062's review (read-only per
  FR-029/C-34) coined its `REC-C5`/`REC-C6` ids without registering them, and 063 does
  not retro-edit 062 artifacts. The C-12 mechanism landed by this feature is the
  *carrier* (template enumeration + register duty text at instructions line 176); the
  census of live rows is 062's debt outside this feature's scope.

## S6 — Compiled wrap-up faces execute as written (SC-007, SC-008)

Isolated worktree (`git worktree add --detach /tmp/s63-s6-worktree HEAD`), placeholders
substituted per the compiled convention line (尖括号为本轮运行时值——代入后照抄执行):

1. `run-determination.py --action determine --unit-id "/speckit.plan" --unit-type
   command --run-id s63-test-20261019T182908Z --complexity complex` → **rc=0** on
   first call (four not_evaluated quantities + trigger_feedback: false — no per-arg
   error chain).
2. `feedback-utils.py --action record --unit-id "/speckit.plan" --unit-type command
   --run-id s63-test-x --review "test" --points "No significant optimization points
   identified this run."` → **rc=0**, `duplicate: false`, entry
   `20261019T182931Z-speckit-plan.md`, `should_prompt: true` (threshold 10, count 76).
3. Duplicate re-run of step 2 → `duplicate: true`, same path, **no new entry minted**.
4. Missing-required legs → **rc=2 with ONE error listing all**:
   - run-determination (missing --run-id/--complexity):
     `error: determine is missing required arguments: --run-id (the key is (unit_id,
     run_id)); --complexity (it is a caller declaration, never an engine derivation)`
   - feedback record (missing --run-id/--review/--points):
     `error: record is missing required arguments: --run-id (the entry key is
     (unit_id, run_id)); --review / --review-file (record requires a non-empty
     review); --points / --points-file (at least one line; use 'No significant
     optimization points identified this run.' for a clean run)`
   - Quickstart-literal note: the `--unit-type y` form in quickstart S6 trips
     argparse's own choices validation (invalid choice 'y') before the business check
     — the one-shot all-listing behavior is demonstrated with a legal unit-type and
     the two genuinely missing flags (output above). Recorded as a quickstart text
     imprecision, not an engine defect.
5. `run-determination.py … --run-id s63-test-20261019T182908Z --complexity complex
   --json` (repeat of the step-1 key) → `"duplicate": true`, `"run_id":
   "s63-test-20261019T182908Z"` echoed back unchanged — the engine never mints or
   replaces a run-id (C-24).
6. `probe-utils.py --action compile-embeds --check` → `ok: True units: 74 drift: 0`.
7. Backlog row: `.specify/memory/feedback/backlog.md` line 89 reads `closed(063
   C-20..C-25 落位 …)` — flipped in commit cf8c882e, the same commit as the recompile
   evidence (`git show --stat cf8c882e` carries backlog.md + the registry row).
8. Teardown: `git worktree remove --force /tmp/s63-s6-worktree`; the worktree's
   disposable feedback/session records died with it (isolated-workspace form, per the
   quickstart's own note).

## S7 — Environment-premise carriers closed (SC-009)

Drill executed in the US6 section (fixture `/tmp/sdd-review-p1/s7-drill`, removed):
D-T1 (no date/pointer) FLAG; D-T2 (date-only) FLAG; D-T3 (pointer-only) FLAG; D-T4
(both) PASS — both together, neither alone. Renumbering leg: bare gate id silently
resolves to the wrong gate after renumbering (invisible mismatch); the verbatim quote
fails visibly. Details in `verification.md` § US6.

## S8 — Pass claims bind to archived evidence (SC-010)

The S8 fixture shape (four `pass` samples — matching/missing/empty/mismatch — plus a
`fail` sample and the no-section form) runs as the C-28 drill legs of
`tests/contract/test_evidence_binding_contract.py` → **19 passed**. Details in
`verification.md` § US4.

## S9 — Baseline pre-flight re-reads frozen values (SC-011)

Drill executed in the US5 section (fixture git repo `/tmp/sdd-review-p1/s9-drill`,
removed): values re-captured (widget 5→2 differs, coverage matches); write-back into
citing rows; classification BEFORE verdict via `git log` (inherited — post-freeze
upstream commit 3ab9c77); missing baseline = first capture with provenance (citing row
T001, freeze commit c659adb), never zero drift. Details in `verification.md` § US5.

## S10 — Global regression & invariants (SC-012, SC-013, SC-014)

```bash
bash scripts/bash/run-tests.sh --names-out /tmp/s63-after.txt          # 21 failed / 4089 passed, rc=1
comm -13 notes/baseline-failed-tests.txt /tmp/s63-after.txt            # empty — 0 NEW
python3 scripts/python/sync-mirrors.py --check                         # 3 DIFF (pre-existing agents drift), 0 NEW vs T001 baseline
git diff --stat -- .specify/specs/062-humanize-command/                # empty
grep -rn "gate-implement-evidence-binding" shared/definitions/probe-definitions.md   # Object row + HandlerBinding row
rm -f /tmp/s63-after.txt                                               # cleanup
```

- Zero NEW failing names vs the frozen 63-name baseline (21 pre-existing failures
  remain — not this feature's repair surface; the baseline is untouched).
- Mirror drift: 3 DIFF, all in `.specify/agents/templates` — inside the T001 baseline
  set, untouched prefix; touched pairs byte-identical.
- 062's governed artifacts: zero diff.
- Gate row registered (Object row line 119 + HandlerBinding row line 233).
- C-18 verbal check: the quickstart's "bare gate id fails the C-18 rule" expectation is
  honored — this feature's red-first notes record commands/outputs/exit codes and
  never cite a bare gate id (the shape rule's owner text forbids it; the S7 renumbering
  drill demonstrated why).

## C-03 — S6 reconcile-flag decision (carried finding)

`--reconcile` runs as part of C-25's closure (T044): `probes --validate --reconcile`
→ `{"ok": true, "reconciled": true, "classes": 10, "objects": 116, "embeds": 74}`.
Decision: the reconcile flag is used at the Polish recompile boundary (where the
registry and faces reach their final state), not per-phase — matching its
rows↔embeds purpose. The run also exposed and closed the pre-existing
`skill:sdd-project-setup` registration gap (disclosed in `verification.md` §
Polish/T044).
