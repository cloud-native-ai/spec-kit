# Pre-change measurements — 095-superagent-role

Captured **2026-11-10** at task generation (RUN `r20261110T065604Z-b095`, HEAD `2c8da54c0`). These are
frozen measurements: re-capture at implement start per `/speckit.implement`'s baseline pre-flight
(never cached), and a row whose re-capture yields a different value carries the new value — never the
stale frozen one.

## 1. Instruction budget (premise EP-005 / A13)

| Measurement | Command | Value |
|---|---|---|
| Live instructions size | `wc -c .specify/instructions.md` | **37,454 B** |
| Template size | `wc -c templates/instructions-template.md` | **32,975 B** |
| Budget constant | `grep -n 'INSTRUCTIONS_BUDGET_BYTES' scripts/bash/generate-instructions.sh` | line **107**: `INSTRUCTIONS_BUDGET_BYTES=38400` |
| Arithmetic headroom | `38400 - 37454` | **946 B** |

Trap form: the generator's `over` verdict fires at `size >= budget`, so the last admissible byte is
`budget - 1 = 38,399`; `tests/contract/test_instructions_size_budget.py::test_c17_...` states this
arithmetic (`size <= budget - 1`). A 946 B section would be over; the useful headroom is 945 B.

## 2. Mirror drift baseline (plan § Mirror Obligations)

Command: `python3 scripts/python/sync-mirrors.py --check` (2026-11-10, this tree).

- Total output lines: **437** — naive `wc -l` reads 437.
- **DIFF-class lines: 428** = 422 `DIFF` + 6 `DIFF[projected]` — this matches the plan's recorded
  428-line baseline; the criterion stays “no NEW drift on the pairs this spec touches”.
- Remaining lines: 1 `DRIFT`, 1 `ok`, 3 `projected[bash-version-guard]`, 3
  `projected[python-version-bridge]`, 1 blank.

Trap form: quoting 437 as “the baseline” overstates it by the non-DIFF projection/`ok` lines; quoting
428 is the plan-comparable reading.

## 3. Slice inventory for the 080–094 observation appendix (FR-038)

Command: `ls .specify/specs/ | grep -E '^0(8|9)[0-9]' | sort` → 15 lines:
`080, 081, 082, 083, 084, 085, 086, 087, 088, 089, 090, 091, 093, 094, 095`.

- Slices **080–094 actually present: 14** (080–091, 093, 094).
- **092 does not exist** on this tree.
- Trap form: the arithmetic reading “080..094 = 15 slices” is wrong here, and including 095 in the
  enumeration also yields 15. The appendix enumerates the 14 present slices, never an assumed range.

## 4. Per-Agent Payload table row count (constrains the `role_fields` addition)

Command: read the `Per-Agent Payload:` block in `skills/internal/create-team/references/patterns.md`
and count `^\| \`([a-z_]+)\` \|` rows.

- Current rows: **7** — `task_brief`, `territory`, `forbidden_files`, `output_convention`,
  `incremental_landing`, `model_hint`, `fast_fail_clause`.
- `tests/contract/test_fast_fail_discipline.py::test_i13_channel_three_payload_sixth_field_row`
  hard-codes `len(rows) == 7` (the count itself is the contract).
- Consequence: adding `role_fields` makes 8; the same task that adds the row MUST update that
  assertion to 8 (pin hygiene — a count that is the contract is updated in the same task that changes
  the population).

## 5. Digest CLI surface (constrains the role view; do not confuse with the new engine)

- `scripts/python/status-digest.py`: `--action {digest,guard,report}`; `--format {table,json}`;
  `NOTHING_RUNNING = "nothing-running"` (exit 3); per-row `stale` + `omitted` semantics unchanged.
- `--format text` is **retired** for `status-digest.py` (existing test asserts exit 2).
- Trap form: the **new** `role-edge-check.py` contract specifies `--format json|text` — that is a
  different script; the digest's `table|json` vocabulary is not changed by this feature.

## 6. Template anchors for the new instructions section

