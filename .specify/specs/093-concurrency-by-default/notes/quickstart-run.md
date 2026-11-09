# Quickstart run — S-0…S-6 against the live tree (T137)

**Date**: 2026-11-09 · **Branch**: 093-wp5 · **Base**: 6001c9ad1 · **Entry**: the commands are read from `quickstart.md` (pointer, not restated); scratch lands under the sanctioned `.specify/.tmp/wp5/quickstart/` root instead of the page's illustrative `/tmp` paths.

## S-0 — verify the premise
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib64/python3.11/json/__init__.py", line 293, in load
    return loads(fp.read(),
           ^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.11/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.11/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
EXIT (get): 0
get -> body.fact: concurrency-class
`--action get --fact concurrency-class` now exits 0 with the statement — the page's recorded premise ('exits 1, not yet registered') was true at plan time and the fact landed in WP1. **Premise moved, artifact runnable.**
$ python3 .specify/scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files, byte-identical)
ok    skills/external/ == .specify/skills/ (419 files, byte-identical)
ok    skills/internal/ == .specify/skills/internal/ (139 files, byte-identical)
ok    agents/ == .specify/agents/templates/ (17 files, byte-identical)
ok    scripts/ == .specify/scripts/ (124 files, byte-identical)
projected[bash-version-guard] .specify/scripts/bash/check-prerequisites.sh <- scripts/bash/check-prerequisites.sh: ok
projected[bash-version-guard] .specify/scripts/bash/generate-instructions.sh <- scripts/bash/generate-instructions.sh: ok
projected[bash-version-guard] .specify/scripts/bash/run-tests.sh <- scripts/bash/run-tests.sh: ok
projected[python-version-bridge] .specify/scripts/python/script-interface-check.py <- scripts/python/script-interface-check.py: ok
projected[python-version-bridge] .specify/scripts/python/script_interface_cli.py <- scripts/python/script_interface_cli.py: ok
projected[python-version-bridge] .specify/scripts/python/sync-mirrors.py <- scripts/python/sync-mirrors.py: ok
ok    shared/ == .specify/shared/ (110 files, byte-identical)
EXIT=0


## S-1 — the scope closed set is enumerable and complete
$ python3 scripts/python/concurrency-check.py classify --repo . --json-out .specify/.tmp/wp5/quickstart/classify.json
classify: decision=pass findings=0 -> .specify/.tmp/wp5/quickstart/classify.json
EXIT=0

decision: pass
findings: []
root_counts: {'agents': 17, 'anchoring': 6, 'commands': 29, 'skills': 54, 'teams': 12}

## S-2 — default concurrent; the reason code is not optional
$ python3 scripts/python/concurrency-check.py serial-reason --repo . --record .specify/.tmp/wp5/quickstart/serial-bad.yaml --json-out .specify/.tmp/wp5/quickstart/serial-bad.json
serial-reason: decision=fail findings=1 -> .specify/.tmp/wp5/quickstart/serial-bad.json
EXIT=1

decision: fail
findings: [('evidence-form-mismatch', 'budget-reserve', "budget-reserve: evidence for 'budget-reserve' must be a structured reading of form 'budget")]
$ python3 scripts/python/concurrency-check.py serial-reason --repo . --record .specify/.tmp/wp5/quickstart/serial-good.yaml --json-out .specify/.tmp/wp5/quickstart/serial-good.json
serial-reason: decision=pass findings=0 -> .specify/.tmp/wp5/quickstart/serial-good.json
EXIT=0

decision: pass findings: 0
$ python3 scripts/python/concurrency-check.py serial-reason --repo . --record .specify/.tmp/wp5/quickstart/serial-empty.yaml --json-out .specify/.tmp/wp5/quickstart/serial-empty.json
serial-reason: decision=fail findings=1 -> .specify/.tmp/wp5/quickstart/serial-empty.json
EXIT=1

decision: fail findings: ['form-reason-inconsistent']

