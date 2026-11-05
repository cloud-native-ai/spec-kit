# Plan-stage checks — 082-self-explanatory-integration

**Stage**: plan | **Date**: 2026-11-05 | **stage_base**: `506adf88` | **Branch**: `082-self-explanatory-integration`

## Baseline measurements

Each block is the command and what it printed in this repository during the stage. Where the same
command printed differently later in the stage, both readings are kept.

```text
$ python3 scripts/python/sync-mirrors.py --check     # first reading, start of stage
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
MISS  .specify/shared/definitions/self-explanatory-definitions.md
MISS  .specify/shared/guidelines/self-explanatory.md
MISS  .specify/shared/workflow/best-practice-optimization.md
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
exit=2   (captured with `>/dev/null 2>&1; echo $?` — the printed verdict and the process status
          disagree when the output is piped, so the status was re-captured separately)

$ python3 scripts/python/sync-mirrors.py --check     # second reading, later in the same stage
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
OK: all per-tool command copies match the source templates.
exit=0

$ for f in definitions/self-explanatory-definitions.md guidelines/self-explanatory.md \
           workflow/best-practice-optimization.md; do cmp -s "shared/$f" ".specify/shared/$f" \
    && echo "IDENTICAL shared/$f"; done
IDENTICAL shared/definitions/self-explanatory-definitions.md
IDENTICAL shared/guidelines/self-explanatory.md
IDENTICAL shared/workflow/best-practice-optimization.md

$ ls -la --time-style=full-iso shared/definitions/self-explanatory-definitions.md \
      .specify/shared/definitions/self-explanatory-definitions.md
2026-11-04 14:40:51.431892221 shared/definitions/self-explanatory-definitions.md
2026-11-04 14:40:51.431892221 .specify/shared/definitions/self-explanatory-definitions.md
# identical mtime — the timestamped backup below proves this stage did not write them
# (--check never writes; the plan stage never invoked --write)

$ python3 --version; git --version; python3 -m pytest --version
Python 3.11.11
git version 2.43.5
pytest 8.4.2

$ wc -c .specify/instructions.md; grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh
32739 .specify/instructions.md
38:INSTRUCTIONS_BUDGET_BYTES=32768

$ grep -cE '^### [IVXLC0-9]+\. ' templates/constitution-template.md .specify/memory/constitution.md
templates/constitution-template.md:17
.specify/memory/constitution.md:18
# mandate list: 10 entries (the double-landing suite's _skill_entry_names block parser)

$ python3 scripts/python/scan-confirmation-gates.py --json | python3 -c \
    'import json,sys; d=json.load(sys.stdin); print(d["total"], d["by_class"], d["violations"])'
27 {'governance_kept': 7, 'destructive': 20} []
# frozen baseline .specify/specs/050-proactive-flow-trigger/baseline-gates.json -> confirmationGates.total = 23
```

## Validators run

```text
$ python3 .specify/scripts/python/validate-requirements.py \
      .specify/specs/082-self-explanatory-integration/requirements.md
status: ok  |  [id-contiguous] pass (0)  [doc-order] pass (0)  [ref-resolvable] pass (0)
             [marker-count] pass (0)  [dup-id] pass (0)  [path-marker] pass (0)
scanned: 194 lines, 21 definition rows, 4 shared strings
0 error(s), 0 warning(s)
# requirements.md was NOT modified by this stage; this run confirms the plan read a valid spec.

$ python3 .specify/scripts/python/validate-decision-tensions.py \
      --spec .specify/specs/082-self-explanatory-integration --json
status: ok, errors: 0, warnings: 0, records: 2 (T-001, T-002)
# first run reported 2 HIGH findings (expected_sacrifice direction token / one-SC rule);
# both fixed in plan.md and the checker re-run to status ok.

$ python3 .specify/scripts/python/flow-class-check.py --action lookup \
      --unit-id "spec:082-self-explanatory-integration"
unit_id: spec:082-self-explanatory-integration | flow_class: execution | flow_type: - |
source: declaration | marker: null | neutral: false | exit 0
```