Command: `grep -n '^## Spec Kit Framework Map\|^## Spec Kit Runtime & Symlink Model' templates/instructions-template.md .specify/instructions.md`

- `templates/instructions-template.md`: Framework Map at line **266**, Runtime & Symlink Model at
  line **272**.
- `.specify/instructions.md`: Framework Map at line **283**, Runtime & Symlink Model at line **289**.
- The new `## Super Agent (相对逻辑角色)` section lands between the two anchors in the template; the
  live file is produced only by `bash scripts/bash/generate-instructions.sh`.

## 7. Path existence (creation targets are new; tooling is present)

| Path | Reading |
|---|---|
| `scripts/python/role-edge-check.py` | **absent** (new file) |
| `tests/fixtures/superagent-role/` | **absent** (new directory set) |
| `scripts/bash/run-tests.sh` | present (single test entry) |
| `.specify/scripts/python/validate-tasks.py` | present |
| `.specify/scripts/python/script-interface-check.py` | present — repo-wide checker: `--files <path[,path]>`; a positional file is rejected (exit 2) |
| `.specify/scripts/python/account-clause-coverage.py` | present |
| `scripts/python/sync-mirrors.py` | present; `--only` takes an exact repo-relative source path prefix |

## 8. Carrier roots the engine reads (premise EP-003)

| Carrier | Reading (2026-11-10) |
|---|---|
| `.specify/state/` | present — spine files plus four-piece artifacts `pid-`/`status-`/`log-`/`heartbeat-<line>-<stage>` |
| `.specify/teams/` | present — 20 team directories, each with `runs/<stamp>-report.md` |
| `.specify/agents/execution/logs/` | present (currently no files; directory exists) |
| `~/.local/state/spec-kit/lines/*.json` | present — line-registry entries with `line_id` / `run_id` / `parent_line_id` / `line_role` |

## 9. Existing tests that constrain the edits (FR-036 disposition inputs)

| Module | Constraint |
|---|---|
| `tests/contract/test_fast_fail_discipline.py` | `test_i13` pins the Per-Agent Payload table at **7** rows (see §4); `test_i14` pins the Context Isolation Rules after the table; `RUN_AGENT_SKILL` assert only requires the Run Mode section to point at the discipline doc |
| `tests/contract/test_status_digest.py` | the table render must keep naming its six reader columns (线路/状态/阶段/已静默/标记/最近步骤与消耗); JSON key sets are not pinned, so additive fields are safe |
| `tests/contract/test_instructions_section_propagation.py` | the live file must carry every template section → the generator must run after the template edit |
| `tests/contract/test_instructions_size_budget.py` | live size must stay `<= budget - 1` (derived from the script, no literal) |
| `tests/contract/test_nested_run_report.py` | the team report's top-level section list is pinned → the dispatch mapping table must land **inside** `## Execution Detail` |
| `tests/contract/test_agent_dispatch_mechanism.py` | `test_c3_no_third_owner_of_three_layers` forbids the literal marker `Agent Template → Agent Instance → Agent Execution` in any other `shared/definitions/*.md` → the new owner page must not repeat that literal |

## 10. Contract / coverage baseline

- The four contracts use the `md-heading` clause form (`## C-N. …`), resolvable by
  `clause_extract.py` (`HEADING_RE`).
- Coverage baseline frozen at this tasks run: `.specify/specs/095-superagent-role/coverage-baseline.txt`
  — 642 lines, `base-sha: 2c8da54c06e7`, `files: 286 (parsed 179 + named 107)`.

## 11. Runtime & registry facts

- `python3 --version` → **Python 3.11.11**; `pyproject.toml` `requires-python = ">=3.8"`.
- `.specify/glossary.md:194` already carries the `Super Agent` term row (`auto` / `proposed`); the
  definition owner lands at `shared/definitions/superagent-definitions.md`.
- `better-harness.md` is **not** modified (clarify Q6 ruling; it is the improvement north star, not a
  role owner). The plan brief's “better-harness.md 增加指针” line was superseded by that ruling.
- Flow class for this spec: `flow_class: execution` / `source: declaration` (lookup exit 0).
