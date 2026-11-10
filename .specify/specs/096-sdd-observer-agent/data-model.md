# Data Model — 096-sdd-observer-agent

Every entity below is a projection of the requirements' Key Entities section; field spellings that a program consumes are owned by `shared/declarations/facts/journal-format.yaml` (journal side) or by the owning document named per row. This page owns the information face and the validation rules.

## E-1 — Observer Template（观察者角色模板）

| Field | Value / rule |
|-------|--------------|
| Form | Agent Template (layer 1), shipped source `agents/sdd-observer.agent.md`, mirror `.specify/agents/templates/sdd-observer.agent.md` |
| Frontmatter | `name`, `description`, `user-invocable: false`, `disable-model-invocation: false`, `supervisor: false`, `model-tier: auto`, `capability-tools: [Read, Grep, Glob, Bash]`, `skills: []`, `run-turn-budget: 500` |
| Role face | `observer` — third-party, observation-only; declared explicitly (FR-002) |
| Read domain | disk carriers and repository facts only: state spine, stage logs and completion sentinels, checkpoint files, git history, the driver positive-evidence quartet (`pid-*` / `status-*` / `log-*.log` / `heartbeat-*.log`), execution records. Driver conversation and stage prompts are NOT observation input (FR-013) |
| Write surface | exactly journal (through the engine) + own execution artifacts under the existing `.specify/agents/execution/logs/` layout (FR-016) |
| Forbidden | evaluation, suggestion, causal inference, severity/recommendation (the definition text carries 「不评价、不建议、不推断」 verbatim, SC-004); loading or referencing the driver/loop skill; hosting or starting an SDD run; user-visible reports/questions/approval requests |
| Internal subagents | MAY be used for observation duties; serial only; never a concurrency carrier (host in-process concurrency BANNED); they inherit the read domain, write surface and objectivity structure (FR-022) |
| Dispatch clause | byte-identical copy of the fast-fail injection block (owner literal `shared/guidelines/fast-fail.md` § 子代理派发注入) |

## E-2 — Observer Instance（专用观察实例）

| Field | Value / rule |
|-------|--------------|
| Layer | Agent Instance (layer 2), `.specify/agents/instances/sdd-observer-<line_id>.agent.md` in the client project (never shipped) |
| Identity | `line_id` + spec key (FR-004); one instance per line; never shared across lines |
| Created by | the driver's startup step through the existing `create-agent` delegation; no stage command creates it (FR-003) |
| Reuse | many executions per instance; `run_id` is line-scoped and does not distinguish instances |
| Duty | observe line `<line_id>` / spec `<spec>`; derive journal path, spine path, state dir, read domain |

## E-3 — Observer Execution（观察执行）

| Field | Value / rule |
|-------|--------------|
| Layer | Agent Execution (layer 3); external mode only — fork carrier (`stage-runner.sh`, same-family `qodercli`) or subprocess carrier (heterogeneous CLI). native/virtual MUST NOT carry it (FR-006) |
| Label | `<line_id>--<run_stamp>--observer`, the existing three-segment convention (`shared/definitions/subagent-definitions.md` § External Dispatch Visibility Contract point 5) |
| Window | bounded by the existing dispatch turn budget and stage deadline; no new timer, scheduler or daemon (FR-007, FR-008) |
| Cardinality | at most one unsettled execution per line; the driver serializes (`status` record unsettled → no next dispatch) and the engine's single-writer flock refuses a second writer (FR-007) |
| States | `started` → `settled` \| `failed`; recorded in the state spine observer record section (E-9), never in the journal as its own failure record |
| Artifacts | the visibility triplet `<label>.live.log` / `<label>.jsonl` / `<label>.status` under the existing execution log layout |
| Restart | MAY restart from the same instance at the next stage boundary after a failed/expired window; restart appends to the same journal and the engine writes one `observer-gap` for the uncovered window (FR-008) |

State machine:

```text
(no execution) --start--> started --window-end/settle--> settled
                              \--error/kill--> failed --next stage boundary--> started (same instance)
line terminal: final execution --append --final--> line-terminal + observer-settle; spine state=closed
```

## E-4 — Journal（观察记录文件）

