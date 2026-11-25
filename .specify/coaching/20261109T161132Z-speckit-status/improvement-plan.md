# Improvement plan — /speckit.status

**Run**: `20261109T161132Z-speckit-status` · entries ordered by priority; each names a Trainee file and a
concrete tweak, with the finding it cites.

## Entries

| # | Trainee file / section | Tweak | Evidence |
|---|---|---|---|
| P-1 | `.specify/scripts/python/status-digest.py` — digest header line | Add the **resolved registry directory** to the `generated_at=… cap=… profile=…` header (one extra `registry=<dir>` field), so a reader can tell which registry produced the line set without re-deriving the resolution order. The Trainee itself recorded this as a feedback optimization point. | D-O2 (verbatim digest header), return §4.3 |
| P-2 | `templates/commands/status.md` — § Wrap-up / § Close-out | State explicitly that a record-only run has no requirement number, so the closeout's `ask` branch SHOULD offer a `run-<run_id>` branch-name default instead of leaving `<feature-branch>` as an open input. | D-O5, return §5 (open input `<feature-branch>`) |

## Run Status

- `run: success` — the Trainee's real work completed end-to-end; the primary artifact (the digest
  invocation record with exit 0) exists; the closeout stop is the command's own `ask` contract.
- `optimization: skipped` — P-1 is already captured as a feedback entry by the Trainee itself
  (`.specify/memory/feedback/20261109T161409Z-speckit-status.md`), and P-2 is a wording tweak that does not
  justify a separate `improve-skills` dispatch in this run; both stand for the next improvement batch.
  Skipping optimization does not change the execution verdict.
