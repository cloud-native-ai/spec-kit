# PKG-4b2b stage status — closing proofs (T062–T066)

date: 2026-11-07
line: `flow_class=execution; source=declaration; marker=null; error=-`
parent package: PKG-4b2a (`516cb8f2`, T061)

## Closed in this package

| task | verdict | record |
|---|---|---|
| T062 | **no change needed** — measured | this file, § T062 |
| T063 | **green** — mirrors re-projected, `--check` exit 0, projection 6/6 `ok` `idempotent=True` | this file, § T063 |
| T064 | **4 of 5 families zero-difference; the 5th shows defect D-1** (halted, handed up) | `SC-007-zero-regression.txt` |
| T065 | **green** — 141/141 framework+skill scripts follow the edited `pyproject.toml`; literal scan 0 in script bodies | `SC-011-version-source.txt` |
| T066 | **green** — rejected-unknown-option limb pinned, both snapshot files byte-unchanged | `T068-incident-unknown-option.txt` |

No implementation file was edited by this package. `scripts/`, `skills/`, `tests/`, `shared/`,
`templates/` are byte-identical to PKG-4b2a's head; `.specify/` was re-projected only through
`sync-mirrors.py --write` and came out byte-identical (no mirror changed).

## T062 — instructions budget

Measured before deciding, as the task requires:

| reading | value |
|---|---|
| live budget in the script (`INSTRUCTIONS_BUDGET_BYTES`, `scripts/bash/generate-instructions.sh:82`) | 34816 |
| live `.specify/instructions.md` size | **33766 B** |
| headroom under the script's own rule (`size >= budget` is "over") | **1049 B** |
| ambient section "Script Interface Contract" (what the backfill added) | **409 B** |
| template top-level `##` sections (`.specify/templates/instructions.md`) | 33 = `TPL_EXPECTED` |
| live top-level `##` sections | 34 = `LIVE_EXPECTED` |

old / new / measured / reason: `old = new = 34816`; `measured = 33766 B, headroom 1049 B,
ambient section 409 B`; `reason = the section fits the existing headroom, so the rule "raise only if
it does not fit" does not fire`. The smallest multiple of 1024 that would still leave ≥ 1024 B is
34816 itself — the value in the file — so even a raise would be a no-op.

`tests/contract/test_fast_fail_discipline.py`: both consumer counts (`TPL_EXPECTED = 33`,
`LIVE_EXPECTED = 34`) already match the measured tree, so nothing was re-pinned. Both pins are
green (`test_a7_section_counts_20_to_21_and_21_to_22`).

Note for the next package: the headroom is **1049 B** on today's tree, not the 1459 B `plan.md`
cites (that reading was taken at 33357 B, i.e. before the latest ambient growth). The rule still
holds, but the margin is now one ambient section away from firing.

## T063 — mirrors

    sync-mirrors.py --write   -> exit 0, no mirror changed (tree already projected)
    sync-mirrors.py --check   -> exit 0; six `projected[...] ok` rows and
                                 templates 22 / skills/external 415 / skills/internal 138 /
                                 agents 16 / scripts 118 / shared 95 files, all byte-identical
    script-interface-check.py --check-projection --root . --json
                              -> exit 0; candidates=0 applicable=0 exempt=0 violations=0;
                                 projection 6 rows, every one status=ok idempotent=True;
                                 findings []
    pytest -q tests/contract/test_mirror_parity_suite.py   -> green (inside the 910-pass run below)

## T064 / SC-007 — see `SC-007-zero-regression.txt`

Method and per-family readings are in that file. Summary:

| family | PRE rc / POST rc | output |
|---|---|---|
| shell-cli (`check-prerequisites.sh --paths-only --include-spec`) | 0 / 0 | **DIFFERS — defect D-1** |
| shell-lib (`common.sh --help`) | 0 / 0 | differs only by the newly added `--help` path (permitted) |
| py-engine (`script_interface_cli.py --emit-rule`) | 0 / 0 | byte-identical (729 B) |
| skill-shell (`scaffold-ci.sh --root . --platform nosuchplatform`) | 2 / 2 | identical |
| skill-py (`wp-gate.py --stage x --check`) | 2 / 2 | identical |

No family writes to its tree on either side (sha256 snapshot before/after).

## T065 / SC-011 — see `SC-011-version-source.txt`

On a copy tree (`/var/tmp/pkg4b2b/version`, archive `516cb8f2` + working sources, `0.0.22` →
`0.0.99`): scripts/python 39/39, scripts/bash 15/15, skills py 71/71, skills bash 16/16 all print
the mutated version in `<script-name> <version>` shape; 141/141 framework+skill scripts react.
`.specify` mirrors 140/149 (the 9 non-conforming are declared regeneration artefacts, named in the
record); tests/src/install 6/455 are fixtures. Repository-wide literal scan: 2 hits, both in
`tests/contract/test_script_interface_contract.py` (`:1227`, `:1324`) as fixture `pyproject.toml`
writers that must carry a literal to test the reader; zero in any script body.

