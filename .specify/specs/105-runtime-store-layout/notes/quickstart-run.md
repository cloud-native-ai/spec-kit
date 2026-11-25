# Quickstart run — 105 runtime-store-layout (T037)

- Date: 2026-11-25
- Run: `r20261125T022857Z-06dd` (implement package P5)
- Method: Scenario 0 and Scenario 7 are **route (a)** — executed now, real output below.
  Scenarios 1–6 and 8 are **route (b)** — each is pinned by the named test, with its premises
  restated so the next stage re-measures instead of inheriting.
- Teardown: none of the route-(b) scratch directories were created, so
  `.specify/.tmp/quickstart-105/` never existed; the temporary capture files under
  `.specify/.tmp/` were deleted after this record was written.

## Scenario 0 — read the baseline (route a)

```console
$ git ls-tree -d 23938f22e:.specify/memory
040000 tree a2f1ecaf2066518465c828ebcadc1af8cdf0d101	coaching
040000 tree c0807237e7de9d6bdab02105f49470e6e606352c	evidence
040000 tree c4c9f61cfde1adeede6178203b0c30f4c7965f68	exec-quant
040000 tree ccfc6a5f93f1ad75444bd3f0dbf73f6282c767d5	feedback
040000 tree d0da05a5a93d5bacb46f704068890d8d8f0813b9	housekeeping
040000 tree 7e5597c0a36d3b1561884bee334fea2dc305d22e	knowledge
040000 tree c94744f56159061469ada558d7d260a8414ff915	renumber
040000 tree 7fdea5528286614d6e4656664c8cf4e3813dd26c	retention
040000 tree 53136a3d83060c8297574cec2fd845f16293c6dd	session
040000 tree 4d927e0b07ba91c7767c9e6eec779893fe973bc8	todo
040000 tree c96de145f3e73741d87fdf964d57883cc70708fe	tools
040000 tree 6d9f54c01c7b13bf3a7d82cf23551c81516d015c	trigger
exit=0
```

- Reading: the frozen baseline still carries **12** subdirectories at `23938f22e`; the current
  tree carries **zero** tracked paths under the retired root:

```console
$ git ls-files .specify/memory | awk -F/ '{print $3}' | sort | uniq -c | sort -nr
(no output)
exit=0
```

```console
$ git check-ignore -v .specify/memory/sanitize/findings.json \
    .specify/memory/trigger/telemetry.jsonl .specify/tools/system.json
.specify/.gitignore:23:sanitize/	.specify/memory/sanitize/findings.json
.specify/.gitignore:16:tools/*.json	.specify/tools/system.json
exit=0
```

- Reading (corrected against the plan-stage snapshot): the plan-stage reading pinned three hits
  (`memory/sanitize/`, `memory/trigger/telemetry.jsonl`, `tools/`). Post-feature the *rules* are
  `sanitize/`, `trigger/telemetry.jsonl`, `tools/*.json`:
  - `sanitize/` is an unanchored gitignore pattern, so it also matches a `sanitize/` directory at
    any depth — the retired-path probe still matches that rule; the store itself is what it governs
    (whole-store machine-regenerable cache, C-4);
  - the retired `memory/trigger/telemetry.jsonl` path **no longer matches** (the new rule is
    anchored to `.specify/trigger/telemetry.jsonl`, which does match — control below);
  - `.specify/tools/system.json` matches the narrowed `tools/*.json` rule (records stay tracked).
- Control (the current paths the rules are written for):

```console
$ git check-ignore -v .specify/sanitize/findings.json \
    .specify/trigger/telemetry.jsonl .specify/tools/system.json
.specify/.gitignore:23:sanitize/	.specify/sanitize/findings.json
.specify/.gitignore:27:trigger/telemetry.jsonl	.specify/trigger/telemetry.jsonl
.specify/.gitignore:16:tools/*.json	.specify/tools/system.json
exit=0
```

## Scenario 7 — dogfood: this repository converges (route a)

