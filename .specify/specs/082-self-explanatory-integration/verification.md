# Verification Log — 082-self-explanatory-integration

baseline_commit=2f6b8bbb
baseline_date=2026-11-04
baseline_branch=082-self-explanatory-integration

# Baseline counters used to evaluate the SCs (pre-change readings from T002, frozen in
# `notes/pre-change-measurements.md`; owner of the values is that notes file, not this log).
baseline_instructions_bytes=32739
baseline_instructions_budget_bytes=32768
baseline_constitution_version=1.15.0
baseline_gate_total=27

# -- /speckit.implement results --

implementation_date=2026-11-05
post_change_commit=c37129f1

post_change_instructions_bytes=33357
post_change_instructions_budget_bytes=34816
post_change_constitution_version=1.16.0
post_change_gate_total=27

# -- Smoke test record (exactly one per feature) --
# One command, verbatim, run end to end over the feature's main flow: the four guard classes the
# feature lands (constitution double-landing, instructions section propagation, mirror+`specify init`
# distribution, glossary integration). Deterministic, local, no network and no wall clock.

smoke_command=python3 -m pytest tests/contract/test_self_explanatory_constitution.py tests/contract/test_instructions_section_propagation.py tests/contract/test_self_explanatory_distribution.py tests/contract/test_self_explanatory_glossary.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/smoke-20261105.txt

# -- Evidence records (bind every `pass` claim to archived evidence) --
# One record per evaluation sample. SHA-256 is over the archived file's bytes (sha256sum-compatible);
# `evidence_path` is repo-relative. See the binding-check note under `notes=` for how the C-28 rows
# were checked.

sample_id=SC-001
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-3.md
evidence_sha256=c25eac32d4cf6b4dfb936fe5d5a35d1c4467fbf8a04983787cd45663614c8812
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-3.md
evidence_sha256=c25eac32d4cf6b4dfb936fe5d5a35d1c4467fbf8a04983787cd45663614c8812
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-5.md
evidence_sha256=f220a8ab2cb46164979bfc1c123facc32c794d1776e88bb7ed9c60bde7fbd6d3
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-6.md
evidence_sha256=7271e249f39c67b6cbc9bfbad5a347ebdc79f78c90b990547e1cbc5e36146656
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-6.md
evidence_sha256=7271e249f39c67b6cbc9bfbad5a347ebdc79f78c90b990547e1cbc5e36146656
verdict=pass

sample_id=SC-006
evidence_path=.specify/specs/082-self-explanatory-integration/notes/red-first-evidence.md
evidence_sha256=b7cfd2b75bbf2297f5478743db6ffac8794ec544ae6c0a0d2b72c885847aa45b
verdict=partial

sample_id=SC-007
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-9.md
evidence_sha256=e1c25da392fbe632910f1390993aa3845073df4d5a1352e5fe85cb26438fab36
verdict=pass

sample_id=SC-008
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-7.md
evidence_sha256=1822040bc44a080dc42cf8ad9ecafd5df876cb671d4a623b7f1cb97a3e7a5103
verdict=pass

sample_id=SC-009
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/implement-part-5.md
evidence_sha256=f220a8ab2cb46164979bfc1c123facc32c794d1776e88bb7ed9c60bde7fbd6d3
verdict=pass

sample_id=SMOKE-2026-11-05
evidence_path=.specify/specs/082-self-explanatory-integration/test-evidence/smoke-20261105.txt
evidence_sha256=19fdfbbd48bfcf8e2fa3eec771fdbd91b3d54df856c95b373914ed058824751d
verdict=pass

# -- Success Criteria evaluation --
# Status vocabulary is the closed set owned by the template (pass | fail | partial | blocked |
# deferred | unknown); no row narrows it.

SC-001_status=pass
SC-001_value=3/3 surfaces carry the title `Self-Explanatory Structure (不言自明)` under their own per-surface numeral — template `### XVIII.` at `templates/constitution-template.md:304`, live `### XIX.` at `.specify/memory/constitution.md:350`, generator mandate entry at `skills/internal/manage-constitution/SKILL.md:215` and its byte-identical mirror (same line); both principle blocks point at the client-resolvable runtime owner `.specify/shared/definitions/self-explanatory-definitions.md`, whose framework owner `shared/definitions/self-explanatory-definitions.md` exists (4508 B, 7 headings)
SC-001_note=command/exit-code/line evidence in `test-evidence/implement-part-3.md` (US1 subset 12 passed rc 0, carrier 19 passed rc 0); the per-surface numbering is C-3's declared normal, not a divergence

