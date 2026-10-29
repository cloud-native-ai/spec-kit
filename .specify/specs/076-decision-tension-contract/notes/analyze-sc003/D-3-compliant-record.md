# SC-003 analyze snapshot — D-3-compliant-record

- fixture: same fixture with one compliant T-001 record written in place of the N/A block
- judged artifact: `plan.md` under `REQUIREMENTS_DIR` (the channel's only object; `requirements.md` is the mapping reference, never a second judged object)
- validator: `scripts/python/validate-decision-tensions.py --spec <fixture> --json`
- exit_code: 0
- records: 1
- HIGH findings: 0

| label | status | count |
|---|---|---|
| `dtr-anchor` | pass | 0 |
| `dtr-section-missing` | pass | 0 |
| `dtr-record-incomplete` | pass | 0 |
| `dtr-tension-id` | pass | 0 |
| `dtr-rejected-form` | pass | 0 |
| `expected-sacrifice-unmapped` | pass | 0 |
