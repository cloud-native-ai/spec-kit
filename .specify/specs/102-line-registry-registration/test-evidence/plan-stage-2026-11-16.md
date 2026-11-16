# Plan stage — evidence record (2026-11-16)

Full command output for every gate is in `plan.jsonl` (row `stage=plan`, `row_type=stage-status`). This file carries the readings those verdicts rest on and the dispositions of the same-author audit.

## Execution Premises — measured evidence

| EP | Reading | Command / source |
|----|---------|------------------|
| EP-001 | `Python 3.11.0rc1`; declared floor `requires-python = ">=3.8"`; scanner design imports stdlib only | `python3 --version`; `pyproject.toml:5` |
| EP-002 | `pytest 9.0.3`; unique entry `scripts/bash/run-tests.sh` (parallel default); fixture isolation via `SPECIFY_LINE_REGISTRY_DIR` | `python3 -m pytest --version`; `scripts/bash/run-tests.sh:1-51`; `tests/fixtures/line_fixtures.py:50-58` |
| EP-003 | Both engine candidates answer `--version` → `line-registry.py 0.0.22`; `register` requires `--project-dir`/`--repo-root`; `deregister` requires `--reason`; `closed` terminal | `--version` on both paths; `line-registry.py:42-43,576-600,818,895-900` |
| EP-004 | Stale bound `900` (`DEFAULT_STALE_BOUND_SECONDS`); closed entries filtered from the current view; lifecycle executed below | `status-digest.py:74,985-989,1097`; S-7 run |
| EP-005 | `GNU bash 5.1.16(1)-release`; shared guard `scripts/bash/script-interface.sh` present and consumed by `run-tests.sh` | `bash --version`; `run-tests.sh:41-51` |

## Registry / digest lifecycle (quickstart S-7, executed)

Scratch registry: `.specify/.tmp/line-registry-registration/registry` (git-ignored); removed at the end of the same round.

| Step | Reading | Exit |
|------|---------|------|
| digest on empty registry | `nothing-running` | 3 |
| `register` `probe-line-20261116` / `r20261116T090000Z-abcd` | entry `state=active`, `last_event=registered` | 0 |
| digest while active | row naming `probe-line-20261116`, state `活跃` (active) | 0 |
| `deregister --reason completed` | entry `state=closed`, `last_event=completed`, `run_history` `outcome=completed` | 0 |
| digest after close | `nothing-running` | 3 |

Disclosure: an earlier probe command in this session registered a one-off `probe-json-20261116` entry in the operator's environment registry by omitting the isolation variable. The entry was created by this run and was deleted immediately (`probe-json-20261116.json` removed); no other environment-registry entry was touched. The corrected S-7 block sets the variable on every engine call.

## Live scan baseline (planning-time measurement)

Read-only grep over the declared roots `scripts/bash/`, `scripts/python/`, `skills/`:
- marker member 1 (`[[STR-004]]`): 0 hits.
- marker member 2 (`[[STR-005]]`): 4 hits, all `.md` under `skills/external/*/references/` (`efficiency-model.md:91,92`, `stage-prompts.md:165,206`) — excluded by the judged-file surface (`.sh`/`.bash`/`.py` or shebang).
- `line-run-required` marker: 0 hits; `line-run.sh` references: 0 hits.

The literals are owned by `requirements.md` § Shared Strings and the scanner constants; they are not restated here.

## Mirror baseline (measured before any edit)

`python3 scripts/python/sync-mirrors.py --check` → rc 2:
- `DIFF`: `.specify/skills/coaching-skills/SKILL.md`, `.specify/skills/coaching-skills/data-model.md`, `.specify/skills/coaching-skills/references/prompt-templates.md`, `.specify/skills/create-skills/SKILL.md`, `.specify/skills/sdd-loop-driver/references/cli/qodercli.md` (pre-existing, outside this feature's pairs).
- `ORPHAN`: `.specify/scripts/line-registry.py`, `.specify/scripts/stage-runner.sh` (pre-existing untracked copies; not committed and not reverted, FR-023).

Acceptance for this feature is **no NEW drift on the pairs it touches**, not "all green".

## Gate readings

| Gate | rc | Verdict |
|------|----|---------|
| `pre-analyze-check.py --stage plan --repo .` | 0 | `decision=pass`, errors=0, advisories=41 (all `missing-path` for planned-new files and the git-ignored fixture root) |
| `validate-decision-tensions.py --spec <spec>` | 0 | 0 error / 0 warning, 2 records |
| `sync-mirrors.py --check` | 2 | baseline drift only (above); no pair of this feature was edited in the plan stage |
| `regen-command-copies.py --check` | 0 | ok |
| `flow-class-check.py --action check` | 0 | clean (91 units) |
| plan integrity | 0/0 | exactly one `# Implementation Plan:` heading, one `Requirement → Feature` stamp, zero `[UPPER_SNAKE_CASE]` residue |
| `doc-consistency-check.py` | not evaluated | execution-class plan carries no Document Structure section; the checker's structure action applies to expression-class artifacts |
| tests | not run (docs-only) | `status=not-run-docs-only`; no executable or test path changed |

## Same-author audit (objective-analysis gate) and dispositions

Two disjoint read-only scopes ran in fresh context: (a) Constitution Check + clarification binding + premises; (b) post-generation quality gate. Findings and dispositions:

| Finding | Disposition |
|---------|-------------|
| `features.md` row 102 still `Draft` while the plan claimed it advanced (caught by both auditors) | Corrected by performing the integration: row now `Planned`, parent detail note added; Gate II's evidence is now true |
| quickstart S-7 omitted the registry isolation variable on the engine calls, and used bare `/tmp` elsewhere | Block rewritten to the sanctioned `.specify/.tmp` root with the variable on every call; re-executed with pasted output; scratch removed |
| S-4's negative leg dropped the marker, making "clean" trivial | Negative leg now keeps the marker and adds the wrapper invocation, so only compliant-invocation detection explains the verdict |
| wiring contract C-10 named only engine candidate 1 | Both A-17 candidates named (downstream projects hold only candidate 2) |
| identity wording `git -C "$PWD"` read as conflicting with A-18 | Aligned to `git rev-parse --show-toplevel`; the toplevel, never `$PWD`, is the identity |
| four Constitution Check principle names truncated | Restored verbatim |
| scan contract E-4 and data-model E2 restated marker/regex literals | Replaced by constant names and pointer statements |
| `batch-apply-…` character count 36 → 34 | Corrected |

No clarification A-14…A-24 was reopened, and no new external dependency, daemon, second registry or status spine was introduced.

**Anomaly line**: no anomaly remains open — every audit finding above is a single-reading correction consistent with the bound clarifications, except the registry-row claim, which was a pending integration step rather than a contradiction and has been executed.
