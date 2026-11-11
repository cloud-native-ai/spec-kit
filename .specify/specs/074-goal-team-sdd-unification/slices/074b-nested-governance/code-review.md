# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `074b-nested-governance` |
| **基准** | `9360718a1801b7686ecb6730df1a6ec028b3d247` (`9360718a1`) |
| **目标** | `91726a64171c3fcbb265ae0cacabb5ed5390c176` (`91726a641`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-10-29T06:50:58Z` |

## 变更概览

```
 .specify/instructions.md                           |  11 +
 .specify/memory/features.md                        |   2 +-
 .specify/memory/features/074.md                    |  17 +-
 .specify/shared/guidelines/proactive-trigger.md    |   2 +
 .specify/skills/internal/create-team/SKILL.md      |  14 +
 .../create-team/references/conceptual-model.md     |   2 +-
 .specify/skills/internal/run-agent/SKILL.md        |   9 +
 .../specs/074-goal-team-sdd-unification/tasks.md   |   2 +
 .../074-goal-team-sdd-unification/verification.md  |  41 +
 .../074b-nested-governance/baseline-failed.txt     |  21 +
 .../checklists/readiness-2026-10-29.md             | 154 ++++
 .../checklists/requirements.md                     |  90 ++
 .../contracts/compat-and-safety.md                 | 107 +++
 .../074b-nested-governance/contracts/diffusion.md  |  79 ++
 .../contracts/report-and-attribution.md            |  89 ++
 .../074b-nested-governance/coverage-baseline.txt   | 497 ++++++++++
 .../specs/074b-nested-governance/data-model.md     | 169 ++++
 .../specs/074b-nested-governance/feature-ref.md    | 124 +++
 .../notes/pre-change-file-sets.txt                 | 688 ++++++++++++++
 .../notes/pre-change-measurements.md               | 303 +++++++
 .../074b-nested-governance/notes/quickstart-run.md | 399 +++++++++
 .../notes/red-first-evidence.md                    | 426 +++++++++
 .specify/specs/074b-nested-governance/plan.md      | 374 ++++++++
 .../specs/074b-nested-governance/quickstart.md     | 245 +++++
 .../specs/074b-nested-governance/requirements.md   | 307 +++++++
 .specify/specs/074b-nested-governance/research.md  | 296 ++++++
 .specify/specs/074b-nested-governance/tasks.md     | 256 ++++++
 .../test-evidence/analyze-fix-checks.md            | 201 +++++
 .../test-evidence/checklist-stage-checks.md        | 163 ++++
 .../test-evidence/compat-baseline-nodeids.txt      | 301 +++++++
 .../containment-post-change-collect.txt            | 313 +++++++
 .../test-evidence/containment-post-change-run.txt  |  34 +
 .../test-evidence/implement-baseline-run.txt       | 996 +++++++++++++++++++++
 .../implement-targeted-part1-failed.txt            |   1 +
 .../test-evidence/implement-targeted-part1-run.txt |  63 ++
 .../implement-targeted-part1-supp-failed.txt       |   1 +
 .../implement-targeted-part1-supp-run.txt          |  42 +
 .../implement-targeted-part2-failed.txt            |   1 +
 .../test-evidence/implement-targeted-part2-run.txt |  64 ++
 .../implement-targeted-part2-supp-failed.txt       |   3 +
 .../implement-targeted-part2-supp-run.txt          | 100 +++
 .../implement-targeted-part3-failed.txt            |   1 +
 .../test-evidence/implement-targeted-part3-run.txt |  68 ++
 .../implement-targeted-part4-failed.txt            |   1 +
 .../test-evidence/implement-targeted-part4-run.txt |  73 ++
 .../test-evidence/implement.jsonl                  |   8 +
 .../test-evidence/plan-stage-checks.md             | 258 ++++++
 .../test-evidence/requirements-checks.txt          |  52 ++
 .../test-evidence/targeted-set-v1-baseline.txt     |  94 ++
 .../test-evidence/tasks-stage-checks.md            | 221 +++++
 .../specs/074b-nested-governance/verification.md   | 282 ++++++
 .specify/templates/instructions-template.md        |  11 +
 shared/guidelines/proactive-trigger.md             |   2 +
 skills/internal/create-team/SKILL.md               |  14 +
 .../create-team/references/conceptual-model.md     |   2 +-
 skills/internal/run-agent/SKILL.md                 |   9 +
 templates/instructions-template.md                 |  11 +
 tests/contract/test_fast_fail_discipline.py        |  13 +-
 tests/contract/test_nested_run_report.py           | 558 ++++++++++++
 tests/contract/test_sdd_compat_containment.py      | 360 ++++++++
 tests/contract/test_sdd_diffusion.py               | 648 ++++++++++++++
 tests/contract/test_sdd_invocation_governance.py   | 174 +++-
 62 files changed, 9854 insertions(+), 13 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] skills/internal/create-team/SKILL.md (Line 80)