## Plan integrity gate

```text
$ grep -c '^# Implementation Plan:' plan.md          -> 1
$ grep -c 'Requirement → Feature' plan.md            -> 1
$ grep -nE '\[[A-Z][A-Z0-9_]+\]' plan.md             -> no match (residual placeholders: 0)
$ grep -n 'PLACEHOLDER\|[REPLACE\|[DATE]\|[SPEC]\|[PRINCIPLE' plan.md -> no match
$ grep -nE 'Wait —|Actually,|On second thought|Let me reconsider|re-reading:|Hmm,|I think|I realize|To be clear:|For the avoidance of doubt' <all artifacts> -> no match
```

## Executed scenarios (quickstart)

| Scenario | Executed | Observation |
|----------|----------|-------------|
| S-0 baseline | yes | readings above |
| S-1 `specify init` fresh project | yes | `shared/` sink created (`constants definitions guidelines patterns workflow`); the three documents absent because the installed CLI predates them |
| S-2 generator additive injection on a fixture | yes | `Injected missing template section(s): Beta, Gamma`; customized and project-specific sections preserved; second run reports "already carry all template sections" |
| S-3 regenerate this repository's live instructions | no (post-implementation) | premises listed in the scenario |
| S-4 guard suites | no (post-implementation) | the new subjects do not exist yet; today's suite would pass vacuously for this feature |
| S-5 mutation drill | yes | mutated copies lose the subject (`False`, `False`); real files verified untouched (`True`) |
| S-6 distribution listing | yes | prints nothing (same reason as S-1) |
| S-7 docs page pointers | yes | 3 referenced paths, 0 missing |

## Side effects of the stage, and their disposal

- `bash scripts/bash/generate-instructions.sh` was run once against the real tree to read the `BUDGET:`
  line. It wrote one backup, `.specify/instructions.md-2026-11-05-112729` (git-ignored by
  `.specify/.gitignore:19`); that file was created by this stage and was deleted after the reading. No
  tracked file changed: `git status --short .specify/instructions.md templates/ .specify/templates/
  .specify/scripts/ scripts/` is empty.
- All fixtures lived under `mktemp -d` and were removed with `rm -rf`.

## E-3 stage-status row

```json
{"stage": "plan", "row_type": "stage-status", "status": "not-run-docs-only", "selection_basis": "targeted-set-v1 with stage_base=506adf88: the plan stage produced only design documents (plan.md, research.md, data-model.md, contracts/, quickstart.md, feature-ref.md, test-evidence/) plus the feature index/detail status advance; no executable surface was changed, so the selection program yields the docs-only branch (spec: 'plan 是 docs-only, 记录 status=not-run-docs-only'); behavioural checks were replaced by the deterministic validators and executed quickstart scenarios recorded above", "changed_paths": [".specify/specs/082-self-explanatory-integration/plan.md", ".specify/specs/082-self-explanatory-integration/research.md", ".specify/specs/082-self-explanatory-integration/data-model.md", ".specify/specs/082-self-explanatory-integration/contracts/constitution-double-landing.contract.md", ".specify/specs/082-self-explanatory-integration/contracts/instructions-propagation.contract.md", ".specify/specs/082-self-explanatory-integration/contracts/mirror-distribution.contract.md", ".specify/specs/082-self-explanatory-integration/contracts/glossary-integration.contract.md", ".specify/specs/082-self-explanatory-integration/quickstart.md", ".specify/specs/082-self-explanatory-integration/feature-ref.md", ".specify/specs/082-self-explanatory-integration/test-evidence/plan-stage-checks.md", ".specify/memory/features.md", ".specify/memory/features/082.md", ".specify/state/082-self-explanatory-integration.md"], "evidence_ptr": "this file (test-evidence/plan-stage-checks.md) + the plan-stage commit"}
```

Pre-existing red, disclosed and not repaired:
`tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` (gate total 27
vs frozen 23; plan EP-003, `Decision: fallback`).
