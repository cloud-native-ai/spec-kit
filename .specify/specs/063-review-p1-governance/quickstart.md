# Quickstart: Verification Recipes（063-review-p1-governance）

**Spec**: `.specify/specs/063-review-p1-governance/requirements.md` | **Feature**: 063
**Purpose**: the executable recipe `/speckit.implement` runs to verify each mechanism fix. Every command below is either (a) already executed during plan with real output pasted, or (b) an implement-stage step whose premises are declared per example. Nothing here is pre-written as a verdict — expected results are re-measured at run time.

## S0 — Current-state evidence (executed at plan, 2026-10-19)

```bash
bash scripts/bash/run-tests.sh --names-out .specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt
# → 63 failed, 3954 passed (0:02:43); 63-name sorted list written (baseline frozen BEFORE any change)
python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/062-humanize-command
# → status: baseline-missing; 512 error(s); [fr-uncovered] fail (16) — 13 of 29 FRs cited (the F1 dark lane, live)
find .specify/specs -name coverage-baseline.txt
# → only .specify/specs/053-machine-decidable-artifacts/coverage-baseline.txt
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check
# → compile-embeds --check: 74 units, zero drift (clean pre-change state)
```

These four runs are this feature's frozen starting line: SC-013 judges against the 63-name list; SC-002's `find` starts from exactly one baseline; C-25's recompile starts from zero drift.

## S1 — Dual-width citation groups yield one total (SC-001; premises: C-1, C-2 landed)

```bash
mkdir -p /tmp/s63-s1/contracts && cat > /tmp/s63-s1/contracts/mixed.md <<'EOF'
**C-1** 引用全角组（FR-001）与半角组 (FR-002) 同语料。嵌套组 (FR-003(a))。
**C-2** 畸形组（FR-004) 跨宽度不配对。
EOF
python3 scripts/python/account-clause-coverage.py --spec /tmp/s63-s1
python3 scripts/python/clause_extract.py --help   # or the module's self-test entry used by tests
grep -n "（\|(" shared/definitions/contract-clause-definitions.md | sed -n '/引用组/p'
```

Expected (asserted by tests/contract at implement, not pre-written here): the accountant's total for the ASCII-only corpus is identical to the dual-width total on an ASCII-only corpus; the mixed corpus yields one total; the malformed group in C-2's second line is reported, not counted either way. **Premises**: the owner § 4 rule 2 charset sentence exists (C-1); `parentheticals()` accepts both widths and reports malformed groups (C-2); self-test samples exist in `tests/contract/test_clause_forms.py`. Teardown: `rm -rf /tmp/s63-s1`.

## S2 — Coverage lane wired into analyze (SC-002; premises: C-5, C-6 landed)

```bash
bash scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks   # spec dir of a fixture feature WITH contracts/
python3 scripts/python/account-clause-coverage.py --spec <fixture-spec-dir>       # frozen baseline present → compare mode, exit per delta
grep -n "account-clause-coverage" .specify/skills/internal/analyze-artifacts/SKILL.md .specify/templates/commands/analyze.md   # the wired callers
grep -rn "coverage-baseline" .specify/skills/internal/create-tasks/SKILL.md       # the freeze duty
find .specify/specs -name coverage-baseline.txt | wc -l                            # grows by one per contract-set feature after tasks
```

Expected: a feature whose `tasks.md` was generated after C-6 owns `coverage-baseline.txt` at `<spec-dir>/`; analyze's report carries the coverage verdict; a missing baseline surfaces as `baseline-missing` with the remedy (re-run `/speckit.tasks`), never a silent pass. **Premises**: the analyze skill load table + workflow reference the accountant (C-5); create-tasks freezes the baseline at its existing re-freeze timing (C-6).

## S3 — Gap items are consumed at first analyze (SC-003; premises: C-3, C-4 landed)