```console
$ PYTHONPATH=src /usr/local/bin/python3 -c "from specify_cli import main; main()" migrate --workspace . --apply
migrate plan — mode=apply, workspace-kind=framework-source, items=0
outcome: clean (exit 0)
pointer: goal/team archive migration stays with /speckit.anchor migrate-archive
exit=0
```

- Reading: a post-dogfood apply emits **zero items** and exits `clean`; its receipt
  `.specify/migrate/receipts/20261125T070056Z-e5d8a761.json` records `status=completed`,
  `outcome=clean`, `storeLayout {stores 0, resolved 0, refused 0, blocked 0, container absent}` —
  one receipt file per run, alongside the two T033 receipts.

```console
$ test ! -e .specify/memory ; echo $?
0
$ ls .specify | sort
agents  anchoring  archive  coaching  constitution.md  derive  evidence  exec-quant  features
features.md  feedback  gate.yaml  glossary.md  goals  history  housekeeping  instructions.md
knowledge  migrate  register.md  renumber  retention  scripts  session  shared  skills
skills.md  source.json  specs  state  studies  teams  templates  todo  tools  tools.md
trigger  workflow
```

- Reading: the retired root is absent. **13** of the 14 declared store roots are present; the
  `sanitize` store root is absent because it is created lazily by its owner (C-1: runtime stores
  are never seeded), which is the declared behaviour, not a missing root. The quickstart's "14
  store roots" comment is a maximally-populated expectation; the measured reading is 13 + lazy
  `sanitize`, recorded as the platform fact.

```console
$ python3 scripts/python/sync-mirrors.py --check        # literal quickstart form
… ok lines …
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
exit=2

$ /usr/local/bin/python3 scripts/python/sync-mirrors.py --check
ok    scripts/ == .specify/scripts/ (132 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (116 files, byte-identical)
exit=0

$ /usr/local/bin/python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
exit=0
```

- Reading: the profile `python3` has no `typer`, so the literal command's internal regen step
  cannot run and the check reports a false DRIFT (rc 2) — the platform fact already recorded in
  P4 (`test-evidence/u4-p4-independent-checks.txt`, R-10: the same interpreter rule binds
  `sync-mirrors.py`). Under the pinned interpreter (`/usr/local/bin/python3`) every pair is
  byte-identical and both checks exit 0. No mirror was hand-edited; nothing was regenerated here.

## Scenarios 1–6, 8 — route (b), pinned tests and premises

| Scenario | Pinned by | Premises re-measured at this run |
|---|---|---|
| S-1 client upgrade (old layout only) | `tests/integration/test_store_layout_migration_us1_us2.py` (legacy: dry-run zero-write, apply byte-identical, container absent, rerun no-op) | the fixture is declaration-built at run time (`tests/fixtures/store-layout-105/builders.py`); no historical snapshot |
| S-2 dual content refusal | same module, `test_dual_content_refuses_with_both_paths_and_leaves_both_trees` | both sides hashed before/after; both paths and the repair entry named |
| S-3 fresh initialization | `tests/integration/test_init_new_layout.py` | empty-dir fixture; package seed `seed/`; anchors at `.specify/` |
| S-4 memory and determination under the new roots | `tests/integration/test_memory_preservation.py` | fixture workspace after init; entry lands under `.specify/session/`, recall returns it |
| S-5 dispatch with a memory-recall child | `tests/integration/test_dispatch_injection_paths.py` | seven downlink fields / four injections / five uplink elements; reverse-token boundary |
| S-6 tools domain | `tests/contract/test_tools_domain.py`, `tests/contract/test_specify_gitignore_template.py` | `git check-ignore` fixture; template and installed copy byte-identical |
| S-8 live-reference containment | `tests/contract/test_store_layout_live_refs.py` | allowlist equality both directions; three product classes measured |

Every route-(b) scenario was re-executed inside this package's test runs (P5 T035/T041 readings),
so the pinned tests are green on the current tree.
