# PKG-5b stage status — the block position, the one pair, and the version line (T073–T077)

date: 2026-11-08
line: `flow_class=execution; source=declaration; marker=null; error=-`
parent package: PKG-5b base (`b7de8202`, T067–T072)
stage: `implement`; SPINE_WRITE_MODE=direct (the spine was NOT written by this package — see § Spine)

## Closed in this package

| task | verdict | record |
|---|---|---|
| T073 | **green** — the guard block is the first executable block of every consumer; the insertion rule is section 4.1 of the owner page | § T073, `test_t073_*` |
| T074 | **green** — one pair function, three limbs, non-vacuous, carrying the help-wins comparison | § T074, `test_t074_*` |
| T075 | **green** — 748/748 candidates, pair identical after every flag run, 0 moved | `SC-001-zero-side-effect.txt` |
| T076 | **green** — `script_interface_version_text` published; its body inlined through `__SCRIPT_INTERFACE_VERSION_BODY__`; a copy with no library answers | § T076, `test_t076_*` |
| T077 | **green** — `--no-such-flag` exits 2 with error + usage on stderr on the live face, nothing written | `T075-rejection-face.txt` |

Files edited (all inside the declared territory):

    scripts/bash/script-interface.sh                           T076: the published version line
    scripts/python/sync-mirrors.py                             T076: the sentinel's body source
    shared/definitions/script-interface-definitions.md         T073: section 4.1
    tests/contract/test_script_interface_contract.py           T073/T074/T076/T077 assertions
    .specify/... (task ticks, this file, the two evidence files, and the mirrors that
    `sync-mirrors.py --write` re-projected — no `.specify/` file was hand-edited)

## T073 — the insertion position

Section 4.1 of `shared/definitions/script-interface-definitions.md` states the rule: the guard
block MUST be the consumer's FIRST executable block and MUST precede any `source`/`.`, any
`mkdir`/`rm`/`mv`/`cp`, any `git` write, any manifest/template generation, and the script's own
parsing and main action. The position is judged TEXTUALLY: above the block only a shebang,
comments and blank lines.

