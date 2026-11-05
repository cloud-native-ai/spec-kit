# Phase 0 Research — 084 Harness 三重结构（markdown + yaml + script）

**Date**: 2026-11-05 | **Spec**: `.specify/specs/084-harness-triple-structure/requirements.md`
**Method**: every reading below was taken on this branch at `171c2ff8` with the commands shown; the raw console output is
`.specify/specs/084-harness-triple-structure/test-evidence/plan-readings.txt`. `specify init` source-route transcript:
`test-evidence/specify-init-source-route.txt`.

Scope of this research: the eight questions the plan cannot answer from the requirements alone — the executable
toolchain, whether the repo's own distribution path reaches a client project, how a mirror copy differs from a client
copy (because one of them rewrites paths), what the candidate screen actually enumerates today, where the migration
inputs live, which existing test files are the zero-new-failure surface, how the call site interacts with the gate
host's stated self-containment, and what the decomposition gate says.

---

## R1 — Executable toolchain

| Reading | Command | Result |
|---------|---------|--------|
| interpreter | `python3 --version` | `Python 3.11.13` (satisfies the declared `requires-python >= "3.8"`) |
| pytest | `python3 -m pytest --version` | `pytest 9.2.0` — matches the pin already recorded in the spec's runtime row |
| git | `git --version` | `git version 2.43.7` |
| runner resolution | `bash scripts/bash/run-tests.sh --collect-only -q tests/contract/test_requirements_checker.py` | stderr line `# test runner: python3 -m pytest …` — the runner resolves `python3` (no `.venv` exists on this host) |

Consequence: the new script and the shared reader MUST stay import-free beyond the standard library, because the
interpreter that runs them is a plain CPython 3.11 without a project virtualenv. `pyproject.toml` `dependencies` holds
six entries and none is a YAML library, so "parse a declared subset ourselves" is the only library-free route.

## R2 — Does the repo's own distribution path reach a client project? (two routes, opposite answers)

Two ways to run the initializer exist on this host, and they do **not** produce the same tree:

- **Route A — the console script on `PATH`.** `specify init demo --ai claude --script sh --no-git --ignore-agent-tools`
  exits 0, and the produced `.specify/shared/` carries **55** Markdown files. The working tree's `shared/` carries
  **62**. `get_resource_path()` returns the installed package directory first, so route A distributes a **snapshot of
  whatever was installed**, not the tree under edit.
- **Route B — the source checkout ahead of the installed package.**
  `PYTHONPATH=<repo>/src python3 -c "from specify_cli import main; main()" init demo3 …` exits 0,
  `get_resource_path()` returns `<repo>`, and the produced `.specify/shared/` carries **62** Markdown files with all
  five subdirectories present including `definitions/` (12 files). Nested subdirectories are copied.

Consequence: the closure reading for distribution MUST name route B, and route A's reading is recorded as a
**falsified** premise (§ Execution Premises `EP-002`) rather than as an out-of-scope remark. A statement like "run
`specify init`, then check the directory exists" is unpassable on route A for any file this branch adds.

## R3 — What a copy actually does to path references (the load-bearing mirror asymmetry)

`copy_local_templates()` copies `shared/` through `copy_tree_with_rewrite()`, which runs `rewrite_paths()` on **every
UTF-8-decodable file** — not only Markdown. `rewrite_paths()` rewrites a segment that *starts* a path reference
(`memory/`, `scripts/`, `templates/`, `shared/`) to its `.specify/` form and maps the two-branch skills layout onto the
runtime shape. A declaration file's `consumers` / `former_carriers` / `unit` / `carrier` values are exactly such
references.

`scripts/python/sync-mirrors.py` copies byte-identically (its whole job is to detect a byte difference). Therefore the
same declaration file exists in **three forms**:

1. framework source `shared/declarations/…` — source-form paths;
2. this repo's runtime mirror `.specify/shared/declarations/…` — source-form paths (byte-identical);
3. a client project's `.specify/shared/declarations/…` — `.specify/`-prefixed paths (rewritten on the way in).

Consequence, and this is a design requirement rather than a preference: the checker MUST resolve a path after stripping
**one optional leading `.specify/`**, and every declaration path field MUST be written in source form. Without that
normalization, the same declaration validates in form 1/2 and fails to resolve its carriers in form 3 — a client-only
failure the framework repo can never observe.

## R4 — Candidate screen S: what it enumerates today

Recomputed by directory scan (never from a list):

| Surface | Count |
|---------|-------|
| `templates/commands/*.md` | 27 |
| `skills/{external,internal}/*/SKILL.md` | 53 |
| `shared/workflow/*.md` | 19 |
| `shared/definitions/*.md` (explicitly **not** units) | 12 |

The screen is a **text** test over those 99 unit carriers: a carrier enters the candidate set when its text contains a
reference to a framework-internal deterministic engine (`scripts/python/<name>.py` or
`skills/<layer>/<name>/scripts/<file>`). The Edge Cases section already accepts the conservative side of a text test
(a carrier that merely mentions a script enters the candidate set and gets an exclusion record).

## R5 — The migration inputs, located

Batch-1 material, each with the engine-side twin that makes the fact "machine-consumed ∧ cross-face":