SC-002_status=pass
SC-002_value=live constitution version line reads `Version change: 1.15.0 → 1.16.0 (MINOR; new Principle XIX added, 2026-11-05)` (`.specify/memory/constitution.md:3`) against the recorded baseline `1.15.0`, and the Sync Impact Report records the added principle, its five content obligations, the six surfaces it touched and two follow-up TODOs
SC-002_note=`git show HEAD:.specify/memory/constitution.md` baseline reading is in `test-evidence/implement-part-3.md` § T017; the 1.15.0 baseline row is frozen in `notes/pre-change-measurements.md`

SC-003_status=pass
SC-003_value=2/2 renderings carry the section — template `## Self-Explanatory Structure (不言自明)` at `templates/instructions-template.md:77`, live at `.specify/instructions.md:89`; both sections are summary + one pointer to the client-resolvable `.specify/shared/definitions/self-explanatory-definitions.md` (the source owner `shared/definitions/…` is NOT restated on either surface); incremental injection into a fixture that already has a live file succeeded (generator rc 0, `Section reconcile: live instructions already carry all template sections.`, pre-existing content preserved)
SC-003_note=`test-evidence/implement-part-5.md`: 32 passed rc 0 across `test_instructions_section_propagation.py` + `test_self_explanatory_constitution.py` + `test_instructions_size_budget.py`; red/green pair and the M-3/M-4 legs in `notes/red-first-evidence.md` § Part 5

SC-004_status=pass
SC-004_value=`python3 scripts/python/sync-mirrors.py --check` exits 0 with six `ok` pairs and `shared/ == .specify/shared/ (65 files)`; the three new documents are byte-identical across the pair (`cmp -s` rc 0 for each), and the parity suite picks them up by derivation from `MIRROR_PAIRS` — exactly 3 matching node ids, each naming its own `source->mirror` pair — with the whole suite at 766 passed rc 0
SC-004_note=`test-evidence/implement-part-6.md` (distribution 4 passed rc 0; parity 766 passed; three `cmp` rc 0); M-5 mutation leg proves the byte-identity assertion can go red (`notes/red-first-evidence.md` § Part 7)

SC-005_status=pass
SC-005_value=3/3 documents present after `specify init` in a temporary project — `.specify/shared/definitions/self-explanatory-definitions.md` 4553 B, `.specify/shared/guidelines/self-explanatory.md` 6298 B, `.specify/shared/workflow/best-practice-optimization.md` 4703 B — with `init` rc 0 and `ok Using local templates: shared copied`; the build under test was an editable install of this working tree (`Successfully installed specify-cli-0.0.22`), not the stale published CLI the environment probe found
SC-005_note=`test-evidence/implement-part-6.md` T029 fixture (4 passed rc 0, red proven by removal: 2 failed naming the removed document) and `notes/quickstart-run.md` § Part 6 + § T036-b (raw `init` transcript); the client copies are 45 B / 27 B / 90 B longer than their sources because `copy_tree_with_rewrite` rewrites framework paths to runtime paths

SC-006_status=partial
SC-006_value=5/6 mutation legs PASS with captured non-zero red on temp copies (M-1 principle-block deletion, M-2 mandate-entry deletion, M-3 template-section deletion, M-4 generator non-injection with anti-vacuity, M-5 one-byte mirror drift); M-6 is green in-run as a self-checking contract test (`test_m6_docs_pointer_removal_turns_c27_red`, inside the smoke module) rather than as a captured standalone transcript; the real tree is green on the same group (`test_self_explanatory_distribution.py` 9 passed rc 0)
SC-006_note=this is a **supporting** criterion; the residue is the real-tree full green report for the group, which carries the inherited EP-003 red — see the ladder below
SC-006_blocked_at=EP-003 inherited baseline red (`tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`, gate total 27 vs frozen 23) keeps the extended real-tree group at 821 passed / 1 failed; plus no standalone M-6 transcript separate from the in-suite self-check
SC-006_reduced_measurement=per-leg measurement: 5/6 legs with captured non-zero red (M-1/M-2 in `notes/red-first-evidence.md` § T018, M-3/M-4 in § Part 5, M-5 in § Part 7); M-6 asserted in-suite by `test_m6_docs_pointer_removal_turns_c27_red`; real-tree group readings 37 passed (GATE-1 trio rc 0) and 798 passed (four feature modules rc 0)
SC-006_reduced_measurement_run=yes
SC-006_why_reduced_insufficient=SC-006 names "真实树上同一组测试全绿" as a conjunct, and that readable set is green only by excluding an inherited, name-identified baseline failure; a per-leg count is evidence that each guard CAN go red, not evidence that the named group is uniformly green, so the reduced reading does not discharge the conjunct on its own
SC-006_unblock=re-pin `test_c11_gate_scan_total_unchanged` to the current gate total (27) in the change that owns Feature 050's frozen `baseline-gates.json` — outside this feature's scope (EP-003, `Decision: fallback`) — and capture an M-6 transcript outside the suite

