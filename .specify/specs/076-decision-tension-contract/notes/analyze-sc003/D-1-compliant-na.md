# SC-003 analyze snapshot — D-1-compliant-na

- fixture: trivial plan: N/A plus one line per trigger
- judged artifact: `plan.md` under `REQUIREMENTS_DIR` (the channel's only object; `requirements.md` is the mapping reference, never a second judged object)
- validator: `scripts/python/validate-decision-tensions.py --spec <fixture> --json`
- channel: value_domain=HIGH-or-0 — printed by the program; every label is HIGH when it fires and 0 when it does not (no advisory or downgrade tier)
- exit_code: 0
- records: 0
- HIGH findings: 0

| label | status | count | severity |
|---|---|---|---|
| `dtr-anchor` | pass | 0 | 0 |
| `dtr-section-missing` | pass | 0 | 0 |
| `dtr-record-incomplete` | pass | 0 | 0 |
| `dtr-tension-id` | pass | 0 | 0 |
| `dtr-rejected-form` | pass | 0 | 0 |
| `expected-sacrifice-unmapped` | pass | 0 | 0 |