Measured over the consumers (`git ls-files '*.sh'` filtered by "sources
`script-interface.sh` and calls `script_interface_guard define`"):
`test_t073_the_guard_block_is_the_first_executable_block_of_every_consumer` — green.
The owner-page statement is pinned by `test_t073_the_owner_page_states_the_insertion_rule`.

## T074 — the one pair

`_tree_snapshot(root)` in `tests/contract/test_script_interface_contract.py` returns ONE value:
`(git status --porcelain lines, {path: sha256} for every *.sh/*.py, {path: sha256} for the
`.specify/` manifest)`. It is the only instrument both the zero-side-effect assertion and the
help-wins comparison run on, so a comparison cannot silently drop a limb.

Two things about it are load-bearing and were both fixed by measurement here:

* `.git/` is not part of the manifest — version-control bookkeeping is not a script's side
  effect, and a populated index (which `git status` itself writes as its own cache) made the
  limb move on its own;
* the `.specify/` limb takes EVERY file under it, not only `*.sh`/`*.py` — that is what the
  control (`test_t074_..._it_notices_a_write`, which writes `.specify/touched.md`) asserts.

## T075 — SC-001 at closure scale

See `SC-001-zero-side-effect.txt`. Headline:

    denominator                          748 candidates (git ls-files '*.sh' '*.py')
    pair identical before/after          748 / 748
    pairs that moved                         0
    families (all disjoint, all complete)    12

Whole-repo in one pass does not close inside one window: the tree fingerprint must be taken
before the FIRST probe and compared after the LAST. Twelve family trees were cloned once and
each family measured start to finish, so the frame stays a complete partition — no sampling.

## T076 — the version line, self-sufficient

`script_interface_version_text` (in `scripts/bash/script-interface.sh`) prints
`<basename of $1> <version read from the nearest pyproject.toml under a directory carrying
.git>`, and `unknown` when the bounded upward search finds no such root. Its constants are
defaulted INSIDE the body (`${_SCRIPT_INTERFACE_VERSION_SOURCE:-pyproject.toml}`,
`${_SCRIPT_INTERFACE_MAX_LEVELS:-12}`) so the spliced copy does not depend on the library's
file scope.

`scripts/python/sync-mirrors.py` reads that body from the LIBRARY (`GUARD_LIBRARY_SOURCE`) and
splices it into the emitted `bash-version-guard` block at the
`__SCRIPT_INTERFACE_VERSION_BODY__` sentinel; the engine also strips a previously projected
block by reconstructing it through the same `project_source` dry run, so projection is
idempotent and its inverse is exact.

Proof, on a downstream copy that has neither the library nor the source tree:
`scripts/guard-only.sh --version` -> `guard-only.sh 9.9.9` (9.9.9 read from that copy's own
`pyproject.toml`); `--help` -> exit 0 with `usage:` / `options:` / `side-effects:` /
`exit-codes:`. Green: `test_t076_the_projection_inlines_the_body_through_the_sentinel` and
`test_t076_the_version_text_function_is_published_and_defaults_its_own_constants`.

## T077 — the rejection face

See `T075-rejection-face.txt`. `--no-such-flag` -> exit 2, `error: unrecognized option: ...`
first line of stderr, the full four-label usage body on stderr, empty stdout, no write target
created, snapshot pair identical. `--help` beats the declared write option in both orders.

## Verification readings

    pytest -q tests/contract/test_script_interface_contract.py
              tests/unit/test_script_interface_cli.py
              tests/unit/test_workspace_guard.py            -> 118 passed in 22.68s
    sync-mirrors.py --check                                 -> exit 0 (12 `ok` rows)
    workspace-guard.py --check <snapshot>                   -> clean, exit 0
                                                               (taken after the suite ran)

## Anomalies handed up (not repaired here)

1. **Interpreter resolution in the checker (pre-existing, outside T073–T077).**
   `_python_for()` in `scripts/python/script-interface-check.py` answers `python3` for a
   `#!/usr/bin/env python3` shebang, but `_runner_for()` prefixes it with `bash`, so every
   `.py` candidate is read as a shell script and answers none of the flags. 40 of the 40
   `.py` candidates in `scripts/` were measured that way; the sweep at closure scale is
   general. Also measured: on this host, `bash <file>` reads ANY file as shell regardless of
   shebang, so the same effect shows up in the live face (`/var/tmp` probe). The owner task
   for interpreter resolution is not in this package; reported, not fixed.
2. **The checker's own closure run does not finish.** `script-interface-check.py` copies the
   measured tree once into a sandbox under `/var/tmp` and captures the tree fingerprint
   (including `.git`, ~102 MB) before and after EVERY probe. Measured: 748 candidates, 37
   reached inside 30 minutes of budget (1806 s at `--budget-seconds 1800`), the rest
   `probe-budget-exhausted`; extrapolated ~47 s/candidate, i.e. ~10 h for the full screen.
   Not a T073–T077 finding; it is why T075 was measured with the T074 pair in twelve family
   trees instead of by aggregating the checker's rows.
3. **Terminal-taking candidates in the live face.** `tests/contract/test_goal_targets_engine.py`
   documents `$EDITOR`/`view` in its docstring; read as shell, the backticks reach `view`
   (vim) and wait on a terminal. The T075 driver pins `EDITOR`/`VISUAL`/`GIT_EDITOR` to `true`
   and caps each invocation at 30 s; this candidate is the one timed-out row and its pair did
   not move.
4. **Workspace drift (external).** The workspace snapshot taken at package start
   (`/var/tmp/086-5b-workspace.json`) no longer matches the tree: branch
   `089-script-interface-contract` -> `202-script-interface-check`, ~110 new
   `NNN-script-interface-check` branches and spec dirs. Nothing in this package creates a
   branch or a spec dir (probes ran only in `/var/tmp` clones); this is concurrent activity in
   the shared worktree. Treated as a STOP condition for probes (none of the new carriers
   were touched) and reported rather than repaired. A fresh snapshot
   (`/var/tmp/086-5b-workspace-final.json`) taken after all probes is `clean`.

## Spine

`.specify/state/089-script-interface-contract.md` was NOT written: the package brief marks it
read-only for this executor. `SPINE_WRITE_MODE=direct` is recorded here for the driver.