Fixture: a feature whose `checklists/*.md` contains one unchecked item tagged `[覆盖/安全, Gap]` (replicating 062 CHK005's shape) and one unchecked item WITHOUT a `Gap` tag. Run `/speckit.analyze` on the fixture. Expected: the `Gap` item appears in the gate report either as a raised finding or with a deterministic disposition marker; the untagged item loads under existing semantics with no new obligation; the report's "unchecked + unraised + undispositioned Gap" count is observable and equals 0. **Premises**: the skill's load table includes `checklists/*.md` (C-3); the checklist detection pass and marker form exist (C-4).

## S4 — Recheck answers replace the every-feature waiver (SC-004; premises: C-8, C-9, C-10 landed)

Fixture: a checklist whose `Gap` item was answered by a downstream stage via `checklists/recheck-<date>-<topic>.md` (entry quotes the requirement line it answers). Run implement's Step 2 gate. Expected: the answered item counts as answered (no waiver); a genuinely unresolved item produces a waiver carrying all four parts `Scope`/`Basis`/`Disposition`/`Closed`; the original checklist file's git diff across the run is empty (no in-place refresh). **Premises**: recheck form declared in create-checklist § 5 (C-8); third branch in implement Step 2 (C-9); four-part waiver (C-10).

## S5 — REC- ids persist and transitions resolve (SC-005, SC-006; premises: C-11..C-15 landed)

```bash
# fixture: a seed review with 2-3 REC- ids; simulate the review stage's closure duty
grep -c "REC-" .specify/memory/register.md          # ≥ seed count after registration; same commit (git show --stat)
grep -n "REC-" .specify/instructions.md             # enumeration reached the live file via /speckit.instructions content refresh (Action 5)
grep -n "A3 自省" .specify/shared/workflow/feedback-step.md   # the named legal entry
git clone --quiet . /tmp/s63-clean && test -f /tmp/s63-clean/<a REC target repo-relative path> && echo resolvable; rm -rf /tmp/s63-clean
grep -n "speckit.review" .specify/shared/workflow/feature-integration.md   # the new transition row
```

Expected: each seed REC- id has a register.md pointer row in the same commit; targets resolve on a clean clone (repo-relative primary form); the scope guard names the A3 自省 entry; the transition table carries the review row with the annotated checklist row; "each command owns exactly one transition" holds (one row per command). **Premises**: C-11..C-15 landed and synced.

## S6 — Compiled wrap-up faces execute as written (SC-007, SC-008; premises: C-20..C-25 landed)

```bash
# in an isolated worktree; substitute <…> placeholders per the face's convention line
python3 .specify/scripts/python/run-determination.py --action determine --unit-id "/speckit.plan" --unit-type command --run-id s63-test-$(date -u +%Y%m%dT%H%M%SZ) --complexity complex
python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "/speckit.plan" --unit-type command --run-id s63-test-x --review "test" --points "No significant optimization points identified this run."
python3 .specify/scripts/python/run-determination.py --action determine --unit-id x --unit-type y        # missing ≥2 → ONE error listing all
python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check                           # zero drift after recompile
```

Expected: steps 1–2 succeed on first call (no per-arg error chain); step 3 exits 2 with one error naming every missing required flag; a duplicate `(unit_id, run_id)` re-run returns `duplicate: true` and never mints a run-id; `--check` is zero-drift; the 2026-10-15 backlog row reads `closed` (in the same commit as the recompiled units — verified via `git show --stat`). **Premises**: renderer placeholder convention + engine manifests (C-20..C-22); one-shot error listing (C-23); idempotency untouched (C-24); recompile + backlog flip (C-25). Note: S6's steps 1–2 must run against a disposable workspace state (or accept the record they write into the live feedback store as this run's own wrap-up record); the isolated-worktree form is preferred.

## S7 — Environment-premise carriers closed (SC-009; premises: C-16, C-17 landed)

Fixture: a seed `tasks.md` with a `**D-Tn**` row restating an environment verdict without date/pointer. Run `/speckit.tasks` generation rules against it (create-tasks carrier rule). Expected: the row is flagged until it carries an ISO date AND `(see § Environment Prerequisites)`; both required — date-only or pointer-only each fails. **Premises**: the carrier list covers assumption/decision and free-prose rows (C-16); the template's ACTION REQUIRED carries the date+pointer duty (C-17).

## S8 — Pass claims bind to archived evidence (SC-010; premises: C-26..C-28 landed)

Fixture: a `verification.md` built from the new template with four `pass` samples — one with existing+matching evidence, one missing the archived file, one empty file, one hash-mismatched. Run the gate check. Expected: green only for the matching sample; each red names the sample id and reason (missing/empty/mismatch); a `fail`-verdict sample triggers no binding duty. Then run the same check WITHOUT the evidence section: every `pass` is unverified. **Premises**: evidence section in the template (C-26); gate row + HandlerBinding registered and referenced at implement Step 9 (C-27); red semantics (C-28).

## S9 — Baseline pre-flight re-reads frozen values (SC-011; premises: C-19, C-29, C-30 landed)

Fixture: a spec dir with a frozen `notes/baseline-*` whose value the tree no longer matches, plus one missing baseline file. Run implement's pre-flight. Expected: values re-captured; citing rows written back; each difference classified (or explicitly `undecidable` — no guessing); the missing file treated as first-capture with provenance, not zero-drift. **Premises**: pre-flight step exists before Step 1 (C-29); the set is directory-derived (both glob roots + coverage baseline); re-freeze timing text points at this step (C-19); the command face states the duty (C-30).

## S10 — Global regression & invariants (SC-012, SC-013, SC-014)

```bash
bash scripts/bash/run-tests.sh --names-out /tmp/s63-after.txt
comm -13 .specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt /tmp/s63-after.txt   # MUST be empty
python3 scripts/python/sync-mirrors.py --check
git diff --stat -- .specify/specs/062-humanize-command/                                               # MUST be empty
grep -rn "gate-implement-evidence-binding" shared/definitions/probe-definitions.md                     # the registered row ([[STR-001]])
rm -f /tmp/s63-after.txt
```

Expected: zero NEW failing test names vs the frozen 63-name baseline (pre-existing failures are not this feature's repair surface); no new mirror drift on the pairs this spec touches; 062's four governed artifacts untouched; a red-first note quoting only a bare gate id fails the C-18 rule in review (verbal check against the shape rule). **Premises**: all mechanisms landed and synced; the frozen baseline from S0 is the comparison basis.
