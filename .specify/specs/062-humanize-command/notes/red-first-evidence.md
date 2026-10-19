# Red-First Evidence (T002)

**Feature**: 062-humanize-command | **Discipline**: Constitution IV template-only Red-Green — the structural contract test landed before the artifacts exist; red = an asserted path/literal is not there yet.

## Test authored

`tests/contract/test_humanize_command_surface.py` — `test_c01`..`test_c10` per `contracts/command-surface.md` § 可追溯性 (one function per clause).

## RED run (pre-implementation, 2026-10-19)

```bash
python3 -m pytest tests/contract/test_humanize_command_surface.py
# exit code: 1
# ========================= 8 failed, 2 passed in 0.08s ==========================
```

Failed (artifacts absent — the intended red):

| Test | First failing assertion |
|------|------------------------|
| test_c01_thin_entry_shape | `thin command template missing: templates/commands/humanize.md` |
| test_c02_single_skill_delegation | `delegation must name exactly one skill (found 0 SKILL.md mentions)` |
| test_c03_skill_frontmatter_and_self_sufficient | `external skill missing: skills/external/humanize/SKILL.md` |
| test_c04_generated_copies_present | `generated copy missing: .claude/commands/speckit.humanize.md` |
| test_c05_docs_page_content | `docs page missing: docs/reference/commands/humanize.md` |
| test_c07_skill_probe_unit_and_compiled_wrapup | `probe-definitions lacks the skill-humanize-wrapup unit row` |
| test_c09_baseline_no_new_failures | `027 classification table lacks a humanize row` |
| test_c10_detector_honesty_wording | `no humanize surfaces exist yet (expected red before implementation)` |

Passed pre-implementation (already-true structural facts, per C-6/C-9 wording):

- `test_c06_registry_rows_resolve` — the 062 registry row + details file landed at clarify (dated record 2026-10-19); C-6 says implementation-time verification of existence, not re-registration.
- `test_c08_no_runtime_surface` — trivially true before any surface exists; it stays meaningful as a regression guard after implementation (T006+ must not add runtime code).

## GREEN obligations (downstream of this evidence)

The 8 red tests turn green at: T006 (c01, c02), T007 (c03), T020 (c04), T022 (c05), T018/T019/T021 (c07), T017 + T026 (c09), T022/T007 (c10 wording windows authored honestly from the start).

Baseline comparison stays a runtime gate: full-suite name-level `comm -13` vs `notes/baseline-failed-tests.txt` must be empty at GATE-7 (C-9), recorded in `verification.md` — not re-run inside this test file.