| Field | Value / rule |
|-------|--------------|
| Path | `.specify/specs/<NNN-slug>/journal.md` (STR-001), one file per line |
| Title | `# SDD Journal — <spec-key>` |
| Header keys | `line_id`, `run_id`, `spec`, `observer_instance`, `created_at` (UTC ISO-8601 seconds) — written once by the engine |
| Body | exactly one markdown table with the nine entry columns in the fixed order of E-5 |
| Write mode | append-only rows; no existing row is rewritten or deleted; appended by the engine only |
| Commit | may be swept into intermediate stage commits; the closing commit carries the final entries (FR-010) |
| Failure | if the journal cannot be written, the failure evidence lands in the execution's `.status` record and the spine observer record section; the journal is never its own failure record |

## E-5 — Journal Entry（记录条目）

Nine fields, in this order (spellings owned by `journal-format`):

| # | Field | Domain |
|---|-------|--------|
| 1 | `seq` | integer, engine-assigned, starts at 1, strictly +1 in file order |
| 2 | `observed_at` | engine clock, UTC ISO-8601 seconds (`YYYY-MM-DDTHH:MM:SSZ`) |
| 3 | `event_at` | carrier-provided time or `-`; for `observer-gap` it is the gap window **start** |
| 4 | `stage` | a stage name from the declared stage sequence, or `-` for line-level and observer events |
| 5 | `event` | one literal of the closed event-class set (E-6) |
| 6 | `command` | literal command text or `-` |
| 7 | `artifact` | repo-relative path or `-` |
| 8 | `exit` | integer or `-` |
| 9 | `evidence` | one or more evidence pointers separated by `; ` (E-7); at least one |

No field carries evaluation, suggestion, causal inference, severity or recommendation. Values escape `|` as `\|` and newlines as a single space.

## E-6 — Event Class（事件类，closed）

| Event | Meaning | Primary carrier | `min_persistent` |
|-------|---------|-----------------|------------------|
| `line-start` | the line began | state spine U0 block (first append only) | 1 |
| `line-terminal` | the line reached its terminal stage boundary (`--final`) | state spine observer record | 1 |
| `stage-start` | a stage dispatch started | `pid-<line>-<stage>` envelope `at=` | 0 |
| `stage-end` | a stage execution ended | `status-<line>-<stage>` envelope `at=` / `exit=` | 0 |
| `stage-verdict` | the completion evidence of a stage (sentinel + exit record) was observed | `status-*` + last non-empty line of `log-*.log` | 0 |
| `checkpoint` | a checkpoint file appeared | `checkpoints/<NN>-<stage>.md` | 1 |
| `commit` | a git commit appeared | `git log` over the observation window | 1 |
| `anomaly` | the stage log's last `ANOMALY:` line, even when a completion sentinel follows it | `log-*.log` (+ `status-*` if present) | 0 |
| `stall` | the spine records a stalled line | state spine `卡死状态: stalled` | 1 |
| `retry` | the same stage started a new attempt (new pid `start` token) | the two `pid-*` envelopes | 0 |
| `dispatch` | a dispatch meta file appeared | `prompt-<line>-<stage>.md.meta.json` | 0 |
| `artifact-write` | a commit touched paths under the spec directory (excluding `journal.md`, `checkpoints/`) | `git log --name-only` | 1 |
| `observer-start` | an observer execution's first append | state spine observer record + triplet `.status` if present | 1 |
| `observer-settle` | an observer execution settled (`--settle` / `--final`) | state spine observer record | 1 |
| `observer-gap` | an uncovered window between executions | state spine observer record + previous entry | 1 |
| `observer-error` | an observation pass could not read a carrier | the carrier path (runtime pointer) | 0 |

The set is closed; growth is a revision of `journal-format.yaml`, never an inline invention (FR-012).

## E-7 — Evidence Pointer（证据指针）

Grammar: `<retention>:<kind>:<target>[#<anchor>]`

- `retention` ∈ `persistent` | `runtime`
- `kind` ∈ `spine` | `log` | `status` | `pid` | `heartbeat` | `meta` | `checkpoint` | `artifact` | `commit` | `triplet`
- `target` = repo-relative path; for `kind=commit` the target is a commit hash
- `anchor` = a section heading expected in the target file (optional)