> The section states the outcome closed set only as `[[STR-004]]` / `[[STR-005]]` / `[[STR-006]]`, and those tokens resolve to the WRONG values through every registry pointer that is live in this repo:
(a) `shared/definitions/sdd-routing-definitions.md:16` — the only registration sentence a shipped document carries — says (quoted with the upper token written plainly, because the registered form of it dangles here) "`[[STR-001]]` … STR-010 的取值与语义 owner 是本特性切片的 requirements.md § Shared Strings" and points at `074a`'s registry, where STR-004/005/006 are `"sdd"` / `"direct"` / `"adjudicate"` (the routing verdicts), not the outcomes;
(b) the parent authority (`.specify/specs/074-goal-team-sdd-unification/requirements.md` § Shared Strings) names these three literals STR-007/008/009, and `074a`'s shipped `nested-invocation.md:40` cites them under those ids — this slice renumbered them to 004/005/006 in its own requirements table (`Slice STR → Parent STR`: local STR-004 ← parent STR-007);
(c) the file itself carries no registration pointer at all, so a reader in a consuming project — which never receives `.specify/specs/074b-nested-governance/requirements.md` — has no path to the three values, while the section is the sole owner of a contract-mandated closed set.
The slice-local resolution test (`test_sdd_diffusion.py::test_every_shared_string_citation_resolves_to_a_registry_row`) cannot see this: it resolves citations inside the slice directory plus itself, never in the shipped skill.
Answer: agreed — fix by naming the values where the obligation lands (keep the tokens if you wish, but state `completed` / `blocked` / `failed` beside them, as `sdd-routing-definitions.md` does for its own set) or by citing the registry with its owning slice, the convention `.specify/memory/glossary.md:40` already follows (`… Target Decomposition([[STR-004]])` with the owning feature named). Blocking? No: the three values stay recoverable from the handoff owner the same section cites by path (`nested-invocation.md`), so the defect misleads rather than severs.

<sub>14:51:15</sub>


### 🟠 [IMPORTANT] tests/contract/test_sdd_compat_containment.py (Line 131)

> The module measures the C-11 / C-12 negatives ("no new command, no new skill, no new store") over `_delivery_surface()`, which parses the nine rows of `feature-ref.md` § 2 — the slice own declaration of what it delivers — and never over the committed delta. The header claims the stronger rule ("The delivery surface is read, not recalled"), but reading a self-declaration is not reading the change set: a file the slice actually edited and forgot to declare is invisible to every case here, so the check cannot go red on the one failure mode it exists to catch.
That is not hypothetical in this delta: `tests/contract/test_fast_fail_discipline.py` is edited (pin 29/30 -> 30/31) and is not row 10 of § 2, so the delta holds ten code files where the declaration says nine, and no case in this module notices.
Answer: agreed as a defect of the check shape, not of the C-11 conclusion — flow-class (79 units / 0 findings) and the command-template count carry that conclusion independently. Fix: derive the judged path set from `git diff --name-only base..head` (the receipt already knows the range) and use § 2 only to check that every NEW row is a test, which is what the clause actually claims.

<sub>14:51:22</sub>


### 🟢 [SUGGESTION] tests/contract/test_sdd_diffusion.py (Line 111)

> `PRE_CHANGE_GATE_TOTAL = 27` is a second, independent pin of a fact that already has an owner: `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` pins the same scan total against its frozen 23 and is the recorded pre-existing red. Two live literals now disagree about one fact (27 vs 23) and nothing states which one a future repair must move; when the four-gate debt behind the red is paid, this constant goes stale silently, and its failure message ("the headroom on that budget is 0") will read as a regression of this slice.
The slice genuinely needs "the total after equals the total before" — that is the criterion. Suggested shape: measure the before-value in the same test run (scan the base commit into a temp worktree) or derive it from the owner, so the fact keeps one owner instead of two.

<sub>14:51:22</sub>


### 🟢 [SUGGESTION] tests/contract/test_sdd_invocation_governance.py (Line 331)

> `_absent_copy(declared_path, declared_path)` passes the same path as source and target. It works (the read completes before the write), but the helper is documented as producing a (declared, absent) pair of documents, and the in-place call makes the review reason about aliasing to decide whether the comparison is between two documents or between two states of one. `_absent_copy(declared_path, absent_path)` states the intent and removes the question.

