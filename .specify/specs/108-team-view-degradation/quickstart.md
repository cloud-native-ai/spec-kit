# Quickstart — 108-team-view-degradation

**Rule**: every command example below is either executed once at plan time (route **a**, with its real output quoted) or pinned by a named test (route **b**, written by `/speckit.tasks`/`/speckit.implement`). Route-b examples are not executable before the implementation lands; each carries its own premises and names exactly the test that pins it. Repo root = the worktree `team-view-degradation`; all fixture trees are built under the sanctioned scratch root `.specify/.tmp/sdd-loop/tmp/team-view-degradation/` or pytest `tmp_path`.

## S-0 — Environment and current readings (executed at plan time, 2026-11-26)

Purpose: fix the floor the plan stands on — CLI contract, corpus misreporting, engine messages, baseline object.

```bash
python3 scripts/python/team-view.py --help
# exit 0 (measured). Output starts:
#   usage: team-view.py [-h] [--repo-root REPO_ROOT] [--scope {teams,auto,anchor,goals}] [--spec-dir SPEC_DIR] [--json] [--version] [<team-slug>]
# and ends with:
#   side-effects: none; reads the team archive and prints; a flag-only invocation writes nothing
#   exit-codes: 0 rendering produced; 2 input error; 3 team not found; 4 definition corrupt; 5 rendered with a degraded engine read

python3 scripts/python/team-view.py --version
# exit 0 (measured): team-view.py 0.0.22

python3 scripts/python/team-view.py viz-skill-arena --repo-root .
# exit 0 (measured). The relevant lines today:
#   - 运行报告: 为空（…/.specify/teams/viz-skill-arena/runs）
#   - 未识别（unrecognized）: 2026-08-07T15-00-00Z-report.md, … (5 names, unbounded)
#   - 最近报告（latest_report）: 未记录
# This is the misreporting FR-005/FR-006 repair targets (five real reports shown as empty).

git cat-file -e 54c6efa8c && echo baseline-object-present
# measured: baseline-object-present
git show 54c6efa8c:scripts/python/team-view.py | sha256sum
# measured: 81fad3f9… (identical to the current scripts/python/team-view.py)
```

Premises for S-0: the worktree is a git checkout containing commit `54c6efa8c`; `python3` can execute the program; the archive contains `viz-skill-arena` with its five non-conforming report names. These are plan-time readings; `/speckit.implement` re-measures them (research § Re-measure list 1–2).

## S-1 — Healthy fixture stays byte-identical (route b)

Scenario: a fixture satisfying the full FR-022 healthy predicate (the single owner of the condition set) — complete three-key binding, two compact-named readable reports, zero auxiliary artifacts, zero residue, `agent` column present, `goal` absent or slug-form (both variants are exercised: `goal` absent and `goal: <slug>`), `items.jsonl` present with at least one line, and all three continuous-spine files present.

```bash
# pseudocode of the pinning test's own steps (subprocess use is internal to the test):
# 1. build the fixture with tests/fixtures/team_view_fixtures.py — reports=<two compact
#    names>, items_lines=<one valid ledger line>, spine=("constraints.md", "STATE.md",
#    "run-log.jsonl"); build the goal-absent and the goal:<slug> variants
# 2. materialize git show 54c6efa8c:scripts/python/team-view.py beside copies of
#    scripts/python/script_interface_cli.py and scripts/python/goal-utils.py
# 3. run baseline and amended programs on the single-team view (`<slug> --repo-root <fixture>`)
# expected: identical stdout bytes, identical exit code (0), for both goal variants
```

Pinned by `tests/integration/test_team_view_degradation.py::test_healthy_fixture_is_byte_identical_to_the_baseline_program`. Premises: the fixture builder's `default_frontmatter()` renders the canonical binding block the engine accepts; `items_lines=` and `spine=` write the ledger and the three continuous-spine files; `script_interface_cli.py` and `goal-utils.py` are importable/executable siblings of the materialized baseline; commit `54c6efa8c` is present. The plan-time reading (research M4) was taken with the *unamended* program on the smaller builder-default fixture, which does not satisfy the completed predicate (no ledger, no spine) — the amended-vs-baseline reading MUST be re-taken on the completed-predicate fixture.

## S-2 — Production replica: latest is the parsed maximum (route b)

Fixture from the user-supplied production facts — four reports and one auxiliary artifact plus two residue files:
`20261124T074500Z-report.md` (old conforming), `20261125T121924Z-93cc-stage.md` (4-hex + stage), `2026-11-25T140000Z-report.md` (ISO-dashed), `20261008T214100Z-report.md` (same stamp as the auxiliary), `20261008T214100Z-seat-result.md` (auxiliary), `2026-10-07-progress-snapshot.md` and `2026-10-06-S1-judgment-contract.md` (residue).

```bash
python3 scripts/python/team-view.py prod-replica --repo-root <fixture>
# expected after implementation: exit 5 (residue ≥ 1 → report-recognition-uncertain);
# 最近报告（latest_report） = 2026-11-25T140000Z-report.md, the maximum parsed stamp
# (normalized token 20261125T140000Z); the 4-hex stage file (20261125T121924Z) and the old
# report (20261124T074500Z) MUST NOT be selected;
# 报告/辅助样本分类命中 = 5/5 (the four reports are reports; the seat-result file is auxiliary
# and never latest); the residue line reads 共 2 份；示例: …（省略 0）.
```

Pinned by `tests/integration/test_team_view_degradation.py::test_production_replica_latest_is_the_parsed_maximum` (latest name + 5/5 classification + residue line shape) and `::test_auxiliary_artifact_never_becomes_latest`. Premises: the five stamp forms in C-201; examples cap 3; the two residue names carry date-only prefixes. Production names are user-provided facts (A-12), not live files.