| Fact | Engine-side definition | Prose / definition-side twin |
|------|------------------------|------------------------------|
| feedback prompt threshold | `scripts/python/feedback-utils.py:93` `DEFAULT_THRESHOLD = 10` | `shared/workflow/feedback-step.md:368` ("threshold defaults to `10`") |
| evidence seven states | `scripts/python/evidence-utils.py:23` `SEVEN_STATES` | `skills/internal/collect-evidence/references/evidence-discipline.md` (definition owner) and `shared/guidelines/better-harness.md` § 证据纪律 item 2 (full re-listing) |
| evidence five lanes | `scripts/python/evidence-utils.py:27` `LANE_NAMES` | the consumer prose that names the lanes |
| flow-class classes | `scripts/python/flow-class-check.py:96` `CLASS_VALUES` | `shared/definitions/flow-class-definitions.md` |
| flow-class basis | `scripts/python/flow-class-check.py:97` `BASIS_VALUES` | same |
| flow-class document types | `scripts/python/flow-class-check.py:882` `FLOW_TYPE_VALUES` | same |
| flow-class ledger columns | `scripts/python/flow-class-check.py:120` `REQUIRED_LEDGER_COLUMNS` | same |
| flow-class neutral categories | `scripts/python/flow-class-check.py:99` `NEUTRAL_CATEGORIES` | same |
| `Path` value domain | `scripts/python/validate-requirements.py:98` `PATH_VALUES` **and** `scripts/python/closure-acceptance-check.py:505` (inline tuple) | `shared/workflow/acceptance-hardening.md` § Closure Verdict § Input contract — the `Path` marker |

Two readings that shape the plan: the `Path` domain has **three** faces including an inline tuple in a second engine
(the migration deletes one of them, not both), and `FLOW_TYPE_VALUES` really exists at the cited script — the spec's
adjudication row is backed.

## R6 — Reusable machinery, and its limits

- **Residual-literal judgement**: `doc-consistency-check.py --action verify --faces duplicate --spec-dir <spec>` runs
  today — on this spec directory it printed `faces: duplicate=pass`, `files_scanned: 2`, `findings: 0`. The plan reuses
  the `duplicate-fact` label instead of writing a scanner (the spec's FR-010 forbids a second one).
- **Gate host, part 1 — a stated invariant**: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` is the
  host the spec names. Its module docstring states "Self-contained; never reads the framework runtime scripts tree". A
  subprocess delegation to `scripts/python/harness-triple-check.py` contradicts that sentence while leaving its
  *mechanism* (no framework imports) intact. Resolution: the delegation is optional and degradation-aware (checker
  absent ⇒ an advisory naming the absence, never a silent pass), and the host's own docstring is corrected in the same
  change so the documentation and the code agree. The host is **not** one of the five scripts whose criteria and exit
  codes the spec freezes.
- **Gate host, part 2 — a hard ceiling on the new finding class**: `tests/contract/test_acceptance_premises.py:274`
  asserts `checks <= set(FINDING_CHECKS)` where `FINDING_CHECKS` is the closed four-name tuple (`runtime-stack-row`,
  `runtime-contract-incomplete`, `premise-undecided`, `inherited-blocker`). A new unconditional finding class
  therefore makes an existing 081 assertion go red — which the spec's FR-018 forbids ("081 test assertions: zero
  change, zero new failures"). Consequence: the delegation is **opt-in by a flag** (default off ⇒ the host's behavior
  is byte-for-byte what it is today), and the plan-stage gate row is what passes the flag. The wire exists, the
  existing closed set stays closed, and both facts are mechanical rather than remembered.

## R7 — The zero-new-failure surface (measured, not assumed)

Selection rule: test files that reference any of the five frozen gate scripts. Command and result are in
`plan-readings.txt` § R10 → **39** files. Two of them are the 081 acceptance files whose assertions must not move:
`tests/contract/test_requirements_checker.py` collects **40** tests, `tests/contract/test_checker_form.py` collects
**37**. This is a *collect* reading, not a run: the plan stage is docs-only, and the full baseline belongs to the
implement stage's own budget.

## R8 — Mirror baseline before any edit

`python3 scripts/python/sync-mirrors.py --check` → exit 0 with every pair `ok` (`shared/ == .specify/shared/`, 62 files;
`scripts/ == .specify/scripts/`, 119 files). Recorded so the closure criterion reads "no **new** drift", and so any
drift a later run reports is attributable to this feature rather than to the baseline.

## R9 — Decomposition gate

`decomposition-check.py --mode plan --requirements <spec>` → `{"decision": "proceed", "measured": {"fr_count": 19,
"task_count": null, "fr_ceiling": 30, "task_ceiling": 40}}`. Decision `single-package`: no slice split, and no task
count is pre-committed (the gate's own task ceiling is read at the tasks stage, not guessed here).

## R10 — What was deliberately not executed

- The full pytest suite: the plan stage produces documents only, so the stage budget records `status=not-run-docs-only`;
  the implement stage owns the whole-suite baseline and the closure comparison.
- `harness-triple-check.py` and `declaration_reader.py` do not exist yet, so no example involving them could be run at
  this stage. Every such example in the Phase 1 artifacts is marked per-example (route (b)) with the premises it rests
  on, and each premise names the file or fact a later stage must re-measure instead of inheriting.
