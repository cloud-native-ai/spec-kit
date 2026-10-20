# Line State Spine — fixture (valid two-slot ledger)

## Admission (E1)

```text
decision=fast-lane
entry_evidence=fast-lane=opt-in
lines_manifest_ptr=012-medium/lines.manifest
measured.fr_count=12
measured.task_count=25
decided_at=2026-10-20T00:00:00Z
criteria:
  a: pass — FR 12 and tasks 25 inside the frozen ranges
  b: pass — no constitution change in base..HEAD
  c: pass — no engine/template/dependency path touched
  d: pass — no sensitive surface touched
  e: pass — one lines.manifest record for this branch
  f: pass — clarify complete, zero open markers, related feature resolved
  g: pass — requirements quality checklist all checked
checklist=skipped(fast-lane)
```

## Test Budget (E2)

<!-- test-budget:begin -->
{"seq":1,"slot":"baseline","stage":"implement","purpose":"implement-start-baseline","trigger":"scheduled","at":"2026-10-20T00:10:00Z","command":"bash scripts/bash/run-tests.sh --names-out baseline-failed.txt","selection_basis":"full-suite","rc":1,"passed":100,"failed":2,"failed_names_path":"baseline-failed.txt","baseline_compare":"na","evidence_ptr":"logs/baseline.log","merge_source":"na","merged_at":"na"}
{"seq":2,"slot":"closure","stage":"review","purpose":"final-closure","trigger":"scheduled","at":"2026-10-20T02:00:00Z","command":"bash scripts/bash/run-tests.sh --names-out final-failed.txt","selection_basis":"full-suite","rc":0,"passed":102,"failed":0,"failed_names_path":"final-failed.txt","baseline_compare":"comm -13 baseline-failed.txt final-failed.txt -> 0 new failures","evidence_ptr":"logs/closure.log","merge_source":"na","merged_at":"na"}
<!-- test-budget:end -->

## Targeted Evidence (E3 fixture row for the audit linkage case)

```json
{"stage":"checklist","row_type":"stage-status","status":"not-applicable-skipped-stage","command":"","selection_basis":"E1 fast-lane admission + checklist=skipped(fast-lane)","selected_paths":[],"sufficiency":"stage skipped by the ratified fast lane (E1)","rc":0,"passed":0,"failed":0,"new_failures":[],"baseline":"na","changed_paths":[],"evidence_ptr":"state-spine-valid.md#admission"}
```