Rules: persistent pointers MUST resolve at line closeout (path exists, or commit resolves through `git cat-file -e`); runtime pointers are marked and are never the sole evidence of a fact that has a persistent carrier (FR-014). A pointer to a cleaned-up runtime file stays valid as a marked runtime pointer.

## E-8 — Observer Gap（观察缺口）

| Field | Rule |
|-------|------|
| Window start | the previous entry's `observed_at`; with no entries, the spine observer record section's `started_at` |
| Window end | the current execution's first entry `observed_at` |
| Encoding | one `observer-gap` row: `event_at` = window start, `observed_at` = window end, `evidence` = spine pointer (+ previous entry's evidence if any) |
| Never | inferred events filling the window (FR-013) |

## E-9 — State Spine Observer Record Section（状态脊观察者记录节）

Append-only sections written by the driver, never by the observer (FR-004, FR-016):

```text
## Observer Record — <YYYY-MM-DDTHH:MM:SSZ>
- state: started | failed | disabled | closed
- line_id: <value>
- run_id: <value>
- spec: <NNN-slug>
- instance: <instance slug>
- execution_label: <label or ->
- started_at: <UTC ISO-8601 or ->
- reason: <one line or ->
```

Reading rule: the latest section wins for current state; every section is retained. `state=disabled` comes from the entry switch `observer: off`; `state=failed` carries the reason; `state=closed` is written by the driver after the final observer execution settles (or after it fails, with the reason).

## E-10 — Carrier Fact（载体事实）

Closed observation-input list (FR-013): state spine (E-9 section + the two narrow stage grammars), stage logs and completion sentinels, checkpoint files, git history, the driver positive-evidence quartet and its envelopes, execution records (triplet, meta). Driver conversation and stage prompt bodies are excluded by rule, not by scanning.

## Validation Rules

- **V-1** Journal header carries exactly the five keys; `created_at` is UTC ISO-8601 seconds.
- **V-2** The body contains exactly one table whose header row is the nine column names in order.
- **V-3** `seq` starts at 1 and increments by exactly 1 in file order; a gap or duplicate is a finding.
- **V-4** `observed_at` matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`; `event_at` is `-` or the same form.
- **V-5** `event` is one literal of E-6; any other literal is a finding.
- **V-6** `stage` is `-` or a stage from `shared/declarations/facts/driver-stage-sequence.yaml#/statement`.
- **V-7** `exit` is `-` or an integer.
- **V-8** `evidence` parses as one or more E-7 pointers; retention and kind are in the closed sets.
- **V-9** Each entry carries at least one pointer; entries whose event class declares `min_persistent: 1` carry at least one persistent pointer.
- **V-10** Every persistent path pointer resolves relative to the repository root; every commit pointer resolves via `git cat-file -e`.
- **V-11** No column outside the nine exists; a tenth column (e.g. `recommendation`) is a finding.
- **V-12** A non-table narrative paragraph inside the journal body is a finding (free narrative is not an entry).
- **V-13** Rows are never rewritten: a checker run never mutates the journal; the engine opens the file for append only.
- **V-14** The engine refuses a second concurrent writer with exit 3 and appends nothing.
- **V-15** The observer record section parses with the fixed key set; unknown keys are a spine-side finding, not a journal one.
- **V-16** An observer execution whose label does not match the latest spine record's `execution_label` is refused (exit 2) — a foreign or stale execution cannot append. Append-time rule, enforced by `journal-engine.contract.md` C-07; `check` does not evaluate it (C-09).
- **V-17** `observer-gap` exists whenever a new execution's `started_at` is later than the last entry's `observed_at`; its window is [last `observed_at`, new execution's first `observed_at`].
- **V-18** The observer writes nothing except the journal and its own execution artifacts: the template declares exactly that surface and the driver text forbids observer spine writes.
- **V-19** Each line has its own journal path derived from its spec key; two parallel lines' journals never share a path (fixture proves it).
- **V-20** Deprecated or removed event classes and pointer kinds are a format-owner revision, never a silent acceptance: the checker reads the closed sets from `journal-format.yaml`, not from constants.
