# Verification Log — 083-mechanism-policy-separation

Shape follows `.specify/templates/verification-log-template.md`; every `status` value below is
drawn from that template's closed vocabulary (`pass | fail | partial | blocked | deferred |
unknown`) and nothing narrower. Every `pass` carries a complete evidence row
(`sample_id` / `evidence_path` / `evidence_sha256` / `verdict`), hashed over the archived file's
bytes with `shasum -a 256`.

# -- Baseline (recorded once, BEFORE any /speckit.implement work changed the tree) --

baseline_commit=28662977fab2d8cae60e7f2c2e369df0d984affd
baseline_date=2026-11-05
baseline_branch=083-mechanism-policy-separation

baseline_full_suite_passed=7157
baseline_full_suite_failed=24
baseline_full_suite_skipped=7
baseline_targeted_set_collected=893
baseline_targeted_set_passed=892
baseline_targeted_set_failed=1
baseline_mirror_pairs_clean=6
<!-- 092 handoff: E2 → 083 -->
<!-- 092 handoff — E2 校正陈述（三条 baseline 槽位，两个不同对象）。`baseline_commit=28662977…` 是**实现期测试基线所测的那棵树**（本特性自身工作树上的提交，`base_sha` 是 `3ffeb26e`，见 `.specify/state/083-mechanism-policy-separation.md`）；**字节基线**是 `STR-002` = `3ffeb26e`，只供 SC-003 / SC-007 的逐字节与包含性断言。两者不是同一个对象，不得相互「对齐」。`baseline_commit` 的取值 owner 是本块（上方 `# -- Baseline` 行；原文保留不改）；下述 `baseline_full_suite_*` 的取值 owner 是 `test-evidence/implement-part1-baseline.txt`（实测 `24 failed, 7157 passed, 7 skipped`），失败名清单 owner 是 `baseline-failed.txt`（24 条）；`baseline_targeted_set_*` 的 owner 是 `test-evidence/plan2026-11-05-baseline.txt`。本标记不复制任何计数。-->

> Owners of those numbers: the full-suite slot is `test-evidence/implement-part1-baseline.txt`
> (E2, captured at implement start; its 24 failed node ids are listed in
> `.specify/specs/083-mechanism-policy-separation/baseline-failed.txt`); the 12-module targeted
> baseline is `test-evidence/plan2026-11-05-baseline.txt` (Reading A: one contaminated failure,
> Reading B: zero); the mirror baseline is `notes/pre-change-measurements.md` § 1.

# -- /speckit.implement results --

implementation_date=2026-11-05
post_change_commit=28662977fab2d8cae60e7f2c2e369df0d984affd

> `post_change_commit` is the commit the measured tree is based on. The Part 7 evidence files
> (`sc-004`, the T050 append to `sc-003`, `final-gates.txt`), this file and the closing task rows
> land in the commit **after** it, so no hash here claims to contain them.

post_change_full_suite_passed=not-evaluated
post_change_full_suite_failed=not-evaluated
post_change_full_suite_skipped=not-evaluated
post_change_targeted_set_collected=100
post_change_targeted_set_passed=100
post_change_targeted_set_failed=0
post_change_new_failed_nodeids=0
post_change_mirror_pairs_clean=6
<!-- 092 handoff — E2 校正陈述（verification 侧，接 `baseline_mirror_pairs_clean` 之上的 E2 标记）。`post_change_*` 每一条只与**同范围的**测试基线比，不与字节基线比：`post_change_new_failed_nodeids=0` 的对象是 `baseline-failed.txt` 的 24 条**节点名**（GATE-2 的 `comm -13`），`post_change_targeted_set_*=100` 的对象是 GATE-1 的十一个模块；`post_change_full_suite_*=not-evaluated` 是**未测量**，不是零，也不得与 `baseline_full_suite_*` 相减读成「无变化」。故 `post_change == baseline` 只在一个意义上成立：相对同一范围没有**新增失败**；字节是否变化由 (a) 上的 SC-003 单独度量。原文保留不改；读数一律以本文件的实测行为准。-->

