# Plan-stage deterministic checks — slice 074b-nested-governance

Recorded 2026-10-29 during `/speckit.plan` for `.specify/specs/074b-nested-governance`
(`stage_base=33269994a`). Every block below is a command actually run in this repository followed by
its real output. Nothing here is a pre-written expectation.

## 0. Test budget record (targeted-set-v1, `stage_base=plan`)

Two records, because the stage's change set is docs-only while a targeted suite was in fact run:

**E3 stage-status row (targeted evidence)** — `stage=plan`, `row_type=stage-status`, `status=ran`,
`selection_basis=targeted-set-v1` (19 files, § 7 below),
`changed_paths[]=.specify/specs/074b-nested-governance/{plan.md,research.md,data-model.md,contracts/*.md,quickstart.md,feature-ref.md,test-evidence/*}`,
`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt`.

**Full-suite row (docs-only, six reduced fields per
`.specify/skills/sdd-loop-driver/references/efficiency-model.md`)** — `stage=plan`,
`row_type=stage-status`, `status=not-run-docs-only`,
`selection_basis=no executable surface changed by this stage (design artifacts only), so the full suite
has no new subject`, `changed_paths[]=.specify/specs/074b-nested-governance/** (markdown only)`,
`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/plan-stage-checks.md`. Run fields do
not apply and are not reported as `unknown`.

## 1. Contract clause extraction

```bash
python3 scripts/python/clause_extract.py .specify/specs/074b-nested-governance/contracts/*.md
```

```text
compat-and-safety.md	form=md-bold-closed	clauses=12
  C-1 … C-12
diffusion.md	form=md-bold-closed	clauses=8
  C-13 … C-20
report-and-attribution.md	form=md-bold-closed	clauses=10
  C-21 … C-30
rc=0
```

30 clauses across 3 files (the real run printed each id on its own line; elided here only in the `…`
ranges). All three are canonical `md-bold-closed` and the ids are contiguous C-1…C-30 in file-name
order: `compat-and-safety` 1–12, `diffusion` 13–20, `report-and-attribution` 21–30.

## 2. Clause and FR coverage accounting

```bash
python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance
```

```text
scanned 215 files: parsed 121 + named-unparseable 94 == 215  [relational sentinel OK]
clause universe: 1315 distinct names over 121 parsed files (1339 ids extracted)

== FR coverage (universe: requirements.md definition rows outside code spans; claimed: clause citation groups, never task rows) ==
FR universe: 8
FR claimed: 8
FR uncovered: 0

ERROR frozen baseline not found: .specify/specs/074b-nested-governance/coverage-baseline.txt — an absent baseline is NOT an empty exemption list, so this run cannot judge the delta
companion (must be non-empty on a green run): claimed clauses 0, scanned files 215, clause universe 1315, FR universe 8
  [clause-uncovered] fail (525) — 525 uncovered, 525 beyond the frozen baseline
  [fr-uncovered] pass (0) — 8 of 8 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id under the owner's forms; 0 of them declare a positive form, which is parse doubt and is never read as zero-and-covered
  [coverage-baseline-delta] fail (525) — baseline holds 0 names; 0 uncovered items are baseline-internal and do not block
526 error(s), 0 warning(s)
status: baseline-missing
rc=2
```

**Reading (no suppression)**: the FR lane is green (8/8, uncovered 0). The clause lane is red **by
design at this stage** and is not claimed as green: clause claims are `[green:]` rows in `tasks.md`,
which does not exist yet, and the frozen baseline belongs to the tasks stage. Freezing a baseline now
would record zero claimed clauses and make that stage trivially green — the failure mode the
`[coverage-baseline-delta]` line exists to prevent. The `clause-unparsable` advisory covers 94
pre-existing files across the repository corpus, unrelated to this slice.

## 3. Cross-artifact pre-analyze gate (plan stage, canonical invocation)

```bash
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/074b-nested-governance --stage plan
```

```text
pre-analyze-check: stage=plan decision=pass errors=0 advisories=0 waived=0
{"stage": "plan", "decision": "pass", "findings": [], "summary": {"errors": 0, "advisories": 0,
 "waived": 0, "fr": 8, "sc": 2, "tasks": 0, "clauses": 0, "files": 10},
 "checked_at": "2026-10-29T04:44:03Z"}
rc=0
```

`clauses=0` is a known reading of this checker, not an absence of clauses: its legacy prefix pattern
(`[A-Z]{2,4}-\d{2}`) does not match the canonical `**C-N**` form. The clause count is taken from § 1.

