# Spec audit — 069a-flow-classification-docs-gates (batch 9)

- **Date**: 2026-11-10
- **Tree**: `/storage/project/cloud-native-ai/spec-kit` @ `master` (read-only audit; working tree as-is)
- **Spec under audit**: `.specify/archive/specs/069a-flow-classification-docs-gates/`
- **In-scope artifacts**: `requirements.md`, `plan.md`, `tasks.md`, `data-model.md`, `verification.md`, `contracts/*.md` (4), `notes/*.md` (7)
- **Method**: extract every concrete repository path from the in-scope artifacts, resolve each against the current tree, then inspect the consolidation ledger, the named guard files and three implementation claims.

## Counts

| Measure | Count |
|---|---|
| Unique concrete path references | **135** |
| Alive | **110** |
| Archived-elsewhere (target under `.specify/archive/specs/069a-flow-classification-docs-gates/`) | **13** |
| Dead | **12** |

Extraction exclusions (not counted as references): 3 temp-fixture paths in a transcript (``<fixture>/docs/clean.md``, ``<fixture>/docs/dup-a.md``, ``<fixture>/docs/dup-b.md``), 1 ellipsis placeholder (``shared/guidelines/...``), and `docs/SKILL.md` (0 real occurrences — a substring match inside `create-docs/SKILL.md`).

Archived-elsewhere set (13, all present in the archive): `checklists/classification-gates.md`, `contracts/compatibility-distribution.md`, `contracts/doc-consistency-checker.md`, `contracts/expression-gate-operators.md`, `contracts/flow-class-ledger.md`, `coverage-baseline.txt`, `notes/expression-baseline.md`, `notes/parent-fr-mapping.md`, `notes/pre-change-file-hashes.txt`, `notes/pre-change-measurements.md`, `notes/quickstart-run.md`, `notes/red-first-evidence.md`, `notes/test-baseline-contract.txt`.

## Broken list (dead references, 12)

**A. Stale pre-archive self-paths (8)** — objects survive under the archive; the written path is dead per the audit rule.