> `post_change_full_suite_*=not-evaluated`: the closure full-suite slot is the driver's step after
> `/speckit.review`; the dispatch forbids a second full run in this segment. `post_change_new_
> failed_nodeids=0` is the `comm -13` result over node-id **names** against `baseline-failed.txt`
> (GATE-2), not a count difference. The targeted-set numbers are GATE-1's eleven modules
> (100 passed); GATE-2's 12-module companion run is 899 passed with an empty failed-name set.

# -- Run determination (the four measured quantities) --

run_determination_unit=/speckit.implement
run_determination_run_id=r20261105T033420Z-082a
run_quantity_token_consumption=not-evaluated
run_quantity_token_consumption_note=no session-row span for this segment was bound to the run-determination engine, and a token number is never fabricated; the engine's record schema owns the measured form
run_quantity_elapsed_time=measured
run_quantity_elapsed_time_value=0:16:56 (1016 s)
run_quantity_elapsed_time_note=from `stage_started_at=1793874936` (2026-11-05T18:35:36+08:00, read-only state spine) to 2026-11-05T18:52:32+08:00, the instant this file was drafted; the segment continued after that instant, so the value is a floor, not the final span
run_quantity_artifact_correctness=evaluated
run_quantity_artifact_correctness_value=GATE-1 100 passed / 0 failed; GATE-2 899 passed with an empty failed-name difference; GATE-3–GATE-7 readings and disclosures in `test-evidence/final-gates.txt`; the nine SC statuses below
run_quantity_satisfaction=not-evaluated
run_quantity_satisfaction_note=unattended run; no user-turn class was supplied to the satisfaction axis, and the discipline forbids soliciting one, so no verdict is claimed

# -- Smoke test record (exactly one per feature) --

smoke_command=env -u PYTHONPATH bash scripts/bash/run-tests.sh -q tests/contract/test_mechanism_policy_owner_doc.py tests/contract/test_mechanism_policy_ownership.py tests/contract/test_mechanism_policy_skill_wiring.py tests/contract/test_mechanism_policy_guard.py tests/contract/test_mechanism_policy_missing_policy.py tests/contract/test_mechanism_policy_decidability.py tests/contract/test_skill_reference_grammar.py tests/contract/test_skill_reference_matrix.py tests/contract/test_skill_reference_consumers.py tests/contract/test_skill_reference_command_surface.py tests/contract/test_skill_reference_failures.py
smoke_exit_code=0
smoke_evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/final-gates.txt

> The smoke is the feature's own main surface — the eleven contract modules that carry its two
> capabilities — not the whole suite. Its verbatim run (`100 passed in 43.44s`, exit 0) is
> GATE-1 in the evidence file.

# -- Evidence records (bind every `pass` claim to an archived file) --

sample_id=SC-001
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-001-2026-11-05.txt
evidence_sha256=b12994cb6f2d38a59cb1c5c169ccd9afe7e2093e62fa8c06f5bf89e01483ba61
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-002-2026-11-05.txt
evidence_sha256=3d8ae8660e3d21de0d297e38ece997f6c5c2760535d51981d139bec5f06ea922
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-003-2026-11-05.txt
evidence_sha256=2c4d7dccba175fd098572f894fda250fbc94b1557cc1e34866acd68186d2620a
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-004-2026-11-05.txt
evidence_sha256=d3204042a7d608bf48bd2f96f36b023b025253e9b256c62df1b79a19bee1387b
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-005-2026-11-05.txt
evidence_sha256=7892fbb7ba139513b9fe18ae9fb142a567eb31f9f3e6810fa5548acaf5973566
verdict=partial

