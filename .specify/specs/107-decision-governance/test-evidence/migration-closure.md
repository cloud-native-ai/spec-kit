# Migration closure evidence — 107-decision-governance (T051)

Captured: 2026-11-26 (UTC), worktree `.specify/.tmp/sdd-loop/worktrees/decision-governance`,
branch `107-decision-governance`, base `08b59695c` (line base `fbab7a45c`; worktree merged with
line 106 at `0d7519521` before implement).

Every BC row of `plan.md` § Backward-Incompatible Change Inventory is exercised here by its
named behavior; the command, the real output excerpt and the pinning test are recorded per row.
The row-set/mapping closure itself is guarded by
`tests/contract/test_decision_governance_migration_map.py` (C-501/C-505).

## BC-01 — new decision record block in existing carriers → `compatibility-bridge` (legacy floor)

The minimal qualifying form is `^### D-\d{3}` **and** ≥1 C-201 field line; below it every
heading and register row is `legacy` (readable, not judged, not rewritten); at it the block is
new-form even when incomplete, and missing fields are M-01's red.

```text
$ python3 scripts/python/validate-decisions.py --action records --carrier tests/fixtures/decision-governance/legacy/legacy.md --register tests/fixtures/decision-governance/legacy/register.md
PASS: 0 violation(s) (rules: M-01, M-02, M-03, M-04, M-08, M-09)
EXIT=0        # `### D-1` / `### D-12` / `### D-001` headings and D1–D9 / D-001 / D-001-a rows reported LEGACY

$ python3 scripts/python/validate-decisions.py --action records --carrier tests/fixtures/decision-governance/legacy/incomplete-new-form.md --register tests/fixtures/decision-governance/legacy/register.md
M-01 .../incomplete-new-form.md:3: missing base-layer field(s): context, options, chosen_option, rationale, evidence, actor, created_at, transmission_status
FAIL: 1 violation(s)
EXIT=1
```

Pinned by `tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy`.

## BC-02 — `decision_block` in the dispatch payload → `compatibility-bridge` + deterministic refusal

A decision-backed dispatch without a block (or with a missing block field) is refused at payload
construction (M-06); a non-decision dispatch without a block stays legal; legacy payloads are
never rewritten (the checker is read-only).

```text
$ python3 scripts/python/validate-decisions.py --action payload --fixture tests/fixtures/decision-governance/m06/red-no-block.md
M-06 .../red-no-block.md:1: a decision-backed dispatch MUST carry a decision_block with decision_id, decision_class, chosen_option, implementation_constraints and archive_pointer; it is refused at payload construction (the decision_block is absent)
FAIL: 1 violation(s)
EXIT=1

$ python3 scripts/python/validate-decisions.py --action payload --fixture tests/fixtures/decision-governance/payload/non-decision.md
PASS: 0 violation(s) (rules: M-06)
EXIT=0
```

Pinned by `tests/contract/test_decision_governance_guards.py::test_m06_dispatch_without_block_refused`
(C-504) and `::test_m06_block_completeness`.

## BC-03 — new `D-NNN` id family beside `D1–D9` / `D-001` → `compatibility-bridge`

Ids are three-digit and dense per carrier, registered at birth; the legacy `D-001` register row
keeps its id shape but is never treated as a new-form record; duplicates are red and a conflict
is repaired through `/speckit.sanitize --lane renumber`, never by silent renumbering.

```text
$ python3 scripts/python/validate-decisions.py --action records --carrier tests/fixtures/decision-governance/m04/red-form.md --register tests/fixtures/decision-governance/m04/register.md
M-04 .../red-form.md:3: heading id 'D-001-a' does not match the D-NNN form (exactly three digits)
FAIL: 1 violation(s)
EXIT=1

$ python3 scripts/python/validate-decisions.py --action records --carrier tests/fixtures/decision-governance/legacy/legacy.md --register tests/fixtures/decision-governance/legacy/register.md --json
status pass | legacy register rows: ['D-001', 'D-001-a', 'D1–D9']
```

Pinned by `tests/unit/test_validate_decisions.py::test_m04_id_density_register` and the legacy
register fixture half of `test_legacy_two_digit_reported_legacy`.

## BC-04 — new instruction-template section → `compatibility-bridge` through `templates-generated`

Measured reading (the C-503 chain): the migrate dry-run lists the instruction-template
convergence item under the existing `templates-generated` dimension — `.specify/templates/instructions-template.md`
is the source of truth the generated `.specify/instructions.md` is rendered from, and the
migrate command's own Handoffs section delegates the regeneration of the generated file to
`/speckit.instructions` (the 097 engine contract's compared surfaces do not include
`.specify/instructions.md` itself). The integration test proves the section end to end.

```text
$ specify migrate --dry-run --format json        # on a client workspace whose instruction template predates the section
outcome: planned | exitCode: 1 | workspaceKind: client
dimensions observed: ['templates-generated']
  templates-generated | .specify/templates/instructions-template.md | replace | replace
raw payload: test-evidence/us6-migrate-dryrun.json

