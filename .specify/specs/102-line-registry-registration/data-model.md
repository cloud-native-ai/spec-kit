# Data Model — 102-line-registry-registration

**Scope**: the shapes this feature reads or produces. The Line Registry schema is **owned by the engine** (`skills/external/sdd-loop-driver/scripts/line-registry.py`); this document records the projection this feature consumes and produces, never a second definition. Mechanical criterion members are referenced through `requirements.md` § Shared Strings (`[[STR-NNN]]`); their executable owner is the scanner module constant set (A-15).

## E1 — Registry entry (consumed, engine-owned)

| Field | Type / domain | This feature's use |
|-------|---------------|--------------------|
| `line_id` | string, `LINE_ID_RE` | identity; the wrapper's composed id (E2) |
| `run_id` | string, `RUN_ID_RE` | the run this line belongs to (A-18) |
| `project_dir`, `repo_root` | absolute paths | the digest matches entries by these two fields |
| `state` | engine's closed set | wrapper writes `active` at registration; close lands `closed` |
| `last_event` | string | `registered` at register; `<reason>` at close; run-team step label on `update` |
| `created_at`, `updated_at`, `closed_at` | ISO-8601 Z | evidence of the two-event lifecycle |
| `run_history` | list of `{run_id, started_at, ended_at, outcome}` | close appends one entry whose `outcome` is the close reason |

Validation rules: none are added by this feature. The engine validates ids, states and reasons; a rejected value is surfaced, never repaired.

## E2 — Composed line id

- **Form**: `<line-id>-<run-id>` (e.g. `batch-apply-r20261116T090000Z-a001`).
- **Validation**: the engine's own `LINE_ID_RE` / `RUN_ID_RE` (engine source lines 42-43) decide; the wrapper validates neither. The grammars are the engine's, referenced by constant name, not restated here.
- **Run-id generation**: `r<UTC yyyymmdd>T<UTC hhmmss>Z-<4 lowercase hex>` (e.g. `r20261116T090000Z-a001`, A-18); it must match the engine's `RUN_ID_RE`. A bare UTC timestamp is not a run id.
- **Uniqueness**: each run yields a new id; a retried run id equals a repeated registration and fails closed on the engine's `line already exists` — never overwrite, never delete.
- **Consumers**: the wrapper (creates and closes), run-team §7 (records it in the report body), tests (read the entry by this id).

## E3 — Wrapper invocation

| Element | Definition |
|---------|------------|
| Inputs | `--line-id <slug>`, `--run-id <id>`, `--`, then the command and its arguments |
| Identity | `git rev-parse --show-toplevel` from the caller's cwd → both `--project-dir` and `--repo-root` (the toplevel, never `$PWD`) |
| Engine | first readable of the two A-17 candidates, resolved from the wrapper's own path |
| Events | exactly two: register (`registered`) and deregister (reason from `[[STR-008]]`) |
| Streams | the child owns stdout/stderr; engine payloads go to stderr on failure only |

**Phase state machine**

```text
S0 parse ──usage error──▶ exit 2 (command not executed)
  │ ok
  ▼
S1 identity ──no git toplevel / no readable engine──▶ exit 4 (command not executed)
  │ ok
  ▼
S2 register ──engine non-zero──▶ exit <engine status> (command not executed)
  │ ok
  ▼
S3 execute child ──▶ capture status (never rewritten)
  │
  ▼
S4 close ──ok──▶ exit <child status>   (0 on success)
          └─failed─▶ child 0  → exit <engine status>, stderr carries payload
                     child ≠0 → exit <child status>, stderr carries payload
```

Invariants: S2 always precedes S3; S4 always follows a started S3; a killed wrapper performs no S4 (entry stays `active`).

## E4 — Scan root

| Field | Rule |
|-------|------|
| Path | repository-relative or absolute; must resolve to a directory **inside** the repository root |
| Existence | absent or not a directory → input error (exit 2) naming the root |
| Default set | `DEFAULT_SCAN_ROOTS` (A-21); `--root` is repeatable and **replaces** the defaults for that invocation |
| Forbidden | runtime directories (e.g. `.specify/teams/.work/`) may be used only as an explicit fixture root, never as the declared default set |

## E5 — Judged file

A file enters judgement iff **all** hold: it is a regular file (symlinks skipped, never followed), it lies under a scan root without escaping the repository root, and it has a `.sh` / `.bash` / `.py` suffix **or** a `#!` first line. The scanner's own resolved path is skipped and counted as `owner-skipped`.

## E6 — Long-task criterion (constant-owned)

| Constant | Role | Member literals |
|----------|------|-----------------|
| `LONG_TASK_MARKERS` | content strings that make a file a long task | `[[STR-004]]`, `[[STR-005]]` |
| `SELF_DECLARATION_MARKER` | a standalone comment line (first non-whitespace character `#`) whose text contains the literal, case-sensitive | `[[STR-003]]` |
| `COMPLIANT_INVOCATIONS` | invocation forms that discharge the registration duty | wrapper form (`[[STR-001]]`); engine `register` / `update` / `deregister` (`[[STR-002]]`) |
| `DEFAULT_SCAN_ROOTS` | the declared live roots | members owned by the constant; the set is the one A-21 declares |

The four constants are the only machine-readable owner; this table names them and points at the literal owner, it does not define a second set.

## E7 — Finding

| Field | Meaning |
|-------|---------|
| `path` | repository-relative path of the judged file |
| `line` | 1-based line of the first hit (content marker or self-declaration) |
| `criterion` | `content-marker` or `self-declaration` |
| `matched` | the marker text as it appeared (for diagnosis) |

One finding per judged file (the first hit is enough to fail the file); the scanner reports every violating file.

## E8 — Scanner reading

| Field | Meaning |
|-------|---------|
| `roots` | the resolved root list in use (printed, never inferred by the reader) |
| `files` | number of judged files |
| `violations` | number of files reported |
| `owner-skipped` | 1 when the scanner's own path was in scope, else 0 |

Exit status is part of the reading: `0` clean, `1` at least one violation, `2` input error. A missing root never yields a clean reading.

## Invariants

- **INV-01**: registry writes flow only through `[[STR-002]]`; `scripts/python/journal-utils.py` is never called by this feature.
- **INV-02**: `closed` is terminal; nothing in this feature reopens or deletes an entry.
- **INV-03**: a failed registration never starts the wrapped command.
- **INV-04**: the wrapper never rewrites the child's exit status (A-24's priority is about *which* status wins, not about altering it).
- **INV-05**: the wrapper can observe only the child process; it claims no visibility of work the child hands off and returns from (A-13).
- **INV-06**: exactly two engine events from the wrapper; no timer, daemon, heartbeat file or second channel (A-19).
- **INV-07**: the scanner writes nothing, spawns nothing and reaches no network.
- **INV-08**: the scanner's owner file is skipped by resolved path and named in the reading; it is never counted as clean evidence.
- **INV-09**: the live reading is zero violations on the declared roots; a missing root is an input error, never a clean zero.
- **INV-10**: the digest contract is untouched: `status-digest.py` keeps its action set, exit codes and `[[STR-006]]` rendering.
- **INV-11**: `templates/instructions-template.md` is the only authored surface for the ambient bullet; the live file and symlinks are refreshed, never hand-edited.
- **INV-12**: no new third-party dependency, registry, status spine or ledger (§ 十一 prohibition).