sample_id=SC-006
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-006-2026-11-05.txt
evidence_sha256=6d358a8456a7a518e6a798aa7284314a22f1cfd96983556ec4e289887cb77296
verdict=pass

sample_id=SC-007
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-007-2026-11-05.txt
evidence_sha256=fcffe0d2d60c9dec6141d2668e006fa49fd1a78dbc6bfb0ab3571bdb520d227b
verdict=pass

sample_id=SC-008
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-008-2026-11-05.txt
evidence_sha256=34a26f900569e2fe45b272dc192f0302b6c5230ab7caa5de9c6f15e8f799823c
verdict=pass

sample_id=SC-009
evidence_path=.specify/specs/083-mechanism-policy-separation/test-evidence/sc-009-2026-11-05.txt
evidence_sha256=1ab081c85af16dad46494c81e7dc14202de5077a21c45ea7108dcf21b082ac31
verdict=pass

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=`judges_agree = 14 / 14 = 100.0 %` — two fresh-context read-only judges answered the closed 14-item worked-example set using the owner document alone; both verdict sets match each other and the owner's own key on every item
SC-001_note=The set is the owner appendix's own denominator; no second question set exists. The boundary item (Q-06 / S-12) was answered `待澄清` by both judges. Source: `sc-001-2026-11-05.txt` § 6.

SC-002_status=pass
SC-002_value=detection 2 / 2 = 100 % on the deliberately misplaced samples; false positives 0 / 2 on the correctly layered samples (after the change); the before-change false-positive leg is also 0 / 2
SC-002_note=The harness supplies the policy **values** so the flow can proceed, and a capable general model detects both misplaced samples in the before state too, so this reading does **not** establish that the changed skill causes detection (disclosed in `sc-002-2026-11-05.txt` § 7). The criterion's two numbers are met on the post-change flow; the mechanised counterpart (symptom tables, judgement line and its negative case) is green in GATE-1.

SC-003_status=pass
SC-003_value=`compared=575 unit=575 complement=566 allowed_in_unit=10 allowed_in_baseline=9 frozen_mismatches=0`; the 083-attributed changed-path set and the registered in-unit allowed set are the same 10 paths (both differences empty); the T050 complement reading gives `included_minus_implied=[]` and `implied_minus_included=[]`
SC-003_note=Two disclosures, both recorded in `final-gates.txt` GATE-4: the gate's literal "rows 1–8" is stale (GM-03 registers 10 in-unit paths: rows 1–8 + 19–20 after the ratified CL-04 absorption); the raw `git diff` also carries 24 paths with zero 083 commits from absorbed concurrent work lines, attributed rather than swallowed.

SC-004_status=pass
SC-004_value=missing-policy host run: the owner's three-field prompt produced, **zero writes** (snapshot 8 files / 10 dirs identical before and after across the full file set); supplied-policy run: the produced path set and every file's sha256 are identical between the baseline and changed states, and equal the draft's own bytes
SC-004_note=Host Qoder CLI 1.1.83 with write tools available, so the stop is the flow's own; the four trial/premise corrections are disclosed in `sc-004-2026-11-05.txt` § 5. The deterministic face (`test_mechanism_policy_missing_policy.py`) is green in GATE-1.
<!-- 092 handoff — E2 校正陈述（SC-004 的等式不是「post_change == baseline」）。`SC-004_value` 的 `identical between the baseline and changed states` 读的是**同一个技能树在两种状态下的产物**，不是本特性的前后提交：`sc-004-2026-11-05.txt` § 1 写明 changed state = HEAD `28662977…`，baseline state = 从 `3ffeb26e` 读出的同一技能树（该基线里**没有** mechanism-policy owner）。等式的含义是「同一输入、同一策略 ⇒ 产物逐字节一致」，即确定性；它不主张本特性没有引入字节增量，也不使 `post_change` 的差集读数失效。两个不同问题：本条证确定性，SC-003 证字节不变性。原文保留不改。-->

