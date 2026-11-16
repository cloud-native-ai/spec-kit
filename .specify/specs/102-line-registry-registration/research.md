# Phase 0 Research — 102-line-registry-registration

**Spec**: `requirements.md` (23 FR / 9 SC, Clarifications A-14…A-24)
**Method**: every claim below was measured on 2026-11-16 against this repository (engine source, CLI runs, digest runs, generator source). Where a spec premise was re-measured, the measurement is the evidence; the spec's adjudications (A-14…A-24) are binding input and are not reopened.

The spec's Shared Strings are referenced as `[[STR-NNN]]`; their literals are owned by `requirements.md` § Shared Strings and are not copied here.

## R-01 — Wrapper CLI shape and exit-code policy

- **Decision**: `[[STR-001]]` declares `--line-id <slug>` and `--run-id <id>` (both required), the option value as the **next argument** (`--opt=value` is rejected by the shared guard's token vocabulary), and a mandatory bare `--` before the wrapped command. `-h` / `--help` / `--version` answer before any action.
- **Exit codes**: `0` success; the wrapped command's own status when it is non-zero; `2` wrapper usage error (undeclared option, missing option value, missing `--`, empty command) with the command not executed; `4` wrapper environment/identity failure (engine unreadable at both declared candidates, or no git toplevel) with the command not executed; a non-zero engine status propagates unchanged when registration or close fails (A-24 fixes the close-failure priority).
- **Alternative rejected**: a `--command "<string>"` form — it forces re-quoting of every argument and hands the wrapper a shell-injection surface it does not have with `-- "$@"`.
- **Evidence**: `scripts/bash/script-interface.sh` § "Usage" (token scan, bare `--` terminator, C-9 "a recognized option never rescues an unrecognized one"); `scripts/bash/run-tests.sh:37-51` shows the house pattern (source the guard above `common.sh`, declare the option set after `--`).

## R-02 — Engine resolution and project identity (A-17 / A-18)

- **Decision**: the wrapper resolves the engine by its own path, in the two declared candidates — `<repo-root>/skills/external/sdd-loop-driver/scripts/line-registry.py`, then `<repo-root>/.specify/skills/sdd-loop-driver/scripts/line-registry.py` — where `<repo-root>` is the wrapper's own `../..`, moved up one level when that directory is named `.specify` (the guard `scripts/python/status-digest.py:81-85` already carries). The first readable candidate wins; both unreadable is a registration failure (`4`) naming both paths. Project identity comes from `git rev-parse --show-toplevel` run in the caller's cwd (the toplevel result, never `$PWD`) and is passed as both `--project-dir` and `--repo-root`.
- **Alternative rejected**: resolving the engine from the caller's `PATH` (nondeterministic, and it would pick `.specify/scripts/line-registry.py`, an untracked local copy) or from an environment variable (A-17 forbids a new one).
- **Evidence**: both candidates exist and answer `--version` (`line-registry.py 0.0.22`); `register` refuses without `--project-dir` / `--repo-root` (`line-registry.py:578-586`); registry-root resolution is the engine's alone (`line-registry.py:145-153`).

## R-03 — Registry line id composition (A-18)

- **Decision**: the wrapper passes `--line-id "<line-id>-<run-id>"` and `--run-id "<run-id>"`. The composed id must satisfy the engine's own `LINE_ID_RE` (engine line 42) and the run id its `RUN_ID_RE` (line 43); the grammars are referenced by constant name and not restated here. The wrapper validates neither grammar itself — the engine is the validator — and a rejected id is a registration failure with the command not executed. run-team generates its run id in the same engine-valid form (A-18: `r<UTC yyyymmdd>T<UTC hhmmss>Z-<4 lowercase hex>`); the bare UTC timestamp the skill uses today is not a run id.
- **Alternative rejected**: a fixed id per slug — `closed` is terminal and the entry file is never reused (`update` refuses any transition out of `closed`, engine line 818), so a fixed id would make the second run of the same script fail permanently.
- **Evidence**: the spec's example `batch-apply-r20261116T090000Z-a001` is 34 characters and matches `LINE_ID_RE`; a live register/deregister round with a composed-shape id succeeded (see § Baseline measurements).

## R-04 — Fail-closed registration and dual-failure priority (A-5 / A-24)

- **Decision**: registration is a precondition, not a best effort: on any registration failure the wrapper prints the cause and the engine payload to stderr and exits without starting the wrapped command. On close failure with a zero child status, the wrapper exits with the engine's non-zero status; when the child is also non-zero, the child's status is the wrapper's status and the close failure is written to stderr. Neither result is rewritten.
- **Alternative rejected**: best-effort registration — it reproduces the exact invisibility the feature exists to remove.
- **Evidence**: `deregister` requires `--reason` and refuses to close a write line without an integration result (engine `action_deregister`), so "close failed" is a reachable, non-hypothetical state; the closed entry is terminal (line 818).

## R-05 — Residue on SIGKILL (A-10 / A-20)

- **Decision**: the wrapper installs no trap that would fabricate a close on an uncatchable signal. A wrapped child that dies by signal surfaces as a non-zero status and is closed with `failed`; a wrapper that is itself killed leaves the entry `active`, which is exactly what the digest shows. No cleanup, timer or threshold is added: staleness is the digest's own `DEFAULT_STALE_BOUND_SECONDS` (`scripts/python/status-digest.py:74`, `--stale-bound` overrides it).
- **Alternative rejected**: a `trap ... EXIT` that closes the line — it cannot run on SIGKILL, adds a second close path to reason about, and would mark a genuinely interrupted run as completed in the catchable cases.
- **Evidence**: digest constants measured at lines 74 and 2692-2712; closed entries are filtered from the digest's current view (`status-digest.py:985-989`, `1097`).

## R-06 — Heartbeat is an event, never a clock (A-8 / A-19)

- **Decision**: the wrapper emits exactly two engine events — `register` (the engine writes `last_event: "registered"`) and `deregister` (the engine writes `last_event: <reason>`). Stage-boundary heartbeats belong to the caller that can observe stages (`run-team` §6, one `update --last-event <step-label>` per orchestration step). No heartbeat file, timer or second channel is introduced.
- **Alternative rejected**: a background heartbeat loop inside the wrapper — a daemon in miniature, forbidden by `reporting-obligations.md` § 十一.
- **Evidence**: `register` / `deregister` payloads measured in the baseline round below; `update` accepts `--last-event` (engine `build_parser`).

## R-07 — Mechanical criterion owner = scanner module constants (A-15)

- **Decision**: `[[STR-009]]` carries four module-level constants as the single machine owner of the mechanical projection — `LONG_TASK_MARKERS` (members `[[STR-004]]`, `[[STR-005]]`), `SELF_DECLARATION_MARKER` (`[[STR-003]]`), `COMPLIANT_INVOCATIONS` (the wrapper form and the engine's `register` / `update` / `deregister` forms), and `DEFAULT_SCAN_ROOTS`. Tests import them; the owner document, the plan and the contracts cite the constant names. The scanner skips its own resolved path and counts it as `owner-skipped`, which is never folded into the clean reading.
- **Alternative rejected**: a declaration-layer fact file — it would add a fact registration and break FR-022 / SC-009's closed delta; reopen only if a second engine must consume the same criterion (A-15).
- **Evidence**: `shared/declarations/facts/` is read through `scripts/python/declaration_reader.py`, i.e. a fact entry is a new registration, not a free-standing YAML file.

## R-08 — Scan roots and judged file surface (A-21)

- **Decision**: default roots are `scripts/bash/`, `scripts/python/`, `skills/`, recursively; a judged file is a **regular file** (symlinks are skipped, never followed, and no walk escapes the repository root) with a `.sh` / `.bash` / `.py` suffix or a `#!` first line. `--root` is repeatable and replaces the default set for that invocation. A missing or non-directory root is an input error naming it — never a clean reading.
- **Alternative rejected**: including `templates/` or `tests/` — `templates/` holds no executable script, and `tests/` holds fixtures written to be violations.
- **Evidence**: measured live-tree reading below: the only `[[STR-005]]` hits under the declared roots are `.md` files under `skills/external/*/references/`, which the file-surface predicate excludes; no `[[STR-004]]` hit exists anywhere under those roots.

## R-09 — Compliance forms, self-declaration and the owner skip (FR-014)

- **Decision**: a hit is compliant when the same file contains a compliant invocation — a `line-run.sh` invocation, or a direct engine invocation whose action is `register` / `update` / `deregister`. `SELF_DECLARATION_MARKER` declares that a file **is** a long task (so it enters the judged set even without a marker-string hit) and therefore still requires a compliant invocation; the marker never excuses registration. A standalone comment line carrying the marker counts; the intended placement is the file header, and the scanner deliberately does not bound the position (an extra positional threshold would be a fifth constant with no owner need).
- **Alternative rejected**: treating the marker as an exemption — it would create a one-line way to silence the scan without registering anything, i.e. a green check that would not go red when its subject breaks.
- **Evidence**: `run-tests.sh` itself does not contain the contiguous `[[STR-005]]` string (measured), which is why "supports `--full`" is not a violation while a caller that invokes it is.

## R-10 — How the ambient instructions sentence reaches the live file (A-6 / A-22)

- **Decision**: the only authored edit is `templates/instructions-template.md` (one bullet after `Exemptions and precedence` in `## Progress Reporting Discipline`). The live `.specify/instructions.md` receives that bullet through the `/speckit.instructions` command's in-place, section-by-section refresh (its User Input explicitly accepts section-level update requests), after which the four compatibility symlinks keep pointing at the same file. A contract test asserts the sentence in the template **and** in the live file, and asserts the bullet carries a pointer rather than the owner's criterion.
- **Alternative rejected**: relying on `bash scripts/bash/generate-instructions.sh` alone. Measured: its reconcile is additive at **top-level section** granularity and its own contract test forbids it from modifying an existing section (`tests/contract/test_instructions_section_propagation.py` C-2); an in-section bullet therefore cannot arrive from the generator. The generator is **not** modified — widening it would break C-2 and exceed FR-022 / SC-009's delivery surface.
- **Residual risk**: the command's section refresh is agent-mediated, so the implementation task must supply the section-level request explicitly rather than run the command bare; the contract test is the red leg if the sentence does not land.

## R-11 — run-team wiring anchors (A-23)

- **Decision**: three edits to `skills/internal/run-team/SKILL.md`, by existing section names — §5 Present & Execute top: register the run line (fail-closed before any seat is dispatched); §6 Orchestrate: one `update --last-event <step-label>` at each orchestration step boundary; §7 Report: close the line before writing the report and write the composed `line_id` into the report body. Each site names the engine path; none restates the engine's parameter table (read from `--help`).
- **Alternative rejected**: registering in §2 Preview — a `blocked` verdict would leave a dangling `active` line for a run that never executed.
- **Evidence**: the skill's current headings are `### 1. Load` … `### 7. Report` (measured), matching the spec's A-7/A-23 correction.

## R-12 — Test design, isolation and the single runner entry

- **Decision**: new tests split by artifact — `tests/contract/` for the two CLI contracts and the wiring surfaces, `tests/integration/` for the registry/digest behaviour, the SIGKILL residue and the live-repo reading. Every test isolates state with `SPECIFY_LINE_REGISTRY_DIR` under `tmp_path` and reuses `tests/fixtures/line_fixtures.py` (`base_env`, `engine_path`, `make_git_repo`). Parallel safety (the runner's default is `-n <effective> --dist load`) follows from per-test directories. The fixture scan root is `.specify/.tmp/line-registry-registration/` (already matched by `.specify/.gitignore` `.tmp/`), generated and removed by the test.
- **Alternative rejected**: module-level shared registry fixtures — they serialize the suite and alias across workers.
- **Evidence**: `tests/fixtures/line_fixtures.py:24-99`; `.specify/.gitignore` `.tmp/`; `scripts/bash/run-tests.sh` header (default parallel, `--full` tier, `--names-out`).

## R-13 — Scope and mirror baseline

- **Decision**: no new third-party dependency, no scheduler/daemon/store, no second registry or status spine, no change to `status-digest.py`'s action set, exit-code set or `[[STR-006]]` rendering. Mirrors are generated, never hand-edited: `scripts/` → `.specify/scripts/`, `shared/` → `.specify/shared/`, `skills/internal/` → `.specify/skills/internal/`, `templates/` → `.specify/templates/` (commands excluded), and `templates/commands/status.md` fans out to the four per-tool copies via `regen-command-copies.py`.
- **Baseline drift measured before any edit** (`sync-mirrors.py --check`, rc=2): five pre-existing `DIFF` rows under `skills/external/` (`coaching-skills/SKILL.md`, `coaching-skills/data-model.md`, `coaching-skills/references/prompt-templates.md`, `create-skills/SKILL.md`, `sdd-loop-driver/references/cli/qodercli.md`) and two `ORPHAN` mirrors (`.specify/scripts/line-registry.py`, `.specify/scripts/stage-runner.sh`). The acceptance criterion is **no NEW drift on the pairs this feature touches**, never "all green".
- **Alternative rejected**: repairing the pre-existing drift in this feature — it would fold unrelated files into SC-009's delta and into this feature's commit.

## Unknown adjudications (recorded, not asked)

| ID | Question | Adjudication | Reason |
|----|----------|--------------|--------|
| U-1 | Which exit code for engine-unavailable / non-git-repo? | `4`, wrapper-owned | Keeps `2` exclusively for usage and lets tests separate "you typed it wrong" from "the environment cannot register"; engine failures still propagate their own codes (A-24). |
| U-2 | Where may the self-declaration marker appear? | On any standalone comment line (first non-whitespace character `#`) whose text contains the literal, case-sensitive | The criterion owner stays four constants; one textual predicate (comment line + literal containment) needs no positional window and therefore no fifth owned threshold. |
| U-3 | Does the read-only scanner need `--version`? | No; `-h`/`--help` yes (argparse default) | The Script Interface Contract places read-only scripts outside the required set; help and unknown-option rejection (exit 2) are kept because they cost nothing and improve diagnosis. |
| U-4 | Is `--line-id=<value>` accepted by the wrapper? | No | The shared bash guard judges `-*` tokens whole; the usage line states the separated form. |
| U-5 | Where do engine payloads go? | stderr only | The wrapped command owns stdout; a caller parsing its output must never see registry JSON interleaved. |

## Baseline measurements (2026-11-16)

| Quantity | Reading | Command |
|----------|---------|---------|
| Interpreter / runner | Python 3.11.0rc1 (declared floor `>=3.8`), pytest 9.0.3 | `python3 --version`, `python3 -m pytest --version` |
| Shell | GNU bash 5.1.16(1) | `bash --version` |
| Engine | `line-registry.py 0.0.22` at both declared candidates | `--version` on each path |
| Empty registry digest | `nothing-running`, rc 3 | `status-digest.py --action digest --workspace <repo>` with an empty `SPECIFY_LINE_REGISTRY_DIR` |
| Active line digest | entry listed, state active, rc 0 | same, after `register` |
| Closed line digest | `nothing-running`, rc 3; entry shows `closed` + `reason=completed` | same, after `deregister --reason completed` |
| Live scan baseline | `[[STR-004]]`: 0 hits; `[[STR-005]]`: 4 hits, all `.md` under `skills/external/*/references/` | `grep -rn` over the three declared roots |
| Mirror baseline | 5 pre-existing `DIFF`, 2 `ORPHAN`, rc 2 | `sync-mirrors.py --check` |
| Command copies baseline | ok, rc 0 | `regen-command-copies.py --check` |
| Flow-class ledger | clean (91 units, 0 findings), rc 0 | `flow-class-check.py --action check` |
