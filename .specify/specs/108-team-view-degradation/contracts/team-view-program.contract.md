# Contract — `team-view.py` Program (108 amendment)

**Path**: `scripts/python/team-view.py` (source), `.specify/scripts/python/team-view.py` (regenerated mirror)
**Pinning tests**: `tests/contract/test_team_view_degradation_contract.py` (reason set, exit map, envelope keys, single entry, three-surface consistency), `tests/integration/test_team_view_degradation.py` (healthy fidelity, degraded rendering, snapshot), plus the inherited `tests/contract/test_team_view_program_contract.py` (CLI surface, closed exit set, read-only scan).
**Supersession**: this file is the live program contract for the amended reader. It supersedes `.specify/specs/103-team-view/contracts/team-view-program.contract.md` on four points — the exit-5 trigger surface, the state-vocabulary owner (which moves to `view-labels.contract.md`), report ordering and report bounds, and the normalized latest value. The 103 file is untouched and remains a dated record; no surface may cite it as the live owner after this feature lands.
**Rule owners cited, never restated**: `shared/definitions/script-interface-definitions.md`; `skills/internal/create-team/SKILL.md` § Report contract; `shared/definitions/anchor-definitions.md` § The Binding Record.

**C-101** Read-only program.

`team-view.py` MUST NOT write any file, create any directory, register any run line, dispatch any seat, reach the network, or invoke any `goal-utils.py` action other than the three declared reads (`binding team <slug>`, `list`, `targets <anchor-slug> --list`). A view MUST leave the working tree byte-identical. (FR-021, FR-025)

**C-102** One engine, one recognition entry.

The program MUST contain exactly one runs classifier (`classify_runs`) and exactly one compiled timestamp grammar; the single-team view and the overview MUST both obtain report classification, the latest selection and the normalized token through that one function. A second matching rule, a second latest-selection routine, or a second reader MUST NOT exist in the source tree. (FR-006, FR-021)

**C-103** Closed CLI surface (unchanged).

The declared options remain `--repo-root`, `--scope`, `--spec-dir`, `--json`, `-h`/`--help`, `--version`; `--target` stays undeclared and is refused with exit 2; no option is added by this feature. (FR-021)

**C-104** Closed exit codes and degradation reasons.

The exit-code set stays exactly `0 / 2 / 3 / 4 / 5`. Exit `5` means "rendering produced, but a required fact group is unreadable or the latest run is undeterminable". The degradation reason set is exactly `{engine-degraded, report-recognition-uncertain}`; `engine-degraded` is emitted only when an engine read (`binding` / anchor facts through `list` + `targets --list`) fails to produce the fact, `report-recognition-uncertain` only when a readable `runs/` directory holds at least one residue file. Every active reason MUST be named individually in the output; reasons may coexist; every reason maps to exit `5`. File-level states (`缺失` / `为空` / `不可读` / `未记录`) are not reasons and MUST NOT change the exit code by themselves; an unreadable latest report is the FR-009 presentation state, not a reason. (FR-017, FR-018)

**C-105** Envelope shape (no new top-level key).

The `--json` envelope keeps its existing ten top-level keys. Degradation reasons ride the existing `errors[]` array with `code` values from C-104; `degraded` is `true` if and only if at least one reason is active; `as_of.latest_report_timestamp` carries the normalized token (`YYYYMMDDThhmmssZ`) or `null`. Additions are nested fields only and MUST NOT remove or rename an existing field. (FR-002, FR-017, FR-019)

**C-106** Script interface.

The program belongs to the required set of `shared/definitions/script-interface-definitions.md` and keeps its current behaviour: `-h` / `--help` / `--version` exit 0 with zero writes before any action; an undeclared option exits 2 with a recognizable error. (FR-021)

**C-107** Healthy fidelity (closed claim).

The healthy predicate is owned by FR-022; this clause is its test-facing projection and MUST stay item-for-item identical to it. A fixture satisfies the predicate only when **all** of the following hold: (1) the engine binding read succeeds with all three keys (`owner` / `owner_id` / `origin`); (2) every file under `runs/` is a run report — zero auxiliary artifacts, zero residue — named compact `<YYYYMMDD>T<hhmmss>Z-report.md` and readable; (3) the `## Static Structure` matrix carries the `agent` column; (4) the `goal` key is absent, or its value passes the shared identity grammar (`shared/definitions/goal-definitions.md` § Identity grammar) — a slug-form `goal` is a healthy declaration, adds no state line (C-302) and MUST NOT be treated as a defect; (5) `items.jsonl` exists, is readable and carries at least one line (the folded `已聚合` rendering C-304 does not change); (6) all three continuous-spine files (`constraints.md` / `STATE.md` / `run-log.jsonl`) are present, so no spine-applicability form (C-305) triggers. On a fixture satisfying the predicate, the program of baseline commit `54c6efa8c` and the amended program MUST produce byte-identical stdout and the same exit code (machine diff). **The allowed-delta set is empty for predicate-satisfying inputs only**: inputs that fail any predicate condition are degraded inputs outside this claim and carry the named correction increments of A-11 (the C-205 auxiliary line, the C-301…C-307 states), so a byte-fidelity test MUST build a fixture satisfying every condition — a fixture missing the ledger, the spine or the goal condition, or carrying auxiliary artifacts, is not a healthy fixture and MUST NOT be used to claim the empty set. (FR-022)

**C-108** No shape change; migration or refusal for any future one.

This feature changes neither the report-naming owner (`skills/internal/create-team/SKILL.md` § Report contract) nor the `team.md` schema; no team definition is rewritten and no team migration is required. Every name that conformed before MUST remain a run report. Any proposal to change the recognized shape further MUST ship a migration or a deterministic refusal in the same change, otherwise it MUST NOT be merged. (FR-023)

**C-109** Three-surface consistency (pointer-shaped).

The exit codes and degradation reasons MUST agree across three surfaces: the View Mode section of `docs/reference/commands/team.md`, the error-navigation table of `skills/internal/view-team/SKILL.md`, and the program's own declaration (`--help`, module documentation). Each surface MUST name both reason ids (`engine-degraded`, `report-recognition-uncertain`) and cite this contract as the owner of the closed set and mapping; no surface restates a second definition. The agreement MUST be asserted by a test. (FR-020)
