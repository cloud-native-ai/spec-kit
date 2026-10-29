# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `074-goal-team-sdd-unification` |
| **基准** | `371869045d7c86cace67bb49b40b5aa2fd18ceb0` (`371869045`) |
| **目标** | `0024585c4a58af455a19aec218396e8098d05748` (`0024585c4`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-10-29T04:01:56Z` |

## 变更概览

```
 .specify/memory/features.md                        |    4 +-
 .specify/memory/features/074.md                    |   20 +-
 .specify/scripts/python/sdd-route.py               | 1045 +++++++++++++++++++
 .../shared/definitions/sdd-routing-definitions.md  |  212 ++++
 .../shared/definitions/subagent-definitions.md     |   16 +-
 .../internal/create-team/references/create-mode.md |    6 +
 .specify/skills/internal/run-agent/SKILL.md        |   42 +-
 .specify/skills/sdd-loop-driver/SKILL.md           |   21 +
 .../references/nested-invocation.md                |   79 ++
 .../074-goal-team-sdd-unification/requirements.md  |   12 +-
 .../074a-authorized-routing/baseline-failed.txt    |   23 +
 .../checklists/readiness-2026-10-29.md             |  105 ++
 .../recheck-2026-10-29-implement-start.md          |   52 +
 .../checklists/requirements.md                     |   70 ++
 .../contracts/bootstrap-and-maintenance.md         |   52 +
 .../contracts/hierarchy-and-authorization.md       |  153 +++
 .../contracts/nested-invocation.md                 |  110 ++
 .../contracts/routing-decision.md                  |  151 +++
 .../074a-authorized-routing/coverage-baseline.txt  |  497 +++++++++
 .../specs/074a-authorized-routing/data-model.md    |  258 +++++
 .../specs/074a-authorized-routing/feature-ref.md   |  130 +++
 .../notes/full-baseline-run.txt                    | 1057 +++++++++++++++++++
 .../074a-authorized-routing/notes/golden-rows.txt  |   15 +
 .../074a-authorized-routing/notes/golden-run1.json |  373 +++++++
 .../074a-authorized-routing/notes/golden-run2.json |  373 +++++++
 .../notes/green-t016-demo.txt                      |   99 ++
 .../074a-authorized-routing/notes/green-t016.txt   |    2 +
 .../074a-authorized-routing/notes/green-t017.txt   |    3 +
 .../074a-authorized-routing/notes/green-t021.txt   |    3 +
 .../notes/green-t025-targeted.txt                  |   29 +
 .../074a-authorized-routing/notes/green-t025.txt   |    3 +
 .../074a-authorized-routing/notes/part5-failed.txt |    0
 .../notes/part5-regression.txt                     |   33 +
 .../notes/pre-change-measurements.md               |  228 +++++
 .../notes/quickstart-run.md                        | 1081 ++++++++++++++++++++
 .../notes/red-first-evidence.md                    |  420 ++++++++
 .../074a-authorized-routing/notes/red-t005.txt     |  120 +++
 .../074a-authorized-routing/notes/red-t007.txt     |  226 ++++
 .../074a-authorized-routing/notes/red-t012.txt     |  837 +++++++++++++++
 .../074a-authorized-routing/notes/red-t018.txt     |  467 +++++++++
 .../074a-authorized-routing/notes/red-t022.txt     |  202 ++++
 .../notes/targeted-set-v1-failed.txt               |    0
 .specify/specs/074a-authorized-routing/plan.md     |  359 +++++++
 .../specs/074a-authorized-routing/quickstart.md    |  195 ++++
 .../specs/074a-authorized-routing/requirements.md  |  513 ++++++++++
 .specify/specs/074a-authorized-routing/research.md |  218 ++++
 .specify/specs/074a-authorized-routing/tasks.md    |  271 +++++
 .../test-evidence/analyze-fix-checks.md            |  154 +++
 .../test-evidence/checklist-stage-checks.md        |   93 ++
 .../test-evidence/implement.jsonl                  |    7 +
 .../test-evidence/plan-stage-checks.md             |  208 ++++
 .../test-evidence/targeted-set-v1-baseline.txt     |   19 +
 .../test-evidence/tasks-stage-checks.md            |  172 ++++
 .../specs/074a-authorized-routing/verification.md  |  248 +++++
 scripts/python/sdd-route.py                        | 1045 +++++++++++++++++++
 shared/definitions/sdd-routing-definitions.md      |  212 ++++
 shared/definitions/subagent-definitions.md         |   16 +-
 skills/external/sdd-loop-driver/SKILL.md           |   21 +
 .../references/nested-invocation.md                |   79 ++
 .../internal/create-team/references/create-mode.md |    6 +
 skills/internal/run-agent/SKILL.md                 |   42 +-
 src/specify_cli/__init__.py                        |   18 +-
 tests/contract/test_nested_sdd_invocation.py       |  563 ++++++++++
 tests/contract/test_neutral_metadata_schema.py     |    4 +
 tests/contract/test_sdd_authorization.py           |  269 +++++
 tests/contract/test_sdd_invocation_governance.py   |  490 +++++++++
 tests/contract/test_sdd_routing_definitions.py     |  437 ++++++++
 tests/contract/test_sdd_routing_engine.py          |  856 ++++++++++++++++
 tests/fixtures/nested_sdd.py                       |  369 +++++++
 69 files changed, 15492 insertions(+), 21 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] tests/contract/test_nested_sdd_invocation.py (Line 470)