SC-005_status=partial
SC-005_value=correct = 13 / 14 (full set size = 14); the one divergence is Q-06, answered `策略` while the owner's key is `待澄清`
SC-005_note=Path `supporting`: the decidability itself is carried by SC-001 (14/14) and by `test_mechanism_policy_decidability.py`. The shortfall is written as measured; no second reader was run to search for a passing sample.
SC-005_blocked_at=2026-11-05 — one uninvolved reader answered 13/14; Q-06 differed from the owner key
SC-005_reduced_measurement=the same closed 14-item set answered by one reader who did not take part in the feature, against the owner document alone
SC-005_reduced_measurement_run=yes
SC-005_why_reduced_insufficient=the criterion's literal wording asks for no fewer than all samples (14/14); 13/14 is short, and a reader sample cannot be generalized by running more readers until one scores full marks
SC-005_unblock=a reader session that answers all 14 correctly, or a ratified clarification of the Q-06 boundary sentence in the owner document; either is a new measurement, not a re-score of this one

SC-006_status=pass
SC-006_value=`rows=30 matched=30 failed=0` — every matrix row recomputed through `skill_reference_matrix.py`, denominator = the fixture's own 30 rows (≥ 12)
SC-006_note=Per-row readings and the fail-on-first-mismatch rule are in `sc-006-2026-11-05.txt`; the module is green in GATE-1.

SC-007_status=pass
SC-007_value=five consumers each `source_refs=1 mirror_refs=0`; containment scan `scanned=54 skills/**/SKILL.md`, permitted classes `owner=0 / owner-mirror=0 / fixture=0`, every failure-class literal count 0
SC-007_note=Exactly one source-path reference per consumer is read per file, not in aggregate; the scan's denominator is the framework source tree, with mirror parity proved separately by `sync-mirrors.py --check` (GATE-3).

SC-008_status=pass
SC-008_value=positive rows: `speckit.skills`, `/speckit.skills` and `speckit.skills/SKILL.md` → `command-surface` pointing at `templates/commands/skills.md`; negative rows: `create-docs`, `humanize`, `my-draft.md`, `SCRATCH-HELPER` and others → failure, never command-surface
SC-008_note=Positives and negatives come from one run; the negatives include command-shaped names, so the ruling is not "anything with a dot or a slash is a command".

SC-009_status=pass
SC-009_value=four failure classes each have a recomputable assertion carrying both the raw and the normalised identifier, plus mutual-exclusion assertions (`out-of-ladder` is never reported as `zero-hit`; `unreadable` is never reported as `out-of-ladder`)
SC-009_note=The `dual-layer` fixture uses two genuinely different layers, never a source-and-mirror pair. Readings and the class fixtures are in `sc-009-2026-11-05.txt`.

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-004_joint_acceptance=pass

> RS-004 is this feature's only `in-scope` runtime-stack row (the mirror and command-copy
> regenerators). `sync-mirrors.py --check` and `regen-command-copies.py --check` both exit 0 with
> six pairs `ok` and zero changed command copies (GATE-3).

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=nothing deferred — T001…T052 all `[x]`

# -- Gates --

