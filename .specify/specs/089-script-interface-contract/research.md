# Research — Feature 089 脚本接口契约（Script Interface Contract）

**Status**: Phase 0 + Phase 1 rulings. Each ruling records the decision, the rejected alternative and the
measured anchor. All measurements were taken on 2026-11-06 in
`/cws_data/cloud-native-ai/spec-kit` at base `23c7a83b` (branch `089-script-interface-contract`). Probes that
would mutate the tree ran in a throwaway `git worktree` under `.specify/.tmp/086-probe/` (removed afterwards,
`git worktree list` back to one entry).

Machine readings quoted below come from `python3` (CPython 3.11) and `git ls-files`; where a reading corrects an
earlier one in `requirements.md`, the correction is stated as a correction rather than silently overwritten
(the requirements file is not edited by this stage).

## R1 — The checker is ONE file, and the classification rule is declared as data

**Decision**: `scripts/python/script-interface-check.py` owns both halves (candidate screen + per-file
classification). No second engine, no second data file. The classification **rule** is written where the
authority artifact says it lives — the owner document
`shared/definitions/script-interface-definitions.md` — and the engine emits it in `--emit-rule` mode so a guard
can assert "the page and the code agree".

**Rejected alternative**: put the rule into a `shared/declarations/facts/*.yaml` declaration fact (the Feature 084
harness-triple form), so a generic declaration engine judges it. Rejected because (a) the requirements name the
executable form explicitly (FR-031: `argparse` / read-only / exit 0·1·2 / `--json`, sibling of
`scan-confirmation-gates.py`), and (b) the rule is not a closed-set membership but a **procedure over the
filesystem** (run the file in a sandbox and compare), which a static fact cannot express.

**Evidence**: `scripts/python/scan-confirmation-gates.py` is the declared sibling (argparse, `REPO_ROOT` guard for
mirror invocation, exit 0/1/2, `--json`); `scripts/python/gate-check.py` and `clause_extract.py` are the two
engines that already handle flags without `argparse`, and they are the two that fail the contract today
(`python3 scripts/python/clause_extract.py --help` → `--help: not a file`, exit 2 — a silent misread of the
read-only intent, the same failure class as the incident).

## R2 — The candidate screen: two machine-readable sources, plus an assertion that cannot go green on nothing

**Decision**: candidate set = `git ls-files '*.sh' '*.py'` minus `.gitignore`-ignored paths; coverage assertion =
walk the work tree for `*.sh` / `*.py`; any file neither a candidate nor ignored is a **finding**
(`candidate-not-collected`), exit 1. Git absent → the walk alone is the candidate set, and the screen reports
`source=walk-only` in its own `--json` payload so the degraded source is never silent.

**Measured**: tracked 71 `.sh` + 666 `.py` = 737; work-tree count 737; untracked-and-not-ignored 0. The two
sources currently coincide, which is why the assertion is cheap and why a "nothing scanned, therefore all good"
green is impossible: the screen fails when the work-tree walk finds a file the candidate set lacks.

**Rejected alternative**: hand-written directory list (the requirements forbid it), or "walk only" (it cannot
distinguish a vendored tree from a delivered one, and `.gitignore` is the project's own statement about which is
which).

**Probe**: `touch probe.sh` in the copy tree → `git check-ignore -v probe.sh` exits 1 (not ignored) → the screen
reports it; appending `probe.sh` to `.gitignore` → `git check-ignore -v` prints `.gitignore:68:probe.sh` and
exits 0 → the screen turns green. This is SC-009's falsification, executed.

## R3 — Classification is a sandbox experiment, not a source scan

**Decision**: for every candidate, classify by **running it** in a sandbox copy of the repository and observing
whether the file's own code executed (side effects landed in the sandbox). bash: instrument the file so that the
statement following a recognized option trigger records one marker line, then run it with a declared option and
look for the marker. python: run it with a declared action and observe either work extended outside the
interpreter's import machinery or absence of import. A file with no marker is exempt.

**Rejected alternatives** (all three rejected with a measured counter-example):

