---
id: "20261106T080845Z-speckit-clarify"
unit_id: "/speckit.clarify"
unit_type: "command"
run_id: "r20261106T090000Z-086a"
scope: "local"
probe: "speckit-clarify-wrapup"
kind: "internal"
slice: "commands"
feature: "086-script-interface-contract"
partial: false
created: "2026-11-06T08:08:45Z"
summary: "086 clarify (Mode A, zero questions): resolved nine pre-plan open points and encoded them into requirements.md — candidate surface derived from git ls-files minus .gitignore plus a coverage assertion;"
---

## Review
086 clarify (Mode A, zero questions): resolved nine pre-plan open points and encoded them into requirements.md — candidate surface derived from git ls-files minus .gitignore plus a coverage assertion; bash/python applicability judged by run semantics (does the entry actually do work when executed) rather than source literals; owner doc fixed at shared/definitions/script-interface-definitions.md; --version form <script-name> <framework-version> read from pyproject.toml; check wired as scripts/python/script-interface-check.py + tests/contract/test_script_interface_contract.py; declared exceptions registered in the owner doc and recomputed by the checker; zero-side-effect evidence taken on an out-of-repo copy tree with before/after sha256 snapshots. 31 FR / 12 SC.

## Optimization Points
- 1) The clarify executor wrote eight new FR rows as '- **FR-024**（...）：' with no ASCII colon after the bold id, so the pre-analyze checker reported 46 false dangling-id errors; the driver normalized the rows. The checker's definition regex is the single owner of that shape but nothing tells authors about it. 2) The clarify executor again skipped Wrap-up accounting; driver backfilled run-determination/exec-quant/feedback. 3) Two requirements-stage fact readings were falsified by measurement: 0 (not 2) python scripts implement --version, and refresh-tools.sh has usage() but no --help branch; grep hits must not be treated as implementation evidence. 4) Driver observed goal-utils.py silently ignoring --scope/--spec-dir placed before the subcommand, writing a global goal; correct order is after the subcommand. This is the same silent-argument class the feature targets.
