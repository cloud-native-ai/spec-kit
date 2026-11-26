# Verification Log — 107-decision-governance

<!--
  Derived spec-side at the review stage (2026-11-26) from
  `.specify/specs/107-decision-governance/test-evidence/verification-input.md` (the crew-side
  close-out input, T056). The implement stage flipped the registry to `Implemented` without
  this carrier and without the closure judgement; the review stage derived it, ran
  `scripts/python/closure-acceptance-check.py`, and copied the verdict below (review finding
  A1). One correction is applied on derivation and disclosed: the SC-001 note's sentence
  claiming the documented scan "equals the owner page's declared producer set minus the two
  declared exemptions" did not match the measured scan output; it is restated to the measured
  reading (review finding A3). Statuses and values are copied verbatim from the input.
  THE KEY=VALUE BLOCK IS THE RECORD; the narrative above is orientation only.
-->

# -- Baseline (recorded before the implement work changed the tree) --

baseline_commit=0d7519521
baseline_date=2026-11-26
baseline_branch=107-decision-governance

# -- Implementation results (implement stage, run r20261125T134500Z-107a) --

implementation_date=2026-11-26
post_change_commit=3f0200b42

# -- Status rows (copied from test-evidence/verification-input.md) --

SC-001_status=pass
SC-001_value=tests/contract/test_decision_governance_guards.py::test_inventory_closure=1 passed declared=12 exempt=2 observed=10 unregistered=0
SC-001_note=final path. The documented code-face scan (`grep -rEl 'shared/definitions/decision-definitions\.md' templates skills agents scripts src --include=*.md --include=*.py --include=*.sh | sort`) hits ten faces: four map to declared producers (P-04, P-05, P-06, P-09), three are declared non-producer faces (templates/instructions-template.md, dispatch-recipes.md, stage-prompts.md) and one is the checker itself; the action's observed set (declared=12, exempt=2, observed=10) additionally attests the remaining declared producer faces by owner-path existence. Review-corrected from the crew input's "scan equals declared minus exemptions" wording (review.md finding A3); the open semantic question is recorded there. An unregistered face and a vanished producer face each turn it red (mutations inside the test). Evidence test-evidence/us5-green.txt § SC-007, test-evidence/mutation-drill.md.
SC-002_status=pass
SC-002_value=m02_red_then_green=yes m08_red_then_green=yes instruction_and_owner_page_present=yes
SC-002_note=final path. Empty `resource_locator` / single-dimension locator → M-02 red, business resource group + region id → green; registered glossary variant → M-08 red, full name → green (stubbed glossary in `tests/fixtures/decision-governance/m08/`); both rules appear in the owner page § 决策文本契约 and in the generated instruction section (asserted inside `test_full_name_minimum_bar_four_surfaces`). Evidence notes/us1-green.txt, notes/us6-green.txt.
SC-003_status=pass
SC-003_value=class_missing_or_outside_red=yes human_template_elements=all ai_template_elements=all B03_B04_B06_review_surfaces=named
SC-003_note=final path. `decision_class` outside the closed set → M-01 red; the `human-interactive` template carries plain-language/context/consequences/reversibility/default/full-names-and-locator and the `ai-autonomous` template carries closed options/predicate/assumptions/evidence pointers/deterministic conclusion — both asserted by `test_human_template_elements` / `test_ai_template_elements`; class-vs-holder mismatch is routed to the named B-03/B-04/B-06 review surfaces with the explicit no-machine-coverage statement (`test_review_surfaces_named`). Evidence notes/us1-green.txt, test-evidence/mutation-drill.md.
SC-004_status=pass
SC-004_value=tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples=1 passed ::test_ai_replay_deterministic=1 passed reverse_samples=7
SC-004_note=final path. Empty set / duplicate label / `other` without `path` / missing element / single option without `forced` / count mismatch each red with its own message; a completed set green; the chosen option replays deterministically from the recorded predicate + inputs (and a doctored record replays to a different choice, so the mismatch is detectable). Evidence notes/us2-green.txt.
SC-005_status=pass
SC-005_value=test_m01_field_closure_reverse_samples=1 passed test_m04_id_density_register=1 passed test_reconstruct_from_register_and_carriers=1 passed test_broken_pointer_red=1 passed
SC-005_note=final path. Four-carrier fixture set (requirements/plan/checkpoint/run report) reconstructs each record's applicable-layer fields from register + carriers only; a missing base-layer or conditional field → M-01 red, a malformed/non-dense/unregistered id → M-04 red, a broken evidence pointer → M-09 red; the load-bearing record cross-references `T-NNN` and copies no tension six-field set (`test_no_tension_field_copy`). Evidence notes/us3-green.txt.
SC-006_status=pass
SC-006_value=tests/contract/test_decision_governance_guards.py::US4_guards=8 passed silent_redecision=explicit_anomaly no_record_dispatch=refused
SC-006_note=final path. Complete decision block green / each missing block field red (M-06); acknowledgement + four-field `implementation_receipt` present, missing receipt item → M-05 red; record → dispatch attempt → receipt chain green and each missing segment red (M-07); a silent re-decision fixture breaks the chain and the correct return is the explicit `ANOMALY:` escalation; multi-hop keeps one `decision_id` and a re-decision preserves the old record (`superseded_by`). Evidence notes/us4-green.txt, notes/red-first-evidence.md § US4.
SC-007_status=pass
SC-007_value=mutation_drill=9/9 red per_rule verdict_lines=rule_carrying B_rows=7 named parity=table_guard_row_identical
SC-007_note=supporting path (measured baseline). Every M-01…M-09 guard executed against its reverse sample with exit 1 and its own rule id; B-01…B-07 each carries a named review surface and the explicit "不声称机器覆盖" statement; the owner page's M/B tables and the test-side rosters are row-identical (`test_table_guard_parity`). Evidence test-evidence/mutation-drill.md, notes/us5-green.txt.
SC-008_status=pass
SC-008_value=regen_rc=0 sync_new_drift_members=0 section=1276B template_eq_live=yes live_total=40170 budget=40960 gate_new_hits=0 client_init=received
SC-008_note=supporting path (measured baseline). `sync-mirrors.py --check` rc 0 with no drift member at all; `regen-command-copies.py --check` rc 0; the Decision Items section byte-identical template↔live at 1,276 B under the 1,500 B cap and 40,170 B < 40,960 B; `scan-confirmation-gates.py` 30 blocking / 0 violations, zero NEW hits on the feature-touched faces (re-baseline 31→30 adjudicated at the 106 merge, `test-evidence/gate-neutrality.txt`; the literal "blocking count unchanged" clause is restated by that adjudication — review finding A4); the empty-client init fixture receives the section (template + generated file + `QODER.md` copy). Evidence test-evidence/us6-mirror-check.txt, notes/us6-green.txt, test-evidence/gate-neutrality.txt.
SC-009_status=pass
SC-009_value=bc_rows=6/6 mapped register_numstat=14/0 corpus_deleted_lines=0 deleted_files=0 legacy_carrier=pass migrate_item=templates-generated no_seventh_dimension=yes
SC-009_note=supporting path (measured baseline). Every BC-01…BC-06 row maps to a tested migration or deterministic refusal; the row-set/mapping guard and the no-fallback-only guard are green with mutation red-ability; the base corpus (3,127 pre-existing carrier files) shows zero deleted lines and no deleted file, and all 89 pre-existing clarifications bodies are append-only; a real legacy carrier reports `legacy` and passes; the migrate dry-run lists the instruction-template convergence item under `templates-generated` with the dimension set still the closed six. Evidence test-evidence/migration-closure.md, test-evidence/us6-migrate-dryrun.json, test-evidence/us6-red-first.txt.
SC-010_status=pass
SC-010_value=section_bytes=1276 per_tool_copy=QODER.md->.specify/instructions.md live_total=40170 budget=40960
SC-010_note=final path. The generated `.specify/instructions.md` carries the `## Decision Items（决策项）` pointer section with both production rules and both class emphases, the per-tool compatibility copy follows it, and the section/total byte ceilings hold; a throwaway `specify init --here --ai qoder --script sh --no-git` workspace receives the section end to end. Evidence notes/us6-green.txt, test-evidence/us6-mirror-check.txt (plus `test_client_init_receives_section`).