| Alternative | Counter-example |
|---|---|
| "has top-level executable statements" (bash) | `scripts/bash/common.sh` has `if ! check_dependency; then … exit 1; fi` at top level. Measured: `env -u CWS_LIB_BASH_HOME bash scripts/bash/common.sh` → two error lines, exit 1, no main action. A source-shape rule calls it applicable. |
| "has `if __name__ == \"__main__\"`" (python) | `scripts/python/declaration_reader.py` has the block **and** is imported by `validate-requirements.py`; measured `python3 scripts/python/declaration_reader.py --action get --fact probe-does-not-exist` → `no declaration for fact …`, exit 1. A literal rule cannot separate "imported library that happens to have a demo block" from "real CLI". |
| "directory-level exemption for `tests/`" | `tests/conftest.py` imports `pytest` and installs an autouse fixture that creates temp git config on every test; `tests/contract/test_migration_distribution.py` and five `tests/fixtures/*.py` carry `__main__` blocks. A directory rule would silently exempt 449 files, which FR-024(c) forbids. |

**Measured cost**: 737 candidates × (sandbox copy 1 + runs 1, 2, 4, 5, 6, 7… the classification run). A `git
worktree add --detach` of this repository completes in under 2 s (measured during the probes); a per-file run of
the cheap probes is a few tens of ms. The `--json` payload is written incrementally so a partial run is still
evidence; a soft budget (default 900 s) that trips is a **finding**, never a silent pass (see R11).

## R4 — `--version`: one line, read at run time, one mechanism per language

**Decision**: output `<script-name> <framework-version>`, where `<framework-version>` is read from
`pyproject.toml` **at run time**; unreachable file → the literal `unknown`, still exit 0 (A4, amended: see F-3).
One mechanism per language:

- python: a shared module `scripts/python/script_interface_cli.py` exposing `version_text()`, `print_version()` and
  a `VersionAction` (an `argparse.Action` subclass — `action="version"` is a *string* dispatch to
  `argparse._VersionAction`, which prints a constant), plus the bash guard's literal prefix.
- bash: `scripts/bash/script-interface.sh` defining `script_interface_version_text <name>`; a guard block inlines
  the body via the `__SCRIPT_INTERFACE_VERSION_BODY__` sentinel so a script that cannot `source` (a broken
  `common.sh`, a downstream copy) still answers.

**Measured probes** (in the scratch worktree):

- Python 3.9+ `$script --version` precedence: putting the version handling in `main()` is **not** safe for
  `goal-utils.py`, whose subparsers are `required=True` (a call pattern of the shape `--version` with no action is
  rejected at exit 2 by argparse). The safe form is a `VersionAction` (`nargs=0`, `parser.exit(0)`) on **every**
  parser including each subparser — argparse then exits 0 before requiring a subcommand.
- Custom `VersionAction` with a run-time `pyproject.toml` read: built and run in the copy —
  `python3 scripts/python/sync-mirrors.py --version` → `sync-mirrors.py <version>` exit 0. Editing the copy's
  `pyproject.toml` to `9.9.9` and re-running changed the output to `sync-mirrors.py 9.9.9`; restoring it to the
  real value restored the output. This is SC-011's mechanism, executed.
- Downstream case (no `pyproject.toml` in reach): the same action printed `sync-mirrors.py unknown`, exit 0.
- `find_repo`-style upward walks are refused: a first probe that walked up from a script copied into a
  subdirectory found the **host checkout's** `pyproject.toml` and reported the host version. The probe variant
  that searches only the script's own directory printed `unknown`. Reaching a foreign checkout's version is a
  wrong answer stated confidently; `unknown` says "not known here".

**Rejected alternative**: a per-script `version` file, a `version.py` constant, or a literal in each script —
each is a second definition point and drifts on the next release (A4, Out of Scope).