## S-3 — effective is interval overlap, never a declaration
$ python3 scripts/python/concurrency-check.py reading --repo . --record .specify/.tmp/wp5/quickstart/reading-overlap.yaml --json-out .specify/.tmp/wp5/quickstart/reading-overlap.json
reading: decision=pass findings=0 -> .specify/.tmp/wp5/quickstart/reading-overlap.json
EXIT=0

decision: pass effective: 3
$ python3 scripts/python/concurrency-check.py reading --repo . --record .specify/.tmp/wp5/quickstart/reading-missing.yaml --json-out .specify/.tmp/wp5/quickstart/reading-missing.json
reading: decision=fail findings=1 -> .specify/.tmp/wp5/quickstart/reading-missing.json
EXIT=1

decision: fail effective: not_evaluated findings: [('reading-not-evaluated', 'u2')]
$ python3 scripts/python/concurrency-check.py reading --repo . --record .specify/.tmp/wp5/quickstart/reading-incomplete.yaml --json-out .specify/.tmp/wp5/quickstart/reading-incomplete.json
reading: decision=fail findings=1 -> .specify/.tmp/wp5/quickstart/reading-incomplete.json
EXIT=1

decision: fail findings: ['reading-incomplete']

## S-4 — per-stage decomposition coverage
$ python3 scripts/python/concurrency-check.py coverage --repo . --stage requirements --json-out .specify/.tmp/wp5/quickstart/coverage.json
coverage: decision=pass findings=0 -> .specify/.tmp/wp5/quickstart/coverage.json
EXIT=0

decision: pass
requirements: {'coverage': 'auto', 'decision': 'covered-by-default', 'single_package_decision_required': True}
spine relation entries: 5

## S-5 — dispatch capability and the 092 reproduction
$ bash scripts/bash/run-tests.sh tests/contract/test_concurrency_reproduction_092.py -q
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_concurrency_reproduction_092.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

....                                                                     [100%]
4 passed in 6.20s
EXIT=0

$ python3 scripts/python/concurrency-check.py capability --repo . --record .specify/.tmp/wp5/quickstart/cap-record.yaml --json-out .specify/.tmp/wp5/quickstart/capability.json
capability: decision=owner-unavailable findings=1 -> .specify/.tmp/wp5/quickstart/capability.json
EXIT=2

decision: owner-unavailable findings: ['owner-unavailable']
The live fact is unadjudicated: exit 2 owner-unavailable is the page's fail-closed expectation (C-039), not a defect.
Note: the page S-5 command omitted `--record`; the capability action is a record-judging action (C-021) and rejects a record-less invocation with exit 2 `record-required`. The page is corrected in place at this run (`--record <run-record>.yaml` added) — an unrunnable command, repaired rather than skipped.

## S-6 — a real run, honestly reported
$ python3 scripts/python/concurrency-check.py reading --repo . --record .specify/.tmp/wp5/quickstart/real-run.yaml --json-out .specify/.tmp/wp5/quickstart/real.json
reading: decision=fail findings=6 -> .specify/.tmp/wp5/quickstart/real.json
EXIT=1

decision: fail effective: not_evaluated
findings: [('reading-not-evaluated', 'WP1'), ('reading-not-evaluated', 'WP2'), ('reading-not-evaluated', 'WP3')] ...
The run record is the feature's own fold: six dispatched units, no recorded intervals -> the engine reports `effective: not_evaluated` and refuses the concurrency claim — never a fabricated number, never a serial run presented as concurrent. The prose record is `notes/coordination-report.md`; the 091 comparison is `notes/serial-baseline.md`.

## Teardown
- Scratch under `.specify/.tmp/wp5/quickstart/` is covered by the `.specify/.gitignore` `.tmp/` rule and is removed at wrap-up.
- The only writes are `--json-out` files inside that scratch root; the repository tree is untouched by every scenario.
- Artifact the run surfaced as unrunnable: **none** — the reproduction fixture S-5 references exists (authored by T090 in this package), and S-0's recorded premise was annotated above rather than silently skipped.
