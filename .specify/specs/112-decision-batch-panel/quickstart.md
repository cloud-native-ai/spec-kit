# Quickstart — Batch Decision Panel（批量决策面板）

The mechanism's documented surfaces are one command `/speckit.decide`, one internal skill `decide-batch` and one engine `python3 .specify/scripts/python/decision-batch.py` (framework source `scripts/python/decision-batch.py`). The engine is an implementation output of this feature: every example that invokes it is **not executable at plan time** and is **pinned by the named contract test**, with its premises listed so the next stages can re-measure instead of inherit. Examples over existing engines were executed on 2026-11-27; their measured output is quoted. Full captures live at `test-evidence/plan-stage-2026-11-27.md`.

## Scenario 1 — Inspect the pending sources (executed 2026-11-27)

```bash
awk -F'|' '$2 ~ /^ *(OI-|D-)/ && $5 ~ /^ *open([[:space:],，（(]|$)/ {n++} END{print n+0}' .specify/register.md
```

Measured: `17` — the register-derived candidate population (research M-1).

```bash
grep -rE '^### PENDING —' .specify/specs .specify/goals .specify/anchoring .specify/teams | wc -l
```

Measured: `0` — no authored pending-item block exists yet, so the first batch presents all 17 rows `incomplete` and settles nothing (research M-2, A-16).

```bash
python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:112-decision-batch-panel"
```

Measured: `flow_class: execution`, `flow_type: -`, `source: declaration`, rc 0.

## Scenario 2 — One complete presentation (pinned)

```bash
python3 scripts/python/decision-batch.py scan --workspace-root . --format text
```

The expected result shape (not executable yet — the engine is an implementation output of this feature):

- a batch-level context block stating why the items appear now, what silence will mean, how to object or park, which items stay pending and why, and the completeness disclosure;
- **17** item rows in deterministic order, each `incomplete` with named reasons (`class-missing`, `authority-unresolved`) and no invented slot value;
- bookkeeping: `candidates = presented rows + merged references + named exclusions` with per-source counts, and the verdict `complete` (all sources read, zero absent);
- zero `ai-autonomous` presentations; zero batch records written.

**Pin**: `tests/unit/test_decision_batch_engine.py::test_row_slots_incomplete_named`,
`::test_bookkeeping_identity_holds`, `::test_presentation_order_deterministic`.
**Premises**: engine path and action names of C-608; the register predicate of C-101; the qualification precedence of data-model § 2; the four scan roots existing while containing zero blocks.

## Scenario 3 — Object only, record the batch (pinned)

On a fixture workspace under `.specify/.tmp/decide-demo/` (sanctioned temp root, git-ignored), with one complete `human-interactive` item, one `irreversible-default` item and one `ai-autonomous` item:

```bash
python3 scripts/python/decision-batch.py scan --workspace-root .specify/.tmp/decide-demo --format json > .specify/.tmp/decide-demo/scan.json
python3 scripts/python/decision-batch.py record \
  --workspace-root .specify/.tmp/decide-demo \
  --presentation .specify/.tmp/decide-demo/scan.json \
  --reply .specify/.tmp/decide-demo/reply.md \
  --authorization interactive
```

The reply file carries the user's exact text plus structured entries bound by item identity:

```text
reply_verbatim: |
  只对「<item A 的完整名称>」改为「<另一具名选项>」，其余没意见。
objections:
  - subject: <item A 的完整名称>
    action: alternative
    option_label: <另一具名选项>
no_objections: false
```

Expected result: exit 0; one batch record titled `decision-batch-<B-id>` in `<workspace>/.specify/knowledge/`; the complete reversible item settled `accepted-default`; the named item `objected-alternative`; the `irreversible-default` and the `ai-autonomous` candidates not settled (the former stays pending with its reason, the latter excluded `not-human-held`); register rows and the block `resolution` annotation updated; a same-id second `record` refused before any write.

**Pin**: `tests/unit/test_decision_batch_engine.py::test_silence_eligibility_matrix`,
`::test_reply_membership_refusals`, `::test_batch_record_layout_via_memory_engine`,
`::test_batch_id_shape_and_duplicate_refusal`.
**Premises**: the reply-file grammar above; `record`'s closed flags (C-608); the batch-id shape (C-502); the mapping of dispositions to choice signals (C-408); the memory engine's knowledge scope and upsert-by-slug (research M-6) — create-only is enforced by the batch engine, not the memory engine.

**Teardown (verified by the same pin)**: `rm -rf .specify/.tmp/decide-demo` — the scenario leaves no state outside the temp root.

## Scenario 4 — Replay the batch from the record alone (pinned)

```bash
python3 scripts/python/decision-batch.py replay \
  --workspace-root .specify/.tmp/decide-demo \
  --batch .specify/.tmp/decide-demo/.specify/knowledge/decision-batch-<B-id>.md
```

Expected result: exit 0; item set, completeness bookkeeping, defaults/grounding, objections/dispositions and decision records reproduced from the record and resolvable pointers only. Corrupt one evidence pointer in a copy of the record → replay exits non-zero and names the pointer.

**Pin**: `tests/unit/test_decision_batch_engine.py::test_replay_from_record_only`,
`::test_replay_broken_pointer_nonzero`.
**Premises**: replay is read-only (C-508); "resolvable" uses the same reading as the decision checker's evidence rule (path exists; anchor findable).

## Scenario 5 — Refusal and honest emptiness (pinned)

- A `register.md` that exists but cannot be parsed by columns → `scan` exits `1`, names the source, presents nothing and writes nothing.
- A scan root that does not exist → recorded as a named absent empty source; the verdict stays complete-with-disclosure.
- A tree with zero candidates → `scan` exits `0` with an explicit `nothing-pending` result and creates no batch record.

**Pin**: `tests/unit/test_decision_batch_engine.py::test_unreadable_source_refusal`,
`::test_absent_source_named_not_clean`, `::test_nothing_pending_success_no_record`.
**Premises**: presence levels of C-109; the exit-code set of C-608.

## Scenario 6 — Inspect recorded batches (executed 2026-11-27)

```bash
ls .specify/knowledge/ | grep '^decision-batch-' | wc -l
```

Measured: `0` — no batch has been recorded on this tree yet. After Scenario 3 the same command lists one file per batch (the record's title carries the batch id, so two batches never share a path).

## Scenario 7 — Maintainer verification (pinned)

```bash
python3 scripts/python/validate-decisions.py --action records --carrier <batch record path>
```

Expected at implementation: exit 0 over the batch record — every `### D-NNN` block passes the 107 grammar, and the three batch-family fields pass their trigger/value rule.

```bash
bash scripts/bash/run-tests.sh tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q
```

Expected at implementation: exit 0 through the single test entry. **Not run at plan time**: this worktree carries no pytest interpreter (the runner reports `no interpreter with pytest found`; research M-14), and this stage changes documentation only.

**Pin**: `tests/contract/test_decision_batch_contract.py::test_engine_interface_contract`,
`test_decision_governance_guards.py` (batch M rows and reverse samples).
**Premises**: the validator's field closure admits the batch family (C-504, research M-5); the guard roster moves with the owner page (table–guard parity); the runner's ladder resolves an interpreter with pytest in the implementation environment.