GATE-1_status=pass
GATE-1_value=100 passed / 0 failed, exit 0 (eleven modules, negative cases included)
GATE-2_status=pass
GATE-2_value=899 passed; failed-name set ∅; `head − baseline = ∅` against the 24-entry E2 list
GATE-3_status=pass
GATE-3_value=six mirror pairs `ok`, zero new drift; zero changed command copies; both `--check` exit 0
GATE-4_status=pass
GATE-4_value=083-attributed changed paths == registered in-unit allowed set (10 == 10, both differences empty); two named disclosures (stale "rows 1–8" literal; 24 non-083 absorbed paths in the raw diff)
GATE-5_status=pass
GATE-5_value=closing `grep -cE '^- \[[ >]\]'` → 0 (the mid-run reading was 4, kept in the evidence)
GATE-6_status=pass
GATE-6_value=0 hits in each of the 4 scanned excluded-member files (denominator printed)
GATE-7_status=pass
GATE-7_value=0 mirror-path references across 54 `SKILL.md` files; each of the 5 consumers has exactly 1 framework-source reference
GATE-8_status=pass
GATE-8_value=every `final`-path criterion (SC-001, SC-002, SC-003, SC-004, SC-006, SC-007, SC-008, SC-009) reads `pass`; SC-005 (`supporting`) reads `partial` and cannot refuse GATE-8; `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` are present above and the evidence path exists and is non-empty
validate_tasks_status=pass
validate_tasks_value=`PASS: .specify/specs/083-mechanism-policy-separation/tasks.md — 0 error(s), 0 warning(s)` at T051 execution and again after the closing rows
pre_analyze_status=pass
pre_analyze_value=`stage=tasks decision=pass errors=0 advisories=10 waived=0` (the advisories are pre-existing placeholder-shaped paths in requirements/plan/checklist prose)

> All gate commands, exit codes and verbatim outputs: `test-evidence/final-gates.txt`.

# -- Definition of Done --

| DoD | status | evidence |
|---|---|---|
| DoD-1 | met | both owner documents exist as the only owners of their fact groups (`test_mechanism_policy_owner_doc.py` / `test_skill_reference_grammar.py`, GATE-1); GATE-7 proves consumers cite the source path, not a mirror |
| DoD-2 | met | the three `included` meta-skills carry one judgement line plus an owner-path reference (`test_mechanism_policy_skill_wiring.py`, GATE-1); SC-002's correctly-layered samples demand no additions |
| DoD-3 | met | five consumers, each exactly one framework-source reference (`source_refs=1`, `mirror_refs=0`); `coaching-skills` / `run-skills` carry zero mechanism/policy literals (GATE-6) |
| DoD-4 | met | eleven contract modules + one test-only helper exist; the matrix lives at `tests/fixtures/skill-reference/normalization-matrix.json`; every module carries a negative case (inside GATE-1's 100 passed) |
| DoD-5 | met | nine SC carriers in place; the six test-borne criteria green on the final tree (GATE-1); the three sample-borne criteria recorded (SC-001 / SC-002 / SC-005), with SC-005's shortfall stated as measured |
| DoD-6 | met | both regeneration entries `--check` exit 0 with zero new drift; `regen-command-copies.py --check` proves 27 templates / zero per-tool copy change (GATE-3) |
| DoD-7 | met | five frozen-hash registration points in `tests/contract/test_expression_compatibility.py`; the module is green in GATE-2 (its previous contaminated failure is green after T038) |
| DoD-8 | met | `glossary.md`, `framework-map.md` and `CHANGELOG.md` each carry one registration line (T039); GATE-3 shows no second data file, gate script, directory root or environment variable, and the command surface is unchanged |
| DoD-9 | met | targeted-set failure-name difference is empty (GATE-2); every new module is green (GATE-1); no pre-existing failure was folded into this feature's verdict |
| DoD-10 | met | every `final`-path criterion reads `pass`; the smoke record is present; the one short criterion (SC-005) is `supporting` and disclosed rather than folded into `green` |

# -- Feature-level statement --

All 52 task rows are `[x]`; `grep -cE '^- \[[ >]\]' tasks.md` → `0`. Every SC-001…SC-009 has a
status row above, every `final`-path criterion reads `pass`, and the smoke record carries
`smoke_exit_code=0` with an existing evidence path. The `Planned → Implemented` gate
(`templates/feature-details-template.md` § Canonical Status State Machine) is therefore satisfied
on all four conditions; **the Feature status advances `Planned → Implemented`**.

SC-005 is recorded as `partial` (13/14, `supporting` path): it is an honest shortfall, not a DoD
failure, and it does not refuse the transition. `PLAN-EDIT: none`.
