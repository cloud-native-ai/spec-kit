# SC-002 analyze snapshot — S3-record-incomplete

- fixture: one record missing `revision_trigger`
- judged artifact: `plan.md` under `REQUIREMENTS_DIR` (the channel's only object; `requirements.md` is the mapping reference, never a second judged object)
- validator: `scripts/python/validate-decision-tensions.py --spec <fixture> --json`
- channel severity mapping: every finding of this channel is HIGH or absent (`detection-and-severity.md` § I declares HIGH-or-0 with no advisory tier)
- exit_code: 1
- records: 1
- HIGH findings: 1

| label | status | count |
|---|---|---|
| `dtr-anchor` | pass | 0 |
| `dtr-section-missing` | pass | 0 |
| `dtr-record-incomplete` | fail | 1 |
| `dtr-tension-id` | pass | 0 |
| `dtr-rejected-form` | pass | 0 |
| `expected-sacrifice-unmapped` | pass | 0 |