<sub>14:51:22</sub>


### 👍 [PRAISE] tests/contract/test_sdd_diffusion.py (Line 197)

> The reverse-count audit takes its query set from the landed owner (`_routing_owner_query_set()` extracts the backticked tokens of the routing owner § Inputs / § Verdict table / § Reason codes) and asserts the extracted set is non-empty before counting. A copy detector written from remembered phrases cannot detect a copy; this one cannot go vacuous silently.

<sub>14:51:26</sub>


### 👍 [PRAISE] tests/contract/test_sdd_compat_containment.py (Line 281)

> The gate-scan absence check carries its own positive control (the scanner must report gates in two sibling documents of the same families), so an empty intersection is evidence rather than a blind pass. That is the discipline the whole module header states, applied where it is hardest.

<sub>14:51:26</sub>


### 👍 [PRAISE] tests/contract/test_nested_run_report.py (Line 497)

> The attribution boundary is measured with the real engine (`goal-utils.parse_goal`) over a fixture goal before and after the ledger row, and the 12-key field set is pinned in the same test — the SC-002 claim is executed in two independent places (here and quickstart S3) rather than asserted once.

<sub>14:51:26</sub>


### 🟢 [SUGGESTION] tests/contract/test_nested_run_report.py (Line 399)

> `test_nested_section_is_a_peer_of_verification_not_a_replacement` ends with a four-way alternation (`回归数字注明口径|同口径|One-Source-Of-Truth|One Source Of Truth`) over the whole `## Verification` body, presented as "its three criteria are still stated". Any one of the four satisfies it, so the case passes on a phrase that has nothing to do with the three criteria it names, and would keep passing if the criteria were deleted. The C-27 subject itself is pinned properly two assertions above; this tail is the only part that cannot go red for its stated reason. Either name the three criteria and count them, or drop the tail and let the case assert what it actually measures.

<sub>14:51:31</sub>