**Withdrawn alternative — non-zero exit when the version is unresolvable.** Considered and rejected as a
tension record: it fails the owner's admissibility criteria (`shared/guidelines/decision-tension.md`), because its
`expected_sacrifice` is ≤ 0 — the zero-exit reading is already fixed by US2 acceptance 1 and SC-001, so there is no
genuine sacrifice to name and the "antithesis" is a preference, not a competing constraint. The decision is
therefore recorded here as an assumption rather than as `T-00N`: an unreachable `pyproject.toml` yields
`<script-name> unknown` and exit 0 (F-3). One line of consequence, stated so it is not a silent compromise: a
downstream copy with a broken packaging layout shows up as `unknown` in a green run, not as a red one; the
discriminator lives in the checker's report, not in the script's exit code — the payload's per-candidate `version`
field (C-18) is `unknown` for exactly that candidate, so `jq '.candidates[] | select(.version=="unknown")'` names
it without failing the run.

## R5 — The bash guard: scan `"@"`, before any `source`, never `getopts`

**Decision**: the first executable block of a script is

```bash
# script-interface:begin guard
for __si_arg in "$@"; do
  case "$__si_arg" in
    --) break ;;
    -h|--help) <print help>; exit 0 ;;
    --version) <print version>; exit 0 ;;
    -*) <unrecognized-option>; <usage to stderr>; exit 2 ;;
  esac
done
# script-interface:end guard
```

placed **before** `source .../common.sh` and before any `mkdir` / `git` write / manifest generation. Options the
script knows that look like flags are case branches **above** the `-*` reject arm, so a recognised option is never
rejected and an unrecognised one never reaches the main action.

**Measured counter-examples that fix the shape**:

- `getopts` stops at `--` and does not consume long options — `refresh-tools.sh`'s `*)` branch calls `usage()` and
  then **continues**, which is the "usage printed, action still ran" shape.
- `source common.sh` first turns `--help` into exit 1: `common.sh` runs a dependency check at top level (measured
  above). A guard after the `source` therefore cannot claim zero side effects.
- Position of `--version` inside argparse: with a required-subparsers parser, `--version` before the subcommand is
  rejected; the `VersionAction` on the top parser plus every subparser fixes it (R4).

**Probe**: patched the incident script `scripts/bash/generate-instructions.sh` in the copy tree with the guard
block; `--help` → usage, exit 0, `sha256sum -c` on `.specify/instructions.md` still `OK`; `-h` → exit 0;
`--version` → `generate-instructions.sh <version>`, exit 0; `--bogus` → `error: unrecognized option: --bogus`
plus usage on stderr, exit 2. `git status --porcelain` showed only the patched script itself.

## R6 — python `--version` reaches the mirrored copy only through a generated bridge

**Decision**: `.specify/scripts/python/*.py` and `.specify/skills/**/scripts/*.py` are **generated mirrors**. The
source keeps its `if __name__ == "__main__":` block, and the mirror gets a bridge inserted **before** that block by
`sync-mirrors.py` at projection time (a per-named-file rule, not a generic transform). The bridge reuses the same
`sibling_path(__file__)` / `pyproject.toml` reader the source uses, so it does not depend on the source's CLI form.

**Why this exists** (the alternative was proved to fail): appending the bridge to the end of a mirrored file does
nothing, because `sys.exit(main())` in the `__main__` block runs first — measured: the bridge written after the
block left `--version` reported as `unrecognized arguments` with exit 2. Moving the bridge above the block works:
`declaration_reader.py <version>`, exit 0, while `--action list` still exits 0. But a bridge **inside the file**
cannot survive a re-projection when the mirror is required to equal the source: copying the source over the mirror
(a simulated projection) removed the bridge and `--version` went back to exit 2.

**Rejected alternative**: make the mirror unconditionally applicable and add `--version` to every library module —
that contradicts FR-009/FR-026 (a library is exempt) and would paste a CLI into `declaration_reader.py`'s API
surface, which C-053 explicitly calls the "real surface, CLI is a debug door" split. The bridge is a projection
of the mirror, not a second implementation: it calls the same helper and prints the same string.

## R7 — `tests/` classification: the run result decides, not the directory name