**First run of this gate failed and was repaired in place** — recorded because a green re-run alone
would hide it: 9 `dangling-id` errors, every one of them a *parent* requirement number written in the
local hyphen notation inside a facet parenthetical (`(FR-028 facet)` in `plan.md:245`,
`contracts/compat-and-safety.md:15` and `:78`; `C-54 (FR-013 facet)` / `C-66 (FR-018 facet)` in
`plan.md:260`/`:263` and `plan.md:283`; `the FR-013/FR-018 facets` in `research.md:47`). The slice's
local universe defines FR-001–FR-008, so a bare parent number reads as a dangling local id. Repair: the
parent form `parent FR 028 facet`, which the checker correctly does not read as a local id — the same
notation the requirements stage adopted and the same repair `074a` needed. Re-run:
`decision=pass errors=0`.

## 4. Pre-analyze with repository path resolution (advisory lane)

```bash
python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py \
  --spec-dir .specify/specs/074b-nested-governance --stage plan --repo .
```

```text
pre-analyze-check: stage=plan decision=pass errors=0 advisories=13 waived=0
```

All 13 advisories are `missing-path` findings naming the three test modules this slice plans to create
(`tests/contract/test_nested_run_report.py`, `test_sdd_diffusion.py`,
`test_sdd_compat_containment.py`) at the eleven sites that reference them. None is an error: a design
artifact naming a file that `/speckit.implement` will create is exactly what a plan is for. The
canonical stage invocation (§ 3) does not pass `--repo`, which is why it reports `advisories=0`; both
readings are recorded so neither is mistaken for the other.

## 5. Mirror, per-tool copy and flow-class baselines

```bash
python3 scripts/python/sync-mirrors.py --check        # rc=0
python3 scripts/python/regen-command-copies.py --check  # rc=0
python3 scripts/python/flow-class-check.py --action check  # rc=0
```

```text
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (406 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (114 files)
ok    shared/ == .specify/shared/ (59 files)
OK: all per-tool command copies match the source templates.
flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
```

Zero pre-existing drift, so the mirror criterion in `plan.md` is both "no NEW drift" and measurably
"clean". The counts read 406/114/59 rather than `074a`'s recorded 405/113/58 because `074a` added three
files — a baseline belongs to the commit it was taken at, never to a copy of an older number. The
flow-class result (79 units / 0 findings) is the mechanical form of local C-11 (no new command, no new
skill).

## 6. Diagnostic measurements quoted by `research.md` and `quickstart.md`

```bash
wc -c .specify/instructions.md templates/instructions-template.md
grep -n "INSTRUCTIONS_BUDGET_BYTES" scripts/bash/generate-instructions.sh
grep -c '^## ' templates/instructions-template.md .specify/instructions.md shared/guidelines/proactive-trigger.md
grep -n "^## Result Summary" skills/internal/create-team/SKILL.md
grep -n "Stage\*\* — one of" skills/internal/create-team/references/conceptual-model.md
grep -n "Report contract\|create-team SKILL.md → Report" skills/internal/run-team/SKILL.md
grep -c "sdd-invocation" agents/sdd-executor.agent.md
grep -rn "Nested SDD Runs" skills/ templates/ shared/ src/
grep -n "sdd-routing-definitions" templates/instructions-template.md shared/guidelines/proactive-trigger.md
```