> **未提交范围（未评审）**: 37 个未提交路径未计入本次评审对象（.specify/memory/session/20261024T164126Z-run-determination-speckit-checklist-checklist-069b-20261025t.md, .specify/memory/session/20261027T063828Z-run-determination-speckit-plan-r20261027t061144z-a3ec.md, .specify/memory/session/20261027T065612Z-run-determination-speckit-checklist-r20261027t061144z-a3ec.md, .specify/memory/session/20261027T095352Z-run-determination-speckit-plan-r20261027t095352z-072plan.md, .specify/memory/session/20261028T134339Z-run-determination-speckit-plan-r20261028t132000z-074d.md, .specify/memory/session/20261028T160359Z-run-determination-speckit-requirements-r20261028t132000z-074.md, .specify/memory/session/20261029T021009Z-run-determination-speckit-plan-r20261028t132000z-074d-plan2.md, .specify/memory/session/20261029T022534Z-run-determination-speckit-checklist-r20261028t132000z-074d-c.md, .specify/memory/exec-quant/records/20261029T043134701475Z-49b4c069.json, .specify/memory/exec-quant/records/20261029T043510043737Z-418c9bbc.json, .specify/memory/exec-quant/records/20261029T044654214591Z-4ff0250f.json, .specify/memory/exec-quant/records/20261029T045342638935Z-8bb67394.json, .specify/memory/exec-quant/records/20261029T050019919695Z-dba780bf.json, .specify/memory/exec-quant/records/20261029T050717259584Z-4f40a8a1.json, .specify/memory/exec-quant/records/20261029T052326986793Z-eb6bed6d.json, .specify/memory/exec-quant/records/20261029T053423866846Z-d36c9c5e.json, .specify/memory/exec-quant/records/20261029T064147507252Z-1450eb1c.json, .specify/memory/feedback/20261029T043138Z-speckit-requirements.md, .specify/memory/feedback/20261029T043513Z-speckit-clarify.md, .specify/memory/feedback/20261029T044701Z-speckit-plan.md, .specify/memory/feedback/20261029T045346Z-speckit-tasks.md, .specify/memory/feedback/20261029T050023Z-speckit-checklist.md, .specify/memory/feedback/20261029T050729Z-speckit-analyze.md, .specify/memory/feedback/20261029T052337Z-speckit-analyze.md, .specify/memory/feedback/20261029T053430Z-speckit-analyze.md, .specify/memory/feedback/20261029T064217Z-speckit-implement.md, .specify/memory/session/20261029T043131Z-run-determination-speckit-requirements-r20261029t045000z-b07.md, .specify/memory/session/20261029T043507Z-run-determination-speckit-clarify-r20261029t045000z-b074.md, .specify/memory/session/20261029T044648Z-run-determination-speckit-plan-r20261029t045000z-b074.md, .specify/memory/session/20261029T045337Z-run-determination-speckit-tasks-r20261029t045000z-b074.md, .specify/memory/session/20261029T050017Z-run-determination-speckit-checklist-r20261029t050500z-074bch.md, .specify/memory/session/20261029T050714Z-run-determination-speckit-analyze-r20261029t045000z-b074.md, .specify/memory/session/20261029T052323Z-run-determination-speckit-analyze-r20261029t052224z-b074fix.md, .specify/memory/session/20261029T053420Z-run-determination-speckit-analyze-r20261029t053000z-b074an2.md, .specify/memory/session/20261029T064138Z-run-determination-speckit-implement-r20261029t064500z-074b4.md, .specify/specs/074b-nested-governance/review.md, .specify/state/074b-nested-governance.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=9360718a1801b7686ecb6730df1a6ec028b3d247
head=91726a64171c3fcbb265ae0cacabb5ed5390c176
base_source=feature-first-commit
renderer=text
changed_files=62
judged_files=5
skipped_files=57
gap_files=0
lines_added=9854
lines_deleted=13
file.01.path=.specify/instructions.md
file.01.verdict=skipped
file.01.reason=non-code-file
file.02.path=.specify/memory/features.md
file.02.verdict=skipped
file.02.reason=non-code-file
file.03.path=.specify/memory/features/074.md
file.03.verdict=skipped
file.03.reason=non-code-file
file.04.path=.specify/shared/guidelines/proactive-trigger.md
file.04.verdict=skipped
file.04.reason=non-code-file
file.05.path=.specify/skills/internal/create-team/SKILL.md
file.05.verdict=skipped
file.05.reason=non-code-file
file.06.path=.specify/skills/internal/create-team/references/conceptual-model.md
file.06.verdict=skipped
file.06.reason=non-code-file
file.07.path=.specify/skills/internal/run-agent/SKILL.md
file.07.verdict=skipped
file.07.reason=non-code-file
file.08.path=.specify/specs/074-goal-team-sdd-unification/tasks.md
file.08.verdict=skipped
file.08.reason=non-code-file
file.09.path=.specify/specs/074-goal-team-sdd-unification/verification.md
file.09.verdict=skipped
file.09.reason=non-code-file
file.10.path=.specify/specs/074b-nested-governance/baseline-failed.txt
file.10.verdict=skipped
file.10.reason=non-code-file
file.11.path=.specify/specs/074b-nested-governance/checklists/readiness-2026-10-29.md
file.11.verdict=skipped
file.11.reason=non-code-file
file.12.path=.specify/specs/074b-nested-governance/checklists/requirements.md
file.12.verdict=skipped
file.12.reason=non-code-file
file.13.path=.specify/specs/074b-nested-governance/contracts/compat-and-safety.md
file.13.verdict=skipped
file.13.reason=non-code-file
file.14.path=.specify/specs/074b-nested-governance/contracts/diffusion.md
file.14.verdict=skipped
file.14.reason=non-code-file
file.15.path=.specify/specs/074b-nested-governance/contracts/report-and-attribution.md
file.15.verdict=skipped
file.15.reason=non-code-file
file.16.path=.specify/specs/074b-nested-governance/coverage-baseline.txt
file.16.verdict=skipped
file.16.reason=non-code-file
file.17.path=.specify/specs/074b-nested-governance/data-model.md
file.17.verdict=skipped
file.17.reason=non-code-file
file.18.path=.specify/specs/074b-nested-governance/feature-ref.md
file.18.verdict=skipped
file.18.reason=non-code-file
file.19.path=.specify/specs/074b-nested-governance/notes/pre-change-file-sets.txt
file.19.verdict=skipped
file.19.reason=non-code-file
file.20.path=.specify/specs/074b-nested-governance/notes/pre-change-measurements.md
file.20.verdict=skipped
file.20.reason=non-code-file
file.21.path=.specify/specs/074b-nested-governance/notes/quickstart-run.md
file.21.verdict=skipped
file.21.reason=non-code-file
file.22.path=.specify/specs/074b-nested-governance/notes/red-first-evidence.md
file.22.verdict=skipped
file.22.reason=non-code-file
file.23.path=.specify/specs/074b-nested-governance/plan.md
file.23.verdict=skipped
file.23.reason=non-code-file
file.24.path=.specify/specs/074b-nested-governance/quickstart.md
file.24.verdict=skipped
file.24.reason=non-code-file
file.25.path=.specify/specs/074b-nested-governance/requirements.md
file.25.verdict=skipped
file.25.reason=non-code-file
file.26.path=.specify/specs/074b-nested-governance/research.md
file.26.verdict=skipped
file.26.reason=non-code-file
file.27.path=.specify/specs/074b-nested-governance/tasks.md
file.27.verdict=skipped
file.27.reason=non-code-file
file.28.path=.specify/specs/074b-nested-governance/test-evidence/analyze-fix-checks.md
file.28.verdict=skipped
file.28.reason=non-code-file
file.29.path=.specify/specs/074b-nested-governance/test-evidence/checklist-stage-checks.md
file.29.verdict=skipped
file.29.reason=non-code-file
file.30.path=.specify/specs/074b-nested-governance/test-evidence/compat-baseline-nodeids.txt
file.30.verdict=skipped
file.30.reason=non-code-file
file.31.path=.specify/specs/074b-nested-governance/test-evidence/containment-post-change-collect.txt
file.31.verdict=skipped
file.31.reason=non-code-file
file.32.path=.specify/specs/074b-nested-governance/test-evidence/containment-post-change-run.txt
file.32.verdict=skipped
file.32.reason=non-code-file
file.33.path=.specify/specs/074b-nested-governance/test-evidence/implement-baseline-run.txt
file.33.verdict=skipped
file.33.reason=non-code-file
file.34.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part1-failed.txt
file.34.verdict=skipped
file.34.reason=non-code-file
file.35.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part1-run.txt
file.35.verdict=skipped
file.35.reason=non-code-file
file.36.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part1-supp-failed.txt
file.36.verdict=skipped
file.36.reason=non-code-file
file.37.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part1-supp-run.txt
file.37.verdict=skipped
file.37.reason=non-code-file
file.38.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part2-failed.txt
file.38.verdict=skipped
file.38.reason=non-code-file
file.39.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part2-run.txt
file.39.verdict=skipped
file.39.reason=non-code-file
file.40.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part2-supp-failed.txt
file.40.verdict=skipped
file.40.reason=non-code-file
file.41.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part2-supp-run.txt
file.41.verdict=skipped
file.41.reason=non-code-file
file.42.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part3-failed.txt
file.42.verdict=skipped
file.42.reason=non-code-file
file.43.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part3-run.txt
file.43.verdict=skipped
file.43.reason=non-code-file
file.44.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part4-failed.txt
file.44.verdict=skipped
file.44.reason=non-code-file
file.45.path=.specify/specs/074b-nested-governance/test-evidence/implement-targeted-part4-run.txt
file.45.verdict=skipped
file.45.reason=non-code-file
file.46.path=.specify/specs/074b-nested-governance/test-evidence/implement.jsonl
file.46.verdict=skipped
file.46.reason=non-code-file
file.47.path=.specify/specs/074b-nested-governance/test-evidence/plan-stage-checks.md
file.47.verdict=skipped
file.47.reason=non-code-file
file.48.path=.specify/specs/074b-nested-governance/test-evidence/requirements-checks.txt
file.48.verdict=skipped
file.48.reason=non-code-file
file.49.path=.specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt
file.49.verdict=skipped
file.49.reason=non-code-file
file.50.path=.specify/specs/074b-nested-governance/test-evidence/tasks-stage-checks.md
file.50.verdict=skipped
file.50.reason=non-code-file
file.51.path=.specify/specs/074b-nested-governance/verification.md
file.51.verdict=skipped
file.51.reason=non-code-file
file.52.path=.specify/templates/instructions-template.md
file.52.verdict=skipped
file.52.reason=non-code-file
file.53.path=shared/guidelines/proactive-trigger.md
file.53.verdict=skipped
file.53.reason=non-code-file
file.54.path=skills/internal/create-team/SKILL.md
file.54.verdict=skipped
file.54.reason=non-code-file
file.55.path=skills/internal/create-team/references/conceptual-model.md
file.55.verdict=skipped
file.55.reason=non-code-file
file.56.path=skills/internal/run-agent/SKILL.md
file.56.verdict=skipped
file.56.reason=non-code-file
file.57.path=templates/instructions-template.md
file.57.verdict=skipped
file.57.reason=non-code-file
file.58.path=tests/contract/test_fast_fail_discipline.py
file.58.verdict=reviewed
file.59.path=tests/contract/test_nested_run_report.py
file.59.verdict=reviewed
file.60.path=tests/contract/test_sdd_compat_containment.py
file.60.verdict=reviewed
file.61.path=tests/contract/test_sdd_diffusion.py
file.61.verdict=reviewed
file.62.path=tests/contract/test_sdd_invocation_governance.py
file.62.verdict=reviewed
<!-- coverage-receipt:end -->