> SC-003's zero-merge / zero-push face is asserted by comparing a scratch repo's log+status+branch+HEAD before and after a call to the authorize action. Nothing in the case performs or simulates a nested run, so the assertion cannot go red when its subject breaks; it is a tripwire, not evidence. The module docstring discloses the absence of an executable nested run, and D-3 declares the content face, so this is answered rather than blocking - but the SC-003 'pass' row should be read as 'artifact-chain + path-reference content face', never as a measured zero-merge property.

<sub>12:02:03</sub>


### 🟢 [SUGGESTION] scripts/python/sdd-route.py (Line 284)

> _resolve_seat_half refuses the whole (team, seat) resolution when ANY seat key in the map is dangling, including an entry for a seat nobody is asking about. The rule it enforces (create-mode.md rule b: report dangling, never silently ignore) is satisfied by naming the offending key, which the message does; but the blast radius is wider than the rule - one stale roster entry makes every seat of that team unresolvable, and the caller sees an exit-2 input error instead of a policy verdict for its own seat. Consider refusing only when the dangling key is the seat under resolution, and otherwise proceeding with the resolved seat.

<sub>12:02:03</sub>


### 🟢 [SUGGESTION] tests/contract/test_sdd_invocation_governance.py (Line 201)

> The C-9..C-16 cases assert token presence in prose ('sdd-invocation', 'seat policy', 'depth 2', 'no scheduler'). They do go red when a statement is deleted (the T022 red run proves it), and the exclusivity case does assert a negative; but a rewrite that keeps every token while inverting a meaning stays green. This is the weakest evidence class in the delta and it should not be read as proof that the predicate is enforced - the only executable half in the delta is the authorize action itself.

<sub>12:02:03</sub>


### ❓ [QUESTION] scripts/python/sdd-route.py (Line 180)