```text
41948 .specify/instructions.md
34666 templates/instructions-template.md
76614 total
38:INSTRUCTIONS_BUDGET_BYTES=32768
68:# Report the generated file's size against INSTRUCTIONS_BUDGET_BYTES, plus a
91:  budget_out="$(python3 - "$target" "$rendered" "$INSTRUCTIONS_BUDGET_BYTES" <<'PYEOF'
templates/instructions-template.md:29
.specify/instructions.md:30
shared/guidelines/proactive-trigger.md:10
60:## Result Summary ## Deliverables ## Verification ## Execution Detail ## Run Workspace ## Summary
10:- **Stage** — one of `executor`, `evaluator`, `optimizer` (canonical names; the deprecated dimension name "SubRole" and stage name "improver" are removed).
66:执行结束后把带日期的运行报告写入 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`(**每次运行强制**,报告契约真源:create-team SKILL.md → Report;含 `## Verification` 节)。Target 指派的运行报告带固定字段,逐字形态:`**Target 指派**: T-<nnn>(<statement>)` 或 `无(goal 整体)`,团队默认路径追加 `(团队默认)`;新台账条目带 `"target_ref": "T-<nnn>"`。
0
rc=1                       # grep -rn "Nested SDD Runs" over shipped surfaces: no hit
rc=1                       # no pointer names the routing owner yet
```

**What each reading settles**: the instructions budget is already exceeded (41,948 B live, 34,666 B
template, 32,768 B budget) so the acceptance criterion is a declared ceiling plus a measured delta; the
template/live section counts differ by one, proving the reconcile is additive rather than a re-render;
the report contract's mandatory section list is one line at `create-team/SKILL.md:60`, so appending one
heading is the whole edit; `run-team` already delegates at `:66`; the leaf preset declares no
`sdd-invocation` key; neither the report-section literal nor the routing pointer exists anywhere in the
shipped tree yet (D-3's hand-over is intact).

## 7. Targeted contract suite baseline

See `targeted-set-v1-baseline.txt`: 19 files, `1 failed, 289 passed in 34.27s`, `rc=1`,
`stage_base=33269994a`, single failed id
`tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`.

**Pre-existing red, disclosed**: that case asserts the confirmation-gate scan total equals its frozen
baseline and reports `gate total moved from the frozen 23 to 27`. The four added gates predate this
slice (the tree is unmodified at capture time), so this is drift inherited from earlier features, not
an effect of this stage. It is recorded rather than repaired: repairing it would mean editing another
feature's declarations or rebasing its frozen baseline inside a plan-only commit — a decision, not a
correction, and outside this slice's declared scope. The slice's own criterion (local C-19's pointer
sentence adds no gate-scannable declaration) is that the total measured after the edit equals the
pre-change total, and no green claim is made over the inherited case.

## 8. Containment baseline capture (pre-change, 7 named sets)

```bash
python3 -m pytest --collect-only -q <17 named suite files>   # per set, node ids sorted into the carrier
```

```text
S1-pre-dispatch-governance      cases: 49     (test_sdd_invocation_governance 17 + test_agent_dispatch_mechanism 32)
S2-standalone-driver-entry      cases: 25     (test_sdd_loop_driver_skill 25)
S3-070-stage-team-preset        cases: 24     (test_sdd_loop_driver_wp_preset 14 + test_non_regression_070 10)
S4-064-line-worktree-ownership  cases: 40     (test_non_regression_064 9 + test_line_registry_contract 13 + test_line_envelope_contract 18)
S5-058-u0-u6                    cases: 36     (test_sdd_loop_driver_gates 7 + test_loop_state_contract 29)
S6-team-suites                  cases: 54     (test_team_item_ledger 13 + test_team_command_routing 32 + test_team_territory 6 + test_single_conceptual_model 3)
S7-agent-suites                 cases: 38     (test_shipped_agent_presets 5 + test_neutral_metadata_schema 29 + test_agent_chain_guards 4)
total cases: 266 across 17 files
```

Carrier: `test-evidence/compat-baseline-nodeids.txt` (one node id per line, sorted per set). The claim
is the **sets**, never these integers: `074a`'s precedent and the cross-cutting lessons both record the
count-comparison failure mode (a rename and an addition net to zero). The set is re-captured at
implement start under the never-cache rule before any edit.

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
(`074b-nested-governance` → prefix `074b`, but `find_feature_dir_by_prefix` matches the glob `074-*`,
which cannot match `074b-…`), so the single match is the **parent** directory, whose `plan.md` exists,
and the guard refused. `--force` was deliberately **not** used: it would have overwritten the parent
plan, which is read-only authority for this stage.

**Repair**: `plan.md` was authored in place at the slice path, following
`.specify/templates/plan-template.md` section order and placeholder obligations. Classified as a
**correction**, not an adjudication: exactly one reading is consistent with the dispatch brief and the
slice requirement — the stage's target directory is the slice's own spec directory — the change is
local and reversible, and no downstream premise is falsified. The same prefix collision was recorded by
`074a` (`074a-authorized-routing/test-evidence/plan-stage-checks.md` § 9) and will affect
`create-new-tasks.sh` at the next stage, which must target the slice directory explicitly.

## 10. Scratch discipline

The one scratch probe of this stage (the SC-002 goal fixture) ran under the sanctioned
`.specify/.tmp/074b-goal-fixture` root and was removed in the same capture (`rm -rf`, teardown rc=0,
`git status` shows no residue). The failed-name lists were written to `.specify/.tmp/` as well. No
scratch path is committed; `.gitignore` already matches `*.tmp`.
