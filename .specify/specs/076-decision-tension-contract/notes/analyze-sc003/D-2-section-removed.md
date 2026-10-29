# SC-003 analyze snapshot — D-2-section-removed

- fixture: trivial plan plus one irreversible decision (rollback requires a migration), compliant N/A section removed
- judged artifact: `plan.md` under `REQUIREMENTS_DIR` (the channel's only object; `requirements.md` is the mapping reference, never a second judged object)
- validator: `scripts/python/validate-decision-tensions.py --spec <fixture> --json`
- exit_code: 1
- records: 0
- HIGH findings: 1

| label | status | count |
|---|---|---|
| `dtr-anchor` | pass | 0 |
| `dtr-section-missing` | fail | 1 |
| `dtr-record-incomplete` | pass | 0 |
| `dtr-tension-id` | pass | 0 |
| `dtr-rejected-form` | pass | 0 |
| `expected-sacrifice-unmapped` | pass | 0 |