| # | Reference (source `path:line`) | What it now resolves to |
|---|---|---|
| 1 | `plan.md:72` (also `tasks.md:7`, `tasks.md:31`, `tasks.md:32`, `tasks.md:33`, `tasks.md:36`, `tasks.md:46`, `tasks.md:67`, `tasks.md:75`, `verification.md:127`, `notes/red-first-evidence.md:470`) → `.specify/specs/069a-flow-classification-docs-gates/` | dead directory; `.specify/archive/specs/069a-flow-classification-docs-gates/` |
| 2 | `plan.md:5` (also `notes/parent-fr-mapping.md:5`, `notes/quickstart-run.md:155`) → `.specify/specs/069a-flow-classification-docs-gates/requirements.md` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/requirements.md` |
| 3 | `tasks.md:38` (GATE-8) → `.specify/specs/069a-flow-classification-docs-gates/tasks.md` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/tasks.md` |
| 4 | `tasks.md:18`, `tasks.md:39`, `verification.md:14` → `.specify/specs/069a-flow-classification-docs-gates/verification.md` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/verification.md` |
| 5 | `tasks.md:78`, `tasks.md:143`, `tasks.md:274` → `.specify/specs/069a-flow-classification-docs-gates/coverage-baseline.txt` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/coverage-baseline.txt` |
| 6 | `tasks.md:142`, `notes/pre-change-measurements.md:104` → `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` |
| 7 | `tasks.md:67`, `tasks.md:142` → `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-measurements.md` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/notes/pre-change-measurements.md` |
| 8 | `tasks.md:12`, `notes/red-first-evidence.md:470` → `.specify/specs/069a-flow-classification-docs-gates/notes/red-first-evidence.md` | dead; `.specify/archive/specs/069a-flow-classification-docs-gates/notes/red-first-evidence.md` |

**B. Renamed skill paths (2)** — object survives under a new name; wiring verified present there.

| # | Reference (source `path:line`) | What it now resolves to |
|---|---|---|
| 9 | `plan.md:98`, `plan.md:130`, `plan.md:179`, `plan.md:230`, `tasks.md:65`, `tasks.md:202`, `tasks.md:237`, `verification.md:92`, `verification.md:167`, `contracts/compatibility-distribution.md:54`, `contracts/compatibility-distribution.md:75`, `contracts/flow-class-ledger.md:127`, `contracts/expression-gate-operators.md:3`, `requirements.md:263`, `notes/red-first-evidence.md:528`, `notes/red-first-evidence.md:785`, `notes/red-first-evidence.md:791`, `notes/red-first-evidence.md:800` → `skills/external/humanize/SKILL.md` | missing; renamed to `skills/external/humanize-conclusion/SKILL.md` (Stage 6 lookup wiring survives at line 109) |
| 10 | `plan.md:130`, `verification.md:92`, `notes/red-first-evidence.md:530` → `.specify/skills/humanize/SKILL.md` | missing; mirror renamed to `.specify/skills/humanize-conclusion/SKILL.md` |

**C. Historical transcript paths (2)** — recorded by the spec as pre-existing broken links, not as claims.

| # | Reference (source `path:line`) | What it now resolves to |
|---|---|---|
| 11 | `notes/pre-change-measurements.md:74` (checker `detail: "../../tests/unit/test_qoder_support_matrix.py"`) | missing; the same link is still live-broken in `docs/concepts/overview.md:240` today |
| 12 | `notes/pre-change-measurements.md:75` (checker `detail: "../../tests/integration/test_qoder_refresh.py"`) | missing; still live-broken in `docs/concepts/overview.md:240` today |

No implementation, template, test, registry or shared-owner target named by the spec is missing.

## Ledger-target check

- Row: `.specify/archive/specs/CONSOLIDATION-LEDGER.md:18` → `| 069a-flow-classification-docs-gates | merge | 069 (decomposition-gate slice) | review-G7 |`.
- Target resolves: `.specify/specs/069-execution-expression-sdd/` exists (live, with `requirements.md` and `notes/decomposition-gate.md`); `.specify/memory/features/069.md` exists; registry row `.specify/memory/features.md:78` exists (`069`, status `Implemented`, records “slice: 069b Implemented; 069a Implemented”).
- Accuracy: `feature-ref.md:9-15` binds 069a as a slice of **Feature 069**; `.specify/memory/features/069.md:22-23` records the 069a plan/review history; archive move commit `c5b17a9fc` matches the ledger date (2026-11-09). Verdict wording (“merge → 069”) is accurate at the feature/registry level; the spec directory itself is archived, consistent with the ledger header’s archive-not-delete discipline.
- Note: the ledger’s own table has a formatting defect outside this row — see the anomaly line below.

## Missing guards

- All 20 test/guard files named in the in-scope artifacts exist: `tests/contract/{test_compile_embeds,test_doc_consistency_checker,test_docs_command_template,test_expression_compatibility,test_expression_gates_doc,test_expression_gate_wiring,test_fast_fail_discipline,test_feedback_command_classification,test_feedback_mechanism_boundary,test_flow_class_correctness,test_flow_class_ledger,test_humanize_command_surface,test_mirror_parity_suite,test_run_determination_passive_wiring,test_self_improvement_conformance,test_shared_reference_directory,test_shared_reference_rewrite,test_token_efficiency_discipline}.py`, `tests/unit/test_doc_consistency_rules.py`, `tests/unit/test_flow_class_check.py`, `tests/fixtures/flow_class/classification-oracle.md`.
- Sampled guard symbols all present: `test_a6_wiring_set_is_closed` (`tests/contract/test_expression_gate_wiring.py`), `test_c01_thin_entry_shape` (`tests/contract/test_humanize_command_surface.py`), `test_lookup_matches_independent_oracle` (`tests/contract/test_flow_class_correctness.py`), `test_c05_copied_owner_text_is_reported_as_duplicate_fact` (`tests/contract/test_doc_consistency_checker.py`).
- **Missing guards: none.** The two qoder test paths (#11/#12) are unrelated transcript details, not guards of this spec.

## Three implementation spot-checks

1. **File** — `shared/workflow/expression-gates.md` (and mirror `.specify/shared/workflow/expression-gates.md`) exists and holds the claimed closed six-face set: `requirements-clarity`, `reader-purpose`, `evidence-asof`, `structure-links-build`, `fact-consistency`, `review`, each with exactly one `owner_pointer` (lines 16-23). The later declaration-layer owners `shared/declarations/facts/expression-gate-faces.yaml` and `expression-stage-operator-table.yaml` exist. **PASS**
2. **Command/symbol** — `scripts/python/flow-class-check.py` exists; `--action` accepts `check|lookup|isomorphism|delegation|faces` (line 2726), `--unit-id` is supported (line 2733). Read-only run: `--action lookup --unit-id "/speckit.docs"` → `flow_class: expression`, `source: ledger`, exit 0. Mirror `.specify/scripts/python/flow-class-check.py` exists. **PASS**
3. **Behaviour surface** — `templates/commands/docs.md:36-38` executes the lookup, then the owner-registered document gates via `doc-consistency-check.py --action verify --path <doc> [--spec-dir <dir>] --strict`, with a visible degradation clause; `templates/commands/humanize.md:41` carries only the owner pointer and no script call (the resolved Simple-command ruling); `doc-consistency-check.py --help` accepts `--action {verify,structure}`, `--path`, `--spec-dir`, `--strict` (now documented as a deprecated alias, still accepted). `skills/external/create-docs/SKILL.md:103,133` carries the matching gate text. **PASS**

## Anchor-layout rename flags (alive now, will move)

The pending `rename-anchors` branch moves the project anchors out of `.specify/memory/`:

- `.specify/memory/constitution.md` → `.specify/constitution.md`
- `.specify/memory/features.md` → `.specify/features.md`
- `.specify/memory/features/069.md` → `.specify/features/069-execution-expression-sdd.md`
- `.specify/memory/glossary.md` → `.specify/glossary.md`
- Generic `.specify/memory/` references: anchors leave, but `session/`, `feedback/` and `exec-quant/` stores stay put (no moves on the branch).

All four new paths were verified present on `rename-anchors`.

## Verdict

**BROKEN** — 12 dead references: 8 stale pre-archive self-paths (objects preserved in the archive), 2 humanize-rename paths (object preserved as `humanize-conclusion`), 2 historical transcript paths (already recorded as broken at measurement time). **Zero missing implementation targets**: every shared owner, script, template, test, skill and registry target the spec names is alive, and all three spot-checks pass.

Anomaly: `.specify/archive/specs/CONSOLIDATION-LEDGER.md:23` — the `054-agent-registration-wiring` row sits after the “Deferred”/“Not executed” prose (lines 21-22), outside the table; it is the file’s only occurrence.

SPEC-AUDIT-9-DONE
