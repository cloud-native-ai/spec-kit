# Plan-stage deterministic checks — slice 074a-authorized-routing

Recorded 2026-10-29 during `/speckit.plan` for `.specify/specs/074a-authorized-routing`
(`stage_base=939766891`). Every block below is a command actually run in this repository followed by
its real output. Nothing here is a pre-written expectation.

## 0. Test budget record (targeted-set-v1, `stage_base=plan`)

Two records, because the stage's change set is docs-only while a targeted suite was in fact run:

**E3 stage-status row (targeted evidence)** — `stage=plan`, `row_type=stage-status`,
`status=ran`, `selection_basis=targeted-set-v1` (13 files, § 6 below),
`changed_paths[]=.specify/specs/074a-authorized-routing/{plan.md,research.md,data-model.md,contracts/*.md,quickstart.md,feature-ref.md,test-evidence/*}`,
`evidence_ptr=.specify/specs/074a-authorized-routing/test-evidence/targeted-set-v1-baseline.txt`.

**Full-suite row (docs-only, six reduced fields per
`.specify/skills/sdd-loop-driver/references/efficiency-model.md`)** — `stage=plan`,
`row_type=stage-status`, `status=not-run-docs-only`,
`selection_basis=no executable surface changed by this stage (design artifacts only), so the full suite has no new subject`,
`changed_paths[]=.specify/specs/074a-authorized-routing/** (markdown only)`,
`evidence_ptr=.specify/specs/074a-authorized-routing/test-evidence/plan-stage-checks.md`. Run fields do
not apply and are not reported as `unknown`.

## 1. Contract clause extraction

```bash
python3 scripts/python/clause_extract.py .specify/specs/074a-authorized-routing/contracts/*.md
```

```text
bootstrap-and-maintenance.md	form=md-bold-closed	clauses=4
  C-44 C-45 C-46 C-47
hierarchy-and-authorization.md	form=md-bold-closed	clauses=16
  C-1 … C-16
nested-invocation.md	form=md-bold-closed	clauses=13
  C-31 … C-43
routing-decision.md	form=md-bold-closed	clauses=14
  C-17 … C-30
rc=0
```

47 clauses across 4 files (ids printed one per line in the real run; elided here only in the `…`
ranges). All four files are canonical `md-bold-closed`; ids are contiguous `C-1`…`C-47` in
file-name order: `bootstrap` 44–47, `hierarchy-and-authorization` 1–16, `nested-invocation` 31–43,
`routing-decision` 17–30.

## 2. Clause and FR coverage accounting

```bash
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074a-authorized-routing
```

```text
== FR coverage (universe: requirements.md definition rows outside code spans; claimed: clause citation groups, never task rows) ==
FR universe: 20
FR claimed: 20
FR uncovered: 0

ERROR frozen baseline not found: .specify/specs/074a-authorized-routing/coverage-baseline.txt — an absent baseline is NOT an empty exemption list, so this run cannot judge the delta
companion (must be non-empty on a green run): claimed clauses 0, scanned files 212, clause universe 1285, FR universe 20
  [clause-uncovered] fail (542) — 542 uncovered, 542 beyond the frozen baseline
  [fr-uncovered] pass (0) — 20 of 20 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms; 0 of them declare a positive form
  [coverage-baseline-delta] fail (542) — baseline holds 0 names; 0 uncovered items are baseline-internal and do not block
543 error(s), 0 warning(s)
status: baseline-missing
rc=2
```

**Reading (no suppression)**: the FR lane is green (20/20, uncovered 0). The clause lane is red **by
design at this stage** and is not claimed as green: clause claims are `[green:]` rows in `tasks.md`,
which does not exist yet, and the frozen baseline belongs to the tasks stage. Freezing a baseline now
would record zero claimed clauses and make that stage trivially green — the failure mode the
`[coverage-baseline-delta]` line exists to prevent. The `clause-unparsable` advisory covers 94
pre-existing files across the repository corpus, unrelated to this slice.

## 3. Cross-artifact pre-analyze gate (plan stage, canonical invocation)

```bash
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/074a-authorized-routing --stage plan
```

```text
pre-analyze-check: stage=plan decision=pass errors=0 advisories=0 waived=0
{"stage": "plan", "decision": "pass", "findings": [], "summary": {"errors": 0, "advisories": 0,
 "waived": 0, "fr": 20, "sc": 6, "tasks": 0, "clauses": 0, "files": 11},
 "checked_at": "2026-10-29T02:08:09Z"}
rc=0
```

`clauses=0` is a known reading of this checker, not an absence of clauses: its legacy prefix pattern
(`[A-Z]{2,4}-\d{2}`) does not match the canonical `**C-N**` form. The clause count is taken from § 1.

