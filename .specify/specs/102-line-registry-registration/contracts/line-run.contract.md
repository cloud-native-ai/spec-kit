# Contract — `line-run.sh` (long-task registration wrapper)

**Subject**: `scripts/bash/line-run.sh` (framework source; mirror `.specify/scripts/bash/line-run.sh`, generated — never hand-edited).
**Owners**: wrapper semantics are owned here; the registry schema, id grammars, state set and reasons are owned by `skills/external/sdd-loop-driver/scripts/line-registry.py`; the registration criterion is owned by `shared/guidelines/reporting-obligations.md` § 九. Shared literals are referenced as `[[STR-NNN]]` and owned by `requirements.md` § Shared Strings.

## C-01 — Surface

The script accepts exactly these options before a mandatory `--`:

| Option | Value | Required | Meaning |
|--------|-------|----------|---------|
| `--line-id` | slug | yes | human-facing line identity |
| `--run-id` | engine run id | yes | this run's identity |
| `-h`, `--help` | — | — | print usage, exit 0 |
| `--version` | — | — | print `<script-name> <framework-version>`, exit 0 |

C-02 The value of an option is the **next argument**; the `--opt=value` form MUST be rejected as an undeclared token.
C-03 A bare `--` is mandatory and separates the wrapper's options from the command. Tokens after `--` belong to the wrapped command, including `-h`.
C-04 An undeclared option, a missing option value, a missing `--`, or an empty command MUST exit `2` without starting the command.

## C-05 — Zero side effects when answering

`-h`, `--help` and `--version` MUST print and exit `0` before any registry read, registry write, git probe or child launch. A flag present anywhere before `--` wins over every action option.

## C-06 — Identity

The project identity MUST be `git rev-parse --show-toplevel` run from the caller's working directory — an absolute path passed to the engine as both `--project-dir` and `--repo-root`. The toplevel result, never `$PWD` itself, is the identity. A failing `git` probe MUST fail registration (C-09/C-18) and MUST NOT start the command.

## C-07 — Engine resolution

The engine MUST be the first readable of, in order:

1. `<repo-root>/skills/external/sdd-loop-driver/scripts/line-registry.py`
2. `<repo-root>/.specify/skills/sdd-loop-driver/scripts/line-registry.py`

where `<repo-root>` is the wrapper's own `../..`, moved up one level when that directory is named `.specify`. When neither is readable the wrapper MUST report both candidate paths and fail registration. The wrapper MUST NOT use `.specify/scripts/line-registry.py`, `PATH` lookup, or any new environment variable.

## C-08 — Registration

Before the command starts, the wrapper MUST invoke `[[STR-002]] --action register` with `--line-id "<line-id>-<run-id>"`, `--run-id "<run-id>"`, the identity from C-06 and state `active`. The wrapper MUST NOT apply its own id grammar; the engine validates and its refusal is surfaced.

C-09 Registration failure MUST be fail-closed: the command MUST NOT be executed and the wrapper MUST exit non-zero, naming the failed step and echoing the engine payload on stderr.

## C-10 — Execution

The command after `--` MUST run as a child of the wrapper, inheriting stdin, stdout, stderr, cwd and environment. The wrapper MUST NOT parse, quote or rewrite the command's arguments.

## C-11 — Close

After the child returns, the wrapper MUST invoke `[[STR-002]] --action deregister --line-id "<composed id>" --reason completed` when the child status is `0`, and `--reason failed` otherwise. `[[STR-008]]` is the closed reason set; no other reason is written by the wrapper.

C-12 The wrapper MUST emit no engine event other than the registration of C-08 and the close of C-11. It MUST NOT refresh intermediate events, and MUST NOT create a heartbeat file, timer or second channel.

## C-13 — Exit status

| Situation | Wrapper exit |
|-----------|--------------|
| child `0`, close ok | `0` |
| child `N ≠ 0`, close ok or failed | `N` |
| child `0`, close failed | the engine's non-zero status |
| usage error (C-04) | `2` |
| no git toplevel or no readable engine | `4` |
| registration refused by the engine | the engine's non-zero status |

C-14 The child's status MUST NOT be rewritten or masked. When close fails while the child is non-zero, the close failure (engine payload plus engine status) MUST be written to stderr.
C-15 Engine payloads MUST never be written to stdout; stdout belongs to the child.

## C-16 — Signals and residue

A child terminated by a signal surfaces as its non-zero shell status and is closed with `failed`. A wrapper killed by an uncatchable signal (e.g. `SIGKILL`) MUST leave the entry `active` — not deleted, not rewritten to `closed`. No cleanup, staleness threshold or deletion is added by the wrapper.

## C-17 — Registry location

The wrapper MUST pass the registry location decision to the engine unchanged: `$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`. The wrapper MUST NOT introduce a registry-root override variable of its own.

C-18 Re-entry: an existing composed id is a registration failure surfaced from the engine (`line already exists`). The wrapper MUST NOT overwrite, delete or reuse the existing entry; nested wrappers register their own ids.

## C-19 — Scope

The wrapper MUST NOT use `scripts/python/journal-utils.py`, MUST NOT write JSON itself, MUST NOT read digest state, MUST NOT spawn auxiliary processes beyond `git` and the engine, and MUST NOT reach the network or push.

## Examples

**E-1 (not runnable in this planning run — the wrapper does not exist yet).**
Premises: `line-run.sh` implemented at C-01…; a git repository as cwd; an isolated registry under the sanctioned `.specify/.tmp/line-registry-registration/registry` path via `SPECIFY_LINE_REGISTRY_DIR`; engine present at candidate 1.

```bash
SPECIFY_LINE_REGISTRY_DIR=.specify/.tmp/line-registry-registration/registry line-run.sh --line-id demo-batch --run-id r20261116T090000Z-a001 -- true
```

Expected: exit `0`; registry entry `demo-batch-r20261116T090000Z-a001` closes with `state=closed`, `last_event=completed`. Pinned by `tests/integration/test_line_run_behavior.py` (route b).

**E-2 (not runnable in this planning run).** Premises: as E-1.

```bash
SPECIFY_LINE_REGISTRY_DIR=.specify/.tmp/line-registry-registration/registry line-run.sh --line-id demo-fail --run-id r20261116T090000Z-a002 -- false
```

Expected: exit `1` (the child's status); entry closed with `last_event=failed`. Pinned by the same test file.

**E-3 (not runnable in this planning run).** Premises: as E-1.

```bash
line-run.sh --help
line-run.sh --version
```

Expected: both exit `0`; no registry directory is created or modified. Pinned by `tests/contract/test_line_run_contract.py`.

**E-4 (runnable now — engine identity probe, measured 2026-11-16).** Premises: this repository as cwd.

```bash
python3 skills/external/sdd-loop-driver/scripts/line-registry.py --version
```

Measured output: `line-registry.py 0.0.22` (exit `0`). This is the engine C-07/C-08 targets.