# -- Runtime-stack joint acceptance (requirements.md § Runtime Stack & Dependency Ownership) --

RS-001_joint_acceptance=new tests pass on the >=3.8 interpreter through the single entry (review smoke 43 passed on CPython 3.11.11 via scripts/bash/run-tests.sh); zero new third-party imports (stdlib only)
RS-002_joint_acceptance=new tests run through scripts/bash/run-tests.sh with zero new name-level failures against the entry baseline (targeted batteries green; preservation sweep failures all inside baseline-failed.txt)
RS-003_joint_acceptance=new tests all execute through the single bash entry and one run exits 0 (review smoke exit 0, captured in test-evidence/review-evidence.txt)
RS-004_joint_acceptance=dispatch fixtures carry the decision block and implementation receipt; a missing block is refused; an incomplete return is not consumed (M-06/M-05/M-07 reverse samples red, green chain tests pass)
RS-005_joint_acceptance=every guard's reverse sample turns red (mutation drill 9/9); scan-confirmation-gates relative to the recorded baseline shows zero new hits (30 blocking / 0 violations with the recorded 31->30 re-baseline adjudication)
RS-006_joint_acceptance=instruction template and live copy are byte-identical and inside the byte ceilings (1,276 B section, 40,170 B total < 40,960 B); regen-command-copies.py --check rc 0; sync-mirrors.py --check rc 0 with no drift member

# -- Smoke test record (exactly one per feature) --

smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py tests/contract/test_decision_governance_guards.py tests/contract/test_decision_governance_migration_map.py tests/unit/test_validate_decisions.py tests/integration/test_decision_governance_migrate_dryrun.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/107-decision-governance/notes/us6-green.txt

# -- Closure verdict (copied from scripts/python/closure-acceptance-check.py) --

closure_verdict=accept
closure_reasons=none (blocking reason set empty)
closure_final_path=pass 7 / blocked 0 / deferred 0 / partial 0 / fail 0 / unknown 0 / total 7
closure_checked_at=2026-11-26 review stage, tree at HEAD 3f0200b42 plus this derived carrier