**Decision**: `tests/**` is classified by exactly the same rule as everything else (R3), and the measurement is
recorded per file in `--json`. Measured shape of the surface: 449 candidates under `tests/` (447 `.py` + 2 `.sh`),
of which 441 `.py` have no `__main__` block and no side effect on run (`python3 -m pytest` is not "running the
module"); 1 (`conftest.py`) imports `pytest` — measured `ModuleNotFoundError` in the bare interpreter — and 6
carry `__main__` blocks (5 under `tests/fixtures/` plus `tests/contract/test_migration_distribution.py`) whose
bodies are fixtures, not actions.

**Rejected alternative**: exempt `tests/` as a directory. Rejected on the requirements' own authority
(FR-024(c), Clarifications Q3) and on a counter-example: `tests/conftest.py` installs an autouse fixture that
writes git config files before any test runs, and six modules execute on `__main__`.

**Consequence written into the plan**: the classification marker is `python-imported-or-side-effect-free` for the
441, and the six `__main__` modules must be **read**, not assumed — the tasks stage turns each into either a
one-line `--version` or a recorded entry. The check reports them; it never exempts them by path.

## R8 — Declared exceptions: the owner page is the register, and the checker recomputes

**Decision**: `## Declared Exceptions` in
`shared/definitions/script-interface-definitions.md` (+ `.specify/` mirror) is the only register. Each row carries
`path`, `skill`, `unsatisfied clause`, `alternative handling`. The checker recomputes for each row: path exists;
path is under `skills/external/<skill>/`; that skill's `SKILL.md` declares `classification: external`. Any limb
failing → `exception-unverifiable`, exit 1. A third-party candidate **not** in the page → ordinary candidate,
judged and failed like any other.

**Measured, and it corrects a fact the requirements state twice**: `skills/external/coaching-skills/SKILL.md` and
`skills/external/create-skills/SKILL.md` **both declare `classification: external`** (line 3 of each, measured with
`grep -n 'classification:' skills/*/*/SKILL.md`). The requirements (A6, Clarifications Q6, Edge Cases "上游来源
不可判定") say those two declare `internal`. Under Requirements v2 they therefore classify as third-party. That
changes the disposition of the files inside them from "fix in place" to "declare as exception", which is exactly
the escape hatch FR-027 forbids for framework source. Recorded as `PLAN-EDIT` in the stage report; the plan does
not silently pick a reading.

**Follow-up measured 2026-11-06**: neither skill directory carries a `*.sh` or `*.py` file
(`git ls-files 'skills/external/coaching-skills/*' 'skills/external/create-skills/*' | grep -cE '\.(sh|py)$'` →
`0`), so this feature modifies neither of them and registers no exception row for them; the disposition question
above is therefore closed for this feature, and would only reopen if a script appeared under either skill.

**Rejected alternative**: put exceptions in the checker's constants (register and code fused) or in the
constitution (the checker cannot read it mechanically).

## R9 — Where the contract text lives, and what each surface may carry

**Decision**: the owner page `shared/definitions/script-interface-definitions.md` owns exactly five things
(stated at its top): (1) the candidate/classification rule, (2) the mandatory flags and their mandatory content,
(3) the zero-side-effect boundary, (4) the unrecognised-option rejection requirement, (5) the exemption and
declared-exception criteria. Every other surface carries a summary + a path, with a **banned literal list**
asserted by the guard: the page's four mandatory help-content labels (`usage`, `options`, side-effect statement,
exit codes) appear in no other surface.

**Rejected alternative**: copy the rule into each of the five landing points (drifts within one release — the
constitution's own Sync Impact Report records this happening twice for a neighbouring principle).

**Grounded naming**: the title `Script Interface Contract (Declared, Zero-Side-Effect)` is derived by sibling
imitation — `Directory Governance (Named, Documented, Ignored When Temporary)`,
`Self-Explanatory Structure (不言自明)`, `Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)`: a name plus
its two load-bearing properties. Length 57 chars, which fits the existing title-length band (longest current
title: 64).

## R10 — Instructions side: the live file grows by one `##` section, and the budget must be raised deliberately

**Decision**: `templates/instructions-template.md` gains exactly one top-level `## Script Interface Contract`
section (summary + pointers, no engine call forms, project-neutral wording), and `.specify/instructions.md` is
**regenerated** by `scripts/bash/generate-instructions.sh` so the live file carries the same section. The size
budget constant in that script is raised by the smallest multiple of 1024 that leaves ≥ 1024 B headroom
(the rule already recorded in its own comment).

**Measured**: template 28 930 B / live 33 357 B at plan time; the budget is `34816` with 1459 B of headroom for the
live file and the template's own guard suite pins the ceiling. Two existing pins move in the same commit:
`test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22` (`TPL_EXPECTED` 32→33,
`LIVE_EXPECTED` 33→34) and `tests/contract/test_constitution_double_landing.py`
(`TEMPLATE_COUNT` 18→19, `LIVE_COUNT` 19→20, `COMMAND_COUNT` 11→12, watchlist 6→7).

**Rejected alternative**: hand-append the section to `.specify/instructions.md`. Rejected: the live file is a
generator output; a hand edit is a client-side fix that the next reconcile erases, and the Two Hats rule names it
a defect.

**Hazard (recorded as a risk, not a step)**: invoking that generator is the incident itself. The compatibility leg
proves that with the guard in place `--help` is free and the running path is unchanged. The instructions are never
written by this plan stage, and the tasks stage reaches the generator through a scratch copy of the repository,
never the live tree.

## R11 — The checker's own failure modes must be red, never silent

**Decision**: four explicit non-green paths, each with its own finding name:

| Situation | Finding | Exit |
|---|---|---|
| a candidate is neither applicable-compliant nor exempt-classified | `contract-violation` (with the missing limbs) | 1 |
| the work-tree walk sees a `*.sh`/`*.py` outside candidate ∪ ignored | `candidate-not-collected` | 1 |
| a declared exception row fails recomputation | `exception-unverifiable` | 1 |
| the sandbox probe budget trips, or the sandbox cannot be created | `probe-budget-exhausted` / `probe-unavailable` | 1 |
| a candidate's classification run failed for an environment reason | `probe-inconclusive` (never treated as exempt) | 1 |

**Rejected alternative**: treat an unprobeable file as exempt. That is the "nothing scanned, therefore all good"
green, and it makes the whole check optional to a hostile environment.

## R12 — Wiring: existing surfaces only, and an opt-in-only presence elsewhere

**Decision**: the new engine is consumed by the new contract test
`tests/contract/test_script_interface_contract.py` (`pytestmark = pytest.mark.contract`), which the existing
`pytest -m contract` invocation already selects. No driver stage gate is wired (FR-031). Each guarded behavior is
red-first: the test asserts today's (failing) state first, then the fix.

**Measured**: `python3 -m pytest --version` fails in this shell (the venv on `PATH` has no pytest); pytest 9.0.3 is
reachable as `/usr/local/bin/pytest` and `/usr/bin/python3 -m pytest`. The baseline slot must therefore pin
`SPECKIT_PYTHON` (the `run-tests.sh` resolver reads it first) — recorded as an execution premise, not a silent
assumption.

## R13 — Mirror scope: a declared, executable projection instead of a hand-maintained list

**Decision**: the framework-side projection of a mirrored script adds the guard/version surface above the source
content, driven by a per-named rule inside `sync-mirrors.py`. The byte-equality criterion is **withdrawn for those
named files** and replaced by an executable weakening: the mirror equals `source + declared projection`, and the
set of projected names is declared in one place and asserted against the code that implements it.

**Rejected alternative**: keep byte equality and require the source to carry the whole surface. Rejected for the
measured reason in R6 (a bridge cannot survive an equality projection, and a source-level CLI pasted into every
library contradicts the exemption rule).

**Consequence for FR-030 / SC-003**: FR-030 says "MUST be byte-identical". The plan keeps a strictly stronger,
machine-checkable form — the projection is deterministic, so the mirror is a pure function of the source and the
rule — but the literal "byte-identical" claim no longer holds for the named files. Stated as `PLAN-EDIT` F-4.