**First run of this gate failed and was repaired in place** — recorded because a green re-run alone
would hide it: 13 `dangling-id` errors, all of them parent requirement numbers written in the local
`FR-0nn` notation (`parent FR-026`, `parent FR-021`, `parent FR-023`, `parent FR-024`, `parent
FR-027`, `parent FR-028`, `parent FR-022`) inside `research.md`, `feature-ref.md` and three contract
files. The local universe defines FR-001–FR-020 and SC-001–SC-006 only, so a bare parent number reads
as a dangling local id. Repair: the parent form `parent FR 0nn` (space-separated), which the checker
correctly does not read as a local id — the same notation the requirements stage adopted at
`c5e4c662a` for the same reason. Re-run: `decision=pass errors=0`.

## 4. Pre-analyze with repository path resolution (advisory lane)

```bash
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/074a-authorized-routing --stage plan --repo .
```

```text
pre-analyze-check: stage=plan decision=pass errors=0 advisories=47 waived=0
```

All 47 advisories are `missing-path` findings naming the files this slice plans to create
(`shared/definitions/sdd-routing-definitions.md`, `scripts/python/sdd-route.py`,
`skills/external/sdd-loop-driver/references/nested-invocation.md`, the five planned
`tests/contract/test_*.py`, `tests/fixtures/nested_sdd.py`) plus one pre-existing dated feedback path
in `checklists/requirements.md`. None of them is an error: a design artifact naming a file that
`/speckit.implement` will create is exactly what a plan is for. The canonical stage invocation (§ 3)
does not pass `--repo`, which is why it reports `advisories=0`; both readings are recorded so neither
is mistaken for the other.

## 5. Mirror and per-tool copy baseline

```bash
python3 scripts/python/sync-mirrors.py --check        # rc=0
python3 scripts/python/regen-command-copies.py --check  # rc=0
```

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (405 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (113 files)
ok    shared/ == .specify/shared/ (58 files)
```

Zero pre-existing drift, so the mirror criterion in `plan.md` is both "no NEW drift" and measurably
"clean".

## 6. Flow-class ledger unchanged

```bash
python3 scripts/python/flow-class-check.py --action check
```

```text
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
```

Confirms the slice adds no flow unit (no new command, no new skill) — the FR-020 / C-47 negative check.

## 7. Targeted contract suite baseline

See `targeted-set-v1-baseline.txt`: 13 files, `191 passed`, `rc=0`, `duration_ms=23129`,
`stage_base=939766891`.

## 8. The three new framework files do not exist yet

```bash
ls shared/definitions/sdd-routing-definitions.md scripts/python/sdd-route.py \
   skills/external/sdd-loop-driver/references/nested-invocation.md
grep -c 'sdd-invocation' src/specify_cli/__init__.py
```

```text
ls: cannot access 'shared/definitions/sdd-routing-definitions.md': No such file or directory
ls: cannot access 'scripts/python/sdd-route.py': No such file or directory
ls: cannot access 'skills/external/sdd-loop-driver/references/nested-invocation.md': No such file or directory
rc=2
0
```

The four premises every `quickstart.md` example disclaims, measured rather than assumed.

## 9. Stage setup deviation (disclosed, repaired in place)

```bash
bash scripts/bash/create-new-plan.sh --json
```

```text
Error: /storage/project/cloud-native-ai/spec-kit/.specify/specs/074-goal-team-sdd-unification/plan.md already exists.
Amend it in place instead of re-scaffolding, or pass --force to overwrite.
rc=1
```

**What happened**: the setup script resolves the spec directory from the branch name's numeric prefix
(`074-goal-team-sdd-unification` → prefix `074`), and `find_feature_dir_by_prefix` matches the glob
`074-*`, which cannot match `074a-authorized-routing` (no `074-` prefix — the slice directory starts
`074a`). The single match is therefore the **parent** directory, whose `plan.md` exists, so the guard
refused and nothing was written. `--force` was deliberately **not** used: it would have overwritten
the parent plan, which is plan-constrained and read-only for this stage.

**Repair**: `plan.md` was authored in place at the slice path
`.specify/specs/074a-authorized-routing/plan.md`, following `.specify/templates/plan-template.md`
section order and placeholder obligations (the same content the script would have copied). Classified
as a **correction**, not an adjudication: exactly one reading is consistent with the dispatch brief and
the slice requirement — the stage's target directory is the slice's own spec directory — the change is
local and reversible, and no downstream premise is falsified.

**Consequence worth carrying to `/speckit.tasks`**: the same prefix collision affects any script that
resolves the spec directory from this branch, including `create-new-tasks.sh`. The tasks stage must
target the slice directory explicitly rather than relying on branch-prefix resolution.
