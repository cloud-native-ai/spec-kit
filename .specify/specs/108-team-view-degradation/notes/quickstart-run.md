# Quickstart run — 108-team-view-degradation (T026)

Executed 2026-11-26 on worktree team-view-degradation (branch 108-team-view-degradation),
every scenario of `quickstart.md` as written: S-0 re-taken live (route a), S-1…S-7 executed
through their named pinning tests (route b) via the single entry
(`SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh`, pytest 8.4.2).
Full raw capture of every command below: `.specify/.tmp/sdd-loop/tmp/team-view-degradation/p4/quickstart-capture.txt`.

## S-0 — Environment and current readings (re-taken)

```bash
python3 scripts/python/team-view.py --help
```
exit 0. Usage synopsis unchanged (`usage: team-view.py [-h] [--repo-root REPO_ROOT]
[--scope {teams,auto,anchor,goals}] [--spec-dir SPEC_DIR] [--json] [--version]
[<team-slug>]`); the epilog now reads
`side-effects: none; reads the team archive and prints; a flag-only invocation writes nothing`
and `exit-codes: 0 rendering produced; 2 input error; 3 team not found; 4 definition corrupt; 5 rendered with a degraded engine read (degradation reasons: engine-degraded | report-recognition-uncertain; owner: .specify/specs/108-team-view-degradation/contracts/team-view-program.contract.md)`.

```bash
python3 scripts/python/team-view.py --version
```
exit 0 — `team-view.py 0.0.22` (unchanged).

```bash
python3 scripts/python/team-view.py viz-skill-arena --repo-root .
```
exit 0. The plan-time misreporting is repaired on the live archive: the relevant lines now
read `- 运行报告: 已列出（共 5 份，显示最新 5 份，省略 0）` and
`- 最近报告（latest_report）: 2026-09-15T090000Z-report.md` — no `运行报告: 为空`, no
unbounded unrecognized-name line, no `未记录` latest.

```bash
git cat-file -e 54c6efa8c && echo baseline-object-present
git show 54c6efa8c:scripts/python/team-view.py | sha256sum
```
`baseline-object-present`; baseline blob sha256 =
`81fad3f9df019319c75d1a73c1ffa27338ac942db6b22c4b90e6b5b61e7bf06b` (the same baseline
object the plan measured; the working-tree program has since been amended by this feature,
so the plan-time equality of the two hashes no longer applies — the fidelity claim is the
S-1 test's, not a hash equality).

## S-1 — Healthy fixture stays byte-identical (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "healthy_fixture_is_byte_identical"
```
exit 0 — `1 passed in 6.82s`. The node materializes `git show 54c6efa8c:scripts/python/team-view.py`
beside read-only `script_interface_cli.py` / `goal-utils.py`, builds the completed FR-022
predicate fixture in both goal variants, and asserts byte-identical stdout + equal exit
codes (diff lines = 0).

## S-2 — Production replica: latest is the parsed maximum (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "production_replica or auxiliary_artifact"
```
exit 0 — `2 passed in 6.48s`. Latest = `2026-11-25T140000Z-report.md` (normalized
`20261125T140000Z`), 5/5 classification, bounded residue line `共 2 份；示例: …（省略 0）`,
exit 5 with `report-recognition-uncertain`; the auxiliary artifact never becomes latest.

## S-3 — Corpus-style reports are recognized (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "corpus_style"
```
exit 0 — `1 passed in 6.45s`. 13/13 recognized, `运行报告: 已列出（共 13 份…）`, latest
`2026-09-17T11-54-53Z-report.md` (normalized `20260917T115453Z`), exit 0.

## S-4 — Residue-only history is never "empty" (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "residue_only"
```
exit 0 — `1 passed in 6.30s`. `运行报告: 未识别（unrecognized）—— 仅残留，最新不可确定`,
bounded residue line with both names, `最近报告: 未记录`, degradation block names
`report-recognition-uncertain`, exit 5.

## S-5 — Degraded definition names every state (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "degraded_definition_names_every_state"
```
exit 0 — `1 passed in 6.48s`. All six named states present (binding `不可读` + repair
pointers, `goal 需归一为 anchor_slug`, matrix `形态异常（缺列: agent）`, `roster_delta`
`不可比对` with reason, ledger `缺失` with consequences, spine `按声明 pattern 不适用`),
9/9 members, `/speckit.team modify` ≥ 1, zero fabricated values, exit 5.

## S-6 — Overview discloses uncertainty inline (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_team_view_degradation.py -q -k "overview_matches_single_view"
```
exit 0 — `1 passed in 6.52s`. The overview cells equal the single-view
`as_of.latest_report_timestamp` values (2/2), the residue row carries
`（report-recognition-uncertain：残留 1）`, overview exit 0.

## S-7 — Closed sets and single entry (route b)

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_team_view_degradation_contract.py -q -k "single_recognition or reason_set or exit_mapping or label_closure or three_surfaces"
```
exit 0 — `5 passed in 6.83s`. One `classify_runs` definition / one compiled timestamp
grammar; reason ids == `{engine-degraded, report-recognition-uncertain}`; exit mapping 2/2
plus missing/empty-only at exit 0; label constants close against the owner tables both
ways; the three surfaces each name both ids and cite the owner contract.

**Name correspondence (disclosed, not silent)**: quickstart S-7's parenthetical lists
`test_label_constants_match_the_owner_table`; the tasks.md Clause Coverage table — the
implement-stage owner of the pinning-test names — pins C-401 on
`test_label_closure_both_directions`, which is the node executed above and covers exactly
that subject. The plan-owned quickstart is left unedited (no PLAN-EDIT needed: the name is
a pointer, and the tasks-stage table is authoritative for the node id).

## Teardown

- Route-b fixtures live under pytest `tmp_path` and are removed by pytest at process exit;
  no fixture was written under the repository's `.specify/teams/`.
- Route-a S-0 invocations are read-only by contract (`side-effects: none`); the only
  scratch written by this run is the capture file under the sanctioned temp root
  `.specify/.tmp/sdd-loop/tmp/team-view-degradation/`.
- No background process, no network, no container runtime was used.

## Cross-references

- Guard detail and US3 green readings: `notes/us3-green.txt`, `test-evidence/us3-guards.txt`.
- Red-first captures: `test-evidence/us1-red-unit.txt`, `us1-red-integration.txt`,
  `us2-red-degraded.txt`, `us2-red-states.txt`, `us3-red-contract.txt`.
