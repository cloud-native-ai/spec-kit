# Unattended reporting — root fix (2026-11-09)

Owner: `shared/guidelines/progress-reporting.md` (new `## 无人值守模式（Unattended Mode）`).
Ambient: `templates/instructions-template.md` + `.specify/instructions.md` (one sentence + pointer).
Rule: a run declared unattended emits ONE final-state report at completion; periodic "where we are / what remains" narration is suppressed; anomalies still surface immediately (fast-fail). Interactive 15-min cadence and the reporter-seat long-run cadence are unchanged.
Guards: `test_progress_reporting.py` green; `test_proactive_trigger_section::test_c11` remains the known baseline failure.