## T066 — see `T068-incident-unknown-option.txt`

On the incident script `scripts/bash/generate-instructions.sh`, run from a copy tree: unknown
option → rc 2, 0 B stdout, 7 stderr lines; `--version` answers before any reconcile
(`generate-instructions.sh 0.0.22` with a `.git`, `generate-instructions.sh unknown` without one).
Both snapshot files (`instructions.md` d971fe82…, `.gitignore` fcf24bb7…) byte-unchanged, backup
count 1 → 1. The main work tree never ran a reconcile-capable invocation.

## Defect D-1 — `check-prerequisites.sh` returns empty paths after the bash backfill

**Severity: behavioural regression on a declared call; silent (exit code unaffected).**
Found by T064; **not repaired** (a semantic change inside the landed `scripts/bash` deliverable,
which this package's brief excludes; and at least two readings exist, so it is a judgement to hand
up, not a correction).

Observed, on the real work tree, with no flags the user would not type:

    $ bash scripts/bash/check-prerequisites.sh --paths-only --include-spec
    .../scripts/bash/script-interface.sh: line 360: git_repo_root: command not found
    .../scripts/bash/script-interface.sh: line 361: git_current_branch: command not found
    .../scripts/bash/script-interface.sh: line 363: is_git_repo: command not found
    [specify] Warning: Git repository not detected; skipped branch validation
    REPO_ROOT:
    BRANCH:
    REQUIREMENTS_DIR: /.specify/specs/
    ...
    rc=0

Before the backfill (`git archive efa3a270`) the same call printed every field populated
(`REPO_ROOT: /`, `BRANCH: main`, `REQUIREMENTS_DIR: //.specify/specs/main`, …), also rc 0.

Cause (two limbs; both measured, neither inferred):

* **A — the publish list does not carry the helpers the code needs.** `common.sh` now keeps its
  whole body in `_script_interface_library_body()` and publishes only the names listed at its tail
  (`_script_interface_library_link …`). The three `git_*` names are not listed, and they used to
  arrive through the host shell library that the body sources — inside a subshell whose content is
  filtered by that same list. Measured after a bare `source`:
  PRE `git_repo_root: function` / POST `git_repo_root: undefined`.
  Repair site: the list at the tail of `scripts/bash/common.sh`, or the decision not to inherit
  the host library's helpers at all (then `get_feature_paths` has to stop calling them).
* **B — the entry/link decision reads a variable that can be empty.** `script-interface.sh:74`
  (`_SCRIPT_INTERFACE_ENTRY="${_SCRIPT_INTERFACE_ENTRY:-}"`) is compared with `BASH_SOURCE[0]` at
  `:310` to choose "run the body" vs "publish the helpers". Two files reproduce the hazard
  without a repository; the exact minimal reproduction and the observation are in
  `SC-007-zero-regression.txt` § item (2), limb B.

Blast radius today: `check-prerequisites.sh` (the preflight every `/speckit.*` flow runs) reports
an empty prerequisite set while exiting 0. Nothing in this package's tests observes it, because the
contract tests probe flag surfaces and exit codes, not the path payload of the JSON/text modes.

## Test readings

    pytest -q tests/contract/test_script_interface_contract.py \
              tests/unit/test_script_interface_cli.py \
              tests/contract/test_mirror_parity_suite.py      -> 910 passed, 0 failed
    pytest -q tests/contract/test_fast_fail_discipline.py     -> 103 passed, 1 failed
              (test_g9_total_equals_frozen_baseline, 27 vs frozen 23 — pre-existing,
               listed in test-evidence/baseline-failed.txt:6)
    sync-mirrors.py --check                                   -> exit 0
    script-interface-check.py --check-projection --root .     -> exit 0, 6/6 idempotent=True

## Anomalies carried out of this package

* `ANOMALY:` D-1 — the landed bash guard/backfill makes `scripts/bash/check-prerequisites.sh`
  print empty paths (with `git_repo_root: command not found`) on exit 0, where it printed
  populated paths before; SC-007's "diff is zero except added flag paths" therefore does not hold
  for the shell-cli family.
* `ANOMALY:` the instructions budget headroom is 1049 B (not the 1459 B `plan.md` cites); the
  raise rule does not fire today, but the margin changed.

## Notes for the next package

* Repair D-1 before any downstream flow relies on `check-prerequisites.sh`'s path payload; the
  two candidate readings are named above and the fix belongs in `scripts/bash`, with the mirror
  re-projection and the bash contract tests re-run afterwards.
* T062 needs re-measuring (not re-deciding) if another ambient section lands: the trigger is
  `size >= 34816`, i.e. 1050 B from today's tree.