$ specify migrate --apply --format json          # outcome: applied (exit 0)
$ bash .specify/scripts/bash/generate-instructions.sh   # client's own generator: rc 0
=> .specify/instructions.md carries `## Decision Items（决策项）` with the full-name and
   same-name-locator production rules; the project's custom section survives the regeneration.
```

The migrate dimension set stays the closed six (`templates-generated`, `anchor-layout`,
`compat-links`, `mirror-consistency`, `migration-residue`, `store-layout`) — read from
`src/specify_cli/__init__.py` `MIGRATE_DIMENSIONS` and asserted identical inside the test; no
seventh member is added.

Pinned by
`tests/integration/test_decision_governance_migrate_dryrun.py::test_instructions_generated_dimension`
(C-503) and `tests/contract/test_decision_governance_contracts.py::test_client_init_receives_section`
(SC-010).

## BC-05 — new guards facing old records → `compatibility-bridge`

The checker judges only blocks at the new-form threshold; the real base-corpus carrier below is
reported `legacy` and exits 0 (no false red on legacy text), and the zero-rewrite line-level
reading holds over the corpus.

```text
$ python3 scripts/python/validate-decisions.py --action records --carrier .specify/specs/065-loop-interruption-recovery/research.md
PASS: 0 violation(s) (rules: M-01, M-02, M-03, M-04, M-08, M-09)
EXIT=0        # 32 legacy entries (16 `### D-NN` headings), zero violations
```

Pinned by `tests/integration/test_decision_governance_migrate_dryrun.py::test_base_corpus_zero_rewrite`
(C-502) and the legacy fixture tests above.

## BC-06 — two production rules → `compatibility-bridge` (new decisions only)

The rules constrain decisions created after landing; existing decision text is reported by
review under B-01/B-02 and never rewritten retroactively. The four-surface presence (owner
page, instruction section, decision-item templates, guard fixtures + the named B-01/B-02
review surfaces) is asserted by the contract test; the review-surface pointers live in
`skills/internal/{analyze-artifacts,review-feature-quality,review-sdd-process}`.

Pinned by `tests/contract/test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces`
(plus `::test_behavior_surfaces_named` for the named review surfaces).

## Zero-rewrite readings (C-502, line-level containment over `08b59695c..HEAD`)

```text
$ git diff --numstat 08b59695c..HEAD -- .specify/register.md
14	0	.specify/register.md          # appended T-019…T-021 rows; zero deletions

$ git diff --numstat 08b59695c..HEAD -- .specify/specs | awk '$2 != 0'
77	43	.specify/specs/107-decision-governance/requirements.md

$ git diff --diff-filter=D --name-only 08b59695c..HEAD -- .specify/register.md .specify/specs
(no output — no deleted file)
```

- The single file with deletions is **this feature's own in-flight requirements.md** — authored
  after the run base `fbab7a45c` by this run's requirements/clarify/plan/analyze stages (the
  analyze repair rounds rewrote FR/A/P bodies). It is not a legacy record; the C-502 corpus is
  the pre-existing records of prior work.
- The record body inside that file — its `## Clarifications` section — is append-only:
  base 5,290 B → head 14,170 B, every added line appended after the base text.
- The same append-only property holds for **all 89** pre-existing `requirements.md` files that
  carry a `## Clarifications` section at base (asserted by the integration test).
- Over the carrier families (register, `plan.md`, `checkpoints/**`, `test-evidence/**`,
  `verification.md`): 3,127 pre-existing files at base, every one present at HEAD, zero
  deletions in the numstat deletion column, empty `--diff-filter=D` set.

## Mirror / copy closure (C-506)

```text
$ python3 scripts/python/sync-mirrors.py --check      # rc 0, no drift member at all
ok templates/ == .specify/templates/ (23 files, byte-identical)
ok skills/external/ == .specify/skills/ (394 files, byte-identical)
ok skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok agents/ == .specify/agents/templates/ (20 files, byte-identical)
ok scripts/ == .specify/scripts/ (133 files, byte-identical)
ok shared/ == .specify/shared/ (117 files, byte-identical)
projected[bash-version-guard|python-version-bridge] ...: ok (6 pairs)

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.   # rc 0

Decision Items section: template 1,276 B == live 1,276 B (byte-identical);
live instructions total 40,170 B < 40,960 B budget.
```

Pinned by `tests/contract/test_decision_governance_contracts.py::test_mirror_and_copy_closure`.

## Disclosure — the C-503 wording vs the measured migrate surface

C-503's literal sentence names "the `.specify/instructions.md` convergence item"; the measured
engine behavior (and the 097 engine contract's compared-surface list, and the migrate command's
Handoffs delegation to `/speckit.instructions`) converges the instruction **template** under
`templates-generated` and never compares the generated file directly. This evidence and the
pinning test record the corrected reading — the template item plus the end-to-end landing is
what C-503's own first half ("through the existing templates-generated dimension") requires;
no seventh dimension, command or planner is added. Recorded for the review-stage adjudication.