> C-27 / FR-013 say the verdict MUST be recorded in the Agent execution evidence and referenced by stable path. The delta delivers the record SHAPE (the route payload's E4 face, pinned by test_record_carries_the_e4_face_and_invents_no_clock) and a pre-recorded fixture record; it delivers no writer, because the engine is read-only by design. Question for the next slice: is 'the caller writes the record' a 074b deliverable, or does it stay an agent duty with no mechanical carrier? Today a duty can skip the write and nothing in the repository notices.

<sub>12:02:03</sub>


### 👍 [PRAISE] tests/contract/test_sdd_routing_engine.py (Line 724)

> test_route_follows_a_renamed_reason_code / _a_reordered_precedence / _a_mutated_value_domain are the strongest cases in the delta: they mutate a copy of the owner document and require the verdict to follow, which is the only way to prove the four routing facts are read at run time rather than carried as a second copy. Keep them.

<sub>12:02:03</sub>


### 👍 [PRAISE] scripts/python/sdd-route.py (Line 430)

> _owner_doc_path resolves the owner document from the script's own location and never walks up to an ancestor holding .specify/, with the two-hats trap named in the docstring - the exact defect class the ambient dogfooding section warns about, avoided deliberately. Same for the fixture's refusal to build inside the framework tree and its explicit cwd on every subprocess.

<sub>12:02:03</sub>


> **未提交范围（未评审）**: 49 个未提交路径未计入本次评审对象（.specify/memory/session/20261019T133423Z-run-determination-speckit-tasks-tasks-063-20261019t133409z.md, .specify/memory/session/20261024T124553Z-run-determination-speckit-tasks-tasks-069a-20261024t1245z.md, .specify/memory/session/20261027T070314Z-run-determination-speckit-analyze-r20261027t061144z-a3ec.md, .specify/memory/exec-quant/records/20261028T124651937182Z-7fd772fb.json, .specify/memory/exec-quant/records/20261028T124652237453Z-e4ba14f4.json, .specify/memory/exec-quant/records/20261028T131040921319Z-0fce00d5.json, .specify/memory/exec-quant/records/20261028T131041222137Z-9c32540e.json, .specify/memory/exec-quant/records/20261028T134350629408Z-c59db43d.json, .specify/memory/exec-quant/records/20261028T134548856368Z-4f876af9.json, .specify/memory/exec-quant/records/20261028T152505986776Z-4f97c686.json, .specify/memory/exec-quant/records/20261028T160403218399Z-7663625e.json, .specify/memory/exec-quant/records/20261029T020007282103Z-e5f8d1e6.json, .specify/memory/exec-quant/records/20261029T021014316987Z-0f6b248c.json, .specify/memory/exec-quant/records/20261029T022001803573Z-2ae19888.json, .specify/memory/exec-quant/records/20261029T022536807989Z-62e25de8.json, .specify/memory/exec-quant/records/20261029T023140000541Z-c8e92070.json, .specify/memory/exec-quant/records/20261029T025011351885Z-51cf9de6.json, .specify/memory/exec-quant/records/20261029T035638996096Z-56c7b7cc.json, .specify/memory/feedback/20261028T124704Z-speckit-requirements.md, .specify/memory/feedback/20261028T124708Z-skill-create-requirements.md, .specify/memory/feedback/20261028T131050Z-speckit-clarify.md, .specify/memory/feedback/20261028T131053Z-skill-clarify-artifact.md, .specify/memory/feedback/20261028T134353Z-speckit-plan.md, .specify/memory/feedback/20261028T134552Z-skill-sdd-loop-driver.md, .specify/memory/feedback/20261028T152509Z-speckit-tasks.md, .specify/memory/feedback/20261028T160637Z-speckit-requirements.md, .specify/memory/feedback/20261029T020012Z-speckit-clarify.md, .specify/memory/feedback/20261029T021018Z-speckit-plan.md, .specify/memory/feedback/20261029T022007Z-speckit-tasks.md, .specify/memory/feedback/20261029T022540Z-speckit-checklist.md, .specify/memory/feedback/20261029T023143Z-speckit-analyze.md, .specify/memory/feedback/20261029T025017Z-speckit-analyze.md, .specify/memory/feedback/20261029T035644Z-speckit-implement.md, .specify/memory/session/20261028T124645Z-run-determination-speckit-requirements-20261028t1245z-074-go.md, .specify/memory/session/20261028T124648Z-run-determination-skill-create-requirements-20261028t1245z-0.md, .specify/memory/session/20261028T131037Z-run-determination-speckit-clarify-20261028t1305z-074-clarify.md, .specify/memory/session/20261028T131038Z-run-determination-skill-clarify-artifact-20261028t1305z-074.md, .specify/memory/session/20261028T134339Z-run-determination-speckit-plan-r20261028t132000z-074d.md, .specify/memory/session/20261028T134545Z-run-determination-skill-sdd-loop-driver-r20261028t132000z-07.md, .specify/memory/session/20261028T152503Z-run-determination-speckit-tasks-r20261028t132000z-074d.md, .specify/memory/session/20261028T160359Z-run-determination-speckit-requirements-r20261028t132000z-074.md, .specify/memory/session/20261029T020004Z-run-determination-speckit-clarify-20261029t0200z-074a-clarif.md, .specify/memory/session/20261029T021009Z-run-determination-speckit-plan-r20261028t132000z-074d-plan2.md, .specify/memory/session/20261029T021955Z-run-determination-speckit-tasks-r20261028t132000z-074d-tasks.md, .specify/memory/session/20261029T022534Z-run-determination-speckit-checklist-r20261028t132000z-074d-c.md, .specify/memory/session/20261029T023137Z-run-determination-speckit-analyze-r20261028t132000z-074d-ana.md, .specify/memory/session/20261029T025007Z-run-determination-speckit-analyze-r20261029t024852z-074d-ana.md, .specify/memory/session/20261029T035638Z-run-determination-speckit-implement-r20261028t132000z-074d.md, .specify/state/074-goal-team-sdd-unification.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=371869045d7c86cace67bb49b40b5aa2fd18ceb0
head=0024585c4a58af455a19aec218396e8098d05748
base_source=feature-first-commit
renderer=text
changed_files=69
judged_files=9
skipped_files=60
gap_files=0
lines_added=15492
lines_deleted=21
file.01.path=.specify/memory/features.md
file.01.verdict=skipped
file.01.reason=non-code-file
file.02.path=.specify/memory/features/074.md
file.02.verdict=skipped
file.02.reason=non-code-file
file.03.path=.specify/scripts/python/sdd-route.py
file.03.verdict=skipped
file.03.reason=generated
file.04.path=.specify/shared/definitions/sdd-routing-definitions.md
file.04.verdict=skipped
file.04.reason=generated
file.05.path=.specify/shared/definitions/subagent-definitions.md
file.05.verdict=skipped
file.05.reason=generated
file.06.path=.specify/skills/internal/create-team/references/create-mode.md
file.06.verdict=skipped
file.06.reason=generated
file.07.path=.specify/skills/internal/run-agent/SKILL.md
file.07.verdict=skipped
file.07.reason=generated
file.08.path=.specify/skills/sdd-loop-driver/SKILL.md
file.08.verdict=skipped
file.08.reason=generated
file.09.path=.specify/skills/sdd-loop-driver/references/nested-invocation.md
file.09.verdict=skipped
file.09.reason=generated
file.10.path=.specify/specs/074-goal-team-sdd-unification/requirements.md
file.10.verdict=skipped
file.10.reason=non-code-file
file.11.path=.specify/specs/074a-authorized-routing/baseline-failed.txt
file.11.verdict=skipped
file.11.reason=non-code-file
file.12.path=.specify/specs/074a-authorized-routing/checklists/readiness-2026-10-29.md
file.12.verdict=skipped
file.12.reason=non-code-file
file.13.path=.specify/specs/074a-authorized-routing/checklists/recheck-2026-10-29-implement-start.md
file.13.verdict=skipped
file.13.reason=non-code-file
file.14.path=.specify/specs/074a-authorized-routing/checklists/requirements.md
file.14.verdict=skipped
file.14.reason=non-code-file
file.15.path=.specify/specs/074a-authorized-routing/contracts/bootstrap-and-maintenance.md
file.15.verdict=skipped
file.15.reason=non-code-file
file.16.path=.specify/specs/074a-authorized-routing/contracts/hierarchy-and-authorization.md
file.16.verdict=skipped
file.16.reason=non-code-file
file.17.path=.specify/specs/074a-authorized-routing/contracts/nested-invocation.md
file.17.verdict=skipped
file.17.reason=non-code-file
file.18.path=.specify/specs/074a-authorized-routing/contracts/routing-decision.md
file.18.verdict=skipped
file.18.reason=non-code-file
file.19.path=.specify/specs/074a-authorized-routing/coverage-baseline.txt
file.19.verdict=skipped
file.19.reason=non-code-file
file.20.path=.specify/specs/074a-authorized-routing/data-model.md
file.20.verdict=skipped
file.20.reason=non-code-file
file.21.path=.specify/specs/074a-authorized-routing/feature-ref.md
file.21.verdict=skipped
file.21.reason=non-code-file
file.22.path=.specify/specs/074a-authorized-routing/notes/full-baseline-run.txt
file.22.verdict=skipped
file.22.reason=non-code-file
file.23.path=.specify/specs/074a-authorized-routing/notes/golden-rows.txt
file.23.verdict=skipped
file.23.reason=non-code-file
file.24.path=.specify/specs/074a-authorized-routing/notes/golden-run1.json
file.24.verdict=skipped
file.24.reason=non-code-file
file.25.path=.specify/specs/074a-authorized-routing/notes/golden-run2.json
file.25.verdict=skipped
file.25.reason=non-code-file
file.26.path=.specify/specs/074a-authorized-routing/notes/green-t016-demo.txt
file.26.verdict=skipped
file.26.reason=non-code-file
file.27.path=.specify/specs/074a-authorized-routing/notes/green-t016.txt
file.27.verdict=skipped
file.27.reason=non-code-file
file.28.path=.specify/specs/074a-authorized-routing/notes/green-t017.txt
file.28.verdict=skipped
file.28.reason=non-code-file
file.29.path=.specify/specs/074a-authorized-routing/notes/green-t021.txt
file.29.verdict=skipped
file.29.reason=non-code-file
file.30.path=.specify/specs/074a-authorized-routing/notes/green-t025-targeted.txt
file.30.verdict=skipped
file.30.reason=non-code-file
file.31.path=.specify/specs/074a-authorized-routing/notes/green-t025.txt
file.31.verdict=skipped
file.31.reason=non-code-file
file.32.path=.specify/specs/074a-authorized-routing/notes/part5-failed.txt
file.32.verdict=skipped
file.32.reason=non-code-file
file.33.path=.specify/specs/074a-authorized-routing/notes/part5-regression.txt
file.33.verdict=skipped
file.33.reason=non-code-file
file.34.path=.specify/specs/074a-authorized-routing/notes/pre-change-measurements.md
file.34.verdict=skipped
file.34.reason=non-code-file
file.35.path=.specify/specs/074a-authorized-routing/notes/quickstart-run.md
file.35.verdict=skipped
file.35.reason=non-code-file
file.36.path=.specify/specs/074a-authorized-routing/notes/red-first-evidence.md
file.36.verdict=skipped
file.36.reason=non-code-file
file.37.path=.specify/specs/074a-authorized-routing/notes/red-t005.txt
file.37.verdict=skipped
file.37.reason=non-code-file
file.38.path=.specify/specs/074a-authorized-routing/notes/red-t007.txt
file.38.verdict=skipped
file.38.reason=non-code-file
file.39.path=.specify/specs/074a-authorized-routing/notes/red-t012.txt
file.39.verdict=skipped
file.39.reason=non-code-file
file.40.path=.specify/specs/074a-authorized-routing/notes/red-t018.txt
file.40.verdict=skipped
file.40.reason=non-code-file
file.41.path=.specify/specs/074a-authorized-routing/notes/red-t022.txt
file.41.verdict=skipped
file.41.reason=non-code-file
file.42.path=.specify/specs/074a-authorized-routing/notes/targeted-set-v1-failed.txt
file.42.verdict=skipped
file.42.reason=non-code-file
file.43.path=.specify/specs/074a-authorized-routing/plan.md
file.43.verdict=skipped
file.43.reason=non-code-file
file.44.path=.specify/specs/074a-authorized-routing/quickstart.md
file.44.verdict=skipped
file.44.reason=non-code-file
file.45.path=.specify/specs/074a-authorized-routing/requirements.md
file.45.verdict=skipped
file.45.reason=non-code-file
file.46.path=.specify/specs/074a-authorized-routing/research.md
file.46.verdict=skipped
file.46.reason=non-code-file
file.47.path=.specify/specs/074a-authorized-routing/tasks.md
file.47.verdict=skipped
file.47.reason=non-code-file
file.48.path=.specify/specs/074a-authorized-routing/test-evidence/analyze-fix-checks.md
file.48.verdict=skipped
file.48.reason=non-code-file
file.49.path=.specify/specs/074a-authorized-routing/test-evidence/checklist-stage-checks.md
file.49.verdict=skipped
file.49.reason=non-code-file
file.50.path=.specify/specs/074a-authorized-routing/test-evidence/implement.jsonl
file.50.verdict=skipped
file.50.reason=non-code-file
file.51.path=.specify/specs/074a-authorized-routing/test-evidence/plan-stage-checks.md
file.51.verdict=skipped
file.51.reason=non-code-file
file.52.path=.specify/specs/074a-authorized-routing/test-evidence/targeted-set-v1-baseline.txt
file.52.verdict=skipped
file.52.reason=non-code-file
file.53.path=.specify/specs/074a-authorized-routing/test-evidence/tasks-stage-checks.md
file.53.verdict=skipped
file.53.reason=non-code-file
file.54.path=.specify/specs/074a-authorized-routing/verification.md
file.54.verdict=skipped
file.54.reason=non-code-file
file.55.path=scripts/python/sdd-route.py
file.55.verdict=reviewed
file.56.path=shared/definitions/sdd-routing-definitions.md
file.56.verdict=skipped
file.56.reason=non-code-file
file.57.path=shared/definitions/subagent-definitions.md
file.57.verdict=skipped
file.57.reason=non-code-file
file.58.path=skills/external/sdd-loop-driver/SKILL.md
file.58.verdict=skipped
file.58.reason=non-code-file
file.59.path=skills/external/sdd-loop-driver/references/nested-invocation.md
file.59.verdict=skipped
file.59.reason=non-code-file
file.60.path=skills/internal/create-team/references/create-mode.md
file.60.verdict=skipped
file.60.reason=non-code-file
file.61.path=skills/internal/run-agent/SKILL.md
file.61.verdict=skipped
file.61.reason=non-code-file
file.62.path=src/specify_cli/__init__.py
file.62.verdict=reviewed
file.63.path=tests/contract/test_nested_sdd_invocation.py
file.63.verdict=reviewed
file.64.path=tests/contract/test_neutral_metadata_schema.py
file.64.verdict=reviewed
file.65.path=tests/contract/test_sdd_authorization.py
file.65.verdict=reviewed
file.66.path=tests/contract/test_sdd_invocation_governance.py
file.66.verdict=reviewed
file.67.path=tests/contract/test_sdd_routing_definitions.py
file.67.verdict=reviewed
file.68.path=tests/contract/test_sdd_routing_engine.py
file.68.verdict=reviewed
file.69.path=tests/fixtures/nested_sdd.py
file.69.verdict=reviewed
<!-- coverage-receipt:end -->