SC-007_status=pass
SC-007_value=1 entry carries canonical `不言自明 (Self-explanatory)` with the retired name `望文生义` in the variants cell only, `origin=auto`, `status=proposed` (`.specify/memory/glossary.md:185`); the mechanism suite reports 12 passed and the integration carrier 14 passed (10 carried + 4 C-34 naming-consistency assertions), store byte-identical at `21482f64…` / 161 entries
SC-007_note=`test-evidence/implement-part-8.md` (mechanism 12 passed; store digest) and `test-evidence/implement-part-9.md` (carrier 10 → `implement-part-10a.md` 14 passed)

SC-008_status=pass
SC-008_value=2/2 owner pointers on `docs/concepts/self-explanatory.md` resolve on both sides — the concept owner `shared/definitions/self-explanatory-definitions.md` and the workflow owner `shared/workflow/best-practice-optimization.md` — with the mirror side resolved through the same `MIRROR_PAIRS` the engine enumerates; the distribution module reports 9 passed rc 0 including C-27's four assertions (floor, resolution, anti-vacuity, no-owner-body)
SC-008_note=`test-evidence/implement-part-7.md` (9 passed rc 0; M-6 leg 13 PASS / 0 FAIL rc 0)

SC-009_status=pass
SC-009_value=live instructions 33357 B against the revised `INSTRUCTIONS_BUDGET_BYTES=34816` (1459 B headroom), generator rc 0 and printing `within`; the constant is identical on both trees (`scripts/bash/generate-instructions.sh:53` and its mirror); the raise 32768 → 34816 and its reason are recorded in the landing commit message and `notes/quickstart-run.md` § T049
SC-009_note=`test-evidence/implement-part-5.md` (33357 B / 34816 / 1459 B) re-confirmed in `test-evidence/implement-part-10a.md` § T049; the constant's owner is the generator script, this row carries no second copy of the rule

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-004_joint_acceptance=pass

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=nothing deferred — 53/53 task rows are `[X]` and no `[~]` row exists

# -- Free-form notes --

notes=Completion Gate re-validation (task rows: 53 `[X]`, 0 `[ ]`, 0 `[>]`): GATE-1 PASS (named trio 37 passed rc 0; extended four-guard + baseline set 821 passed / 1 failed, that one failure is IN baseline-failed.txt so `comm -13` is empty); GATE-2 PASS (six `ok` mirror pairs, six `cmp` IDENTICAL, regen `OK:` with an empty `git diff --stat -- templates/commands/`); GATE-3 PASS (`grep -cE '^- \[[ >]\]'` → 0); GATE-4 PASS (SC-001/003/004/005 all `pass` and the smoke triple present with a 338 B evidence file). GATE-premise decay: none — every gate premise re-measured true on this tree. PLAN-EDIT: none (no plan-owned artifact modified). Evidence binding: the C-28 duties were checked with the checker DERIVED FROM the template's own declared section (`tests/contract/test_evidence_binding_contract.py::_gate_check`): every recorded `pass` row resolved, was non-empty and hash-matched; SC-006 is `partial` and carries no binding duty. The smoke artifact is committed under a `.txt` name (`smoke-20261105.txt`): `test-evidence/*.log` is matched by `.gitignore:37 *.log`, so a log file would not survive the commit and the evidence path would dangle in any later checkout. The file is a curated record, not a raw `.log` capture — it carries this run's command, its two full pytest outputs verbatim, both exit codes and both invocation timestamps, and its header says so; the raw pair of transcripts (with a byte comparison modulo the duration line) is summarised in the same file rather than pasted with divergence from `smoke_command=`. Disclosure: the repo-local `scripts/python/closure-acceptance-check.py` is byte-identical to its `.specify` mirror but predates this feature; it carries the `verification.md` smoke check in `evaluate_smoke` while the pre-flip protocol's checklist item 4 (`deferred_tasks=`) is not part of the checker's payload — this log satisfies that item textually rather than pretending the checker judged it.