## S-3 — Corpus-style reports are recognized (route b)

Fixture replicating the three in-repo teams' naming (13 report-style names: 5 × `YYYY-MM-DDThh-mm-ssZ-report.md`, 7 × `YYYY-MM-DDThhmmssZ-report.md`, 1 × `YYYYMMDDThhmmZ-report.md`), each with a complete binding.

```bash
python3 scripts/python/team-view.py corpus-replica --repo-root <fixture>
# expected after implementation: exit 0; 运行报告: 已列出（共 13 份…）; latest = the
# name with the maximum parsed stamp (2026-09-17T115453Z-report.md normalizes to 20260917T115453Z);
# state MUST NOT be 为空 or 缺失.
```

Pinned by `tests/integration/test_team_view_degradation.py::test_corpus_style_reports_are_recognized` (13/13 coverage, latest name, exit 0) — SC-002. Premises: research M1's per-team style table; the fixture's frontmatter uses the canonical binding; normalization is C-204.

## S-4 — Residue-only history is never "empty" (route b)

```bash
python3 scripts/python/team-view.py residue-only --repo-root <fixture>
# expected after implementation: exit 5; 运行报告: 未识别（unrecognized）—— 仅残留，最新不可确定;
# 未识别（unrecognized）: 共 2 份；示例: 2026-10-06-S1-judgment-contract.md,
# 2026-10-07-progress-snapshot.md（省略 0）; 最近报告: 未记录; the degradation block names
# report-recognition-uncertain.
```

Pinned by `tests/integration/test_team_view_degradation.py::test_residue_only_runs_state_is_not_empty_or_missing`. Premises: the two residue names have date-only prefixes (no time), so no stamp parses; the fixture has a complete binding.

## S-5 — Degraded definition names every state (route b)

Fixture reproducing the production shape: no `binding` block, inline `goal`, matrix without the `agent` column, missing `items.jsonl`, `pattern: iteration` with the three spine files missing, nine frontmatter members.

```bash
python3 scripts/python/team-view.py degraded-team --repo-root <fixture>
# expected after implementation: exit 5; and all six named states present:
#   绑定（binding）: 不可读（binding-missing: … carries no binding block…）
#   绑定修复路径: /speckit.team modify … goal-utils.py bind
#   goal 需归一为 anchor_slug（repair pointers…）
#   正文矩阵: 形态异常（缺列: agent）
#   名册差异（roster_delta）: 不可比对（not comparable）（原因：…）
#   台账: 缺失（…；后果：无台账聚合计数、无非终态信号）
#   constraints.md / STATE.md / run-log.jsonl: 按声明 pattern 不适用（pattern=iteration…）
#   frontmatter 成员 9/9 listed; /speckit.team modify appears ≥ 1 time; no fabricated zeros.
```

Pinned by `tests/integration/test_team_view_degradation.py::test_degraded_definition_names_every_state` — SC-003. Premises: the engine's binding message text (research M3); nine members in the fixture; `pattern: iteration` (a declared non-`continuous` value); owner pointers as in C-301/C-302/C-305.

## S-6 — Overview discloses uncertainty inline (route b)

```bash
python3 scripts/python/team-view.py --repo-root <fixture-with-two-teams>
# expected after implementation: exit 0; the clean team's latest cell = its normalized token;
# the residue-bearing team's cell = <token or 未记录>（report-recognition-uncertain：残留 N）;
# the two cells' token values equal the single-team view's as_of.latest_report_timestamp.
```

Pinned by `tests/integration/test_team_view_degradation.py::test_overview_matches_single_view_and_discloses_uncertainty` — SC-006. Premises: overview performs no engine read and keeps the `0/2` exit domain; the marker string is C-207's.

## S-7 — Closed sets and single entry (route b)

```bash
# source scans (no subprocess needed):
#  - exactly one `def classify_runs(` and one timestamp grammar in scripts/python/team-view.py
#  - reason ids in source == {engine-degraded, report-recognition-uncertain}
#  - program label constants ⊆ contracts/view-labels.contract.md tables
#  - the three surfaces (docs View Mode, skill row 5, program declaration) each name both
#    reason ids and this feature's program contract path
# behavioural:
#  - binding-unreadable fixture → exit 5; residue fixture → exit 5; missing/empty-only fixture → exit 0
```

Pinned by `tests/contract/test_team_view_degradation_contract.py` (tests `test_single_recognition_entry_source_scan`, `test_reason_set_is_closed`, `test_exit_mapping_two_of_two`, `test_label_constants_match_the_owner_table`, `test_three_surfaces_cite_the_owner`) — SC-005, SC-006. Premises: the program keeps its label constants as `STATE_*` / new constants; the contracts' tables are machine-readable Markdown tables; the skill and docs pages keep the paths named in C-109.

## Run the targeted set (implement stage)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/unit/test_team_view_report_recognition.py \
  tests/contract/test_team_view_degradation_contract.py \
  tests/integration/test_team_view_degradation.py \
  tests/unit/test_team_view_parsers.py \
  tests/contract/test_team_view_program_contract.py \
  tests/contract/test_team_view_command.py \
  tests/integration/test_team_view_program.py -q --names-out <evidence path>
# expected: rc 0 with zero new failure names against the implement-entry baseline
```

Pinned by SC-008's stage record (the runner's own exit code and name-level diff). Premises: `SPECKIT_PYTHON=/usr/local/bin/python3` (pytest 8.4.2 measured); the four 103 test files unchanged since plan time (research § Re-measure list 5); the selection above covers every new and inherited team-view test file.
