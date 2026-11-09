# Verification — 901-fixture

| SC | Path | Status | Evidence |
|----|------|--------|----------|
| SC-001 | final | **pass** | the fixture is its own evidence |

SC-001_status=pass
SC-001_note=the fixture records its own reading
SC-001_evidence=the fixture itself
SC-001_verified_at=2026-11-09

smoke_command: `python3 -m pytest -q tests/contract/test_non_disposable_check.py`
smoke_exit_code: 0
smoke_evidence_path: `tests/fixtures/non-disposable/surface.yaml`
smoke_comparison: exit 0 and the same finding count as the recorded run
